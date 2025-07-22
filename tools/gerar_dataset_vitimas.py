
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from collections import Counter

def gerar_dataset_vitimas(n_vitimas=100, media_idade=35, desvio_idade=7, tipo_acidente="aéreo"):
    np.random.seed(42)
    random.seed(42)

    distribuicoes_por_tipo = {
        'aéreo': {'verde': 0.2, 'amarelo': 0.3, 'vermelho': 0.4, 'preto': 0.1},
        'rodoviário': {'verde': 0.4, 'amarelo': 0.3, 'vermelho': 0.2, 'preto': 0.1},
        'ferroviário': {'verde': 0.3, 'amarelo': 0.3, 'vermelho': 0.3, 'preto': 0.1},
        'deslizamento': {'verde': 0.25, 'amarelo': 0.25, 'vermelho': 0.3, 'preto': 0.2}
    }

    triagem_parametros = {
        'verde': {
            'fc': (60, 100), 'fr': (12, 20), 'pas': (110, 130), 'spo2': (96, 100),
            'gcs': (15, 15), 'avpu': ['A'], 'temp': (36.5, 37.4), 'pulso': ['sim'],
            'sangramento': ['nao'], 'fratura': ['nao'], 'queimadura': ['nenhuma'],
            'prob_sobrevivencia': (0.95, 1.00)
        },
        'amarelo': {
            'fc': (100, 120), 'fr': (20, 30), 'pas': (90, 110), 'spo2': (90, 95),
            'gcs': (13, 14), 'avpu': ['A', 'V'], 'temp': (37.0, 38.5), 'pulso': ['sim', 'nao'],
            'sangramento': ['leve', 'moderado'], 'fratura': ['nao', 'sim'],
            'queimadura': ['nenhuma'] * 85 + ['leve'] * 10 + ['moderada'] * 5,
            'prob_sobrevivencia': (0.75, 0.94)
        },
        'vermelho': {
            'fc': (121, 160), 'fr': (31, 45), 'pas': (60, 89), 'spo2': (75, 89),
            'gcs': (9, 12), 'avpu': ['D'], 'temp': (34.0, 35.0), 'pulso': ['nao'],
            'sangramento': ['grave'], 'fratura': ['sim'],
            'queimadura': ['nenhuma'] * 40 + ['moderada'] * 30 + ['grave'] * 30,
            'prob_sobrevivencia': (0.20, 0.74)
        },
        'preto': {
            'fc': (0, 0), 'fr': (0, 0), 'pas': (0, 0), 'spo2': (0, 74),
            'gcs': (3, 6), 'avpu': ['U'], 'temp': (25.0, 34.0), 'pulso': ['nao'],
            'sangramento': ['grave'], 'fratura': ['sim', 'nao'],
            'queimadura': ['nenhuma'] * 50 + ['grave'] * 50,
            'prob_sobrevivencia': (0.00, 0.19)
        }
    }

    distrib = distribuicoes_por_tipo[tipo_acidente]
    classificacoes = np.random.choice(
        list(distrib.keys()),
        size=n_vitimas,
        p=list(distrib.values())
    )

    idades = np.clip(np.random.normal(media_idade, desvio_idade, n_vitimas), 1, 90).astype(int)

    dados = []
    for i in range(n_vitimas):
        classe = classificacoes[i]
        idade = idades[i]
        params = triagem_parametros[classe]
        gcs_range = params['gcs']
        gcs_value = gcs_range[0] if gcs_range[0] == gcs_range[1] else np.random.randint(*gcs_range)

        registro = {
            'idade': idade,
            'fc': np.random.randint(*params['fc']) if params['fc'] != (0, 0) else 0,
            'fr': np.random.randint(*params['fr']) if params['fr'] != (0, 0) else 0,
            'pas': np.random.randint(*params['pas']) if params['pas'] != (0, 0) else 0,
            'spo2': np.random.randint(*params['spo2']),
            'gcs': gcs_value,
            'avpu': random.choice(params['avpu']),
            'temperatura': round(np.random.uniform(*params['temp']), 1),
            'pulso_radial': random.choice(params['pulso']),
            'sangramento': random.choice(params['sangramento']),
            'fratura_exposta': random.choice(params['fratura']),
            'queimadura': random.choice(params['queimadura']),
            'classificacao_triagem': classe,
            'probabilidade_sobrevivencia': round(np.random.uniform(*params['prob_sobrevivencia']), 2)
        }
        dados.append(registro)

    df = pd.DataFrame(dados)

    contagem = Counter(df['classificacao_triagem'])
    print("\nNúmero de vítimas por classificação START:")
    for k, v in contagem.items():
        print(f"  {k.capitalize()}: {v}")

    plt.figure(figsize=(8, 5))
    plt.hist(df['probabilidade_sobrevivencia'], bins=10, color='skyblue', edgecolor='black', weights=np.ones(n_vitimas) / n_vitimas)
    plt.title('Distribuição percentual da probabilidade de sobrevivência')
    plt.xlabel('Probabilidade de Sobrevivência')
    plt.ylabel('% de Vítimas')
    plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1))
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

        df.to_csv("dataset_vitimas.csv", index=False)
    print("\nDataset salvo como dataset_vitimas.csv")
    return df

# Exemplo de uso
if __name__ == "__main__":
    gerar_dataset_vitimas(n_vitimas=100, media_idade=35, desvio_idade=7, tipo_acidente='aéreo')
