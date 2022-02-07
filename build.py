from pathlib import Path
import urllib.request
import zipfile
import sys
import io

BUILD_HOME = Path(__file__).parent
LIBS_PATH = BUILD_HOME / "libs"
SQLITE_EXTS_PATH = LIBS_PATH / "sqlite_exts"
SQLITE_EXTS_PATH.mkdir(exist_ok=True, parents=True)
EXTENSIONS = (
    "spellfix",
)
EXTS_DOWNLOAD_URL = "https://github.com/nalgeon/sqlean/releases/latest/download/{}"
SQLITE_DOWNLOAD_URL = "https://www.sqlite.org/{}/sqlite-dll-win{}-x{}-{}.zip"
WIN32_SQLITE = (2022, 32, 86, 3370200)
WIN64_SQLITE = (2022, 64, 64, 3370200)

platform = sys.platform.lower()
if platform in ("linux", "linux2", "cygwin"):
    file_ext = "so"

elif "darwin" in platform:
    file_ext = "dylib"

elif "win" in platform:
    file_ext = "dll"
    if sys.maxsize > 2 ** 32:
        sqlite_version = WIN32_SQLITE
    else:
        sqlite_version = WIN64_SQLITE
    with urllib.request.urlopen(SQLITE_DOWNLOAD_URL.format(*sqlite_version)) as f:
        with zipfile.ZipFile(io.BytesIO(f.read()), "r") as zip_ref:
            zip_ref.extractall(str(LIBS_PATH))

else:
    raise Exception("Unsupported platform")

for name in EXTENSIONS:
    filename = f"{name}.{file_ext}"
    with urllib.request.urlopen(EXTS_DOWNLOAD_URL.format(filename)) as f:
        (SQLITE_EXTS_PATH / filename).write_bytes(f.read())


def build(setup_kwargs: dict):
    """ This function is mandatory in order to build the extensions. """
    data_files: list = setup_kwargs.get("data_files", list())
    data_files.append(
        (
            "utmo/libs",
            [str(i) for i in LIBS_PATH.rglob("*") if i.is_file()]
        )
    )
    setup_kwargs["data_files"] = data_files
