# Referências: 
# https://youtu.be/_3VcRHwZpPU

# Transformar uma imagem para tons de cinza

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


def getNomeImagem(caminhoDaImagem):
    nome = ""

    for i in caminhoDaImagem:
        if(ord(i) == 92): # if(i == "\")
           nome = ""
        else:
            nome += i

    return nome

def img2gray(caminhoDaImagem):

    imagem = Image.open(caminhoDaImagem)

    largura, altura = imagem.size # width, height

    imgGray = Image.new("RGB", (largura, altura))

    total = largura * altura

    cont = 0

    for x in range(largura):
        for y in range(altura):
            pixel = imagem.getpixel((x, y))
            luminancia = sum(pixel) // 3

            imgGray.putpixel((x, y), (luminancia, luminancia, luminancia))

            cont += 1

            if(cont * 10000 % total == 0):
                print(f"\r{cont * 100 // total}% Concluído", end="")

    novaImagem = "Output\\" + getNomeImagem(caminhoDaImagem)

    print(f"\nImagem salva em: {novaImagem}")

    imgGray.save(novaImagem)

path = trataCaminho(input("Caminho da imagem: "))
imagem = img2gray(path)