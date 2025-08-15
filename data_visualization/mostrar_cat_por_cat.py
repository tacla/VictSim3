
"""
Análise genérica de associação entre duas variáveis categóricas

- Lê sinais vitais das vítimas (data.csv)
- Para cada par (x, y) em PAIRS:
  * Tabela de contingência (absoluta)
  * Tabela de proporções por linha (%)
  * Heatmap (Y invertido se y for 'avpu': A, V, P, U de baixo para cima)
  * Barras empilhadas (cores de TRI fixas: verde=green, amarelo=yellow, vermelho=red, preto=black)
  * Teste Qui-quadrado e Cramér’s V
  * Relatório Markdown com tabelas e métricas

Edite PAIRS abaixo para os pares desejados.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

# === Caminhos ===
BASE   = Path("../../datasets/vict/100v")
INPUT  = BASE / "data.csv"
OUTDIR = BASE

# === Pares a analisar (edite aqui) ===
PAIRS = [
    ("avpu", "tri"),    # AVPU x START
    ("queim", "tri"),   # queimados x tri
    ("sg", "tri"),      # sangramento x tri
    ("fx", "tri"),      # fratura exposta
    ("gcs", "tri"),     # Glasgow comma scale
    
]

# === Ordens conhecidas (opcionalmente extendível) ===
ORDER_MAP = {
    "avpu": ["A", "V", "P", "U"],
    "tri":  ["verde", "amarelo", "vermelho", "preto"],
}

# === Cores fixas para 'tri' na ordem acima ===
COLOR_MAP_TRI = {
    "verde": "green",
    "amarelo": "yellow",
    "vermelho": "red",
    "preto": "black"
}

def normalize_series(name: str, s: pd.Series) -> pd.Series:
    """Normaliza conteúdo textual por variável conhecida."""
    s = s.astype("string").str.strip()
    if name.lower() == "avpu":
        return s.str.upper()
    if name.lower() == "tri":
        return s.str.lower()
    return s

def apply_order(name: str, s: pd.Series) -> pd.Series:
    """Aplica ordem conhecida, se houver; senão, usa ordem dos valores únicos (classificada)."""
    key = name.lower()
    if key in ORDER_MAP:
        cats = ORDER_MAP[key]
        return pd.Categorical(s, categories=cats, ordered=True)
    # ordem inferida:
    cats = sorted(pd.Series(s).dropna().unique(), key=lambda x: str(x))
    return pd.Categorical(s, categories=cats, ordered=True)

def cramers_v(tab: pd.DataFrame) -> float:
    """Cramér’s V a partir de uma tabela de contingência pandas."""
    chi2, _, _, _ = chi2_contingency(tab)
    n = tab.to_numpy().sum()
    return np.sqrt(chi2 / (n * (min(tab.shape) - 1))) if n > 0 else np.nan

def plot_heatmap(tab_abs: pd.DataFrame, x_name: str, y_name: str, out_path: Path):
    """
    Heatmap com Y invertido se o eixo Y for 'avpu' (mostrando A,V,P,U de baixo para cima).
    y_name é a variável das linhas (index) da tabela.
    """
    tab = tab_abs.copy()

    # reordena linhas (Y) para AVPU invertido (baixo->cima: A,V,P,U)
    if y_name.lower() == "avpu" and "avpu" in ORDER_MAP:
        order_y = ORDER_MAP["avpu"][::-1]  # invertido
        tab = tab.reindex(index=[lvl for lvl in order_y if lvl in tab.index], fill_value=0)

    plt.figure(figsize=(8, 5))
    ax = sns.heatmap(tab, annot=True, fmt="d", cmap="Blues", cbar_kws={'label': 'Frequência'})
    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name.upper() if y_name.lower() == "avpu" else y_name)
    plt.title(f"Frequências {y_name} × {x_name}")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()

def plot_stacked_bars(tab_pct: pd.DataFrame, x_name: str, y_name: str, out_path: Path):
    """
    Barras empilhadas (% por linha) — linhas são y, colunas são x.
    Cores fixas para 'tri' se a variável das colunas for 'tri'.
    """
    colors = None
    # Se as colunas representarem TRI, impõe paleta fixa na ordem ORDER_MAP['tri']
    if x_name.lower() == "tri" and "tri" in ORDER_MAP:
        cols_order = [c for c in ORDER_MAP["tri"] if c in tab_pct.columns]
        tab_plot = tab_pct[cols_order].copy()
        colors = [COLOR_MAP_TRI[c] for c in cols_order]
    else:
        tab_plot = tab_pct.copy()

    ax = tab_plot.plot(kind="bar", stacked=True, figsize=(8, 5), color=colors)
    ax.set_ylabel("% por " + y_name)
    ax.set_xlabel(y_name)
    ax.set_title(f"Proporção de {x_name} por {y_name}")
    # legenda
    ax.legend(title=x_name, bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()

def analyze_pair(df: pd.DataFrame, x: str, y: str):
    """
    Analisa (y linhas) × (x colunas).
    - Normaliza conteúdo
    - Aplica ordem (se conhecida)
    - Gera tabelas, gráficos e resumo
    """
    subdir = OUTDIR / f"{x}_{y}"
    subdir.mkdir(parents=True, exist_ok=True)

    sx = normalize_series(x, df[x])
    sy = normalize_series(y, df[y])

    # filtra apenas categorias não-nulas
    mask = sy.notna() & sx.notna()
    sx, sy = sx[mask], sy[mask]

    # aplica ordens
    sy = apply_order(y, sy)  # linhas
    sx = apply_order(x, sx)  # colunas

    df_ok = pd.DataFrame({y: sy, x: sx}).dropna()

    # tabelas
    tab_abs = pd.crosstab(df_ok[y], df_ok[x])
    tab_pct = pd.crosstab(df_ok[y], df_ok[x], normalize="index") * 100

    # métricas
    chi2, p_val, dof, expected = chi2_contingency(tab_abs) if tab_abs.shape[0] > 0 and tab_abs.shape[1] > 0 else (np.nan, np.nan, np.nan, None)
    cv = cramers_v(tab_abs) if tab_abs.size > 0 else np.nan

    # gráficos
    plot_heatmap(tab_abs, x_name=x, y_name=y, out_path=subdir / f"{x}_{y}_heatmap.png")
    plot_stacked_bars(tab_pct, x_name=x, y_name=y, out_path=subdir / f"{x}_{y}_barras_empilhadas.png")

    # markdown
    lines = []
    lines.append(f"# Análise {y} × {x}\n")
    lines.append(f"- **Arquivo**: `{INPUT.name}`")
    lines.append(f"- **Total de registros analisados**: {len(df_ok)}\n")
    lines.append("## Tabela de contingência (absoluta)")
    lines.append(tab_abs.to_markdown())
    lines.append("\n## Tabela de proporções por linha (%)")
    lines.append(tab_pct.round(2).to_markdown())
    lines.append("\n## Medidas de associação")
    lines.append(f"- **Qui-quadrado**: χ² = {chi2:.4f}" if not np.isnan(chi2) else "- **Qui-quadrado**: n/d")
    lines.append(f"- **gl**: {dof}" if not np.isnan(dof) else "- **gl**: n/d")
    lines.append(f"- **p-valor**: {p_val:.4g}" if not np.isnan(p_val) else "- **p-valor**: n/d")
    lines.append(f"- **Cramér's V**: {cv:.4f}" if not np.isnan(cv) else "- **Cramér's V**: n/d")
    lines.append("\n## Gráficos gerados")
    lines.append(f"- `{x}_{y}_heatmap.png`")
    lines.append(f"- `{x}_{y}_barras_empilhadas.png`")
    (subdir / f"readme.md").write_text("\n".join(lines), encoding="utf-8")

    print(f"OK: {x}_{y} → resultados em {subdir}")

def main():
    if not INPUT.exists():
        raise SystemExit(f"Arquivo não encontrado: {INPUT}")

    df = pd.read_csv(INPUT, encoding="utf-8")

    # checagem rápida de existência de colunas
    missing_pairs = [(x, y) for x, y in PAIRS if x not in df.columns or y not in df.columns]
    if missing_pairs:
        for x, y in missing_pairs:
            print(f"Colunas ausentes para o par ({x}, {y})")
    pairs_ok = [(x, y) for x, y in PAIRS if x in df.columns and y in df.columns]
    if not pairs_ok:
        raise SystemExit("Nenhum par válido encontrado em PAIRS.")

    OUTDIR.mkdir(parents=True, exist_ok=True)

    for x, y in pairs_ok:
        analyze_pair(df, x, y)

if __name__ == "__main__":
    main()
