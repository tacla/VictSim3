# DATASET DE VÍTIMAS

---

## Variáveis geradas

| Variável                 | Descrição                                                   |
|--------------------------|-------------------------------------------------------------|
|  1 idade                   | Idade da vítima (entre 1 e 90 anos)                         |
|  2 fc                      | Frequência cardíaca (bpm) de 0 a 160                        |
|  3 fr                      | Frequência respiratória (rpm) de 0 a 45                     |
|  4 pas                     | Pressão arterial sistólica (mmHg)                           |
|  5 spo2                    | Saturação de oxigênio (%)   de 0 a 100                      |
|  6 gcs                     | [Escala de Coma de Glasgow (3–15)](https://pt.wikipedia.org/wiki/Escala_de_coma_de_Glasgow) |
|  7 avpu                    | Estado de consciência: A, V, P, U (Alerta, Voz, Pain (dor), inconsciente |
|  8 temp                    | Temperatura corporal (°C)  de 0 a 38.5                      |
|  9 pr                      | pulso radial: 'S' ou 'N'                                    |
| 10 sg                      | sangramento: 'N': não, 'L': leve, 'M': moderado, 'G': grave |
| 11 fx                      | fratura exposta: 'S' ou 'N'                                 |
| 12 queim                   | queimadura: 'N': não, 'L': leve, 'M': moderado, 'G': grave  |
| 13 tri                     | Triagem classif. START: "verde", "amarelo", "vermelho", "Ppreto" |
| 14 sobr                    | Prob. de sobrevivência (0 a 1)  contínuo                    |

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

