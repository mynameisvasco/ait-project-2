from find_lang import FindLang

find_lang = FindLang('datasets', 'examples/por_PT/mandarim.txt', 100000, 1000)

print(find_lang.find())
