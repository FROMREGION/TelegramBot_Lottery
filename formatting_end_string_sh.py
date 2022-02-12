from os import listdir, path
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'


def replacement_strings():
    files_sh = [file_name for file_name in listdir() if file_name.endswith(".sh")]
    for file_name in files_sh:
        with open(path.join(BASE_DIR, file_name), "rb") as file:
            content = file.read()
            content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
        with open(path.join(BASE_DIR, file_name), "wb") as file:
            file.write(content)
    print("Complete!")


if __name__ == "__main__":
    replacement_strings()