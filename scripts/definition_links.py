"""Safe definition references shared by review cards and public pages."""
import html
import re


def definition_html(text: str) -> str:
    """Render HTTP(S) Markdown references; escape all other definition text."""
    parts, end = [], 0
    for match in re.finditer(r"\[([^\]\n]+)\]\((https?://[^\s()<>]+)\)", text):
        parts.append(html.escape(text[end:match.start()], quote=True))
        label, url = match.groups()
        parts.append(f'<a href="{html.escape(url, quote=True)}">'
                     f'{html.escape(label, quote=True)}</a>')
        end = match.end()
    parts.append(html.escape(text[end:], quote=True))
    return "".join(parts)
