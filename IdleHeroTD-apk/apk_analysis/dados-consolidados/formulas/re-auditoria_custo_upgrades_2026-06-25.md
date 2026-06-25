# Re-auditoria de custo dos upgrades - 2026-06-25

Status: fonte canonica para custo de upgrade de Research/Energy e Prestige/PowerUps. Esta auditoria foi feita depois de identificar que uma recomendacao FARM anterior tratou Research como custo constante/eixo de potencia errado.

## Conclusao

O custo de Research/Energy nao e constante.

Para os upgrades centrais (`researchDmg*`, `researchKillGold*`, `researchPrestigePower*`), o custo por nivel e:

```text
targetLevel = currentLevel + 1
levelCost = roundToEven(baseCost * targetLevel ^ multCost)
```

Como os upgrades centrais de Research atualmente tem `multCost = 1`, isso vira uma progressao linear por nivel:

```text
levelCost = baseCost * targetLevel
```

Exemplo validado contra a UI: `researchDmg1` no level `446` custa `5 * 447 = 2.235` Energy para o proximo nivel.

Prestige/PowerUps usa `BigDouble`:

```text
if overrideFormulaEndGameUpgrade:
  levelCost = BigDouble(baseCost) * BigDouble.Pow(BigDouble(multCost), targetLevel - 1)
else:
  levelCost = BigDouble(baseCost) * BigDouble.Pow(BigDouble(targetLevel), multCost)

levelCost *= extraMultiplier(targetLevel, maxLevel)
total += levelCost
return BigDouble.Round(total)
```

Multiplicadores extras de Prestige/PowerUps:

```text
thresholdA = roundFloatToInt(maxLevel * 0.5)
thresholdB = roundFloatToInt(maxLevel * 0.800000011920929)

if targetLevel >= thresholdA: extra *= 3
if targetLevel >= thresholdB: extra *= 8
if targetLevel >= 2 and maxLevel >= 1000:
  extra *= 1 + targetLevel * 0.0010000000474974513
```

## Evidencia do app

Campos extraidos:

- `UpgradesResearchCell.baseCost`: offset `0x3C`
- `UpgradesResearchCell.multCost`: offset `0x40`
- `UpgradesResearchCell.currLevel`: offset `0x98`
- `UpgradesResearchCell.cost`: offset `0x9C`
- `UpgradesResearchCell.upgNumLevels`: offset `0xA0`
- `UpgradesPowerUpsCell.baseCost`: offset `0x40`
- `UpgradesPowerUpsCell.multCost`: offset `0x48`
- `UpgradesPowerUpsCell.overrideFormulaEndGameUpgrade`: offset `0x4C`
- `UpgradesPowerUpsCell.currLevel`: offset `0xA0`
- `UpgradesPowerUpsCell.cost`: offset `0xA8`
- `UpgradesPowerUpsCell.upgNumLevels`: offset `0xB8`

Trecho chave de Research em `scripts-extraidos/il2cpp/Cpp2IL-isil/IsilDump/Assembly-CSharp/UpgradesResearchCell.txt`:

- linha `2837`: le `currLevel` de `[X19+152]`
- linha `2847`: calcula `targetLevel = currLevel + loopIndex`
- linha `2859`: le `multCost` de `[X19+64]`
- linha `2861`: le `baseCost` de `[X19+60]`
- linha `2862`: chama a funcao de potencia
- linha `2863`: multiplica `baseCost * pow(...)`
- linha `2865`: soma no custo acumulado
- linha `2868`: arredonda
- linhas `2891-2892`: incrementa `upgNumLevels`/loop

A ordem dos argumentos da potencia e confirmada pela UI: se fosse `baseCost * multCost ^ targetLevel`, `researchDmg1` com `multCost = 1` custaria sempre `5`, mas o jogo mostra `2.235`. A formula `baseCost * targetLevel ^ multCost` bate exatamente.

Trecho chave de Prestige/PowerUps em `scripts-extraidos/il2cpp/Cpp2IL-isil/IsilDump/Assembly-CSharp/UpgradesPowerUpsCell.txt`:

- linhas `3505-3517`: calcula thresholds de `maxLevel * 0.5` e `maxLevel * 0.800000011920929`
- linha `3540`: le `currLevel`
- linha `3551`: calcula o proximo `targetLevel`
- linhas `3567-3572`: escolhe o ramo por `overrideFormulaEndGameUpgrade`
- linhas `3576-3586` e `3691-3696`: ramo endgame, `BigDouble.Pow(multCost, targetLevel - 1)`
- linhas `3705-3717`: ramo normal, `BigDouble.Pow(targetLevel, multCost)` e multiplica por `baseCost`
- linhas `3726-3772`: aplica multiplicadores extras `x3`, `x8`, `1 + targetLevel * slope`
- linhas `3782-3787`: soma o custo do nivel ao total

`BreakInfinity/BigDouble.txt` confirma que `BigDouble.Pow(..., double)` chama `PowInternal` e normaliza o resultado (`linhas 7352-7355`, `7764`).

## Validacao contra UI

Estado usado: snapshot interno de validacao com levels conhecidos de Research/Energy e Prestige/PowerUps.

| Upgrade | Level | Custo +1 calculado | Valor esperado na UI |
| --- | ---: | ---: | ---: |
| `researchDmg1` | 446 | 2.235 | 2.235 |
| `researchDmg2` | 112 | 8.475 | 8.475 |
| `researchDmg3` | 31 | 32.000 | 32.000 |
| `researchDmg4` | 10 | 110.000 | 110.000 |
| `researchDmg5` | 10 | 1,10M | 1,10M |
| `researchPrestigePower1` | 765 | 7.660 | 7.660 |
| `prestigeDmg2` | 332.689 | 1.411858498205e14 | 141,19T |
| `prestigeDmg3` | 10.936 | 4.251015530343e15 | 4.25E+15 |
| `prestigeDmg4` | 638 | 6.938252494388e16 | 6.94E+16 |

Tabelas completas para `+1`, `+10`, `+100`, `+1000`, `+10000` podem ser regeneradas localmente com `scripts/generate_research_cost_table.py`.

## Correcao nos artefatos

Artefatos antigos que recomendavam `researchDmg1: 446 -> 71455 (+71009)` estavam errados e foram invalidados. Com `2,2M` Energy, o resultado coerente salvo agora compra:

```text
researchDmg1: 446 -> 657 (+211), custo 582360 Energy
researchDmg2: 112 -> 167 (+55),  custo 577500 Energy
researchDmg3: 31  -> 45  (+14),  custo 539000 Energy
researchDmg4: 10  -> 14  (+4),   custo 500000 Energy
saldo Energy: 1140
```

O teste deterministico salvo em `scripts/test_upgrade_cost_formulas.py` usa os prints de 2026-06-25 como fixtures e falha se Research voltar a ser tratado como constante ou se a potencia trocar de eixo.

## Regra operacional

Para qualquer otimizacao futura:

1. Calcular custo por nivel com o nivel-alvo atualizado.
2. Somar nivel a nivel para `+N`.
3. Excluir upgrades bloqueados por wave, mesmo quando aparecem como `Lv. 0`.
4. Tratar upgrades omitidos por max level como maxados, nao como `0`.
5. Validar pelo menos os custos `+1`, `+10`, `+100` contra a UI antes de confiar em uma recomendacao nova.
