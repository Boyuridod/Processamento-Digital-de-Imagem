# Atividade Prática de Extração de Características
# Estudante: Yuri David Silva Duarte
# Data: 06/07/2025

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
from skimage.feature import graycomatrix, graycoprops
from skimage.util import img_as_ubyte
from skimage.color import rgb2gray

# - Escolha uma métricas de distância entre histogramas e apresente o resultado

def getNomeImagem(caminho):
    caminho = caminho.split("/")

    caminho = caminho[-1].split(".")

    return caminho[0]

def getHistograma(img_pil, bins=256):
    img_np = np.array(img_pil.convert("RGB"))
    hist = {}
    for i, canal in enumerate(['R', 'G', 'B']):
        h, _ = np.histogram(img_np[:, :, i], bins=bins, range=(0, 256))
        hist[canal] = h / h.sum()
    return hist

def comparaHistogramas(img1, img2):
    hist1 = getHistograma(img1)
    hist2 = getHistograma(img2)

    dist_total = 0
    print("*** DISTÂNCIA ENTRE HISTOGRAMAS ***")
    for canal in ['R', 'G', 'B']:
        dist = distance.euclidean(hist1[canal], hist2[canal])
        print(f"Canal {canal}: distância Euclidiana = {dist:.4f}")
        dist_total += dist
    print(f"Distância total (soma dos canais): {dist_total:.4f}")

    plt.figure(figsize=(12, 4))
    for i, canal in enumerate(['R', 'G', 'B']):
        plt.subplot(1, 3, i+1)
        plt.plot(hist1[canal], label='Imagem 1', color=canal.lower())
        plt.plot(hist2[canal], '--', label='Imagem 2', color=canal.lower())
        plt.title(f'Histograma - Canal {canal}')
        plt.legend()
    plt.tight_layout()
    plt.show()

# - Apresente as 15 características dos descritores de Haralick

def clusterShadeClusterProminence(coMatriz):
    glcm_sum = np.sum(coMatriz, axis=3).astype(np.float64)
    glcm_norm = glcm_sum / glcm_sum.sum()

    levels = glcm_norm.shape[0]
    i_vals = np.arange(levels).reshape((-1, 1))
    j_vals = np.arange(levels).reshape((1, -1))

    mu_i = np.sum(i_vals * np.sum(glcm_norm, axis=1))
    mu_j = np.sum(j_vals * np.sum(glcm_norm, axis=0))

    diff = (i_vals + j_vals - mu_i - mu_j)

    cluster_shade = np.sum((diff ** 3) * glcm_norm)
    cluster_prominence = np.sum((diff ** 4) * glcm_norm)

    return cluster_shade, cluster_prominence

def haralick(imagem):
    imagemCinza = imagem.convert("L")
    vetorImagem = img_as_ubyte(np.array(imagemCinza))
    coMatriz = graycomatrix(vetorImagem, distances=[1], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4],
                        symmetric=True, normed=True)
    cluster = clusterShadeClusterProminence(coMatriz)

    descritores = {
        "1. ASM (Segundo Momento Angular)": graycoprops(coMatriz, 'ASM').mean(),
        "2. Energia": graycoprops(coMatriz, 'energy').mean(),
        "3. Entropia": -np.sum(coMatriz * np.log2(coMatriz + 1e-10)),
        "4. Contraste": graycoprops(coMatriz, 'contrast').mean(),
        "5. Dissimilaridade": graycoprops(coMatriz, 'dissimilarity').mean(),
        "6. Homogeneidade": graycoprops(coMatriz, 'homogeneity').mean(),
        "7. Correlação 1": graycoprops(coMatriz, 'correlation').mean(),
        "8. Correlação 2": np.corrcoef(vetorImagem.flatten()[:-1], vetorImagem.flatten()[1:])[0, 1],
        "9. Cluster Shade": cluster[0],
        "10. Cluster Prominence": cluster[1],
        "11. Variância": np.var(vetorImagem),
        "12. Desvio Padrão (J)": np.std(vetorImagem),
        "13. Média nas linhas (I)": np.mean(np.mean(coMatriz, axis=1)),
        "14. Média nas colunas (J)": np.mean(np.mean(coMatriz, axis=0)),
        "15. Média geral (G)": np.mean(coMatriz)
    }

    print("\n*** DESCRITORES DE HARALICK ***")
    for nome, valor in descritores.items():
        print(f"{nome}: {valor:.4f}")

caminho1 = "./Images/RaioxA.jpg"
caminho2 = "./Images/RaioxB.jpg"

imagem1 = Image.open(caminho1)
imagem2 = Image.open(caminho2)

plt.figure(figsize=(8, 4))
plt.subplot(1, 2, 1)
plt.imshow(imagem1)
plt.title("Imagem 1: " + getNomeImagem(caminho1))
plt.axis("off")
plt.subplot(1, 2, 2)
plt.imshow(imagem2)
plt.title("Imagem 2: " + getNomeImagem(caminho2))
plt.axis("off")
plt.tight_layout()
plt.show()

comparaHistogramas(imagem1, imagem2)
haralick(imagem1)