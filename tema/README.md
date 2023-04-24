Nume: BREAZU Radu-Mihai          Grupa: 334CB

# Tema 1 - Marketplace în Python

## Organizare
În implementare, nu am definit metode sau clase suplimentare (doar am completat
cele deja existente în schelet cu logica necesară implementării soluției).

### **Descrierea soluției alese**

#### _Soluția pentru producător_
Producătorul își ia un ID, iar apoi, într-o buclă infinită, iterează prin lista
de produse și le livrează pieței (Marketplace). Înainte de a încerca să publice
un produs, el așteaptă timp de `production_time`, iar în cazul în care
publicarea eșuează, așteaptă timp de `republish_wait_time` până a reîncerca
livrarea acestuia.

#### _Soluția pentru consumator_
Consumatorul iterează prin lista sa de coșuri de cumpărături, și, pentru
fiecare coș, își ia un ID, iterează prin lista de acțiuni reprezentată de
`cart` și execută acțiunile întâlnite acolo. Odată ce coșul de cumpărături
are componența dorită, consumatorul își plasează comanda, și astfel produsele
sunt cumpărate.

### **Consideri tema utilă?**
După părerea mea, realizarea Marketplace-ului este o metodă bună de
familiarizare atât cu sintaxa limbajului Python, cât și cu eficientizarea
operațiilor din cod, astfel încât cred că este o temă utilă.

### **Consideri implementarea eficientă?**
Cred că soluția mea este oarecum eficientă, în sensul că am optimizat
operațiile pe care le-am depistat (prin analiza logică a codului) a fi
ineficiente (detalii în secțiunea __Implementare__). Cu toate acestea,
cred că implementarea lasă loc de optimizări suplimentare.

## Implementare

#### **Detalii de implementare**

Soluția mea tratează toate cazurile descrise în enunț, și implementează în plus
posibilitatea de refolosire a ID-urilor producătorilor și ale coșurilor de
cumpărături (detalii mai jos, în secțiunea __Funcționalități extra__). 

**Structuri de date**

Pentru reținerea produselor, împreună cu ID-urile producătorilor, respectiv ale
consumatorilor, am folosit două dicționare: `available_products`, care
stochează mapări între ID-urile producătorilor și cozile asociate de produse,
și `carts`, care folosește pe post de cheie ID-ul coșului de cumpărături, iar
valoarea memorată este o mapare (un dicționar) între ID-urile producătorilor și
produsele din coș ce provin de la acel producător.

**Sincronizare**

Pentru sincronizare, am folosit:
1. în `Consumer`, o variabilă statică de tipul `Lock`, pentru a garanta
faptul că 2 consumatori nu pot printa în același timp date. Acest Lock este
static, deoarece el trebuie să fie același pentru toți consumatorii (altfel
nu s-ar mai realiza sincronizarea).
2. în `Marketplace`, 4 variabile de tipul `Lock`, astfel:
    1. `lock_producer_id` și `lock_consumer_id` pentru a asigura faptul că
    nu se pot înregistra simultan 2 producători, respectiv 2 consumatori
    2. `lock_add_products` pentru a nu permite unui producător să livreze un
    produs în timp ce un consumator renunță la un produs (nu mai dorește să-l
    achiziționeze) (este posibil ca producătorul să nu-și mai poată adăuga
    produsul pe piață)
    3. `lock_remove_products` pentru a nu permite situația în care 2
    consumatori încearcă să adauge simultan la coșul de cumpărături un produs
    (este posibil ca ei să dorească același produs, iar acesta să nu fie
    disponibil în cantitate suficientă). De asemenea, `lock_remove_products`
    permite unui consumator să încerce adăugarea unui produs în coșul său de
    cumpărături în timp ce un producător încearcă livrarea unui produs (în
    acest caz, sincronizarea se face în mod implicit, prin forțarea
    consumatorului sau a producătorului să aștepte, dacă este necesar)

Metoda `place_order` este sincronizată în mod implicit, datorită faptului că
2 consumatori își pot plasa comenzile în același timp, indiferent de ce fac
producătorii, fără a apărea vreo problemă de sincronizare (consumatorii nu
pot avea același ID pentru coșurile de cumpărături, astfel că se încearcă
eliminarea unor intrări -- entries -- corespunzătoare unor chei diferite).

**Alte detalii de implementare**

1. Clasa `Consumer`

    Pentru eficientizare, la iterarea prin `cart`, tipul acțiunii este
    accesat o singură dată, la declanșarea sa (i.e. doar atunci când se schimbă
    acțiunea de efectuat). Totodată, pentru a garanta rezervarea unui produs,
    în cazul acțiunii `add`, se încearcă luarea acestuia până când este găsit
    în stoc.

2. Clasa `Producer`

    Nimic special de spus aici, doar am implementat funcționalitatea descrisă
    în enunț.

3. Clasa `Marketplace`

    Pentru agregarea tuturor produselor ce aparțin aceluiași coș de cumpărături
    (indiferent de producător) am folosit funcționala `reduce()` din modulul
    `functools`. Am făcut acest lucru din 2 motive:
    1. conform [acestei surse](https://learnpython.com/blog/map-filter-reduce-python/)
    `reduce()` este optimizat în Python, deci mai rapid decât o buclă
    `for` obișnuită
    2. am vrut să văd cum pot integra elemente de programare funcțională într-un
    program ce-și propune a implementa un algoritm folositor în viața reală

**Funcționalități extra**
După cum am precizat și mai sus, în plus față de funcționalitățile standard, am
implementat și refolosirea ID-urilor atribuite producătorilor și coșurilor de
cumpărături. Am vrut să fac acest lucru pentru a simula comportamentul unei
aplicații reale, care trebuie să refolosească ID-urile, după un timp determinat
(altfel ar rămâne fără ID-uri disponibile -- trebuie ținut cont de limitele de
reprezentare a numerelor). Astfel, pentru determinarea următorului ID, se
parcurge fluxul infinit al numerelor naturale până când se găsește primul număr
nefolosit în acest scop.

**Dificultăți întâmpinate**
Pe lângă familiarizarea cu sintaxa limbajului, cea mai mare dificultate pe care
am avut-o a fost accea că, în timpul testării, mi-am dat seama că producătorii
trebuie să-și producă bunurile într-o buclă infinită (inițial, plecasem de la
ideea că ei, similar consumatorilor, trebuie să treacă prin lista de produse o
singură dată). De asemenea, tot din aceeași categorie, am avut nevoie de ceva
timp până să înțeleg cum funcționează parametrul `daemon` furnizat prin
`kwargs` thread-urilor Producer.

**Lucruri interesante descoperite**
În timpul realizării temei, am descoperit (căutând pe Internet,
[aici](https://www.programiz.com/python-programming/generator)) că se pot
implementa fluxuri în Python, folosind generatori infiniți. Până la urmă, a
trebuit să abandonez ideea unui generator infinit pentru generarea fluxului
numerelor naturale din motive de eficiență (presupune prea multe apeluri de
funcție, care, și dacă ar fi cache-uite -- cu @cache -- tot ar conduce la
timeout, pe local, în cazul testului 10 -- am testat acest lucru).

## Resurse folosite
Pe lângă link-urile deja menționate, am folosit
[laboratorul 1 de ASC](https://ocw.cs.pub.ro/courses/asc/laboratoare/01)
și tutoriale de pe 
[programiz](https://www.programiz.com/python-programming) pentru a mă acomoda
mai bine cu sintaxa limbajului.
Pentru realizarea logging-ului, am folosit
[documentația oficială](https://docs.python.org/3/howto/logging.html),
împreună cu [RotatingFileHandler](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.RotatingFileHandler).
