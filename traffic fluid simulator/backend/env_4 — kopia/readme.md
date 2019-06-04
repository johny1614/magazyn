Akcja w początkowych chwilach to ['wait', 'wait', 'wait']


Od chwili 3 mozna juz podawac typu [3, 3, 1]
Wtedy mamy odpowiednie fazy do poszczegolnych agentow

Pojazdy wjeżdżają do drogi n (wiersz) z drogi m (kolumna)
jak mamy tablice A=
[
  1 0 0
  0 0 0
  0 1 0
] to oznacza, że pojazdy na drodze 1 stoją.
Z kolei do drogi 3 wjedzie pojazd z drogi 2.

Kolumna m musi się sumować do 1 - zawsze z drogi m wyjeżdża 1.

1 0 0   1       1
0 0 0 * 2   =   0
0 1 0   3       2