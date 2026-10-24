"""Rebuild browser-compatible, responsive product images from the originals.

Optional authoring dependencies: Pillow and pillow-heif.
The deployed website does not need Python or these packages.
"""

from io import BytesIO
from pathlib import Path
from PIL import Image, ImageOps
from pillow_heif import register_heif_opener

register_heif_opener()
root = Path(__file__).resolve().parents[1] / 'images'
destination = root / 'web'
destination.mkdir(exist_ok=True)
total = 0

for source in sorted(root.iterdir()):
    if source.suffix.lower() not in {'.png', '.jpg', '.jpeg'}:
        continue
    original = ImageOps.exif_transpose(Image.open(source)).convert('RGB')
    for width, suffix in [(1000, ''), (480, '-small')]:
        # Exact widths match the HTML srcset descriptors. All source photos are
        # at least 1024px wide, so no upscaling is necessary.
        assert original.width >= width, f'Source photo is too small: {source}'
        height = round(original.height * width / original.width)
        image = original.resize((width, height), Image.Resampling.LANCZOS)
        buffer = BytesIO()
        image.save(buffer, 'WEBP', quality=84, method=6)
        encoded = buffer.getvalue()
        assert encoded, f'Encoder produced an empty file: {source}'
        with Image.open(BytesIO(encoded)) as check:
            check.load()
            assert check.width == width
        target = destination / f'{source.stem}{suffix}.webp'
        temporary = target.with_suffix('.tmp')
        temporary.write_bytes(encoded)
        temporary.replace(target)
        total += len(encoded)

print(f'Rebuilt and decoded all responsive images: {total / 1e6:.2f} MB.')
