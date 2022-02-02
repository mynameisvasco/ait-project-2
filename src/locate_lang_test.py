from matplotlib import pyplot
from fcm import Fcm

from locate_lang import LocateLang

locate_lang_target = 'locatelangresults/locatelangtest.txt'
locate_lang = LocateLang('locatelangresults',
                         'locatelangresults/locatelangtest.txt', 3000000, 11)

results = locate_lang.lang_results

locate_lang.find_lang_indexes()
indexes = locate_lang.lang_segments
print(locate_lang.lang_results)
print(len(locate_lang.lang_results['por_PT']))
lang_names = [lang[1] for lang in indexes]
colors = {lang_names[0]: 'blue', lang_names[1]: 'green'}

context_size = 9
for i, lang in enumerate(results):
    pyplot.plot([i for i in range(context_size, len(results[lang]) +
                context_size)], results[lang], label=lang, color=colors[lang])
pyplot.xlabel('Char index')
pyplot.ylabel('Information amount (bits)')
pyplot.legend()

print(indexes)
for i in range(len(indexes)):
    if i != len(indexes) - 1:
        pyplot.axvspan(indexes[i][0], indexes[i+1][0], alpha=0.2, color=colors[indexes[i][1]])
    else:
        pyplot.axvspan(indexes[i][0], len(results[lang_names[0]]) - 1 + context_size, alpha=0.2, color=colors[indexes[i][1]])

with open(locate_lang_target) as target_file:
    target_text = target_file.read()
    for i, char in enumerate(target_text):
        pyplot.annotate(char, (i, -0.5), horizontalalignment='center',
                        fontfamily='monospace', fontsize='x-small')

pyplot.savefig('locatelangresults/graph.png')
pyplot.show()
