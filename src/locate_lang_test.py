from matplotlib import pyplot

from fcm import Fcm
from locate_lang import LocateLang

context_size = 3
fcm1 = Fcm(0.2, context_size)
fcm1.add_file('datasets/por_PT.latn.Portugese.EP7-train.utf8')
fcm2 = Fcm(0.2, context_size)
fcm2.add_file('datasets/eng_GB.latn.English.EP7-train.utf8')

locate_lang_target = 'examples/locatelangtest.txt'
locate_lang = LocateLang(3, fcm1, fcm2)
locate_lang.generate_fcm_results(locate_lang_target)

results = locate_lang.fcms_results
locate_lang.find_fcm_indexes()
indexes = locate_lang.fcm_indexes

pyplot.plot([i for i in range(context_size, len(results['fcm1']) +
            context_size)], results['fcm1'], label='Fcm1', color='blue')
pyplot.plot([i for i in range(context_size, len(results['fcm2']) +
            context_size)], results['fcm2'], label='Fcm2', color='green')
pyplot.xlabel('Char index')
pyplot.ylabel('Information amount')
pyplot.legend()

print(indexes)
for fcm in indexes:
    if fcm == 'fcm1':
        color = 'blue'
    else:
        color = 'green'
    for span in indexes[fcm]:
        pyplot.axvspan(span[0], span[1], alpha=0.2, color=color)

with open(locate_lang_target) as target_file:
    target_text = target_file.read()
    for i, char in enumerate(target_text):
        pyplot.annotate(char, (i, -0), horizontalalignment='center',
                        fontfamily='monospace', fontsize='x-small')

pyplot.show()
