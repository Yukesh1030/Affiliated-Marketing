import os
from PIL import Image

# Mapping of source images (from generation) to target names
logos = {
    r"C:\Users\YUKESH G\.gemini\antigravity\brain\7532cfb0-7bfd-4928-aff6-b30a438f7374\logo_hyugalife_1775711566142.png": "logo_hyugalife.webp",
    r"C:\Users\YUKESH G\.gemini\antigravity\brain\7532cfb0-7bfd-4928-aff6-b30a438f7374\logo_dermaco_1775711586188.png": "logo_dermaco.webp",
    r"C:\Users\YUKESH G\.gemini\antigravity\brain\7532cfb0-7bfd-4928-aff6-b30a438f7374\logo_shopsy_1775711600037.png": "logo_shopsy.webp",
    r"C:\Users\YUKESH G\.gemini\antigravity\brain\7532cfb0-7bfd-4928-aff6-b30a438f7374\logo_firstcry_1775711613246.png": "logo_firstcry.webp",
    r"C:\Users\YUKESH G\.gemini\antigravity\brain\7532cfb0-7bfd-4928-aff6-b30a438f7374\logo_mcaffeine_1775711626972.png": "logo_mcaffeine.webp",
    r"C:\Users\YUKESH G\.gemini\antigravity\brain\7532cfb0-7bfd-4928-aff6-b30a438f7374\logo_sbicard_1775711650598.png": "logo_sbicard.webp",
    r"C:\Users\YUKESH G\.gemini\antigravity\brain\7532cfb0-7bfd-4928-aff6-b30a438f7374\logo_agoda_1775711666513.png": "logo_agoda.webp",
    r"C:\Users\YUKESH G\.gemini\antigravity\brain\7532cfb0-7bfd-4928-aff6-b30a438f7374\logo_koparo_1775711682954.png": "logo_koparo.webp",
    r"C:\Users\YUKESH G\.gemini\antigravity\brain\7532cfb0-7bfd-4928-aff6-b30a438f7374\logo_dotkey_1775711697400.png": "logo_dotkey.webp",
    r"C:\Users\YUKESH G\.gemini\antigravity\brain\7532cfb0-7bfd-4928-aff6-b30a438f7374\logo_muscleblaze_1775711716597.png": "logo_muscleblaze.webp",
}

target_dir = r"d:\yukesh\projects\Affiliated Marketing\asset"
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

for src, name in logos.items():
    if os.path.exists(src):
        img = Image.open(src)
        # Convert to RGB if needed (webp loves RGB/RGBA)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        target_path = os.path.join(target_dir, name)
        
        # We try to target 70-90kb. Webp quality adjustment can help.
        # High quality (80-90) usually results in smaller files for minimalist logos.
        img.save(target_path, "WEBP", quality=85)
        
        file_size = os.path.getsize(target_path) / 1024
        print(f"Converted {name}: {file_size:.2f} KB")
    else:
        print(f"NOT FOUND: {src}")
