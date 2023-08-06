# Django todos
## modele
1. TODO: zamiast usera w pelni od zera, zrobic rozszerzenie modelu z django.contrib.auth?
2. TODO: mozliwe jest i nawet latwe stworzenie wszystkich routes albo API schema z openAPI, kiedys by sie przydalo tym zajac, potem swagger itd

## endpointy i zwracanie informacji
1. TODO: Powinien byc na 100% sposob zwracania informacji w response takich jak, ze np wybrana nazwa nie jest unique, co frontend by w response odbieral, co nie powinno byc trudne (bo axios zwraca obiekt res), ale kwestia jest jak sprawdzac w Django takie contraints i dodawac na tej bazie do response - nie powinno byc takie trudne, ale

2. TODO: Defintywnie dodac gdzies jakies dodawanie losowych koncowek do nazw elementow jak przeslane zdjecia, zeby uzytkownik mniej sie musial martwic unikalnoscia

3. TODO: Przesylanie nowych avatarow uzytkownikow [ obrazki ], czyli dodatkowy endpoint odbierajacy obrazek i aktualizujacy w rekordzie i fajnie gdyby stary byl jednoczesnie usuwany z media

4. TODO: generalnie - jak usuwac z media?
bo kwestia co usuwac powinna byc dosyc latwa - zanim zastapisz nowym, usun stare/aktualne, hmm


## cleanup
1. Rozdzielenie views, serializatorow itd na pliki?