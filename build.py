from pathlib import Path
import urllib.request
import sys

BUILD_HOME = Path(__file__).parent
SQLITE_EXT_PATH = BUILD_HOME / "sqlite_ext"
SQLITE_EXT_PATH.mkdir(exist_ok=True)
EXTENSIONS = (
    "spellfix",
)
DOWNLOAD_URL = "https://github.com/nalgeon/sqlean/releases/latest/download/{}"

platform = sys.platform.lower()
if platform in ("linux", "linux2", "cygwin"):
    file_ext = "so"
elif "darwin" in platform:
    file_ext = "dylib"
elif "win" in platform:
    file_ext = "dll"
else:
    raise Exception("Unsupported platform")

for name in EXTENSIONS:
    filename = f"{name}.{file_ext}"
    with urllib.request.urlopen(DOWNLOAD_URL.format(filename)) as f:
        (SQLITE_EXT_PATH / filename).write_bytes(f.read())


def build(setup_kwargs: dict):
    """ This function is mandatory in order to build the extensions. """
    data_files: list = setup_kwargs.get("data_files", list())
    data_files.append(("utmo/sqlite_ext", ["utmo/sqlite_ext/*"]))
    setup_kwargs["data_files"] = data_files
