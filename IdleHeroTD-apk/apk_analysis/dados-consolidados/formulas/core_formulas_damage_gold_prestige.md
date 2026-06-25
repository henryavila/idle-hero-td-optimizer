# Core formulas: Damage, Gold e Prestige Power

Status: reverse engineering parcial focado nos upgrades pedidos. O objetivo deste arquivo e permitir que uma IA ou planilha modele o impacto de Research/Energy e Prestige sem misturar stats de heroi, efeitos pessoais, mapas, temporarios ou eventos.

## Resumo curto

- Os upgrades pedidos entram como fatores multiplicativos independentes.
- A regra base de cada linha e:

```text
factor(level, statAmt) = 1 + level * (statAmt / 100)
```

- Nao some os percentuais de tiers diferentes antes de aplicar. Multiplique cada tier.
- O ganho marginal do proximo nivel de uma linha com percentual `p = statAmt / 100` e:

```text
next_relative_gain = (1 + (level + 1) * p) / (1 + level * p) - 1
next_relative_gain = p / (1 + level * p)
```

- Para otimizar recursos, compare o ganho marginal por custo:

```text
roi_next = LN((1 + (level + 1) * p) / (1 + level * p)) / next_cost
```

Use log quando quiser comparar multiplicadores compostos sem favorecer artificialmente fatores ja grandes.

## Damage

Metodo confirmado: `Hero.getDmgPermEffect()`.

O jogo calcula um multiplicador permanente de dano e o multiplica ao resto da cadeia de dano. Para os upgrades pedidos:

```text
ResearchDamageFactor =
  PRODUCT_i(1 + researchDmg_i * p_i)

PrestigeDamageFactor =
  PRODUCT_i(1 + prestigeDmg_i * p_i)

RequestedDamageUpgradeFactor =
  ResearchDamageFactor * PrestigeDamageFactor

FinalDamage =
  DamageBaseAndOtherFactors * RequestedDamageUpgradeFactor
```

Percentuais por nivel:

| Grupo | Campo | Tier | p |
| --- | --- | ---: | ---: |
| Research | `researchDmg1` | 1 | 0.05 |
| Research | `researchDmg2` | 2 | 0.10 |
| Research | `researchDmg3` | 3 | 0.25 |
| Research | `researchDmg4` | 4 | 0.50 |
| Research | `researchDmg5` | 5 | 0.75 |
| Research | `researchDmg6` | 6 | 1.00 |
| Prestige | `prestigeDmg1` | 1 | 0.05 |
| Prestige | `prestigeDmg2` | 2 | 0.10 |
| Prestige | `prestigeDmg3` | 3 | 0.25 |
| Prestige | `prestigeDmg4` | 4 | 0.50 |
| Prestige | `prestigeDmg5` | 5 | 0.75 |
| Prestige | `prestigeDmg6` | 6 | 1.00 |
| Prestige | `prestigeDmg7` | 7 | 1.25 |

Exemplo:

```text
researchDmg1 = 10 => factor = 1 + 10 * 0.05 = 1.5
researchDmg2 = 10 => factor = 1 + 10 * 0.10 = 2.0
combined = 1.5 * 2.0 = 3.0
```

Nao e `1 + 150%`; e produto dos fatores.

## Gold / Kill Gold

Metodo confirmado: `GameManager.getBaseGoldDrop(int _useWaveNum)`.

O jogo aplica os upgrades de Kill Gold dentro do `baseGoldDrop`, antes de `Enemy.getKillGoldAmt()` aplicar multiplicadores de heroi, tipo de inimigo, boss/hoarder/mimic, super/ultra e outros efeitos. Para isolar o impacto pedido:

```text
ResearchKillGoldFactor =
  PRODUCT_i(1 + researchKillGold_i * p_i)

PrestigeKillGoldFactor =
  PRODUCT_i(1 + prestigeKillGold_i * p_i)

RequestedKillGoldUpgradeFactor =
  ResearchKillGoldFactor * PrestigeKillGoldFactor

BaseGoldDrop =
  GoldWaveBaseAndOtherFactors * RequestedKillGoldUpgradeFactor

KillGoldAmount =
  BaseGoldDrop * HeroEnemyAndTemporaryFactors
```

Percentuais por nivel:

| Grupo | Campo | Tier | p |
| --- | --- | ---: | ---: |
| Research | `researchKillGold1` | 1 | 0.05 |
| Research | `researchKillGold2` | 2 | 0.10 |
| Research | `researchKillGold3` | 3 | 0.25 |
| Research | `researchKillGold4` | 4 | 0.50 |
| Research | `researchKillGold5` | 5 | 0.75 |
| Research | `researchKillGold6` | 6 | 1.00 |
| Prestige | `prestigeKillGold1` | 1 | 0.05 |
| Prestige | `prestigeKillGold2` | 2 | 0.10 |
| Prestige | `prestigeKillGold3` | 3 | 0.25 |
| Prestige | `prestigeKillGold4` | 4 | 0.50 |
| Prestige | `prestigeKillGold5` | 5 | 0.75 |
| Prestige | `prestigeKillGold6` | 6 | 1.00 |
| Prestige | `prestigeKillGold7` | 7 | 1.25 |

## Prestige Power

Metodos confirmados:

- `GlobalMethods.getPrestigePointsReward(int _onWaveNum, bool _includeTempPerks)`
- `GlobalMethods.getPrestigePointsPermEffect(bool _includeTempPerks)`

Formula de recompensa por wave:

```text
PrestigeReward(wave, includeTempPerks) =
  ROUND(
    (wave * (wave + 1) / 2)
    * (1 + 0.01 * wave)
    * PrestigePointsPermEffect(includeTempPerks)
  )
```

Para os upgrades pedidos, `PrestigePointsPermEffect` inclui:

```text
ResearchPrestigePowerFactor =
  (1 + researchPrestigePower1 * 0.10)
  * (1 + researchPrestigePower2 * 0.25)
  * (1 + researchPrestigePower3 * 0.50)
  * (1 + researchPrestigePower4 * 0.75)
  * (1 + researchPrestigePower5 * 1.00)
```

Assim, para otimizar apenas Research Prestige Power:

```text
PrestigeReward =
  PrestigeWaveBase * OtherPrestigeFactors * ResearchPrestigePowerFactor
```

Percentuais por nivel:

| Grupo | Campo | Tier | p |
| --- | --- | ---: | ---: |
| Research | `researchPrestigePower1` | 1 | 0.10 |
| Research | `researchPrestigePower2` | 2 | 0.25 |
| Research | `researchPrestigePower3` | 3 | 0.50 |
| Research | `researchPrestigePower4` | 4 | 0.75 |
| Research | `researchPrestigePower5` | 5 | 1.00 |

Nao encontrei upgrade de Prestige Power na aba Prestige dentro do escopo pedido; os upgrades de Prestige extraidos para este foco sao Damage e Kill Gold.

## CSV para planilha

Arquivo tabular salvo em:

```text
csv/core_upgrade_formula_factors.csv
```

Colunas importantes:

- `system`: `research_energy` ou `prestige`.
- `metric`: `damage`, `kill_gold`, `prestige_power`.
- `data_manager_field`: campo salvo no `DataManager`.
- `stat_amt_percent`: valor de UI/asset, em percentual.
- `percent_per_level`: `stat_amt_percent / 100`.
- `formula_factor`: fator direto para multiplicar.
- `wave_req`, `max_level`, `base_cost`, `mult_cost`, `override_formula_endgame`: parametros extraidos da celula Unity.
- `source_method`, `source_address`: metodo e endereco ARM64 usados para confirmar a formula.

## Custo dos upgrades

O impacto no resultado final esta confirmado pelas formulas acima. O custo real foi extraido depois diretamente de `UpgradesResearchCell.updCell` e `UpgradesPowerUpsCell.updCell`; nao use os valores arredondados da UI como fonte.

Resumo:

- Research/Energy: soma `baseCost * pow(targetLevel, multCost)` e arredonda o acumulado a cada nivel com `roundToEven`.
- Prestige normal (`override_formula_endgame = 0`): soma `BigDouble(baseCost) * BigDouble.Pow(BigDouble(targetLevel), multCost)`.
- Prestige endgame (`override_formula_endgame = 1`): soma `BigDouble(baseCost) * BigDouble.Pow(BigDouble(multCost), targetLevel - 1)`.
- PowerUps/Prestige ainda aplica multiplicadores extras de custo por limiar: `x3`, `x8` e, quando `maxLevel >= 1000`, `1 + targetLevel * 0.0010000000474974513`.

Detalhamento salvo em:

- `core_upgrade_cost_formulas.md`
- `csv/core_upgrade_cost_formula_classes.csv`

## Evidencias principais

- `Hero.getDmgPermEffect`: carrega `researchDmg1..6` e `prestigeDmg1..7`, monta `1 + level * p` e chama multiplicacao de `BigDouble` entre os fatores.
- `GameManager.getBaseGoldDrop`: carrega `researchKillGold1..6` e `prestigeKillGold1..7`, monta `1 + level * p` e multiplica no base gold drop.
- `GlobalMethods.getPrestigePointsReward`: calcula `wave*(wave+1)/2`, multiplica por `1 + 0.01*wave`, chama `getPrestigePointsPermEffect` e arredonda.
- `GlobalMethods.getPrestigePointsPermEffect`: carrega `researchPrestigePower1..5` e multiplica os fatores `1 + level * p`.
- Os enderecos no CSV sao VAs corrigidos; os RVAs dos indices Cpp2IL ficam `0x4000` abaixo desses enderecos no `libil2cpp.so`.
