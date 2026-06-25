# Otimizador de upgrades para FARM

Status: ferramenta operacional criada sobre os dados reais extraidos do APK. O script usa os CSVs consolidados de fator e custo, nao os valores arredondados da UI.

## Script

```text
../../../../scripts/optimize_farm_upgrades.py
```

A partir da raiz do projeto:

```bash
python3 "Idle Hero TD/scripts/optimize_farm_upgrades.py" --print-template
python3 "Idle Hero TD/scripts/optimize_farm_upgrades.py" --state estado_farm.json --output resultado_farm.json
```

Tambem aceita stdin:

```bash
python3 "Idle Hero TD/scripts/optimize_farm_upgrades.py" --state - < estado_farm.json
```

## Entrada

O JSON de entrada tem tres partes:

```json
{
  "objective": "FARM",
  "resources": {
    "energy": "100K",
    "prestige_points": "10M"
  },
  "levels": {
    "researchDmg1": 0,
    "researchPrestigePower1": 0,
    "prestigeDmg1": 0
  },
  "locked_upgrades": ["prestigeDmg5"],
  "farm": {
    "damage_effective": true,
    "prestige_power_effective": true,
    "include_gold": false,
    "weights": {
      "damage": 1.0,
      "prestige_power": 1.0,
      "kill_gold": 0.0
    }
  }
}
```

Niveis omitidos viram `0`. Recursos aceitos:

- `energy`
- `prestige_points` ou `prestige`

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
  "prestige_points": "1.25B"
}
```

Tambem aceita virgula decimal em valores com escala, como `"1,5B"`.

Nota: em valores com escala, virgula e tratada como decimal. Portanto `"1,000M"` significa `1.000M`, nao `1000M`. Para mil milhoes, use `"1B"` ou `"1000M"`.

Para gerar um template completo com todos os upgrades:

```bash
python3 "Idle Hero TD/scripts/optimize_farm_upgrades.py" --print-template
```

Omitido no print nao significa sempre `0`. Quando montar o estado a partir de OCR:

- upgrade maxado: coloque o level maximo, ou use `merge_optimizer_states.py --maxed upgrade_key`;
- upgrade bloqueado por wave: coloque em `locked_upgrades`, ou use `merge_optimizer_states.py --locked upgrade_key`;
- upgrade visivel/compravel: use o level lido.

Upgrades em `locked_upgrades` ficam excluidos das compras candidatas.

## Objetivo FARM

Por padrao, FARM maximiza:

```text
score =
  1.0 * ln(Damage_final / Damage_inicial)
  + 1.0 * ln(PrestigePower_final / PrestigePower_inicial)
  + 0.0 * ln(KillGold_final / KillGold_inicial)
```

Este corte segue a analise do codigo:

- Damage pode reduzir tempo de farm ou aumentar a wave atingida.
- Prestige Power multiplica o prestige recebido na wave ja alcancada.
- Kill Gold so tem valor para FARM se o gold extra virar level util de heroi durante a run.

Para incluir Kill Gold em um cenario de push ou farm com compra de level durante a run:

```bash
python3 "Idle Hero TD/scripts/optimize_farm_upgrades.py" --state estado.json --include-gold
```

Ou defina peso manual:

```bash
python3 "Idle Hero TD/scripts/optimize_farm_upgrades.py" --state estado.json --gold-weight 0.25
```

## Formulas usadas

Impacto de cada upgrade:

```text
factor(level, q) = 1 + level * q
```

Damage, Kill Gold e Prestige Power sao produtos dos fatores de suas respectivas linhas. Os percentuais `q` vem de:

```text
csv/core_upgrade_formula_factors.csv
```

Custos por nivel vem de:

```text
csv/core_upgrade_cost_formula_classes.csv
```

Research/Energy:

```text
cost_next = roundToEven(baseCost * targetLevel ^ multCost)
```

Prestige/PowerUps normal:

```text
cost_next = BigDouble.Round(baseCost * targetLevel ^ multCost * extraMultiplier)
```

Prestige/PowerUps endgame:

```text
cost_next = BigDouble.Round(baseCost * multCost ^ (targetLevel - 1) * extraMultiplier)
```

O script replica os thresholds de custo de PowerUps:

```text
x3 a partir de round(maxLevel * 0.5)
x8 a partir de round(maxLevel * 0.800000011920929)
x(1 + targetLevel * 0.0010000000474974513) quando targetLevel >= 2 e maxLevel >= 1000
```

## Como a distribuicao e escolhida

Para cada upgrade candidato, o script calcula o ganho marginal do proximo nivel:

```text
gain = weight_metric * ln(factor(level + 1, q) / factor(level, q))
roi = gain / cost_next
```

Ele compra o melhor ROI disponivel, atualiza nivel/recurso, recalcula o proximo custo e repete. Research/Energy tambem usa custo variavel por nivel: o script avanca o upgrade escolhido ate o ponto em que o ROI marginal encosta no proximo candidato do mesmo recurso ou o recurso acaba. PowerUps/Prestige usam o mesmo batching monotônico.

Para PowerUps com expoente fracionario, a potencia e calculada em forma logaritmica estilo BigDouble, que e mais coerente com o tipo numerico do jogo e evita travar em orcamentos altos como `1e20`.

Energy e Prestige Points sao otimizados como orcamentos separados. Um upgrade de Energy nao compete com um upgrade de Prestige Points.

## Saida

O JSON de saida contem:

- `resources`: gasto e saldo de `energy` e `prestige_points`.
- `factors`: fator inicial, final e multiplicador ganho para Damage, Prestige Power e Kill Gold.
- `purchases`: lista de compras recomendadas por upgrade.
- `final_levels`: niveis finais para copiar para planilha ou nova simulacao.
- `diagnostics`: iteracoes, limite de seguranca e metricas excluidas.

## Limite do modelo

O script otimiza o estado permanente de FARM para os pesos definidos. Ele nao simula combate, spawn, HP, mapa, herois, sinergias ou compra de level dentro da run.

Isso e correto para o corte FARM estavel que foi definido:

```text
Gold so vale se virar level util durante a run.
Sem essa conversao, Kill Gold fica com peso 0.
```

Para push real, o proximo passo e acoplar este otimizador a uma simulacao de run que estime:

```text
Damage -> tempo/wave
Kill Gold -> level comprado -> DPS efetivo -> tempo/wave
Prestige Power -> prestige por wave
```
