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

