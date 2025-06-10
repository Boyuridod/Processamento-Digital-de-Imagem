# Atividade Prática de Convolução de Imagem
# Estudante: Yuri David Silva Duarte
# Data: 05/06/2025

# Pegar a Imagem original
from PIL import Image

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
path = trataCaminho("D:\DesenvolvimentoProjetos\Processamento-Digital-de-Imagem\Images\The Forest Arco e Flecha.jpeg")
imagem = Image.open(path)

# implementação do filtro Negativo em RGB: os valores das bandas R, G e B são invertidos conforme a operação aritmética: 255 menos o valor do pixel da matriz;
def filtroNegativo(imagem):
    largura, altura = imagem.size  # width, height
    imgNegativo = Image.new("RGB", (largura, altura))
    total = largura * altura
    cont = 0
    for x in range(largura):
        for y in range(altura):
            pixel = imagem.getpixel((x, y))

            imgNegativo.putpixel((x, y), (255 - pixel[0], 255 - pixel[1], 255 - pixel[2]))

            cont += 1

            if((cont * 10000) % total == 0):
                print(f"\rFiltro negativo {cont * 100 // total}% concluído", end="")

    print("")

    return imgNegativo

# implementação do controle de Brilho Aditivo: é somado uma medida definida pelo usuário a todos os pixels das bandas R, G e B;

def aumentaBrilho(img, quantidade):
    largura, altura = img.size  # width, height
    imgBrilho = Image.new("RGB", (largura, altura))
    total = largura * altura
    cont = 0
    for x in range(largura):
        for y in range(altura):
            R, G, B = imagem.getpixel((x, y))

            R += quantidade
            G += quantidade
            B += quantidade

            if(R > 255):
                R = 255

            if(G > 255):
                G = 255

            if(B > 255):
                B = 255

            imgBrilho.putpixel((x, y), (R, G, B))

            cont += 1

            if((cont * 10000) % total == 0):
                print(f"\rSoma brilho {cont * 100 // total}% concluído", end="")

    print("")
    
    return imgBrilho

# implementação do controle de Brilho Multiplicativo: é multiplicado uma medida definida pelo usuário a todos os pixels das bandas R, G e B;

def multiplicaBrilho(img, quantidade):
    largura, altura = img.size  # width, height
    imgBrilho = Image.new("RGB", (largura, altura))
    total = largura * altura
    cont = 0
    for x in range(largura):
        for y in range(altura):
            R, G, B = imagem.getpixel((x, y))

            R *= quantidade
            G *= quantidade
            B *= quantidade

            if(R > 255):
                R = 255

            if(G > 255):
                G = 255

            if(B > 255):
                B = 255

            imgBrilho.putpixel((x, y), (R, G, B))

            cont += 1

            if((cont * 10000) % total == 0):
                print(f"\rMultiplica brilho {cont * 100 // total}% concluído", end="")

    print("")

    return imgBrilho

# Filtro da média com máscara 3x3

def mascara3img(imagem):
    largura, altura = imagem.size  # width, height
    mascaraAplicada = Image.new("RGB", (largura, altura))
    total = largura * altura
    cont = 0
    for x in range(largura):
        for y in range(altura):
            R = 0
            G = 0
            B = 0

            for j in range(y - 1, y + 2, 1):
                for i in range(x - 1, x + 2, 1):
                    try:
                        r, g, b = imagem.getpixel((i, j))
                        R += r
                        G += g
                        B += b
                    except:
                        R += 255 // 2 
                        G += 255 // 2 
                        B += 255 // 2 

            R = R // 9
            G = G // 9
            B = B // 9

            mascaraAplicada.putpixel((x, y), (R, G, B))

            cont += 1

            if((cont * 10000) % total == 0):
                print(f"\rMascara 3x3 {cont * 100 // total}% concluído", end="")

    print("")
    
    return mascaraAplicada

# Filtro da média com máscara 9x9

def mascara9img(imagem):
    largura, altura = imagem.size  # width, height
    mascaraAplicada = Image.new("RGB", (largura, altura))
    total = largura * altura
    cont = 0
    for x in range(largura):
        for y in range(altura):
            R = 0
            G = 0
            B = 0

            for j in range(y - 4, y + 5, 1):
                for i in range(x - 4, x + 5, 1):
                    try:
                        r, g, b = imagem.getpixel((i, j))
                        R += r
                        G += g
                        B += b
                    except:
                        R += (255 // 2)
                        G += (255 // 2)
                        B += (255 // 2)

            R = R // 81
            G = G // 81
            B = B // 81

            mascaraAplicada.putpixel((x, y), (R, G, B))

            cont += 1

            if((cont * 10000) % total == 0):
                print(f"\rMascara 9x9 {cont * 100 // total}% concluído", end="")

    print("")
    
    return mascaraAplicada

# Outro Filtro Passa Baixa
# Escolhi o 15x15

def mascara15img(imagem):
    largura, altura = imagem.size  # width, height
    mascaraAplicada = Image.new("RGB", (largura, altura))
    total = largura * altura
    cont = 0
    for x in range(largura):
        for y in range(altura):
            R = 0
            G = 0
            B = 0

            for j in range(y - 7, y + 8, 1):
                for i in range(x - 7, x + 8, 1):
                    try:
                        r, g, b = imagem.getpixel((i, j))
                        R += r
                        G += g
                        B += b
                    except:
                        R += (255 // 2)
                        G += (255 // 2)
                        B += (255 // 2)

            R = R // (15 * 15)
            G = G // (15 * 15)
            B = B // (15 * 15)

            mascaraAplicada.putpixel((x, y), (R, G, B))

            cont += 1

            if((cont * 10000) % total == 0):
                print(f"\rMascara 15x15 {cont * 100 // total}% concluído", end="")

    print("")
    
    return mascaraAplicada

# Fazer, usando convolução, o Filtro Passa-Alta (Prewitt)

from math import sqrt

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
                print(f"\rTransformando em cinza {cont * 100 // total}% concluído", end="")

    print("")

    return cinza

def filtroPrewitt(imagem):
    imagem = imgParaCinza(imagem)
    largura, altura = imagem.size  # width, height
    prewitt = Image.new("L", (largura, altura))
    total = largura * altura
    cont = 0

    mascHorizontal = [
        [-1,  0,  1],
        [-1,  0,  1],
        [-1,  0,  1]
    ]
    mascVertical = [
        [-1, -1, -1],
        [ 0,  0,  0],
        [ 1,  1,  1]
    ]

    for x in range(largura):
        for y in range(altura):
            Ph = 0
            Pv = 0
            for i in range(x - 1, x + 2, 1):
                for j in range(y - 1, y + 2, 1):
                    try:
                        Ph += (imagem.getpixel((i, j)) * mascHorizontal[x - i][y - j])
                        Pv += (imagem.getpixel((i, j)) * mascVertical[x - i][y - j])

                        res = int(sqrt((Ph * Ph) + (Pv * Pv)))
            
                    except:
                        Ph += 255//2
                        Pv += 255//2

                        res = int(sqrt((Ph * Ph) + (Pv * Pv)))

            prewitt.putpixel((x, y), res)

            cont += 1

            if((cont * 10000) % total == 0):
                print(f"\rFiltro de Prewitt {cont * 100 // total}% concluído", end="")

    print("")

    return prewitt

# Fazer, usando convolução, o Filtro Passa-Alta (Sobel)

def filtroSobel(imagem):
    imagem = imgParaCinza(imagem)
    largura, altura = imagem.size  # width, height
    sobel = Image.new("L", (largura, altura))
    total = largura * altura
    cont = 0

    mascHorizontal = [
        [-1,  0,  1],
        [-2,  0,  2],
        [-1,  0,  1]
    ]
    mascVertical = [
        [-1, -2, -1],
        [ 0,  0,  0],
        [ 1,  2,  1]
    ]

    for x in range(largura):
        for y in range(altura):
            Ph = 0
            Pv = 0
            for i in range(x - 1, x + 2, 1):
                for j in range(y - 1, y + 2, 1):
                    try:
                        Ph += (imagem.getpixel((i, j)) * mascHorizontal[x - i][y - j])
                        Pv += (imagem.getpixel((i, j)) * mascVertical[x - i][y - j])

                        res = int(sqrt((Ph * Ph) + (Pv * Pv)))
            
                    except:
                        Ph += 255//2
                        Pv += 255//2

                        res = int(sqrt((Ph * Ph) + (Pv * Pv)))

            sobel.putpixel((x, y), res)

            cont += 1

            if((cont * 10000) % total == 0):
                print(f"\rFiltro de Sobel {cont * 100 // total}% concluído", end="")

    print("")

    return sobel

# Fazer, usando convolução, o Filtro Passa-Alta (Laplace)

def filtroLaplaciano(imagem):
    largura, altura = imagem.size  # width, height
    total = largura * altura
    cont = 0
    imagem = imgParaCinza(imagem)
    laplace = Image.new("L", (largura, altura))

    for x in range(largura):
        for y in range(altura):
            pixel = 0

            for j in range(y - 1, y + 2, 1):
                for i in range(x - 1, x + 2, 1):
                    try:
                        if(i == x and j == y):
                            pixel += (imagem.getpixel((i, j)) * -8)
                        else:
                            pixel += imagem.getpixel((i, j))
                    except:
                        pixel += 255 // 2

            laplace.putpixel((x, y), pixel)

            cont += 1

            if((cont * 10000) % total == 0):
                print(f"\rFiltro de Laplace {cont * 100 // total}% concluído", end="")

    print("")
    
    return laplace

# Propor um outro filtro Passa-Alta
# Proponho um que a matriz é
# [1, 1, 1]
# [1, -14, 1]
# [1, 1, 1]

def filtroYuri(imagem):
    largura, altura = imagem.size  # width, height
    total = largura * altura
    cont = 0
    imagem = imgParaCinza(imagem)
    yuri = Image.new("L", (largura, altura))

    for x in range(largura):
        for y in range(altura):
            pixel = 0

            for j in range(y - 1, y + 2, 1):
                for i in range(x - 1, x + 2, 1):
                    try:
                        if(i == x and j == y):
                            pixel += (imagem.getpixel((i, j)) * -14)
                        else:
                            pixel += imagem.getpixel((i, j))
                    except:
                        pixel += 255 // 2

            yuri.putpixel((x, y), pixel)

            cont += 1

            if((cont * 10000) % total == 0):
                print(f"\rFiltro do Yuri {cont * 100 // total}% concluído", end="")

    print("")
    
    return yuri

imagemNegativo = filtroNegativo(imagem)

imagemNegativo.show()

# medida = int(input())
medida = 17

imgComMedida = aumentaBrilho(imagem, medida)

imgComMedida.show()

# medida = int(input())
medida = 2

multBrilho = multiplicaBrilho(imagem, medida)

multBrilho.show()

mascara3 = mascara3img(imagem)

mascara3.show()

mascara9 = mascara9img(imagem)

mascara9.show()

mascara15 = mascara15img(imagem)

mascara15.show()

imagemPrewitt = filtroPrewitt(imagem)

imagemPrewitt.show()

imagemSobel = filtroSobel(imagem)

imagemSobel.show()

imagemLaplace = filtroLaplaciano(imagem)

imagemLaplace.show()

imagemYuri = filtroYuri(imagem)

imagemYuri.show()