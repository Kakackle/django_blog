# Django todos
## modele
1. TODO: zamiast usera w pelni od zera, zrobic rozszerzenie modelu z django.contrib.auth?

## endpointy i zwracanie informacji
1. Powinien byc na 100% sposob zwracania informacji w response takich jak, ze np wybrana nazwa nie jest unique, co frontend by w response odbieral, co nie powinno byc trudne (bo axios zwraca obiekt res), ale kwestia jest jak sprawdzac w Django takie contraints i dodawac na tej bazie do response - nie powinno byc takie trudne, ale

- https://stackoverflow.com/questions/75508077/return-custom-response-on-django-rest-framework-generics-retrieve-api-view

- jest to kwestia wtedy jaka metoda ma byc wywolana, czy post czy get czy cokolwiek i overwrite (czy jak to tam w pythonie sie nazywa) jej i w response ktore zwraca dodanie poza data: serializer.data (pamietaj o serializacji!) cos typu msg: 'wiadomosc'

Zatem: TODO: w lakich endpointach bys chcial to dodac i co konkretnie zwracac
oraz kwestia gdy sa bledy jak rozpoznawac

6. DONE: poki co zrobie tak ze we froncie sprawdzane czy juz polajkowane
i w zaleznosci od tego wyslij liste z nowym uzytnikiem albo bez jak juz byl
ale potem lepiej by to robic w django, bo to taka racej backendowa operacja
a frontent powinien byc glownie od wyswietlania a nie trzymania stanu
- do zrobienia w sposob zlizony do dodawania i usuwania following

7. DONE: moze zacznij proby rozbijania od /view zwiekszajacego views zamiast we froncie

8. OPTIONAL: zwracanie liczby followowers w obie strony - jakos w modelu czy tylko w view? - to mozna dodac jakos po prostu w response albo dodac pola to uzytkownika tak jak post ma aktualnie likes i auaktualniac w endpointach followowania uzytkownikow itd - tylko wlasnie - musialoby (najlatwiej) byc to pelnoprawne pole typu followers = Integer, followed = ...

9. OPTIONAL: post list view - specjalne tryby filtracji - moze mozna by zalogowanego uzytkownika przesylac w body albo gdzies oddzielnie w query, i potem kazda metoda mogla z tego korzystac, a nie ze kazda metoda podaje sama, bo to zbyteczne troche


# Duze rzeczy
1. custom user / profile i logowanie
    - potem powiazywanie tworzonych postow z aktualnym uzytkownikiem itd
    - komentarze - sposob powiazania w django i odpowiadania i forma na tworzenie

3. TODO: REFACTOR ENDPOINTÓW / VIEWS - rozbicie na mniejsze, intuicyjne, one purpose, np. dla postów, oddzielne /view, /like, /unlike i inne, zwykly z query, /all, /szczegolne warunki

4. TODO: usuniecie zbednych views, w szczegolnosci duplikacja po ID i po slug, bo sie openschema denerwowalo i sam sie mylisz


## cleanup
1. Rozdzielenie views, serializatorow itd na pliki?