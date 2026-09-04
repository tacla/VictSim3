# Relatório de Correlações (Pearson) com LOWESS

Este relatório apresenta a análise de correlação entre variáveis numéricas usando o **coeficiente de Pearson**.
- O **coeficiente de Pearson (r)** mede a relação linear entre duas variáveis.
- O **LOWESS com comutação automática** desenha uma curva suave para mostrar tendências não-lineares quando a correlação é fraca ou p-valor alto.
- Se a correlação é forte e significativa, usa-se regressão linear para a linha de tendência.


---

## fc × sobr

- r = -0.137, p = 2.58e-43, N = 10000, modo = LOWESS

![fc × sobr](figs/correlacao_fc_sobr.png)


---

## fr × sobr

- r = -0.188, p = 5.26e-80, N = 10000, modo = LOWESS

![fr × sobr](figs/correlacao_fr_sobr.png)


---

## pas × sobr

- r = 0.073, p = 2.88e-13, N = 10000, modo = LOWESS

![pas × sobr](figs/correlacao_pas_sobr.png)


---

## spo2 × sobr

- r = 0.921, p = 0.00e+00, N = 10000, modo = Linear

![spo2 × sobr](figs/correlacao_spo2_sobr.png)


---

## gcs × sobr

- r = 0.990, p = 0.00e+00, N = 10000, modo = Linear

![gcs × sobr](figs/correlacao_gcs_sobr.png)


---
