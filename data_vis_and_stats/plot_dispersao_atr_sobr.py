##############################################################################
### Plota a dispersão de cada atributo do data.csv (sinais vitais das vítimas)
### contra a sobr. 
### Utiliza o tri para dar cor aos pontos: 
### 0 verde; 1 amarelo; 2 vermelho, 3 preto


import pandas as pd
import matplotlib.pyplot as plt
import math

# 1. Carregar o arquivo CSV
df = pd.read_csv('data.csv')


# 2. Definir o mapeamento de cores com base no valor de 'tri'
# tri=0 (verde), tri=1 (amarelo), tri=2 (vermelho), tri=3 (preto)
cores_tri = {0: 'green', 1: 'gold', 2: 'red', 3: 'black'}

# Criar uma nova coluna no DataFrame contendo a cor correspondente de cada linha
# Se houver algum valor fora de 0-3 por segurança, mapeia para cinza ('gray')
df['cor_ponto'] = df['tri'].map(cores_tri).fillna('gray')

# 3. Isolar a variável alvo (Y) e selecionar os preditores para o eixo X
target = 'sobr'
# Removemos 'sobr', 'tri' (pois virou cor) e a coluna de cor auxiliar que criamos
features = df.select_dtypes(include=['number']).columns.drop([target, 'tri', 'cor_ponto'], errors='ignore')

# 4. Configurar a matriz de subplots dinamicamente
num_features = len(features)
num_cols = 3  # Número de gráficos por linha
num_rows = math.ceil(num_features / num_cols)

fig, axes = plt.subplots(num_rows, num_cols, figsize=(5 * num_cols, 4 * num_rows))
axes = axes.flatten()  # Achata a matriz para facilitar a iteração

# 5. Plotar cada atributo contra 'sobr' usando as cores do 'tri'
for i, col in enumerate(features):
    ax = axes[i]
    
    # O parâmetro 'c' recebe a série de cores baseada no 'tri'
    scatter = ax.scatter(df[col], df[target], c=df['cor_ponto'], alpha=0.6, edgecolors='none')
    
    ax.set_title(f'{col} vs {target}', fontsize=12, fontweight='bold')
    ax.set_xlabel(col, fontsize=10)
    ax.set_ylabel(target, fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.5)

# 6. Criar uma legenda manual para as cores do 'tri' e adicionar ao gráfico
legenda_elementos = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Tri 0 (Verde)'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='gold', markersize=10, label='Tri 1 (Amarelo)'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Tri 2 (Vermelho)'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=10, label='Tri 3 (Preto)')
]
# Adiciona a legenda no canto superior do primeiro gráfico (ou pode ajustar a posição global)
fig.legend(handles=legenda_elementos, loc='upper center', bbox_to_anchor=(0.5, 0.98), ncol=4, fontsize=11)

# 7. Esconder subplots vazios (caso o número de atributos não seja múltiplo de 3)
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

# Ajustar o espaçamento superior para não cortar a legenda global
plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.show()