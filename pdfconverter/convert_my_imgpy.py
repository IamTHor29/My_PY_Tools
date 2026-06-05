#!/usr/bin/env python3

from pathlib import Path
from PIL import Image
import argparse
import fitz  # PyMuPDF


# =========================================================
#   SUPPORTED FORMATS
# =========================================================

SUPPORTED_IMAGE_INPUTS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
    ".gif",
    ".tiff",
    ".tif",
}

SUPPORTED_OUTPUTS = {
    "jpg",
    "jpeg",
    "png",
    "webp",
}


# =========================================================
#   HELPERS
# =========================================================

def normalize_format(fmt: str) -> str:
    fmt = fmt.lower().replace(".", "")

    if fmt == "jpg":
        return "jpeg"

    return fmt


def output_extension(fmt: str) -> str:
    if fmt == "jpeg":
        return ".jpg"

    return f".{fmt}"


def is_image(path: Path) -> bool:
    return path.suffix.lower() in SUPPORTED_IMAGE_INPUTS


def is_pdf(path: Path) -> bool:
    return path.suffix.lower() == ".pdf"


def get_files(source: Path, recursive: bool) -> list[Path]:
    if source.is_file():
        return [source]

    pattern = "**/*" if recursive else "*"

    files = []

    for item in source.glob(pattern):
        if not item.is_file():
            continue

        if item.name.startswith("."):
            continue

        if is_pdf(item) or is_image(item):
            files.append(item)

    return files


# =========================================================
#   PDF TO IMAGE
# =========================================================

def convert_pdf_to_images(
    pdf_path: Path,
    source: Path,
    output_folder: Path,
    dpi: int,
    image_format: str,
    start_page: int | None,
    end_page: int | None,
    dry_run: bool
) -> None:
    try:
        document = fitz.open(pdf_path)
    except Exception as error:
        print(f"Failed to open PDF: {pdf_path}")
        print(error)
        return

    page_count = document.page_count

    start = start_page if start_page else 1
    end = end_page if end_page else page_count

    start = max(1, start)
    end = min(page_count, end)

    if start > end:
        print(f"Invalid page range for {pdf_path.name}")
        document.close()
        return

    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)

    if source.is_file():
        relative_parent = Path("")
    else:
        relative_parent = pdf_path.relative_to(source).parent

    pdf_output_folder = output_folder / relative_parent / pdf_path.stem

    print(f"\nPDF: {pdf_path}")
    print(f"Pages: {start} to {end}")
    print(f"DPI: {dpi}")
    print(f"Output: {pdf_output_folder}")

    if dry_run:
        print("Dry run only. No PNG files created.")
        document.close()
        return

    pdf_output_folder.mkdir(parents=True, exist_ok=True)

    for page_number in range(start, end + 1):
        page = document.load_page(page_number - 1)
        pix = page.get_pixmap(matrix=matrix, alpha=False)

        output_path = pdf_output_folder / f"{pdf_path.stem}_page_{page_number:03d}.{image_format}"

        if image_format == "png":
            pix.save(output_path)
        else:
            temp_png = pdf_output_folder / f"__temp_page_{page_number:03d}.png"
            pix.save(temp_png)

            with Image.open(temp_png) as img:
                img.save(output_path, format=image_format.upper(), quality=95, optimize=True)

            temp_png.unlink()

        print(f"Created: {output_path}")

    document.close()


# =========================================================
#   IMAGE TO IMAGE
# =========================================================

def resize_image(
    image: Image.Image,
    max_width: int | None,
    max_height: int | None
) -> Image.Image:
    if not max_width and not max_height:
        return image

    width, height = image.size

    if max_width and width > max_width:
        ratio = max_width / width
        width = max_width
        height = int(height * ratio)

    if max_height and height > max_height:
        ratio = max_height / height
        height = max_height
        width = int(width * ratio)

    return image.resize((width, height), Image.Resampling.LANCZOS)


def prepare_image_for_format(image: Image.Image, image_format: str) -> Image.Image:
    if image_format == "jpeg":
        if image.mode in ("RGBA", "LA", "P"):
            background = Image.new("RGB", image.size, "white")

            if image.mode == "P":
                image = image.convert("RGBA")

            if image.mode in ("RGBA", "LA"):
                background.paste(image, mask=image.split()[-1])
            else:
                background.paste(image)

            return background

        return image.convert("RGB")

    return image


def convert_image_to_image(
    image_path: Path,
    source: Path,
    output_folder: Path,
    image_format: str,
    quality: int,
    max_width: int | None,
    max_height: int | None,
    dry_run: bool
) -> None:
    extension = output_extension(image_format)

    if source.is_file():
        output_path = output_folder / f"{image_path.stem}{extension}"
    else:
        relative_path = image_path.relative_to(source)
        output_path = output_folder / relative_path.with_suffix(extension)

    print(f"{image_path} -> {output_path}")

    if dry_run:
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with Image.open(image_path) as img:
            img = resize_image(img, max_width, max_height)
            img = prepare_image_for_format(img, image_format)

            save_options = {}

            if image_format in ("jpeg", "webp"):
                save_options["quality"] = quality
                save_options["optimize"] = True

            if image_format == "png":
                save_options["optimize"] = True

            img.save(output_path, format=image_format.upper(), **save_options)

    except Exception as error:
        print(f"Failed to convert image: {image_path}")
        print(error)


# =========================================================
#   MAIN
# =========================================================

def main():
    parser = argparse.ArgumentParser(
        description="Convert PDFs to PNG/JPG/WebP and convert images between formats."
    )

    parser.add_argument(
        "source",
        help="File or folder to convert. Example: file.pdf, ~/Downloads, image.jpg"
    )

    parser.add_argument(
        "--output",
        default="converted_output",
        help="Output folder. Default: converted_output"
    )

    parser.add_argument(
        "--format",
        default="png",
        choices=["png", "jpg", "jpeg", "webp"],
        help="Output format. Default: png"
    )

    parser.add_argument(
        "--dpi",
        type=int,
        default=200,
        help="DPI for PDF conversion. Default: 200"
    )

    parser.add_argument(
        "--start-page",
        type=int,
        help="First PDF page to convert. Example: --start-page 1"
    )

    parser.add_argument(
        "--end-page",
        type=int,
        help="Last PDF page to convert. Example: --end-page 3"
    )

    parser.add_argument(
        "--quality",
        type=int,
        default=90,
        help="JPG/WebP quality from 1 to 100. Default: 90"
    )

    parser.add_argument(
        "--max-width",
        type=int,
        help="Resize image output to max width."
    )

    parser.add_argument(
        "--max-height",
        type=int,
        help="Resize image output to max height."
    )

    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Convert files inside subfolders."
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview only. Does not create files."
    )

    args = parser.parse_args()

    source = Path(args.source).expanduser().resolve()
    output_folder = Path(args.output).expanduser().resolve()
    image_format = normalize_format(args.format)

    if not source.exists():
        print(f"Source does not exist: {source}")
        return

    files = get_files(source, args.recursive)

    if not files:
        print("No supported PDF or image files found.")
        return

    print(f"Files found: {len(files)}")
    print(f"Output format: {image_format}")
    print(f"Output folder: {output_folder}")
    print(f"Dry run: {args.dry_run}")

    for file in files:
        if is_pdf(file):
            convert_pdf_to_images(
                pdf_path=file,
                source=source,
                output_folder=output_folder,
                dpi=args.dpi,
                image_format=image_format,
                start_page=args.start_page,
                end_page=args.end_page,
                dry_run=args.dry_run
            )

        elif is_image(file):
            convert_image_to_image(
                image_path=file,
                source=source,
                output_folder=output_folder,
                image_format=image_format,
                quality=args.quality,
                max_width=args.max_width,
                max_height=args.max_height,
                dry_run=args.dry_run
            )

    print("\nDone.")


if __name__ == "__main__":
    main()