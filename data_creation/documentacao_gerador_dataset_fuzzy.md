# DATASET DE VÍTIMAS

---

## Variáveis geradas

| Variável                 | Descrição                                                   |
|--------------------------|-------------------------------------------------------------|
| idade                   | Idade da vítima (entre 1 e 90 anos)                         |
| fc                      | Frequência cardíaca (bpm) de 0 a 160                        |
| fr                      | Frequência respiratória (rpm) de 0 a 45                     |
| pas                     | Pressão arterial sistólica (mmHg)                           |
| spo2                    | Saturação de oxigênio (%)   de 0 a 100                      |
| gcs                     | Escala de Coma de Glasgow (3–15)                            |
| avpu                    | Estado de consciência: A, V, P, U (Alerta, Voz, Pain (dor), inconsciente |
| temp                    | Temperatura corporal (°C)  de 0 a 38.5                      |
| pr                      | pulso radial: 'S' ou 'N'                                    |
| sg                      | sangramento: 'N': não, 'L': leve, 'M': moderado, 'G': grave |
| fx                      | fratura exposta: 'S' ou 'N'                                 |
| queim                   | queimadura: 'N': não, 'L': leve, 'M': moderado, 'G': grave  |
| tri                     | Triagem classif. START: "verde", "amarelo", "vermelho", "Ppreto" |
| sobr                    | Prob. de sobrevivência (0 a 1)  contínuo                    |

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

