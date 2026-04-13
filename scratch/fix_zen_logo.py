from PIL import Image
import os

src = r"d:\yukesh\projects\Affiliated Marketing\asset\logo_zen_fitness.png"
dst = r"d:\yukesh\projects\Affiliated Marketing\asset\logo_zen_fitness.webp"

img = Image.open(src)
if img.mode != 'RGB':
    img = img.convert('RGB')

for scale in [1.5, 1.2, 1.1, 1.3, 1.4]:
    w, h = img.size
    resized = img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
    for q in range(100, 50, -2):
        resized.save(dst, "WEBP", quality=q)
        size = os.path.getsize(dst)
        if 70 * 1024 <= size <= 90 * 1024:
            print(f"Fixed! Size: {size/1024:.2f} KB at scale {scale}, Q {q}")
            exit(0)
print("Could not fix automatically")
