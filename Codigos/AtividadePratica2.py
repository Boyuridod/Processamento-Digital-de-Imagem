# Atividade Prática
# Estudante: Yuri David Silva Duarte
# Data: 05/06/2025

# **Histograma e Limiarização**
# Insira e apresente uma imagem colorida da sua escolha.

from PIL import Image
import matplotlib.pyplot as plt

def trataCaminho(caminhoDaImagem):
    
    caminho = ""
    
    for i in range(len(caminhoDaImagem)):
        if(i != 0 and i != len(caminhoDaImagem) - 1):
            caminho += caminhoDaImagem[i]
        else:
            if(caminhoDaImagem[i] != '"'):
                caminho += caminhoDaImagem[i]

    return caminho

# path = trataCaminho(input("Caminho da imagem: "))
path = trataCaminho("Images\The Forest Arco e Flecha.jpeg")
imagem = Image.open(path)
imagem.show()

# Apresente o Histograma da imagem em RGB

imagem = imagem.convert("RGB")

r, g, b = imagem.split()

plt.figure(figsize=(10, 4))
plt.hist(r.histogram(), bins=256, color='red', alpha=0.5, label='Red')
plt.hist(g.histogram(), bins=256, color='green', alpha=0.5, label='Green')
plt.hist(b.histogram(), bins=256, color='blue', alpha=0.5, label='Blue')
plt.title("Histograma RGB")
plt.xlabel("Valor de Intensidade")
plt.ylabel("Frequência")
plt.legend()
plt.grid(True)
plt.tight_layout()
# plt.show()

# Apresente o Hostograma da imagem em RGB, porém agora apresente separado cada conjunto de cores, desta forma, será apresentado o
# histograma apenas do R (RED);

plt.figure(figsize=(10, 4))
plt.hist(r.histogram(), bins=256, color='red', alpha=0.5, label='Red')
plt.title("Histograma RED")
plt.xlabel("Valor de Intensidade")
plt.ylabel("Frequência")
plt.legend()
plt.grid(True)
plt.tight_layout()
# plt.show()

# Depois do G (GREEN):

plt.figure(figsize=(10, 4))
plt.hist(g.histogram(), bins=256, color='green', alpha=0.5, label='Green')
plt.title("Histograma GREEN")
plt.xlabel("Valor de Intensidade")
plt.ylabel("Frequência")
plt.legend()
plt.grid(True)
plt.tight_layout()
# plt.show()

# E finalmente do B (BLUE).

plt.figure(figsize=(10, 4))
plt.hist(b.histogram(), bins=256, color='blue', alpha=0.5, label='Blue')
plt.title("Histograma BLUE")
plt.xlabel("Valor de Intensidade")
plt.ylabel("Frequência")
plt.legend()
plt.grid(True)
plt.tight_layout()
# plt.show()

# Apresente o Histograma em tons de Cinza (8 bits).

imagem_gray = imagem.convert("L")
plt.figure(figsize=(10, 4))
plt.hist(imagem_gray.histogram(), bins=256, color='gray', alpha=0.7, label='Gray')
plt.title("Histograma em Tons de Cinza (8 bits)")
plt.xlabel("Valor de Intensidade")
plt.ylabel("Frequência")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Utilizando o recurso SUBPLOT, crie uma matriz 2x2 para poder apresentar 4 gráficos diferentes.
# O Gráfico 1 será o histograma de valores que vão de 0 até 63;
# O Gráfico 2 será o histograma de valores que vão de 64 até 127;
# O Gráfico 3 será o histograma de valores que vão de 128 até 191;
# O Gráfico 4 será o histograma de valores que vão de 192 até 255;

hist_gray = imagem_gray.histogram()

ranges = [(0, 63), (64, 127), (128, 191), (192, 255)]
titles = [
    "Histograma: Intensidade 0-63",
    "Histograma: Intensidade 64-127",
    "Histograma: Intensidade 128-191",
    "Histograma: Intensidade 192-255"
]

fig, axs = plt.subplots(2, 2, figsize=(12, 8))
axs = axs.flatten()

for i, (start, end) in enumerate(ranges):
    bins = list(range(start, end + 2))
    data = []
    for j in range(start, end + 1):
        data.extend([j] * hist_gray[j])
    axs[i].hist(data, bins=bins, color='gray', alpha=0.7)
    axs[i].set_title(titles[i])
    axs[i].set_xlabel("Valor de Intensidade")
    axs[i].set_ylabel("Frequência")
    axs[i].grid(True)

plt.tight_layout()
plt.show()

# Faça a limirização da imagem RGB original com valor a sua escolha, apresente a imagem original e ao lado a imagem limiarizada.
def limiarizador(imagem, limite):
    largura, altura = imagem.size
    img_limiarizada = Image.new("L", (largura, altura))  # Imagem em tons de cinza

    total = largura * altura
    cont = 0

    for x in range(largura):
        for y in range(altura):
            pixel = imagem.getpixel((x, y))  # pixel = (R, G, B)

            luminancia = sum(pixel) // 3  # média dos canais

            if luminancia >= limite:
                img_limiarizada.putpixel((x, y), luminancia)  # valor em escala de cinza
            else:
                img_limiarizada.putpixel((x, y), 0)  # preto

            cont += 1
            if((cont * 10000) % total == 0):
                print(f"\rLimiarização {cont * 100 // total}% Concluída!", end="")

    print(f"\rLimiarização {100}% concluída!")

    return img_limiarizada


T = 150 # Valor de limiarização escolhido

imagem_limiarizada = limiarizador(imagem, T)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(imagem)
plt.title("Imagem Original")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(imagem_limiarizada, cmap='gray')
plt.title(f"Imagem Limiarizada (T={T})")
plt.axis("off")

plt.tight_layout()
plt.show()

# Faça outra limirização da imagem RGB original com valor a sua escolha e diferente do exercício anterior, apresente a imagem original e ao lado a imagem limiarizada.
