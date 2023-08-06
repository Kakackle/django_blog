## TODO: Funkcja followersow
Tzn mozliwosc by uzytkownicy wchodzac na profil innego uzytkownika mogli kliknac "follow", co dodawaloby ich do listy przypisanej do uzytkownika dodajacego, dzieki ktorej pozniej mozna by na stronie blogu dac checkbox typu "only display posts by users you follow" + mozliwosc wyswietlania ich na liscie uzytkownikow ktorych followujesz itd

Czego by to wymagalo?

1. Dla kazdego uzytkownika pole ManyToMany ale self referential? bo uzytkownicy followuja uzytkownikow? W sumie troche jak komenty

2. Odbieranie w patchu listy uzytkownikow followowanych po kliknieciu "follow" w vue czy cos

3. Filtracja tylko po postach nalezacych do followanych uzytkownikow - czyli trzeba by w query przeslac liste? albo tylko haslo typu ?followed_by=admin i wtedy podczas zbierania querysetu:
    - wez uzytkownika -> wez jego liste followowanych -> wez queryset gdzie autor postu in [ lista ] -> zwroc ofc


## TODO: Wiecej zliczan
Tzn:
- ile jest postow z danym tagiem
- postow uzytkownika
- komentow na poscie,
- ile uzytkownik ma komentow,
- ile ma lajkow na postach,
- ile ma lajkow na komentach,

Jak ogolnie dokonywac zliczen? Bo aktualnie tez robione jest lajkowaie w Vue - lajki przesylane sa w poscie, w Vue przy wykryciu eventu zwiekszane (tzn. dodawany uzytkownik do listy lajkujacych), ale tez zwiekszane  i przesylany patch - Ale jak to zrobic w Django?
### funkcjonalnosc lajkowania
1. Mozna by zrobic np endpoint - np. posts/costam/like , ktory jednak musialby wymagac przeslania w requescie uzytkownika, ktorego dodamy do listy lajkow, ale to nie powinien byc problem, po prostu aktualnie zalogowany, na tej podstawie tez by sie aktualizowalo liczbe (length)

### zwykle zliczenia
Musialyby byc aktualizowane wraz z przychodzacymi requestami, tzn. jesli chodzi o liczbe postow uzytkownika / z tagiem / komentow na poscie - przy POST requestach tworzacych je trzeba by brac odpowiednie rekordy z DB (uzytkownika, tag) i je aktualizowac

### zliczanie ile uzytkownik DOSTAL lajkow
Musialoby to byc wywolywane przy aktualizacji lajkow postu - przy okazji brany bylby uzytkownik i do dodawane byloby do jego liczby lajkow posiadanych


### Co z usuwaniem lajkow??
Kilka kwestii:
1. Wyswietlanie na froncie - lista uzytkownikow przez ktore jest polajkowane musialaby byc przesylana z postem (albo na nowym endpoincie typu /likes) i na froncie sprawdzane czy jest w tej liscie
[ albo endpoint odbierajacy zalogowanego uzytkownika i sam sprawdzajacy i zwracajacy bool? maybe]

2. Aktualizacja na backendzie:
    1. Jesli byblby endpoint z cala lista, to mozna by na froncie usuwac z listy i przesylac patch - albo na sam post albo na tylko ten endpoint
    2. Jesli mamy endpoint typu /like odbierajacy uzytkownika, to czy nie moglby on przy wywolywaniu sprawdzac czy uzytkownik jest na liscie i jesli jest to usuwac, jak nie ma to dodawac? Moze

+ TODO: modyfikacja wyswietlen? Bo aktualnie wyswietlenia robione sa tak, z kiedy ktokolwiek wchodzi na strone postu, do backendu wysylany jest patch aktualizujacy wyswietlenia, co wymaga, by najpierw je odebral, uaktualnil i przeslal spowrotem PATCH

Jak by mozna to rozwiazac lepiej? 2 pomysly:
1. endpoint na poscie ktory sam to aktualizuje (nie trzeba nic pobierac i przesylac), aktualizowany przy "dotknieciu", get
2. praktycznie to co wyzej, tylko zrealizowane na samym endpoincie/view postu - powinno byc to mozliwe

jak? Moze przypisujac jakos do get requestu - i w wypadku takiego aktualizacja na bazie modelu/serializatora jakis .save()


## TODO: Daty i filtracje
Juz to gdzies pisalem, ale

Na froncie wyswietlanie jakies typu <1 week, <1 month itd, a na tle wysylaloby liczby typu 7, 31 itd odpowiadajce ilosci dni

i potem na endpoincie filtrujacym odbierane i queryset filtrowany funkcja obliczajaca roznice miedzy dzisiaj a date_posted i jesli mniejsza od przeslanej liczby to nalezy do querysetu i wlasciwie tyle


    