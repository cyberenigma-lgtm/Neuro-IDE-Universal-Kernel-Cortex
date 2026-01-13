import sys
import os
import shutil
from unittest.mock import MagicMock

# 1. Mock Tkinter BEFORE importing modules that use it
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()

# 2. Setup environment
sys.path.append(os.getcwd())

# 3. Import the specific plugin
try:
    from modules.scaffold import Plugin
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

# 4. Setup Test
plugin = Plugin()
plugin.ent_name = MagicMock()
plugin.ent_name.get.return_value = "TestGenOS" # The project name
plugin.log = MagicMock() # The log widget

print(f"Testing Generator with Project Name: {plugin.ent_name.get.return_value}")

# 5. Run Generation
try:
    plugin.generate_kernel()
except Exception as e:
    print(f"Generation Exception: {e}")
    sys.exit(1)

# 6. Verify Output
target_dir = os.path.join("projects", "TestGenOS")
files = ["kernel.c", "boot.asm", "Makefile", "linker.ld"]
missing = []

for f in files:
    path = os.path.join(target_dir, f)
    if os.path.exists(path):
        print(f"[OK] Found {f}")
    else:
        print(f"[FAIL] Missing {f}")
        missing.append(f)

if not missing:
    print("SUCCESS: All kernel files generated.")
else:
    print("FAILURE: Missing files.")

# Cleanup
# try:
#     shutil.rmtree(target_dir)
#     print("Cleanup complete.")
# except:
#     pass
