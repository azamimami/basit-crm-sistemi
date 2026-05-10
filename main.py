import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QDialog, QLabel,
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QMessageBox,
    QTabWidget, QFrame, QScrollArea
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QIcon
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt5.QtCore import QPointF
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# ============ CLASSLAR ==========

class Musteri:
    def __init__(self, musteri_id, ad, soyad, telefon):
        self.musteri_id = musteri_id
        self.ad = ad
        self.soyad = soyad
        self.telefon = telefon


class Satis:
    def __init__(self, satis_id, musteri_id, urun, fiyat):
        self.satis_id = satis_id
        self.musteri_id = musteri_id
        self.urun = urun
        self.fiyat = fiyat


class DestekTalebi:
    def __init__(self, talep_id, musteri_id, aciklama):
        self.talep_id = talep_id
        self.musteri_id = musteri_id
        self.aciklama = aciklama


# ============ CRM SISTEMI ==========

class CRM:
    def __init__(self):
        self.musteriler = {}
        self.satislar = {}
        self.destek_talepleri = []

        self.musteri_id_sayac = 1
        self.satis_id_sayac = 1
        self.talep_id_sayac = 1

    def musteri_ekle(self, ad, soyad, telefon):
        musteri_id = self.musteri_id_sayac
        self.musteri_id_sayac += 1
        self.musteriler[musteri_id] = Musteri(musteri_id, ad, soyad, telefon)
        return musteri_id

    def musteri_sil(self, musteri_id):
        if musteri_id in self.musteriler:
            del self.musteriler[musteri_id]
            return True
        return False

    def satis_ekle(self, musteri_id, urun, fiyat):
        if musteri_id not in self.musteriler:
            return None
        satis_id = self.satis_id_sayac
        self.satis_id_sayac += 1
        self.satislar[satis_id] = Satis(satis_id, musteri_id, urun, fiyat)
        return satis_id

    def satis_sil(self, satis_id):
        if satis_id in self.satislar:
            del self.satislar[satis_id]
            return True
        return False

    def destek_olustur(self, musteri_id, aciklama):
        if musteri_id not in self.musteriler:
            return None
        talep_id = self.talep_id_sayac
        self.talep_id_sayac += 1
        self.destek_talepleri.append(DestekTalebi(talep_id, musteri_id, aciklama))
        return talep_id

    def toplam_satis(self):
        return sum(s.fiyat for s in self.satislar.values())

    def musteri_sayisi(self):
        return len(self.musteriler)

    def destek_sayisi(self):
        return len(self.destek_talepleri)


# ============ DIALOG PENCERELERI ==========

class MusteriEkleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Müşteri Ekle")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #f5f5f5;")
        self.init_ui()
        self.result = None

    def init_ui(self):
        layout = QVBoxLayout()

        # Ad
        ad_label = QLabel("Ad:")
        ad_label.setFont(QFont("Arial", 10))
        self.ad_input = QLineEdit()
        self.ad_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        # Soyad
        soyad_label = QLabel("Soyad:")
        soyad_label.setFont(QFont("Arial", 10))
        self.soyad_input = QLineEdit()
        self.soyad_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        # Telefon
        telefon_label = QLabel("Telefon:")
        telefon_label.setFont(QFont("Arial", 10))
        self.telefon_input = QLineEdit()
        self.telefon_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        # Butonlar
        button_layout = QHBoxLayout()
        ekle_btn = QPushButton("✓ Ekle")
        ekle_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; border-radius: 4px; font-weight: bold;")
        ekle_btn.clicked.connect(self.ekle)

        iptal_btn = QPushButton("✕ İptal")
        iptal_btn.setStyleSheet("background-color: #9E9E9E; color: white; padding: 8px; border-radius: 4px; font-weight: bold;")
        iptal_btn.clicked.connect(self.reject)

        button_layout.addWidget(ekle_btn)
        button_layout.addWidget(iptal_btn)

        layout.addWidget(ad_label)
        layout.addWidget(self.ad_input)
        layout.addWidget(soyad_label)
        layout.addWidget(self.soyad_input)
        layout.addWidget(telefon_label)
        layout.addWidget(self.telefon_input)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def ekle(self):
        if self.ad_input.text() and self.soyad_input.text() and self.telefon_input.text():
            self.result = (
                self.ad_input.text(),
                self.soyad_input.text(),
                self.telefon_input.text()
            )
            self.accept()
        else:
            QMessageBox.warning(self, "Hata", "Tüm alanları doldurun!")


class SatisEkleDialog(QDialog):
    def __init__(self, crm, parent=None):
        super().__init__(parent)
        self.crm = crm
        self.setWindowTitle("Satış Ekle")
        self.setGeometry(100, 100, 400, 350)
        self.setStyleSheet("background-color: #f5f5f5;")
        self.init_ui()
        self.result = None

    def init_ui(self):
        layout = QVBoxLayout()

        # Müşteri seçimi
        musteri_label = QLabel("Müşteri:")
        musteri_label.setFont(QFont("Arial", 10))
        self.musteri_combo = QComboBox()
        self.musteri_combo.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        for mid, m in self.crm.musteriler.items():
            self.musteri_combo.addItem(f"{m.ad} {m.soyad}", mid)

        if not self.crm.musteriler:
            self.musteri_combo.addItem("Müşteri yok", None)
            self.musteri_combo.setEnabled(False)

        # Ürün
        urun_label = QLabel("Ürün:")
        urun_label.setFont(QFont("Arial", 10))
        self.urun_input = QLineEdit()
        self.urun_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        # Fiyat
        fiyat_label = QLabel("Fiyat (TL):")
        fiyat_label.setFont(QFont("Arial", 10))
        self.fiyat_input = QDoubleSpinBox()
        self.fiyat_input.setMaximum(1000000)
        self.fiyat_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        # Butonlar
        button_layout = QHBoxLayout()
        ekle_btn = QPushButton("✓ Ekle")
        ekle_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; border-radius: 4px; font-weight: bold;")
        ekle_btn.clicked.connect(self.ekle)

        iptal_btn = QPushButton("✕ İptal")
        iptal_btn.setStyleSheet("background-color: #9E9E9E; color: white; padding: 8px; border-radius: 4px; font-weight: bold;")
        iptal_btn.clicked.connect(self.reject)

        button_layout.addWidget(ekle_btn)
        button_layout.addWidget(iptal_btn)

        layout.addWidget(musteri_label)
        layout.addWidget(self.musteri_combo)
        layout.addWidget(urun_label)
        layout.addWidget(self.urun_input)
        layout.addWidget(fiyat_label)
        layout.addWidget(self.fiyat_input)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def ekle(self):
        musteri_id = self.musteri_combo.currentData()
        if musteri_id and self.urun_input.text() and self.fiyat_input.value() > 0:
            self.result = (musteri_id, self.urun_input.text(), self.fiyat_input.value())
            self.accept()
        else:
            QMessageBox.warning(self, "Hata", "Tüm alanları doldurun ve fiyat > 0 olmalı!")


class DestekDialog(QDialog):
    def __init__(self, crm, parent=None):
        super().__init__(parent)
        self.crm = crm
        self.setWindowTitle("Destek Talebi Oluştur")
        self.setGeometry(100, 100, 400, 350)
        self.setStyleSheet("background-color: #f5f5f5;")
        self.init_ui()
        self.result = None

    def init_ui(self):
        layout = QVBoxLayout()

        # Müşteri seçimi
        musteri_label = QLabel("Müşteri:")
        musteri_label.setFont(QFont("Arial", 10))
        self.musteri_combo = QComboBox()
        self.musteri_combo.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        for mid, m in self.crm.musteriler.items():
            self.musteri_combo.addItem(f"{m.ad} {m.soyad}", mid)

        if not self.crm.musteriler:
            self.musteri_combo.addItem("Müşteri yok", None)
            self.musteri_combo.setEnabled(False)

        # Açıklama
        aciklama_label = QLabel("Açıklama:")
        aciklama_label.setFont(QFont("Arial", 10))
        self.aciklama_input = QLineEdit()
        self.aciklama_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        # Butonlar
        button_layout = QHBoxLayout()
        ekle_btn = QPushButton("✓ Oluştur")
        ekle_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; border-radius: 4px; font-weight: bold;")
        ekle_btn.clicked.connect(self.olustur)

        iptal_btn = QPushButton("✕ İptal")
        iptal_btn.setStyleSheet("background-color: #9E9E9E; color: white; padding: 8px; border-radius: 4px; font-weight: bold;")
        iptal_btn.clicked.connect(self.reject)

        button_layout.addWidget(ekle_btn)
        button_layout.addWidget(iptal_btn)

        layout.addWidget(musteri_label)
        layout.addWidget(self.musteri_combo)
        layout.addWidget(aciklama_label)
        layout.addWidget(self.aciklama_input)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def olustur(self):
        musteri_id = self.musteri_combo.currentData()
        if musteri_id and self.aciklama_input.text():
            self.result = (musteri_id, self.aciklama_input.text())
            self.accept()
        else:
            QMessageBox.warning(self, "Hata", "Tüm alanları doldurun!")


# ============ MATPLOTLIB GRAFIKLERI ==========

class StatisticsWidget(QWidget):
    def __init__(self, crm, parent=None):
        super().__init__(parent)
        self.crm = crm
        self.figure = Figure(figsize=(12, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_charts(self):
        self.figure.clear()

        # Pasta grafik - Satış dağılımı
        ax1 = self.figure.add_subplot(121)
        if self.crm.satislar:
            urunler = {}
            for s in self.crm.satislar.values():
                urunler[s.urun] = urunler.get(s.urun, 0) + s.fiyat

            ax1.pie(urunler.values(), labels=urunler.keys(), autopct='%1.1f%%', colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'])
            ax1.set_title('💰 Ürün Bazlı Satış Dağılımı', fontsize=12, fontweight='bold')
        else:
            ax1.text(0.5, 0.5, 'Satış Yok', ha='center', va='center', fontsize=14)
            ax1.set_title('💰 Ürün Bazlı Satış Dağılımı', fontsize=12, fontweight='bold')

        # Bar grafik - Istatistikler
        ax2 = self.figure.add_subplot(122)
        labels = ['👥 Müşteri', '💳 Satış', '🔧 Destek']
        values = [self.crm.musteri_sayisi(), len(self.crm.satislar), self.crm.destek_sayisi()]
        colors_bar = ['#4CAF50', '#2196F3', '#FF9800']
        bars = ax2.bar(labels, values, color=colors_bar, edgecolor='black', linewidth=1.5)
        ax2.set_title('📊 CRM İstatistikleri', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Sayı', fontsize=10)

        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontweight='bold')

        self.canvas.draw()


# ============ MAIN WINDOW ==========

class CRMMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.crm = CRM()
        self.setWindowTitle("🏢 CRM YÖNETİM SİSTEMİ")
        self.setGeometry(0, 0, 1400, 800)
        self.setStyleSheet("background-color: #ffffff;")
        self.init_ui()

    def init_ui(self):
        # Ana widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()

        # Başlık
        header = QLabel("🏢 CRM YÖNETİM SİSTEMİ")
        header_font = QFont()
        header_font.setPointSize(20)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #4CAF50; padding: 20px;")

        # Dashboard
        dashboard_layout = QHBoxLayout()

        # İstatistik kartları
        musteri_card = self.create_stat_card("👥 Müşteriler", "0", "#4CAF50")
        satis_card = self.create_stat_card("💳 Toplam Satış", "0 TL", "#2196F3")
        destek_card = self.create_stat_card("🔧 Destek Talepleri", "0", "#FF9800")

        dashboard_layout.addWidget(musteri_card)
        dashboard_layout.addWidget(satis_card)
        dashboard_layout.addWidget(destek_card)

        self.musteri_label = musteri_card.findChild(QLabel, "value_label")
        self.satis_label = satis_card.findChild(QLabel, "value_label")
        self.destek_label = destek_card.findChild(QLabel, "value_label")

        # Sekme penceresi
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab { 
                background-color: #e0e0e0; 
                padding: 8px 20px; 
                border-radius: 4px;
                font-weight: bold;
            }
            QTabBar::tab:selected { 
                background-color: #4CAF50; 
                color: white;
            }
        """)

        # Müşteriler sekmesi
        self.musteri_tab = self.create_musteri_tab()
        self.tabs.addTab(self.musteri_tab, "👥 Müşteriler")

        # Satışlar sekmesi
        self.satis_tab = self.create_satis_tab()
        self.tabs.addTab(self.satis_tab, "💳 Satışlar")

        # Destek sekmesi
        self.destek_tab = self.create_destek_tab()
        self.tabs.addTab(self.destek_tab, "🔧 Destek Talepleri")

        # Grafikler sekmesi
        self.stats_widget = StatisticsWidget(self.crm)
        self.tabs.addTab(self.stats_widget, "📊 Grafikler")

        main_layout.addWidget(header)
        main_layout.addLayout(dashboard_layout)
        main_layout.addWidget(self.tabs)

        central_widget.setLayout(main_layout)

        # Timer for refresh
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_all)
        self.timer.start(500)

    def create_stat_card(self, title, value, color):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 8px;
                padding: 20px;
                color: white;
            }}
        """)

        layout = QVBoxLayout()
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)

        value_label = QLabel(value)
        value_font = QFont()
        value_font.setPointSize(18)
        value_font.setBold(True)
        value_label.setFont(value_font)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setObjectName("value_label")

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        card.setLayout(layout)

        return card

    def create_musteri_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Butonlar
        button_layout = QHBoxLayout()
        ekle_btn = QPushButton("➕ Müşteri Ekle")
        ekle_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        ekle_btn.clicked.connect(self.musteri_ekle)

        sil_btn = QPushButton("🗑️ Seçili Sil")
        sil_btn.setStyleSheet("background-color: #f44336; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        sil_btn.clicked.connect(self.musteri_sil)

        yenile_btn = QPushButton("🔄 Yenile")
        yenile_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        yenile_btn.clicked.connect(self.musterileri_goster)

        button_layout.addWidget(ekle_btn)
        button_layout.addWidget(sil_btn)
        button_layout.addWidget(yenile_btn)

        # Tablo
        self.musteri_table = QTableWidget()
        self.musteri_table.setColumnCount(4)
        self.musteri_table.setHorizontalHeaderLabels(["ID", "Ad", "Soyad", "Telefon"])
        self.musteri_table.setStyleSheet("border: 1px solid #ccc; border-radius: 4px;")

        layout.addLayout(button_layout)
        layout.addWidget(self.musteri_table)
        widget.setLayout(layout)

        return widget

    def create_satis_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Butonlar
        button_layout = QHBoxLayout()
        ekle_btn = QPushButton("➕ Satış Ekle")
        ekle_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        ekle_btn.clicked.connect(self.satis_ekle)

        sil_btn = QPushButton("🗑️ Seçili Sil")
        sil_btn.setStyleSheet("background-color: #f44336; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        sil_btn.clicked.connect(self.satis_sil)

        yenile_btn = QPushButton("🔄 Yenile")
        yenile_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        yenile_btn.clicked.connect(self.satisleri_goster)

        button_layout.addWidget(ekle_btn)
        button_layout.addWidget(sil_btn)
        button_layout.addWidget(yenile_btn)

        # Tablo
        self.satis_table = QTableWidget()
        self.satis_table.setColumnCount(5)
        self.satis_table.setHorizontalHeaderLabels(["ID", "Müşteri ID", "Müşteri Adı", "Ürün", "Fiyat (TL)"])
        self.satis_table.setStyleSheet("border: 1px solid #ccc; border-radius: 4px;")

        layout.addLayout(button_layout)
        layout.addWidget(self.satis_table)
        widget.setLayout(layout)

        return widget

    def create_destek_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Butonlar
        button_layout = QHBoxLayout()
        ekle_btn = QPushButton("➕ Destek Talebi Oluştur")
        ekle_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        ekle_btn.clicked.connect(self.destek_olustur)

        yenile_btn = QPushButton("🔄 Yenile")
        yenile_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        yenile_btn.clicked.connect(self.destekleri_goster)

        button_layout.addWidget(ekle_btn)
        button_layout.addWidget(yenile_btn)

        # Tablo
        self.destek_table = QTableWidget()
        self.destek_table.setColumnCount(4)
        self.destek_table.setHorizontalHeaderLabels(["ID", "Müşteri Adı", "Müşteri Soyadı", "Açıklama"])
        self.destek_table.setStyleSheet("border: 1px solid #ccc; border-radius: 4px;")

        layout.addLayout(button_layout)
        layout.addWidget(self.destek_table)
        widget.setLayout(layout)

        return widget

    # ============ MUSTERI METODLARI ==========

    def musteri_ekle(self):
        dialog = MusteriEkleDialog(self)
        if dialog.exec_() == QDialog.Accepted and dialog.result:
            ad, soyad, telefon = dialog.result
            self.crm.musteri_ekle(ad, soyad, telefon)
            QMessageBox.information(self, "Başarılı", f"Müşteri eklendi!")
            self.musterileri_goster()

    def musteri_sil(self):
        row = self.musteri_table.currentRow()
        if row >= 0:
            musteri_id = int(self.musteri_table.item(row, 0).text())
            reply = QMessageBox.question(self, "Onay", f"Müşteri #{musteri_id} silinsin mi?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.crm.musteri_sil(musteri_id)
                QMessageBox.information(self, "Başarılı", "Müşteri silindi!")
                self.musterileri_goster()
        else:
            QMessageBox.warning(self, "Hata", "Lütfen bir müşteri seçin!")

    def musterileri_goster(self):
        self.musteri_table.setRowCount(0)
        for m in self.crm.musteriler.values():
            row = self.musteri_table.rowCount()
            self.musteri_table.insertRow(row)
            self.musteri_table.setItem(row, 0, QTableWidgetItem(str(m.musteri_id)))
            self.musteri_table.setItem(row, 1, QTableWidgetItem(m.ad))
            self.musteri_table.setItem(row, 2, QTableWidgetItem(m.soyad))
            self.musteri_table.setItem(row, 3, QTableWidgetItem(m.telefon))

    # ============ SATIS METODLARI ==========

    def satis_ekle(self):
        dialog = SatisEkleDialog(self.crm, self)
        if dialog.exec_() == QDialog.Accepted and dialog.result:
            musteri_id, urun, fiyat = dialog.result
            self.crm.satis_ekle(musteri_id, urun, fiyat)
            QMessageBox.information(self, "Başarılı", f"Satış eklendi!")
            self.satisleri_goster()

    def satis_sil(self):
        row = self.satis_table.currentRow()
        if row >= 0:
            satis_id = int(self.satis_table.item(row, 0).text())
            reply = QMessageBox.question(self, "Onay", f"Satış #{satis_id} silinsin mi?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.crm.satis_sil(satis_id)
                QMessageBox.information(self, "Başarılı", "Satış silindi!")
                self.satisleri_goster()
        else:
            QMessageBox.warning(self, "Hata", "Lütfen bir satış seçin!")

    def satisleri_goster(self):
        self.satis_table.setRowCount(0)
        for s in self.crm.satislar.values():
            musteri_adi = ""
            if s.musteri_id in self.crm.musteriler:
                m = self.crm.musteriler[s.musteri_id]
                musteri_adi = m.ad

            row = self.satis_table.rowCount()
            self.satis_table.insertRow(row)
            self.satis_table.setItem(row, 0, QTableWidgetItem(str(s.satis_id)))
            self.satis_table.setItem(row, 1, QTableWidgetItem(str(s.musteri_id)))
            self.satis_table.setItem(row, 2, QTableWidgetItem(musteri_adi))
            self.satis_table.setItem(row, 3, QTableWidgetItem(s.urun))
            self.satis_table.setItem(row, 4, QTableWidgetItem(f"{s.fiyat:.2f}"))

    # ============ DESTEK METODLARI ==========

    def destek_olustur(self):
        dialog = DestekDialog(self.crm, self)
        if dialog.exec_() == QDialog.Accepted and dialog.result:
            musteri_id, aciklama = dialog.result
            self.crm.destek_olustur(musteri_id, aciklama)
            QMessageBox.information(self, "Başarılı", "Destek talebi oluşturuldu!")
            self.destekleri_goster()

    def destekleri_goster(self):
        self.destek_table.setRowCount(0)
        for d in self.crm.destek_talepleri:
            musteri = self.crm.musteriler.get(d.musteri_id)

            row = self.destek_table.rowCount()
            self.destek_table.insertRow(row)
            self.destek_table.setItem(row, 0, QTableWidgetItem(str(d.talep_id)))
            self.destek_table.setItem(row, 1, QTableWidgetItem(musteri.ad if musteri else "Bilinmiyor"))
            self.destek_table.setItem(row, 2, QTableWidgetItem(musteri.soyad if musteri else "Bilinmiyor"))
            self.destek_table.setItem(row, 3, QTableWidgetItem(d.aciklama))

    # ============ REFRESH METODU ==========

    def refresh_all(self):
        self.musteri_label.setText(str(self.crm.musteri_sayisi()))
        self.satis_label.setText(f"{self.crm.toplam_satis():.2f} TL")
        self.destek_label.setText(str(self.crm.destek_sayisi()))
        self.stats_widget.update_charts()


# ============ MAIN ==========

def main():
    app = QApplication(sys.argv)
    window = CRMMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
