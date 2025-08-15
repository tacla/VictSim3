# DATASET DE VÍTIMAS

---

## Variáveis geradas

| Seq|Variável  | Descrição                                             | Tipo   |
|----|----------|-------------------------------------------------------|--------|
|  1 | idade    | Idade da vítima (entre 1 e 90 anos)                   | INT    |
|  2 | fc       | Frequência cardíaca (bpm) de 0 a 160                  | INT    |
|  3 | fr       | Frequência respiratória (rpm) de 0 a 45               | INT    |
|  4 | pas      | Pressão arterial sistólica (mmHg)                     | INT    |                  
|  5 | spo2     | Saturação de oxigênio (%)   de 0 a 100                | INT    |     
|  6 | temp     | Temperatura corporal (°C)  de 0 a 38.5                | FLOAT  |
|  7 | pr       | pulso radial: 'S' ou 'N'                              | CAT    |
|  8 | sg       | sangramento: 'N': não, 'L': leve, 'M': moderado, 'G': grave | CAT |
|  9 | fx       | fratura exposta: 'S' ou 'N'                                 | CAT |
| 10 | queim    | queimadura: 'N': não, 'L': leve, 'M': moderado, 'G': grave  | CAT |
| 11 | gcs      | [Escala de Coma de Glasgow (3–15)](https://pt.wikipedia.org/wiki/Escala_de_coma_de_Glasgow) |   INT |
| 12 | avpu     | Estado de consciência: A, V, P, U (Alerta, Voz, Pain (dor), inconsciente | CAT |
| 13 | tri      | Triagem classif. START: "verde", "amarelo", "vermelho", "preto" | CAT |
| 14 | sobr     | Prob. de sobrevivência (0 a 1)  REAL                    | FLOAT |

<small>
APVU: se a vítima está alerta (A), responde a estímulos de voz (V), de dor (P) ou se está inconsciente (U).

GCS: de 3 a 15, quanto menor o valor, menos grave a situação da vítima 
[Ver escala](https://pt.wikipedia.org/wiki/Escala_de_coma_de_Glasgow#/media/Ficheiro:Escala_de_Coma_de_Glasgow_-_ECG.png)
</small>
---

## Probabilidade de Sobrevivência


| Classificação START | Faixa de probabilidade de sobrevivência |
|---------------------|-----------------------------------------|
| Verde               | [0.93 – 1.00]                           |
| Amarelo             | [0.75 – 0.95]                           |
| Vermelho            | [0.15 – 0.80]                           |
| Preto               | [0.00 – 0.25]                           |


---

