Nume: Epure Rares Stefan 

Grupă: 336CC

# Tema 1 

Organizare
-

Solutia abordata se bazeaza pe clasele consumer, marketplace si producer.
* Producatorul produce obiecte intr-o anumita cantitate pana cand nu mai exista loc in coada sa 
din marketplace si reincearca operatiunea dupa un timp t (in coada se adauga cate un produs).
* Consumerul ia cate un cos de cumparaturi (adica un 'cart' in implementare) pentru fiecare lista
de produse si consuma elemente din cozile producatorilor conform listei de produse.
* Marketplace-ul inglobeaza atat functionalitati ale consumatorului, cat si ale producatorului.
Tot in aceasta clasa sunt realizate sincronizari la nivelul fiecarei operatii. Marketplace-ul
este un mediator intre aceste 2 entitati.

Consider ca tema a fost utila, deoarece am inteles mai bine notiunile de sincronizare si 
modul lor de utilizare in python.
Consider ca implementarea se putea realiza mai eficient, prin implementarea optima
a cozilor in care stocheaza producatorii produsele. Aceasta implementare mai optima
s-ar baza pe folosirea unor hashmap-uri.

Implementare
-

Tema implementeaza intreaga functionalitate din enunt.

Producatorul este un proces daemon care produce pana cand metoda main se termina. Pentru a indica sfarsitul metodei main si foloseste un flag "daemon". Producatorul va genera produse unu cate unu, iar in cazul in care nu mai este loc in coada sa din marketplace se va folosi va astepta un timp t pana va reincerca sa il publice in coada sa din marketplace. Producatorul are o lista de produse pe care poate sa le genereze si le produce in ordinea din lista respectiva, iar in momentul in care produce toate elementele din lista va reitera prin lista si va produce elementele in ordine specificata in lista.

Consumator itereaza prin listele de cumparaturi, iar listele au cosuri de cumparaturi diferite. Consumatorul poate sa consume produse pe baza unei singure liste la un moment dat.

In marketplace se realizeaza sincronizarea dintre producator si consumator. In primul rand se va folosi cate un lock atat pentru generarea id-urilor producatorilor cat si pentru generarea id-urilor cosurilor de cumparaturi, deoarece la un moment dat pot doi sau mai multi producatori pot genera un id. La fel se intampla si in cazul consumatorilor cu id-urile cosurilor de cumparaturi. Se mai foloseste o lista de lock-uri asociate cu cozile producatorilor, deoarece atat producatorii cat si consumatorii le pot modifica in acelasi timp.
Lockuri pentru generarea id-urilor producatorilor si id-urilor cosurilor de cumparaturi sunt stocate intr-o lista.

Pentru a tine o evidenta asupra cosurilor de cumparaturi, acestea sunt stocate intr-o lista.

Resurse utilizate
-
Pentru implementarea temei am consultat atat laboratoarele de asc cat si paginile cu descrierile
oficiale ale obiectelor de sincronizare din python.

Git
-
https://github.com/EpureRares/ASC-Producer-Consumer.git