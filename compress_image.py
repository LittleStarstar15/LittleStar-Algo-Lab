"""Compress LittleStar.png to ~100KB. Output: LittleStar.jpg"""
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    import subprocess
    subprocess.run(["py", "-m", "pip", "install", "Pillow", "-q"], check=True)
    from PIL import Image

SRC = Path(__file__).parent / "assets" / "images" / "LittleStar.png"
DEST = Path(__file__).parent / "assets" / "images" / "LittleStar.jpg"
TARGET_B = 100 * 1024

def main():
    img = Image.open(SRC)
    print(f"Original: {SRC.stat().st_size / 1024:.1f} KB, {img.size[0]}x{img.size[1]}")

    if img.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        if img.mode == "RGBA":
            bg.paste(img, mask=img.split()[-1])
        else:
            bg.paste(img)
        img = bg
    elif img.mode != "RGB":
        img = img.convert("RGB")

    lo, hi = 20, 85
    for _ in range(10):
        q = (lo + hi) // 2
        img.save(DEST, "JPEG", quality=q, optimize=True)
        s = DEST.stat().st_size
        if TARGET_B * 0.8 <= s <= TARGET_B * 1.2:
            break
        if s > TARGET_B:
            hi = q - 1
        else:
            lo = q + 1

    s = DEST.stat().st_size
    if s > TARGET_B * 1.5:
        scale = (TARGET_B / s) ** 0.5
        w, h = img.size
        img = img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
        for q in range(70, 35, -5):
            img.save(DEST, "JPEG", quality=q, optimize=True)
            if DEST.stat().st_size <= TARGET_B * 1.2:
                break

    print(f"Compressed: {DEST.name} = {DEST.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    main()
