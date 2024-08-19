import tkinter as tk
from tkinter import messagebox, simpledialog
import json

class OkulSistemiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MEB | OKUL YÖNETİM")

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        self.ana_menu()

    def ana_menu(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        tk.Label(self.frame, text="OKUL YÖNETİM SİSTEMİ", font=("Impact", 16)).pack()
        tk.Label(self.frame, text="by toprak efe", font=("Arial", 8)).pack()

        tk.Button(self.frame, text="Öğrenci Girişi", command=self.ogrenci_giris).pack(pady=5)
        tk.Button(self.frame, text="Yönetici Girişi", command=self.yonetici_giris).pack(pady=5)
        tk.Button(self.frame, text="Uygulamayı Kapat", command=self.root.quit).pack(pady=5)

    def ogrenci_giris(self):
        self.frame.destroy()
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=50, padx=20)

        tk.Label(self.frame, text="Öğrenci Numarası", font=("Arial", 12)).pack()
        self.no_entry = tk.Entry(self.frame)
        self.no_entry.pack(pady=5)
        tk.Button(self.frame, text="Giriş Yap", command=self.ogrenci_giris_check).pack(pady=5)

        tk.Button(self.frame, text="Ana Menü", command=self.ana_menu).pack(pady=5)

    def ogrenci_giris_check(self):
        no = int(self.no_entry.get())
        sifre = simpledialog.askstring("Şifre", "Şifrenizi Giriniz:")

        try:
            with open('ogrenci.json', 'r+', encoding='utf-8') as f:
                ogrenci = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Hata", "Öğrenci verileri bulunamadı!")
            return

        ogrenci_id = next((ogr for ogr in ogrenci['ogrenci'] if ogr['no'] == no), None)

        if ogrenci_id is None:
            messagebox.showerror("Hata", "Numara kayıtlı değil")
        elif ogrenci_id['sifre'] != sifre:
            messagebox.showerror("Hata", "Yanlış şifre")
        else:
            self.ogrenci_menu(ogrenci_id)

    def ogrenci_menu(self, ogrenci_id):
        self.frame.destroy()
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        tk.Label(self.frame, text=" Öğrenci Menüsü ", font=("Impact", 16)).pack()

        tk.Button(self.frame, text="Notlarını Görüntüle", command=lambda: self.notlarini_goruntule(ogrenci_id)).pack(pady=5)
        tk.Button(self.frame, text="Devamsızlık Bilgisini Görüntüle", command=lambda: self.devamsizlik_goruntule(ogrenci_id)).pack(pady=5)
        tk.Button(self.frame, text="Kişisel Bilgilerimi Güncelle", command=lambda: self.kisisel_bilgiler_guncelle(ogrenci_id)).pack(pady=5)
        tk.Button(self.frame, text="Şifre Değiştir", command=lambda: self.sifre_degistir(ogrenci_id)).pack(pady=5)
        tk.Button(self.frame, text="Sınav Sonuçlarımı Görüntüle", command=lambda: messagebox.showinfo("Bilgi", "Sınav sonuçları şu anda mevcut değil.")).pack(pady=5)
        tk.Button(self.frame, text="Bildirimler ve Duyurular", command=lambda: messagebox.showinfo("Bilgi", "Bildirimler ve Duyurular şu anda mevcut değil.")).pack(pady=5)
        tk.Button(self.frame, text="Ana Menü", command=self.ana_menu).pack(pady=5)

    def notlarini_goruntule(self, ogrenci_id):
        ortalama = (ogrenci_id['fen'] + ogrenci_id['mat'] + ogrenci_id['turkce'] + ogrenci_id['sosyal'] + ogrenci_id['din'] + ogrenci_id['ydil']) / 6
        notlar = f"Matematik: {ogrenci_id['mat']}\nFen: {ogrenci_id['fen']}\nTürkçe: {ogrenci_id['turkce']}\nSosyal Bilgiler: {ogrenci_id['sosyal']}\nDin Kültürü: {ogrenci_id['din']}\nYabancı Dil: {ogrenci_id['ydil']}\nOrtalama: {ortalama:.2f}"
        messagebox.showinfo("Notlar", notlar)

    def devamsizlik_goruntule(self, ogrenci_id):
        messagebox.showinfo("Devamsızlık Bilgisi", f"Devamsızlık: {ogrenci_id['devamsizlik']} gün")

    def kisisel_bilgiler_guncelle(self, ogrenci_id):
        yeni_ad = simpledialog.askstring("Yeni Ad", f"Yeni Adınız (mevcut: {ogrenci_id['ad']}):")
        yeni_sinif = simpledialog.askstring("Yeni Sınıf", f"Yeni Sınıfınız (mevcut: {ogrenci_id['sinif']}):")

        if yeni_ad:
            ogrenci_id['ad'] = yeni_ad
        if yeni_sinif:
            ogrenci_id['sinif'] = yeni_sinif

        self.update_ogrenci_json(ogrenci_id)
        messagebox.showinfo("Başarı", "Kişisel bilgiler başarıyla güncellendi.")

    def sifre_degistir(self, ogrenci_id):
        yeni_sifre = simpledialog.askstring("Yeni Şifre", "Yeni Şifrenizi Giriniz:")
        ogrenci_id['sifre'] = yeni_sifre
        self.update_ogrenci_json(ogrenci_id)
        messagebox.showinfo("Başarı", "Şifreniz başarıyla güncellendi.")

    def update_ogrenci_json(self, ogrenci_id):
        try:
            with open('ogrenci.json', 'r+', encoding='utf-8') as f:
                ogrenci_data = json.load(f)
        except FileNotFoundError:
            ogrenci_data = {"ogrenci": []}

        for i, ogr in enumerate(ogrenci_data['ogrenci']):
            if ogr['no'] == ogrenci_id['no']:
                ogrenci_data['ogrenci'][i] = ogrenci_id
                break

        with open('ogrenci.json', 'w', encoding='utf-8') as f:
            json.dump(ogrenci_data, f, indent=4)

    def yonetici_giris(self):
        self.frame.destroy()
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        tk.Label(self.frame, text="Yönetici TC Kimlik No", font=("Arial", 12)).pack()
        self.tc_entry = tk.Entry(self.frame)
        self.tc_entry.pack(pady=5)
        tk.Button(self.frame, text="Giriş Yap", command=self.yonetici_giris_check).pack(pady=5)

        tk.Button(self.frame, text="Ana Menü", command=self.ana_menu).pack(pady=5)

    def yonetici_giris_check(self):
        tc_no = self.tc_entry.get()
        sifre = simpledialog.askstring("Şifre", "Şifrenizi Giriniz:")

        try:
            with open('yonetici.json', 'r+', encoding='utf-8') as f:
                yonetici = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Hata", "Yönetici verileri bulunamadı!")
            return

        yonetici_id = next((yon for yon in yonetici['yonetici'] if yon['tc'] == tc_no), None)

        if yonetici_id is None:
            messagebox.showerror("Hata", "TC Kimlik No kayıtlı değil")
        elif yonetici_id['sifre'] != sifre:
            messagebox.showerror("Hata", "Yanlış şifre")
        else:
            self.yonetici_menu(yonetici_id)

    def yonetici_menu(self, yonetici_id):
        self.frame.destroy()
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        tk.Label(self.frame, text=" Yönetici Menüsü ", font=("Impact", 16)).pack()

        tk.Button(self.frame, text="Öğrencileri Görüntüle", command=self.ogrenci_goruntule).pack(pady=5)
        tk.Button(self.frame, text="Öğrenci Ekle", command=self.yeni_ogrenci_ekle).pack(pady=5)
        tk.Button(self.frame, text="Kayıtlı Olan Öğrenciyi Sil", command=self.ogrenci_sil).pack(pady=5)
        tk.Button(self.frame, text="Not Düzenle", command=self.not_duzenle).pack(pady=5)
        tk.Button(self.frame, text="Çıkış Yap", command=self.ana_menu).pack(pady=5)

    def ogrenci_goruntule(self):
        no = simpledialog.askinteger("Öğrenci No", "Öğrencinin Numarasını Giriniz:")
        try:
            with open('ogrenci.json', 'r+', encoding='utf-8') as f:
                ogrenci = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Hata", "Öğrenci verileri bulunamadı!")
            return

        ogrenci_id = next((ogr for ogr in ogrenci['ogrenci'] if ogr['no'] == no), None)

        if ogrenci_id is None:
            messagebox.showerror("Hata", "Numara kayıtlı değil")
        else:
            ortalama = (ogrenci_id['fen'] + ogrenci_id['mat'] + ogrenci_id['turkce'] + ogrenci_id['sosyal'] + ogrenci_id['din'] + ogrenci_id['ydil']) / 6
            bilgi = f"Öğrencinin Adı: {ogrenci_id['ad']}\nÖğrencinin Sınıfı: {ogrenci_id['sinif']}\nÖğrencinin Numarası: {ogrenci_id['no']}\nÖğrencinin Not Ortalaması: {ortalama:.2f}\nÖğrencinin Devamsızlık Bilgisi: {ogrenci_id['devamsizlik']} Gün"
            messagebox.showinfo("Öğrenci Bilgileri", bilgi)

    def yeni_ogrenci_ekle(self):
        no = simpledialog.askinteger("Öğrenci No", "Öğrenci No:")
        sifre = simpledialog.askstring("Şifre", "Şifre Belirleyiniz:")
        ad = simpledialog.askstring("Ad", "Öğrencinin Adını Giriniz:")
        mat = simpledialog.askinteger("Matematik Notu", "Matematik Notu:")
        fen = simpledialog.askinteger("Fen Notu", "Fen Notu:")
        turkce = simpledialog.askinteger("Türkçe Notu", "Türkçe Notu:")
        sosyal = simpledialog.askinteger("Sosyal Notu", "Sosyal Notu:")
        din = simpledialog.askinteger("Din Notu", "Din Notu:")
        ydil = simpledialog.askinteger("Yabancı Dil Notu", "Yabancı Dil Notu:")
        devamsizlik = simpledialog.askinteger("Devamsızlık", "Devamsızlık Sayısı:")
        sinif = simpledialog.askstring("Sınıf", "Öğrencinin Sınıfını Giriniz:")

        yeni_ogrenci = {
            "no": no,
            "sifre": sifre,
            "ad": ad,
            "mat": mat,
            "fen": fen,
            "turkce": turkce,
            "sosyal": sosyal,
            "din": din,
            "ydil": ydil,
            "devamsizlik": devamsizlik,
            "sinif": sinif
        }

        try:
            with open('ogrenci.json', 'r+', encoding='utf-8') as f:
                ogrenci = json.load(f)
        except FileNotFoundError:
            ogrenci = {"ogrenci": []}
        
        ogrenci['ogrenci'].append(yeni_ogrenci)
        
        with open('ogrenci.json', 'w', encoding='utf-8') as f:
            json.dump(ogrenci, f, indent=4)
        
        messagebox.showinfo("Başarı", f"{ad} adlı öğrenci {no} numarası ile dataya kayıt edildi")

    def ogrenci_sil(self):
        no = simpledialog.askinteger("Öğrenci No", "Silinecek Öğrencinin No'sunu Giriniz:")
        
        try:
            with open('ogrenci.json', 'r+', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Hata", "Öğrenci verileri bulunamadı!")
            return
        
        data['ogrenci'] = [ogrenci for ogrenci in data['ogrenci'] if ogrenci['no'] != no]
        
        with open('ogrenci.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        
        messagebox.showinfo("Başarı", f"{no} Nolu Öğrencinin verileri silindi.")

    def not_duzenle(self):
        no = simpledialog.askinteger("Öğrenci No", "Notlarını düzenlemek istediğiniz öğrencinin numarasını giriniz:")
        
        try:
            with open('ogrenci.json', 'r+', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Hata", "Öğrenci verileri bulunamadı!")
            return
        
        ogrenci_id = next((ogrenci for ogrenci in data['ogrenci'] if ogrenci['no'] == no), None)

        if ogrenci_id is None:
            messagebox.showerror("Hata", "Girdiğiniz No'lu bir öğrenci bulunamadı.")
        else:
            mat = simpledialog.askinteger("Yeni Matematik Notu", "Yeni Matematik Notu:")
            fen = simpledialog.askinteger("Yeni Fen Notu", "Yeni Fen Notu:")
            turkce = simpledialog.askinteger("Yeni Türkçe Notu", "Yeni Türkçe Notu:")
            sosyal = simpledialog.askinteger("Yeni Sosyal Bilgiler Notu", "Yeni Sosyal Bilgiler Notu:")
            din = simpledialog.askinteger("Yeni Din Kültürü Notu", "Yeni Din Kültürü Notu:")
            ydil = simpledialog.askinteger("Yeni Yabancı Dil Notu", "Yeni Yabancı Dil Notu:")

            ogrenci_id.update({
                "mat": mat,
                "fen": fen,
                "turkce": turkce,
                "sosyal": sosyal,
                "din": din,
                "ydil": ydil
            })

            with open('ogrenci.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)

            messagebox.showinfo("Başarı", "Notlar başarıyla güncellendi.")

if __name__ == "__main__":
    root = tk.Tk()
    app = OkulSistemiApp(root)
    root.mainloop()
