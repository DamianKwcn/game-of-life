import sys
from PyQt5.QtWidgets import QApplication
from plansza import Plansza
from widok import GUIWidok
from symulacja import Symulacja
from PyQt5.QtCore import QTimer

if __name__ == "__main__":
    app = QApplication(sys.argv)

    plansza = Plansza(Plansza.SZEROKOSC, Plansza.WYSOKOSC)
    widok = GUIWidok()
    symulacja = Symulacja(plansza, widok)

    timer = QTimer()
    timer.timeout.connect(symulacja.aktualizuj)
    widok.podlacz_symulacje(symulacja, timer)

    sys.exit(app.exec_())
