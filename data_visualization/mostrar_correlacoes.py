
"""
=====================================================================
Correlação (Pearson) com comutação automática para LOWESS
=====================================================================

O script:
1) Lê o dataset de sinais vitais (vars. BASE_FOLDER e INPUT_CSV)
2) Para cada par (fc, fr, pas, spo2, gcs) × (sobr):
   - Calcula r e p (Pearson)
   - Se p >= 0.05 ou |r| < 0.8 → plota DISPERSÃO com LOWESS
   - Caso contrário → regressão linear
3) Salva PNGs individuais e um PNG com todos os gráficos.

Dependências: pandas, numpy, matplotlib, seaborn
LOWESS: requer statsmodels (opcional; se ausente, cai em fallback sem linha)
=====================================================================
"""

from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import numpy as np

# Configuração de paths
BASE_FOLDER   = Path("../../datasetS/vict/100v")
INPUT_CSV     = BASE_FOLDER / "data.csv"
OUTPUT_FOLDER = BASE_FOLDER / "correlacoes"

# Pares de variáveis
VAR_PAIRS = [
    ("fc", "sobr"),
    ("fr", "sobr"),
    ("pas", "sobr"),
    ("spo2", "sobr"),
    ("gcs", "sobr"),
]

ALPHA = 0.05
R_THRESHOLD = 0.8  # min para mostrar regressão linear

def fmt_p(p):
    if np.isnan(p):
        return "na"
    return f"{p:.2e}" if p < 0.001 else f"{p:.3f}"

def safe_pearson(x, y):
    x = pd.to_numeric(pd.Series(x), errors="coerce")
    y = pd.to_numeric(pd.Series(y), errors="coerce")
    mask = x.notna() & y.notna()
    x, y = x[mask], y[mask]
    n = len(x)
    if n < 3 or x.nunique() < 2 or y.nunique() < 2:
        return np.nan, np.nan, n
    r, p = pearsonr(x, y)
    return r, p, n

def should_use_lowess(r, p, alpha=ALPHA, r_thresh=R_THRESHOLD):
    if np.isnan(r) or np.isnan(p):
        return True  # sem base para linear
    return (p >= alpha) or (abs(r) < r_thresh)

def annotate(ax, r, p, n, mode):
    ax.text(
        0.03, 0.97, f"r = {r:.3f}\np = {fmt_p(p)}\nN = {n}\nmode = {mode}",
        transform=ax.transAxes, va="top", ha="left", fontsize=10,
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="gray", alpha=0.75)
    )

def regplot_auto(ax, data, x, y, use_lowess):
    """
    Plota scatter + linha:
      - use_lowess=True  -> LOWESS (se disponível)
      - use_lowess=False -> regressão linear
    Se LOWESS não disponível, faz fallback para scatter sem linha.
    """
    scatter_kws = {"alpha": 0.6}
    line_kws = {"color": "red"}

    if use_lowess:
        try:
            # LOWESS via seaborn (requer statsmodels instalado)
            sns.regplot(x=x, y=y, data=data, ax=ax, lowess=True,
                        scatter_kws=scatter_kws, line_kws=line_kws)
            return "LOWESS"
        except Exception:
            # Fallback: apenas scatter
            sns.scatterplot(x=x, y=y, data=data, ax=ax, alpha=0.6)
            return "LOWESS (indisp.)"
    else:
        sns.regplot(x=x, y=y, data=data, ax=ax, lowess=False,
                    scatter_kws=scatter_kws, line_kws=line_kws)
        return "Linear"

def main():
    if not INPUT_CSV.exists():
        raise SystemExit(f"Arquivo não encontrado: {INPUT_CSV}")

    df = pd.read_csv(INPUT_CSV, encoding="utf-8")
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    # Figura geral (2x3)
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    axes = axes.flatten()

    for i, (x, y) in enumerate(VAR_PAIRS):
        if x not in df.columns or y not in df.columns:
            print(f"Colunas {x} ou {y} não encontradas.")
            continue

        data = df[[x, y]].dropna()
        r, p, n = safe_pearson(data[x], data[y])
        use_low = should_use_lowess(r, p)

        # Painel na grade
        ax = axes[i]
        mode = regplot_auto(ax, data, x, y, use_low)
        annotate(ax, r, p, n, mode)
        ax.set_title(f"{x} × {y}")
        ax.grid(True, linestyle="--", alpha=0.6)

        # PNG individual
        fig_ind, ax_ind = plt.subplots(figsize=(6, 4))
        mode_ind = regplot_auto(ax_ind, data, x, y, use_low)
        annotate(ax_ind, r, p, n, mode_ind)
        ax_ind.set_title(f"Correlação {x} × {y}")
        ax_ind.grid(True, linestyle="--", alpha=0.6)
        fig_ind.tight_layout()
        fig_ind.savefig(OUTPUT_FOLDER / f"correlacao_{x}_{y}.png", dpi=150)
        plt.close(fig_ind)

    # Remove eixos vazios (se houver)
    for j in range(len(VAR_PAIRS), len(axes)):
        fig.delaxes(axes[j])

    fig.tight_layout()
    fig.savefig(OUTPUT_FOLDER / "correlacoes_todas.png", dpi=150)
    plt.show()

if __name__ == "__main__":
    main()
