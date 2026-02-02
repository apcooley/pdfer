# pdfer

A simple Python CLI utility that converts all images in a folder to a single PDF file.

## Features

- Converts multiple image formats to a single PDF
- Preserves image quality (lossless conversion)
- One image per page with aspect ratio preserved
- Alphabetical ordering by filename
- Simple command-line interface

## Supported Image Formats

- JPEG (`.jpg`, `.jpeg`)
- PNG (`.png`)
- TIFF (`.tiff`, `.tif`)
- WebP (`.webp`)
- BMP (`.bmp`)

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Install dependencies
uv sync
```

## Configuration

You can create a `config.yaml` file to set base directories:

```yaml
# Base source directory - folder argument is relative to this path
source_dir: C:/Users/JohnDoe/Documents/Scans/

# Target directory where PDFs are saved
target_dir: C:/Users/JohnDoe/Documents/PDF/
```

With this configuration, `uv run pdfer "Beethoven Moonlight Sonata"` will:
- Read images from: `C:/Users/JohnDoe/Documents/Scans/Beethoven Moonlight Sonata`
- Save PDF to: `C:/Users/JohnDoe/Documents/PDF/Beethoven Moonlight Sonata.pdf`

## Usage

Basic usage:

```bash
uv run pdfer [folder] [output.pdf]
```

Both arguments are optional:
- `folder`: Folder name (relative to `source_dir` in config.yaml) or absolute path. If omitted, uses `source_dir` itself.
- `output.pdf`: Output filename. If omitted, defaults to `<folder_name>.pdf` in `target_dir` from config.yaml.

### Examples

Convert all images in the `photos` folder to `album.pdf`:

```bash
uv run pdfer photos album.pdf
```

Convert images in `photos` to `photos.pdf` (using target_dir from config):

```bash
uv run pdfer photos
```

Convert images from current directory using defaults:

```bash
uv run pdfer
```

### Help

```bash
uv run pdfer --help
```

## How It Works

1. Loads configuration from `config.yaml` if present (optional)
2. Resolves the source folder (relative to `source_dir` if configured)
3. Scans the folder for supported image files (non-recursive, top-level only)
4. Sorts images alphabetically by filename
5. Converts them to a single PDF file using lossless compression
6. Saves the PDF to `target_dir` with automatic naming if output not specified
7. Each image appears on its own page with preserved aspect ratio

## Behavior Notes

- **Non-recursive**: Only scans the top-level folder, not subdirectories
- **Alphabetical ordering**: Images are sorted by filename. Rename files if you need a specific order (e.g., `001-first.jpg`, `002-second.jpg`)
- **Lossless conversion**: Uses `img2pdf` which embeds images without recompression, preserving quality
- **Error handling**: Provides clear error messages for common issues

## Common Issues

### No images found

Make sure your folder contains files with supported extensions. The tool only searches the top-level folder, not subdirectories.

### Permission denied

Ensure you have:
- Read permissions for the source folder
- Write permissions for the output directory

### Invalid image file

If an image file is corrupted or not a valid image format, the conversion will fail with an error message.

## Technical Details

- **img2pdf**: Used for lossless image-to-PDF conversion
- **Pillow**: Image processing library (dependency of img2pdf)
- **PyYAML**: Configuration file parsing
- **pathlib**: Modern Python file path handling
- **argparse**: Command-line argument parsing

## License

MIT
