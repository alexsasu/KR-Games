import copy
import time

import pygame
import sys
import math


ADANCIME_MAX = 6


def distEuclid(p0, p1):
    (x0, y0) = p0
    (x1, y1) = p1
    return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)

def validitate_mutare(jucator, pozitieCurenta, pozitieDorita, coordonateNoduri, nrMutariPeVerticalaConsecutiveCaini):
    if jucator == 'c':
        if coordonateNoduri[pozitieCurenta][0] > coordonateNoduri[pozitieDorita][0]:
            return False
        if coordonateNoduri[pozitieCurenta][0] == coordonateNoduri[pozitieDorita][0]:
            return nrMutariPeVerticalaConsecutiveCaini + 1
        return 0

class Joc:
    JMIN = None
    JMAX = None

    # coordonatele nodurilor ()
    noduri = [
        (1, 2),  # 0
        (2, 2),  # 1
        (3, 2),  # 2
        (0, 1),  # 3
        (1, 1),  # 4
        (2, 1),  # 5
        (3, 1),  # 6
        (4, 1),  # 7
        (1, 0),  # 8
        (2, 0),  # 9
        (3, 0),  # 10
    ]
    # muchii = [(0, 1), (0, 3), (0, 4), (0, 5), (1, 2), (1, 5), (2, 5), (2, 6), (2, 7),
    #           (3, 4), (3, 8), (4, 5), (4, 8), (5, 6), (5, 8), (5, 9), (5, 10), (6, 7), (6, 10), (7, 10),
    #           (8, 9), (9, 10)]
    muchii = [(3, 0), (3, 4), (3, 8), (0, 1), (0, 5), (0, 4), (4, 5), (4, 8), (8, 5), (8, 9),
              (1, 2), (1, 5), (5, 2), (5, 6), (5, 10), (5, 9), (9, 10), (2, 7), (2, 6), (6, 7), (6, 10), (10, 7)]
    scalare = 100
    translatie = 20
    razaPct = 10
    razaPiesa = 20

    @classmethod
    def initializeaza(cls):
        cls.ecran = pygame.display.set_mode(size=(700, 400))
        cls.culoareEcran = (255, 255, 255)
        cls.culoareLinii = (0, 0, 0)

        cls.piesaAlba = pygame.image.load('piesa-alba.png')
        cls.diametruPiesa = 2 * Joc.razaPiesa
        cls.piesaAlba = pygame.transform.scale(cls.piesaAlba, (cls.diametruPiesa, cls.diametruPiesa))
        cls.piesaNeagra = pygame.image.load('piesa-neagra.png')
        cls.piesaNeagra = pygame.transform.scale(cls.piesaNeagra, (cls.diametruPiesa, cls.diametruPiesa))
        cls.piesaVerde = pygame.image.load('piesa-verde.png')
        cls.piesaVerde = pygame.transform.scale(cls.piesaVerde, (cls.diametruPiesa, cls.diametruPiesa))
        cls.piesaSelectata = pygame.image.load('piesa-rosie.png')
        cls.piesaSelectata = pygame.transform.scale(cls.piesaSelectata, (cls.diametruPiesa, cls.diametruPiesa))
        cls.coordonateNoduri = [[Joc.translatie + Joc.scalare * x for x in nod] for nod in Joc.noduri]
        cls.pieseAlbe = [[420, 120]]
        cls.nodPiesaSelectata = None
        cls.pieseNegre = [[120, 220], [20, 120], [120, 20]]
        cls.nrMutariPeVerticalaConsecutiveCaini = 0

    def __init__(self, pieseAlbe=None, pieseNegre=None, nrMutariPeVerticalaConsecutiveCaini=None):
        self.pieseAlbe = pieseAlbe or [[420, 120]]
        self.pieseNegre = pieseNegre or [[120, 220], [20, 120], [120, 20]]
        self.nrMutariPeVerticalaConsecutiveCaini = nrMutariPeVerticalaConsecutiveCaini or 0

    def deseneazaEcranJoc(self):
        rezultat = self.final()
        self.ecran.fill(self.culoareEcran)
        for nod in self.coordonateNoduri:
            pygame.draw.circle(surface=self.ecran, color=self.culoareLinii, center=nod, radius=self.__class__.razaPct,
                               width=0)  # width=0 face un cerc plin

        for muchie in self.__class__.muchii:
            p0 = self.coordonateNoduri[muchie[0]]
            p1 = self.coordonateNoduri[muchie[1]]
            pygame.draw.line(surface=self.ecran, color=self.culoareLinii, start_pos=p0, end_pos=p1, width=5)
        for nod in self.pieseAlbe:
            if rezultat == 'i':
                self.ecran.blit(self.piesaVerde, (nod[0] - self.__class__.razaPiesa, nod[1] - self.__class__.razaPiesa))
            else:
                self.ecran.blit(self.piesaAlba, (nod[0] - self.__class__.razaPiesa, nod[1] - self.__class__.razaPiesa))
        for nod in self.pieseNegre:
            if rezultat == 'c':
                self.ecran.blit(self.piesaVerde, (nod[0] - self.__class__.razaPiesa, nod[1] - self.__class__.razaPiesa))
            else:
                self.ecran.blit(self.piesaNeagra, (nod[0] - self.__class__.razaPiesa, nod[1] - self.__class__.razaPiesa))
        if self.nodPiesaSelectata:
            self.ecran.blit(self.piesaSelectata, (self.nodPiesaSelectata[0] - self.__class__.razaPiesa, self.nodPiesaSelectata[1] - self.__class__.razaPiesa))
        pygame.display.update()

    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def final(self):
        if self.nrMutariPeVerticalaConsecutiveCaini >= 10:
            if self.JMIN == 'i':
                return self.JMIN
            else:
                return self.JMAX
        elif self.pieseAlbe[0][0] < self.pieseNegre[0][0] \
                and self.pieseAlbe[0][0] < self.pieseNegre[1][0] \
                and self.pieseAlbe[0][0] < self.pieseNegre[2][0]:
            if self.JMIN == 'i':
                return self.JMIN
            else:
                return self.JMAX
        else:
            indexPiesaNeagra1 = self.coordonateNoduri.index(self.pieseNegre[0])
            indexPiesaNeagra2 = self.coordonateNoduri.index(self.pieseNegre[1])
            indexPiesaNeagra3 = self.coordonateNoduri.index(self.pieseNegre[2])
            muchiiPiesaAlba = []
            indexPiesaAlba = self.coordonateNoduri.index(self.pieseAlbe[0])
            for muchie in self.muchii:
                if muchie[0] == indexPiesaAlba or muchie[1] == indexPiesaAlba:
                    muchiiPiesaAlba.append(muchie)
            if len(muchiiPiesaAlba) > 3:
                return False
            else:
                nrMuchiiOcupate = 0
                if (indexPiesaAlba, indexPiesaNeagra1) in muchiiPiesaAlba \
                        or (indexPiesaNeagra1, indexPiesaAlba) in muchiiPiesaAlba:
                    nrMuchiiOcupate += 1
                if (indexPiesaAlba, indexPiesaNeagra2) in muchiiPiesaAlba \
                        or (indexPiesaNeagra2, indexPiesaAlba) in muchiiPiesaAlba:
                    nrMuchiiOcupate += 1
                if (indexPiesaAlba, indexPiesaNeagra3) in muchiiPiesaAlba \
                        or (indexPiesaNeagra3, indexPiesaAlba) in muchiiPiesaAlba:
                    nrMuchiiOcupate += 1
                if nrMuchiiOcupate == 3:
                    if self.JMIN == 'c':
                        return self.JMIN
                    else:
                        return self.JMAX
                else:
                    return False

    def mutari(self, jucator):  # jucator = simbolul jucatorului care muta
        indexPiesaNeagra1 = self.coordonateNoduri.index(self.pieseNegre[0])
        indexPiesaNeagra2 = self.coordonateNoduri.index(self.pieseNegre[1])
        indexPiesaNeagra3 = self.coordonateNoduri.index(self.pieseNegre[2])
        indexPiesaAlba = self.coordonateNoduri.index(self.pieseAlbe[0])

        l_mutari = []
        if jucator == 'c':
            for muchie in self.muchii:
                if (muchie[0] == indexPiesaNeagra1 or muchie[1] == indexPiesaNeagra1) and \
                        (muchie[0] != indexPiesaAlba and muchie[0] != indexPiesaNeagra2 and muchie[0] != indexPiesaNeagra3 and
                         muchie[1] != indexPiesaAlba and muchie[1] != indexPiesaNeagra2 and muchie[1] != indexPiesaNeagra3):
                    if muchie[0] != indexPiesaNeagra1:
                        if validitate_mutare(jucator, muchie[1], muchie[0], self.coordonateNoduri, self.nrMutariPeVerticalaConsecutiveCaini) is not False:
                            copie_piese_negre = [copy.deepcopy(self.coordonateNoduri[muchie[0]]), copy.deepcopy(self.pieseNegre[1]), copy.deepcopy(self.pieseNegre[2])]
                            l_mutari.append(Joc(copy.deepcopy(self.pieseAlbe), copie_piese_negre, validitate_mutare(jucator, muchie[1], muchie[0], self.coordonateNoduri, self.nrMutariPeVerticalaConsecutiveCaini)))
                    else:
                        if validitate_mutare(jucator, muchie[0], muchie[1], self.coordonateNoduri, self.nrMutariPeVerticalaConsecutiveCaini) is not False:
                            copie_piese_negre = [copy.deepcopy(self.coordonateNoduri[muchie[1]]), copy.deepcopy(self.pieseNegre[1]), copy.deepcopy(self.pieseNegre[2])]
                            l_mutari.append(Joc(copy.deepcopy(self.pieseAlbe), copie_piese_negre, validitate_mutare(jucator, muchie[0], muchie[1], self.coordonateNoduri, self.nrMutariPeVerticalaConsecutiveCaini)))

                elif (muchie[0] == indexPiesaNeagra2 or muchie[1] == indexPiesaNeagra2) and \
                        (muchie[0] != indexPiesaAlba and muchie[0] != indexPiesaNeagra1 and muchie[0] != indexPiesaNeagra3 and
                         muchie[1] != indexPiesaAlba and muchie[1] != indexPiesaNeagra1 and muchie[1] != indexPiesaNeagra3):
                    if muchie[0] != indexPiesaNeagra2:
                        if validitate_mutare(jucator, muchie[1], muchie[0], self.coordonateNoduri, self.nrMutariPeVerticalaConsecutiveCaini) is not False:
                            copie_piese_negre = [copy.deepcopy(self.pieseNegre[0]), copy.deepcopy(self.coordonateNoduri[muchie[0]]), copy.deepcopy(self.pieseNegre[2])]
                            l_mutari.append(Joc(copy.deepcopy(self.pieseAlbe), copie_piese_negre, validitate_mutare(jucator, muchie[1], muchie[0], self.coordonateNoduri, self.nrMutariPeVerticalaConsecutiveCaini)))
                    else:
                        if validitate_mutare(jucator, muchie[0], muchie[1], self.coordonateNoduri, self.nrMutariPeVerticalaConsecutiveCaini) is not False:
                            copie_piese_negre = [copy.deepcopy(self.pieseNegre[0]), copy.deepcopy(self.coordonateNoduri[muchie[1]]), copy.deepcopy(self.pieseNegre[2])]
                            l_mutari.append(Joc(copy.deepcopy(self.pieseAlbe), copie_piese_negre, validitate_mutare(jucator, muchie[0], muchie[1], self.coordonateNoduri, self.nrMutariPeVerticalaConsecutiveCaini)))

                elif (muchie[0] == indexPiesaNeagra3 or muchie[1] == indexPiesaNeagra3) and \
                        (muchie[0] != indexPiesaAlba and muchie[0] != indexPiesaNeagra1 and muchie[0] != indexPiesaNeagra2 and
                         muchie[1] != indexPiesaAlba and muchie[1] != indexPiesaNeagra1 and muchie[1] != indexPiesaNeagra2):
                    if muchie[0] != indexPiesaNeagra3:
                        if validitate_mutare(jucator, muchie[1], muchie[0], self.coordonateNoduri, self.nrMutariPeVerticalaConsecutiveCaini) is not False:
                            copie_piese_negre = [copy.deepcopy(self.pieseNegre[0]), copy.deepcopy(self.pieseNegre[1]), copy.deepcopy(self.coordonateNoduri[muchie[0]])]
                            l_mutari.append(Joc(copy.deepcopy(self.pieseAlbe), copie_piese_negre, validitate_mutare(jucator, muchie[1], muchie[0], self.coordonateNoduri, self.nrMutariPeVerticalaConsecutiveCaini)))
                    else:
                        if validitate_mutare(jucator, muchie[0], muchie[1], self.coordonateNoduri, self.nrMutariPeVerticalaConsecutiveCaini) is not False:
                            copie_piese_negre = [copy.deepcopy(self.pieseNegre[0]), copy.deepcopy(self.pieseNegre[1]), copy.deepcopy(self.coordonateNoduri[muchie[1]])]
                            l_mutari.append(Joc(copy.deepcopy(self.pieseAlbe), copie_piese_negre, validitate_mutare(jucator, muchie[0], muchie[1], self.coordonateNoduri, self.nrMutariPeVerticalaConsecutiveCaini)))
        elif jucator == 'i':
            for muchie in self.muchii:
                if (muchie[0] == indexPiesaAlba or muchie[1] == indexPiesaAlba) and \
                        (muchie[0] != indexPiesaNeagra1 and muchie[0] != indexPiesaNeagra2 and muchie[0] != indexPiesaNeagra3 and
                         muchie[1] != indexPiesaNeagra1 and muchie[1] != indexPiesaNeagra2 and muchie[1] != indexPiesaNeagra3):
                    if muchie[0] != indexPiesaAlba:
                        copie_piese_albe = [copy.deepcopy(self.coordonateNoduri[muchie[0]])]
                    else:
                        copie_piese_albe = [copy.deepcopy(self.coordonateNoduri[muchie[1]])]
                    l_mutari.append(Joc(copie_piese_albe, copy.deepcopy(self.pieseNegre), self.nrMutariPeVerticalaConsecutiveCaini))

        return l_mutari

    def nr_pozitii_avantajoase(self, jucator):
        indexPiesaNeagra1 = self.coordonateNoduri.index(self.pieseNegre[0])
        indexPiesaNeagra2 = self.coordonateNoduri.index(self.pieseNegre[1])
        indexPiesaNeagra3 = self.coordonateNoduri.index(self.pieseNegre[2])
        indexPiesaAlba = self.coordonateNoduri.index(self.pieseAlbe[0])
        nrPozitiiAvantajoase = 0
        if jucator == 'c':
            noduriVecineIepure = []
            nrRuteVecineIepureBlocateDeCaini = 0
            for muchie in self.muchii:
                if (muchie[0] == indexPiesaAlba or muchie[1] == indexPiesaAlba) and \
                        (muchie[0] == indexPiesaNeagra1 or muchie[0] == indexPiesaNeagra2 or muchie[0] == indexPiesaNeagra3 or
                         muchie[1] == indexPiesaNeagra1 or muchie[1] == indexPiesaNeagra2 or muchie[1] == indexPiesaNeagra3):
                    if muchie[0] == indexPiesaAlba:
                        noduriVecineIepure.append(muchie[1])
                    else:
                        noduriVecineIepure.append(muchie[0])
                    nrRuteVecineIepureBlocateDeCaini += 1
            for muchie in self.muchii:
                if (muchie[0] == indexPiesaNeagra1 or muchie[1] == indexPiesaNeagra1) and \
                        (muchie[0] != indexPiesaAlba and muchie[0] != indexPiesaNeagra2 and muchie[0] != indexPiesaNeagra3 and
                         muchie[1] != indexPiesaAlba and muchie[1] != indexPiesaNeagra2 and muchie[1] != indexPiesaNeagra3):
                    if muchie[0] == indexPiesaNeagra1:
                        if muchie[1] in noduriVecineIepure:
                            nrPozitiiAvantajoase += (nrRuteVecineIepureBlocateDeCaini + 1)
                    else:
                        if muchie[0] in noduriVecineIepure:
                            nrPozitiiAvantajoase += (nrRuteVecineIepureBlocateDeCaini + 1)

                if (muchie[0] == indexPiesaNeagra2 or muchie[1] == indexPiesaNeagra2) and \
                        (muchie[0] != indexPiesaAlba and muchie[0] != indexPiesaNeagra1 and muchie[0] != indexPiesaNeagra3 and
                         muchie[1] != indexPiesaAlba and muchie[1] != indexPiesaNeagra1 and muchie[1] != indexPiesaNeagra3):
                    if muchie[0] == indexPiesaNeagra2:
                        if muchie[1] in noduriVecineIepure:
                            nrPozitiiAvantajoase += (nrRuteVecineIepureBlocateDeCaini + 1)
                    else:
                        if muchie[0] in noduriVecineIepure:
                            nrPozitiiAvantajoase += (nrRuteVecineIepureBlocateDeCaini + 1)

                if (muchie[0] == indexPiesaNeagra3 or muchie[1] == indexPiesaNeagra3) and \
                        (muchie[0] != indexPiesaAlba and muchie[0] != indexPiesaNeagra1 and muchie[0] != indexPiesaNeagra2 and
                         muchie[1] != indexPiesaAlba and muchie[1] != indexPiesaNeagra1 and muchie[1] != indexPiesaNeagra2):
                    if muchie[0] == indexPiesaNeagra3:
                        if muchie[1] in noduriVecineIepure:
                            nrPozitiiAvantajoase += (nrRuteVecineIepureBlocateDeCaini + 1)
                    else:
                        if muchie[0] in noduriVecineIepure:
                            nrPozitiiAvantajoase += (nrRuteVecineIepureBlocateDeCaini + 1)
        else:
            for muchie in self.muchii:
                if muchie[1] == indexPiesaAlba and (muchie[0] != indexPiesaNeagra1 and muchie[0] != indexPiesaNeagra2 and muchie[0] != indexPiesaNeagra3):
                    if self.coordonateNoduri[muchie[0]][0] <= self.coordonateNoduri[indexPiesaNeagra1][0]:
                        nrPozitiiAvantajoase += 1
                    if self.coordonateNoduri[muchie[0]][0] <= self.coordonateNoduri[indexPiesaNeagra2][0]:
                        nrPozitiiAvantajoase += 1
                    if self.coordonateNoduri[muchie[0]][0] <= self.coordonateNoduri[indexPiesaNeagra3][0]:
                        nrPozitiiAvantajoase += 1

        return nrPozitiiAvantajoase

    def estimeaza_scor(self, adancime):
        t_final = self.final()
        if t_final == self.__class__.JMAX:
            return (99 + adancime)
        elif t_final == self.__class__.JMIN:
            return (-99 - adancime)
        else:
            return (self.nr_pozitii_avantajoase(self.__class__.JMAX) - self.nr_pozitii_avantajoase(self.__class__.JMIN))

    def sirAfisare(self):
        sir = "  " + ('c' if [120, 20] in self.pieseNegre else 'i' if [120, 20] in self.pieseAlbe else '*') + '-' + ('c' if [220, 20] in self.pieseNegre else 'i' if [220, 20] in self.pieseAlbe else '*') + '-' + ('c' if [320, 20] in self.pieseNegre else 'i' if [320, 20] in self.pieseAlbe else '*') + '\n' \
              + " /|\\|/|\\" + '\n' \
              + ('c' if [20, 120] in self.pieseNegre else 'i' if [20, 120] in self.pieseAlbe else '*') + '-' + ('c' if [120, 120] in self.pieseNegre else 'i' if [120, 120] in self.pieseAlbe else '*') + '-' + ('c' if [220, 120] in self.pieseNegre else 'i' if [220, 120] in self.pieseAlbe else '*') + '-' + ('c' if [320, 120] in self.pieseNegre else 'i' if [320, 120] in self.pieseAlbe else '*') + '-' + ('c' if [420, 120] in self.pieseNegre else 'i' if [420, 120] in self.pieseAlbe else '*') + '\n' \
              + " \\|/|\\|/" + '\n' \
              + "  " + ('c' if [120, 220] in self.pieseNegre else 'i' if [120, 220] in self.pieseAlbe else '*') + '-' + ('c' if [220, 220] in self.pieseNegre else 'i' if [220, 220] in self.pieseAlbe else '*') + '-' + ('c' if [320, 220] in self.pieseNegre else 'i' if [320, 220] in self.pieseAlbe else '*') + '\n'

        return sir

    def __str__(self):
        return self.sirAfisare()

    def __repr__(self):
        return self.sirAfisare()


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
    """

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare = estimare

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = Joc.jucator_opus(self.j_curent)
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Jucatorul curent: " + ("cainii" if self.j_curent == 'c' else "iepurele") + ")\n"
        return sir


def min_max(stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)
    stare.estimare = stare.stare_aleasa.estimare
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (estimare_curenta < stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (alpha < stare_noua.estimare):
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float('inf')

        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare)

            if (estimare_curenta > stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare

            if (beta > stare_noua.estimare):
                beta = stare_noua.estimare
                if alpha >= beta:
                    break

    stare.estimare = stare.stare_aleasa.estimare

    return stare


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if (final):
        print("Au castigat cainii" if final == 'c' else "A castigat iepurele")
        return True
    return False


def main():
    # initializare algoritm
    raspuns_valid = False
    while not raspuns_valid:
        tip_algoritm = input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1. Minimax\n 2. Alpha-beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")
    # initializare jucatori
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = input("Doriti sa jucati cu cainii sau cu iepurele? (introdu litera \'c\' sau \'i\') ").lower()
        if (Joc.JMIN in ['c', 'i']):
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie \'c\' sau \'i\'!")
    Joc.JMAX = 'i' if Joc.JMIN == 'c' else 'c'
    raspuns_valid = False
    while not raspuns_valid:
        nivel_dificultate = input("Nivelul de dificultate al jocului? (raspundeti cu 1, 2, sau 3)\n 1. Incepator\n 2. Mediu\n 3. Avansat\n")
        if nivel_dificultate in ['1', '2', '3']:
            raspuns_valid = True
        else:
            print("Nu ati ales un nivel de dificultate valid.")
    if nivel_dificultate == '1':
        ADANCIME_MAX = 1
    elif nivel_dificultate == '2':
        ADANCIME_MAX = 4
    elif nivel_dificultate == '3':
        ADANCIME_MAX = 8
    # initializare tabla
    tabla_curenta = Joc();
    tabla_curenta.initializeaza()
    print(tabla_curenta.coordonateNoduri)
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, 'c', ADANCIME_MAX)

    # setari interfata grafica
    pygame.init()
    pygame.display.set_caption('Sasu Alexandru-Cristian: ex_recapitulare_jocuri_minimax_alphabeta')

    tabla_curenta.deseneazaEcranJoc()
    flag = False

    while True:
        if not flag:
            flag = True
            print("Acum muta " + ("cainii" if stare_curenta.j_curent == 'c' else "iepurele") + '\n')

        if stare_curenta.j_curent == Joc.JMIN:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_r:
                        tabla_curenta = Joc();
                        stare_curenta = Stare(tabla_curenta, 'c', ADANCIME_MAX)
                        Joc.initializeaza()
                        tabla_curenta.deseneazaEcranJoc()
                elif ev.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for nod in stare_curenta.tabla_joc.coordonateNoduri:
                        if distEuclid(pos, nod) <= Joc.razaPct:  # testare ca am apasat pe un nod
                            if stare_curenta.j_curent == 'c':
                                pieseCurente = stare_curenta.tabla_joc.pieseNegre
                            else:
                                pieseCurente = stare_curenta.tabla_joc.pieseAlbe

                            if nod not in stare_curenta.tabla_joc.pieseAlbe + stare_curenta.tabla_joc.pieseNegre:  # testare ca nodul pe care am apasat nu se afla printre nodurile deja ocupate
                                if stare_curenta.tabla_joc.nodPiesaSelectata:  # vrem sa repozitionam un nod
                                    n0 = stare_curenta.tabla_joc.coordonateNoduri.index(nod)
                                    n1 = stare_curenta.tabla_joc.coordonateNoduri.index(stare_curenta.tabla_joc.nodPiesaSelectata)
                                    if ((n0, n1) in Joc.muchii or (n1, n0) in Joc.muchii):
                                        if stare_curenta.j_curent == 'c':
                                            if stare_curenta.tabla_joc.coordonateNoduri[n0][0] >= stare_curenta.tabla_joc.coordonateNoduri[n1][0]:
                                                pieseCurente.remove(stare_curenta.tabla_joc.nodPiesaSelectata)
                                                pieseCurente.append(nod)

                                                print("\nTabla dupa mutarea jucatorului:")
                                                print(str(stare_curenta))

                                                stare_curenta.tabla_joc.nrMutariPeVerticalaConsecutiveCaini = validitate_mutare(stare_curenta.j_curent, n1, n0, stare_curenta.tabla_joc.coordonateNoduri, stare_curenta.tabla_joc.nrMutariPeVerticalaConsecutiveCaini)

                                                stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                                stare_curenta.tabla_joc.nodPiesaSelectata = False

                                                flag = False

                                                if (afis_daca_final(stare_curenta)):
                                                    break
                                        else:
                                            pieseCurente.remove(stare_curenta.tabla_joc.nodPiesaSelectata)
                                            pieseCurente.append(nod)

                                            print("\nTabla dupa mutarea jucatorului:")
                                            print(str(stare_curenta))

                                            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                            stare_curenta.tabla_joc.nodPiesaSelectata = False

                                            flag = False

                                            if (afis_daca_final(stare_curenta)):
                                                break
                            else:
                                if nod in pieseCurente:  # daca nodul pe care am apasat se afla printre nodurile ocupate de catre jucatorul curent
                                    if stare_curenta.tabla_joc.nodPiesaSelectata == nod:  # am apasat pe un nod pe care il selectasem (un nod care era rosu, iar acum o sa revina la culoarea initiala)
                                        stare_curenta.tabla_joc.nodPiesaSelectata = False
                                    else:
                                        stare_curenta.tabla_joc.nodPiesaSelectata = nod

                            stare_curenta.tabla_joc.deseneazaEcranJoc()
        else:  # Mutare calculator
            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print("Tabla dupa mutarea calculatorului:")
            print(str(stare_curenta))

            stare_curenta.tabla_joc.deseneazaEcranJoc()
            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.\n")

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)

            flag = False

            if (afis_daca_final(stare_curenta)):
                break


if __name__ == "__main__":
    main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()