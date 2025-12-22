################################################
# Programmeerimine I
# 2024/2025 sügissemester
#
# Teema: Keskendumise hindaja
#
# Eesmärk: Parandada keskendumisvõimet arvutis töötamisel.
#           Võimalik valida klaviatuuri kontroll, selleks saab määrata enda jaoks
#           sobiv intervall KLAVIATUURI_INTERVALL. Klaviatuuri kontroll pakub täiendavat
#           võimalust keskendumise hindamiseks. Näiteks võimaldab hinnata iseseisvate ülesannete lahendamise effektiivsust.
#           Samuti saab valida videopildi nägemist, näiteks programmi toimimise kontrolliks.
#
# Juhis - vaja laadida:
#   1. Requirements
#   2. VS Tools
#
# Kasutus:
#   Kui esimesel kasutusel ei toimi, proovida uuesti käivitada.
#   Programmist väljumine 2 viisil: 
#       'q' (kui valida video nägemise võimalus, siis hiirega videopildil hoides ning siis 'q' vajutamisel)
#       kombinatsioon 'ctrl + alt + e' terminalis. (kombinatsioon on valitud selliselt, et suure
#                                                       tõenäosusega klaviatuuri kasutusel programm ei sulge kogemata)
#   
#   Programmi lõpus kuvatakse vasakul praegust sooritust. graafikuna kuvatakse kuni 25 järjestikkust eelnevat tulemust.
#   Lisaks kuvatakse ka klaviatuuri kontrollimise tulemus, kui see valik sai alguses märgitud.
#
# 
##################################################

# Vajalikud teegid
import face_recognition
import cv2
from pynput import keyboard
import keyboard as kb
import tkinter as tk
import datetime



######  MUUTUJAD  ######
KLAVIATUURI_INTERVALL = 3 # sekundites




def käivita_programm():
    ekraan.destroy()



# ----- ESILEHT ----- #
ekraan = tk.Tk()
ekraan.title("KESKENDUMISE HINDAJA")

laius = ekraan.winfo_screenwidth()
kõrgus = ekraan.winfo_screenheight()
ekraan.geometry(f"{laius}x{kõrgus}")
ekraan.configure(bg="bisque3")

kanvas = tk.Canvas(ekraan, bg='antique white', highlightthickness=0)
kanvas.place(relx=0.5, rely=0.35, relwidth=0.6, relheight=0.4, anchor="center")

# Kirjutab teksti uuesti kui ekraan muutub, 
# et tekst oleks keskel
def joonista_tekst(event):
    kanvas.delete("all")
    w = event.width
    h = event.height
    kanvas.create_rectangle(0, 0, w, h, fill="orange", outline="")
    kanvas.create_rectangle(10, 10, w-10, h-10, fill="antique white", outline="")
    kanvas.create_text(w/2, h/2 - 40, text="Keskendumise", fill="orange", 
                       font=('Arial', int(h/8), "bold"))
    kanvas.create_text(w/2, h/2 + 40, text="hindaja", fill="orange", 
                       font=('Arial', int(h/8), "bold"))

kanvas.bind("<Configure>", joonista_tekst)

# --- NUPUD --- #
klaviatuur_linnuke = tk.BooleanVar()
video_linnuke = tk.BooleanVar()
klaviatuur = tk.Checkbutton(ekraan, text="Soovin klaviatuuri sisestusi näha", 
                            variable=klaviatuur_linnuke, onvalue=True, offvalue=False)
video = tk.Checkbutton(ekraan, text="Soovin näha videot", 
                       variable=video_linnuke, onvalue=True, offvalue=False)

style_options = {"bg": "antique white", "fg": "black", "font": ("Arial", 18), "selectcolor": "white"}
klaviatuur.config(**style_options)
video.config(**style_options)

klaviatuur.place(relx=0.5, rely=0.65, anchor="center")
video.place(relx=0.5, rely=0.72, anchor="center")

alusta_nupp = tk.Button(ekraan, text="Alusta!", command=käivita_programm, 
                        bg="orange", fg="white", font=("Arial", 24, "bold"), padx=20)
alusta_nupp.place(relx=0.5, rely=0.85, anchor="center")

ekraan.mainloop()


#Muutujad linnukese panekul
klaviatuur_muutuja = klaviatuur_linnuke.get()
video_muutuja = video_linnuke.get()
print()
print("############   VALIKUD   #############")
print(f"Klaviatuur: {klaviatuur_muutuja}")
print(f"Video:      {video_muutuja}")
print("######################################")
print()




#Esialgne aeg ning kuupäev
hetkeaeg = datetime.datetime.now()
algusaeg = (hetkeaeg.hour, hetkeaeg.minute)
kuupäev = (hetkeaeg.day, hetkeaeg.month, hetkeaeg.year)
print(f"Tänane kuupäev:  {hetkeaeg.day}.{hetkeaeg.month}.{hetkeaeg.year}")
print(f"Algusaeg:        {hetkeaeg.hour}:{hetkeaeg.minute}")
print()
print("------  Programmist väljumiseks vajutada 'ctrl' + 'alt' + 'e' või videopildile vajutamise järel 'q'  ------")


# ------------- PÕHIPROGRAMM ---------------- #

# valib veebikaamera (kui on üksainus, siis valib selle)
kaamera = cv2.VideoCapture(0)

näo_asukoht = []
kontrollitav_kaader = True


# muutujad
d = 0.5  # muutuja kasti (näo tuvastuskauguse) jaoks
s = int(1/d)  # muutuja kasti (näo tuvastuskauguse) jaoks
k = 1  #kaadrite arv (mitme kaadri tagant kontrollida kohalolu)
p=0  # positiivsed kaadrid
n=0  # negatiivsed kaadrid
w=0

#######################   Autor: Hugo Tristan Tammik   ################################################
# Muutujate initsialiseerimine
klahv_tuvastatud = False  # Jälgib, kas klahvi on vajutatud jooksvas tsüklis
klahvide_tuvastamise_tsüklid = 0  # Loendab tsükleid, kus vähemalt üks klahv tuvastati
tuvastamise_aken_aktiivne = False  # Lipp tuvastamise akna aktiivsuse kohta
kõik = 0  # Kõigi tsüklite loendur
kasulikud_tsüklid = 0  # Kasulike tsüklite loendur
efektiivsus = 0

# Funktsioon klahvivajutuse käsitlemiseks
def klahvi_vajutusel(klahv):
    global klahv_tuvastatud, tuvastamise_aken_aktiivne
    # Tuvasta klahvivajutus ainult aktiivse tuvastamise akna ajal
    if tuvastamise_aken_aktiivne and not klahv_tuvastatud:
        klahv_tuvastatud = True  # Märgista, et klahvi vajutati

# Käivita klahvikuulaja taustal
kuulaja = keyboard.Listener(on_press=klahvi_vajutusel)
kuulaja.start()

# Salvesta algusaeg
algusaeg1 = datetime.datetime.now()
if (klaviatuur_muutuja):
    print("\n" + f"Valisite klaviatuuri kontrolli. Praeguseks kontrollintervalliks on valitud {KLAVIATUURI_INTERVALL / 60} minutit.")

while True:
    # Arvuta möödunud aeg
    möödunud_aeg = datetime.datetime.now() - algusaeg1

    if (klaviatuur_muutuja):
        # Aktiveeri tuvastamise aken pärast KLAVIATUURI_INTERVALL sekundit
        if not tuvastamise_aken_aktiivne and möödunud_aeg >= datetime.timedelta(seconds=KLAVIATUURI_INTERVALL):
            tuvastamise_aken_aktiivne = True
            akna_lopp_aeg = datetime.datetime.now() + datetime.timedelta(seconds=KLAVIATUURI_INTERVALL)
            print("Tuvastamise aken on aktiivne. Vajuta mõnda klahvi selle tsükli jooksul.")

        # Kontrolli klahvivajutust KLAVIATUURI_INTERVALL-sekundilise akna jooksul
        if tuvastamise_aken_aktiivne:
            if klahv_tuvastatud:
                klahvide_tuvastamise_tsüklid += 1  # Suurenda tsüklite loendurit
                kasulikud_tsüklid += 1  # Suurenda kasulike tsüklite loendurit
                print("Klahv tuvastati selle tsükli jooksul.")
                kõik += 1
                klahv_tuvastatud = False  # Taasta klahvi tuvastamise lipp
                tuvastamise_aken_aktiivne = False  # Lõpeta tuvastamise aken selleks tsükliks
                algusaeg1 = datetime.datetime.now()  # Taasta algusaeg järgmiseks tsükliks
            elif datetime.datetime.now() >= akna_lopp_aeg:
                print("Tuvastamise aken lõppes ilma klahvivajutuseta.")
                kõik += 1
                tuvastamise_aken_aktiivne = False  # Lõpeta tuvastamise aken
                algusaeg1 = datetime.datetime.now()  # Taasta algusaeg järgmiseks tsükliks

        # Arvuta efektiivsus iga tsükli järel
        if kõik > 0:
            efektiivsus = (kasulikud_tsüklid / kõik) * 100
            # print(f"Efektiivsus: {efektiivsus:.2f}%")

###################################################################
    
    
    
    # vahelejäävad kaadrid optimaalsuse jaoks
    i=0
    while i < k:
        ret, kaader = kaamera.read()
        i+=1
        w+=i

    # näo tuvastamine ja koordinaatide lisamine järjendisse näo_asukohad
    if kontrollitav_kaader:
        pisem_kaader = cv2.resize(kaader, (0, 0), fx=d, fy=d)
        näo_asukoht = face_recognition.face_locations(pisem_kaader)
        if face_recognition.face_locations(pisem_kaader) != []:
            p +=1
        else:
            n +=1
            
    kontrollitav_kaader = not kontrollitav_kaader


    # kasti loomine ümber näo
    for (ülemine, parem, alumine, vasak) in näo_asukoht:
        ülemine *= s
        parem *= s
        alumine *= s
        vasak *= s
        
        cv2.rectangle(kaader, (vasak, ülemine), (parem, alumine), (0, 0, 255), 2)


    # näitab kontrollitavat kaadrit
    if video_muutuja:
        cv2.imshow('Video', kaader)
    

    # vajutades "ctrl + alt + e" lõpetab tegevuse
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
    # vajutades "ctrl + alt + e" lõpetab tegevuse
    if kb.is_pressed('ctrl + alt + e'):
        break
    
    


kaamera.release()
cv2.destroyAllWindows()

################################################
if (klaviatuur_muutuja):
    print()
    print("############   KLAVIATUUR   #############")
    print(f"Kõik tsüklid: {kõik}")
    print(f"Kõik tuvastatud tsüklid: {klahvide_tuvastamise_tsüklid}")
########################################################
# arvutused
#print(p)
#print(n)
protsent = 0.0
if n+p != 0:
    protsent = round((p)/(p+n), 2)
    print()
    print(f"Keskendumise protsent: {protsent*100}%", end="")
    if protsent*100 > 80 and protsent*100 < 100:
        print(" - Keskendusid väga palju!", end="")
    elif protsent == 1:
        print(" - Keskendusid kogu aja!", end="")
else:
    protsent = 0    

lõppaeg = (hetkeaeg.hour, hetkeaeg.minute)
aeg=0
minutid=""
tunnid=""
if lõppaeg[0] < algusaeg[0]:
    aeg = (24-lõppaeg[0] + algusaeg[0])*60 + (60-lõppaeg[1]+int(algusaeg[1]))
elif lõppaeg[0] == algusaeg[0]:
    aeg = lõppaeg[1] - algusaeg[1]
else:
    aeg = (lõppaeg[0] - algusaeg[0])*60 + (60-lõppaeg[1]+int(algusaeg[1]))
        
if aeg%60 < 10:
    minutid = "0" + str(aeg%60)
if int(aeg/60) < 10:
    tunnid = "0" + str(int(aeg/60))
t = (tunnid, minutid)
print("\n" + f"Aega kulus:            {t[0]}h {t[1]}min")


ajakulu = t[0] + ":" + t[1]
kuup = str(kuupäev[0]) + "." + str(kuupäev[1])
algus = str(algusaeg[0]) + "." + str(algusaeg[1])
aasta = kuupäev[2]


    


ekraan = tk.Tk()
ekraan.title("KESKENDUMISE HINDAJA")
laius = ekraan.winfo_screenwidth()               
pikkus = ekraan.winfo_screenheight()               
ekraan.geometry(f"{laius}x{pikkus}")
ekraan.configure(bg="bisque3")

kanvas = tk.Canvas(ekraan, bg='antique white', highlightthickness=0)
kanvas.place(relx=0.03, rely=0.03, relwidth=0.94, relheight=0.8)

ekraan.update()
w = kanvas.winfo_width()
h = kanvas.winfo_height()

kanvas.create_rectangle(30, 30, 140, 90, fill="orange")
kanvas.create_rectangle(34, 34, 136, 86, fill="antique white")
kanvas.create_text((85, 50), text="Keskendumise", fill="orange", font=('Arial', 10, "bold"))
kanvas.create_text((85, 65), text="hindaja", fill="orange", font=('Arial', 10, "bold"))

if protsent >= 0.8:
    värv = "green"
elif 0.8 > protsent > 0.70:
    värv = "yellow"
else:
    värv = "red"

baas_y = h * 0.85
skaala_kõrgus = h * 0.6
osakaal = skaala_kõrgus * protsent

kanvas.create_rectangle(w*0.05, baas_y - skaala_kõrgus, w*0.12, baas_y, fill="antique white")
kanvas.create_rectangle(w*0.05, baas_y, w*0.12, baas_y - osakaal, fill=värv)

kanvas.create_text((w*0.085, baas_y + 25), text=(str(int(round(protsent*100, 0))) + "%"), fill="midnight blue", font=("Arial", 15))
kanvas.create_text((w*0.05, h*0.3), text=f"Aeg: {ajakulu}", fill="midnight blue", font=("Arial", 10, "bold"), anchor="w")
kanvas.create_text((w*0.05, h*0.35), text=f"Kuupäev: {kuup}", fill="midnight blue", font=("Arial", 10, "bold"), anchor="w")
kanvas.create_text((w*0.05, h*0.4), text=f"Kellaaeg: {algus}", fill="midnight blue", font=("Arial", 10, "bold"), anchor="w")

telg_x = w * 0.18
kanvas.create_line(telg_x, h*0.1, telg_x, baas_y + 10, width=4, fill="black")

kanvas.create_text((telg_x + 30, baas_y + 25), text="Protsent:", fill="midnight blue", anchor="e")
kanvas.create_text((telg_x + 30, baas_y + 50), text="Aeg:", fill="midnight blue", anchor="e")
kanvas.create_text((telg_x + 30, baas_y + 75), text="Kuupäev:", fill="midnight blue", anchor="e")
kanvas.create_text((telg_x + 30, baas_y + 100), text="Kellaaeg:", fill="midnight blue", anchor="e")

puudub = False
try:
    f = open("keskendumiste_ajalugu.txt", encoding="UTF-8")
except:
    puudub = True

if not puudub:
    andmed = [line for line in f if line.strip()]
    f.close()
    
    if len(andmed) > 0:
        if len(andmed) > 25:
            andmed = andmed[-25:]
        
        graafiku_x = telg_x + 60
        samm = (w - graafiku_x - 50) / max(len(andmed), 1)
        
        for i in range(len(andmed)):
            tükid = andmed[i].strip().split(" - ")
            y1 = float(tükid[0]) / 100
            punkt_y = baas_y - (y1 * skaala_kõrgus)
            
            kanvas.create_line(graafiku_x, punkt_y, graafiku_x, baas_y, width=1, fill="black", dash=(5,2))
            kanvas.create_oval(graafiku_x-4, punkt_y-4, graafiku_x+4, punkt_y+4, fill="black")
            
            kanvas.create_text((graafiku_x, baas_y + 25), text=f"{int(y1*100)}%", font=('Arial', 9, "bold"))
            kanvas.create_text((graafiku_x, baas_y + 50), text=tükid[1], font=('Arial', 8))
            kanvas.create_text((graafiku_x, baas_y + 75), text=tükid[2], font=('Arial', 7))
            kanvas.create_text((graafiku_x, baas_y + 100), text=tükid[3], font=('Arial', 7))
            
            if i < len(andmed) - 1:
                y2 = float(andmed[i+1].strip().split(" - ")[0]) / 100
                punkt_y2 = baas_y - (y2 * skaala_kõrgus)
                j_värv = "green" if y2 >= y1 else "darkred"
                kanvas.create_line(graafiku_x, punkt_y, graafiku_x + samm, punkt_y2, width=3, fill=j_värv)
            
            graafiku_x += samm
if (klaviatuur_muutuja):
    kanvas.create_text((w*0.8, 10), text=f"### KLAVIATUURI KONTROLL ###", fill="midnight blue", font=("Arial", 12, "bold"), anchor="w")
    kanvas.create_text((w*0.8, 50), text=f"Kõik tsüklid: {kõik}", fill="midnight blue", font=("Arial", 12, "bold"), anchor="w")
    kanvas.create_text((w*0.8, 90), text=f"Kasulikud tsüklid: {kasulikud_tsüklid}", fill="midnight blue", font=("Arial", 12, "bold"), anchor="w")
    kanvas.create_text((w*0.8, 130), text=f"Efektiivsus: {efektiivsus:.2f}%", fill="midnight blue", font=("Arial", 12, "bold"), anchor="w")

salvestus_linnuke = tk.BooleanVar(value=True)
salvestus = tk.Checkbutton(ekraan, text="Soovin tulemust salvestada", variable=salvestus_linnuke, onvalue=True, offvalue=False)
salvestus.config(bg="antique white", fg="black", font=("Arial", 18), selectcolor="white")
salvestus.place(relx=0.5, rely=0.88, anchor="center")

nupp_väljumiseks = tk.Button(ekraan, text="Välju programmist", command=ekraan.destroy, bg="antique white", fg="black", font=("Arial", 16))
nupp_väljumiseks.place(relx=0.5, rely=0.95, anchor="center")

ekraan.mainloop()

if salvestus_linnuke.get():
    with open("keskendumiste_ajalugu.txt", "a", encoding="UTF-8") as f:
        f.write(f"{protsent*100} - {ajakulu} - {kuup} - {algus} - {aasta} - Kõik tsüklid: {kõik} - Kasulikud tsüklid: {kasulikud_tsüklid} - Efektiivsus: {efektiivsus:.2f}%\n")