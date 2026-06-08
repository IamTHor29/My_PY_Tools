#!/usr/bin/env python3
from PIL import Image
import subprocess
import sys
from pathlib import Path


def png_to_svg(input_path, output_path=None, threshold=180):
    input_path = Path(input_path)

    if not input_path.exists():
        print(f"File not found: {input_path}")
        return

    if output_path is None:
        output_path = input_path.with_suffix(".svg")
    else:
        output_path = Path(output_path)

    temp_pbm = input_path.with_suffix(".pbm")

    # Open PNG and convert to black/white bitmap
    img = Image.open(input_path).convert("L")

    # Threshold: lower = more black detail, higher = cleaner/simple shapes
    bw = img.point(lambda x: 0 if x < threshold else 255, "1")

    # Save temporary PBM for potrace
    bw.save(temp_pbm)

    try:
        subprocess.run(
            [
                "potrace",
                str(temp_pbm),
                "-s",
                "-o",
                str(output_path)
            ],
            check=True
        )

        print(f"SVG created: {output_path}")

    except FileNotFoundError:
        print("potrace is not installed. Run: brew install potrace")

    except subprocess.CalledProcessError:
        print("Error converting PNG to SVG.")

    finally:
        if temp_pbm.exists():
            temp_pbm.unlink()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("python3 png_to_svg.py input.png")
        print("python3 png_to_svg.py input.png output.svg")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) >= 3 else None

    png_to_svg(input_file, output_file)