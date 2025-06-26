from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QColor
from plansza import Plansza
from obserwator import Obserwator

class PlanszaView(QGraphicsView):
    def __init__(self, scene, plansza, parent=None):
        super().__init__(scene, parent)
        self.plansza = plansza
        self.setMouseTracking(True)
        self.drawing = False
        self.editable = True

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.editable:
            self.drawing = True
            self.ozyw_komorke(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def mouseMoveEvent(self, event):
        if self.drawing and self.editable:
            self.ozyw_komorke(event)

    def ozyw_komorke(self, event):
        pos = self.mapToScene(event.pos())
        w = self.viewport().width()
        h = self.viewport().height()
        cell_width = w / self.plansza.szerokosc
        cell_height = h / self.plansza.wysokosc
        x = int(pos.x() / cell_width)
        y = int(pos.y() / cell_height)
        if 0 <= x < self.plansza.szerokosc and 0 <= y < self.plansza.wysokosc:
            komorka = self.plansza.pobierz_komorke(x, y)
            if not komorka.zywa:
                komorka.zmien_stan(True)
                self.plansza.powiadom_obserwatorow()

class GUIWidok(Obserwator):
    def __init__(self):
        super().__init__()
        self.window = QWidget()
        self.layout = QVBoxLayout(self.window)
        self.label = QLabel("Gra w Życie", self.window)
        self.label.setStyleSheet("color: #1de9b6; font-size: 20px; font-weight: bold; background: transparent;")
        self.layout.addWidget(self.label)

        self.buttons_layout = QHBoxLayout()
        self.start_button = QPushButton("START")
        self.stop_button = QPushButton("STOP")
        self.start_button.setFixedWidth(100)
        self.stop_button.setFixedWidth(100)
        self.start_button.clicked.connect(self.rozpocznij_symulacje)
        self.stop_button.clicked.connect(self.zatrzymaj_symulacje)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #1de9b6;
                color: #181a1b;
                border-radius: 10px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:disabled {
                background-color: #1de9b699;
                color: #23272b;
            }
        """)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #1de9b6;
                color: #181a1b;
                border-radius: 10px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:disabled {
                background-color: #1de9b699;
                color: #23272b;
            }
        """)
        self.buttons_layout.addWidget(self.start_button)
        self.buttons_layout.addWidget(self.stop_button)
        self.layout.addLayout(self.buttons_layout)

        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QColor("#000000"))
        self.view = PlanszaView(self.scene, Plansza.instancja(), self.window)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.layout.addWidget(self.view)
        self.window.setLayout(self.layout)
        self.window.setWindowTitle("Gra w Życie")
        self.window.resize(1000, 600)
        self.window.setStyleSheet("background-color: #000000;")
        self.window.show()

        self.simulation_running = False
        self.timer = None
        self.symulacja = None
        self.stop_button.setEnabled(False)
        self.aktualizuj_widok()

    def podlacz_symulacje(self, symulacja, timer):
        self.symulacja = symulacja
        self.timer = timer

    def rozpocznij_symulacje(self):
        if not self.simulation_running:
            self.simulation_running = True
            self.view.editable = False
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            if self.timer:
                self.timer.start(200)

    def zatrzymaj_symulacje(self):
        if self.simulation_running:
            self.simulation_running = False
            if self.timer:
                self.timer.stop()
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.view.editable = True

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.aktualizuj_widok()

    def aktualizuj(self, plansza):
        self.aktualizuj_widok()

    def aktualizuj_widok(self):
        plansza = Plansza.instancja()
        self.scene.clear()
        w = self.view.viewport().width()
        h = self.view.viewport().height()
        cell_width = w / plansza.szerokosc
        cell_height = h / plansza.wysokosc

        self.scene.setSceneRect(0, 0, w, h)

        turkus = QColor("#1de9b6")
        szary = QColor("#424242")
        tlo = QColor("#000000")

        self.scene.setBackgroundBrush(tlo)

        thin_pen = QPen(szary)
        thin_pen.setWidth(1)

        for x in range(plansza.szerokosc):
            for y in range(plansza.wysokosc):
                rect = QGraphicsRectItem(x * cell_width, y * cell_height, cell_width, cell_height)
                komorka = plansza.pobierz_komorke(x, y)
                if komorka.zywa:
                    rect.setBrush(turkus)
                rect.setPen(thin_pen)
                self.scene.addItem(rect)
