from combined_fcm import CombinedFcm
from fcm import Fcm

fcm1 = Fcm(0.05, 3)
fcm1.add_text("datasets/por_PT.latn.Portugese.EP7-devtest.utf8")
fcm2 = Fcm(0.05, 6)
fcm2.add_text("datasets/por_PT.latn.Portugese.EP7-devtest.utf8")
fcm3 = Fcm(0.05, 9)
fcm3.add_text("datasets/por_PT.latn.Portugese.EP7-devtest.utf8")


fcm = CombinedFcm([fcm1, fcm2, fcm3])
print(fcm.get_information_amount("b", "Olá tudo "))
print(fcm3.get_information_amount("b", "Olá tudo "))
