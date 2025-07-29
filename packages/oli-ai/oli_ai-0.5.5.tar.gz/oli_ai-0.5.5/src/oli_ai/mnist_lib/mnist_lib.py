from keras.datasets import mnist
from matplotlib import pyplot as plt
import numpy as np
from numpy import dot
from numpy.linalg import norm
import networkx as nx

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



def show_nn_graph(input_size=2, hidden_size=0, output_size=1):
    """Versione ultra-compatta con distanze minime"""
    G = nx.DiGraph()
    pos = {}
    
    # SPACING RIDOTTO AL MINIMO
    vertical_spacing = 0.3  # Era 1.0, ora 0.3
    
    # Input layer
    for i in range(input_size):
        node_name = f'I{i}'
        G.add_node(node_name, layer='input')
        pos[node_name] = (0, (i - (input_size-1)/2) * vertical_spacing)
    
    # Hidden layer
    if hidden_size > 0:
        for i in range(hidden_size):
            node_name = f'H{i}'
            G.add_node(node_name, layer='hidden')
            pos[node_name] = (1, (i - (hidden_size-1)/2) * vertical_spacing)
            
            for j in range(input_size):
                G.add_edge(f'I{j}', node_name)
    
    # Output layer
    output_x = 1 if hidden_size == 0 else 2
    for i in range(output_size):
        node_name = f'O{i}'
        G.add_node(node_name, layer='output')
        pos[node_name] = (output_x, (i - (output_size-1)/2) * vertical_spacing)
        
        if hidden_size > 0:
            for j in range(hidden_size):
                G.add_edge(f'H{j}', node_name)
        else:
            for j in range(input_size):
                G.add_edge(f'I{j}', node_name)
    
    # Plot compattissimo
    plt.figure(figsize=(8, 4))
    
    colors = {'input': '#3498db', 'hidden': '#2ecc71', 'output': '#e74c3c'}
    node_colors = [colors[G.nodes[node]['layer']] for node in G.nodes()]
    
    nx.draw(G, pos,
            with_labels=True,
            node_color=node_colors,
            node_size=600,       # Neuroni più piccoli
            font_size=10,
            font_weight='bold',
            font_color='white',
            arrows=True,
            arrowsize=15,
            edge_color='#95a5a6',
            width=1.5,
            alpha=0.8)
    
    arch = f"{input_size}→{hidden_size}→{output_size}" if hidden_size > 0 else f"{input_size}→{output_size}"
    plt.title(f'NN: {arch}', fontsize=14, pad=15)
    plt.axis('off')
    plt.tight_layout()
    plt.show()


