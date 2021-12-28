from matplotlib import pyplot
from fcm import Fcm

from locate_lang import LocateLang

locate_lang_target = 'locatelangdemo/locatelangtest.txt'
locate_lang = LocateLang('locatelangdemo', 'locatelangdemo/locatelangtest.txt',
                         3000000, 6)

results = locate_lang.lang_results

locate_lang.find_lang_indexes()
indexes = locate_lang.lang_segments
lang_names = list(indexes)
colors = {lang_names[0]: 'blue', lang_names[1]: 'green'}

context_size = 5
for i, lang in enumerate(results):
    pyplot.plot([i for i in range(context_size, len(results[lang]) +
                context_size)], results[lang], label=lang, color=colors[lang])
pyplot.xlabel('Char index')
pyplot.ylabel('Information amount')
pyplot.legend()

print(results)
fcm = Fcm(0.01, context_size)
fcm.add_file('locatelangdemo/por_PT.latn.Portugese.EP7-train.utf8')
target_path = 'locatelangdemo/locatelangtest.txt'
with open(target_path, "r") as target_file:
    target_text = target_file.read()
fcm_result = []
for i, char in enumerate(target_text[context_size:], start=context_size):
    context = target_text[i - context_size:i]
    bits = fcm.get_information_amount(char, context)
    # print(context, len(context))
    # print(len(target_text))
    # print(context_size)
    # print(bits)
    fcm_result.append(bits)
print(fcm_result)

print(indexes)
for i, lang in enumerate(indexes):
    for span in indexes[lang]:
        pyplot.axvspan(span[0], span[1], alpha=0.2, color=colors[lang])

with open(locate_lang_target) as target_file:
    target_text = target_file.read()
    for i, char in enumerate(target_text):
        pyplot.annotate(char, (i, -0), horizontalalignment='center',
                        fontfamily='monospace', fontsize='x-small')

pyplot.show()
