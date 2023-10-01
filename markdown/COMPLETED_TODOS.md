1. mozliwe jest i nawet latwe stworzenie wszystkich routes albo API schema z openAPI, kiedys by sie przydalo tym zajac, potem swagger itd

2. Defintywnie dodac gdzies jakies dodawanie losowych koncowek do nazw elementow jak przeslane zdjecia, zeby uzytkownik mniej sie musial martwic unikalnoscia

3. Przesylanie nowych avatarow uzytkownikow [ obrazki ], czyli dodatkowy endpoint odbierajacy obrazek i aktualizujacy w rekordzie i fajnie gdyby stary byl jednoczesnie usuwany z media

4.  generalnie - jak usuwac z media?
bo kwestia co usuwac powinna byc dosyc latwa - zanim zastapisz nowym, usun stare/aktualne, hmm

odp: rozne sposoby:
- https://stackoverflow.com/questions/2878490/how-to-delete-old-image-when-update-imagefield

5. jakies resizowanie obrazkow przy uploadzie i zapisywanie w roznych rozmiarach typu thumbnail - jakos z PIL, widzialem ze to dziala, w section.io np

odp:
- https://www.section.io/engineering-education/an-extensive-guide-on-handling-images-in-django/
- https://stackoverflow.com/questions/273946/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio

6. DONE: poki co zrobie tak ze we froncie sprawdzane czy juz polajkowane
i w zaleznosci od tego wyslij liste z nowym uzytnikiem albo bez jak juz byl
ale potem lepiej by to robic w django, bo to taka racej backendowa operacja
a frontent powinien byc glownie od wyswietlania a nie trzymania stanu
- do zrobienia w sposob zlizony do dodawania i usuwania following

7. DONE: moze zacznij proby rozbijania od /view zwiekszajacego views zamiast we froncie

8. DONE: usuniecie zbednych views, w szczegolnosci duplikacja po ID i po slug, bo sie openschema denerwowalo i sam sie mylisz
9. a poza tym DONE: niespójność w tym czy odnosisz się do endpointów po slug czy id - potem korzystając z takiego API nigdy nie wiadomo
