# Estudante: Yuri David Silva Duarte

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import pywt # pip install PyWavelets

# Transformar a imagem em cinza
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

## - Aplique um filtro passa-alta, passa-baixa, passa-banda e rejeita-banda
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

    return img_pb, img_pa, img_pbanda, img_rbanda

## - Aplique a transformação inversa e Mostre as imagens resultantes
# TODO FIX Ta td preto
def inversaFourier(filtrados):
    nomes = ["Passa-Baixa (Após Inversa)", "Passa-Alta (Após Inversa)",
             "Passa-Banda (Após Inversa)", "Rejeita-Banda (Após Inversa)"]

    plt.figure(figsize=(12, 8))

    for i, filtrado in enumerate(filtrados):
        f_ishift = np.fft.ifftshift(filtrado)        # Desfaz o shift no espectro
        img_back = np.fft.ifft2(f_ishift)            # Faz a transformada inversa
        img_resultado = np.abs(img_back)             # Mantém apenas a parte real/magnitude

        plt.subplot(2, 2, i+1)
        plt.imshow(img_resultado, cmap='gray')
        plt.title(nomes[i])
        plt.axis('off')

    plt.tight_layout()
    plt.show()

# Baseado na Transformada Wavelet
## - Apresente a imagem com 3 níveis de aplicação da Transformada Wavelet
def aplicarWavelet(imagemCinza):
    imagem_array = np.array(imagemCinza)

    plt.figure(figsize=(12, 10))

    dados = imagem_array
    for nivel in range(1, 4):
        coeffs = pywt.dwt2(dados, 'haar')
        cA, (cH, cV, cD) = coeffs

        plt.subplot(3, 3, (nivel - 1)*3 + 1)
        plt.imshow(cA, cmap='gray')
        plt.title(f'Nível {nivel} - Aproximação (cA)')
        plt.axis('off')

        plt.subplot(3, 3, (nivel - 1)*3 + 2)
        plt.imshow(np.abs(cH), cmap='gray')
        plt.title(f'Nível {nivel} - Horizontal (cH)')
        plt.axis('off')

        plt.subplot(3, 3, (nivel - 1)*3 + 3)
        plt.imshow(np.abs(cV + cD), cmap='gray')
        plt.title(f'Nível {nivel} - Vertical+Diagonal (cV+cD)')
        plt.axis('off')

        dados = cA  # Para o próximo nível, trabalha sobre a aproximação atual

    plt.tight_layout()
    plt.show()

## - Aplique um filtro passa-alta e um passa-baixa
def filtrosPAPBWavelet(imagemCinza):
    imagem_array = np.array(imagemCinza)

    # Aplica a Transformada Discreta de Wavelet (DWT) de 1 nível
    coeffs = pywt.dwt2(imagem_array, 'haar')
    cA, (cH, cV, cD) = coeffs

    # Filtro Passa-Baixa: reconstruindo só com cA (Aproximação)
    zeros_detalhes = (np.zeros_like(cH), np.zeros_like(cV), np.zeros_like(cD))
    passa_baixa = pywt.idwt2((cA, zeros_detalhes), 'haar')

    # Filtro Passa-Alta: reconstruindo só com os detalhes (cH, cV, cD)
    zeros_aproximacao = np.zeros_like(cA)
    passa_alta = pywt.idwt2((zeros_aproximacao, (cH, cV, cD)), 'haar')

    # Exibe os resultados
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 3, 1)
    plt.imshow(imagem_array, cmap='gray')
    plt.title("Imagem Original")
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(passa_baixa, cmap='gray')
    plt.title("Passa-Baixa (Wavelet)")
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(np.abs(passa_alta), cmap='gray')
    plt.title("Passa-Alta (Wavelet)")
    plt.axis('off')

    plt.tight_layout()
    plt.show()

## - Aplique a transformação inversa e Mostre as imagens resultantes
def inversaWavelet(imagemCinza):
    imagem_array = np.array(imagemCinza)

    # Faz a DWT nível 1
    coeffs = pywt.dwt2(imagem_array, 'haar')
    cA, (cH, cV, cD) = coeffs

    # Reconstrói a imagem completa (usando todos os coeficientes)
    imagem_reconstruida = pywt.idwt2((cA, (cH, cV, cD)), 'haar')

    # Reconstrói imagens parciais (só com algumas partes)
    # Só aproximação
    img_aproximacao = pywt.idwt2((cA, (np.zeros_like(cH), np.zeros_like(cV), np.zeros_like(cD))), 'haar')

    # Só detalhes (bordas)
    img_detalhes = pywt.idwt2((np.zeros_like(cA), (cH, cV, cD)), 'haar')

    # Exibe os resultados
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 3, 1)
    plt.imshow(imagem_array, cmap='gray')
    plt.title("Imagem Original")
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(img_aproximacao, cmap='gray')
    plt.title("Somente Aproximação (cA)")
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(np.abs(img_detalhes), cmap='gray')
    plt.title("Somente Detalhes (cH+cV+cD)")
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    # Mostra a imagem reconstruída completa
    plt.figure()
    plt.imshow(np.abs(imagem_reconstruida), cmap='gray')
    plt.title("Imagem Reconstruída Completa (Após Inversa)")
    plt.axis('off')
    plt.show()

opcao = 1000

# caminho = input("Digite o caminho da imagem: ").strip('"')
caminho = ".\Images\The Forest Arco e Flecha.jpeg"
imagem = Image.open(caminho)
# imagem.show() # Mostra a imagem escolhida

imagemCinza = imgParaCinza(imagem)
# imagemCinza.show() # Mostra a imagem em cinza

while(opcao != "0"):
    print('''
    **Selecione uma opção**
Baseado na Transformada de Fourier:
    1) Apresente-a em seu espectro da frequência
    2) Aplique um filtro passa-alta, passa-baixa, passa-banda e rejeita-banda
    3) Aplique a transformação inversa e Mostre as imagens resultantes
    4) Comente sua percepção do resultado e o que cada um dos filtros causou na imagem
Baseado na Transformada Wavelet:
    5) Apresente a imagem com 3 níveis de aplicação da Transformada Wavelet
    6) Aplique um filtro passa-alta e um passa-baixa
    7) Aplique a transformação inversa e Mostre as imagens resultantes
    8) Comente sua percepção do resultado e o que cada um dos filtros causou na imagem
Aplicação
    9) Executar todos em sequencia
    0) Fechar''')

    opcao = input("Digite o número da opção aqui: ")

    if(opcao == "1"):
        print("1) Apresente-a em seu espectro da frequência")
        transformadaFourier(imagemCinza)

    elif(opcao == "2"):
        print("2) Aplique um filtro passa-alta, passa-baixa, passa-banda e rejeita-banda")
        filtros_resultados = filtros_frequencia(imagemCinza)

    elif(opcao == "3"):
        print("3) Aplique a transformação inversa e Mostre as imagens resultantes")
        filtros_resultados = filtros_frequencia(imagemCinza)
        inversaFourier(filtros_resultados)

    elif(opcao == "4"):
        print("4) Comente sua percepção do resultado e o que cada um dos filtros causou na imagem")
        print("O passa-baixa deixou a imagem borrada")
        print("O passa-alta deixou as bordas mais nítidas")
        print("O passa-banda deixou as bordas da imagem borrada")
        print("O rejeita-banda deixou a imagem mais clara e borrada")
        input("Aperte ENTER para continuar ")

    elif(opcao == "5"):
        print("5) Apresente a imagem com 3 níveis de aplicação da Transformada Wavelet")
        aplicarWavelet(imagemCinza)

    elif(opcao == "6"):
        print("6) Aplique um filtro passa-alta e um passa-baixa")
        filtrosPAPBWavelet(imagemCinza)

    elif(opcao == "7"):
        print("7) Aplique a transformação inversa e Mostre as imagens resultantes")
        inversaWavelet(imagemCinza)

    elif(opcao == "8"):
        print("8) Comente sua percepção do resultado e o que cada um dos filtros causou na imagem")
        print("O passa-alta deixou a imagem menos sombreada")
        print("O passa-baixa escureceu a imagem e ressaltou as bordas mais próximas da câmera")
        input("Aperte ENTER para continuar ")

    elif(opcao == "9"):
        print("Executando todos em sequência...")
        transformadaFourier(imagemCinza)
        filtros_resultados = filtros_frequencia(imagemCinza)
        inversaFourier(filtros_resultados)
        print("4) Comente sua percepção do resultado e o que cada um dos filtros causou na imagem")
        print("O passa-baixa deixou a imagem borrada")
        print("O passa-alta deixou as bordas mais nítidas")
        print("O passa-banda deixou as bordas da imagem borrada")
        print("O rejeita-banda deixou a imagem mais clara e borrada")
        input("Aperte ENTER para continuar ")
        aplicarWavelet(imagemCinza)
        filtrosPAPBWavelet(imagemCinza)
        print("8) Comente sua percepção do resultado e o que cada um dos filtros causou na imagem")
        print("O passa-alta deixou a imagem menos sombreada")
        print("O passa-baixa escureceu a imagem e ressaltou as bordas mais próximas da câmera")
        input("Aperte ENTER para continuar ")

    elif(opcao == "0"):
        print("\nFechando o programa...\n")

    else:
        print(f"\n\"{opcao}\" não é uma opção válida!\nTente digitar outro valor!!!\n")
        input("Aperte ENTER para continuar ")
