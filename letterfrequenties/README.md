## Analyse letterfrequenties

Voor het maken van deze opdracht was aanbevolen om Hadoop te gebruiken voor de map-reduce functionaliteit. Wij hebben veel moeite gehad om Hadoop werkend te krijgen, daarom hadden we besloten om een eigen Hadoop-geïnspireerde programma te maken om in dezelfde stijl map reduce parallel uit te voeren. 

Onze mini Hadoop oftewel "[Hadopy](https://github.com/MariaDukmak/Hadopy)", is via pip te installeren.


## Algoritme trainen 
Voor het "trainen" van ons algoritme hebben we gebruik gemaakt van twee verschillende teksten dat kan je [hier](https://github.com/MariaDukmak/DIP/tree/main/letterfrequenties/tekst) vinden. 

Het algoritme scoort het volgende op deze teksten:

*alice.txt*
```bash 
$ cat tekst/alice.txt |  hadopy --m  "python mapper.py" --r  "python reducer.py" |  python matrix_saver.py nederlands.txt

```

*theoldway.txt*
```bash 
$ cat tekst/theoldway.txt |  hadopy --m  "python mapper.py" --r  "python reducer.py" |  python matrix_saver.py engels.txt

```
__hier een screenshot van de resultaten plakken__


Zoals we kunnen zien, doet het algoritme het best goed. Nu tijd om te gaan testen hoe het bij de test tekst doet. 



## Algoritme testen 
Voor het testen van het algoritme maken we gebruik van [deze](https://github.com/MariaDukmak/DIP/blob/main/letterfrequenties/tekst/sentences.nl-en.txt) tekst. 




__hier een screenshot van de resultaten plakken__


Zoals we kunnen zien, scoort ons algoritme __ van de __ voor Nederlandse zinnen en __ van de __ voor Engelse zinnen. 
Deze resultaten zijn goedgekeurd! 

## Het programma runnen

Om dit programma te runnen zou je de volgende command eerst moeten runnen:

```$ pip install -r requirements.txt```

__Met hadopy__

```bash 
$ cat tekst/sentences.nl-en.txt | hadopy --m  "python mapper.py" --r  "python reducer.py" |  python classifier.py
```

__Zonder hadopy__

```bash 
$ cat tekst/sentences.nl-en.txt | python mapper.py | sort | python reducer.py |  python classifier.py
```