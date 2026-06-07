import numpy as np
import math
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
        novos_pixels_borda = set()  # conjunto para salvar a nova borda após adicionar a região (n~]ao sei se vai precisar disso, sepa não)

        for bx, by in borda:
            intensidade = imagem[bx, by]
            if mu - (f * sigma) < intensidade < mu + (f * sigma):
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

# def nome_da_funcao(parametro: set[tuple[int, int]]) -> set[tuple[int, int]]:


#formula de atualizar media do slide 
def atualizar_media(mu, N, Ip):
    novo_mu = (N * mu + Ip) / (N + 1) 

    return novo_mu

#formula de atualizar desvio padrao do slide 
def atualizar_desvio(mu, sigma, N, Ip):
    Ip = float(Ip) #se nao colocar isso da overflow qnd fizer ip**2
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


def main():


#isso é só um teste  
    imagem = np.array([
        [0, 0, 0, 0, 0],
        [0, 90, 100, 110, 0],
        [0, 95, 100, 105, 0],
        [0, 90, 100, 110, 0],
        [0, 0, 0, 0, 0]
    ], dtype=np.uint8)

    regiaoInicial = [
    (2,2),
    (2,3),
    (3,2)
]
    resultado = segmentacao(imagem, regiaoInicial, 1.0)

    print(resultado)
   
   #isso aqui embaixo é teste pra quando for usar img de verdade
    caminho = "CAMINHO_IMAGEM"
    imagem = np.array(Image.open(caminho))

    #segmentacao(imagem)
if __name__ == "__main__":
    main()