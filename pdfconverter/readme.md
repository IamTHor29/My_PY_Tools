Copy and paste this into `README.md`:

````markdown
# Convert My ImgPy

A simple Python command-line tool to convert PDFs and images.

The main goal of this tool is to convert PDF files into PNG images, especially when you receive files as PDFs and need them as image files.

It can also convert normal image files between formats like PNG, JPG, JPEG, and WebP.

## Tool File

```bash
convert_my_imgpy.py
````

## What This Tool Can Do

* Convert PDF pages to PNG
* Convert PDF pages to JPG
* Convert PDF pages to WebP
* Convert one PDF file
* Convert all PDFs inside a folder
* Convert files inside subfolders with `--recursive`
* Choose DPI quality for PDF conversion
* Convert only selected PDF pages
* Convert images between formats
* Resize image output
* Compress JPG and WebP output
* Save converted files into a separate output folder
* Preview actions with `--dry-run`

## Installation

Install the required Python packages:

```bash
pip3 install pymupdf pillow
```

## Requirements

* Python 3.10+
* PyMuPDF
* Pillow

## Basic Usage

Convert one PDF to PNG:

```bash
python3 convert_my_imgpy.py myfile.pdf
```

By default, output files are saved inside:

```bash
converted_output
```

Example output:

```text
converted_output/myfile/myfile_page_001.png
converted_output/myfile/myfile_page_002.png
converted_output/myfile/myfile_page_003.png
```

## Convert PDF to PNG

Convert a PDF using the default DPI:

```bash
python3 convert_my_imgpy.py myfile.pdf --format png
```

Convert a PDF with higher quality:

```bash
python3 convert_my_imgpy.py myfile.pdf --format png --dpi 300
```

Convert a PDF with lower file size:

```bash
python3 convert_my_imgpy.py myfile.pdf --format png --dpi 150
```

Recommended DPI:

```text
150 DPI = smaller files
200 DPI = good default
300 DPI = high quality
400 DPI = very high quality, bigger files
```

## Convert Only One Page

Convert only page 1:

```bash
python3 convert_my_imgpy.py myfile.pdf --start-page 1 --end-page 1
```

Convert only page 2:

```bash
python3 convert_my_imgpy.py myfile.pdf --start-page 2 --end-page 2
```

## Convert a Page Range

Convert pages 1 to 3:

```bash
python3 convert_my_imgpy.py myfile.pdf --start-page 1 --end-page 3
```

Convert pages 5 to 10:

```bash
python3 convert_my_imgpy.py myfile.pdf --start-page 5 --end-page 10
```

## Convert PDF to JPG

Convert PDF pages to JPG:

```bash
python3 convert_my_imgpy.py myfile.pdf --format jpg
```

Convert PDF pages to JPG with high quality:

```bash
python3 convert_my_imgpy.py myfile.pdf --format jpg --dpi 300 --quality 95
```

## Convert PDF to WebP

Convert PDF pages to WebP:

```bash
python3 convert_my_imgpy.py myfile.pdf --format webp
```

Convert PDF pages to WebP with quality setting:

```bash
python3 convert_my_imgpy.py myfile.pdf --format webp --quality 85
```

## Convert All PDFs in a Folder

Convert all supported files inside Downloads:

```bash
python3 convert_my_imgpy.py ~/Downloads
```

Convert all supported files inside Downloads and subfolders:

```bash
python3 convert_my_imgpy.py ~/Downloads --recursive
```

Convert all PDFs/images in Downloads to PNG at 300 DPI:

```bash
python3 convert_my_imgpy.py ~/Downloads --recursive --format png --dpi 300
```

## Choose Output Folder

Save converted files to a custom folder:

```bash
python3 convert_my_imgpy.py myfile.pdf --output my_converted_files
```

Convert Downloads and save output to a custom folder:

```bash
python3 convert_my_imgpy.py ~/Downloads --recursive --output converted_pdfs
```

## Convert Images Between Formats

Convert JPG to PNG:

```bash
python3 convert_my_imgpy.py image.jpg --format png
```

Convert PNG to JPG:

```bash
python3 convert_my_imgpy.py image.png --format jpg
```

Convert PNG to WebP:

```bash
python3 convert_my_imgpy.py image.png --format webp
```

Convert JPG to WebP:

```bash
python3 convert_my_imgpy.py image.jpg --format webp
```

## Resize Images

Resize output to max width of 1000 pixels:

```bash
python3 convert_my_imgpy.py image.jpg --format png --max-width 1000
```

Resize output to max height of 1000 pixels:

```bash
python3 convert_my_imgpy.py image.jpg --format png --max-height 1000
```

Resize while keeping proportions:

```bash
python3 convert_my_imgpy.py image.jpg --format webp --max-width 1200 --max-height 1200
```

## Quality Settings

Quality is used for JPG and WebP output.

Default quality:

```text
90
```

Use lower quality for smaller file size:

```bash
python3 convert_my_imgpy.py image.png --format jpg --quality 70
```

Use higher quality for better image output:

```bash
python3 convert_my_imgpy.py image.png --format jpg --quality 95
```

WebP compressed example:

```bash
python3 convert_my_imgpy.py image.png --format webp --quality 80
```

## Dry Run

Preview what will be converted without creating files:

```bash
python3 convert_my_imgpy.py myfile.pdf --dry-run
```

Preview a full folder conversion:

```bash
python3 convert_my_imgpy.py ~/Downloads --recursive --dry-run
```

## Common Commands

Convert one PDF to PNG:

```bash
python3 convert_my_imgpy.py myfile.pdf
```

Convert one PDF to high-quality PNG:

```bash
python3 convert_my_imgpy.py myfile.pdf --format png --dpi 300
```

Convert only the first page of a PDF:

```bash
python3 convert_my_imgpy.py myfile.pdf --start-page 1 --end-page 1
```

Convert all PDFs/images in Downloads:

```bash
python3 convert_my_imgpy.py ~/Downloads --recursive
```

Convert all PDFs/images in Downloads to PNG at 300 DPI:

```bash
python3 convert_my_imgpy.py ~/Downloads --recursive --format png --dpi 300
```

Convert all PDFs/images in Downloads and save to a custom folder:

```bash
python3 convert_my_imgpy.py ~/Downloads --recursive --output converted_pdfs
```

Convert PDF to JPG:

```bash
python3 convert_my_imgpy.py myfile.pdf --format jpg --dpi 300 --quality 95
```

Convert PDF to WebP:

```bash
python3 convert_my_imgpy.py myfile.pdf --format webp --dpi 300 --quality 85
```

Convert PNG to JPG:

```bash
python3 convert_my_imgpy.py image.png --format jpg
```

Convert JPG to WebP:

```bash
python3 convert_my_imgpy.py image.jpg --format webp --quality 80
```

Resize image while converting:

```bash
python3 convert_my_imgpy.py image.jpg --format png --max-width 1200
```

Preview before converting:

```bash
python3 convert_my_imgpy.py ~/Downloads --recursive --dry-run
```

## Supported Input Files

PDF files:

```text
.pdf
```

Image files:

```text
.jpg
.jpeg
.png
.webp
.bmp
.gif
.tiff
.tif
```

## Supported Output Formats

```text
.png
.jpg
.jpeg
.webp
```

## Best Workflow

For most PDF-to-PNG use cases:

```bash
python3 convert_my_imgpy.py myfile.pdf --format png --dpi 300
```

For a folder full of PDFs:

```bash
python3 convert_my_imgpy.py ~/Downloads --recursive --format png --dpi 300 --output converted_pdfs
```

For checking before converting:

```bash
python3 convert_my_imgpy.py ~/Downloads --recursive --dry-run
```

## Notes

PDF files are converted page by page.

A PDF with 5 pages will create 5 image files.

Example:

```text
invoice.pdf
```

Becomes:

```text
invoice_page_001.png
invoice_page_002.png
invoice_page_003.png
invoice_page_004.png
invoice_page_005.png
```

The tool does not overwrite your original files. Converted files are saved in the output folder.

## Troubleshooting

If you get this error:

```text
ModuleNotFoundError: No module named 'fitz'
```

Install PyMuPDF:

```bash
pip3 install pymupdf
```

If you get this error:

```text
ModuleNotFoundError: No module named 'PIL'
```

Install Pillow:

```bash
pip3 install pillow
```

Or install both:

```bash
pip3 install pymupdf pillow
```

## Why I Built This

I receive a lot of files as PDFs, but many times I need them as PNG images. This tool makes it easy to convert PDF pages into images from the terminal.

## Repo Description

A simple Python tool to convert PDFs to PNG, JPG, or WebP and convert images between formats.

## License

MIT License

Feel free to use, modify, and improve.

```
```
