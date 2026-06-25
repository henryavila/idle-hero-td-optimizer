# Otimizador de Kill Gold para preparar PUSH

Status: segunda otimizacao operacional. Este script aloca os recursos permanentes somente em Kill Gold, usando os custos e fatores reais extraidos do APK.

## Script

```text
../../../../scripts/optimize_gold_push_prep.py
```

A partir da raiz do projeto:

```bash
python3 "Idle Hero TD/scripts/optimize_gold_push_prep.py" --print-template
python3 "Idle Hero TD/scripts/optimize_gold_push_prep.py" --state estado_gold.json --output resultado_gold.json
```

Tambem aceita stdin:

```bash
python3 "Idle Hero TD/scripts/optimize_gold_push_prep.py" --state - < estado_gold.json
```

## Entrada

O JSON de entrada usa o mesmo formato do otimizador de FARM:

```json
{
  "objective": "GOLD_PREP",
  "resources": {
    "energy": "100K",
    "prestige_points": "10M"
  },
  "levels": {
    "researchKillGold1": 0,
    "prestigeKillGold1": 0
  },
  "locked_upgrades": ["prestigeKillGold6"]
}
```

Niveis omitidos viram `0`.

Ao montar estado a partir de OCR, diferencie upgrade maxado de upgrade bloqueado: use `merge_optimizer_states.py --maxed upgrade_key` para maxados e `--locked upgrade_key` para itens ainda indisponiveis por wave/unlock.

Escalas aceitas nos recursos:

- `K` = `1e3`
- `M` = `1e6`
- `B` = `1e9`
- `T` = `1e12`
- notacao cientifica: `1e15`, `2.4e16`, `e15`

Exemplos validos:

```json
{
  "energy": "850K",
  "prestige_points": "1,5B"
}
```

Nota: em valores com escala, virgula e tratada como decimal. Portanto `"1,000M"` significa `1.000M`, nao `1000M`. Para mil milhoes, use `"1B"` ou `"1000M"`.

Para gerar um template completo:

```bash
python3 "Idle Hero TD/scripts/optimize_gold_push_prep.py" --print-template
```

Objetivos aceitos:

- `GOLD_PREP`
- `PUSH_GOLD`
- `KILL_GOLD`

## O que ele otimiza

O score e apenas Kill Gold:

```text
score =
  ln(KillGold_final / KillGold_inicial)
```

Pesos fixos:

```text
Damage = 0
Prestige Power = 0
Kill Gold = 1
```

Portanto, os candidatos possiveis sao somente:

- `researchKillGold1..6`, pagos com `energy`;
- `prestigeKillGold1..7`, pagos com `prestige_points`.

## Quando usar

Use este script quando o objetivo for preparar uma run de PUSH em que o gold extra sera convertido em levels uteis de heroi durante a run.

Este script nao decide se Kill Gold e melhor que Damage para push. Ele responde uma pergunta mais estreita:

```text
Se eu decidi investir so em Gold agora,
qual distribuicao de Research Kill Gold e Prestige Kill Gold maximiza o fator permanente de Kill Gold?
```

## Formulas usadas

Impacto de cada upgrade:

```text
factor(level, q) = 1 + level * q
KillGold = PRODUCT(fatores de Research Kill Gold e Prestige Kill Gold)
```

Custos por nivel:

- Research/Energy: `roundToEven(baseCost * targetLevel ^ multCost)`
- Prestige/PowerUps normal: `BigDouble.Round(baseCost * targetLevel ^ multCost * extraMultiplier)`
- Prestige/PowerUps endgame: `BigDouble.Round(baseCost * multCost ^ (targetLevel - 1) * extraMultiplier)`

Os valores `q`, `baseCost`, `multCost`, `maxLevel` e `override_formula_endgame` vem dos CSVs consolidados:

```text
csv/core_upgrade_formula_factors.csv
csv/core_upgrade_cost_formula_classes.csv
```

## Saida

O JSON de saida contem:

- `purchases`: compras recomendadas, todas de Kill Gold;
- `resources`: gasto e saldo de `energy` e `prestige_points`;
- `factors.kill_gold`: multiplicador inicial, final e delta;
- `final_levels`: niveis finais para copiar para planilha ou nova simulacao;
- `diagnostics.excluded_metrics`: deve listar `damage` e `prestige_power`.

## Relacao com o otimizador de FARM

- FARM estavel: use `optimize_farm_upgrades.py`, com Kill Gold fora por padrao.
- Preparar PUSH com investimento so em gold: use `optimize_gold_push_prep.py`.

O elo estrategico continua condicional:

```text
Kill Gold -> gold extra -> levels uteis de heroi -> DPS efetivo -> wave/tempo de PUSH
```

Este script cobre a primeira parte dessa cadeia: maximizar Kill Gold permanente com os recursos atuais.
