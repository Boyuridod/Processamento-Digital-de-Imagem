from PIL import Image
from math import sqrt

def trataCaminho(caminhoDaImagem):
    
    caminho = ""
    
    for i in range(len(caminhoDaImagem)):
        if(i != 0 and i != len(caminhoDaImagem) - 1):
            caminho += caminhoDaImagem[i]
        else:
            if(caminhoDaImagem[i] != '"'):
                caminho += caminhoDaImagem[i]

    return caminho

def getNomeImagem(caminhoDaImagem):
    nome = ""

    for i in caminhoDaImagem:
        if(ord(i) == 92): # if(i == "\")
           nome = ""
        else:
            nome += i

    return nome

def img2gray(imagem):
    largura, altura = imagem.size # width, height

    imgGray = Image.new("L", (largura, altura))

    total = largura * altura

    cont = 0

    for x in range(largura):
        for y in range(altura):
            pixel = imagem.getpixel((x, y))
            luminancia = sum(pixel) // 3

            imgGray.putpixel((x, y), (luminancia))

            cont += 1

            if((cont * 10000) % total == 0):
                print(f"\rTransformar em cinza {cont * 100 // total}% Concluído", end="")

    return imgGray

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

# TODO Salvar a imagem
def filtroNegativo(imagem):
    # imagem = Image.open(imagem)
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
                print(f"\r{cont * 100 // total}% Concluído", end="")

    return imgNegativo

# TODO Vide anterior
def aumentaBrilho(imagem, quantidade):
    largura, altura = imagem.size  # width, height
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
                print(f"\r{cont * 100 // total}% Concluído", end="")

    return imgBrilho

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

#TODO Transformar em dinâmico
def mascara5img(imagem):
    largura, altura = imagem.size  # width, height
    mascaraAplicada = Image.new("RGB", (largura, altura))
    total = largura * altura
    cont = 0
    for x in range(largura):
        for y in range(altura):
            R = 0
            G = 0
            B = 0

            for j in range(y - 2, y + 3, 1):
                for i in range(x - 2, x + 3, 1):
                    try:
                        r, g, b = imagem.getpixel((i, j))
                        R += r
                        G += g
                        B += b
                    except:
                        R += (255 // 2)
                        G += (255 // 2)
                        B += (255 // 2)

            R = R // 25 #(5 * 5)
            G = G // 25 #(5 * 5)
            B = B // 25 #(5 * 5)

            mascaraAplicada.putpixel((x, y), (R, G, B))

            cont += 1

            if((cont * 10000) % total == 0):
                print(f"\rMascara 9x9 {cont * 100 // total}% concluído", end="")

    print("")
    
    return mascaraAplicada

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

#FIM