# Rozwiazane kwestie

1. Przesylanie do API w postaci post lub patch danych zawierajacych nawiazania do innych modeli (model relations)

jest to o tyle zwodny problem, ze wydawaloby sie, ze jesli w serializatorze ustawisz laczenie pol poprzez np slug, to przesylajac slug, view powinien rozumiec by znalezc ten model po slugu

problemem jest jednak, ze domyslnym dla DB polem kluczowym jest id/pk, wiec probujac podawac w requescie to pole poprzez slug, nie znajduje i wyrzuca blad
o niezgodnosci pola ID z podanym, tzn oczekiwalo inta, dostalo np string

wobec czego, rozwiazania sa 3:
    1. w frontendzie przesylasz w postaci inta, mimo ze z backendu odbierasz w postaci slugu (albo decydujesz ze odbierasz w postaci inta z backendu, albo w postaci calych modeli)
    2. **byc moze mozna by rozwiazac ustawiajac slug jako domyslne pole pk, ale to by trzeba na start projektu**
    3. **wykorzystane poki co** - odbierasz z frontendu te dane w jakiej postaci sobie zyczysz (czyli np tablicy slugow) i recznie odbierasz je, wyciagasz z database obiekty odpowiadajace tym polom i zapisujesz w serializatorze nowo utworzona tablice obiektow

przyklad punktu 3:
PostCreateAPIView
```
def perform_create(self, serializer):
        # print('self.request.data: ', self.request.data)
        # WAZNE: tutaj kwargs jest to czesc argumentow wbudowanych w path
        # prawdziwe dane z requestu sa oczywiscie w requescie
        user_pk = self.kwargs.get("user_pk")
        tags = self.request.data.getlist('tags[]')
        img = self.request.data.get('img')
        print('img: ', img)
        # print('tags: ', tags)
        tagsList = []
        existingTags = Tag.objects.values_list('name', flat=True).distinct()
        # print('existingTags: ', existingTags)
        for tag in tags:
            # print('tag: ', tag)
            if tag not in existingTags:
                # print('not in')
                tagL = Tag.objects.create(
                name = tag,
                description = tag
                )
            else:
                tagL = get_object_or_404(Tag, name=tag)
            tagsList.append(tagL)
        author = get_object_or_404(User, pk=user_pk)
        date_posted = self.request.data.get('date_posted')
        serializer.save(author=author, tags=tagsList, date_posted=date_posted, img=img)
```
gdzie dodatkowo istnieje mozliwosc stworzenia nowego obiektu tak, bazą problemu jest natomiast tagL = get_object_or_404 i dodanie tablicy zawierajacej tagL do serializatora (jesli jest to tablica)


# Nierozwiazywalne kwestie / wymagajace sporych zmian

## Trending posts
Wlasciwie nie jest aktualnie mozliwe zrealizowanie funkcjonalnosci trendujacych postow tak jak bym chcial, bo to wymagaloby sledzenia kiedy zostaly dodanie wyswietlenia i wziecie tylko tych z np ostatnich 30 dni - ale ja nie sledze tego w zaden sposob i troche to bez sensu, musialby lajk byc wlasnym modelem przechowujacym ta informacje

Aktualny sposob czyli wynik dzielenia wysw / dni od postowania faworyzuje posty ktore beda mialy raz bardzo duzo wyswietlen a potem nic kontra posty z malo wyswietlen ale tylko w ostatnim czasie

Aby to wyeliminowac moglbym dodatkowo filtrowac queryset pod tylko posty z ostatnich 30 dni etc, ale poki co ok


# Wazne notatki na przyszosc jak robic rzeczy

## Odnosnie relacji miedzy modelami

Jesli masz ustawione realacje miedzy modelami, w polach typu ForeignKey ustawic mozesz parametr **to_field** wskazujacy po jakim polu ma wiazac relacje. Domylnie bedzie to id, jednak dla wygody mozesz zmienic np na slug, dzieki czemu jesli w serializatorach tez bedziesz poslguiwac sie **SlugRelatedFields**, mozesz uzyskac spojnosc w calym programie.

Mianowicie: nawet jesli dla serializatorow ustawisz related_field = 'slug', to Django pobierajac dane z DB, na przyklad robiac Query, nadal moze chciec sprawdzac warunki po id (bo tak jest domylnie).

Czemu wazne myslec o tym od razu: bo potem zmiana wymagalaby usuniecia wszystkich komentarzy i zrobienia na nowo, gdyz tablica bedzie miala pole foreignKey odpowiadajace ID uzytkownikow, co kompletnie nie bedzie zgadzalo sie z polem slug itp i kompletnie sie to dusi nawet przy probach usuwania

### Nested writable serializer
zeby znalezc uzytkownikow lubiacych post, poniewaz liked_comments jest polem uzytkownika, musialbym wziac uzytkownikow, przefiltrowac po id komentu rownego tego co w endpoincie (kwargs) i zwrocic z tego uzytkownikow a nastepnie dodawac lub usuwac na tym

Ale czy serio nie da sie tego lepiej zrobic? brzmi jak powinno, to zbyt czesta operacja

- no i robie to, bo przesylam cale liked_by i serializator rozumie, ale wymaga to ode mnie wpierw pobrania, zmodyfikowania i odeslania a ja bym chcial bez pobierania, zeby wszystko bylo na backu

------

okej, chyba rozumiem czemu takie problemy, a czemu stworzenie oddzielnego modelu na relacje bylo tak wygodne
- bo standardowym zachowaniem z serializatorami jest tworzenie obiektow, w ktorych jesli chcesz podac jakas wartosc pola (nawet jesli to jest pole stanowiace relacje), po prostu podajesz te wartosci i serializator rozumie to i przypisuje

natomiast opercja którą my chcemy wykonywac, to DOPISYWANIE do pola, czyli dosyc niestandardowa, wymaga nie tylko zapisania, ale odczytania aktualnej i nastepnie dopisania i zapisania tego nowego stanu

w takich sytuacjach, DRF rekomenduje tzw. writable nested serializers, czyli nested serializatory z dodatkowymi metodami create i update w serialiatorze, mogacymi obslugiwac customowe sposoby zapisywania:
https://www.django-rest-framework.org/api-guide/relations/#writable-nested-serializers

## Odnosnie serializatorow i odnoszenia sie do odwrotnych relacji i checi zwracania wszystkiego w jednym view

Czasem sa problemy ze zwracaniem pol ktore wydaje sie powinienes byc w stanie zwracac z pomoca related_name

Przykladowo przy tworzeniu funkcjonalnosci uzytkownikow followujacych innych uzytkownikow
- poniewaz jest to relacja self, wartosciowa opcja moze byc stworzenie oddzielnego modelu tworzacego te relacje poprzez odnoszenie sie dwokrotnie do modelu uzytkownika

https://stackoverflow.com/questions/58794639/how-to-make-follower-following-system-with-django-model


problemem wtedy jednak: jakos by moze z serializatoram sie to zrobilo, ale generalnie mimo related_name, pola z tego nowego modelu zarzadzajacego nie sa defacto czescia modelu uzytkownika, tylko tego nowego modelu.

Tzn. chcac uzyskac informacje o tych relacjach, musisz odniesc sie do tego modelu.

Jesli chcesz wykorzystac te informacje do pobrania np. postów zwiazanych z użytkownikami z modelu followers, musisz je zatem z niego wyciągnąć i potem przekazać jakoś w celu wyciągniecia informacji o postach z modelu i serializatora **związanego z postem**

bo oczywiscie - zeby view z serializatorem zwrocil ci posty, musisz uzyc serializatorow postow, a nie uzytkownikow czy followerow jako ten glowny, one jedynie pomocne

+ sposoby na wyciaganie values z querysetu:
https://stackoverflow.com/questions/48606087/getting-values-of-queryset-in-django

+ wiele malych specyficznych view nie jest problemem, a wrecz lepsze od duzych skomplikowanych ktorych nie rozumiesz a ktore zwracaja "wszystko"