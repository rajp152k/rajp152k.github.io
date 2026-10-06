#!/usr/bin/env python3
"""Maintain pinned local embeddings; checking freshness needs no inference packages."""

from __future__ import annotations

import argparse
import re
import sqlite3
from bisect import bisect_right
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path

from archive import ROOT, read_entries
from embedding_state import (
    DATABASE,
    SPEC_PATH,
    PreparedEntry,
    check_fresh,
    load_spec,
    open_database,
    pending_entries,
    prepare_entries,
    synchronize,
)

WORDS = re.compile(r"\S+")
BOUNDARIES = re.compile(r"\n[ \t]*\n+|(?<=[.!?。！？])[\"'’”\)\]]*\s+")
BATCH_SIZE = 4


@dataclass(frozen=True)
class Chunk:
    text: str
    token_count: int


def model_input(text: str, prefix: str, do_lower_case: bool) -> str:
    # Match SentenceTransformers' Transformer.tokenize, including its strip.
    value = (prefix + text).strip()
    return value.lower() if do_lower_case else value


def chunk_text(
    text: str,
    tokenizer,
    *,
    max_words: int,
    max_tokens: int,
    prefix: str = "",
    do_lower_case: bool = False,
) -> list[Chunk]:
    """Pack original contiguous slices, preferring paragraph/sentence boundaries.

    Hard splits use fast-tokenizer offsets into the original string, never token
    decoding. Every slice is retokenized with prefix and special tokens. A natural
    boundary is preferred unless it would leave a less-than-half-full chunk;
    oversized sentences/code then fill the available budget instead.
    """
    if not tokenizer.is_fast:
        raise ValueError("Lossless chunking requires a fast tokenizer with character offsets")
    if max_words <= 0 or max_tokens <= 0:
        raise ValueError("Chunk word and token budgets must be positive")
    if not text.strip():
        return []

    words = [(match.start(), match.end()) for match in WORDS.finditer(text)]
    word_ends = [end for _, end in words]
    boundaries = [match.end() for match in BOUNDARIES.finditer(text)]
    if not boundaries or boundaries[-1] != len(text):
        boundaries.append(len(text))
    prefix_words = len(WORDS.findall(prefix))
    offset_ends: list[int] | None = None

    def ids(start: int, end: int) -> list[int]:
        return tokenizer(
            model_input(text[start:end], prefix, do_lower_case),
            add_special_tokens=True,
            truncation=False,
        )["input_ids"]

    def offsets() -> list[int]:
        nonlocal offset_ends
        if offset_ends is None:
            encoded = tokenizer(
                text,
                add_special_tokens=False,
                truncation=False,
                return_offsets_mapping=True,
            )
            # Duplicate ends are intentional: byte-level tokens can share the
            # same Unicode character. Slicing at that end cannot split a codepoint.
            offset_ends = sorted(
                end for start, end in encoded["offset_mapping"] if end > start
            )
        return offset_ends

    overhead = len(
        tokenizer(
            model_input("", prefix, do_lower_case),
            add_special_tokens=True,
            truncation=False,
        )["input_ids"]
    )
    source_token_budget = max(1, max_tokens - overhead)
    chunks = []
    start = 0
    while start < len(text):
        first_word = bisect_right(word_ends, start)
        if first_word == len(words):
            # Prepared posts end in prose, but preserve trailing whitespace for
            # callers of this helper as well, without emitting an empty chunk.
            previous = chunks.pop()
            tail = previous.text + text[start:]
            tail_ids = tokenizer(
                model_input(tail, prefix, do_lower_case),
                add_special_tokens=True,
                truncation=False,
            )["input_ids"]
            if len(tail_ids) <= max_tokens:
                chunks.append(Chunk(tail, len(tail_ids)))
            else:
                chunks.append(previous)
                whitespace_ids = ids(start, len(text))
                if len(whitespace_ids) > max_tokens:
                    raise ValueError("Trailing whitespace exceeds the configured token budget")
                chunks.append(Chunk(text[start:], len(whitespace_ids)))
            break

        merges_prefix_word = bool(
            prefix and not prefix[-1].isspace() and not text[start].isspace()
        )
        word_budget = max_words - prefix_words + int(merges_prefix_word)
        if word_budget <= 0:
            raise ValueError("Embedding prefix leaves no room within max_words")
        after_words = first_word + word_budget
        word_limit = words[after_words][0] if after_words < len(words) else len(text)
        end = word_limit

        if offset_ends is not None:
            position = bisect_right(offset_ends, start) + source_token_budget - 1
            if position < len(offset_ends):
                end = min(end, offset_ends[position])
        candidate_ids = ids(start, end)
        if len(candidate_ids) > max_tokens:
            ends = offsets()
            position = bisect_right(ends, start) + source_token_budget - 1
            if position < len(ends):
                end = min(end, ends[position])
            points = sorted(
                {
                    start + 1,
                    end,
                    *ends[bisect_right(ends, start) : bisect_right(ends, end)],
                }
            )
            low, high = 0, len(points) - 1
            fitting = None
            while low <= high:
                middle = (low + high) // 2
                probe_ids = ids(start, points[middle])
                if len(probe_ids) <= max_tokens:
                    fitting = (points[middle], probe_ids)
                    low = middle + 1
                else:
                    high = middle - 1
            if fitting is None:
                raise ValueError(
                    "The configured prefix/max_tokens cannot encode even one source "
                    "character losslessly; increase max_tokens or shorten prefix"
                )
            end, candidate_ids = fitting

        # Packing the latest substantial natural boundary preserves sentence and
        # paragraph structure without making a title-only chunk before long code.
        boundary_index = bisect_right(boundaries, end) - 1
        if boundary_index >= 0 and end < len(text):
            natural_end = boundaries[boundary_index]
            if start < natural_end < end:
                natural_ids = ids(start, natural_end)
                if len(candidate_ids) / 2 <= len(natural_ids) <= max_tokens:
                    end, candidate_ids = natural_end, natural_ids

        chunk = text[start:end]
        if end <= start or not candidate_ids:
            raise ValueError("Tokenizer failed to produce a nonempty lossless chunk")
        if len(WORDS.findall(prefix + chunk)) > max_words:
            raise ValueError("Chunk exceeds the configured whitespace-delimited word budget")
        if len(candidate_ids) > max_tokens:
            raise ValueError("Chunk exceeds the configured actual model-token budget")
        chunks.append(Chunk(chunk, len(candidate_ids)))
        start = end
    return chunks


def infer_vectors(posts: list[PreparedEntry], spec: dict, device: str) -> dict[str, bytes]:
    # This function is reached only for genuinely missing/stale vectors. Checks,
    # metadata/deletion updates, and exact no-ops do not import these libraries.
    try:
        import numpy as np
        import torch
        from huggingface_hub import hf_hub_download
        from sentence_transformers import SentenceTransformer
    except ModuleNotFoundError as error:
        raise SystemExit(
            f"Embedding inference dependency missing ({error.name}). Install with "
            "python3 -m pip install -r requirements-embed.txt"
        ) from error

    if device == "auto":
        device = "mps" if torch.backends.mps.is_available() else "cpu"
    if device == "mps" and not torch.backends.mps.is_available():
        raise ValueError("MPS is unavailable in this PyTorch installation; use --device cpu")

    # Require repository-defined pooling, rather than ST's implicit mean-pooling
    # fallback for a bare Transformers model. Download failures remain real errors.
    hf_hub_download(spec["model"], "modules.json", revision=spec["revision"])
    model = SentenceTransformer(
        spec["model"],
        revision=spec["revision"],
        trust_remote_code=False,
        device=device,
        backend="torch",
        model_kwargs={"torch_dtype": torch.float32, "attn_implementation": "sdpa"},
        config_kwargs={"reference_compile": False},
    )
    model.float()
    model.eval()
    model.default_prompt_name = None
    if model.get_sentence_embedding_dimension() != spec["dimension"]:
        raise ValueError(
            f"Model embedding dimension is {model.get_sentence_embedding_dimension()}, "
            f"but embedding specification requires {spec['dimension']}"
        )
    transformer = model[0]
    tokenizer = transformer.tokenizer
    if not tokenizer.is_fast:
        raise ValueError("The configured model must provide a fast tokenizer")
    limits = [transformer.max_seq_length, tokenizer.model_max_length]
    config = transformer.auto_model.config
    if hasattr(config, "max_position_embeddings"):
        limits.append(config.max_position_embeddings)
    supported_limits = [value for value in limits if isinstance(value, int) and value > 0]
    if supported_limits and spec["max_tokens"] > min(supported_limits):
        raise ValueError(
            f"max_tokens={spec['max_tokens']} exceeds this model's supported "
            f"sequence length ({min(supported_limits)})"
        )
    if config.model_type == "modernbert" and config.reference_compile is not False:
        raise ValueError("ModernBERT reference_compile must be disabled for local inference")
    model.max_seq_length = spec["max_tokens"]
    do_lower_case = transformer.do_lower_case
    totals = {post.key: np.zeros(spec["dimension"], dtype=np.float32) for post in posts}
    weights = {post.key: 0 for post in posts}
    batch: list[tuple[str, Chunk]] = []
    chunk_count = 0

    def encode_batch() -> None:
        inputs = [spec["prefix"] + chunk.text for _, chunk in batch]
        # ST normally tokenizes with truncation enabled. Compare its actual IDs
        # against nontruncated reference IDs before allowing inference to run.
        features = model.tokenize(inputs)
        for index, (_, chunk) in enumerate(batch):
            actual = features["input_ids"][index][features["attention_mask"][index].bool()]
            expected = tokenizer(
                model_input(chunk.text, spec["prefix"], do_lower_case),
                add_special_tokens=True,
                truncation=False,
            )["input_ids"]
            if actual.tolist() != expected or len(expected) != chunk.token_count:
                raise ValueError("Model tokenization would truncate or change a prepared chunk")
        embeddings = model.encode(
            inputs,
            batch_size=BATCH_SIZE,
            device=device,
            show_progress_bar=False,
            convert_to_numpy=True,
            precision="float32",
            normalize_embeddings=False,
        )
        if embeddings.shape != (len(batch), spec["dimension"]):
            raise ValueError(f"Unexpected model embedding shape: {embeddings.shape}")
        if embeddings.dtype != np.float32 or not np.isfinite(embeddings).all():
            raise ValueError("Model returned non-finite or non-float32 embeddings")
        norms = np.linalg.norm(embeddings, axis=1)
        if not np.isfinite(norms).all() or (norms <= 0).any():
            raise ValueError("Model returned a zero or invalid chunk vector")
        embeddings /= norms[:, None]
        for (slug, chunk), vector in zip(batch, embeddings):
            totals[slug] += vector * np.float32(chunk.token_count)
            weights[slug] += chunk.token_count
        batch.clear()

    for post in posts:
        chunks = chunk_text(
            post.text,
            tokenizer,
            max_words=spec["max_words"],
            max_tokens=spec["max_tokens"],
            prefix=spec["prefix"],
            do_lower_case=do_lower_case,
        )
        if not chunks:
            raise ValueError(f"{post.key}: prepared text contains no embeddable content")
        chunk_count += len(chunks)
        for chunk in chunks:
            batch.append((post.key, chunk))
            if len(batch) == BATCH_SIZE:
                encode_batch()
    if batch:
        encode_batch()

    vectors = {}
    for slug, vector in totals.items():
        vector /= np.float32(weights[slug])
        norm = np.linalg.norm(vector)
        if not np.isfinite(norm) or norm <= 0:
            raise ValueError(f"{slug}: token-weighted mean has no finite nonzero direction")
        vector /= norm
        vectors[slug] = vector.astype("<f4", copy=False).tobytes()
    print(f"Encoded {chunk_count} chunks on {device} in float32.")
    return vectors


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check freshness without loading a model")
    parser.add_argument("--device", choices=("cpu", "mps", "auto"), default="cpu")
    parser.add_argument("--database", type=Path, default=DATABASE)
    parser.add_argument("--spec", type=Path, default=SPEC_PATH)
    parser.add_argument("--posts", type=Path, default=ROOT / "meditations")
    parser.add_argument("--logs", type=Path, default=ROOT / "logs")
    args = parser.parse_args(argv)
    try:
        spec = load_spec(args.spec)
        prepared = prepare_entries(read_entries(args.posts, args.logs), spec)
        if not args.database.exists():
            if args.check:
                parser.exit(
                    1,
                    f"Embedding database {args.database} is missing. "
                    "Run python3 scripts/embed.py to generate it "
                    "(using the same --database/--spec/--posts/--logs options).\n",
                )
            pending = prepared
        else:
            with closing(open_database(args.database)) as connection:
                if args.check:
                    check_fresh(connection, prepared, spec)
                    print(f"Embeddings are fresh for {len(prepared)} entries.")
                    return
                pending = pending_entries(connection, prepared, spec)
                if not pending:
                    try:
                        check_fresh(connection, prepared, spec)
                    except ValueError:
                        # Metadata/deletion synchronization needs no inference.
                        pass
                    else:
                        print(f"Reused {len(prepared)} embeddings; recomputed 0. Already current.")
                        return
    except (OSError, ValueError, sqlite3.Error) as error:
        parser.exit(1, f"Embedding state error: {error}\n")

    vectors = infer_vectors(pending, spec, args.device) if pending else {}
    # All inference succeeds before opening a write connection/transaction.
    # synchronize is atomic, including metadata updates and deletion pruning.
    try:
        with closing(open_database(args.database, writable=True)) as connection:
            synchronize(connection, prepared, spec, vectors)
    except (OSError, ValueError, sqlite3.Error) as error:
        parser.exit(1, f"Embedding state error: {error}\n")
    print(f"Reused {len(prepared) - len(pending)} embeddings; recomputed {len(pending)}.")


if __name__ == "__main__":
    main()
