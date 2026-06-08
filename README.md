# My_PY_Tools
# My_PY_Tools

A collection of useful Python command-line tools for file conversion, vector generation, file cleanup, and automation.

Built for real-world workflows like:

* Organizing messy folders
* Converting PDFs to images
* Creating SVG vectors
* Cleaning storage space
* Automating repetitive file tasks

---

# Tools Included

## PNG to SVG Converter

Convert PNG images into SVG vector files using Potrace.

### Features

* PNG → SVG conversion
* Great for:

  * Logos
  * Frames
  * Icons
  * Black & white graphics
  * CNC/Laser templates
* Canva-compatible SVG export

---

## PDF & Image Converter

Convert PDFs into PNG/JPG/WebP images and convert images between formats.

### Features

* PDF → PNG/JPG/WebP
* Image → PNG/JPG/WebP
* Batch conversion
* Recursive folder conversion
* Resize output images
* Adjustable quality and DPI
* Page range selection
* Dry-run preview mode

---

## Smart File Cleaner

Analyze and organize folders safely.

### Features

* File reports
* Find large files
* Find old files
* Detect duplicate files
* ZIP files by date
* Safe Trash deletion
* Permanent delete mode
* Storage cleanup utilities

---

# Installation

Clone the repository:

```bash
git clone https://github.com/YOURUSERNAME/My_PY_Tools.git
cd My_PY_Tools
```

Install Python requirements:

```bash
pip3 install -r requirements.txt
```

Install Potrace (required for PNG to SVG):

```bash
brew install potrace
```

---

# requirements.txt

```txt
pillow
pymupdf
send2trash
```

---

# Usage

## PNG to SVG

```bash
python3 pngtosvg/png_to_svg.py image.png
```

---

## PDF Converter

```bash
python3 pdfconverter/convert_my_imgpy.py file.pdf
```

---

## Smart File Cleaner

```bash
python3 file_executor/smart_file_cleaner.py ~/Downloads --report
```

---

# Project Structure

```bash
My_PY_Tools/
│
├── file_executor/
│   ├── smart_file_cleaner.py
│   └── README.md
│
├── pdfconverter/
│   ├── convert_my_imgpy.py
│   └── README.md
│
├── pngtosvg/
│   ├── png_to_svg.py
│   └── README.md
│
├── requirements.txt
└── README.md
```

---

# Why I Built This

I constantly needed small utilities for:

* converting customer files
* organizing downloads
* generating vectors
* cleaning storage
* automating repetitive tasks

So I started building reusable Python tools instead of repeating the same manual workflows.

---

# Future Plans

* Auto installer
* AI-powered file organization
* OCR utilities
* Batch image processing
* Cross-platform support

---

# License

MIT License

Free to use, modify, and improve.
