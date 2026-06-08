import numpy as np
import math
import matplotlib.pyplot as plt
import random
from PIL import Image
from pathlib import Path

def segmentacao(imagem: np.ndarray, regiaoInicial: list[tuple[int, int]], f: float) -> set[tuple[int, int]]:
    # Inicializacao
    regiao = set(regiaoInicial)
    borda = set()
    N = len(regiao)

    # Definicao do conjunto borda
    defBorda(regiao, borda, imagem)

    valores_regiao = [imagem[rx, ry] for rx, ry in regiao]  # Intensidades da região inicial
    mu = np.mean(valores_regiao)                            # média e desvio padrão da região inicial
    sigma = np.std(valores_regiao) if len(valores_regiao) > 1 else 0

    
    houve_crescimento = True    # flag para condição de parada
    while houve_crescimento:
        houve_crescimento = False
        novos_pixels_regiao = set() # conjunto para salvar a borda que será adicionada a região

        for bx, by in borda:
            intensidade = imagem[bx, by]
            if mu - (f * sigma) <= intensidade <= mu + (f * sigma):
                novos_pixels_regiao.add((bx, by))
        if novos_pixels_regiao: # verifica se o conjunto não é nulo
            houve_crescimento = True
            
            # atualiza media e desvio
            for px, py in novos_pixels_regiao:
                intensidade = imagem[px, py]
                novo_mu = atualizar_media(mu, N, intensidade)

                sigma = atualizar_desvio(mu, sigma, N, intensidade)
                mu = novo_mu
                N += 1 
                
            regiao.update(novos_pixels_regiao)
            defBorda(regiao, borda, imagem)
            
            
    return regiao

#formula de atualizar media
def atualizar_media(mu, N, Ip):
    novo_mu = (N * mu + Ip) / (N + 1) 

    return novo_mu

#formula de atualizar desvio padrao
def atualizar_desvio(mu, sigma, N, Ip):
    Ip = float(Ip)  # evitar overflow ao elevar ao quadrado
    novo_mu = atualizar_media(mu, N, Ip)

    sigma2 = ((((sigma ** 2) + (mu ** 2)) * N + (Ip ** 2))/ (N + 1)) - (novo_mu ** 2)
    
    novo_sigma = math.sqrt(sigma2)

    return novo_sigma 


def defBorda(regiao: set[tuple[int, int]], borda: set[tuple[int, int]], imagem: np.ndarray) -> set[tuple[int, int]]:
    # Obter as dimensões da imagem
    altura, largura = imagem.shape[:2]
    borda.clear()

    # Deslocamento para os 4 vizinhos (cima, baixo, esquerda, direita)
    vizinhos_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for rx, ry in regiao:
        for dx, dy in vizinhos_4:
            nx, ny = rx + dx, ry + dy
            # Verificar se o vizinho está dentro dos limites da imagem e não pertence à região
            if 0 <= nx < altura and 0 <= ny < largura and (nx, ny) not in regiao:
                borda.add((nx, ny))

    
    return borda

def visualizar_segmentacao(imagem: np.ndarray, regiao: set[tuple[int, int]]) -> None:
    # cria uma cópia da imagem e a converte para RGB empilhando a matriz de cinza
    imagem_colorida = np.stack((imagem, imagem, imagem), axis=-1)

    # pinta os pixels da região segmentada de Vermelho [R, G, B]
    cor_destaque = [255, 0, 0]
    
    for rx, ry in regiao:
        imagem_colorida[rx, ry] = cor_destaque

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    axes[0].imshow(imagem, cmap='gray', vmin=0, vmax=255)
    axes[0].set_title("Imagem Original")
    axes[0].axis('off')

    # Para a colorida, o matplotlib detecta automaticamente os 3 canais (não usar cmap)
    axes[1].imshow(imagem_colorida)
    axes[1].set_title("Região Segmentada (Máscara Vermelha)")
    axes[1].axis('off')

    plt.tight_layout()
    plt.show()

def main() -> None:
    # caminho imagem
    caminho = "cameraman.tiff" 
    
    try:
        # assegura que a imagem é em tons de cinza
        imagem_pil = Image.open(caminho).convert('L')
        imagem = np.array(imagem_pil)
    except FileNotFoundError:
        print(f"Erro: Imagem não encontrada no caminho '{caminho}'")
        return

    altura, largura = imagem.shape

    # escolhe um pixel aleatório dentro dos limites da imagem
    rx = random.randint(0, altura - 1)
    ry = random.randint(0, largura - 1)
    
    # região inicial se torna o pixel aleatório junto com seus 4 vizinhos (se existirem)
    regiaoInicial = [(rx, ry)]
    vizinhos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dx, dy in vizinhos:
        nx, ny = rx + dx, ry + dy
        if 0 <= nx < altura and 0 <= ny < largura:
            regiaoInicial.append((nx, ny))

    print(f"Dimensões da Imagem: {altura}x{largura}")
    print(f"Semente Aleatória Escolhida: ({rx}, {ry}) com {len(regiaoInicial)-1} vizinhos válidos.")

    # hiperparametro f
    fator_f = 2.5
    
    print("Iniciando segmentação...")
    resultado = segmentacao(imagem, regiaoInicial, fator_f)
    
    print(f"Segmentação concluída. Região contém {len(resultado)} pixels.")
    
    visualizar_segmentacao(imagem, resultado)

if __name__ == "__main__":
    main()