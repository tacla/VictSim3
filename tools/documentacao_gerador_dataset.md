# Documentação do Script: gerador_dataset_vitimas.py

Este script gera um dataset sintético de vítimas de grandes acidentes (aéreos, rodoviários, ferroviários, ou deslizamentos de terra),
com dados clínicos simulados para tarefas de aprendizado de máquina supervisionado — incluindo classificação (START) e regressão
(probabilidade de sobrevivência).

---

## Parâmetros de entrada da função principal

```python
gerar_dataset_vitimas(n_vitimas=100, media_idade=35, desvio_idade=7, tipo_acidente='aéreo')
```

- `n_vitimas`: número total de vítimas a serem geradas.
- `media_idade`: média da distribuição normal de idades.
- `desvio_idade`: desvio padrão da idade.
- `tipo_acidente`: tipo do acidente (aceita: 'aéreo', 'rodoviário', 'ferroviário', 'deslizamento').

---

## Variáveis geradas (colunas do dataset)

| Variável               | Descrição                                               | Tipo       |
|------------------------|---------------------------------------------------------|------------|
| `idade`                | Idade da vítima (1 a 90 anos)                           | int        |
| `fc`                   | Frequência cardíaca (batimentos por minuto)             | int        |
| `fr`                   | Frequência respiratória (respirações por minuto)        | int        |
| `pas`                  | Pressão arterial sistólica (mmHg)                       | int        |
| `spo2`                 | Saturação de oxigênio no sangue (%)                     | int        |
| `gcs`                  | Escala de Coma de Glasgow (3 a 15)                      | int        |
| `avpu`                 | Nível de consciência: A=Alerta, V=Voz, D=Dor, U=Inconsciente | str    |
| `temperatura`          | Temperatura corporal em graus Celsius                   | float      |
| `pulso_radial`         | Pulso radial detectável: 'sim' ou 'não'                 | str        |
| `sangramento`          | Gravidade do sangramento: 'não', 'leve', 'moderado', 'grave' | str    |
| `fratura_exposta`      | Presença de fratura exposta: 'sim' ou 'não'             | str        |
| `queimadura`           | Grau de queimadura: 'nenhuma', 'leve', 'moderada', 'grave' | str    |
| `classificacao_triagem`| Classificação START: 'verde', 'amarelo', 'vermelho', 'preto' | str     |
| `probabilidade_sobrevivencia` | Valor contínuo entre 0 e 1                        | float      |

---

## Lógica de Cálculo da Classificação START

A classificação START é determinada **aleatoriamente com base em distribuições típicas por tipo de acidente**, mas cada classe define:

- Intervalos realistas de sinais vitais e condições clínicas
- Associação com risco à vida, consciência e perfusão

Distribuições por tipo de acidente:
- Aéreo: mais vítimas vermelhas
- Rodoviário: maioria verde ou amarela
- Ferroviário e deslizamento: equilíbrio entre classes

A lógica da START no script segue os critérios:

| Classificação | Critério típico (START simplificado)                                  |
|---------------|------------------------------------------------------------------------|
| Verde         | Anda, sinais vitais normais, consciente                                |
| Amarelo       | Lesões moderadas, sem risco imediato à vida                            |
| Vermelho      | FR >30 ou <10, PA <90, pulso ausente, GCS <13, inconsciência parcial   |
| Preto         | Sem respiração, GCS <6, inconsciência total, sem chance de recuperação |

---

## Lógica de Geração da Probabilidade de Sobrevivência

A variável `probabilidade_sobrevivencia` é um valor contínuo entre 0 e 1, gerado de forma randômica dentro de faixas típicas por classe START:

| Classificação START | Faixa de probabilidade de sobrevivência |
|---------------------|------------------------------------------|
| Verde               | 0.95 – 1.00                              |
| Amarelo             | 0.75 – 0.94                              |
| Vermelho            | 0.20 – 0.74                              |
| Preto               | 0.00 – 0.19                              |

Essa variável permite usar o dataset também para modelos de **regressão preditiva de risco de óbito**.

---

## Saída Gráfica

Ao final da execução, o script exibe:
- A contagem de vítimas por classificação
- Um histograma percentual da `probabilidade_sobrevivencia` no conjunto gerado

---