import os
from PIL import Image

def save_with_target_size(img, path, min_kb=70, max_kb=90):
    """Save an image in WebP format attempting to hit a target size range."""
    # 1. Initial save at high quality to see baseline size
    img.save(path, "WEBP", quality=90)
    size_kb = os.path.getsize(path) / 1024
    
    if size_kb > max_kb:
        # Too large? Iterate down the quality
        for q in range(85, 10, -5):
            img.save(path, "WEBP", quality=q)
            size_kb = os.path.getsize(path) / 1024
            if size_kb <= max_kb:
                if size_kb >= min_kb:
                    return f"Compressed to {size_kb:.2f} KB (Q={q})"
                break
        
        # If still too large, resize it down
        if os.path.getsize(path) / 1024 > max_kb:
            for scale in [0.9, 0.8, 0.7, 0.6, 0.5, 0.4]:
                w, h = img.size
                img_small = img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
                for q in [90, 80, 70, 60]:
                    img_small.save(path, "WEBP", quality=q)
                    size_kb = os.path.getsize(path) / 1024
                    if size_kb <= max_kb:
                        return f"Resized & Compressed to {size_kb:.2f} KB (Scale={scale}, Q={q})"
    
    if size_kb < min_kb:
        # Too small? If it's a small icon, avoid massive upscaling, but try to bump it up a bit
        # to ensure high quality (large dimensions)
        w, h = img.size
        # Only upscale if smaller than standard desktop resolution 1920x1080 approx
        if w < 1200 or h < 1200:
            scale = (min_kb / size_kb)**0.5
            # Limit scale to reasonable amount (3.0x max)
            scale = min(scale, 3.0)
            img_large = img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
            img_large.save(path, "WEBP", quality=95)
            size_kb = os.path.getsize(path) / 1024
            return f"Upscaled to {size_kb:.2f} KB (Scale={scale:.2f})"
        else:
            # Already large dimensions, just max out quality
            img.save(path, "WEBP", quality=100)
            size_kb = os.path.getsize(path) / 1024
            return f"Max quality saved at {size_kb:.2f} KB"

    return f"Saved at {size_kb:.2f} KB (no adjustments needed)"

asset_dir = r"d:\yukesh\projects\Affiliated Marketing\asset"
image_exts = (".png", ".jpg", ".jpeg", ".bmp", ".webp")

files = [f for f in os.listdir(asset_dir) if f.lower().endswith(image_exts)]
results = []

for filename in files:
    filepath = os.path.join(asset_dir, filename)
    base_name = os.path.splitext(filename)[0]
    target_filename = base_name + ".webp"
    target_path = os.path.join(asset_dir, target_filename)
    
    # Check current size to see if it needs work
    curr_size_kb = os.path.getsize(filepath) / 1024
    if filename.endswith(".webp") and 70 <= curr_size_kb <= 95:
        results.append(f"SKIPPED {filename}: Already {curr_size_kb:.2f} KB")
        continue

    try:
        with Image.open(filepath) as img:
            # Handle transparency (RGBA to WebP works, but ensure no issues)
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                pass 
            else:
                img = img.convert('RGB')
                
            status = save_with_target_size(img, target_path)
            results.append(f"PROCESSED {filename} -> {target_filename}: {status}")
            
            # If we converted from non-webp, we might want to keep the original for now or delete it
            # User wants everything IN webp, so I'll eventually propose updating the HTML.
    except Exception as e:
        results.append(f"FAILED {filename}: {str(e)}")

print("\n".join(results))
