
# Keskendumise hindaja
#####
### Eesmärk: Parandada keskendumisvõimet arvutis töötamisel.
#####           Võimalik valida klaviatuuri kontroll, selleks saab määrata enda jaoks sobiva intervalli KLAVIATUURI_INTERVALL. 
#####           Klaviatuuri kontroll pakub täiendavat võimalust keskendumise hindamiseks. Näiteks võimaldab hinnata iseseisvate ülesannete lahendamise effektiivsust.
#####           Lisaks saab valida videopildi nägemist, näiteks programmi toimimise kontrolliks.
#####
### Juhis:
#####   1. variant (conda) - ``conda env create -f environment.yml``
#####   2. variant - ``pip install -r requirements.txt`` ning vaja laadida build tools ja veenduda, et Pythoni versioon on sobilik.
### Kasutus:
#####       Programmist väljumine 2 viisil: 
#####           1. 'q' (kui valida video nägemise võimalus, siis hiirega videopildil hoides ning siis 'q' vajutamisel);
#####           2. kombinatsioon 'ctrl + alt + e' terminalis. (kombinatsioon on valitud selliselt, et suure tõenäosusega klaviatuuri kasutusel programm kogemata ei sulge);
#####   
#####   Programmi lõpus kuvatakse vasakul praegust sooritust. Graafikuna kuvatakse kuni 25 järjestikkust eelnevat tulemust.
#####   Lisaks kuvatakse ka klaviatuuri kontrollimise tulemus, kui see valik sai alguses märgitud.
