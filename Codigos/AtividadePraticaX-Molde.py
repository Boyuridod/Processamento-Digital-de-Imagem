# Atividade Prática de 
# Estudante: Yuri David Silva Duarte
# Data: 
# TODO Arrumar cabeçalho

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import pywt # pip install PyWavelets

def imgParaCinza(imagem): # Transformar a imagem em cinza
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

# Funções aqui

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
    1) w??
    9) Executar todos em sequencia
    0) Fechar''')

    opcao = input("Digite o número da opção aqui: ")

    if(opcao == "1"):
        print("1) Apresente-a em seu espectro da frequência")
        transformadaFourier(imagemCinza)

    

    elif(opcao == "0"):
        print("\nFechando o programa...\n")

    else:
        print(f"\n\"{opcao}\" não é uma opção válida!\nTente digitar outro valor!!!\n")
        input("Aperte ENTER para continuar ")
