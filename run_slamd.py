import threading
import time
import os
import webbrowser
import sys
from pathlib import Path

# ✅ Set LOLO_JAR_PATH path from bundled .exe or dev folder
if hasattr(sys, "_MEIPASS"):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(__file__)

lolo_jar_path = os.path.join(base_dir, 'slamd', 'libs', 'lolo-0.7.3.jar')
os.environ['LOLO_JAR_PATH'] = lolo_jar_path

# ✅ Monkey-patch lolopy to return correct JAR path
import lolopy.loloserver

def patched_find_lolo_jar(*args, **kwargs):
    return lolo_jar_path

lolopy.loloserver.find_lolo_jar = patched_find_lolo_jar

# ✅ Set other environment variables
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = 'ABC'
os.environ['OPENAI_API_TOKEN'] = 'ABC'

# ✅ Start app
from slamd import create_app
import py4j.java_collections

app = create_app()

def open_browser():
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:5001")

if __name__ == '__main__':
    threading.Thread(target=open_browser).start()
    app.run(debug=False, port=5001, use_reloader=False)
