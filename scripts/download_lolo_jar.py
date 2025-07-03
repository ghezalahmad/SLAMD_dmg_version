import os
import urllib.request

LOLO_VERSION = "0.7.3"
LOLO_FILENAME = f"lolo-{LOLO_VERSION}.jar"
LOLO_DIR = os.path.join("slamd", "libs")
LOLO_PATH = os.path.join(LOLO_DIR, LOLO_FILENAME)
LOLO_URL = f"https://github.com/CitrineInformatics/lolo/releases/download/v{LOLO_VERSION}/{LOLO_FILENAME}"

def download_lolo_jar():
    if not os.path.exists(LOLO_DIR):
        os.makedirs(LOLO_DIR)
        print(f"✅ Created directory: {LOLO_DIR}")

    if not os.path.exists(LOLO_PATH):
        print(f"⬇️ Downloading {LOLO_FILENAME} from {LOLO_URL}...")
        try:
            urllib.request.urlretrieve(LOLO_URL, LOLO_PATH)
            print(f"✅ Downloaded to {LOLO_PATH}")
        except Exception as e:
            print(f"❌ Failed to download {LOLO_FILENAME}: {e}")
    else:
        print(f"✅ {LOLO_FILENAME} already exists at {LOLO_PATH}")

if __name__ == "__main__":
    download_lolo_jar()
