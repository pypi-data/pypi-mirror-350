import os
import sys
import shutil
from importlib.resources import files

def install_man_pages():
    man_dir = "/usr/local/share/man/man1" if sys.platform == "darwin" else "/usr/share/man/man1"

    if not os.access(man_dir, os.W_OK):
        sys.stderr.write(f"Error: You need superuser (sudo) privileges to install man pages to {man_dir}.\n")
        sys.stderr.write("Please rerun the script with sudo.\n")
        return 1

    # Files are expected to be in pygeai/man/man1/
    base = files("pygeai.man.man1")
    man_files = ["geai.1", "geai-proxy.1"]

    for fname in man_files:
        try:
            resource = base / fname
            if not resource.is_file():
                sys.stderr.write(f"Warning: {fname} does not exist in package.\n")
                continue

            dest_path = os.path.join(man_dir, fname)
            sys.stdout.write(f"Installing {fname} to {dest_path}...\n")
            with resource.open("rb") as src_file, open(dest_path, "wb") as dst_file:
                shutil.copyfileobj(src_file, dst_file)

        except Exception as e:
            sys.stderr.write(f"Error installing {fname}: {e}\n")

    return 0

if __name__ == "__main__":
    sys.exit(install_man_pages())
