from plansza import Plansza, FabrykaKomorek, MartwaKomorka

class Symulacja:
    def __init__(self, plansza, obserwator):
        self.plansza = plansza
        self.plansza.dodaj_obserwatora(obserwator)

    def policz_sasiadow(self, x, y):
        liczba = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.plansza.szerokosc and 0 <= ny < self.plansza.wysokosc:
                    if self.plansza.pobierz_komorke(nx, ny).zywa:
                        liczba += 1
        return liczba

    def aktualizuj(self):
        nowe_komorki = [[FabrykaKomorek.utworz_komorke(MartwaKomorka) for _ in range(self.plansza.wysokosc)] for _ in range(self.plansza.szerokosc)]
        for x in range(self.plansza.szerokosc):
            for y in range(self.plansza.wysokosc):
                zywa = self.plansza.pobierz_komorke(x, y).zywa
                sasiedzi = self.policz_sasiadow(x, y)

                if zywa and sasiedzi in (2, 3):
                    nowe_komorki[x][y].zmien_stan(True)
                elif not zywa and sasiedzi == 3:
                    nowe_komorki[x][y].zmien_stan(True)
        for x in range(self.plansza.szerokosc):
            for y in range(self.plansza.wysokosc):
                self.plansza.ustaw_komorke(x, y, nowe_komorki[x][y])
        self.plansza.powiadom_obserwatorow()
