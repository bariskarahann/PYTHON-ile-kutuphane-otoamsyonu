from tkinter import *
from tkcalendar import DateEntry
import pypyodbc
from tkinter import messagebox
import threading
from datetime import datetime
from tkinter import ttk

giris = Tk()

giris.geometry("400x400")
giris.configure(bg="#2A2322")
giris.title("Kütüphane Otomasyonu")
giris.resizable(False,False)
global frame
kullaniciAdi = ""
frame = Frame(giris,width=400,height=400,bg="#2A2322")
frame.place(x=0,y=0)
now = datetime.now()
date = now.strftime("%d/%m/%Y")


def giris_yap(bilgi_label,kullaniciAdi_entry,sifre_entry):

    global giris_cursor,kullaniciAdi
    bilgi_label.config(text="Giriş kontrol ediliyor lütfen bekleyiniz...")
    db = pypyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-N9GSPR5\ZIHS;;'
                      'Database=KütüphaneOtomasyonu;'
                      'Trusted_Connection=yes;')
    giris_cursor = db.cursor()

    giris_cursor.execute("SELECT * FROM kayıtlı_kişiler where kullanıcı_adı= '"+ kullaniciAdi_entry.get() +"' and şifre= '"+ sifre_entry.get()+"';")
    sonuc = giris_cursor.fetchone()

    if sonuc==None:
        messagebox.showerror("Hata","Girdiğiniz kullanıcı adı veya şifre yanlış!")
    else:
        messagebox.showinfo("Başarılı","Başarıyla giriş yaptınız.")
        kullaniciAdi = kullaniciAdi_entry.get()
        print(kullaniciAdi)
        if(sonuc[3]=="kullanıcı"):
            kullanici_anasayfa_ekrani(sonuc,giris_cursor,db)
        else:
            yonetici_anasayfa_ekrani(sonuc,giris_cursor,db)
        giris.withdraw()
        
        

def giris_yap_baslat(bilgi_label,kullaniciAdi_entry,sifre_entry):

    x = threading.Thread(target=giris_yap,args=(bilgi_label,kullaniciAdi_entry,sifre_entry))
    x.start()
    

def giris_ekrani():

    ekrani_temizle()

    girisYap_label = Label(frame,text="Giriş Yap", font=("Arial", 25, "bold italic"), bg="#2A2322",fg="white",bd=5)
    girisYap_label.place(x=110,y=20)

    kullaniciAdi_label = Label(frame,text="Kullanıcı Adı:", font=("Arial", 12, "bold italic"), bg="#2A2322",fg="white",bd=5)
    kullaniciAdi_label.place(x=30,y=110)

    kullaniciAdi_entry = Entry(frame,width=15,font="Arial")
    kullaniciAdi_entry.place(x=150,y=112)

    sifre_label = Label(frame,text="Şifre:", font=("Arial", 12, "bold italic"), bg="#2A2322",fg="white",bd=5)
    sifre_label.place(x=30,y=150)

    sifre_entry = Entry(frame,width=15,font="Arial")
    sifre_entry.place(x=150,y=152)

    sifre_label = Label(frame,text="Şifre:", font=("Arial", 12, "bold italic"), bg="#2A2322",fg="white",bd=5)
    sifre_label.place(x=30,y=150)

    sifre_entry = Entry(frame,width=15,font="Arial")
    sifre_entry.place(x=150,y=152)

    bilgi_label = Label(frame,text="", font=("Arial", 12, "bold italic"), bg="#2A2322",fg="red",bd=5)
    bilgi_label.place(x=50,y=180)

    girisYap_btn = Button(frame, text="Giriş Yap", font=("Arial", 12, "bold italic"), fg='white',
                          bg="#1F77A9",
                          activebackground='green'
                          , activeforeground='white', bd=8, width=9, height=2, compound='left',command=lambda: giris_yap_baslat(bilgi_label,kullaniciAdi_entry,sifre_entry))
    girisYap_btn.place(x= 150 ,y = 220 )

    kayitOl_btn = Button(frame, text="Kayıt Ol", font=("Arial", 8, "bold italic"), fg='white',
                          bg="#9A3223",
                          activebackground='green'
                          , activeforeground='white', bd=5, width=8, height=2, compound='left',command= kayitOl_ekrani)
    kayitOl_btn.place(x= 310 ,y = 340 )


def ekrani_temizle():

    for widget in frame.winfo_children():
        widget.destroy()

def kayit_ol(bilgi_label,kullaniciAdi,sifre,ad,soyad,tel_no,adres,eposta,dogum_tarihi):

    bilgi_label.config(text="Kayıt yapılıyor lütfen bekleyiniz...")
    db = pypyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-N9GSPR5\ZIHS;'
                      'Database=KütüphaneOtomasyonu;'
                      'Trusted_Connection=yes;')
    giris_cursor = db.cursor()
    komut = 'INSERT INTO kayıtlı_kişiler VALUES(?,?,?,?,?,?,?,?,?,?)'
    veriler = (kullaniciAdi,sifre,"kullanıcı",ad,soyad,tel_no,adres,eposta,date,dogum_tarihi)
    try:
        giris_cursor.execute(komut,veriler)
        db.commit()
        messagebox.showinfo("Başarılı","Başarıyla kayıt oldunuz.")
        giris_ekrani()
    except: messagebox.showerror("Hata","Üye veritabanına kayıt edilirken hata oluştu.")

def kayit_ol_baslat(bilgi_label,kullaniciAdi,sifre,ad,soyad,tel_no,adres,eposta,dogum_tarihi):

    x = threading.Thread(target=kayit_ol,args=(bilgi_label,kullaniciAdi,sifre,ad,soyad,tel_no,adres,eposta,dogum_tarihi))
    x.start()


def kayitOl_ekrani():

    ekrani_temizle()

    kullaniciAdi_label = Label(frame,text="Kullanıcı Adı:", font=("Arial", 12, "bold italic"), bg="#2A2322",fg="white",bd=5)
    kullaniciAdi_label.place(x=30,y=20)

    kullaniciAdi_entry = Entry(frame,width=15,font="Arial")
    kullaniciAdi_entry.place(x=150,y=22)

    sifre_label = Label(frame,text="Şifre:", font=("Arial", 12, "bold italic"), bg="#2A2322",fg="white",bd=5)
    sifre_label.place(x=30,y=60)

    sifre_entry = Entry(frame,width=15,font="Arial")
    sifre_entry.place(x=150,y=62)

    ad_label = Label(frame,text="Ad:", font=("Arial", 12, "bold italic"), bg="#2A2322",fg="white",bd=5)
    ad_label.place(x=30,y=100)

    ad_entry = Entry(frame,width=15,font="Arial")
    ad_entry.place(x=150,y=102)

    soyad_label = Label(frame,text="Soyad:", font=("Arial", 12, "bold italic"), bg="#2A2322",fg="white",bd=5)
    soyad_label.place(x=30,y=140)

    soyad_entry = Entry(frame,width=15,font="Arial")
    soyad_entry.place(x=150,y=142)

    telNo_label = Label(frame,text="Tel No:", font=("Arial", 12, "bold italic"), bg="#2A2322",fg="white",bd=5)
    telNo_label.place(x=30,y=180)

    telNo_entry = Entry(frame,width=15,font="Arial")
    telNo_entry.place(x=150,y=182)

    adres_label = Label(frame,text="Adres:", font=("Arial", 12, "bold italic"), bg="#2A2322",fg="white",bd=5)
    adres_label.place(x=30,y=220)

    adres_entry = Entry(frame,width=15,font="Arial")
    adres_entry.place(x=150,y=222)

    eposta_label = Label(frame,text="E-posta:", font=("Arial", 12, "bold italic"), bg="#2A2322",fg="white",bd=5)
    eposta_label.place(x=30,y=260)

    eposta_entry = Entry(frame,width=15,font="Arial")
    eposta_entry.place(x=150,y=262)

    dogumTarihi_label = Label(frame,text="Doğum Tarihi:", font=("Arial", 11, "bold italic"), bg="#2A2322",fg="white",bd=5)
    dogumTarihi_label.place(x=30,y=300)

    dogumTarihi = DateEntry(frame,selectmode="day",date_pattern='dd/mm/y',width=24)
    dogumTarihi.place(x=150,y=302)

    bilgi_label = Label(frame,text="", font=("Arial", 12, "bold italic"), bg="#2A2322",fg="red",bd=5)
    bilgi_label.place(x=20,y=180)

    kayitOl_btn = Button(frame, text="Kayıt Ol", font=("Arial", 12, "bold italic"), fg='white',
                          bg="#1F77A9",
                          activebackground='green'
                          , activeforeground='white', bd=8, width=9, height=1, compound='left',command = lambda: kayit_ol_baslat(bilgi_label,kullaniciAdi_entry.get(),sifre_entry.get(),
                                                                                                                  ad_entry.get(),soyad_entry.get(),telNo_entry.get(),
                                                                                                                  adres_entry.get(),eposta_entry.get(),dogumTarihi.get()))
    kayitOl_btn.place(x= 150 ,y = 340 )

    girisYap_btn = Button(frame, text="Giriş Yap", font=("Arial", 8, "bold italic"), fg='white',
                          bg="#9A3223",
                          activebackground='green'
                          , activeforeground='white', bd=5, width=8, height=2, compound='left',command=giris_ekrani)
    girisYap_btn.place(x= 330 ,y = 360 )

def frame_temizle(frame):

    for widget in frame.winfo_children():
        widget.destroy()

def kullanici_anasayfa_ekrani(sonuc,giris_cursor,db):

    kitap_img = PhotoImage(file='kitap_anasayfa.png')
    kitap_img = kitap_img.subsample(6,8)

    anasayfa = Toplevel()
    
    anasayfa.geometry("850x550")
    anasayfa.configure(bg="#2A2322")
    anasayfa.title("Kütüphane Otomasyonu")
    anasayfa.resizable(False,False)
    global frame2
    frame2 = Frame(anasayfa,width=850,height=550)
    frame2.place(x=0,y=0)
    baslik_frame = Frame(frame2,width=850,height=75,bg="#1F77A9",relief="groove",bd=3)
    baslik_frame.place(x=0,y=0)

    adres_label = Label(frame2,text="Kütüphane Otomasyonu", font=("Arial", 25, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    adres_label.place(x=210,y=15)
    altBaslik_frame = Frame(frame2,width=850,height=65,bg="#9A3223",relief="groove",bd=3)
    altBaslik_frame.place(x=0,y=75)

    giris_cursor.execute("SELECT ad,soyad,id FROM kayıtlı_kişiler where kullanıcı_adı= '"+ str(kullaniciAdi) +"';")
    isim = giris_cursor.fetchall()

    altBaslik_label = Label(altBaslik_frame,bg="#9A3223",font=("Arial", 16, "bold italic"),text="Ad-Soyad: " +isim[0][0]+" "+isim[0][1]+" (id="+str(isim[0][2])+")",fg="white")
    altBaslik_label.place(x=5,y=15)
    
    tarih_label = Label(altBaslik_frame,bg="#9A3223",font=("Arial", 16, "bold italic"),text="Tarih: " +date,fg="white")
    tarih_label.place(x=650,y=15)

    anaKisim_frame = Frame(frame2,width=850,height=410,relief="groove",bd=5)
    anaKisim_frame.place(x=0,y=140)

    kullanici_ana_kisim(sonuc,anaKisim_frame,kitap_img,db)

def kullanici_ana_kisim(sonuc,anaKisim_frame,kitap_img,db):


    image_label = Label(anaKisim_frame,image=kitap_img)
    image_label.image = kitap_img
    image_label.pack()
    kitapListe_btn = Button(anaKisim_frame, text="Kitap Listesi", font=("Arial", 12, "bold italic"), fg='white',
                          bg="#1F77A9",
                          activebackground='green'
                          , activeforeground='white', bd=8, width=12, height=2, compound='left',command = lambda: kitapListe_ekrani(anaKisim_frame,giris_cursor,sonuc,kitap_img,db))
    kitapListe_btn.place(x= 30 ,y = 30 )

    kitapGecmisim_btn = Button(anaKisim_frame, text="Kitap Geçmişim", font=("Arial", 12, "bold italic"), fg='white',
                          bg="#1F77A9",
                          activebackground='green'
                          , activeforeground='white', bd=8, width=12, height=2, compound='left',command = lambda: kitapGecmisim_ekrani(sonuc,anaKisim_frame,giris_cursor,kitap_img,db))
    kitapGecmisim_btn.place(x= 200 ,y = 30 )

def kitapListe_ekrani(frame,giris_cursor,sonuc,kitap_img,db):

    frame_temizle(frame)
    giris_cursor.execute('SELECT * FROM kitaplar')
    rows = giris_cursor.fetchall()
    style =ttk.Style()
    style.theme_use('default')
    
    style.configure("Treeview",
	background="#D3D3D3",
	foreground="black",
	rowheight=25,
	fieldbackground="#1F77A9")
    style.map('Treeview',background=[('selected', "#347083")])

    tree_frame = Frame(frame,width=850,bg="#1F77A9")
    tree_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT,fill=Y)

    my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,selectmode="extended",height=200)
    my_tree.pack(pady=(30,100),padx=(0,0))

    tree_scroll.config(command=my_tree.yview)

    my_tree['columns'] = ("Kitap ID", "Kitap Adı", "Yazar", "Basım Evi", "Basım Yılı", "Toplam Adet", "Mevcut Adet")

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Kitap ID", anchor=W, width=60)
    my_tree.column("Kitap Adı", anchor=W, width=100)
    my_tree.column("Yazar", anchor=CENTER, width=100)
    my_tree.column("Basım Evi", anchor=CENTER, width=140)
    my_tree.column("Basım Yılı", anchor=CENTER, width=140)
    my_tree.column("Toplam Adet", anchor=CENTER, width=100)
    my_tree.column("Mevcut Adet", anchor=CENTER, width=100)

    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("Kitap ID", text="Kitap ID", anchor=W)
    my_tree.heading("Kitap Adı", text="Kitap Adı", anchor=W)
    my_tree.heading("Yazar", text="Yazar", anchor=CENTER)
    my_tree.heading("Basım Evi", text="Basım Evi", anchor=CENTER)
    my_tree.heading("Basım Yılı", text="Basım Yılı", anchor=CENTER)
    my_tree.heading("Toplam Adet", text="Toplam Adet", anchor=CENTER)
    my_tree.heading("Mevcut Adet", text="Mevcut Adet", anchor=CENTER)
    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")

    global count
    count = 0
    for row in rows:
        if count%2 == 0:
            my_tree.insert("", index="end", text="", values=row,tags=('evenrow',))
        else:
            my_tree.insert("", index="end", text="", values=row,tags=('oddrow',))
        count += 1

        geriDon_btn = Button(frame, text="Anasayfaya Dön", font=("Arial", 12, "bold italic"), fg='white',
                          bg="#9A3223",
                          activebackground='green'
                          , activeforeground='white', bd=8, width=13, height=2, compound='left',command = lambda: geri_don(sonuc,frame,kitap_img,db))
    geriDon_btn.place(x= 330 ,y = 330)



def kitapGecmisim_ekrani(sonuc,anaKisim_frame,giris_cursor,kitap_img,db):

    frame_temizle(anaKisim_frame)

    giris_cursor.execute(f'SELECT kitap_adı,alma_tarihi,teslim_tarihi FROM kitap_geçmişi where kullanıcı_id ={sonuc[0]}')
    rows = giris_cursor.fetchall()
    style =ttk.Style()
    style.theme_use('default')
    
    style.configure("Treeview",
	background="#D3D3D3",
	foreground="black",
	rowheight=25,
	fieldbackground="#1F77A9")
    style.map('Treeview',background=[('selected', "#347083")])

    tree_frame = Frame(anaKisim_frame,width=850,bg="#1F77A9")
    tree_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT,fill=Y)

    my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,selectmode="extended")
    my_tree.pack(pady=(30,100),padx=(0,0))

    tree_scroll.config(command=my_tree.yview)

    my_tree['columns'] = ("Kitap Adı", "Alma Tarihi", "Teslim Tarihi")

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Kitap Adı", anchor=CENTER, width=200)
    my_tree.column("Alma Tarihi", anchor=CENTER, width=150)
    my_tree.column("Teslim Tarihi", anchor=CENTER, width=150)

    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("Kitap Adı", text="Kitap Adı", anchor=CENTER)
    my_tree.heading("Alma Tarihi", text="Alma Tarihi", anchor=CENTER)
    my_tree.heading("Teslim Tarihi", text="Teslim Tarihi", anchor=CENTER)

    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")

    global count
    count = 0
    for row in rows:
        if count%2 == 0:
            my_tree.insert("", index="end", text="", values=row,tags=('evenrow',))
        else:
            my_tree.insert("", index="end", text="", values=row,tags=('oddrow',))
        count += 1

    geriDon_btn = Button(anaKisim_frame, text="Anasayfaya Dön", font=("Arial", 12, "bold italic"), fg='white',
                          bg="#9A3223",
                          activebackground='green'
                          , activeforeground='white', bd=8, width=13, height=2, compound='left',command = lambda: geri_don(sonuc,anaKisim_frame,kitap_img,db))
    geriDon_btn.place(x= 330 ,y = 320 )

def geri_don(sonuc,frame,kitap_img,db):

    frame_temizle(frame)
    if(sonuc[3]=="kullanıcı"):
        kullanici_ana_kisim(sonuc,frame,kitap_img,db)
    else:
        yonetici_ana_kisim(sonuc,frame,kitap_img,db)
    
def yonetici_anasayfa_ekrani(sonuc,giris_cursor,db):

    kitap_img = PhotoImage(file='kitap_anasayfa.png')
    kitap_img = kitap_img.subsample(6,8)

    anasayfa = Toplevel()
    
    anasayfa.geometry("850x550")
    anasayfa.configure(bg="#2A2322")
    anasayfa.title("Kütüphane Otomasyonu")
    anasayfa.resizable(False,False)
    global frame2
    frame2 = Frame(anasayfa,width=850,height=550)
    frame2.place(x=0,y=0)
    baslik_frame = Frame(frame2,width=850,height=75,bg="#1F77A9",relief="groove",bd=3)
    baslik_frame.place(x=0,y=0)
    adres_label = Label(frame2,text="Kütüphane Otomasyonu", font=("Arial", 25, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    adres_label.place(x=210,y=15)
    altBaslik_frame = Frame(frame2,width=850,height=65,bg="#9A3223",relief="groove",bd=3)
    altBaslik_frame.place(x=0,y=75)

    giris_cursor.execute("SELECT ad,soyad,id FROM kayıtlı_kişiler where kullanıcı_adı= '"+ str(kullaniciAdi) +"';")
    isim = giris_cursor.fetchall()

    
    altBaslik_label = Label(altBaslik_frame,bg="#9A3223",font=("Arial", 16, "bold italic"),text="Ad-Soyad: " +str(isim[0][0])+" "+str(isim[0][0])+" (id="+str(isim[0][2])+")",fg="white")
    altBaslik_label.place(x=15,y=15)
    
    tarih_label = Label(altBaslik_frame,bg="#9A3223",font=("Arial", 16, "bold italic"),text="Tarih: " +date,fg="white")
    tarih_label.place(x=650,y=15)

    anaKisim_frame = Frame(frame2,width=850,height=410,relief="groove",bd=5)
    anaKisim_frame.place(x=0,y=140)

    yonetici_ana_kisim(sonuc,anaKisim_frame,kitap_img,db)


def yonetici_ana_kisim(sonuc,anaKisim_frame,kitap_img,db):

    image_label = Label(anaKisim_frame,image=kitap_img)
    image_label.image = kitap_img
    image_label.pack()
    kitapListe_btn = Button(anaKisim_frame, text="Kitap Listesi", font=("Arial", 12, "bold italic"), fg='white',
                          bg="#1F77A9",
                          activebackground='green'
                          , activeforeground='white', bd=8, width=12, height=2, compound='left',command = lambda: kitapListe_ekrani(anaKisim_frame,giris_cursor,sonuc,kitap_img,db))
    kitapListe_btn.place(x= 30 ,y = 30 )

    kitapEkle_btn = Button(anaKisim_frame, text="Kitap Ekle", font=("Arial", 12, "bold italic"), fg='white',
                          bg="#1F77A9",
                          activebackground='green'
                          , activeforeground='white', bd=8, width=12, height=2, compound='left',command = lambda: kitapEkle_ekrani(sonuc,anaKisim_frame,kitap_img,giris_cursor,db))
    kitapEkle_btn.place(x= 200 ,y = 30 )

    kitapSil_btn = Button(anaKisim_frame, text="Kitap Sil", font=("Arial", 12, "bold italic"), fg='white',
                          bg="#1F77A9",
                          activebackground='green'
                          , activeforeground='white', bd=8, width=12, height=2, compound='left',command = lambda: kitapSil_ekrani(sonuc,anaKisim_frame,kitap_img,giris_cursor,db))
    kitapSil_btn.place(x= 370 ,y = 30 )

    kitapVer_btn = Button(anaKisim_frame, text="Kitap Ver", font=("Arial", 12, "bold italic"), fg='white',
                          bg="#1F77A9",
                          activebackground='green'
                          , activeforeground='white', bd=8, width=8, height=2, compound='left',command = lambda: kitapVer_ekrani(sonuc,anaKisim_frame,kitap_img,giris_cursor,db))
    kitapVer_btn.place(x= 30 ,y = 110 )

    kitapTeslim_btn = Button(anaKisim_frame, text="Kitap Teslim", font=("Arial", 12, "bold italic"), fg='white',
                          bg="#1F77A9",
                          activebackground='green'
                          , activeforeground='white', bd=8, width=10, height=2, compound='left',command = lambda: kitapTeslim_ekrani(sonuc,anaKisim_frame,kitap_img,giris_cursor,db))
    kitapTeslim_btn.place(x= 150 ,y = 110 )

    uyeListesi_btn = Button(anaKisim_frame, text="Üye Listesi", font=("Arial", 12, "bold italic"), fg='white',
                          bg="#1F77A9",
                          activebackground='green'
                          , activeforeground='white', bd=8, width=8, height=2, compound='left',command = lambda: uyeListesi_ekrani(anaKisim_frame,giris_cursor,sonuc,kitap_img,db))
    uyeListesi_btn.place(x= 290 ,y = 110 )

    uyeSil_btn = Button(anaKisim_frame, text="Üye Sil", font=("Arial", 12, "bold italic"), fg='white',
                          bg="#1F77A9",
                          activebackground='green'
                          , activeforeground='white', bd=8, width=8, height=2, compound='left',command = lambda: uyeSil_ekrani(sonuc,anaKisim_frame,kitap_img,giris_cursor,db))
    uyeSil_btn.place(x= 410 ,y = 110 )

    yoneticiListesi_btn = Button(anaKisim_frame, text="Yönetici Listesi", font=("Arial", 12, "bold italic"), fg='white',
                          bg="#1F77A9",
                          activebackground='green'
                          , activeforeground='white', bd=8, width=12, height=2, compound='left',command = lambda: yoneticiListesi_ekrani(anaKisim_frame,giris_cursor,sonuc,kitap_img,db))
    yoneticiListesi_btn.place(x= 30 ,y = 190 )

    yoneticiEkle_btn = Button(anaKisim_frame, text="Yönetici Ekle", font=("Arial", 12, "bold italic"), fg='white',
                          bg="#1F77A9",
                          activebackground='green'
                          , activeforeground='white', bd=8, width=12, height=2, compound='left',command = lambda: yoneticiEkle_ekrani(anaKisim_frame,giris_cursor,sonuc,kitap_img,db))
    yoneticiEkle_btn.place(x= 200 ,y = 190 )

    yoneticiSil_btn = Button(anaKisim_frame, text="Yönetici Sil", font=("Arial", 12, "bold italic"), fg='white',
                          bg="#1F77A9",
                          activebackground='green'
                          , activeforeground='white', bd=8, width=12, height=2, compound='left',command = lambda: yoneticiSil_ekrani(anaKisim_frame,giris_cursor,sonuc,kitap_img,db))
    yoneticiSil_btn.place(x= 370 ,y = 190 )

def kitapEkle_ekrani(sonuc,frame,kitap_img,giris_cursor,db):

    frame_temizle(frame)

    kitapEkle_frame = Frame(frame,width=850,bg="#1F77A9")
    kitapEkle_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    kitapAdi_label = Label(kitapEkle_frame,text="Kitap Adı:", font=("Arial", 12, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    kitapAdi_label.place(x=220,y=20)

    kitapAdi_entry = Entry(kitapEkle_frame,width=15,font="Arial")
    kitapAdi_entry.place(x=370,y=22)

    yazar_label = Label(kitapEkle_frame,text="Kitabın Yazarı:", font=("Arial", 12, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    yazar_label.place(x=220,y=60)

    yazar_entry = Entry(kitapEkle_frame,width=15,font="Arial")
    yazar_entry.place(x=370,y=62)

    basimEvi_label = Label(kitapEkle_frame,text="Basım Evi:", font=("Arial", 12, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    basimEvi_label.place(x=220,y=100)

    basimEvi_entry = Entry(kitapEkle_frame,width=15,font="Arial")
    basimEvi_entry.place(x=370,y=102)

    basimYili_label = Label(kitapEkle_frame,text="Basım Yılı:", font=("Arial", 12, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    basimYili_label.place(x=220,y=140)

    basimYili_entry = Entry(kitapEkle_frame,width=15,font="Arial")
    basimYili_entry.place(x=370,y=142)

    toplamAdet_label = Label(kitapEkle_frame,text="Adet:", font=("Arial", 12, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    toplamAdet_label.place(x=220,y=180)

    toplamAdet_entry = Entry(kitapEkle_frame,width=15,font="Arial")
    toplamAdet_entry.place(x=370,y=182)

    geriDon_btn = Button(kitapEkle_frame, text="<Anasayfa", font=("Arial", 10, "bold italic"), fg='white',
                          bg="#9A3223",
                          activebackground='green'
                          , activeforeground='white', bd=5, width=9, height=2, compound='left',command = lambda: yonetici_ana_kisim(sonuc,frame,kitap_img,db))
    geriDon_btn.place(x= 10 ,y = 10 )

    kitapKaydet_btn = Button(kitapEkle_frame, text="Kaydet", font=("Arial", 12, "bold italic"), fg='white',
                          bg="#9A3223",
                          activebackground='green'
                          , activeforeground='white', bd=8, width=12, height=2, compound='left',command = lambda: kitap_kaydet_baslat(kitapEkle_frame,db,giris_cursor,kitapAdi_entry.get(),yazar_entry.get(),basimEvi_entry.get(),basimYili_entry.get(),toplamAdet_entry.get()))
    kitapKaydet_btn.place(x= 370 ,y = 230 )

def kitap_kaydet(kitapEkle_frame,db,giris_cursor,kitapAdi,yazar,basimEvi,basimYili,toplamAdet):

    komut = 'INSERT INTO kitaplar VALUES(?,?,?,?,?,?)'
    veriler = (kitapAdi,yazar,basimEvi,basimYili,toplamAdet,toplamAdet)
    try:
        giris_cursor.execute(komut,veriler)
        db.commit()
        messagebox.showinfo("Başarılı","Kitap başarılı bir şekilde kaydedildi.")

    except:
        messagebox.showerror("Hata","Kitap veritabanına kayıt edilirken hata oluştu,girdiğiniz verileri kontrol ediniz.")   

def kitap_kaydet_baslat(kitapEkle_frame,db,giris_cursor,kitapAdi,yazar,basimEvi,basimYili,toplamAdet):

    x = threading.Thread(target=kitap_kaydet,args=(kitapEkle_frame,db,giris_cursor,kitapAdi,yazar,basimEvi,basimYili,toplamAdet))
    x.start()

def kitapSil_ekrani(sonuc,anaKisim_frame,kitap_img,giris_cursor,db):

    frame_temizle(anaKisim_frame)

    kitapSil_frame = Frame(anaKisim_frame,width=850,bg="#1F77A9")
    kitapSil_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    bilgi_label = Label(kitapSil_frame,text="Silmek istediğiniz kitabın id'sini giriniz.", font=("Arial", 15, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    bilgi_label.place(x=200,y=90)

    kitapId_label = Label(kitapSil_frame,text="Kitap ID:", font=("Arial", 12, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    kitapId_label.place(x=220,y=130)

    kitapId_entry = Entry(kitapSil_frame,width=15,font="Arial")
    kitapId_entry.place(x=370,y=132)

    kitapSil_btn = Button(kitapSil_frame, text="Sil", font=("Arial", 12, "bold italic"), fg='white',
                          bg="#9A3223",
                          activebackground='green'
                          , activeforeground='white', bd=8, width=12, height=2, compound='left',command = lambda: kitap_sil_baslat(kitapSil_frame,db,giris_cursor,kitapId_entry.get()))
    kitapSil_btn.place(x= 320 ,y = 180 )

    geriDon_btn = Button(kitapSil_frame, text="<Anasayfa", font=("Arial", 10, "bold italic"), fg='white',
                          bg="#9A3223",
                          activebackground='green'
                          , activeforeground='white', bd=5, width=9, height=2, compound='left',command = lambda: yonetici_ana_kisim(sonuc,anaKisim_frame,kitap_img,db))
    geriDon_btn.place(x= 10 ,y = 10 )

def kitap_sil(frame,db,giris_cursor,id):

    try:
        giris_cursor.execute("SELECT COUNT(*) FROM kitaplar WHERE kitap_id = ?", (id,))
        if giris_cursor.fetchone()[0] == 0:
            messagebox.showerror("Hata","Veritabanında girilen Id'ye sahip bir kitap bulunamadı.")  

        else:
            giris_cursor.execute('DELETE FROM kitaplar WHERE kitap_id =?',(id,))
            db.commit()
            messagebox.showinfo("Başarılı","Kitap başarılı bir şekilde silindi.")
    except:
        messagebox.showerror("Hata","Kitabı silerken bir hata oluştu lütfen girdiğiniz kitap id'yi kontrol ediniz.")

def kitap_sil_baslat(frame,db,giris_cursor,id):

    x = threading.Thread(target=kitap_sil,args=(frame,db,giris_cursor,id))
    x.start()

def kitapVer_ekrani(sonuc,anaKisim_frame,kitap_img,giris_cursor,db):

    frame_temizle(anaKisim_frame)

    kitapVer_frame = Frame(anaKisim_frame,width=850,bg="#1F77A9")
    kitapVer_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    bilgi_label = Label(kitapVer_frame,text="Verilecek kitabın id'sini ve kitabı alacak kullanıcının id'sini giriniz.", font=("Arial", 15, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    bilgi_label.place(x=110,y=70)

    kitapId_label = Label(kitapVer_frame,text="Kitap ID:", font=("Arial", 12, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    kitapId_label.place(x=220,y=120)

    kitapId_entry = Entry(kitapVer_frame,width=15,font="Arial")
    kitapId_entry.place(x=370,y=122)

    kullaniciId_label = Label(kitapVer_frame,text="Kullanıcı ID:", font=("Arial", 12, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    kullaniciId_label.place(x=220,y=190)

    kullaniciId_entry = Entry(kitapVer_frame,width=15,font="Arial")
    kullaniciId_entry.place(x=370,y=192)

    kitapVer_btn = Button(kitapVer_frame, text="Kitabı Ver", font=("Arial", 12, "bold italic"), fg='white',
                          bg="#9A3223",
                          activebackground='green'
                          , activeforeground='white', bd=8, width=12, height=2, compound='left',command = lambda: kitap_ver_baslat(kitapVer_frame,db,giris_cursor,kitapId_entry.get(),kullaniciId_entry.get()))
    kitapVer_btn.place(x= 320 ,y = 262 )

    geriDon_btn = Button(kitapVer_frame, text="<Anasayfa", font=("Arial", 10, "bold italic"), fg='white',
                          bg="#9A3223",
                          activebackground='green'
                          , activeforeground='white', bd=5, width=9, height=2, compound='left',command = lambda: yonetici_ana_kisim(sonuc,anaKisim_frame,kitap_img,db))
    geriDon_btn.place(x= 10 ,y = 10 )

def kitap_ver(kitapVer_frame,db,giris_cursor,kitapId,kullaniciId):

    try:
        giris_cursor.execute("SELECT * FROM kitaplar WHERE kitap_id = ?", (kitapId,))
        sonuc = giris_cursor.fetchone()
        if sonuc == None:
            messagebox.showerror("Hata","Veritabanında girilen Id'ye sahip bir kitap bulunamadı.") 

        giris_cursor.execute("SELECT * FROM kayıtlı_kişiler WHERE id = ?", (kullaniciId,))
        sonuc2 = giris_cursor.fetchone()
        if sonuc2 == None:
            messagebox.showerror("Hata","Veritabanında girilen Id'ye sahip bir kullanıcı bulunamadı.") 

        else:
            if(sonuc[-1]>0):
                giris_cursor.execute('INSERT INTO kitap_geçmişi VALUES(?,?,?,?,?,?,?)',(kitapId,kullaniciId,sonuc2[4],sonuc2[5],sonuc[1],date,"-",))
                db.commit()
                giris_cursor.execute("UPDATE kitaplar SET mevcut_adet = ? WHERE kitap_id = ?",(sonuc[-1]-1,kitapId,))
                db.commit()
                messagebox.showinfo("Başarılı","Kitap başarılı bir şekilde kullanıcının kitap geçmişine eklendi.")

    except:
        messagebox.showerror("Hata","Kullanıcıya kitap verilirken bir hata oluştu lütfen girdiğiniz kitap id'yi kontrol ediniz.")

def kitap_ver_baslat(kitapVer_frame,db,giris_cursor,kitapId,kullaniciId):

    x = threading.Thread(target=kitap_ver,args=(kitapVer_frame,db,giris_cursor,kitapId,kullaniciId))
    x.start()

def kitapTeslim_ekrani(sonuc,anaKisim_frame,kitap_img,giris_cursor,db):
    
    frame_temizle(anaKisim_frame)

    kitapTeslim_frame = Frame(anaKisim_frame,width=850,bg="#1F77A9")
    kitapTeslim_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    bilgi_label = Label(kitapTeslim_frame,text="Teslim edilecek kitabın id'sini ve kitabı teslim eden kullanıcının id'sini giriniz.", font=("Arial", 15, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    bilgi_label.place(x=60,y=70)

    kitapId_label = Label(kitapTeslim_frame,text="Kitap ID:", font=("Arial", 12, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    kitapId_label.place(x=220,y=120)

    kitapId_entry = Entry(kitapTeslim_frame,width=15,font="Arial")
    kitapId_entry.place(x=370,y=122)

    kullaniciId_label = Label(kitapTeslim_frame,text="Kullanıcı ID:", font=("Arial", 12, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    kullaniciId_label.place(x=220,y=190)

    kullaniciId_entry = Entry(kitapTeslim_frame,width=15,font="Arial")
    kullaniciId_entry.place(x=370,y=192)

    kitapTeslim_btn = Button(kitapTeslim_frame, text="Kaydet", font=("Arial", 12, "bold italic"), fg='white',
                          bg="#9A3223",
                          activebackground='green'
                          , activeforeground='white', bd=8, width=12, height=2, compound='left',command = lambda: kitap_teslim_baslat(kitapTeslim_frame,db,giris_cursor,kitapId_entry.get(),kullaniciId_entry.get()))
    kitapTeslim_btn.place(x= 320 ,y = 262 )

    geriDon_btn = Button(kitapTeslim_frame, text="<Anasayfa", font=("Arial", 10, "bold italic"), fg='white',
                          bg="#9A3223",
                          activebackground='green'
                          , activeforeground='white', bd=5, width=9, height=2, compound='left',command = lambda: yonetici_ana_kisim(sonuc,anaKisim_frame,kitap_img,db))
    geriDon_btn.place(x= 10 ,y = 10 )

def kitap_teslim(kitapTeslim_frame,db,giris_cursor,kitapId,kullaniciId):
    try:
        giris_cursor.execute("SELECT * FROM kitap_geçmişi WHERE kitap_id = ? AND kullanıcı_id = ?", (kitapId,kullaniciId,))
        sonuc = giris_cursor.fetchone()
        giris_cursor.execute("SELECT * FROM kitaplar WHERE kitap_id = ?",(kitapId,))
        sonuc2 = giris_cursor.fetchone()
        if sonuc == None:
            messagebox.showerror("Hata","Girilen Id'lere göre kitap geçmişinde bir kayıt bulunamadı.") 
    
        else:
             giris_cursor.execute('UPDATE kitap_geçmişi SET teslim_tarihi = ? WHERE kitap_id = ? AND kullanıcı_id = ?',(date,kitapId,kullaniciId,))
             db.commit()
             giris_cursor.execute("UPDATE kitaplar SET mevcut_adet = ? WHERE kitap_id = ?",(sonuc2[-1]+1,kitapId,))
             db.commit()
             messagebox.showinfo("Başarılı","Kitap başarılı bir şekilde teslim edildi.")
    except:
        messagebox.showerror("Hata","Kitap teslim edilirken bir hata oluştu lütfen girdiğiniz verileri kontrol ediniz.")



def kitap_teslim_baslat(kitapTeslim_frame,db,giris_cursor,kitapId,kullaniciId):
    pass
    x = threading.Thread(target=kitap_teslim,args=(kitapTeslim_frame,db,giris_cursor,kitapId,kullaniciId))
    x.start()

def uyeListesi_ekrani(frame,giris_cursor,sonuc,kitap_img,db):

    frame_temizle(frame)
    giris_cursor.execute('SELECT id,kullanıcı_adı,ad,soyad,tel_no,adres,eposta,üyelik_tarihi,doğum_tarihi FROM kayıtlı_kişiler WHERE üyelik_tipi = ?',("kullanıcı",))
    rows = giris_cursor.fetchall()
    style =ttk.Style()
    style.theme_use('default')
    
    style.configure("Treeview",
	background="#D3D3D3",
	foreground="black",
	rowheight=25,
	fieldbackground="#1F77A9")
    style.map('Treeview',background=[('selected', "#347083")])

    tree_frame = Frame(frame,width=850,bg="#1F77A9")
    tree_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT,fill=Y)

    my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,selectmode="extended",height=200)
    my_tree.pack(pady=(30,100),padx=(0,0))

    tree_scroll.config(command=my_tree.yview)

    my_tree['columns'] = ("ID", "Kullanıcı Adı", "Ad", "Soyad", "Tel No", "Adres", "Eposta","Üyelik Tarihi","Doğum Tarihi")

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("ID", anchor=W, width=30)
    my_tree.column("Kullanıcı Adı", anchor=CENTER, width=100)
    my_tree.column("Ad", anchor=CENTER, width=100)
    my_tree.column("Soyad", anchor=CENTER, width=100)
    my_tree.column("Tel No", anchor=CENTER, width=90)
    my_tree.column("Adres", anchor=CENTER, width=100)
    my_tree.column("Eposta", anchor=CENTER, width=100)
    my_tree.column("Üyelik Tarihi", anchor=CENTER, width=70)
    my_tree.column("Doğum Tarihi", anchor=CENTER, width=80)


    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("ID", text="ID", anchor=W)
    my_tree.heading("Kullanıcı Adı", text="Kullanıcı Adı", anchor=CENTER)
    my_tree.heading("Ad", text="Ad", anchor=CENTER)
    my_tree.heading("Soyad", text="Soyad", anchor=CENTER)
    my_tree.heading("Tel No", text="Tel No", anchor=CENTER)
    my_tree.heading("Adres", text="Adres", anchor=CENTER)
    my_tree.heading("Eposta", text="Eposta", anchor=CENTER)
    my_tree.heading("Üyelik Tarihi", text="Üyelik Tarihi", anchor=CENTER)
    my_tree.heading("Doğum Tarihi", text="Doğum Tarihi", anchor=CENTER)
    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")

    global count
    count = 0
    for row in rows:
        if count%2 == 0:
            my_tree.insert("", index="end", text="", values=row,tags=('evenrow',))
        else:
            my_tree.insert("", index="end", text="", values=row,tags=('oddrow',))
        count += 1

    geriDon_btn = Button(frame, text="Anasayfaya Dön", font=("Arial", 12, "bold italic"), fg='white',
                          bg="#9A3223",
                          activebackground='green'
                          , activeforeground='white', bd=8, width=13, height=2, compound='left',command = lambda: yonetici_ana_kisim(sonuc,frame,kitap_img,db))
    geriDon_btn.place(x= 330 ,y = 330)

def uyeSil_ekrani(sonuc,anaKisim_frame,kitap_img,giris_cursor,db):

    frame_temizle(anaKisim_frame)

    uyeSil_frame = Frame(anaKisim_frame,width=850,bg="#1F77A9")
    uyeSil_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    bilgi_label = Label(uyeSil_frame,text="Silmek istediğiniz üyenin id'sini giriniz.", font=("Arial", 15, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    bilgi_label.place(x=200,y=90)

    uyeId_label = Label(uyeSil_frame,text="Kullanıcı ID:", font=("Arial", 12, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    uyeId_label.place(x=220,y=130)

    uyeId_entry = Entry(uyeSil_frame,width=15,font="Arial")
    uyeId_entry.place(x=370,y=132)

    kitapSil_btn = Button(uyeSil_frame, text="Sil", font=("Arial", 12, "bold italic"), fg='white',
                          bg="#9A3223",
                          activebackground='green'
                          , activeforeground='white', bd=8, width=12, height=2, compound='left',command = lambda: uye_sil(uyeSil_frame,db,giris_cursor,uyeId_entry.get()))
    kitapSil_btn.place(x= 320 ,y = 180 )

    geriDon_btn = Button(uyeSil_frame, text="<Anasayfa", font=("Arial", 10, "bold italic"), fg='white',
                          bg="#9A3223",
                          activebackground='green'
                          , activeforeground='white', bd=5, width=9, height=2, compound='left',command = lambda: yonetici_ana_kisim(sonuc,anaKisim_frame,kitap_img,db))
    geriDon_btn.place(x= 10 ,y = 10 )

def uye_sil(frame,db,giris_cursor,id):

    try:
        giris_cursor.execute("SELECT COUNT(*) FROM kayıtlı_kişiler WHERE id = ?", (id,))
        if giris_cursor.fetchone()[0] == 0:
            messagebox.showerror("Hata","Veritabanında girilen Id'ye sahip bir kullanıcı bulunamadı.")  

        else:
            giris_cursor.execute("SELECT * FROM kayıtlı_kişiler WHERE id = ?",(id,))
            sonuc = giris_cursor.fetchone()
            if(sonuc[3]=="kullanıcı"):
                giris_cursor.execute('DELETE FROM kayıtlı_kişiler WHERE id =?',(id,))
                db.commit()
                messagebox.showinfo("Başarılı","Üye başarılı bir şekilde silindi.")
            else:
                messagebox.showerror("Hata","Girdiğiniz ID'ye sahip kişi kullanıcı değildir.")
    except:
        messagebox.showerror("Hata","Kitabı silerken bir hata oluştu lütfen girdiğiniz kullanıcı id'yi kontrol ediniz.")


def yoneticiListesi_ekrani(frame,giris_cursor,sonuc,kitap_img,db):
    
    frame_temizle(frame)
    giris_cursor.execute('SELECT id,kullanıcı_adı,ad,soyad,tel_no,adres,eposta,üyelik_tarihi,doğum_tarihi FROM kayıtlı_kişiler WHERE üyelik_tipi = ?',("yönetici",))
    rows = giris_cursor.fetchall()
    style =ttk.Style()
    style.theme_use('default')
    
    style.configure("Treeview",
	background="#D3D3D3",
	foreground="black",
	rowheight=25,
	fieldbackground="#1F77A9")
    style.map('Treeview',background=[('selected', "#347083")])

    tree_frame = Frame(frame,width=850,bg="#1F77A9")
    tree_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT,fill=Y)

    my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,selectmode="extended",height=200)
    my_tree.pack(pady=(30,100),padx=(0,0))

    tree_scroll.config(command=my_tree.yview)

    my_tree['columns'] = ("ID", "Kullanıcı Adı", "Ad", "Soyad", "Tel No", "Adres", "Eposta","Üyelik Tarihi","Doğum Tarihi")

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("ID", anchor=W, width=30)
    my_tree.column("Kullanıcı Adı", anchor=CENTER, width=100)
    my_tree.column("Ad", anchor=CENTER, width=100)
    my_tree.column("Soyad", anchor=CENTER, width=100)
    my_tree.column("Tel No", anchor=CENTER, width=90)
    my_tree.column("Adres", anchor=CENTER, width=100)
    my_tree.column("Eposta", anchor=CENTER, width=100)
    my_tree.column("Üyelik Tarihi", anchor=CENTER, width=70)
    my_tree.column("Doğum Tarihi", anchor=CENTER, width=80)


    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("ID", text="ID", anchor=W)
    my_tree.heading("Kullanıcı Adı", text="Kullanıcı Adı", anchor=CENTER)
    my_tree.heading("Ad", text="Ad", anchor=CENTER)
    my_tree.heading("Soyad", text="Soyad", anchor=CENTER)
    my_tree.heading("Tel No", text="Tel No", anchor=CENTER)
    my_tree.heading("Adres", text="Adres", anchor=CENTER)
    my_tree.heading("Eposta", text="Eposta", anchor=CENTER)
    my_tree.heading("Üyelik Tarihi", text="Üyelik Tarihi", anchor=CENTER)
    my_tree.heading("Doğum Tarihi", text="Doğum Tarihi", anchor=CENTER)
    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")

    global count
    count = 0
    for row in rows:
        if count%2 == 0:
            my_tree.insert("", index="end", text="", values=row,tags=('evenrow',))
        else:
            my_tree.insert("", index="end", text="", values=row,tags=('oddrow',))
        count += 1

    geriDon_btn = Button(frame, text="Anasayfaya Dön", font=("Arial", 12, "bold italic"), fg='white',
                          bg="#9A3223",
                          activebackground='green'
                          , activeforeground='white', bd=8, width=13, height=2, compound='left',command = lambda: yonetici_ana_kisim(sonuc,frame,kitap_img,db))
    geriDon_btn.place(x= 330 ,y = 330)

def yoneticiEkle_ekrani(frame,giris_cursor,sonuc,kitap_img,db):

    frame_temizle(frame)

    yoneticiEkle_frame = Frame(frame,width=850,bg="#1F77A9")
    yoneticiEkle_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    kullaniciAdi_label = Label(yoneticiEkle_frame,text="Kullanıcı Adı:", font=("Arial", 12, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    kullaniciAdi_label.place(x=220,y=20)

    kullaniciAdi_entry = Entry(yoneticiEkle_frame,width=15,font="Arial")
    kullaniciAdi_entry.place(x=370,y=22)

    sifre_label = Label(yoneticiEkle_frame,text="Şifre:", font=("Arial", 12, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    sifre_label.place(x=220,y=60)

    sifre_entry = Entry(yoneticiEkle_frame,width=15,font="Arial")
    sifre_entry.place(x=370,y=62)

    ad_label = Label(yoneticiEkle_frame,text="Ad:", font=("Arial", 12, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    ad_label.place(x=220,y=100)

    ad_entry = Entry(yoneticiEkle_frame,width=15,font="Arial")
    ad_entry.place(x=370,y=102)

    soyad_label = Label(yoneticiEkle_frame,text="Soyad:", font=("Arial", 12, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    soyad_label.place(x=220,y=140)

    soyad_entry = Entry(yoneticiEkle_frame,width=15,font="Arial")
    soyad_entry.place(x=370,y=142)

    telNo_label = Label(yoneticiEkle_frame,text="Tel No:", font=("Arial", 12, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    telNo_label.place(x=220,y=180)

    telNo_entry = Entry(yoneticiEkle_frame,width=15,font="Arial")
    telNo_entry.place(x=370,y=182)

    adres_label = Label(yoneticiEkle_frame,text="Adres:", font=("Arial", 12, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    adres_label.place(x=220,y=220)

    adres_entry = Entry(yoneticiEkle_frame,width=15,font="Arial")
    adres_entry.place(x=370,y=222)

    eposta_label = Label(yoneticiEkle_frame,text="Eposta:", font=("Arial", 12, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    eposta_label.place(x=220,y=260)

    eposta_entry = Entry(yoneticiEkle_frame,width=15,font="Arial")
    eposta_entry.place(x=370,y=262)

    dogumTarihi_label = Label(yoneticiEkle_frame,text="Doğum Tarihi:", font=("Arial", 12, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    dogumTarihi_label.place(x=220,y=300)

    dogumTarihi_entry = Entry(yoneticiEkle_frame,width=15,font="Arial")
    dogumTarihi_entry.place(x=370,y=302)

    geriDon_btn = Button(yoneticiEkle_frame, text="<Anasayfa", font=("Arial", 10, "bold italic"), fg='white',
                          bg="#9A3223",
                          activebackground='green'
                          , activeforeground='white', bd=5, width=9, height=2, compound='left',command = lambda: yonetici_ana_kisim(sonuc,frame,kitap_img,db))
    geriDon_btn.place(x= 10 ,y = 10 )

    yoneticiKaydet_btn = Button(yoneticiEkle_frame, text="Kaydet", font=("Arial", 12, "bold italic"), fg='white',
                          bg="#9A3223",
                          activebackground='green'
                          , activeforeground='white', bd=8, width=12, height=2, compound='left',command = lambda: yonetici_kaydet(yoneticiEkle_frame,db,giris_cursor,kullaniciAdi_entry.get(),sifre_entry.get(),ad_entry.get(),soyad_entry.get(),telNo_entry.get(),adres_entry.get(),eposta_entry.get(),dogumTarihi_entry.get()))
    yoneticiKaydet_btn.place(x= 370 ,y = 340 )

def yonetici_kaydet(yoneticiEkle_frame,db,giris_cursor,kullaniciAdi,sifre,ad,soyad,telNo,adres,eposta,dogum_tarihi):

    komut = 'INSERT INTO kayıtlı_kişiler VALUES(?,?,?,?,?,?,?,?,?,?)'
    veriler = (kullaniciAdi,sifre,"yönetici",ad,soyad,telNo,adres,eposta,date,dogum_tarihi)
    try:
        giris_cursor.execute(komut,veriler)
        db.commit()
        messagebox.showinfo("Başarılı","Yönetici başarılı bir şekilde kaydedildi.")
    except:
        messagebox.showerror("Hata","Yönetici veritabanına kayıt edilirken hata oluştu.")   

def yoneticiSil_ekrani(anaKisim_frame,giris_cursor,sonuc,kitap_img,db):

    frame_temizle(anaKisim_frame)

    yoneticiSil_frame = Frame(anaKisim_frame,width=850,bg="#1F77A9")
    yoneticiSil_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    bilgi_label = Label(yoneticiSil_frame,text="Silmek istediğiniz yöneticinin id'sini giriniz.", font=("Arial", 15, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    bilgi_label.place(x=200,y=90)

    yoneticiId_label = Label(yoneticiSil_frame,text="Yönetici ID:", font=("Arial", 12, "bold italic"), bg="#1F77A9",fg="white",bd=5)
    yoneticiId_label.place(x=220,y=130)

    yoneticiId_entry = Entry(yoneticiSil_frame,width=15,font="Arial")
    yoneticiId_entry.place(x=370,y=132)

    yoneticiSil_btn = Button(yoneticiSil_frame, text="Sil", font=("Arial", 12, "bold italic"), fg='white',
                          bg="#9A3223",
                          activebackground='green'
                          , activeforeground='white', bd=8, width=12, height=2, compound='left',command = lambda: yonetici_sil(yoneticiSil_frame,db,giris_cursor,yoneticiId_entry.get()))
    yoneticiSil_btn.place(x= 320 ,y = 180 )

    geriDon_btn = Button(yoneticiSil_frame, text="<Anasayfa", font=("Arial", 10, "bold italic"), fg='white',
                          bg="#9A3223",
                          activebackground='green'
                          , activeforeground='white', bd=5, width=9, height=2, compound='left',command = lambda: yonetici_ana_kisim(sonuc,anaKisim_frame,kitap_img,db))
    geriDon_btn.place(x= 10 ,y = 10 )

def yonetici_sil(yoneticiSil_frame,db,giris_cursor,yoneticiId):

   try:
        giris_cursor.execute("SELECT COUNT(*) FROM kayıtlı_kişiler WHERE id = ?", (yoneticiId,))
        if giris_cursor.fetchone()[0] == 0:
            messagebox.showerror("Hata","Veritabanında girilen Id'ye sahip bir yönetici bulunamadı.")  

        else:
            giris_cursor.execute("SELECT * FROM kayıtlı_kişiler WHERE id = ?",(yoneticiId,))
            sonuc = giris_cursor.fetchone()
            if(sonuc[3]=="yönetici"):
                if(sonuc[1]!="admin"):
                    giris_cursor.execute('DELETE FROM kayıtlı_kişiler WHERE id =?',(yoneticiId,))
                    db.commit()
                    messagebox.showinfo("Başarılı","Yönetici başarılı bir şekilde silindi.")
                else:
                    messagebox.showerror("Hata","Admin kullanıcı adlı yönetici silinemez!")
            else:
                messagebox.showerror("Hata","Id'si girilen kişi yönetici değildir!")
   except:
        messagebox.showerror("Hata","Yöneticiyi silerken bir hata oluştu lütfen girdiğiniz yönetici id'yi kontrol ediniz.")
giris_ekrani()


giris.mainloop()
    