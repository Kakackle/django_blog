# Django todos
## modele
1. TODO: zamiast usera w pelni od zera, zrobic rozszerzenie modelu z django.contrib.auth?

## endpointy i zwracanie informacji
1. TODO: Powinien byc na 100% sposob zwracania informacji w response takich jak, ze np wybrana nazwa nie jest unique, co frontend by w response odbieral, co nie powinno byc trudne (bo axios zwraca obiekt res), ale kwestia jest jak sprawdzac w Django takie contraints i dodawac na tej bazie do response - nie powinno byc takie trudne, ale

- https://stackoverflow.com/questions/75508077/return-custom-response-on-django-rest-framework-generics-retrieve-api-view

- jest to kwestia wtedy jaka metoda ma byc wywolana, czy post czy get czy cokolwiek i overwrite (czy jak to tam w pythonie sie nazywa) jej i w response ktore zwraca dodanie poza data: serializer.data (pamietaj o serializacji!) cos typu msg: 'wiadomosc'


6. // FIXME: poki co zrobie tak ze we froncie sprawdzane czy juz polajkowane
// i w zaleznosci od tego wyslij liste z nowym uzytnikiem albo bez jak juz byl
// ale potem lepiej by to robic w django, bo to taka racej backendowa operacja
// a frontent powinien byc glownie od wyswietlania a nie trzymania stanu

7. TODO: Jakos zwracanie liked_posts, liked_comments - jest teraz, ale kulawe, komenty np zwraca po indexach zamiast w wyswietlalnej formie
- luj tam, jest okej, tylko mozna by dodac warunki typu "zwroc tylko polubione posty", "zwroc tylko wlasne posty", "posty na ktorych uzytkownik skomentowal"


8. TODO: Filtracja postow po dacie

# Duze rzeczy
1. custom user / profile i logowanie
    - potem powiazywanie tworzonych postow z aktualnym uzytkownikiem itd
    - komentarze - sposob powiazania w django i odpowiadania i forma na tworzenie

2. TODO: Followowanie uzytkownikow

## cleanup
1. Rozdzielenie views, serializatorow itd na pliki?