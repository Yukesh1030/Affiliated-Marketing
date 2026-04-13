from PIL import Image
import os

src = r"d:\yukesh\projects\Affiliated Marketing\asset\hw_hero_bg.jpg"
dst = r"d:\yukesh\projects\Affiliated Marketing\asset\hw_hero_bg.webp"

img = Image.open(src).convert('RGB')
min_kb = 70 * 1024
max_kb = 90 * 1024

found = False
for scale in [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]:
    w, h = img.size
    resized = img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
    for q in range(98, 5, -1):
        resized.save(dst, "WEBP", quality=q)
        size = os.path.getsize(dst)
        if min_kb <= size <= max_kb:
            print(f"Fixed: {size/1024:.2f} KB at scale {scale}, quality {q}")
            found = True
            break
    if found: break

if not found:
    print("Failed to find a suitable size in range.")
