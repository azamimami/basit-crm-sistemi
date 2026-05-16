import sys
import random
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QDialog, QLabel,
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QMessageBox,
    QTabWidget, QFrame, QScrollArea, QHeaderView, QSplitter,
    QGroupBox, QRadioButton, QDateEdit, QTextEdit, QCheckBox,
    QStackedWidget, QListWidget, QListWidgetItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer, QDate, QPropertyAnimation, QEasingCurve, QRect, pyqtProperty
from PyQt5.QtGui import QFont, QColor, QIcon, QPalette, QLinearGradient, QBrush, QPainter, QPen
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis, QLineSeries
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8-darkgrid')


# ============ MODERN STYLESHEET WITH BETTER CONTRAST ==========

MODERN_STYLE = """
/* Ana Pencere */
QMainWindow {
    background-color: #0f0f1a;
}

/* Sidebar Stili */
#sidebar {
    background-color: #1a1a2e;
    border-right: 1px solid #2d2d44;
}

#sidebar QPushButton {
    background-color: transparent;
    color: #e2e2e2;
    text-align: left;
    padding: 12px 20px;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 500;
    margin: 4px 10px;
}

#sidebar QPushButton:hover {
    background-color: #2d2d44;
    color: #ffffff;
}

#sidebar QPushButton:checked {
    background-color: #6366f1;
    color: #ffffff;
}

/* User Section in Sidebar - FIXED */
#user_frame {
    background-color: #2d2d44;
    border-radius: 12px;
    margin: 20px;
    padding: 15px;
}

#user_frame QLabel {
    color: #ffffff;
    font-size: 13px;
}

#user_name {
    font-weight: bold;
    font-size: 14px;
    color: #ffffff;
}

#user_email {
    font-size: 11px;
    color: #a5b4fc;
}

/* Top Bar */
#topbar {
    background-color: #1a1a2e;
    border-bottom: 1px solid #2d2d44;
}

/* Kartlar */
.card {
    background-color: #1e1e35;
    border-radius: 16px;
    border: 1px solid #2d2d44;
}

.card-gradient {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #6366f1, stop:1 #8b5cf6);
    border-radius: 16px;
}

/* Tablo Stili - Fixed visibility */
QTableWidget {
    background-color: #1e1e35;
    alternate-background-color: #262640;
    gridline-color: #2d2d44;
    border: none;
    border-radius: 12px;
    color: #ffffff;
    selection-background-color: #6366f1;
}

QTableWidget::item {
    padding: 12px;
    border-bottom: 1px solid #2d2d44;
    color: #ffffff;
}

QTableWidget::item:selected {
    background-color: #6366f1;
    color: #ffffff;
}

QHeaderView::section {
    background-color: #1a1a2e;
    padding: 12px;
    border: none;
    border-bottom: 1px solid #2d2d44;
    font-weight: bold;
    color: #a5b4fc;
}

/* Butonlar */
QPushButton {
    background-color: #6366f1;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 10px;
    font-weight: 600;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #8183f4;
}

QPushButton:pressed {
    background-color: #4f46e5;
}

QPushButton#danger {
    background-color: #ef4444;
}

QPushButton#danger:hover {
    background-color: #f87171;
}

QPushButton#warning {
    background-color: #f59e0b;
}

QPushButton#warning:hover {
    background-color: #fbbf24;
}

QPushButton#secondary {
    background-color: #2d2d44;
    color: #e2e2e2;
}

QPushButton#secondary:hover {
    background-color: #3d3d5c;
    color: white;
}

/* Input Alanları - Fixed visibility */
QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {
    background-color: #1a1a2e;
    border: 1px solid #3d3d5c;
    border-radius: 10px;
    padding: 10px;
    color: #ffffff;
    font-size: 13px;
}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border: 1px solid #6366f1;
}

QLineEdit::placeholder {
    color: #9ca3af;
}

QLabel {
    color: #e2e2e2;
}

QLabel#title {
    color: #ffffff;
    font-size: 18px;
    font-weight: bold;
}

QLabel#subtitle {
    color: #9ca3af;
    font-size: 14px;
}

/* ComboBox dropdown */
QComboBox QAbstractItemView {
    background-color: #1a1a2e;
    color: #ffffff;
    border: 1px solid #3d3d5c;
    selection-background-color: #6366f1;
}

/* Sekmeler */
QTabWidget::pane {
    background-color: #1e1e35;
    border-radius: 12px;
    border: 1px solid #2d2d44;
}

QTabBar::tab {
    background-color: #1a1a2e;
    padding: 10px 25px;
    margin-right: 4px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    color: #9ca3af;
}

QTabBar::tab:selected {
    background-color: #6366f1;
    color: white;
}

QTabBar::tab:hover:!selected {
    background-color: #2d2d44;
    color: #e2e2e2;
}

/* Scrollbar */
QScrollBar:vertical {
    background-color: #1a1a2e;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #6366f1;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
}

/* Dialog */
QDialog {
    background-color: #1a1a2e;
}

QDialog QLabel {
    color: #e2e2e2;
}

/* Message Box */
QMessageBox {
    background-color: #1a1a2e;
}

QMessageBox QLabel {
    color: #e2e2e2;
}

QMessageBox QPushButton {
    min-width: 80px;
}

/* Tooltip */
QToolTip {
    background-color: #2d2d44;
    color: #ffffff;
    border: 1px solid #6366f1;
    border-radius: 8px;
    padding: 5px;
}

/* Group Box */
QGroupBox {
    color: #e2e2e2;
    border: 1px solid #2d2d44;
    border-radius: 12px;
    margin-top: 10px;
    padding-top: 10px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 10px 0 10px;
    color: #a5b4fc;
}

/* Checkbox */
QCheckBox {
    color: #e2e2e2;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1px solid #3d3d5c;
    background-color: #1a1a2e;
}

QCheckBox::indicator:checked {
    background-color: #6366f1;
    border-color: #6366f1;
}

/* Spin Box */
QSpinBox, QDoubleSpinBox {
    background-color: #1a1a2e;
    border: 1px solid #3d3d5c;
    border-radius: 8px;
    padding: 6px;
    color: #ffffff;
}

QSpinBox::up-button, QDoubleSpinBox::up-button,
QSpinBox::down-button, QDoubleSpinBox::down-button {
    background-color: #2d2d44;
    border-radius: 4px;
    width: 20px;
}

/* List Widget */
QListWidget {
    background-color: #1e1e35;
    border: 1px solid #2d2d44;
    border-radius: 12px;
    color: #e2e2e2;
}

QListWidget::item {
    padding: 10px;
    border-bottom: 1px solid #2d2d44;
}

QListWidget::item:selected {
    background-color: #6366f1;
}
"""


# ============ ANIMATED BUTTON ==========

class AnimatedButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(100)
        self.original_geometry = None

    def enterEvent(self, event):
        self.original_geometry = self.geometry()
        self.animation.stop()
        self.animation.setEndValue(QRect(
            self.original_geometry.x() + 5,
            self.original_geometry.y(),
            self.original_geometry.width() - 10,
            self.original_geometry.height()
        ))
        self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self.original_geometry:
            self.animation.stop()
            self.animation.setEndValue(self.original_geometry)
            self.animation.start()
        super().leaveEvent(event)


# ============ STAT CARD ==========

class StatCard(QFrame):
    def __init__(self, title, value, icon, color, parent=None):
        super().__init__(parent)
        self.setProperty("class", "card")
        self.setMinimumHeight(120)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)

        top_layout = QHBoxLayout()
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #9ca3af; font-size: 14px;")
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 28px;")
        top_layout.addWidget(title_label)
        top_layout.addStretch()
        top_layout.addWidget(icon_label)

        value_label = QLabel(str(value))
        value_label.setStyleSheet(f"font-size: 28px; font-weight: bold; color: #ffffff;")

        layout.addLayout(top_layout)
        layout.addWidget(value_label)

        self.setLayout(layout)
        self.value_label = value_label

    def update_value(self, new_value):
        self.value_label.setText(str(new_value))


# ============ DASHBOARD CARD ==========

class DashboardCard(QFrame):
    def __init__(self, title, value, icon, gradient=False, parent=None):
        super().__init__(parent)
        if gradient:
            self.setProperty("class", "card-gradient")
        else:
            self.setProperty("class", "card")

        self.setMinimumHeight(140)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)

        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 40px;")

        value_label = QLabel(str(value))
        value_label.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {'white' if gradient else '#ffffff'};")

        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 14px; color: {'rgba(255,255,255,0.8)' if gradient else '#9ca3af'};")

        layout.addWidget(icon_label)
        layout.addStretch()
        layout.addWidget(value_label)
        layout.addWidget(title_label)

        self.setLayout(layout)
        self.value_label = value_label

    def update_value(self, new_value):
        self.value_label.setText(str(new_value))


# ============ DATA MODELS ==========

class Customer:
    def __init__(self, customer_id, name, email, phone, company, status, join_date):
        self.id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.company = company
        self.status = status
        self.join_date = join_date
        self.total_spent = 0
        self.tickets_count = 0


class Sale:
    def __init__(self, sale_id, customer_id, product, amount, quantity, date, status):
        self.id = sale_id
        self.customer_id = customer_id
        self.product = product
        self.amount = amount
        self.quantity = quantity
        self.date = date
        self.status = status
        self.total = amount * quantity


class SupportTicket:
    def __init__(self, ticket_id, customer_id, subject, description, priority, status, date):
        self.id = ticket_id
        self.customer_id = customer_id
        self.subject = subject
        self.description = description
        self.priority = priority
        self.status = status
        self.date = date


# ============ CRM SYSTEM ==========

class CRM:
    def __init__(self):
        self.customers = {}
        self.sales = {}
        self.tickets = {}

        self.customer_counter = 1
        self.sale_counter = 1
        self.ticket_counter = 1

        self._generate_sample_data()

    def _generate_sample_data(self):
        # Sample customers with Turkish names
        customers_data = [
            ("Ahmet Yılmaz", "ahmet@yilmaz.com", "+90 555 123 4567", "Yılmaz Holding", "Active", "2024-01-15"),
            ("Ayşe Demir", "ayse@demir.com", "+90 555 123 4568", "Demir Teknoloji", "Active", "2024-01-20"),
            ("Mehmet Kaya", "mehmet@kaya.com", "+90 555 123 4569", "Kaya Grup", "Inactive", "2024-02-01"),
            ("Zeynep Çelik", "zeynep@celik.com", "+90 555 123 4570", "Çelik İnşaat", "Active", "2024-02-10"),
            ("Can Öztürk", "can@ozturk.com", "+90 555 123 4571", "Öztürk Yazılım", "Active", "2024-02-15"),
            ("Elif Şahin", "elif@sahin.com", "+90 555 123 4572", "Şahin Medya", "Pending", "2024-03-01"),
        ]

        for data in customers_data:
            self.add_customer(*data)

        # Sample products with Turkish names
        products = [
            ("Kurumsal Lisans", 14999, 1),
            ("Profesyonel Lisans", 7499, 2),
            ("Temel Lisans", 2999, 3),
            ("Premium Destek", 4499, 1),
            ("Bulut Depolama 1TB", 899, 5),
            ("API Erişimi", 2399, 2),
        ]

        # Generate sales
        for _ in range(30):
            customer_id = random.randint(1, len(self.customers))
            product, price, qty = random.choice(products)
            date = (datetime.now() - timedelta(days=random.randint(0, 90))).strftime("%Y-%m-%d")
            status = random.choice(["Completed", "Pending", "Processing"])
            self.add_sale(customer_id, product, price, qty, date, status)

        # Generate support tickets
        ticket_subjects = [
            "Giriş sorunu", "Fatura sorgulama", "Teknik destek gerekli",
            "Yeni özellik talebi", "Hata bildirimi", "Hesap yükseltme",
            "Şifre sıfırlama", "API dokümantasyon", "Entegrasyon yardımı"
        ]

        for _ in range(20):
            customer_id = random.randint(1, len(self.customers))
            subject = random.choice(ticket_subjects)
            priority = random.choice(["Düşük", "Orta", "Yüksek", "Acil"])
            status = random.choice(["Açık", "İşlemde", "Çözüldü", "Kapalı"])
            date = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
            self.add_ticket(customer_id, subject, f"Açıklama: {subject}", priority, status, date)

        # Update customer statistics
        for sale in self.sales.values():
            if sale.customer_id in self.customers:
                self.customers[sale.customer_id].total_spent += sale.total

        for ticket in self.tickets.values():
            if ticket.customer_id in self.customers:
                self.customers[ticket.customer_id].tickets_count += 1

    def add_customer(self, name, email, phone, company, status, join_date):
        customer_id = self.customer_counter
        self.customer_counter += 1
        self.customers[customer_id] = Customer(customer_id, name, email, phone, company, status, join_date)
        return customer_id

    def update_customer(self, customer_id, name, email, phone, company, status):
        if customer_id in self.customers:
            c = self.customers[customer_id]
            c.name = name
            c.email = email
            c.phone = phone
            c.company = company
            c.status = status
            return True
        return False

    def delete_customer(self, customer_id):
        if customer_id in self.customers:
            # Delete related data
            sale_ids = [sid for sid, s in self.sales.items() if s.customer_id == customer_id]
            for sid in sale_ids:
                del self.sales[sid]

            ticket_ids = [tid for tid, t in self.tickets.items() if t.customer_id == customer_id]
            for tid in ticket_ids:
                del self.tickets[tid]

            del self.customers[customer_id]
            return True
        return False

    def add_sale(self, customer_id, product, amount, quantity, date, status):
        sale_id = self.sale_counter
        self.sale_counter += 1
        self.sales[sale_id] = Sale(sale_id, customer_id, product, amount, quantity, date, status)
        return sale_id

    def update_sale(self, sale_id, product, amount, quantity, status):
        if sale_id in self.sales:
            s = self.sales[sale_id]
            s.product = product
            s.amount = amount
            s.quantity = quantity
            s.status = status
            s.total = amount * quantity
            return True
        return False

    def delete_sale(self, sale_id):
        if sale_id in self.sales:
            del self.sales[sale_id]
            return True
        return False

    def add_ticket(self, customer_id, subject, description, priority, status, date):
        ticket_id = self.ticket_counter
        self.ticket_counter += 1
        self.tickets[ticket_id] = SupportTicket(ticket_id, customer_id, subject, description, priority, status, date)
        return ticket_id

    def update_ticket(self, ticket_id, priority, status):
        if ticket_id in self.tickets:
            t = self.tickets[ticket_id]
            t.priority = priority
            t.status = status
            return True
        return False

    def delete_ticket(self, ticket_id):
        if ticket_id in self.tickets:
            del self.tickets[ticket_id]
            return True
        return False

    def get_total_revenue(self):
        return sum(s.total for s in self.sales.values())

    def get_customer_count(self):
        return len(self.customers)

    def get_sale_count(self):
        return len(self.sales)

    def get_open_tickets_count(self):
        return sum(1 for t in self.tickets.values() if t.status in ["Açık", "İşlemde"])

    def get_monthly_revenue(self):
        monthly = {}
        for sale in self.sales.values():
            month = sale.date[:7]
            monthly[month] = monthly.get(month, 0) + sale.total
        return dict(sorted(monthly.items()))

    def get_revenue_by_product(self):
        product_revenue = {}
        for sale in self.sales.values():
            product_revenue[sale.product] = product_revenue.get(sale.product, 0) + sale.total
        return product_revenue

    def get_tickets_by_status(self):
        status_count = {"Açık": 0, "İşlemde": 0, "Çözüldü": 0, "Kapalı": 0}
        for ticket in self.tickets.values():
            status_count[ticket.status] = status_count.get(ticket.status, 0) + 1
        return status_count

    def get_recent_activities(self, limit=10):
        activities = []

        for sale in list(self.sales.values())[-limit:]:
            customer = self.customers.get(sale.customer_id)
            if customer:
                activities.append({
                    "type": "sale",
                    "description": f"Satış: {customer.name}, {sale.product} ürününü satın aldı",
                    "date": sale.date,
                    "amount": sale.total
                })

        for ticket in list(self.tickets.values())[-limit:]:
            customer = self.customers.get(ticket.customer_id)
            if customer:
                activities.append({
                    "type": "ticket",
                    "description": f"Destek #{ticket.id}: {customer.name} - {ticket.subject}",
                    "date": ticket.date,
                    "priority": ticket.priority
                })

        activities.sort(key=lambda x: x["date"], reverse=True)
        return activities[:limit]


# ============ DIALOGS ==========

class CustomerDialog(QDialog):
    def __init__(self, parent=None, customer=None):
        super().__init__(parent)
        self.customer = customer
        self.setWindowTitle("Müşteri Düzenle" if customer else "Müşteri Ekle")
        self.setModal(True)
        self.setFixedSize(500, 550)
        self.setStyleSheet(MODERN_STYLE)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        title = QLabel("Müşteri Bilgileri")
        title.setObjectName("title")
        layout.addWidget(title)

        # Form fields
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ad Soyad / Firma Adı")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-posta Adresi")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Telefon Numarası")

        self.company_input = QLineEdit()
        self.company_input.setPlaceholderText("Şirket Adı")

        self.status_combo = QComboBox()
        self.status_combo.addItems(["Aktif", "Pasif", "Beklemede"])

        # Populate if editing
        if self.customer:
            self.name_input.setText(self.customer.name)
            self.email_input.setText(self.customer.email)
            self.phone_input.setText(self.customer.phone)
            self.company_input.setText(self.customer.company)
            status_map = {"Active": "Aktif", "Inactive": "Pasif", "Pending": "Beklemede"}
            self.status_combo.setCurrentText(status_map.get(self.customer.status, "Aktif"))

        layout.addWidget(QLabel("Ad Soyad"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("E-posta"))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("Telefon"))
        layout.addWidget(self.phone_input)
        layout.addWidget(QLabel("Şirket"))
        layout.addWidget(self.company_input)
        layout.addWidget(QLabel("Durum"))
        layout.addWidget(self.status_combo)

        layout.addStretch()

        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = AnimatedButton("Kaydet")
        save_btn.clicked.connect(self.save)
        cancel_btn = AnimatedButton("İptal")
        cancel_btn.setProperty("class", "secondary")
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def save(self):
        if self.name_input.text() and self.email_input.text():
            self.accept()
        else:
            QMessageBox.warning(self, "Uyarı", "Ad Soyad ve E-posta alanları zorunludur!")

    def get_data(self):
        status_map = {"Aktif": "Active", "Pasif": "Inactive", "Beklemede": "Pending"}
        return {
            "name": self.name_input.text(),
            "email": self.email_input.text(),
            "phone": self.phone_input.text(),
            "company": self.company_input.text(),
            "status": status_map[self.status_combo.currentText()]
        }


class SaleDialog(QDialog):
    def __init__(self, parent=None, sale=None):
        super().__init__(parent)
        self.sale = sale
        self.setWindowTitle("Satış Düzenle" if sale else "Satış Ekle")
        self.setModal(True)
        self.setFixedSize(450, 500)
        self.setStyleSheet(MODERN_STYLE)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        title = QLabel("Satış Bilgileri")
        title.setObjectName("title")
        layout.addWidget(title)

        self.product_input = QLineEdit()
        self.product_input.setPlaceholderText("Ürün Adı")

        self.amount_input = QDoubleSpinBox()
        self.amount_input.setMaximum(1000000)
        self.amount_input.setPrefix("₺ ")
        self.amount_input.setMinimum(0)

        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(1)
        self.quantity_input.setMaximum(1000)

        self.status_combo = QComboBox()
        self.status_combo.addItems(["Tamamlandı", "İşleniyor", "Beklemede"])

        if self.sale:
            self.product_input.setText(self.sale.product)
            self.amount_input.setValue(self.sale.amount)
            self.quantity_input.setValue(self.sale.quantity)
            status_map = {"Completed": "Tamamlandı", "Processing": "İşleniyor", "Pending": "Beklemede"}
            self.status_combo.setCurrentText(status_map.get(self.sale.status, "Beklemede"))

        layout.addWidget(QLabel("Ürün"))
        layout.addWidget(self.product_input)
        layout.addWidget(QLabel("Tutar"))
        layout.addWidget(self.amount_input)
        layout.addWidget(QLabel("Adet"))
        layout.addWidget(self.quantity_input)
        layout.addWidget(QLabel("Durum"))
        layout.addWidget(self.status_combo)

        layout.addStretch()

        btn_layout = QHBoxLayout()
        save_btn = AnimatedButton("Kaydet")
        save_btn.clicked.connect(self.save)
        cancel_btn = AnimatedButton("İptal")
        cancel_btn.setProperty("class", "secondary")
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def save(self):
        if self.product_input.text():
            self.accept()
        else:
            QMessageBox.warning(self, "Uyarı", "Ürün adı zorunludur!")

    def get_data(self):
        status_map = {"Tamamlandı": "Completed", "İşleniyor": "Processing", "Beklemede": "Pending"}
        return {
            "product": self.product_input.text(),
            "amount": self.amount_input.value(),
            "quantity": self.quantity_input.value(),
            "status": status_map[self.status_combo.currentText()]
        }


class TicketDialog(QDialog):
    def __init__(self, parent=None, ticket=None):
        super().__init__(parent)
        self.ticket = ticket
        self.setWindowTitle("Destek Talebi Düzenle" if ticket else "Destek Talebi Oluştur")
        self.setModal(True)
        self.setFixedSize(500, 550)
        self.setStyleSheet(MODERN_STYLE)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        title = QLabel("Destek Talebi Bilgileri")
        title.setObjectName("title")
        layout.addWidget(title)

        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Konu")

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Açıklama...")
        self.description_input.setMaximumHeight(120)

        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Düşük", "Orta", "Yüksek", "Acil"])

        self.status_combo = QComboBox()
        self.status_combo.addItems(["Açık", "İşlemde", "Çözüldü", "Kapalı"])

        if self.ticket:
            self.subject_input.setText(self.ticket.subject)
            self.description_input.setText(self.ticket.description)
            self.priority_combo.setCurrentText(self.ticket.priority)
            self.status_combo.setCurrentText(self.ticket.status)

        layout.addWidget(QLabel("Konu"))
        layout.addWidget(self.subject_input)
        layout.addWidget(QLabel("Açıklama"))
        layout.addWidget(self.description_input)
        layout.addWidget(QLabel("Öncelik"))
        layout.addWidget(self.priority_combo)
        layout.addWidget(QLabel("Durum"))
        layout.addWidget(self.status_combo)

        layout.addStretch()

        btn_layout = QHBoxLayout()
        save_btn = AnimatedButton("Kaydet")
        save_btn.clicked.connect(self.save)
        cancel_btn = AnimatedButton("İptal")
        cancel_btn.setProperty("class", "secondary")
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def save(self):
        if self.subject_input.text() and self.description_input.toPlainText():
            self.accept()
        else:
            QMessageBox.warning(self, "Uyarı", "Konu ve açıklama alanları zorunludur!")

    def get_data(self):
        return {
            "subject": self.subject_input.text(),
            "description": self.description_input.toPlainText(),
            "priority": self.priority_combo.currentText(),
            "status": self.status_combo.currentText()
        }


# ============ MATPLOTLIB CHART WIDGET ==========

class ModernChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(10, 6), dpi=100, facecolor='#1e1e35')
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_revenue_chart(self, monthly_data):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        months = list(monthly_data.keys())
        revenues = list(monthly_data.values())

        colors = ['#6366f1'] * len(months)
        bars = ax.bar(months, revenues, color=colors, edgecolor='none', alpha=0.8)

        ax.set_title('Aylık Gelir (₺)', color='#ffffff', fontsize=14, fontweight='bold')
        ax.set_xlabel('Ay', color='#9ca3af')
        ax.set_ylabel('Gelir (₺)', color='#9ca3af')
        ax.tick_params(colors='#9ca3af')
        ax.set_facecolor('#1a1a2e')
        self.figure.patch.set_facecolor('#1e1e35')

        for spine in ax.spines.values():
            spine.set_color('#2d2d44')

        # Add value labels on bars
        for bar, revenue in zip(bars, revenues):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'₺{revenue:,.0f}',
                    ha='center', va='bottom', color='#ffffff', fontsize=9)

        self.canvas.draw()

    def update_pie_chart(self, product_data):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        products = list(product_data.keys())[:5]
        revenues = list(product_data.values())[:5]

        colors = ['#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b']

        wedges, texts, autotexts = ax.pie(revenues, labels=products, autopct='%1.1f%%',
                                            colors=colors, startangle=90)

        for text in texts:
            text.set_color('#ffffff')
            text.set_fontsize(10)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        ax.set_title('Ürün Bazlı Gelir Dağılımı', color='#ffffff', fontsize=14, fontweight='bold')
        self.figure.patch.set_facecolor('#1e1e35')

        self.canvas.draw()

    def update_ticket_chart(self, ticket_data):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        statuses = list(ticket_data.keys())
        counts = list(ticket_data.values())

        colors = ['#06b6d4', '#f59e0b', '#10b981', '#6b7280']

        bars = ax.bar(statuses, counts, color=colors, edgecolor='none', alpha=0.8)

        ax.set_title('Destek Talepleri Durumu', color='#ffffff', fontsize=14, fontweight='bold')
        ax.set_ylabel('Sayı', color='#9ca3af')
        ax.tick_params(colors='#9ca3af')
        ax.set_facecolor('#1a1a2e')
        self.figure.patch.set_facecolor('#1e1e35')

        for spine in ax.spines.values():
            spine.set_color('#2d2d44')

        # Add value labels
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    str(count),
                    ha='center', va='bottom', color='#ffffff', fontsize=10, fontweight='bold')

        self.canvas.draw()


# ============ MAIN WINDOW ==========

class ModernCRM(QMainWindow):
    def __init__(self):
        super().__init__()
        self.crm = CRM()
        self.setWindowTitle("EY - CRM - Modern Müşteri Yönetim Sistemi")
        self.setGeometry(50, 50, 1400, 850)
        self.setStyleSheet(MODERN_STYLE)

        self.init_ui()
        self.refresh_all()

        # Auto-refresh timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_dashboard_stats)
        self.timer.start(5000)

    def init_ui(self):
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #0f0f1a;")
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(260)
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(0, 30, 0, 30)
        sidebar_layout.setSpacing(5)

        # Logo
        logo_label = QLabel("🎯 EY-CRM")
        logo_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #6366f1; padding: 20px;")
        sidebar_layout.addWidget(logo_label)

        # Navigation buttons
        self.nav_buttons = {}
        nav_items = [
            ("dashboard", "📊", "Ana Panel"),
            ("customers", "👥", "Müşteriler"),
            ("sales", "💰", "Satışlar"),
            ("tickets", "🎫", "Destek Talepleri"),
            ("analytics", "📈", "Analizler"),
            ("settings", "⚙️", "Ayarlar")
        ]

        for key, icon, text in nav_items:
            btn = QPushButton(f"  {icon}  {text}")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, k=key: self.switch_page(k))
            sidebar_layout.addWidget(btn)
            self.nav_buttons[key] = btn

        sidebar_layout.addStretch()

        # User section - FIXED visibility
        user_frame = QFrame()
        user_frame.setObjectName("user_frame")
        user_frame.setStyleSheet("""
            QFrame#user_frame {
                background-color: #2d2d44;
                border-radius: 12px;
                margin: 20px;
                padding: 15px;
            }
            QLabel#user_icon {
                font-size: 32px;
                color: #a5b4fc;
            }
            QLabel#user_name {
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
            }
            QLabel#user_email {
                font-size: 11px;
                color: #a5b4fc;
            }
        """)
        user_layout = QHBoxLayout()
        user_layout.setSpacing(12)

        # User icon
        user_icon = QLabel("👤")
        user_icon.setObjectName("user_icon")

        # User info container
        user_info_layout = QVBoxLayout()
        user_info_layout.setSpacing(2)

        user_name = QLabel("Kullanici")
        user_name.setObjectName("user_name")

        user_email = QLabel("Hos Geldiniz")
        user_email.setObjectName("")

        user_info_layout.addWidget(user_name)
        user_info_layout.addWidget(user_email)

        user_layout.addWidget(user_icon)
        user_layout.addLayout(user_info_layout)
        user_layout.addStretch()

        user_frame.setLayout(user_layout)
        sidebar_layout.addWidget(user_frame)

        self.sidebar.setLayout(sidebar_layout)

        # Main content
        main_content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Top bar
        top_bar = QFrame()
        top_bar.setObjectName("topbar")
        top_bar.setFixedHeight(70)
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(30, 0, 30, 0)

        self.page_title = QLabel("Ana Panel")
        self.page_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff;")

        search_input = QLineEdit()
        search_input.setPlaceholderText("🔍 Müşteri, satış, destek talebi ara...")
        search_input.setFixedWidth(350)
        search_input.setStyleSheet("background-color: #1a1a2e; border-radius: 20px; padding: 8px 15px; color: #ffffff;")

        notification_btn = QPushButton("🔔")
        notification_btn.setFixedSize(40, 40)
        notification_btn.setStyleSheet("border-radius: 20px; background-color: #2d2d44;")

        top_layout.addWidget(self.page_title)
        top_layout.addStretch()
        top_layout.addWidget(search_input)
        top_layout.addWidget(notification_btn)
        top_bar.setLayout(top_layout)

        # Stacked widget for pages
        self.stacked_widget = QStackedWidget()

        # Create pages
        self.dashboard_page = self.create_dashboard_page()
        self.customers_page = self.create_customers_page()
        self.sales_page = self.create_sales_page()
        self.tickets_page = self.create_tickets_page()
        self.analytics_page = self.create_analytics_page()
        self.settings_page = self.create_settings_page()

        self.stacked_widget.addWidget(self.dashboard_page)
        self.stacked_widget.addWidget(self.customers_page)
        self.stacked_widget.addWidget(self.sales_page)
        self.stacked_widget.addWidget(self.tickets_page)
        self.stacked_widget.addWidget(self.analytics_page)
        self.stacked_widget.addWidget(self.settings_page)

        content_layout.addWidget(top_bar)
        content_layout.addWidget(self.stacked_widget)
        main_content.setLayout(content_layout)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(main_content, 1)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Set default page
        self.nav_buttons["dashboard"].setChecked(True)

    def switch_page(self, page_name):
        pages = {
            "dashboard": 0,
            "customers": 1,
            "sales": 2,
            "tickets": 3,
            "analytics": 4,
            "settings": 5
        }

        self.stacked_widget.setCurrentIndex(pages[page_name])

        titles = {
            "dashboard": "Ana Panel",
            "customers": "Müşteri Yönetimi",
            "sales": "Satışlar",
            "tickets": "Destek Talepleri",
            "analytics": "Analizler ve Raporlar",
            "settings": "Ayarlar"
        }

        self.page_title.setText(titles[page_name])

        for key, btn in self.nav_buttons.items():
            btn.setChecked(key == page_name)

    def create_dashboard_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)

        # Stats cards row
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)

        self.revenue_card = DashboardCard("Toplam Gelir", "₺0", "💰", gradient=True)
        self.customers_card = DashboardCard("Aktif Müşteri", "0", "👥")
        self.sales_card = DashboardCard("Toplam Satış", "0", "📈")
        self.tickets_card = DashboardCard("Açık Talepler", "0", "🎫")

        stats_layout.addWidget(self.revenue_card)
        stats_layout.addWidget(self.customers_card)
        stats_layout.addWidget(self.sales_card)
        stats_layout.addWidget(self.tickets_card)

        # Charts row
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(20)

        self.revenue_chart = ModernChartWidget()
        self.product_chart = ModernChartWidget()

        charts_layout.addWidget(self.revenue_chart)
        charts_layout.addWidget(self.product_chart)

        # Recent activity
        activity_frame = QFrame()
        activity_frame.setProperty("class", "card")
        activity_layout = QVBoxLayout()
        activity_layout.setContentsMargins(20, 20, 20, 20)

        activity_title = QLabel("📋 Son Aktiviteler")
        activity_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff; margin-bottom: 15px;")
        activity_layout.addWidget(activity_title)

        self.activity_list = QListWidget()
        self.activity_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                color: #e2e2e2;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #2d2d44;
                color: #e2e2e2;
            }
            QListWidget::item:selected {
                background-color: #6366f1;
            }
        """)
        activity_layout.addWidget(self.activity_list)

        activity_frame.setLayout(activity_layout)

        layout.addLayout(stats_layout)
        layout.addLayout(charts_layout)
        layout.addWidget(activity_frame)

        widget.setLayout(layout)
        return widget

    def create_customers_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)

        # Toolbar
        toolbar = QHBoxLayout()

        self.customer_search = QLineEdit()
        self.customer_search.setPlaceholderText("🔍 Müşteri ara...")
        self.customer_search.setFixedWidth(300)
        self.customer_search.textChanged.connect(self.search_customers)

        add_btn = AnimatedButton("➕ Müşteri Ekle")
        add_btn.clicked.connect(self.add_customer)

        edit_btn = AnimatedButton("✏️ Düzenle")
        edit_btn.setProperty("class", "warning")
        edit_btn.clicked.connect(self.edit_customer)

        delete_btn = AnimatedButton("🗑️ Sil")
        delete_btn.setProperty("class", "danger")
        delete_btn.clicked.connect(self.delete_customer)

        toolbar.addWidget(self.customer_search)
        toolbar.addStretch()
        toolbar.addWidget(add_btn)
        toolbar.addWidget(edit_btn)
        toolbar.addWidget(delete_btn)

        # Customer table
        self.customer_table = QTableWidget()
        self.customer_table.setColumnCount(7)
        self.customer_table.setHorizontalHeaderLabels(["ID", "Ad Soyad", "E-posta", "Telefon", "Şirket", "Durum", "Toplam Harcama"])
        self.customer_table.setAlternatingRowColors(True)
        self.customer_table.horizontalHeader().setStretchLastSection(True)
        self.customer_table.setSelectionBehavior(QTableWidget.SelectRows)

        layout.addLayout(toolbar)
        layout.addWidget(self.customer_table)

        widget.setLayout(layout)
        return widget

    def create_sales_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)

        # Stats row
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)

        self.total_sales_card = StatCard("Toplam Satış", "₺0", "💰", "#10b981")
        self.avg_sale_card = StatCard("Ortalama Satış", "₺0", "📊", "#6366f1")
        self.total_units_card = StatCard("Satılan Ürün", "0", "📦", "#06b6d4")

        stats_layout.addWidget(self.total_sales_card)
        stats_layout.addWidget(self.avg_sale_card)
        stats_layout.addWidget(self.total_units_card)

        # Toolbar
        toolbar = QHBoxLayout()

        self.sale_search = QLineEdit()
        self.sale_search.setPlaceholderText("🔍 Satış ara...")
        self.sale_search.setFixedWidth(300)
        self.sale_search.textChanged.connect(self.search_sales)

        add_btn = AnimatedButton("➕ Satış Ekle")
        add_btn.clicked.connect(self.add_sale)

        edit_btn = AnimatedButton("✏️ Düzenle")
        edit_btn.setProperty("class", "warning")
        edit_btn.clicked.connect(self.edit_sale)

        delete_btn = AnimatedButton("🗑️ Sil")
        delete_btn.setProperty("class", "danger")
        delete_btn.clicked.connect(self.delete_sale)

        toolbar.addWidget(self.sale_search)
        toolbar.addStretch()
        toolbar.addWidget(add_btn)
        toolbar.addWidget(edit_btn)
        toolbar.addWidget(delete_btn)

        # Sales table
        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(7)
        self.sales_table.setHorizontalHeaderLabels(["ID", "Müşteri", "Ürün", "Tutar", "Adet", "Toplam", "Durum"])
        self.sales_table.setAlternatingRowColors(True)
        self.sales_table.horizontalHeader().setStretchLastSection(True)
        self.sales_table.setSelectionBehavior(QTableWidget.SelectRows)

        layout.addLayout(stats_layout)
        layout.addLayout(toolbar)
        layout.addWidget(self.sales_table)

        widget.setLayout(layout)
        return widget

    def create_tickets_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)

        # Stats row
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)

        self.open_tickets_card = StatCard("Açık Talepler", "0", "🟡", "#f59e0b")
        self.in_progress_card = StatCard("İşlemde", "0", "🔵", "#06b6d4")
        self.resolved_card = StatCard("Çözüldü", "0", "✅", "#10b981")

        stats_layout.addWidget(self.open_tickets_card)
        stats_layout.addWidget(self.in_progress_card)
        stats_layout.addWidget(self.resolved_card)

        # Toolbar
        toolbar = QHBoxLayout()

        self.ticket_search = QLineEdit()
        self.ticket_search.setPlaceholderText("🔍 Destek talebi ara...")
        self.ticket_search.setFixedWidth(300)
        self.ticket_search.textChanged.connect(self.search_tickets)

        add_btn = AnimatedButton("➕ Talep Oluştur")
        add_btn.clicked.connect(self.add_ticket)

        toolbar.addWidget(self.ticket_search)
        toolbar.addStretch()
        toolbar.addWidget(add_btn)

        # Tickets table
        self.tickets_table = QTableWidget()
        self.tickets_table.setColumnCount(7)
        self.tickets_table.setHorizontalHeaderLabels(["ID", "Müşteri", "Konu", "Öncelik", "Durum", "Tarih", ""])
        self.tickets_table.setAlternatingRowColors(True)
        self.tickets_table.horizontalHeader().setStretchLastSection(True)
        self.tickets_table.setSelectionBehavior(QTableWidget.SelectRows)

        layout.addLayout(stats_layout)
        layout.addLayout(toolbar)
        layout.addWidget(self.tickets_table)

        widget.setLayout(layout)
        return widget

    def create_analytics_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)

        # Full width charts
        title1 = QLabel("Aylık Gelir Trendi")
        title1.setObjectName("title")

        self.revenue_trend_chart = ModernChartWidget()

        title2 = QLabel("Destek Talebi Dağılımı")
        title2.setObjectName("title")

        self.ticket_status_chart = ModernChartWidget()

        layout.addWidget(title1)
        layout.addWidget(self.revenue_trend_chart)
        layout.addWidget(title2)
        layout.addWidget(self.ticket_status_chart)

        widget.setLayout(layout)
        return widget

    def create_settings_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)

        settings_frame = QFrame()
        settings_frame.setProperty("class", "card")
        settings_layout = QVBoxLayout()
        settings_layout.setContentsMargins(30, 30, 30, 30)
        settings_layout.setSpacing(25)

        # Theme settings
        theme_group = QGroupBox("Görünüm")
        theme_layout = QVBoxLayout()

        dark_mode_check = QCheckBox("Karanlık Mod (Varsayılan)")
        dark_mode_check.setChecked(True)
        dark_mode_check.setEnabled(False)
        theme_layout.addWidget(dark_mode_check)

        theme_group.setLayout(theme_layout)

        # Notification settings
        notif_group = QGroupBox("Bildirimler")
        notif_layout = QVBoxLayout()

        email_notif = QCheckBox("E-posta Bildirimleri")
        email_notif.setChecked(True)
        push_notif = QCheckBox("Bildirim Merkezi")
        push_notif.setChecked(True)

        notif_layout.addWidget(email_notif)
        notif_layout.addWidget(push_notif)

        notif_group.setLayout(notif_layout)

        # Data settings
        data_group = QGroupBox("Veri Yönetimi")
        data_layout = QVBoxLayout()

        auto_refresh = QCheckBox("Otomatik Yenileme (5 saniye)")
        auto_refresh.setChecked(True)
        auto_refresh.stateChanged.connect(lambda state: self.timer.start(5000) if state else self.timer.stop())

        data_layout.addWidget(auto_refresh)

        data_group.setLayout(data_layout)

        settings_layout.addWidget(theme_group)
        settings_layout.addWidget(notif_group)
        settings_layout.addWidget(data_group)
        settings_layout.addStretch()

        settings_frame.setLayout(settings_layout)
        layout.addWidget(settings_frame)

        widget.setLayout(layout)
        return widget

    def refresh_all(self):
        self.update_dashboard_stats()
        self.refresh_customers()
        self.refresh_sales()
        self.refresh_tickets()
        self.update_charts()

    def update_dashboard_stats(self):
        revenue = self.crm.get_total_revenue()
        customers = self.crm.get_customer_count()
        sales = self.crm.get_sale_count()
        tickets = self.crm.get_open_tickets_count()

        self.revenue_card.update_value(f"₺{revenue:,.0f}")
        self.customers_card.update_value(str(customers))
        self.sales_card.update_value(str(sales))
        self.tickets_card.update_value(str(tickets))

        # Update sales page stats
        total_sales = sum(s.total for s in self.crm.sales.values())
        avg_sale = total_sales / len(self.crm.sales) if self.crm.sales else 0
        total_units = sum(s.quantity for s in self.crm.sales.values())

        self.total_sales_card.update_value(f"₺{total_sales:,.0f}")
        self.avg_sale_card.update_value(f"₺{avg_sale:,.0f}")
        self.total_units_card.update_value(str(total_units))

        # Update tickets page stats
        open_count = sum(1 for t in self.crm.tickets.values() if t.status == "Açık")
        progress_count = sum(1 for t in self.crm.tickets.values() if t.status == "İşlemde")
        resolved_count = sum(1 for t in self.crm.tickets.values() if t.status == "Çözüldü")

        self.open_tickets_card.update_value(str(open_count))
        self.in_progress_card.update_value(str(progress_count))
        self.resolved_card.update_value(str(resolved_count))

        # Update activity list
        self.activity_list.clear()
        activities = self.crm.get_recent_activities()
        for activity in activities:
            if activity["type"] == "sale":
                item_text = f"💰 {activity['description']} - ₺{activity['amount']:,.0f}"
            else:
                item_text = f"🎫 {activity['description']}"
            self.activity_list.addItem(item_text)

    def refresh_customers(self):
        self.customer_table.setRowCount(0)
        for customer in self.crm.customers.values():
            row = self.customer_table.rowCount()
            self.customer_table.insertRow(row)

            self.customer_table.setItem(row, 0, QTableWidgetItem(str(customer.id)))
            self.customer_table.setItem(row, 1, QTableWidgetItem(customer.name))
            self.customer_table.setItem(row, 2, QTableWidgetItem(customer.email))
            self.customer_table.setItem(row, 3, QTableWidgetItem(customer.phone))
            self.customer_table.setItem(row, 4, QTableWidgetItem(customer.company))

            status_item = QTableWidgetItem(customer.status)
            if customer.status == "Active":
                status_item.setText("Aktif")
                status_item.setForeground(QColor("#10b981"))
            elif customer.status == "Inactive":
                status_item.setText("Pasif")
                status_item.setForeground(QColor("#ef4444"))
            else:
                status_item.setText("Beklemede")
                status_item.setForeground(QColor("#f59e0b"))
            self.customer_table.setItem(row, 5, status_item)

            self.customer_table.setItem(row, 6, QTableWidgetItem(f"₺{customer.total_spent:,.0f}"))

        self.customer_table.resizeColumnsToContents()

    def refresh_sales(self):
        self.sales_table.setRowCount(0)
        for sale in self.crm.sales.values():
            customer = self.crm.customers.get(sale.customer_id)
            customer_name = customer.name if customer else "Bilinmiyor"

            row = self.sales_table.rowCount()
            self.sales_table.insertRow(row)

            self.sales_table.setItem(row, 0, QTableWidgetItem(str(sale.id)))
            self.sales_table.setItem(row, 1, QTableWidgetItem(customer_name))
            self.sales_table.setItem(row, 2, QTableWidgetItem(sale.product))
            self.sales_table.setItem(row, 3, QTableWidgetItem(f"₺{sale.amount:,.0f}"))
            self.sales_table.setItem(row, 4, QTableWidgetItem(str(sale.quantity)))
            self.sales_table.setItem(row, 5, QTableWidgetItem(f"₺{sale.total:,.0f}"))

            status_item = QTableWidgetItem(sale.status)
            if sale.status == "Completed":
                status_item.setText("Tamamlandı")
                status_item.setForeground(QColor("#10b981"))
            elif sale.status == "Processing":
                status_item.setText("İşleniyor")
                status_item.setForeground(QColor("#06b6d4"))
            else:
                status_item.setText("Beklemede")
                status_item.setForeground(QColor("#f59e0b"))
            self.sales_table.setItem(row, 6, status_item)

        self.sales_table.resizeColumnsToContents()

    def refresh_tickets(self):
        self.tickets_table.setRowCount(0)
        for ticket in self.crm.tickets.values():
            customer = self.crm.customers.get(ticket.customer_id)
            customer_name = customer.name if customer else "Bilinmiyor"

            row = self.tickets_table.rowCount()
            self.tickets_table.insertRow(row)

            self.tickets_table.setItem(row, 0, QTableWidgetItem(str(ticket.id)))
            self.tickets_table.setItem(row, 1, QTableWidgetItem(customer_name))
            self.tickets_table.setItem(row, 2, QTableWidgetItem(ticket.subject))

            priority_item = QTableWidgetItem(ticket.priority)
            if ticket.priority == "Acil":
                priority_item.setForeground(QColor("#ef4444"))
            elif ticket.priority == "Yüksek":
                priority_item.setForeground(QColor("#f59e0b"))
            elif ticket.priority == "Orta":
                priority_item.setForeground(QColor("#06b6d4"))
            else:
                priority_item.setForeground(QColor("#10b981"))
            self.tickets_table.setItem(row, 3, priority_item)

            status_item = QTableWidgetItem(ticket.status)
            if ticket.status == "Açık":
                status_item.setForeground(QColor("#ef4444"))
            elif ticket.status == "İşlemde":
                status_item.setForeground(QColor("#f59e0b"))
            elif ticket.status == "Çözüldü":
                status_item.setForeground(QColor("#10b981"))
            else:
                status_item.setForeground(QColor("#6b7280"))
            self.tickets_table.setItem(row, 4, status_item)

            self.tickets_table.setItem(row, 5, QTableWidgetItem(ticket.date))

            # Action buttons
            action_widget = QWidget()
            action_layout = QHBoxLayout()
            action_layout.setContentsMargins(4, 4, 4, 4)
            action_layout.setSpacing(8)

            edit_btn = QPushButton("✏️")
            edit_btn.setFixedSize(30, 30)
            edit_btn.setStyleSheet("border-radius: 15px; background-color: #f59e0b;")
            edit_btn.clicked.connect(lambda checked, tid=ticket.id: self.edit_ticket(tid))

            delete_btn = QPushButton("🗑️")
            delete_btn.setFixedSize(30, 30)
            delete_btn.setStyleSheet("border-radius: 15px; background-color: #ef4444;")
            delete_btn.clicked.connect(lambda checked, tid=ticket.id: self.delete_ticket(tid))

            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            action_widget.setLayout(action_layout)

            self.tickets_table.setCellWidget(row, 6, action_widget)

        self.tickets_table.resizeColumnsToContents()

    def update_charts(self):
        # Update dashboard charts
        monthly_revenue = self.crm.get_monthly_revenue()
        self.revenue_chart.update_revenue_chart(monthly_revenue)

        product_revenue = self.crm.get_revenue_by_product()
        self.product_chart.update_pie_chart(product_revenue)

        # Update analytics charts
        self.revenue_trend_chart.update_revenue_chart(monthly_revenue)

        ticket_status = self.crm.get_tickets_by_status()
        self.ticket_status_chart.update_ticket_chart(ticket_status)

    def search_customers(self):
        search_text = self.customer_search.text().lower()
        for row in range(self.customer_table.rowCount()):
            visible = False
            for col in range(1, 5):  # Search in name, email, phone, company
                item = self.customer_table.item(row, col)
                if item and search_text in item.text().lower():
                    visible = True
                    break
            self.customer_table.setRowHidden(row, not visible)

    def search_sales(self):
        search_text = self.sale_search.text().lower()
        for row in range(self.sales_table.rowCount()):
            visible = False
            for col in range(1, 6):  # Search in customer, product, status
                item = self.sales_table.item(row, col)
                if item and search_text in item.text().lower():
                    visible = True
                    break
            self.sales_table.setRowHidden(row, not visible)

    def search_tickets(self):
        search_text = self.ticket_search.text().lower()
        for row in range(self.tickets_table.rowCount()):
            visible = False
            for col in range(1, 6):  # Search in customer, subject, priority, status
                item = self.tickets_table.item(row, col)
                if item and search_text in item.text().lower():
                    visible = True
                    break
            self.tickets_table.setRowHidden(row, not visible)

    def add_customer(self):
        dialog = CustomerDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            self.crm.add_customer(
                data["name"], data["email"], data["phone"],
                data["company"], data["status"], datetime.now().strftime("%Y-%m-%d")
            )
            self.refresh_customers()
            self.update_dashboard_stats()
            QMessageBox.information(self, "Başarılı", "Müşteri başarıyla eklendi!")

    def edit_customer(self):
        current_row = self.customer_table.currentRow()
        if current_row >= 0:
            customer_id = int(self.customer_table.item(current_row, 0).text())
            customer = self.crm.customers.get(customer_id)
            if customer:
                dialog = CustomerDialog(self, customer)
                if dialog.exec_() == QDialog.Accepted:
                    data = dialog.get_data()
                    self.crm.update_customer(
                        customer_id, data["name"], data["email"],
                        data["phone"], data["company"], data["status"]
                    )
                    self.refresh_customers()
                    QMessageBox.information(self, "Başarılı", "Müşteri başarıyla güncellendi!")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen düzenlenecek müşteriyi seçin!")

    def delete_customer(self):
        current_row = self.customer_table.currentRow()
        if current_row >= 0:
            customer_id = int(self.customer_table.item(current_row, 0).text())
            customer = self.crm.customers.get(customer_id)

            reply = QMessageBox.question(
                self, "Silme Onayı",
                f"{customer.name} müşterisini silmek istediğinize emin misiniz?\nİlişkili tüm satış ve destek talepleri de silinecektir.",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.crm.delete_customer(customer_id)
                self.refresh_customers()
                self.refresh_sales()
                self.refresh_tickets()
                self.update_dashboard_stats()
                self.update_charts()
                QMessageBox.information(self, "Başarılı", "Müşteri başarıyla silindi!")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen silinecek müşteriyi seçin!")

    def add_sale(self):
        if not self.crm.customers:
            QMessageBox.warning(self, "Uyarı", "Satış eklemeden önce müşteri ekleyin!")
            return

        dialog = SaleDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            # Select first customer for demo
            customer_id = list(self.crm.customers.keys())[0]
            self.crm.add_sale(
                customer_id, data["product"], data["amount"],
                data["quantity"], datetime.now().strftime("%Y-%m-%d"), data["status"]
            )
            self.refresh_sales()
            self.update_dashboard_stats()
            self.update_charts()
            QMessageBox.information(self, "Başarılı", "Satış başarıyla eklendi!")

    def edit_sale(self):
        current_row = self.sales_table.currentRow()
        if current_row >= 0:
            sale_id = int(self.sales_table.item(current_row, 0).text())
            sale = self.crm.sales.get(sale_id)
            if sale:
                dialog = SaleDialog(self, sale)
                if dialog.exec_() == QDialog.Accepted:
                    data = dialog.get_data()
                    self.crm.update_sale(
                        sale_id, data["product"], data["amount"],
                        data["quantity"], data["status"]
                    )
                    self.refresh_sales()
                    self.update_dashboard_stats()
                    self.update_charts()
                    QMessageBox.information(self, "Başarılı", "Satış başarıyla güncellendi!")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen düzenlenecek satışı seçin!")

    def delete_sale(self):
        current_row = self.sales_table.currentRow()
        if current_row >= 0:
            sale_id = int(self.sales_table.item(current_row, 0).text())

            reply = QMessageBox.question(
                self, "Silme Onayı",
                f"Satış #{sale_id} numaralı kaydı silmek istediğinize emin misiniz?",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.crm.delete_sale(sale_id)
                self.refresh_sales()
                self.update_dashboard_stats()
                self.update_charts()
                QMessageBox.information(self, "Başarılı", "Satış başarıyla silindi!")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen silinecek satışı seçin!")

    def add_ticket(self):
        if not self.crm.customers:
            QMessageBox.warning(self, "Uyarı", "Destek talebi oluşturmadan önce müşteri ekleyin!")
            return

        dialog = TicketDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            customer_id = list(self.crm.customers.keys())[0]
            self.crm.add_ticket(
                customer_id, data["subject"], data["description"],
                data["priority"], data["status"], datetime.now().strftime("%Y-%m-%d")
            )
            self.refresh_tickets()
            self.update_dashboard_stats()
            QMessageBox.information(self, "Başarılı", "Destek talebi başarıyla oluşturuldu!")

    def edit_ticket(self, ticket_id):
        ticket = self.crm.tickets.get(ticket_id)
        if ticket:
            dialog = TicketDialog(self, ticket)
            if dialog.exec_() == QDialog.Accepted:
                data = dialog.get_data()
                self.crm.update_ticket(ticket_id, data["priority"], data["status"])
                self.refresh_tickets()
                self.update_dashboard_stats()
                QMessageBox.information(self, "Başarılı", "Destek talebi başarıyla güncellendi!")

    def delete_ticket(self, ticket_id):
        reply = QMessageBox.question(
            self, "Silme Onayı",
            f"Destek talebi #{ticket_id} numaralı kaydı silmek istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.crm.delete_ticket(ticket_id)
            self.refresh_tickets()
            self.update_dashboard_stats()
            QMessageBox.information(self, "Başarılı", "Destek talebi başarıyla silindi!")


# ============ MAIN ==========

def main():
    app = QApplication(sys.argv)

    # Set application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = ModernCRM()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
