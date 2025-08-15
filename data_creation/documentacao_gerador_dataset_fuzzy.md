# DATASET DE VÍTIMAS

---

## Variáveis geradas

| Variável                 | Descrição                                                   |
|--------------------------|-------------------------------------------------------------|
| idade                   | Idade da vítima (entre 1 e 90 anos)                         |
| fc                      | Frequência cardíaca (bpm)                                   |
| fr                      | Frequência respiratória (rpm)                               |
| pas                     | Pressão arterial sistólica (mmHg)                           |
| spo2                    | Saturação de oxigênio (%)                                   |
| gcs                     | Escala de Coma de Glasgow (3–15)                            |
| avpu                    | Estado de consciência: A, V, P, U (                         |
| temp                    | Temperatura corporal (°C)                                   |
| pr                      | pulso radial: 'S' ou 'N'                                    |
| sg                      | sangramento: 'N': não, 'L': leve, 'M': moderado, 'G': grave |
| fx                      | fratura exposta: 'S' ou 'N'                                 |
| queim                   | queimadura: 'N': não, 'L': leve, 'M': moderado, 'G': grave  |
| tri                     | Classif. START: "verde", "amarelo", "vermelho", "preto"     |
| sobr                    | Prob. de sobrevivência (0 a 1)                              |

APVU: se a vítima está alerta (A), responde a estímulos de voz (V), de dor (P) ou se está inconsciente (U).

---

## Probabilidade de Sobrevivência


| Classificação START | Faixa fuzzy da probabilidade de sobrevivência |
|---------------------|-----------------------------------------------|
| Verde               | [0.93 – 1.00]                                 |
| Amarelo             | [0.75 – 0.95]                                 |
| Vermelho            | [0.15 – 0.80]                                 |
| Preto               | [0.00 – 0.25]                                 |


---

