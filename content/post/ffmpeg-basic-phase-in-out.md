---
title: "Minimal Post-Prod with FFmpeg"
date: 2024-08-05T18:34:39+05:30
categories: ["tooling"]
tags: ["ffmpeg"]
draft: true
---

## Context 

### The Minimal Post-Prod Requirements

My minimal post-production requirements typically involve:

* **Re-encoding:** Changing video codec and/or parameters for size/quality trade-off
* **Basic Editing:** Cutting/Joining segments, adjusting audio levels, and potentially adding a soundtrack

I am a tad too lazy to fire up a conventional media editor and I do not intend to spend time on editing content instead of other productive pursuits of mine.

### Why do I use FFmpeg?

FFmpeg offers unparalleled flexibility for audio/video manipulation. It's open-source, cross-platform, command line based, and supports virtually every codec imaginable.  

If you're post-prod is uniformly defined (I have an ending and a starting overlay), you can script it out and won't have to bother with spending time outside your preferred CLI environment.  

Getting started with FFmpeg can be daunting.  

I plan to decompose the daunts into first-principle-ish progressions so that you don't have to read the docs ([you should though](https://ffmpeg.org/ffmpeg.html)).  

## This won't be that long, Do read.

Getting right into it ...

### , Multimedia i.e Video and Audio ..

.. in the digital context, are temporally varying (in a discrete manner) tensors. This allows a computer to intuitively manipulate these interperations, that is, edit (multi)media.


### A Codec ..

.. is like a language translator for digital media.  It defines how media is compressed and decompressed when interfaced with the concerned I/O (screens, speakers, camera sensors, and microphones). Think of it as the protocol for packing and unpacking information efficiently.

* **Encoding:**  Compressing the original media into a smaller file, using compression algorithms (packing the redundancy).  

* **Decoding:** Unpacking the redundancy back into the original form for playback or editing.  

### Muxing & Demuxing ...

... are fundamental FFmpeg concepts. A video file is composed of multiple components: video, audio & subtitles.

* **Demuxing:** This is the process of separating the components from a single file. `ffmpeg` can *demux* individual streams out of a container. This lets you work on the audio and video independently.

* **Muxing:** This is the process of taking these components and combining them into a single file. You use `ffmpeg` to *mux* these components together.

### Filters in FFmpeg ..

 .. are like special effects and editing tools applied to the video and audio streams. They allow you to transform the media, adding effects, changing properties, or manipulating the data in various ways.
 
 Filters can be applied on demuxed formats on separate channels and not directly on a video file.  

Some examples:

* **Video Filters:**
    * **crop:**  Remove portions of the video frame.
    * **scale:** Resize the video, perhaps to fit a specific aspect ratio.
    * **rotate:**  Rotate the video by a specified angle.
    * **overlay:** Add another video or image on top of the original.
    * **colorkey:** Replace specific colors with transparency.

* **Audio Filters:**
    * **volume:** Adjust the overall audio volume.
    * **equalizer:**  Boost or cut specific frequency ranges.
    * **noise reduction:** Remove background noise.
    * **delay:**  Introduce a delay effect.
    * **chorus:**  Add a chorus effect.
    
### Chaining Filters ..

 .. is a powerful ffmpeg usage pattern and complex chains can allow application of elaborate effects. They are a fundamental part of FFmpeg's functionality, offering endless possibilities for video and audio manipulation.

### With FFmpeg, you can ..

* **Transcode:** Convert between formats (e.g., MP4 to AVI, WAV to MP3).
* **Edit:** Cut, trim, merge, concatenate, and apply effects.
* **Analyse:** Inspect media properties for debugging or informational purposes.
* **Stream:**  Receive and output streams over various network protocols.

Summarizing, your usual editing Ops with FFmpeg are doing the following, under the hood:

```
         ┌ ── ── ── ── ── ─┐
         │   Demux Inputs  │
         └───────┬─────────┘
                 |
           ┌─────┴───────┐
           │  Decoding   │
           └─────┬───────┘
                 |
           ┌─────┴───────┐
           │ Transforms  │
           └─────┬───────┘
                 |
           ┌─────┴───────┐
           │  Encoding   │
           └─────┬───────┘
                 |
        ┌────────┴────────┐ 
        │ Mux into Output │ 
        └─────────────────┘ 
```

* **Input (Demuxing):** The input stage involves reading the source media file (e.g., MP4, AVI, MKV) and separating its individual streams (video, audio, subtitles).
* **Decoding:** Each stream is then decoded from its compressed format (e.g., H.264, AAC) into raw data that the computer can understand.
* **Transforms (i.e. Filter Chains):**  This stage allows you to modify the media in various ways (e.g., resizing, cropping, adding watermarks, applying filters, merging streams).
* **Encoding:** The transformed data is then re-encoded back into a compressed format for output.
* **Output (Muxing):**  Finally, the encoded streams are combined into a new media file in the desired format (e.g., MP4, WebM, MKV).


## Pragmatics

Now that you have a conceptual X-Ray of FFmpeg's internals, elaborating upon one of my practical post-production scripts.

But before that, highlighting some basic convnentions:

### The Syntax
    
FFmpeg utilizes a command-line interface, adhering to the following basic syntax:

```
ffmpeg [global_options] {[input_options] -i input} ... {[output_options] output}
```

Where:  

* **`ffmpeg`**: Invokes the FFmpeg program.
* **`global_options`**: Represents options that apply globally to all input and output streams. Examples include verbosity control and logging settings.
* **`input_options`**: Encompasses options specific to the input file. This may include format demuxers.
* **`-i input`**: Designates the input source, which can be a local file, a URL, or even a hardware device.
* **`output_options`**:  Specifies options specific to the output file, such as codecs and bitrates.
* **`output`**: Defines the output destination for the processed media.


### The Scenario

I usually record videos in one go with OBS-studio with a screen capture and faceCam visual input, and microphone audio input. This is my main footage :- I usually record this in the `.mkv` format.  

I also have an intro based on my logo (a simple animation). The intro, reversed, serves as my outro. These are in `.mp4` format

My requirement is to generate an output video (I prefer `.mkv`) that has an initial phasing out overlay (not an append) and a final phasing in overlay for the intro and outro (reversed intro)  respectively over the main video.

```
[INTRO - fade out]  -->  [MAIN VIDEO]  -->  [OUTRO - fade in] 
```


### The Syntax
    
FFmpeg utilizes a command-line interface, adhering to the following basic syntax:

```
ffmpeg [global_options] {[input_options] -i input} ... {[output_options] output}
```

Where:  

* **`ffmpeg`**: Invokes the FFmpeg program.
* **`global_options`**: Represents options that apply globally to all input and output streams. Examples include verbosity control and logging settings.
* **`input_options`**: Encompasses options specific to the input file. This may include format demuxers.
* **`-i input`**: Designates the input source, which can be a local file, a URL, or even a hardware device.
* **`output_options`**:  Specifies options specific to the output file, such as codecs and bitrates.
* **`output`**: Defines the output destination for the processed media.

---------------------------------------

### Elaborate further advanced details of the syntax with audio and video channels, filter chaining, etc

Let's delve deeper into the FFmpeg syntax with a focus on audio and video channels, filter chaining, and other advanced features:

**Audio and Video Channels:**

* **Stream Specifiers**: FFmpeg uses stream specifiers to address individual audio and video channels. The format is `[stream_specifier]`, where `[stream_specifier]` can be:
    * **`-vn`**: Disable video.
    * **`-an`**: Disable audio.
    * **`-map 0:v`**: Map the video stream from the first input (index 0).
    * **`-map 1:a`**: Map the audio stream from the second input (index 1).
    * **`-map 0:v:0`**: Map the first video stream from the first input.
    * **`-map 0:a:1`**: Map the second audio stream from the first input.
    * **`-map v`**: Map all video streams (short for `-map 0:v -map 1:v ...`).
    * **`-map a`**: Map all audio streams (short for `-map 0:a -map 1:a ...`).

* **Combining Audio and Video**: You can combine audio and video streams from multiple sources:

    ```bash
    ffmpeg -i input_video.mp4 -i input_audio.mp3 -map 0:v -map 1:a -c:v copy -c:a copy output.mp4
    ```

    This command copies the video from `input_video.mp4` and the audio from `input_audio.mp3` to a new file `output.mp4`.

**Filter Chaining:**

* **Filters**: FFmpeg offers a wide range of filters for manipulating audio and video. You apply filters using the `-vf` (video filter) or `-af` (audio filter) options.
* **Filter Graphs**: Filters can be chained together using a simple syntax:

    ```bash
    ffmpeg -i input.mp4 -vf "scale=1280:720,fps=25" -c:v libx264 output.mp4 
    ```

    This command scales the video to 1280x720 resolution and sets the frame rate to 25fps.
* **Filter Complexities**: You can create more complex filter graphs with multiple filters and branches. For instance, to resize, crop, and overlay a watermark:

    ```bash
    ffmpeg -i input.mp4 -i watermark.png -filter_complex "[0:v]scale=1280:720[scaled];[scaled]crop=1000:600[cropped];[cropped][1:v]overlay=10:10[out]" -map "[out]" -c:v libx264 output.mp4
    ```

**Examples:**

* **Audio Processing:**

    ```bash
    # Normalize audio to -3dB
    ffmpeg -i input.mp3 -af "volume=-3dB" output.mp3

    # Convert audio to 44.1kHz
    ffmpeg -i input.wav -ar 44100 -c:a libopus output.opus 
    ```

* **Video Processing:**

    ```bash
    # Rotate video by 90 degrees clockwise
    ffmpeg -i input.mp4 -vf "transpose=1" output.mp4

    # Apply a Gaussian blur
    ffmpeg -i input.mp4 -vf "gaussianblur=sigma=10" output.mp4
    ```

* **Combining Audio and Video Filters:**

    ```bash
    ffmpeg -i input.mp4 -vf "scale=1280:720" -af "equalizer=f=500:width_type=h:width=100:gain=10" output.mp4
    ```

    This command resizes the video and applies an equalizer to boost the 500Hz frequency in the audio.

**Key Points:**

* **Filter Documentation**: Refer to the FFmpeg documentation ([https://ffmpeg.org/ffmpeg-filters.html](https://ffmpeg.org/ffmpeg-filters.html)) for a comprehensive list of filters and their options.
* **Filter Graphs**: Experiment with different filter graphs to achieve the desired effects.
* **Efficiency**: For complex operations, consider utilizing dedicated video editing software for improved workflow and visual feedback.

