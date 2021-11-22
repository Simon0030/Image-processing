import cv2 as cv
import numpy as np
from PIL import Image, ImageFont, ImageDraw



imagelist = []


def zamiana_na_hsv(wejscie):
    cv.imshow('Krok1', wejscie); cv.waitKey(0);cv.destroyAllWindows();cv.waitKey(1)
    obraz_hsv = cv.cvtColor(wejscie, cv.COLOR_BGR2HSV)  # konwertowanie z bgr na hsv
    cv.imshow('Krok2', obraz_hsv);
    cv.waitKey(0);
    cv.destroyAllWindows();
    cv.waitKey(1)
    return  obraz_hsv

def sprawdz_kolor(obraz_hsv):
    granica_1 = np.array([0, 10, 60], dtype="uint8")
    granica_2 = np.array([20, 150, 255], dtype="uint8")
    #przybliżone granice koloru skóry w hsv
    wspolrzedne = cv.inRange(obraz_hsv, granica_1, granica_2)  # sprawdzenie czy na obrazku jest coś w cielistym kolorze
    return  wspolrzedne

def kontury(wspolrzedne, obraz):
    rozmycie = cv.blur(wspolrzedne, (2, 2))
    kontury_obraz, hierarchy = cv.findContours(rozmycie, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    kontury_obraz = max(kontury_obraz, key=lambda x: cv.contourArea(x))  # pobranie konturów
    cv.drawContours(obraz, [kontury_obraz], -1, (255, 0, 0), 2)  # rysowanie konturów na obrazku
    cv.imshow('Krok3', obraz);
    cv.waitKey(0);
    cv.destroyAllWindows();
    cv.waitKey(1)
    return  kontury_obraz, obraz

def wypukłosci(kontury_obraz, obraz):
    obrys = cv.convexHull(kontury_obraz)  # skorygowanie wypukłości
    cv.drawContours(obraz, [obrys], -1, (0, 0, 0), 2)
    cv.imshow('Krok4', obraz);
    cv.waitKey(0);
    cv.destroyAllWindows();
    cv.waitKey(1)
    obrys = cv.convexHull(kontury_obraz, returnPoints=False)  # zamiana wartości na wskaźniki
    tablica_niewypklosci = cv.convexityDefects(kontury_obraz, obrys)  # zamiana wad wypukłośći
    return  tablica_niewypklosci, obraz, kontury_obraz

def licz(kontury_obraz, obraz, defects):
    flaga_1_palec = 0
    ilosc = 1
    flaga = 0
    for i in range(defects.shape[0]):
        p1, p2, p3, odleglosc = defects[i, 0]
        punkt_start = (kontury_obraz[p1][0])
        punkt_konc = (kontury_obraz[p2][0])
        punkt_najdalej = (kontury_obraz[p3][0])
        a = np.sqrt((punkt_konc[0] - punkt_start[0]) ** 2 + (punkt_konc[1] - punkt_start[1]) ** 2)
        b = np.sqrt((punkt_najdalej[0] - punkt_start[0]) ** 2 + (punkt_najdalej[1] - punkt_start[1]) ** 2)
        c = np.sqrt((punkt_konc[0] - punkt_najdalej[0]) ** 2 + (punkt_konc[1] - punkt_najdalej[1]) ** 2)
        angle = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  # obliczenie kątów wypukłości
        # print(angle)
        if odleglosc > 9650:
            flaga_1_palec = 1
        if angle <= np.pi/2 and odleglosc>3000: # kąty mniejsze niż 90stopni są traktowane jako palce
            cv.line(obraz, punkt_start, punkt_konc, [0,255 , 0], 2)
            cv.circle(obraz, punkt_start, 5, [1, 102, 255], -1)
            cv.circle(obraz, punkt_konc, 5, [255, 0, 102], -1)
            cv.circle(obraz, punkt_najdalej, 5, [0, 0, 255], -1)
            cv.imshow('Krok5', obraz);
            cv.waitKey(0);
            cv.destroyAllWindows();
            cv.waitKey(1)
            ilosc += 1
            flaga = 1
    if flaga == 0 and flaga_1_palec != 1:
        ilosc = ilosc - 1
    return  ilosc, obraz

def dodaj_do_listy(wejscie, ilosc):
    my_image = Image.open(wejscie)
    title_font = ImageFont.truetype('LEMONMILK-Bold.otf', 40)
    title_text = str(ilosc)
    basewidth = 300
    wpercent = (basewidth / float(my_image.size[0]))
    hsize = int((float(my_image.size[1]) * float(wpercent)))
    my_image = my_image.resize((basewidth, hsize), Image.ANTIALIAS)
    image_editable = ImageDraw.Draw(my_image)
    image_editable.text((1, 1), title_text, (0, 0, 0), font=title_font)
    imagelist.append(my_image)

def przetwarzanie(wejscie):
    obraz = cv.imread(wejscie)
    obraz_hsv = zamiana_na_hsv(obraz)
    wspolrzedne = sprawdz_kolor(obraz_hsv)
    kontur, obraz = kontury(wspolrzedne, obraz)
    wspolrzedne_wypuklosci, obraz2, kontur1 = wypukłosci(kontur, obraz)
    ilosc_palcow, obraz3 = licz(kontur1, obraz, wspolrzedne_wypuklosci)
    print(ilosc_palcow)
    dodaj_do_listy(wejscie, ilosc_palcow)

#łatwe
#latwe = ['hand1.jpg', 'hand14.jpg', 'hand3.jpg', 'hand4.jpg', 'hand5.jpg', 'hand6.jpg', 'hand7.jpg', 'hand8.jpg', 'hand9.jpg', 'hand10.jpg']
#for i in latwe:
    #przetwarzanie(i)


#srednie = ['hand11.jpg', 'hand12.jpg', 'hand13.jpg', 'hand2.jpg', 'hand15.jpg', 'hand16.jpg', 'hand17.jpg', 'hand18.jpg', 'hand19.jpg','hand20.jpg']
#for i in srednie:
    #przetwarzanie(i)

trudne = ['hand21.jpg', 'hand22.jpg', 'hand23.jpg', 'hand24.jpg', 'hand25.jpg', 'hand26.jpg', 'hand27.jpg', 'hand28.jpg', 'hand29.jpg', 'hand30.jpg']
for i in trudne:
    przetwarzanie(i)

#imagelist[0].save("Łatwe.pdf", save_all=True, append_images=imagelist[1:])
#imagelist[0].save("Srednie.pdf", save_all=True, append_images=imagelist[1:])
imagelist[0].save("Trudne.pdf", save_all=True, append_images=imagelist[1:])


