class Komorka:
    def __init__(self, zywa: bool = False):
        self._zywa = zywa

    @property
    def zywa(self):
        return self._zywa

    def zmien_stan(self, stan):
        self._zywa = stan

class ZywaKomorka(Komorka):
    def __init__(self):
        super().__init__(zywa=True)

class MartwaKomorka(Komorka):
    def __init__(self):
        super().__init__(zywa=False)

class FabrykaKomorek:
    @staticmethod
    def utworz_komorke(typ):
        if typ == ZywaKomorka:
            return ZywaKomorka()
        elif typ == MartwaKomorka:
            return MartwaKomorka()
        else:
            raise ValueError(f"Nieznany typ komórki: {typ}")

class Plansza:
    _instancja = None
    SZEROKOSC = 100
    WYSOKOSC = 50

    def __new__(cls, szerokosc=SZEROKOSC, wysokosc=WYSOKOSC):
        if cls._instancja is None:
            cls._instancja = super(Plansza, cls).__new__(cls)
        return cls._instancja

    def __init__(self, szerokosc=SZEROKOSC, wysokosc=WYSOKOSC):
        if not hasattr(self, 'zainicjowano'):
            self.szerokosc = szerokosc
            self.wysokosc = wysokosc
            self.komorki = [[FabrykaKomorek.utworz_komorke(MartwaKomorka) for _ in range(wysokosc)] for _ in range(szerokosc)]
            self.obserwatorzy = []
            self.zainicjowano = True

    @staticmethod
    def instancja():
        return Plansza._instancja

    def ustaw_komorke(self, x, y, komorka):
        self.komorki[x][y] = komorka

    def pobierz_komorke(self, x, y):
        return self.komorki[x][y]

    def dodaj_obserwatora(self, obs):
        self.obserwatorzy.append(obs)

    def usun_obserwatora(self, obs):
        self.obserwatorzy.remove(obs)

    def powiadom_obserwatorow(self):
        for obs in self.obserwatorzy:
            obs.aktualizuj(self)
