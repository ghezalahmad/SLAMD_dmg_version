import threading
import time
import os
import webbrowser
import sys
import py4j.java_gateway
import lolopy.loloserver
import logging
import inspect


# ✅ Setup logger for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Determine base directory (PyInstaller bundle or dev)
if hasattr(sys, "_MEIPASS"):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(__file__)

# ✅ Set JAR paths (CORRECTED TO jars/)
jars_dir = os.path.join(base_dir, 'slamd', 'jars')
lolo_jar_path = os.path.join(jars_dir, 'lolo-0.7.3.jar')
py4j_jar_path = os.path.join(jars_dir, 'py4j-0.10.9.7.jar')

# ✅ Check for JARs
logger.info(f"🧪 Lolo JAR: {lolo_jar_path} exists? {os.path.exists(lolo_jar_path)}")
logger.info(f"🧪 Py4J JAR: {py4j_jar_path} exists? {os.path.exists(py4j_jar_path)}")

# ✅ Set environment for lolopy
os.environ['LOLO_JAR_PATH'] = lolo_jar_path

# ✅ Patch lolopy JAR finder
def patched_find_lolo_jar(*args, **kwargs):
    return lolo_jar_path
lolopy.loloserver.find_lolo_jar = patched_find_lolo_jar

# ✅ Patch py4j to inject jarpath ONLY if not passed
original_launch_gateway = py4j.java_gateway.launch_gateway
param_names = list(inspect.signature(original_launch_gateway).parameters.keys())

def patched_launch_gateway(*args, **kwargs):
    logger.info(f"Injecting py4j jarpath: {py4j_jar_path}")

    # Sanitize positional args: remove existing jarpath if present
    arg_names = inspect.getfullargspec(original_launch_gateway).args
    if 'jarpath' in arg_names and len(args) >= arg_names.index('jarpath') + 1:
        args = list(args)
        logger.info("⚠️ Removing jarpath from positional args to avoid conflict")
        args[arg_names.index('jarpath')] = py4j_jar_path
        return original_launch_gateway(*args, **kwargs)

    # Otherwise, just inject if not already set
    if 'jarpath' not in kwargs or not kwargs['jarpath']:
        kwargs['jarpath'] = py4j_jar_path

    return original_launch_gateway(*args, **kwargs)



py4j.java_gateway.launch_gateway = patched_launch_gateway

# ✅ Set environment variables
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = 'ABC'
os.environ['OPENAI_API_TOKEN'] = 'ABC'

# ✅ Correct template/static folder paths
template_folder = os.path.join(base_dir, 'slamd', 'templates')
static_folder = os.path.join(base_dir, 'slamd', 'static')

# ✅ Run Flask app
from slamd import create_app
import py4j.java_collections  # required by lolopy
app = create_app(template_folder=template_folder, static_folder=static_folder)

def open_browser():
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:5001")

if __name__ == '__main__':
    threading.Thread(target=open_browser).start()
    app.run(debug=False, port=5001, use_reloader=False)
