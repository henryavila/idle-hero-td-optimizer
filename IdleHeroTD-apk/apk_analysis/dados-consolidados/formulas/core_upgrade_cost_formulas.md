# Core upgrade cost formulas

Status: extraido do `libil2cpp.so`/IL2CPP, nao da UI. A UI arredonda e formata valores; este arquivo documenta a regra usada pelo jogo para cobrar upgrades.

## Fontes brutas usadas

- `scripts-extraidos/indices/il2cpp_assembly_csharp_methods.csv`
- `scripts-extraidos/indices/il2cpp_assembly_csharp_fields.csv`
- `scripts-extraidos/il2cpp/Cpp2IL-isil/IsilDump/Assembly-CSharp/UpgradesResearchCell.txt`
- `scripts-extraidos/il2cpp/Cpp2IL-isil/IsilDump/Assembly-CSharp/UpgradesPowerUpsCell.txt`
- `dados-brutos/extracted/split_config.arm64_v8a/lib/arm64-v8a/libil2cpp.so`

Observacao de enderecos: o CSV Cpp2IL esta `0x4000` abaixo do VA real no `libil2cpp.so`. Exemplo: `UpgradesResearchCell.updCell` aparece no CSV como `0x1B0BFF8`; no binario real a rotina esta em `0x1B0FFF8`.

## Constantes confirmadas no binario

| Constante | Valor raw | Uso |
| --- | ---: | --- |
| `DYNAMIC_COST_DIVISOR` | `10000.0` | Ajuste dinamico de `multCost` para `UpgradeManager.killExpFlat` |
| `POWERUPS_HIGH_THRESHOLD_PCT` | `0.800000011920929` | Segundo limiar de custo de PowerUps/Prestige |
| `POWERUPS_ENDGAME_SLOPE` | `0.0010000000474974513` | Multiplicador extra `1 + targetLevel * slope` |

## Arredondamentos

`GlobalMethods.roundFloatToInt(float)` e usado para calcular limiares de PowerUps/Prestige:

```text
roundFloatToInt(x) =
  floor(x), se frac(x) < 0.5
  ceil(x),  se frac(x) >= 0.5
```

Para numeros positivos, isso e arredondamento "meio para cima".

Research usa outro arredondamento no acumulado de custo:

```text
roundToEven(x) =
  inteiro mais proximo;
  se a fracao for exatamente .5, escolhe o inteiro par.
```

PowerUps/Prestige soma em `BigDouble` e chama `BigDouble.Round(total)` no fim.

## Research / Energy

Campos da celula:

- `baseCost`: `UpgradesResearchCell.baseCost`
- `multCost`: `UpgradesResearchCell.multCost`
- `currLevel`: nivel atual salvo no `DataManager`
- `upgNumLevels`: quantidade comprada
- `maxLevel`: limite da celula

Formula exata para comprar `n` niveis a partir do nivel atual `L`:

```text
cost = 0
bought = 0

for targetLevel in (L + 1) .. min(L + n, maxLevel):
  m = effectiveResearchMultCost(targetLevel)
  levelCost = baseCost * pow(targetLevel, m)
  cost = roundToEven(cost + levelCost)
  bought += 1

return cost, bought
```

Para os upgrades centrais deste estudo (`researchDmg1..6`, `researchKillGold1..6`, `researchPrestigePower1..5`), `effectiveResearchMultCost(targetLevel) = multCost` do asset.

Existe uma excecao geral no codigo, mas ela nao afeta os upgrades centrais acima:

```text
if upgrade == UpgradeManager.killExpFlat:
  effectiveResearchMultCost(targetLevel) =
    1.5 + min(0.5, targetLevel / 10000.0)
else:
  effectiveResearchMultCost(targetLevel) = multCost
```

Detalhe importante: a base da potencia e o `targetLevel`, e nao `targetLevel - 1`. Para os upgrades centrais com `multCost = 1`, isso vira `baseCost * targetLevel`, que bate com a UI. Exemplo: `researchDmg1` no level `446` custa `5 * 447 = 2.235` para o proximo nivel.

## Prestige / PowerUps

Campos da celula:

- `baseCost`: `UpgradesPowerUpsCell.baseCost`
- `multCost`: `UpgradesPowerUpsCell.multCost`
- `overrideFormulaEndGameUpgrade`: muda a familia da formula
- `currLevel`: nivel atual salvo no `DataManager`
- `upgNumLevels`: quantidade comprada
- `maxLevel`: limite da celula

Limiares:

```text
thresholdA = roundFloatToInt(maxLevel * 0.5)
thresholdB = roundFloatToInt(maxLevel * 0.800000011920929)
```

Multiplicadores extras aplicados ao custo do nivel-alvo:

```text
extra = 1

if targetLevel >= thresholdA:
  extra *= 3

if targetLevel >= thresholdB:
  extra *= 8

if targetLevel >= 2 and maxLevel >= 1000:
  extra *= 1 + targetLevel * 0.0010000000474974513
```

Formula para comprar `n` niveis a partir de `L`:

```text
total = BigDouble(0)

for i in 0 .. n-1:
  targetLevel = L + i + 1
  m = effectivePowerupsMultCost(targetLevel)

  if overrideFormulaEndGameUpgrade:
    levelCost = BigDouble(baseCost) * BigDouble.Pow(BigDouble(m), targetLevel - 1)
  else:
    levelCost = BigDouble(baseCost) * BigDouble.Pow(BigDouble(targetLevel), m)

  levelCost *= extraMultiplier(targetLevel, maxLevel)
  total += levelCost

return BigDouble.Round(total)
```

O ramo de compra fixa e o ramo de compra maxima usam a mesma formula por nivel. No ramo de compra maxima, o jogo incrementa `upgNumLevels` enquanto o total calculado ainda cabe em `DataManager.resPrestigePoints_big` e o upgrade nao atingiu `maxLevel`.

Para os upgrades centrais de Prestige:

- `prestigeDmg1..6` e `prestigeKillGold1..6`: `overrideFormulaEndGameUpgrade = 0`, entao usam `baseCost * targetLevel ^ multCost`.
- `prestigeDmg7` e `prestigeKillGold7`: `overrideFormulaEndGameUpgrade = 1`, entao usam `baseCost * multCost ^ (targetLevel - 1)`.

Existe a mesma excecao dinamica de `multCost` para `UpgradeManager.killExpFlat`, fora do escopo central:

```text
if upgrade == UpgradeManager.killExpFlat:
  effectivePowerupsMultCost(targetLevel) =
    6.0 + min(1.5, targetLevel / 10000.0)
else:
  effectivePowerupsMultCost(targetLevel) = multCost
```

## Limiar pratico dos upgrades de Prestige pedidos

Para `prestigeDmg1..6` e `prestigeKillGold1..6`, `maxLevel = 999999`:

```text
thresholdA = 500000
thresholdB = 799999
endgame slope ativo a partir de targetLevel = 2
```

Para `prestigeDmg7` e `prestigeKillGold7`, `maxLevel = 999`:

```text
thresholdA = 500
thresholdB = 799
endgame slope inativo, porque maxLevel < 1000
```

## Implicacao para otimizacao

Com niveis atuais e recurso total, da para otimizar com precisao para um estado fixo:

- custo do proximo nivel vem das formulas acima;
- impacto do proximo nivel vem de `core_formulas_damage_gold_prestige.md`;
- cada compra deve atualizar o nivel antes de recalcular o proximo custo e o proximo ganho marginal.

Greedy por ROI costuma ser bom para simulacao rapida, mas nao e prova de otimo global quando voce distribui varios recursos e varias metricas ao mesmo tempo. Para otimo exato em planilha ou script, use busca inteira/branch-and-bound/DP com essas formulas.
