import pygame
import random
import sys
import math

pygame.init()

SZEROKOSC, WYSOKOSC = 800, 600
ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption("Zbijanie Balonikow")

BIALY = (255, 255, 255)
KOLORY_BALONOW = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

poziom = 1
wynik = 0
uplynelo_czasu = 0
pauza = False
zegar = pygame.time.Clock()

def generuj_baloniki():
    mnoznik_predkosci = 0.1

    if poziom == 3:
        mnoznik_predkosci = 0.2

    elif poziom == 4:
        mnoznik_predkosci = 0.5
    if poziom > 4:
        mnoznik_predkosci = 0.5 * (poziom / 5)
    return [
        {
            "x": random.randint(0, SZEROKOSC),
            "y": WYSOKOSC,
            "promien": random.randint(20 + (5 * (4 - poziom)), 50) - (poziom * 5),
            "kolor": random.choice(KOLORY_BALONOW),
            "predkosc": random.randint(1, 1) * mnoznik_predkosci,
        }
        for _ in range(12)
    ]

def generuj_wzorzec_ruchu():
    if poziom == 2:
        return lambda x: WYSOKOSC * 0.5 + WYSOKOSC * 0.4 * math.sin(x * 0.1)
    elif poziom == 3 or poziom == 4:
        return lambda x: WYSOKOSC * 0.5 * math.sin(x * 0.4) + WYSOKOSC * 0.1
    if poziom > 4:
        xaz = lambda x: WYSOKOSC * 0.5 + WYSOKOSC * 0.4 * math.sin(x * 0.1)
        xbz = lambda x: WYSOKOSC * 0.5 * math.sin(x * 0.4) + WYSOKOSC * 0.1
        xrz = random.randint(0, 1)
        if xrz == 0:
            return xaz
        if xbz == 1:
            return xbz

baloniki = generuj_baloniki()
wzorzec_ruchu = generuj_wzorzec_ruchu()

def ekran_kontynuacji():
    ekran.fill(BIALY)
    czcionka = pygame.font.Font(None, 36)
    tekst_kontynuacji = czcionka.render(f"C - aby kontynuowac, Q - aby przerwac gre. Wynik: {wynik}", True, (0, 0, 0))
    ekran.blit(tekst_kontynuacji, (SZEROKOSC // 2 - tekst_kontynuacji.get_width() // 2, WYSOKOSC // 2))
    pygame.display.flip()
    czekanie = True
    while czekanie:
        for zdarzenie in pygame.event.get():
            if zdarzenie.type == pygame.KEYDOWN:
                if zdarzenie.key == pygame.K_c:
                    return
                elif zdarzenie.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def zrestartuj_gre():
    global poziom, wynik, uplynelo_czasu, baloniki, wzorzec_ruchu
    poziom = 1
    wynik = 0
    uplynelo_czasu = 0
    baloniki = generuj_baloniki()
    wzorzec_ruchu = generuj_wzorzec_ruchu()

def ekran_koniec_gry():
    ekran.fill(BIALY)
    czcionka = pygame.font.Font(None, 32)
    tekst_koniec_gry = czcionka.render("Koniec Gry, C aby zrestartowac gre, Q aby wyjsc.", True, (255, 0, 0))
    tekst_wynik = czcionka.render(f"Twoj wynik: {wynik} punktow", True, (255, 0, 0))
    ekran.blit(tekst_koniec_gry, (SZEROKOSC // 2 - tekst_koniec_gry.get_width() // 2, WYSOKOSC // 2 - tekst_koniec_gry.get_height() // 2))
    ekran.blit(tekst_wynik, (SZEROKOSC // 2 - tekst_wynik.get_width() // 2, WYSOKOSC // 2 + 50))
    pygame.display.flip()
    czekanie = True
    while czekanie:
        for zdarzenie in pygame.event.get():
            if zdarzenie.type == pygame.KEYDOWN:
                if zdarzenie.key == pygame.K_c:
                    zrestartuj_gre()
                    return
                elif zdarzenie.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def rysuj_poziom():
    if poziom <= 4:
        czcionka = pygame.font.Font(None, 36)
        tekst_poziom = czcionka.render(f"Poziom: {poziom}", True, (0, 0, 0))
        ekran.blit(tekst_poziom, (10, 10))

def rysuj_czas():
    if poziom > 4:
        czcionka = pygame.font.Font(None, 36)
        tekst_czas = czcionka.render(f"Czas: {uplynelo_czasu / 100:.2f}", True, (0, 0, 0))
        ekran.blit(tekst_czas, (10, 10))

def rysuj_wynik():
    czcionka = pygame.font.Font(None, 36)
    tekst_wynik = czcionka.render(f"Punkty: {wynik}", True, (0, 0, 0))
    ekran.blit(tekst_wynik, (10, 40))

def rysuj_baloniki():
    for i, balonik in enumerate(baloniki):
        balonik["y"] -= balonik["predkosc"]
        balonik["promien"] = max(20, balonik["promien"])
        balonik["promien"] -= poziom * 0.02
        if poziom == 2:
            balonik["x"] += math.sin(uplynelo_czasu * 0.05) * 2
        elif poziom == 3 or poziom == 4:
            balonik["x"] += math.sin((uplynelo_czasu + i * 20) * 0.05) * 2
        if poziom > 4:
            balonik["x"] += math.sin((uplynelo_czasu + i * 20) * 0.05) * (poziom / 3)
        if balonik["x"] < 0:
            balonik["x"] = 0
        elif balonik["x"] > SZEROKOSC:
            balonik["x"] = SZEROKOSC
        pygame.draw.circle(ekran, balonik["kolor"], (int(balonik["x"]), int(balonik["y"])), int(balonik["promien"]))

def sprawdz_kolizje(mysz_x, mysz_y):
    for balonik in baloniki:
        if (balonik["x"] - balonik["promien"] < mysz_x < balonik["x"] + balonik["promien"]) and (balonik["y"] - balonik["promien"] < mysz_y < balonik["y"] + balonik["promien"]):
            return balonik
    return None

def main():
    global poziom, wynik, uplynelo_czasu, baloniki, wzorzec_ruchu, pauza

    przycisk_wyjscia = pygame.Rect(10, WYSOKOSC - 40, 100, 30)
    przycisk_restartu = pygame.Rect(120, WYSOKOSC - 40, 100, 30)
    przycisk_pauzy = pygame.Rect(230, WYSOKOSC - 40, 100, 30)

    dzialanie = True
    while dzialanie:
        for zdarzenie in pygame.event.get():
            if zdarzenie.type == pygame.QUIT:
                dzialanie = False
            elif zdarzenie.type == pygame.MOUSEBUTTONDOWN and zdarzenie.button == 1:
                mysz_x, mysz_y = pygame.mouse.get_pos()
                balonik = sprawdz_kolizje(mysz_x, mysz_y)
                if balonik:
                    wynik += 1
                    baloniki.remove(balonik)
                if przycisk_wyjscia.collidepoint(mysz_x, mysz_y):
                    pygame.quit()
                    sys.exit()
                elif przycisk_restartu.collidepoint(mysz_x, mysz_y):
                    zrestartuj_gre()
                elif przycisk_pauzy.collidepoint(mysz_x, mysz_y):
                    pauza = not pauza
            if poziom > 1 and wynik < (poziom - 1) * 12:
                ekran_koniec_gry()

        ekran.fill(BIALY)
        rysuj_poziom()
        rysuj_czas()
        rysuj_wynik()

        if not pauza:
            rysuj_baloniki()
            if all(balonik["y"] < 0 for balonik in baloniki):
                poziom += 1
                if poziom == 5:
                    ekran_kontynuacji()
                    punkty = wynik
                    zrestartuj_gre()
                    poziom = 5
                    wynik = punkty
                    continue
                baloniki = generuj_baloniki()
                wzorzec_ruchu = generuj_wzorzec_ruchu()

            uplynelo_czasu += 1

        pygame.draw.rect(ekran, (255, 0, 0), przycisk_wyjscia)
        pygame.draw.rect(ekran, (0, 255, 0), przycisk_restartu)
        pygame.draw.rect(ekran, (0, 0, 255), przycisk_pauzy)
        czcionka = pygame.font.Font(None, 36)
        ekran.blit(czcionka.render("Wyjscie", True, BIALY), (20, WYSOKOSC - 35))
        ekran.blit(czcionka.render("Reset", True, BIALY), (130, WYSOKOSC - 35))
        ekran.blit(czcionka.render("Pauza" if not pauza else "Wznow", True, BIALY), (240, WYSOKOSC - 35))

        pygame.display.flip()
        zegar.tick(100)

if __name__ == "__main__":
    main()
