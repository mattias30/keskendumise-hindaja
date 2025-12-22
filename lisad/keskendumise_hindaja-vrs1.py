################################################
# Programmeerimine I
# 2024/2025 sügissemester
#
# Projekt Tuto
# Teema: Keskendumise hindaja
#
#
# Autorid: Mattias Rahnu, Hugo Tristan Tammik
#
# Eeskuju: Saadud inspiratsiooni face_recognitioni projektikirjelduses olevatest näidetest,
#          loodud teemakohasemaks.
#
#Käivitamiseks:Vaja laadida C++ Build tools (installimisel vaja märkida desktop development, kõige ülemine ning vasakpoolseim)
#              Laadida vaja face_recognition: pip install face-recognition cmd-s
#              Laadida vaja ka opencv: pip install opencv-python
#
##################################################


import face_recognition
import cv2
import keyboard
import tkinter as tk






#Ekraani loomine
ekraan = tk.Tk()
ekraan.title(  "KESKENDUMISE HINDAJA")
laius= ekraan.winfo_screenwidth()               
kõrgus= ekraan.winfo_screenheight()               
ekraan.geometry("%dx%d" % (laius, kõrgus))
ekraan.configure(bg="bisque3")

#Esilehe pilt
kanvas = tk.Canvas(ekraan, width=750, height=400, bg='antique white')
kanvas.place(x=250, y=40)
kanvas.create_rectangle(50, 50, 705, 360, fill="orange")
kanvas.create_rectangle(65, 65, 690, 345, fill="antique white")
kanvas.create_text(
    (375, 175),
    text="Keskendumise",
    fill="orange",
    font=('Arial', 50, "bold")
)
kanvas.create_text(
    (375, 250),
    text="hindaja",
    fill="orange",
    font=('Arial', 50, "bold")
)






konspekt_linnuke = tk.IntVar()
video_linnuke = tk.IntVar()


konspekt = tk.Checkbutton(ekraan, text="Konspekt on arvutis", variable=konspekt_linnuke, 
                             onvalue=1, offvalue=0)
video = tk.Checkbutton(ekraan, text="Soovin näha videot", variable=video_linnuke, 
                             onvalue=1, offvalue=0)


konspekt.config(bg="antique white", fg="black", font=("Arial", 21), 
                   selectcolor="white")
video.config(bg="antique white", fg="black", font=("Arial", 21), 
                   selectcolor="white")


konspekt.config(width=45, height=1)
video.config(width=45, height=1)

konspekt.place(x=250, y=510)
video.place(x=250, y=580)

ekraan.mainloop()

print(konspekt_linnuke.get())   #Muutujad linnukese panekul
print(video_linnuke.get())




#PÕHIPROGRAMM

# valib veebikaamera (0 on esimene (ainuke))
kaamera = cv2.VideoCapture(0)

# tulevad koordinaadid
näo_asukoht = []
kontrollitav_kaader = True

# muutuja kasti (näo tuvastuskauguse) jaoks
d = 0.5
s = int(1/d)

#kaadrite arv (mitme kaadri tagant kontrollida kohalolu)
f = 1

# p - mitu kaadrit oldi kohal | n - mitu kaadrit ei tuvastatud inimest
p=0
n=0

while True:

    

    # vahelejäävad kaadrid
    i=0
    while i < f:
        #ret on tagastusväärtus
        ret, kaader = kaamera.read()
        i+=1

    # kontrollitav kaader
    if kontrollitav_kaader:
        # kaadri väiksemaks tegemine näo kiiremaks tuvastamiseks
        pisem_kaader = cv2.resize(kaader, (0, 0), fx=d, fy=d)

        # Näotuvastus - tuvastab ning lisab koordinaadid järjendisse face_locations
        näo_asukoht = face_recognition.face_locations(pisem_kaader)
        # Juhul kui nägu ei tuvastatud
        if face_recognition.face_locations(pisem_kaader) != []:
            p +=1
        else:
            n +=1


    kontrollitav_kaader = not kontrollitav_kaader

    # Teeb kasti
    for (ülemine, parem, alumine, vasak) in näo_asukoht:
        # näo asukoha toob tagasi e kasti asukoha muudab õigeks
        ülemine *= s
        parem *= s
        alumine *= s
        vasak *= s

        cv2.rectangle(kaader, (vasak, ülemine), (parem, alumine), (0, 0, 255), 2)



    # Näitab kontrollitavat kaadrit
    cv2.imshow('Video', kaader)
    

    # Vajutades q-d, lõpetab tegevuse
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

    

# Lõpetab tegevuse
kaamera.release()
cv2.destroyAllWindows()

# arvutused
print(p) #kaadrid, mil oldi kohal
print(n) #kaadrid, millal ei oldud kohal
if n != 0:
    protsent = int(round((p*100)/(p+n), 0))
    print()
    print(f"{protsent}%")
    if (p*100)/(p+n) > 80:
        print("Keskendusid väga palju")
        
else:
    print("Keskendusid kogu aja")
    
    
