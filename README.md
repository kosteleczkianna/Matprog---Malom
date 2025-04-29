# Malom

Projektünkben a közismert malom játékot valósítottuk meg.

## Játékszabály
A malom játékot két játékos játsza, az egyik a fekete, a másik a fehér bábukkal van. A tábla így néz ki:
kép
Minden játékosnak az a célja, hogy a táblán három, egy egyenesen lévő csomópontot elfoglaljon a saját bábuival. Ha ez megtörténik, a játékos levehet egy bábut az ellenféltől. A játéknak három szakasza van. Az első szakaszban a játékosok felváltva lerakják az összes bábujukat. A második szakaszban a játékosok felváltva lépnek egyet-egyet. Lépni csak szomszédos csomópontra lehet. Amikor valakinek mindössze három bábuja marad, elkezdődik számára a harmadik szakasz. Ekkor a játékos már nemcsak szomszédos csomópontra léphat, hanem bármely üres csomópontra átugorhat. A játéknak akkor van vége, ha valakinek csak kettő bábuja marad. A másik fél nyer.
(A játékszabály részletesebb leírása: http://mek.niif.hu/00000/00056/html/135.htm)

## A program futtatása
A feltöltött "malom.py" fájlban található a kód. 
A játék során a tábla csomópontjaira mindig koordinátákkal tudunk hivatkozni. Ezeket a koordinátákat minden esetben vesszővel elválasztva, zárójel nélkül kell beírni, (például: 1,1). A tábla közepe az origó, a (0,0), ez nem is szerepel a játékban. A játékban szereplő csomópontok koordinátái az origóhoz képest határozhatóak meg. A csomópontok koordinátái rendre: -3,3; 0,3; 3,3; -2,2; 0,2; 2,2; -1,1; 0,1; 1,1; -3,0; -2,0; -1,0; 1,0; 2,0; 3,0; -1,-1; 0,-1; 1,-1; -2,-2; 0,-2; 2,-2; -3,-3; 0,-3; 3,-3.
A játékban mi játszunk a fehér bábukkal, a gép a feketékkel. A gépre a továbbiakban AI-ként fogunk hivatkozni. A program futtatásakor először megjelenik az üres tábla.
Ezt be kell zárnunk ahhoz, hogy az első lépésre felszólítást kapjunk.
kép
Ide azokat a koordinátákat kell beírni, ahova a bábut szeretni tennénk.
kép
A lépésünk ezután meg is jelenik:
kép
A táblát a felugró ablakban be kell zárnunk, majd újra megjelenik magától, már az AI lépésével együtt.
kép
A játék során bármikor ha olyan koordinátát írunk, ami valami miatt nem lehetséges, akkor ezt az üzenetet írja a program:
kép
Ha sikerül malmot raknunk, akkor rá fog kérdezni a program, hogy az AI melyik bábuját szeretnénk eltávolítani. Ekkor ugyanúgy koordinátákkal tudunk válaszolni. Amikor már a lépés fázisban vagyunk, akkor egy lépés során a mozgatandó bábu helyét és az új helyet is meg kell adnunk koordinátákkal. Ugyanígy az ugrálásnál is. 

## Az AI stratégiája





