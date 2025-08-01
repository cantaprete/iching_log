# I Ching Log

Questo è un test per capire se l'I Ching è completamente casuale o se le letture sono in qualche modo significative.

Il campione di controllo consiste in 10.000 letture dell'I Ching eseguite con [`iching-cli`](https://github.com/cantaprete/iching-cli) con il comando:

```sh
echo "time,hex,type" > rand.csv

for i in {1..10000};
do
    iching -w -c >> rand.csv ;
done
```

Il risultato è (prevedibilmente) casuale:

![img](./docs/rand_rect.png)
![img](./docs/rand_radar.png)

Questi, invece, sono i medesimi grafici utilizzando letture significative, ossia precedute dal desiderio di interrogare l'I Ching su una specifica domanda:

![img](./docs/sig_rect.png)
![img](./docs/sig_radar.png)

Al momento i dati sono troppo pochi (89 contro 10.000) per trarre qualsiasi conclusione sensata.

Ciò che mi aspetto è uno di questi tre casi:

1. Indipendentemente dal numero di letture, i grafici non mostrano un andamento grossomodo casuale ma mostrano invece degli sbilanciamenti verso alcuni esagrammi, sia questo in generale o per un tipo specifico.
2. Con l'approssimarsi di un numero sufficiente di letture, l'andamento è nel complesso grossomodo casuale. Nonostante ciò, se analizzato in blocchi determinati da periodi di tempo variabili ma significativi mostra sbilanciamenti verso alcuni esagrammi, sia questo in generale o per un tipo specifico.  Questo si spiegherebbe considerando che nel lungo periodo le questioni sottoposte all'I Ching variano, e con ciò la varietà delle risposte; ma presi in periodi significativi (ossia in periodi nei quali la maggior parte delle domande verteva sui medesimi quesiti), mostrano una preponderanza di certe risposte rispetto alle altre.
3. Grossomodo casuale sia nella totalità sia in sottoinsiemi temporali significativi.