from threading import Timer
from find_lang import FindLang


find_lang = FindLang("datasets")
lang = find_lang.find("examples/life_on_mars.txt")

print(lang)
assert lang == "eng_GB"
