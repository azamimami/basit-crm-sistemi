 # ============ classlar ==========
class Musteri:
  def __init__(self,musteri_id, ad, soyad, telefon):
    self.musteri_id = musteri_id
    self.ad = ad
    self.soyad = soyad
    self.telefon = telefon


class Satis:
  def __init__(self,satis_id, musteri_id, urun, fiyat):
    self.satis_id = satis_id
    self.musteri_id = musteri_id
    self.urun = urun
    self.fiyat = fiyat


class DestekTalebi:
  def __init__(self,talep_id, musteri_id, aciklama):
    self.talep_id = talep_id
    self.musteri_id = musteri_id
    self.aciklama = aciklama


class CRM:
  def __init__(self):
    self.musteriler = {}
    self.satislar = {}
    self.destek_talepleri = []

    self.musteri_id_sayac = 1
    self.satis_id_sayac = 1
    self.talep_id_sayac = 1
 # ============ MUSTERI METODLARI ==========
  def musteri_ekle(self):
   ad = input("Ad; ")
   soyad = input("Soyad: ")
   telefon = int(input("Telefon: "))

   musteri_id = self.musteri_id_sayac
   self.musteri_id_sayac += 1

   self.musteriler[musteri_id] = Musteri( musteri_id ,ad, soyad, telefon)
   print(f"Musteri eklendi (ID: {musteri_id} Ad: {ad} Soyad: {soyad})")

  def musteri_sil(self):
    self.musterileri_goster()
    musteri_id = int(input("Musteri ID: "))

    if musteri_id in self.musteriler:
      del self.musteriler[musteri_id]
      print("Musteri silindi.")
    else:
      print("Musteri bulunamadi")

  def musterileri_goster(self):
    if not self.musteriler:
      print("Musteri listesi bos.")
      return
    for m in self.musteriler.values():
      print(f" Musteri ID: {m.musteri_id} adi: {m.ad} soyad: {m.soyad} Telefon: {m.telefon}")
 # ============ SATIS METODLARI ==========

  def satis_ekle(self):
    self.musterileri_goster()
    try:
        musteri_id = int(input("Musteri ID: "))
    except ValueError:
        print("Gecersiz ID")
        return

    if musteri_id not in self.musteriler:
        print("Musteri bulunamadi")
        return

    urun = input("Urun: ")

    try:
        fiyat = float(input("Fiyat: "))
    except ValueError:
        print("Gecersiz fiyat")
        return

    satis_id = self.satis_id_sayac
    self.satis_id_sayac += 1

    self.satislar[satis_id] = Satis(satis_id, musteri_id, urun, fiyat)

    print(f"Satis eklendi -> ID: {satis_id}")

  def satis_bul(self):
    try:
        satis_id = int(input("Satis ID: "))
    except ValueError:
        print("Gecersiz ID")
        return

    if satis_id in self.satislar:
        s = self.satislar[satis_id]
        print(f"Satis ID: {s.satis_id} | Musteri ID: {s.musteri_id} | Urun: {s.urun} | Fiyat: {s.fiyat} TL")
    else:
        print("Satis bulunamadi.")

  def satis_sil(self):
    try:
        satis_id = int(input("Satis ID: "))
    except ValueError:
        print("Gecersiz ID")
        return

    if satis_id in self.satislar:
        del self.satislar[satis_id]
        print(f"Satis silindi (ID: {satis_id})")
    else:
        print("Satis bulunamadi.")

  def satisleri_goster(self):
    if not self.satislar:
        print("Satis yok.")
        return

    for s in self.satislar.values():
        print(f"Satis ID: {s.satis_id} | Musteri ID: {s.musteri_id} | Urun: {s.urun} | Fiyat: {s.fiyat} TL")

 # ============ SATIS METODLARI ==========
  def destek_olustur(self):
    try:
        musteri_id = int(input("Musteri ID: "))
    except ValueError:
        print("Gecersiz ID")
        return

    if musteri_id not in self.musteriler:
        print("Hatali Musteri ID si.")
        return

    aciklama = input("Aciklama: ")

    talep_id = self.talep_id_sayac
    self.talep_id_sayac += 1

    self.destek_talepleri.append(
        DestekTalebi(talep_id, musteri_id, aciklama)
    )

    print(f"Destek talebi olusturuldu (ID: {talep_id})")

  def destekleri_goster(self):
    if not self.destek_talepleri:
        print("Destek talebi yok.")
        return

    print("\n--- DESTEK TALEPLERI ---")

    for d in self.destek_talepleri:
        musteri = self.musteriler.get(d.musteri_id)

        if musteri:
            print(f"ID: {d.talep_id} | {musteri.ad} {musteri.soyad} | {d.aciklama}")
        else:
            print(f"ID: {d.talep_id} | Musteri bulunamadi | {d.aciklama}")

def menu():
    crm = CRM()

    while True:
        print("\n===== CRM MENU =====")
        print("1 - Musteri Ekle")
        print("2 - Musteri Sil")
        print("3 - Musterileri Goster")
        print("4 - Satis Ekle")
        print("5 - Satis Bul")
        print("6 - Satis Sil")
        print("7 - Satislari Goster")
        print("8 - Destek Talebi Olustur")
        print("9 - Destek Talebleri Goster")
        print("0 - Cikis")

        secim = input("Seciminiz: ")

        if secim == "1":
            crm.musteri_ekle()
        elif secim == "2":
            crm.musteri_sil()
        elif secim == "3":
            crm.musterileri_goster()
        elif secim == "4":
            crm.satis_ekle()
        elif secim == "5":
            crm.satis_bul()
        elif secim == "6":
            crm.satis_sil()
        elif secim == "7":
            crm.satisleri_goster()
        elif secim == "8":
            crm.destek_olustur()
        elif secim == "9":
            crm.destek_bul()
        elif secim == "0":
            print("Cikis yapiliyor...")
            break
        else:
            print("Gecersiz secim!")

menu()



