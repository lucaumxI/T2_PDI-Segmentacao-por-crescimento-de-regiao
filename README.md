# T2 PDI: Segmentacao por crescimento de regiao

O que precisamos fazer basicamente é pegar um conjunto de pixeis (inicialmente um pixel) de uma imagem, analisar os vizinhos imediatos (os 4 do lado, sem diagonais) da borda do conjuntoo, e, caso os vizinhos cumpram essa restrição:
$$
\mu -f \cdot \sigma < p < \mu +f \cdot \sigma
$$
onde:
- $\mu$: média da intensidade dos pixeis do conjunto
- $\sigma$: desvio padrão da intensidade dos pixeis do conjunto
- $f$: hiperparametro

o vizinho é adicionado ao conjunto.

## Dicas de implementação:
1. A cada vizinho adicionado, a borda, média e desvio padrão são atualizados. Para não precisar iterar entre todos os pixeis do conjunto para atualizar a média e desvio padrão, podemos usar essas fórmulas:

   ```math
   \begin{aligned}
   \mu_{i+1}&=\frac{N\mu_{i}+I_p}{N+1}\\
   \sigma_{i+1}&=\sqrt{\frac{(\sigma_i^2+\mu_i^2)N+I_p^2}{N+1}-\mu_{i+1}^2}
   \end{aligned}
   ```
   
   onde:
   - $\mu_{i+1}$: média atualizada após adicionar o novo pixel ao conjunto
   - $N$: quantidade de pixeis no conjunto
   - $I_p$: intensidade do novo pixel adicionado
   - $\sigma_{i+1}$: desvio padrão após adiconar o novo pixel ao conjunto


2. Trabalhar com duas listas, uma para armazenar a borda do conjunto ($B$) e outra para armazenar os pixeis do conjunto($R$). Os vizinhos da lista $B$ são os que serão analisados e adicionados ou não ao conjunto $R$, após adicionar os vizinhos, é preciso analisar quais pixeis serão adicionados ou retirados da lista $B$ e, obviamente, $R \supset B$.
