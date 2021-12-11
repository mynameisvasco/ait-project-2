from lang import Lang

lang_pt = Lang("datasets/por_PT.latn.Portugese.EP7-train.utf8", 5, 0.10)
lang_uk = Lang("datasets/eng_UK.latn.English.bible-train.utf8", 5, 0.10)
lang_br = Lang("datasets/por_BR.latn.portugues.bible-train.utf8", 5, 0.10)

total_bits_pt = lang_pt.estimate_bits("example.txt")
total_bits_br = lang_br.estimate_bits("example.txt")
total_bits_uk = lang_uk.estimate_bits("example.txt")

assert total_bits_br == 4741
assert total_bits_pt == 4118
assert total_bits_uk == 8379
