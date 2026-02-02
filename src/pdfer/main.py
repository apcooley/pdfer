#!/usr/bin/env python3
"""Main CLI script for pdfer - converts images in a folder to a PDF."""

import argparse
import sys
from pathlib import Path
from typing import Dict, List

import img2pdf
import yaml


# Supported image extensions (case-insensitive)
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".webp", ".bmp"}


def load_config(config_path: Path) -> Dict[str, str]:
    """
    Load configuration from YAML file.

    Args:
        config_path: Path to the config file

    Returns:
        Dictionary with configuration values (source_dir, target_dir)
    """
    default_config = {"source_dir": ".", "target_dir": "."}

    if not config_path.exists():
        return default_config

    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f) or {}

        # Merge with defaults
        return {**default_config, **config}
    except Exception:
        # If config file is invalid, return defaults
        return default_config


def find_images(folder_path: Path) -> List[Path]:
    """
    Find all supported images in the folder (non-recursive).

    Args:
        folder_path: Path to the folder to search

    Returns:
        List of image file paths sorted alphabetically
    """
    images = []

    for file_path in folder_path.iterdir():
        if file_path.is_file():
            if file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                images.append(file_path)

    # Sort alphabetically by filename
    return sorted(images, key=lambda p: p.name)


def convert_images_to_pdf(image_paths: List[Path], output_path: Path) -> None:
    """
    Convert a list of images to a single PDF file.

    Args:
        image_paths: List of paths to image files
        output_path: Path where the PDF should be saved

    Raises:
        img2pdf.ImageOpenError: If an image cannot be opened
        PermissionError: If output file cannot be written
    """
    # Convert Path objects to strings for img2pdf
    image_paths_str = [str(p) for p in image_paths]

    # Convert images to PDF
    pdf_bytes = img2pdf.convert(image_paths_str)

    # Write to output file
    with open(output_path, "wb") as f:
        f.write(pdf_bytes)


def main() -> int:
    """
    Main entry point for the CLI.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        description="Convert all images in a folder to a single PDF file.",
        epilog=f"Supported formats: {', '.join(sorted(SUPPORTED_EXTENSIONS))}",
    )

    parser.add_argument(
        "folder",
        type=str,
        nargs="?",
        help="Folder name or path (relative to source_dir in config.yaml, or absolute path)",
    )

    parser.add_argument(
        "output",
        type=str,
        nargs="?",
        help="Output PDF filename (default: <folder_name>.pdf in target_dir from config.yaml)",
    )

    args = parser.parse_args()

    # Load configuration
    config_path = Path("config.yaml")
    config = load_config(config_path)

    # Determine source folder
    if args.folder:
        folder_arg = Path(args.folder)
        # If absolute path, use as-is; otherwise relative to source_dir
        if folder_arg.is_absolute():
            folder_path = folder_arg
        else:
            source_base = Path(config["source_dir"])
            folder_path = source_base / folder_arg
    else:
        # If no folder argument, use source_dir itself
        folder_path = Path(config["source_dir"])

    if not folder_path.exists():
        print(f"Error: Folder '{folder_path}' does not exist", file=sys.stderr)
        return 1

    if not folder_path.is_dir():
        print(f"Error: '{folder_path}' is not a directory", file=sys.stderr)
        return 1

    # Find images
    try:
        image_paths = find_images(folder_path)
    except PermissionError:
        print(
            f"Error: Permission denied when reading folder '{folder_path}'",
            file=sys.stderr,
        )
        return 1

    # Check if any images were found
    if not image_paths:
        print(f"Error: No supported images found in '{folder_path}'", file=sys.stderr)
        print(
            f"Supported formats: {', '.join(sorted(SUPPORTED_EXTENSIONS))}",
            file=sys.stderr,
        )
        return 1

    print(f"Found {len(image_paths)} image(s):")
    for img_path in image_paths:
        print(f"  - {img_path.name}")

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        # Default to <folder_name>.pdf in target_dir
        target_dir = Path(config["target_dir"])
        # Use the original folder argument name if provided, otherwise use the folder_path name
        if args.folder:
            folder_name = Path(args.folder).name
        else:
            folder_name = folder_path.resolve().name
        output_filename = f"{folder_name}.pdf"
        output_path = target_dir / output_filename
    try:
        convert_images_to_pdf(image_paths, output_path)
        print(f"\nSuccessfully created PDF: {output_path}")
        return 0
    except PermissionError:
        print(
            f"Error: Permission denied when writing to '{output_path}'", file=sys.stderr
        )
        return 1
    except Exception as e:
        print(f"Error converting images to PDF: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
