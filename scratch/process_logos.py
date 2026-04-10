import os
from PIL import Image

# Mapping of source images to target names
logos = {
    r"C:\Users\YUKESH G\.gemini\antigravity\brain\de4e292a-7eef-4c60-b4fd-3c4f801d7cd5\logo_visa_1775791622456.png": "logo_visa.webp",
    r"C:\Users\YUKESH G\.gemini\antigravity\brain\de4e292a-7eef-4c60-b4fd-3c4f801d7cd5\logo_mastercard_1775791641524.png": "logo_mastercard.webp",
    r"C:\Users\YUKESH G\.gemini\antigravity\brain\de4e292a-7eef-4c60-b4fd-3c4f801d7cd5\logo_rupay_1775791656298.png": "logo_rupay.webp",
    r"C:\Users\YUKESH G\.gemini\antigravity\brain\de4e292a-7eef-4c60-b4fd-3c4f801d7cd5\logo_amex_premium_1775791671488.png": "logo_amex.webp",
    r"C:\Users\YUKESH G\.gemini\antigravity\brain\de4e292a-7eef-4c60-b4fd-3c4f801d7cd5\logo_hdfc_1775791686759.png": "logo_hdfc.webp",
    r"C:\Users\YUKESH G\.gemini\antigravity\brain\de4e292a-7eef-4c60-b4fd-3c4f801d7cd5\logo_icici_1775791700752.png": "logo_icici.webp",
    r"C:\Users\YUKESH G\.gemini\antigravity\brain\de4e292a-7eef-4c60-b4fd-3c4f801d7cd5\logo_axis_1775791718442.png": "logo_axis.webp",
}

target_dir = r"d:\yukesh\projects\Affiliated Marketing\asset"
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

def save_with_target_size(img, path, min_kb=70, max_kb=90):
    # Try different quality settings to hit the target
    for q in range(100, 1, -1):
        img.save(path, "WEBP", quality=q)
        size_kb = os.path.getsize(path) / 1024
        if size_kb <= max_kb:
            if size_kb >= min_kb:
                return size_kb
            else:
                # Too small even at high q? Upscale.
                break
    
    # If still too small, upscale
    if os.path.getsize(path) / 1024 < min_kb:
        curr_size_kb = os.path.getsize(path) / 1024
        scale = (min_kb / curr_size_kb) ** 0.5
        orig_w, orig_h = img.size
        # Iterative upscale to find the sweet spot
        for s_mult in [1.2, 1.5, 2.0, 3.0]:
            new_size = (int(orig_w * scale * s_mult), int(orig_h * scale * s_mult))
            img_large = img.resize(new_size, Image.Resampling.LANCZOS)
            img_large.save(path, "WEBP", quality=80)
            size_kb = os.path.getsize(path) / 1024
            if size_kb >= min_kb and size_kb <= max_kb:
                return size_kb
            if size_kb > max_kb:
                # If too big at scale s_mult, try lower quality
                for q in range(80, 1, -5):
                    img_large.save(path, "WEBP", quality=q)
                    size_kb = os.path.getsize(path) / 1024
                    if size_kb <= max_kb:
                        return size_kb
    return os.path.getsize(path) / 1024

for src, name in logos.items():
    if os.path.exists(src):
        img = Image.open(src)
        # Ensure it has transparency handled or converted to RGB
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            # Keep RGBA for webp transparency
            pass
        else:
            img = img.convert('RGB')
        
        target_path = os.path.join(target_dir, name)
        final_size = save_with_target_size(img, target_path)
        print(f"Processed {name}: {final_size:.2f} KB")
    else:
        print(f"NOT FOUND: {src}")
