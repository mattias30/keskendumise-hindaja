import tkinter as tk


ekraan = tk.Tk()
 

ekraan.title(  "KESKENDUMISE HINDAJA")

width= ekraan.winfo_screenwidth()               
height= ekraan.winfo_screenheight()               


ekraan.geometry("%dx%d" % (width, height))

ekraan.configure(bg="bisque3")


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

print(konspekt_linnuke.get())
print(video_linnuke.get())


