
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

# Apresente o Histograma da imagem em RGB

imagem = imagem.convert("RGB")







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
                img_limiarizada.putpixel((x, y), 255)  # branco

            cont += 1
            if((cont * 10000) % total == 0):
                print(f"\rLimiarização {cont * 100 // total}% Concluída!", end="")

    print(f"\rLimiarização {100}% concluída!")

    return img_limiarizada


T = 200 # Valor de limiarização escolhido

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