import os
import shutil
from PIL import Image

src_path = r"C:\Users\YUKESH G\.gemini\antigravity\brain\246aafc0-8f21-46bd-ac8f-03431b26ab82\affiliate_dashboard_1775642430925.png"
dst_path = r"d:\yukesh\projects\Affiliated Marketing\asset\affiliate-dashboard.webp"

if not os.path.exists("asset"):
    os.makedirs("asset")

# Target size bytes
MIN_SIZE = 70 * 1024
MAX_SIZE = 90 * 1024

def convert_and_compress(src, dst):
    img = Image.open(src)
    
    # Binary search for the right quality to fit size range
    low = 1
    high = 100
    best_quality = 80
    
    while low <= high:
        mid = (low + high) // 2
        img.save(dst, "WEBP", quality=mid, method=6)
        
        size = os.path.getsize(dst)
        print(f"Quality: {mid}, Size: {size/1024:.2f} KB")
        
        if MIN_SIZE <= size <= MAX_SIZE:
            print("Perfect size achieved!")
            return
        elif size < MIN_SIZE:
            low = mid + 1
            best_quality = mid  # store largest size that is under max just in case
        else:
            high = mid - 1
            
    # If we couldn't hit the exact range but found a close one
    print(f"Fallback to quality {best_quality}")
    img.save(dst, "WEBP", quality=best_quality, method=6)
    
convert_and_compress(src_path, dst_path)
