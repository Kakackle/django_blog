# Django todos
## modele
1. TODO: zamiast usera w pelni od zera, zrobic rozszerzenie modelu z django.contrib.auth?

## endpointy i zwracanie informacji
1. TODO: Powinien byc na 100% sposob zwracania informacji w response takich jak, ze np wybrana nazwa nie jest unique, co frontend by w response odbieral, co nie powinno byc trudne (bo axios zwraca obiekt res), ale kwestia jest jak sprawdzac w Django takie contraints i dodawac na tej bazie do response - nie powinno byc takie trudne, ale

2. TODO: Defintywnie dodac gdzies jakies dodawanie losowych koncowek do nazw elementow jak przeslane zdjecia, zeby uzytkownik mniej sie musial martwic unikalnoscia

3. TODO: Przesylanie nowych avatarow uzytkownikow [ obrazki ], czyli dodatkowy endpoint odbierajacy obrazek i aktualizujacy w rekordzie i fajnie gdyby stary byl jednoczesnie usuwany z media

4. TODO: generalnie - jak usuwac z media?
bo kwestia co usuwac powinna byc dosyc latwa - zanim zastapisz nowym, usun stare/aktualne, hmm

5. TODO: jakies resizowanie obrazkow przy uploadzie i zapisywanie w roznych rozmiarach typu thumbnail

6. // FIXME: poki co zrobie tak ze we froncie sprawdzane czy juz polajkowane
// i w zaleznosci od tego wyslij liste z nowym uzytnikiem albo bez jak juz byl
// ale potem lepiej by to robic w django, bo to taka racej backendowa operacja
// a frontent powinien byc glownie od wyswietlania a nie trzymania stanu

7. TODO: Jakos zwracanie liked_posts, liked_comments - jest teraz, ale kulawe, komenty np zwraca po indexach


# Duze rzeczy
1. custom user / profile i logowanie
    - potem powiazywanie tworzonych postow z aktualnym uzytkownikiem itd
    - komentarze - sposob powiazania w django i odpowiadania i forma na tworzenie


## cleanup
1. Rozdzielenie views, serializatorow itd na pliki?