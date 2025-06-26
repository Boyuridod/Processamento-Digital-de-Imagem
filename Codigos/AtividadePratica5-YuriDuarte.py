# Atividade Prática de Transformações Morfológicas
# Estudante: Yuri David Silva Duarte
# Data: 26/06/2025

# TODO Requirements
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import pywt # pip install PyWavelets

# 1) Escolha uma imagem
caminho = ".\Images\wallpaperminimalista.jpg"
imagem = Image.open(caminho)
imagem.show() # Mostra a imagem escolhida

def imgParaCinza(imagem):
    largura, altura = imagem.size  # width, height
    total = largura * altura
    cont = 0
    cinza = Image.new("L", (largura, altura))

    for x in range(largura):
        for y in range(altura):
            R, G, B = imagem.getpixel((x, y))

            pixel = int((0.299 * R) + (0.587 * G) + (0.114 * B))

            cinza.putpixel((x, y), pixel)
            
            cont += 1

            if((cont * 10000) % total == 0):
                print(f"\rConvertendo imagem em tons de cinza {cont * 100 // total}% concluído", end="")

    print("")

    return cinza

imagemCinza = imgParaCinza(imagem)

# 2) Escolher um “objeto-alvo” a ser segmentado (separado)
# 3) Aplicar o melhor Filtro Passa-Baixa para o caso e, em seguida, Realizar
# a melhor limiarização

def filtro_circular(shape, raio_min=0, raio_max=np.inf, passa=True):
    rows, cols = shape
    crow, ccol = rows // 2, cols // 2
    y, x = np.ogrid[:rows, :cols]
    distancia = np.sqrt((x - ccol)**2 + (y - crow)**2)
    if passa:
        return (distancia >= raio_min) & (distancia <= raio_max)
    else:
        return ~((distancia >= raio_min) & (distancia <= raio_max))

def aplicar_filtro(F_shift, mascara):
    filtrado = F_shift * mascara
    f_ishift = np.fft.ifftshift(filtrado)
    img_back = np.fft.ifft2(f_ishift)
    return np.abs(img_back)

def filtros_frequencia(imagemCinza):
    imagem_array = np.array(imagemCinza)
    F = np.fft.fft2(imagem_array)
    F_shift = np.fft.fftshift(F)

    shape = F_shift.shape

    # Filtro Passa-Baixa
    mascara_pb = filtro_circular(shape, raio_max=50, passa=True)
    img_pb = aplicar_filtro(F_shift, mascara_pb)

    # Filtro Passa-Alta
    mascara_pa = filtro_circular(shape, raio_min=30, passa=True)
    img_pa = aplicar_filtro(F_shift, mascara_pa)

    # Filtro Passa-Banda
    mascara_pbanda = filtro_circular(shape, raio_min=20, raio_max=60, passa=True)
    img_pbanda = aplicar_filtro(F_shift, mascara_pbanda)

    # Filtro Rejeita-Banda
    mascara_rbanda = filtro_circular(shape, raio_min=20, raio_max=60, passa=False)
    img_rbanda = aplicar_filtro(F_shift, mascara_rbanda)

    # Exibe os resultados
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.imshow(img_pb, cmap='gray')
    plt.title("Passa-Baixa")
    plt.axis('off')

    plt.subplot(2, 2, 2)
    plt.imshow(img_pa, cmap='gray')
    plt.title("Passa-Alta")
    plt.axis('off')

    plt.subplot(2, 2, 3)
    plt.imshow(img_pbanda, cmap='gray')
    plt.title("Passa-Banda")
    plt.axis('off')

    plt.subplot(2, 2, 4)
    plt.imshow(img_rbanda, cmap='gray')
    plt.title("Rejeita-Banda")
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    return img_pb

passaBaixa = filtros_frequencia(imagemCinza)

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

T = 50

limiarizada = (limiarizador(passaBaixa, T))
limiarizada.show()

# 4) Propor uma sequência de operações morfológicas para se criar uma
# “máscara” para o objeto alvo

# 5) Multiplicar a “máscara” gerada pela imagem original e visualizar o
# resultado
