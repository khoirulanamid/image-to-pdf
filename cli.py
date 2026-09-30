#!/usr/bin/env python3
"""
image_to_pdf.py — Konversi gambar ke PDF tanpa mengurangi resolusi.

Cara pakai:
  python3 image_to_pdf.py gambar.jpg
  python3 image_to_pdf.py gambar.jpg -o output.pdf
  python3 image_to_pdf.py foto1.jpg foto2.png foto3.webp -o gabungan.pdf
  python3 image_to_pdf.py /folder/gambar/ -o hasil.pdf

Format yang didukung: JPG, JPEG, PNG, WEBP, BMP, TIFF, GIF
"""

import sys
import os
import argparse
import img2pdf
from PIL import Image
from pathlib import Path

SUPPORTED = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif", ".gif"}


def collect_images(inputs: list[str]) -> list[Path]:
    """Kumpulkan semua file gambar dari argumen (file atau folder)."""
    files = []
    for inp in inputs:
        p = Path(inp)
        if p.is_dir():
            found = sorted([
                f for f in p.iterdir()
                if f.suffix.lower() in SUPPORTED
            ])
            if not found:
                print(f"[!] Tidak ada gambar ditemukan di folder: {p}")
            files.extend(found)
        elif p.is_file():
            if p.suffix.lower() in SUPPORTED:
                files.append(p)
            else:
                print(f"[!] Format tidak didukung, dilewati: {p.name}")
        else:
            print(f"[!] File/folder tidak ditemukan: {inp}")
    return files


def convert_to_rgb_png(img_path: Path, tmp_dir: Path) -> Path:
    """
    Konversi gambar non-JPG/non-PNG ke PNG sementara agar img2pdf bisa membacanya.
    Khusus WEBP, BMP, GIF, TIFF — disimpan sementara sebagai PNG lossless.
    """
    img = Image.open(img_path)
    # Jika ada alpha channel (RGBA), composite ke putih agar PDF tidak rusak
    if img.mode in ("RGBA", "LA", "P"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
        img = background
    elif img.mode != "RGB":
        img = img.convert("RGB")

    tmp_path = tmp_dir / (img_path.stem + "_tmp.png")
    img.save(tmp_path, format="PNG", compress_level=0)  # lossless, no compression
    return tmp_path


def main():
    parser = argparse.ArgumentParser(
        description="Konversi gambar ke PDF — tanpa mengurangi resolusi (lossless)."
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="File gambar atau folder yang berisi gambar."
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Nama file PDF output (default: output.pdf)"
    )
    args = parser.parse_args()

    # --- Kumpulkan file gambar ---
    images = collect_images(args.inputs)
    if not images:
        print("[✗] Tidak ada gambar valid untuk dikonversi.")
        sys.exit(1)

    print(f"[✓] Ditemukan {len(images)} gambar:")
    for img in images:
        print(f"    • {img.name}")

    # --- Tentukan nama output ---
    if args.output:
        output_path = Path(args.output)
    else:
        # Default: nama sama dengan gambar pertama, ekstensi .pdf
        output_path = images[0].with_suffix(".pdf")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # --- Siapkan folder temp untuk konversi format ---
    tmp_dir = Path("/tmp/img2pdf_tmp")
    tmp_dir.mkdir(exist_ok=True)
    tmp_files = []

    try:
        ready_images = []
        for img_path in images:
            ext = img_path.suffix.lower()
            if ext in {".jpg", ".jpeg", ".png"}:
                # JPG dan PNG langsung diproses img2pdf (zero re-encoding)
                ready_images.append(str(img_path))
            else:
                # WEBP, BMP, TIFF, GIF — konversi ke PNG lossless sementara
                print(f"    → Mengkonversi {img_path.name} ke PNG sementara...")
                tmp_path = convert_to_rgb_png(img_path, tmp_dir)
                tmp_files.append(tmp_path)
                ready_images.append(str(tmp_path))

        # --- Konversi ke PDF menggunakan img2pdf (lossless, tidak re-encode JPEG) ---
        print(f"\n[⏳] Membuat PDF...")
        with open(output_path, "wb") as pdf_file:
            pdf_file.write(img2pdf.convert(ready_images))

        # --- Verifikasi hasil ---
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"\n[✓] PDF berhasil dibuat!")
        print(f"    File  : {output_path.resolve()}")
        print(f"    Ukuran: {size_mb:.2f} MB")
        print(f"    Halaman: {len(images)} halaman")

    finally:
        # --- Bersihkan file sementara ---
        for tmp in tmp_files:
            if tmp.exists():
                tmp.unlink()
        if tmp_dir.exists():
            try:
                tmp_dir.rmdir()
            except OSError:
                pass


if __name__ == "__main__":
    main()
