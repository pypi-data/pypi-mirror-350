

from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


class Bernoulli:
    def __init__(self, p):
        """
        Inizializza il generatore con una distribuzione di Bernoulli con parametro p.
        
        Args:
            p (float): Un valore tra 0 e 1 che rappresenta la probabilità di estrarre 1.
                       Se p = 0, estrai() restituirà sempre 0.
                       Se p = 1, estrai() restituirà sempre 1.
        """
        if not 0 <= p <= 1:
            raise ValueError("La probabilità p deve essere compresa tra 0 e 1")
        self.p = p
        self.bernoulli = stats.bernoulli(p)
    
    def estrai(self):
        """
        Estrae un valore secondo la distribuzione di Bernoulli con parametro p.
        
        Returns:
            int: 1 con probabilità p, 0 con probabilità (1-p).
        """
        return self.bernoulli.rvs(1)[0]


def show_somma_bernoulli(p, n, num_exp):
    # Generazione dati
    np.random.seed(42)
    dati = np.random.binomial(n, p, size=num_exp)

    # Calcolo dei parametri teorici
    media_teorica = n * p
    std_teorica = np.sqrt(n * p * (1 - p))

    # Definiamo il range dei valori da mostrare (centrato sulla media teorica)
    # Vogliamo mostrare esattamente 40 bin
    num_bins = 40
    half_width = num_bins // 2

    # Troviamo il centro approssimativo (arrotondato all'intero più vicino)
    center = round(media_teorica)

    # Definiamo i valori minimo e massimo per i nostri 40 bin
    min_val = center - half_width
    max_val = center + half_width - 1  # -1 perché il bin finale è [max_val-0.5, max_val+0.5)

    # Assicuriamoci che non escano dal range possibile [0, n]
    min_val = max(0, min_val)
    max_val = min(n, max_val)

    # Creiamo i bin, assicurandoci che ogni bin contenga esattamente un valore intero
    bin_edges = np.arange(min_val - 0.5, max_val + 0.5 + 0.001, 1.0)  # +0.001 per evitare errori di arrotondamento

    # Se il numero di bin risultante è diverso da 40, adattiamo
    if len(bin_edges) - 1 != num_bins:
        # Ricalcoliamo in modo da avere esattamente 40 bin
        vals = np.arange(0, n+1)  # Tutti i possibili valori
        # Troviamo i 40 valori più probabili attorno alla media
        probs = norm.pdf(vals, media_teorica, std_teorica)
        idx = np.argsort(probs)[::-1][:num_bins]  # Indici dei 40 valori più probabili
        idx = np.sort(idx)  # Riordiniamo gli indici
        
        min_val = vals[idx[0]]
        max_val = vals[idx[-1]]
        bin_edges = np.arange(min_val - 0.5, max_val + 0.5 + 0.001, 1.0)

    # Calcolo dell'istogramma
    counts, _ = np.histogram(dati, bins=bin_edges, density=True)

    # Centri dei bin (i valori interi)
    bin_centers = np.arange(min_val, max_val + 0.001, 1.0)

    # Figura
    fig = plt.figure(figsize=(7, 5))

    # Istogramma con i bin corretti
    plt.bar(bin_centers, counts, width=1.0, alpha=0.7, 
            color='skyblue', edgecolor='black', label='Frequenza osservata')

    # Curva teorica su un range più ampio per mostrarla completa
    x = np.linspace(min_val - 10, max_val + 10, 1000)
    y = norm.pdf(x, media_teorica, std_teorica)
    plt.plot(x, y, 'r-', linewidth=2, label='Curva normale')

    # Statistiche
    media_empirica = np.mean(dati)
    std_empirica = np.std(dati)

    # Dettagli
    plt.title(f'Distribuzione binomiale B({n}, {p:.2f})  ', fontsize=14)
    plt.xlabel('Numero di successi', fontsize=12)
    plt.ylabel('Densità di probabilità', fontsize=12)
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # Posizionamento della leggenda nell'angolo in alto a destra, fuori dal grafico
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1.0), fontsize=10)

    # Adattiamo il limite x per mostrare bene la distribuzione
    plt.xlim(min_val - 2, max_val + 2)

    plt.tight_layout()
    #plt.show()
    plt.ioff()
    return fig



prof_italiano = Bernoulli(1/2)
prof_informatica = Bernoulli(1/3)
