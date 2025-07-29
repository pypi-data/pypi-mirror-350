from keras.datasets import mnist
from matplotlib import pyplot as plt
import numpy as np
from numpy import dot
from numpy.linalg import norm
import networkx as nx
import plotly.graph_objects as go
import networkx as nx
import matplotlib.pyplot as plt


def plot_img(image):
    image = image.reshape((28, 28))
    plt.imshow(image, cmap='gray')
    plt.show()


def plot_imgs_labels(imgs, labels, rows=2, cols=5):
    figure = plt.figure(figsize=(10, 3))
    # plotting images from the training set
    for i in range(0, rows*cols):
        plt.subplot(rows, cols, i+1)
        plt.subplots_adjust(hspace=1, wspace=1)
        plt.title(f"Label: {labels[i]}")
        img = imgs[i].reshape((28, 28))
        plt.imshow(img, cmap='gray')       
        # Rimuovere le indicazioni numeriche dagli assi
        plt.xticks([])
        plt.yticks([])

def plot_imgs(imgs, labels, rows=2, cols=5):
    figure = plt.figure(figsize=(10, 3))
    # plotting images from the training set
    for i in range(0, rows*cols):
        plt.subplot(rows, cols, i+1)
        plt.subplots_adjust(hspace=1, wspace=1)
        #plt.title(f"Label: {labels[i]}")
        img = imgs[i].reshape((28, 28))
        plt.imshow(img, cmap='gray')
        
        # Rimuovere le indicazioni numeriche dagli assi
        plt.xticks([])
        plt.yticks([])



def predict(model,image):
  image = image.reshape(1, 28, 28)  # Aggiungi dimensione batch
  prediction = model.predict(image)
  #print(f"Raw prediction: {prediction}")  # [0.01, 0.02, 0.95, 0.01, ...]
  # Classe predetta
  predicted_class = np.argmax(prediction)
  return predicted_class


# Funzione per visualizzare i pesi
def visualize_weights(weights, title):
   normalized_weights = (weights - np.min(weights)) / (np.max(weights) - np.min(weights))
   
   fig, axes = plt.subplots(1, 10, figsize=(15, 2))  # Altezza dimezzata
   
   for i in range(10):
       axes[i].imshow(normalized_weights[:, i].reshape(28, 28), cmap='gray')
       axes[i].axis('off')
       axes[i].set_title(f'{i}', fontsize=6)  # Font più piccolo
   
   fig.suptitle(title, fontsize=10, y=0.95)  # Titolo più piccolo
   plt.subplots_adjust(top=0.65, bottom=0.02, hspace=0, wspace=0.05)  # Margini ultra-mini
   plt.show()




def show_nn_graph(layers, max_neurons=10):
    """
    Visualizza una rete neurale con architettura arbitraria
    
    Args:
        layers: lista con il numero di neuroni per ogni layer
                Es: [2,1] = 2 input, 1 output
                    [2,2,1] = 2 input, 2 hidden, 1 output  
                    [2,2,4,5,4] = 2 input, 2 hidden, 4 hidden, 5 hidden, 4 output
        max_neurons: numero massimo di neuroni da mostrare per layer (default=10)
                    Se un layer ha più neuroni, mostra i primi, poi "...", poi l'ultimo
    """
    if len(layers) < 2:
        raise ValueError("Servono almeno 2 layer (input e output)")
    
    G = nx.DiGraph()
    pos = {}
    
    # SPACING DINAMICO in base al numero massimo di neuroni visualizzati
    max_visual_neurons = min(max(layers), max_neurons)
    vertical_spacing = max(0.2, min(0.5, 3.0 / max_visual_neurons))  # Adatta spacing
    horizontal_spacing = 1.5
    
    # Crea tutti i nodi e le posizioni
    all_nodes = []
    all_actual_nodes = []  # Nodi reali (senza "...")
    node_labels = {}  # Mappa per etichette pulite
    
    for layer_idx, layer_size in enumerate(layers):
        layer_nodes = []
        layer_actual_nodes = []
        
        # Determina il tipo di layer
        if layer_idx == 0:
            layer_type = 'input'
            prefix = 'I'
        elif layer_idx == len(layers) - 1:
            layer_type = 'output'
            prefix = 'O'
        else:
            layer_type = 'hidden'
            prefix = f'H{layer_idx}'
        
        # Logica SICURA - prima calcolo esatto dei nodi poi creazione
        visual_nodes = []  # Lista di (nome_display, tipo, posizione_y)
        actual_nodes_only = []  # Solo neuroni reali per connessioni
        
        if layer_size <= max_neurons:
            # Caso semplice: tutti i neuroni (partendo da 1, dall'alto al basso)
            for i in range(layer_size):
                display_name = f'{i+1}'  # SOLO NUMERO per display
                y_pos = ((layer_size-1)/2 - i) * vertical_spacing
                visual_nodes.append((display_name, layer_type, y_pos))
                actual_nodes_only.append(display_name)
        else:
            # Caso complesso: primi + ... + ultimo (dall'alto al basso)
            total_slots = max_neurons
            y_positions_list = [((total_slots-1)/2 - i) * vertical_spacing for i in range(total_slots)]
            
            slot = 0
            # Primi neuroni (max_neurons - 2, partendo da 1)
            for i in range(max_neurons - 2):
                display_name = f'{i+1}'  # SOLO NUMERO: 1,2,3...
                visual_nodes.append((display_name, layer_type, y_positions_list[slot]))
                actual_nodes_only.append(display_name)
                slot += 1
            
            # "..." (PENULTIMO slot)
            visual_nodes.append(('...', 'dots', y_positions_list[slot]))
            slot += 1
            
            # Ultimo neurone (ULTIMO slot)
            last_display = f'{layer_size}'
            visual_nodes.append((last_display, layer_type, y_positions_list[slot]))
            actual_nodes_only.append(last_display)
        
        # Crea tutti i nodi con nomi unici per NetworkX
        x = layer_idx * horizontal_spacing
        
        for display_name, node_type, y_pos in visual_nodes:
            # Nome unico per NetworkX
            unique_name = f'{prefix}_{display_name}'
            G.add_node(unique_name, layer=node_type)
            pos[unique_name] = (x, y_pos)
            layer_nodes.append(unique_name)
            
            # Mappa per etichette pulite
            node_labels[unique_name] = display_name
        
        # Solo neuroni reali per connessioni
        layer_actual_nodes = [f'{prefix}_{name}' for name in actual_nodes_only]
        
        all_nodes.append(layer_nodes)
        all_actual_nodes.append(layer_actual_nodes)
    
    # Crea le connessioni tra layer adiacenti
    for layer_idx in range(len(layers) - 1):
        current_layer = all_actual_nodes[layer_idx]  # Solo nodi reali
        next_layer = all_actual_nodes[layer_idx + 1]  # Solo nodi reali
        
        # Connetti ogni neurone del layer corrente con ogni neurone del layer successivo
        for current_node in current_layer:
            for next_node in next_layer:
                G.add_edge(current_node, next_node)
    
    # Calcola dimensioni figura in base al numero di layer E neuroni visualizzati
    fig_width = max(6, len(layers) * 1.8)
    fig_height = max(3, max_visual_neurons * 0.8 + 1)
    
    plt.figure(figsize=(fig_width, fig_height))
    
    # Colori per i diversi tipi di layer
    colors = {'input': '#3498db', 'hidden': '#2ecc71', 'output': '#e74c3c', 'dots': '#95a5a6'}
    node_colors = [colors[G.nodes[node]['layer']] for node in G.nodes()]
    
    # Dimensioni dei nodi (più piccoli per i "...")
    node_sizes = []
    for node in G.nodes():
        if G.nodes[node]['layer'] == 'dots':
            node_sizes.append(300)  # Più piccoli per "..."
        else:
            node_sizes.append(600)  # Dimensione normale
    
    # Disegna la rete con etichette pulite
    # Crea lista ordinata di nodi per garantire ordine nel drawing
    ordered_nodes = []
    for layer_nodes in all_nodes:
        ordered_nodes.extend(layer_nodes)
    
    nx.draw(G, pos,
            nodelist=ordered_nodes,  # FORZA l'ordine dei nodi
            labels=node_labels,      # Etichette solo numeriche
            with_labels=True,
            node_color=node_colors,
            node_size=node_sizes,
            font_size=10,
            font_weight='bold',
            font_color='white',
            arrows=True,
            arrowsize=15,
            edge_color='#95a5a6',
            width=1.5,
            alpha=0.8)
    
    # Titolo con architettura
    arch_str = '→'.join(map(str, layers))
    plt.title(f'Neural Network Architecture: {arch_str}', fontsize=14, pad=20)
    
    # Aggiungi etichette per i layer
    layer_labels = ['Input']
    if len(layers) > 2:
        for i in range(1, len(layers) - 1):
            layer_labels.append(f'Hidden {i}')
    layer_labels.append('Output')
    
    # Posiziona le etichette dei layer
    for i, label in enumerate(layer_labels):
        plt.text(i * horizontal_spacing, 
                max([pos[node][1] for node in all_nodes[i]]) + 0.5,
                label, 
                ha='center', 
                va='bottom',
                fontsize=12,
                fontweight='bold')
    
    plt.axis('off')
    plt.tight_layout()
    plt.show()





def show_xor_3d(nn, inputs, outputs):
  # Ottieni le attivazioni dello strato nascosto per ogni punto di input
  hidden_activations = np.array([nn.get_hidden_activations(x) for x in inputs])

  # Approssima i valori molto vicini a zero a 0
  epsilon = 1e-10
  hidden_activations[np.abs(hidden_activations) < epsilon] = 0.0

  print("\nHidden Layer Activations:")
  for i, (inp, act) in enumerate(zip(inputs, hidden_activations)):
      print(f"Input: {inp}, Hidden Activations: {act}")

  # Analizziamo quale neurone meglio separa i punti XOR secondo il criterio richiesto
  # Vogliamo che i punti (0,1) e (1,0) abbiano z circa 1, mentre (0,0) e (1,1) abbiano z circa 0
  best_neuron_idx = None
  best_score = float('inf')

  for i in range(hidden_activations.shape[1]):
      # Calcola lo score per questo neurone
      score = abs(hidden_activations[1, i] - 1) + abs(hidden_activations[2, i] - 1) + abs(hidden_activations[0, i]) + abs(hidden_activations[3, i])

      if score < best_score:
          best_score = score
          best_neuron_idx = i

  print(f"\nIl neurone che meglio separa i punti XOR è il neurone {best_neuron_idx+1}")

  # Crea i dati 3D usando l'attivazione del miglior neurone nascosto come terza dimensione
  data_3d = np.column_stack((inputs, hidden_activations[:, best_neuron_idx]))

  # Visualizzazione interattiva con Plotly
  fig = go.Figure()

  # Aggiungi i punti XOR
  fig.add_trace(go.Scatter3d(
      x=data_3d[:, 0],  # Input 1 - Asse X
      y=data_3d[:, 1],  # Input 2 - Asse Y
      z=data_3d[:, 2],  # Attivazione Neurone - Asse Z
      mode='markers+text',
      marker=dict(
        size=14,
        color=outputs.ravel(),
        colorscale='Viridis',
        opacity=1.0,
        symbol='circle',
        line=dict(
            color='black',
            width=1
        )
      ),
      text=[f"({x[0]},{x[1]})" for x in inputs],
      textposition="top center",
      textfont=dict(
        size=12,
        color='black'
      ),
      hovertext=[f"Input: ({x[0]}, {x[1]})<br>Output XOR: {y[0]}<br>Attivazione Neurone: {z:.4f}"
          for x, y, z in zip(inputs, outputs, data_3d[:, 2])],
      hoverinfo="text",
      name='XOR Points'
  ))

  # Imposta il layout con più dettagli
  fig.update_layout( 
      title=dict(
          text='Visualizzazione 3D del Problema XOR con Attivazione del Neurone Nascosto',
          font=dict(size=20)
      ),
      scene=dict(
        xaxis=dict(
            title='Input 1 (X)',
            range=[-0.1, 1.2],
            tickvals=[0, 1],
            showbackground=True,
            backgroundcolor='rgb(255, 230, 230)',  # Sfondo rosato per l'asse X
            gridcolor='red',
        ),
        yaxis=dict(
            title='Input 2 (Y)',
            range=[-0.1, 1.2],
            tickvals=[0, 1],
            showbackground=True,
            backgroundcolor='rgb(230, 255, 230)',  # Sfondo verdino per l'asse Y
            gridcolor='green',
        ),
        zaxis=dict(
            title='Attivazione Neurone (Z)',
            range=[-0.1, 1.2],
            tickvals=[0, 0.5, 1],
            showbackground=True,
            backgroundcolor='rgb(230, 230, 255)',  # Sfondo bluastro per l'asse Z
            gridcolor='blue',
        ),
        camera=dict(
            eye=dict(x=1.8, y=1.8, z=1.2)
        )
      ),
      height=700,
      width=900,
      margin=dict(l=0, r=0, b=0, t=40, pad=100),  # Aumentato il margine inferiore
  )

  # Mostra la figura con più spazio sopra e sotto
  fig.show()
  return data_3d



def show_xor_error(errors_history):
  # Visualizzazione dell'andamento dell'errore durante il training
  fig_error = go.Figure()
  fig_error.add_trace(go.Scatter(
    y=errors_history,
    mode='lines',
    name='MSE',
    line=dict(width=2, color='royalblue')
  ))

  fig_error.update_layout(
    title='Andamento dell\'errore durante il training',
    xaxis_title='Epoca',
    yaxis_title='MSE (Mean Squared Error)',
    yaxis_type='log',
    height=400,
    width=800,
    margin=dict(t=100, b=100)  # Aumentato il margine superiore e inferiore
  )
  fig_error.show()
