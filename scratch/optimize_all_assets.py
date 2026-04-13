import os
from PIL import Image

def save_with_target_size(img, path, min_kb=71, max_kb=89):
    """Save an image in WebP format attempting to hit a target size range."""
    # Convert to RGB if necessary for consistency, though WebP supports RGBA
    if img.mode != 'RGB' and img.mode != 'RGBA':
        img = img.convert('RGB')

    def get_size(quality, scale=1.0):
        temp_path = path + ".tmp.webp"
        curr_img = img
        if scale != 1.0:
            w, h = img.size
            curr_img = img.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.Resampling.LANCZOS)
        
        curr_img.save(temp_path, "WEBP", quality=quality)
        size = os.path.getsize(temp_path) / 1024
        os.remove(temp_path)
        return size

    # Try different qualities and scales to hit 70-90KB
    best_q = 80
    best_scale = 1.0
    
    current_size = get_size(90, 1.0)
    
    if current_size > max_kb:
        # Too big, scale down or reduce quality
        found = False
        for scale in [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]:
            for q in range(95, 10, -5):
                size = get_size(q, scale)
                if min_kb <= size <= max_kb:
                    best_q = q
                    best_scale = scale
                    found = True
                    break
            if found: break
    elif current_size < min_kb:
        # Too small, scale up
        found = False
        for scale in [1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 8.0]:
            for q in range(80, 101, 2):
                if q > 100: q = 100
                size = get_size(q, scale)
                if min_kb <= size <= max_kb:
                    best_q = q
                    best_scale = scale
                    found = True
                    break
                if size > max_kb: # Overshot
                    break
            if found: break
        
        if not found:
            # If still not found, just use the one that got closest
            best_q = 100
            best_scale = 5.0
    else:
        best_q = 90
        best_scale = 1.0

    # Final save
    w, h = img.size
    final_img = img.resize((max(1, int(w * best_scale)), max(1, int(h * best_scale))), Image.Resampling.LANCZOS)
    final_img.save(path, "WEBP", quality=best_q)
    final_size = os.path.getsize(path) / 1024
    return f"Scale={best_scale:.2f}, Q={best_q}, Final Size={final_size:.2f} KB"

asset_dir = r"d:\yukesh\projects\Affiliated Marketing\asset"
image_exts = (".png", ".jpg", ".jpeg", ".bmp", ".webp")

files = [f for f in os.listdir(asset_dir) if f.lower().endswith(image_exts)]
results = []

print(f"Starting optimization of {len(files)} files...")

for filename in files:
    filepath = os.path.join(asset_dir, filename)
    base_name = os.path.splitext(filename)[0]
    target_filename = base_name + ".webp"
    target_path = os.path.join(asset_dir, target_filename)
    
    # Check current size
    curr_size_kb = os.path.getsize(filepath) / 1024
    if filename.lower() == target_filename.lower() and 70 <= curr_size_kb <= 90:
        results.append(f"SKIPPED {filename}: Already {curr_size_kb:.2f} KB")
        continue

    try:
        with Image.open(filepath) as img:
            status = save_with_target_size(img, target_path)
            results.append(f"PROCESSED {filename} -> {target_filename}: {status}") 
    except Exception as e:
        results.append(f"FAILED {filename}: {str(e)}")

print("\n".join(results))
