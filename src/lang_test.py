from lang import Lang

lang_deu = Lang("datasets/deu_DE.latn.German.bible-devtest.utf8", 5, 0.10)
lang_gb = Lang("datasets/eng_GB.latn.English.EP7-devtest.utf8", 5, 0.10)
lang_est = Lang("est_EE.latn.Estonian.EP7-devtest.utf8", 5, 0.10)

total_bits_deu = lang_deu.estimate_bits("examples/life_on_mars.txt")
total_bits_gb = lang_gb.estimate_bits("examples/life_on_mars.txt")
total_bits_est = lang_est.estimate_bits("examples/life_on_mars.txt")


assert total_bits_deu == 19754
assert total_bits_gb == 13291
assert total_bits_est == 20423
