# Prekode for Oblig3 oppgave 1

Dette er et skall for oppgave 1 i Oblig3 i IN2010 høsten 2020. Det er _ikke_
påkrevet å benytte seg av denne koden.

Den består av:
- `Oblig3.java` som inneholder `main` og kjører sorteringsalgoritmene dine på
  en gitt inputfil.
- `Sorter.java` som er en (abstrakt) klasse, som inneholder hjelpemetoder for å
  telle sammenligninger og bytter. I tillegg inneholder den hjelpemetoder for å
  kunne ta tiden på sorteringen, og returnere resultatene i form av strenger.
  Skal du bruke denne prekoden bør alle sorteringsalgoritmene dine
  implementeres som en egen klasse som arver fra `Sorter`.
- `Oblig3Runner.java` som står for kjøringen av eksperimenter og skriving til
  fil. Merk at den inneholder disse feltene:
  ```java
  // Put the sorting algorithms under test for part 1 here
  static final Sorter[] ALGS1 = { new Insertion(), new Quick() };
  // Put the sorting algorithms under test for part 2 here
  static final Sorter[] ALGS2 = { new Insertion(), new Quick() };
  // Time limit for a single sorting in milliseconds
  static final long TIME_LIMIT_MS = 100;
  // How much n grows each iteration
  static final int INCREMENT = 1;
  ```
  som du kan justere for å få resultatene du ønsker
- `Insertion.java` som inneholder et skall for insertion sort, og arver fra
  `Sorter`.
- `Quick.java` som inneholder et skall for quicksort, og arver fra `Sorter`.

I tillegg finner du en rekke inputfiler i mappen `inputs`. Noen filer er store,
og vi forventer ikke at algoritmene dine er raske nok til å håndtere alle.

Ved å kjøre for eksempel:
```sh
$ javac *.java && java Oblig3 inputs/random_100
```

vil du se følgende utskrift:
```
  n, insertion_cmp, insertion_swaps, insertion_time, quick_cmp, quick_swaps, quick_time
```

og det vil ligge tre nye filer i `inputs`-mappen:
- `random_100_insertion.out`
- `random_100_quick.out`
- `random_100_results.csv`

Merk at resultatene ikke vil være rimelige, fordi sorteringen ikke er
implementert.

Grunnen til den ene finurlige linjen med utskrift er at programmet vil én gang
i sekundet skrive ut en linje som skrives til `csv`-filen. Dette er slik at du
kan se om programmet gjør noen fremgang når du utfører eksperimenter.

For å gjøre det enklere å utføre eksperimenter har vi lagt inn en
tidsbegrensning på hvor lenge en sorteringsalgoritme kan kjøre for
deloppgave 2. Den kan justeres ved å endre på `TIME_LIMIT_MS` i
`Oblig3Runner.java`. Den er satt til 100 millisekunder, og så en algoritme
overstiger dette, så vil den ikke kjøres for høyere `n` (som vil si at du får
tomme felter i den resulterende tabellen).
