# PNG to SVG Converter

Simple Python tool that converts PNG images into SVG vector files using Potrace.

---

# Features

* Convert PNG images to SVG
* Works great for:

  * Logos
  * Frames
  * Icons
  * Black & white graphics
  * Line art
* Local/offline conversion
* Clean vector output
* Canva-compatible SVG export

---

# Requirements

## macOS

Install Potrace:

```bash
brew install potrace
```

Install Python dependencies:

```bash
pip3 install pillow
```

---

# Usage

## Convert PNG to SVG

```bash
python3 png_to_svg.py input.png
```

Example:

```bash
python3 png_to_svg.py frames.png
```

Output:

```bash
frames.svg
```

---

## Custom Output Name

```bash
python3 png_to_svg.py input.png output.svg
```

Example:

```bash
python3 png_to_svg.py logo.png neon_logo.svg
```

---

# Best Results

For clean SVG vectors:

* Use black shapes/lines
* Use white or transparent backgrounds
* High contrast images work best
* Avoid shadows and glow effects before converting
* Thicker lines produce cleaner vectors

---

# Canva Support

After generating the SVG:

1. Upload the SVG to Canva
2. Click the graphic
3. Change colors directly from the top toolbar
4. Resize infinitely without losing quality

---

# Troubleshooting

## Error: `potrace is not installed`

Run:

```bash
brew install potrace
```

---

## SVG Looks Jagged

Try:

* Higher resolution PNG
* Cleaner black lines
* Simpler artwork
* Removing gradients/shadows

---

# Recommended Uses

* Neon sign mockups
* CNC cutting templates
* Laser engraving
* Acrylic signs
* Logo vectorization
* Sticker outlines
* Frame templates

---

# Example Workflow

```bash
python3 png_to_svg.py frames.png
```

Then:

* Upload SVG into Canva
* Change frame colors
* Add neon text/glow
* Export final mockup

---

# License

Free to use and modify.
