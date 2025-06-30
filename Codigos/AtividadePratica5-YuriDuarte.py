# Atividade Prática de Transformações Morfológicas
# Estudante: Yuri David Silva Duarte
# Data: 30/06/2025

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
            pixel = imagem.getpixel((x, y))  # pixel já é um valor de 0 a 255

            if pixel >= limite:
                img_limiarizada.putpixel((x, y), pixel)
            else:
                img_limiarizada.putpixel((x, y), 0)

            cont += 1
            if((cont * 10000) % total == 0):
                print(f"\rLimiarização {cont * 100 // total}% Concluída!", end="")

    print(f"\rLimiarização {100}% concluída!")
    return img_limiarizada

T = 50

passaBaixa = Image.fromarray(passaBaixa.astype(np.uint8)) # Transformando de volta em uma imagem PIL
limiarizada = (limiarizador(passaBaixa, T))
limiarizada.show()

# 4) Propor uma sequência de operações morfológicas para se criar uma
# “máscara” para o objeto alvo

def imgDilatacao(imagem_binaria):
    largura, altura = imagem_binaria.size
    pixels = imagem_binaria.load()
    nova_img = Image.new("L", (largura, altura), 0)
    novos_pixels = nova_img.load()
    total = largura * altura
    cont = 0

    for x in range(largura):
        for y in range(altura):
            if pixels[x, y] == 255:
                # Marca o pixel e seus vizinhos (elemento estruturante 3x3)
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < largura and 0 <= ny < altura:
                            novos_pixels[nx, ny] = 255

            cont += 1

            if((cont * 10000) % total == 0):
                print(f"\rDilatação {cont * 100 // total}% Concluída!", end="")
    
    print("")
    
    return nova_img

def imgErosao(imagem_binaria):
    largura, altura = imagem_binaria.size
    pixels = imagem_binaria.load()
    nova_img = Image.new("L", (largura, altura), 0)
    novos_pixels = nova_img.load()
    total = largura * altura
    cont = 0

    for x in range(largura):
        for y in range(altura):
            erode = True
            # Verifica se todos os vizinhos são brancos (255)
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < largura and 0 <= ny < altura:
                        if pixels[nx, ny] != 255:
                            erode = False
            if erode:
                novos_pixels[x, y] = 255
            else:
                novos_pixels[x, y] = 0

            cont += 1
            if((cont * 10000) % total == 0):
                print(f"\rErosão {cont * 100 // total}% Concluída!", end="")

    print("")

    return nova_img

print("1° Primeiro erosão depois dilatacao")
mascara_erodida = imgErosao(limiarizada)
# mascara_erodida.show()
mascara_erodida = imgDilatacao(mascara_erodida)
mascara_erodida.show()

print("2° Primeiro dilatação depois erosão")
mascara_dilatada = imgDilatacao(limiarizada)
# mascara_dilatada.show()
mascara_dilatada = imgErosao(mascara_dilatada)
mascara_dilatada.show()

print("A segunda ficou melhor (no meu caso)")

# 5) Multiplicar a “máscara” gerada pela imagem original e visualizar o
# resultado

def aplica_mascara(imagem_original, mascara_binaria):
    img_array = np.array(imagem_original)
    mask_array = np.array(mascara_binaria)

    # Expande a máscara para 3 canais se necessário
    if len(img_array.shape) == 3 and mask_array.ndim == 2:
        mask_array = np.stack([mask_array]*3, axis=-1)

    # Normaliza a máscara para 0 ou 1
    mask_bin = (mask_array > 0).astype(np.uint8)

    # Multiplica pixel a pixel
    resultado = img_array * mask_bin

    return Image.fromarray(resultado.astype(np.uint8))

resultado = aplica_mascara(imagem, mascara_dilatada)
resultado.show()
