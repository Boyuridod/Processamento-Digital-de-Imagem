# Atividade Prática de Convolução de Imagem
# Estudante: Yuri David Silva Duarte

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

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
                print(f"\rConvertendo em cinza {cont * 100 // total}% concluído", end="")

    print("")

    return cinza

# caminho = input("Digite o caminho da imagem: ").strip('"')
caminho = ".\Images\The Forest Arco e Flecha.jpeg"
imagem = Image.open(caminho)
# imagem.show() # Mostra a imagem escolhida

# Escolha uma imagem em níveis de cinza
imagemCinza = imgParaCinza(imagem)
# imagemCinza.show() # Mostra a imagem em cinza

# Baseado na Transformada de Fourier:
## - Apresente-a em seu espectro da frequência

def transformadaFourier(imagemCinza):

    imagem_array = np.array(imagemCinza) # Converte para array NumPy

    f_transformada = np.fft.fft2(imagem_array) # Aplica a Transformada de Fourier 2D

    f_transformada_shift = np.fft.fftshift(f_transformada) # Desloca o zero (baixa frequência) para o centro da imagem

    espectro = np.abs(f_transformada_shift) # Calcula o módulo (magnitude) da transformada

    espectro_log = np.log(1 + espectro) # Aplica log para visualização melhor

    plt.figure(figsize=(10, 5)) # Mostra a imagem original e o espectro

    plt.subplot(1, 2, 1)
    plt.imshow(imagem_array, cmap='gray')
    plt.title("Imagem em tons de cinza")
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(espectro_log, cmap='gray')
    plt.title("Espectro da Frequência (Fourier)")
    plt.axis('off')

    plt.tight_layout()
    plt.show()

transformadaFourier(imagemCinza)

## - Aplique um filtro passa-alta, passa-baixa, passa-banda e rejeita-banda
## - Aplique a transformação inversa e Mostre as imagens resultantes
## - Comente sua percepção do resultado e o que cada um dos filtros causou na imagem



# Baseado na Transformada Wavelet
## - Apresente a imagem com 3 níveis de aplicação da Transformada Wavelet
## - Aplique um filtro passa-alta e um passa-baixa
## - Aplique a transformação inversa e Mostre as imagens resultantes
## - Comente sua percepção do resultado e o que cada um dos filtros causou na imagem