"""
=====================================================================
Gerador de resumo estatístico de CSV em formato Markdown
=====================================================================

Funcionalidade:
---------------
lê um arquivo CSV contendo dados de vítimas e gera um arquivo de saída em formato Markdown (.md)
com o resumo estatístico dos atributos:

1. Mostra o número total de linhas do CSV.
2. Para colunas numéricas conhecidas:
   - Mínimo
   - Máximo
   - Média
3. Para colunas categóricas conhecidas:
   - Contagem absoluta e percentual de cada valor esperado (mesmo que seja 0)
   - Contagem e percentual de valores ausentes (<NA>)
   - Contagem e percentual de valores inesperados (fora do domínio)

Como usar:
----------
1. Modifique a variável `BASE_FOLDER` para apontar para a pasta onde está
   o seu arquivo CSV.
2. Modifique a variável `INPUT_CSV` para indicar o nome do arquivo CSV
   (por exemplo: `"data.csv"`).
3. Execute o script em um ambiente com Python 3 e pandas instalado:

       python nome_do_arquivo.py

4. O arquivo de saída (`summary.md`) será gerado na mesma pasta definida
   em `BASE_FOLDER`.

=====================================================================
"""


from pathlib import Path
import pandas as pd
import numpy as np

# === Configurações fixas ===
BASE_FOLDER = Path("../datasets/vict/100v")
INPUT_CSV   = BASE_FOLDER / "data.csv"
OUTPUT_MD   = BASE_FOLDER / "summary.md"

# Esquema conhecido (ordem preservada nos conjuntos)
CAT_DOMAINS = {

    "pr":    ["S", "N"],
    "queim": ["N", "L", "M", "G"],
    "fx":    ["S", "N"],
    "sg":    ["N", "L", "M", "G"],
    "avpu":  ["A", "V", "P", "U"],
    "tri":   ["verde", "amarelo", "vermelho", "preto"],  
}

NUM_INT_COLS   = ["idade", "fc", "fr", "pas", "spo2", "gcs"]
NUM_FLOAT_COLS = ["sobr"]  # [0,1]

def read_and_cast(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8")

    # Converte numéricos conhecidos
    for c in NUM_INT_COLS:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").astype("Int64")
    for c in NUM_FLOAT_COLS:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Normaliza categóricos (tri minúsculas; demais maiúsculas)
    for c, _ in CAT_DOMAINS.items():
        if c in df.columns:
            s = df[c].astype("string").str.strip()
            df[c] = s.str.lower() if c == "tri" else s.str.upper()
    return df

def numeric_section(df: pd.DataFrame) -> str:
    lines = []
    cols = [c for c in NUM_INT_COLS + NUM_FLOAT_COLS if c in df.columns]
    if not cols:
        return ""

    rows = []
    for c in cols:
        s = pd.to_numeric(df[c], errors="coerce").dropna()
        if s.empty:
            rows.append((c, np.nan, np.nan, np.nan))
        else:
            rows.append((c, s.min(), s.max(), s.mean()))
    out = pd.DataFrame(rows, columns=["coluna", "mín", "máx", "média"])

    # formata
    fmtd = out.copy()
    for col in ["mín", "máx", "média"]:
        fmtd[col] = fmtd[col].map(
            lambda x: "" if pd.isna(x) else (
                f"{x:.3f}" if isinstance(x, float) and not x.is_integer() else f"{int(x)}"
            )
        )

    lines.append("## Estatísticas (numéricas)")
    lines.append(fmtd.to_markdown(index=False))
    lines.append("")
    return "\n".join(lines)

def _fmt_pct(x: int, total: int) -> str:
    return f"{(100.0 * x / total):.2f}%" if total > 0 else "0.00%"

def categorical_section(df: pd.DataFrame) -> str:
    lines = []
    present_cats = [c for c in CAT_DOMAINS if c in df.columns]
    if not present_cats:
        return ""

    total_rows = len(df)
    lines.append("## Contagem por valor (categóricas)")
    for c in present_cats:
        domain = CAT_DOMAINS[c]  # ordem preservada
        s = df[c]
        vc = s.value_counts(dropna=False)  # inclui NaN

        # Tabela principal: todos valores do domínio (ordem fixa)
        expected_rows = []
        for val in domain:
            cnt = int(vc.get(val, 0))
            expected_rows.append((val, cnt, _fmt_pct(cnt, total_rows)))
        expected_df = pd.DataFrame(expected_rows, columns=["valor", "contagem", "%"])

        lines.append(f"### `{c}`")
        lines.append(expected_df.to_markdown(index=False))

        # Ausentes
        na_cnt = int(s.isna().sum())
        if na_cnt > 0:
            lines.append("")
            lines.append("> **Ausentes**")
            na_df = pd.DataFrame(
                [("<NA>", na_cnt, _fmt_pct(na_cnt, total_rows))],
                columns=["valor", "contagem", "%"]
            )
            lines.append(na_df.to_markdown(index=False))

        # Inesperados
        unexpected_items = [(k, int(v)) for k, v in vc.items()
                            if pd.notna(k) and k not in domain]
        if unexpected_items:
            rows_u = [(k, v, _fmt_pct(v, total_rows)) for k, v in unexpected_items]
            u_df = pd.DataFrame(rows_u, columns=["valor", "contagem", "%"])
            lines.append("")
            lines.append("> **Valores inesperados** (fora do domínio esperado)")
            lines.append(u_df.to_markdown(index=False))

        lines.append("")
    return "\n".join(lines)

def main():
    if not INPUT_CSV.exists():
        raise SystemExit(f"Arquivo não encontrado: {INPUT_CSV}")

    df = read_and_cast(INPUT_CSV)

    lines = [
        "# Resumo do CSV\n",
        f"- **Arquivo**: `{INPUT_CSV.name}`",
        f"- **Número de linhas**: {len(df)}\n",
        numeric_section(df),
        categorical_section(df),
    ]

    md = "\n".join([blk for blk in lines if blk])
    OUTPUT_MD.write_text(md, encoding="utf-8")
    print(f"OK: relatório gerado em {OUTPUT_MD}")

if __name__ == "__main__":
    main()

