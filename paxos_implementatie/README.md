# Opdracht 3: Paxos-implementatie
In deze opdracht moeten wij het Paxos algoritme implementeren. Ook voegen we later een uitbreiding[Fase 2] toe waarin we een deel van de vorige opdracht toevoegen aan het algoritme.


## Runnen

### Voorbeeld #1
```
run_simulation("1 3 0 15\n0 PROPOSE 1 42\n0 END")
```
### Voorbeeld #2
```
run_simulation("2 3 0 50\n0 PROPOSE 1 42\n8 FAIL PROPOSER 1\n11 PROPOSE 2 37\n26 RECOVER PROPOSER 1\n0 END")
```    
### Voorbeeld #3
```
run_simulation("1 3 1 10000\n0 PROPOSE 1 nl: g\n100 PROPOSE 1 nl:ga\n200 PROPOSE 1 nl:af\n300 PROPOSE 1 nl:aa\n400 PROPOSE 1 nl:f "
"\n500 PROPOSE 1 en: g\n600 PROPOSE 1 en:gr\n700 PROPOSE 1 en:re\n800 PROPOSE 1 en:ea"
"\n900 PROPOSE 1 en:at\n1000 PROPOSE 1 en:t \n0 END"&#41;)```