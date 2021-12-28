from threading import Timer
from find_lang import FindLang
from pathlib import Path


for path in Path("examples").rglob("**/*"):
    if not path.is_dir() and ".DS_Store" not in str(path):
        print(path)
        find_lang = FindLang("datasets", path, 1000, 1000)
        print(find_lang.find())
