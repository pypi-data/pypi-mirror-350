# Image Generation with FlowAI

FlowAI can generate images using Google's Gemini models. This guide explains how to use the image generation feature.

## Basic Image Generation

To generate an image, use the `--create-image` flag with a text prompt:

```bash
flowai --create-image "A futuristic spaceship hovering over the surface of Mars"
```

This will:
1. Use Google's Gemini model to generate an image based on your prompt
2. Save the image to a temporary file
3. Display the path to the saved image
4. Automatically open the image in your default image viewer

## Using Reference Images

You can provide a reference image to guide the generation, which can help achieve more consistent styles or include specific elements:

```bash
flowai --create-image "A futuristic spaceship hovering over the surface of Mars" --reference-image path/to/your/image.jpg
```

Alternatively, you can copy an image to your clipboard and use it as a reference:

```bash
flowai --create-image "A futuristic spaceship hovering over the surface of Mars" --reference-from-clipboard
```

> **Note:** Specifying either `--reference-image` or `--reference-from-clipboard` will automatically enable image generation mode even without explicitly using the `--create-image` flag. This means the following commands will work as expected:
>
> ```bash
> # These commands automatically enable image generation mode
> flowai --reference-image path/to/your/image.jpg "A futuristic spaceship hovering over the surface of Mars"
> flowai --reference-from-clipboard "A futuristic spaceship hovering over the surface of Mars"
> ```

## Interactive Image Refinement

Add the `--chat` flag to enter an interactive mode where you can refine your generated images:

```bash
flowai --create-image "A futuristic spaceship hovering over the surface of Mars" --chat
```

In interactive mode, you can:
- Type refinement instructions to modify the current image
- Use `/help` to see available commands
- Use `/reference <path>` to set a new reference image for subsequent generations
- Use `/clipboard` to use an image from clipboard as a reference
- Type `/quit` to exit chat mode

### Tips for Better Refinements

When refining images, be specific about what you want to change:

- Clearly specify what elements to keep from the original image
- Use phrases like "Same exact scene but with..." for better continuity
- For small changes, use phrases like "Make a small adjustment to..."
- Reference specific parts of the image by their position or appearance

## Technical Requirements

Image generation requires:
1. A Google API key configured in your FlowAI settings
2. The PIL/Pillow Python package for image handling

## Supported Models

Currently, image generation is optimized for Google's Gemini models, specifically:
- `gemini/gemini-2.0-flash-preview-image-generation` 