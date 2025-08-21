"""
=====================================================================
Gerador de dataset sintético de vítimas 
=====================================================================

Funcionalidade:
---------------
cria um conjunto de dados representando vítimas de diferentes tipos de acidentes (aéreo, rodoviário,
ferroviário, deslizamento), atribuindo a cada vítima:
- Idade
- Sinais vitais (frequência cardíaca, respiratória, pressão arterial sistólica, saturação de oxigênio, temperatura)
- Pulso radial (PR)
- Grau de sangramento (SG)
- Presença de fratura (FX)
- Grau de queimadura (QUEIM)
- Escala de coma de Glasgow (GCS)
- Estado de consciência (AVPU)
- Classe de triagem (TRI)
- Probabilidade de sobrevivência (SOBR)

Os valores são gerados de forma aleatória controlada, com base em faixas e distribuições associadas a cada classe de triagem.
O programa ainda:
1. Salva o dataset gerado como arquivo CSV (`dataset_vitimas.csv`);
2. Exibe no console a contagem de vítimas por classe de triagem;
3. Gera um histograma percentual da probabilidade de sobrevivência.

Como usar:
----------
1.  Configure:
   - `n_vitimas`     → número total de registros no dataset;
   - `media_idade`   → idade média das vítimas;
   - `desvio_idade`  → desvio padrão da idade;
   - `tipo_acidente` → tipo de acidente (aereo, rodoviario, ferroviario, deslizamento).
3. Ao executar, o arquivo `dataset_vitimas.csv` será salvo no diretório atual.
4. O histograma será exibido em uma janela gráfica via matplotlib.
=====================================================================
"""

import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from collections import Counter

def gerar_dataset_vitimas(n_vitimas=100, media_idade=35, desvio_idade=7, tipo_acidente="aereo"):
    np.random.seed(42)
    random.seed(42)

    # distribuicao de triagem (START) por tipo de acidente
    # 0: verde, 1: amarelo, 2: vermelho, 3: preto
    dist_tri_por_tipo = {
        'aereo': {0: 0.2, 1: 0.3, 2: 0.4, 3: 0.1},
        'rodoviario': {0: 0.4, 1: 0.3, 2: 0.2, 3: 0.1},
        'ferroviario': {0: 0.3, 1: 0.3, 2: 0.3, 3: 0.1},
        'deslizamento': {0: 0.25, 1: 0.25, 2: 0.3, 3: 0.2}
    }

    faixas_fuzzy = {
        0: (0.93, 1.00),          # baixa - lesoes leves        
        1: (0.75, 0.95),          # media - atendimento rapido
        2: (0.15, 0.80),          # critica - atendimento imediato
        3: (0.00, 0.25)           # sem prioridade - obito ou lesoes incompativeis com a vida
    }

    triagem_parametros = {
        0: {
            'fc': (60, 100),
            'fr': (12, 20),
            'pas': (110, 130),
            'spo2': (96, 100),
            'gcs': (15, 15),
            'avpu': [0],
            'temp': (36.5, 37.4),
            'pr': [1],
            'sg': [0],
            'fx': [1],
            'queim': [0]
        },
        1: {
            'fc': (100, 120),
            'fr': (20, 30),
            'pas': (90, 110),
            'spo2': (90, 95),
            'gcs': (13, 14),
            'avpu': [0, 1],
            'temp': (37.0, 38.5),
            'pr': [1, 0],
            'sg': [1, 2],
            'fx': [0, 1],
            'queim': [0] * 85 + [1] * 10 + [2] * 5
        },
        2: {
            'fc': (121, 160),
            'fr': (31, 45),
            'pas': (60, 89),
            'spo2': (75, 89),
            'gcs': (9, 12),
            'avpu': [2],
            'temp': (34.0, 35.0),
            'pr': [0],
            'sg': [3],
            'fx': [1],
            'queim': [0] * 40 + [2] * 30 + [3] * 30
        },
        3: {
            'fc': (0, 0),
            'fr': (0, 0),
            'pas': (0, 0),
            'spo2': (0, 74),
            'gcs': (3, 6),
            'avpu': [3],
            'temp': (25.0, 34.0), 'pr': [0],
            'sg': [3],
            'fx': [1, 0],
            'queim': [0] * 50 + [3] * 50
        }
    }

    distrib = dist_tri_por_tipo[tipo_acidente]
    classificacoes = np.random.choice(
        list(distrib.keys()),
        size=n_vitimas,
        p=list(distrib.values())
    )

    idades = np.clip(np.random.normal(media_idade, desvio_idade, n_vitimas), 1, 90).astype(int)

    dados = []
    for i in range(n_vitimas):
        tri = classificacoes[i]
        idade = idades[i]
        params = triagem_parametros[tri]
        gcs_range = params['gcs']
        gcs_value = gcs_range[0] if gcs_range[0] == gcs_range[1] else np.random.randint(*gcs_range)

        registro = {
            'idade': idade,
            'fc': np.random.randint(*params['fc']) if params['fc'] != (0, 0) else 0,    # freq. cardiaca  
            'fr': np.random.randint(*params['fr']) if params['fr'] != (0, 0) else 0,    # freq. respiratoria
            'pas': np.random.randint(*params['pas']) if params['pas'] != (0, 0) else 0, # pressao art. sistolica
            'spo2': np.random.randint(*params['spo2']),                  # saturacao de oxigenio
            'temp': round(np.random.uniform(*params['temp']), 1),        # temperatura em Celsius
            'pr': random.choice(params['pr']),                           # pulso radial
            'sg': random.choice(params['sg']),                           # sangramento: Nao, Leve, Moderado, Grave
            'fx': random.choice(params['fx']),                           # fratura
            'queim': random.choice(params['queim']),                     # queimadura: Nao, Leve, Moderada, Grave
            'gcs': gcs_value,                                            # Glasgow Comma Scale
            'avpu': random.choice(params['avpu']),                       # alerta, voz, dor (pain), inconsciente
            'tri': tri,                                                  # classe de triagem
            'sobr': round(np.random.uniform(*faixas_fuzzy[tri]), 2)      # prob. de sobrevivencia
        }
        dados.append(registro)

    df = pd.DataFrame(dados)
    df.to_csv("data.csv", index=False)
    print("\nDataset salvo como data.csv")

    # Mapeamento de tri para cores
    cores = {0: 'verde', 1: 'amarelo', 2: 'vermelho', 3: 'preto'}

    contagem = Counter(df['tri'])
    print("\nNúmero de vítimas por classificação START:")

    for k in sorted(contagem.keys()):
        print(f"  {k} ({cores[k]}): {contagem[k]}")

    plt.figure(figsize=(8, 5))
    plt.hist(df['sobr'], bins=10, color='skyblue', edgecolor='black', weights=np.ones(n_vitimas) / n_vitimas)
    plt.title('Distribuicao percentual da probabilidade de sobrevivencia')
    plt.xlabel('Probabilidade de Sobrevivencia')
    plt.ylabel('% de Vitimas')
    plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1))
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

    return df

# Exemplo de uso
if __name__ == "__main__":
    gerar_dataset_vitimas(n_vitimas=100, media_idade=35, desvio_idade=7, tipo_acidente='aereo')
