# AVPU × SOBR

- **Arquivo**: `data.csv`
- **Linhas válidas p/ análise**: 100

- **Eta (razão de correlação)**: 0.8910

  Eta mede quanto da variabilidade total de uma variável numérica pode ser explicada por uma variável categórica.

  Valores próximos de 0 indicam associação fraca e quanto mais próximos de 1, mais forte.
- **ANOVA**: F=123.2839, p=8.329e-33

  Mede se as médias da variável numérica são significativamente diferentes para os valores da variável categórica.

  p < 0,05 → rejeita-se H₀ → existe diferença estatisticamente significativa entre as médias.

  p ≥ 0,05 → não há evidência suficiente para rejeitar H₀ → médias podem ser consideradas estatisticamente iguais.

## Estatísticas por categoria
| avpu   |   N |   mean |   std |   ci95_lo |   ci95_hi |
|:-------|----:|-------:|------:|----------:|----------:|
| A      |  38 |  0.935 | 0.066 |     0.914 |     0.957 |
| V      |  15 |  0.83  | 0.068 |     0.793 |     0.867 |
| P      |  38 |  0.46  | 0.209 |     0.391 |     0.529 |
| U      |   9 |  0.139 | 0.074 |     0.082 |     0.195 |

## Gráficos
![Boxplot e dispersão](figs/avpu_sobr_box_scatter.png)
![Médias com IC95%](figs/avpu_sobr_means_ci.png)
