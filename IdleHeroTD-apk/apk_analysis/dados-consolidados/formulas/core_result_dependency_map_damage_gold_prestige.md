# Dependency map: Damage, Kill Gold e Prestige

Status: mapa de dependencias confirmado por indices IL2CPP/campos `DataManager` e metodos centrais. As formulas exatas de custo/impacto dos upgrades pedidos ficam nos outros arquivos desta pasta; este documento existe para nao confundir "resultado final do jogo" com "fator dos upgrades Research/Prestige".

## Leitura correta para otimizacao

Se o objetivo e distribuir recursos entre os upgrades pedidos, mantendo mapa, herois, temporarios e wave fixos, os fatores externos abaixo podem ser tratados como constantes. Nesse caso, eles cancelam na comparacao de ROI.

Se o objetivo e prever wave futura, gold por hora ou prestige por run, os fatores externos nao cancelam: Damage altera progressao de wave, wave altera base de Gold/Prestige, e mapas/herois/sinergias alteram varios multiplicadores.

## Damage

Metodo nuclear confirmado:

- `Hero.getDmg(BigDouble baseDps, bool _includeSkills)`
- `Hero.getDmgPermEffect()`
- `Enemy.dealDamage(...)` para crit/super/ultra, splash, skill damage e aplicacao no alvo

Upgrades pedidos que entram diretamente no fator permanente:

- Research: `researchDmg1..6`
- Prestige: `prestigeDmg1..7`

Outras familias que interagem com Damage final ou DPS efetivo:

| Familia | Exemplos de campos/sistemas |
| --- | --- |
| Heroi/base | stats do heroi, nivel do heroi, raridade/rank, skills, mastery do heroi |
| Critico | `researchCritChance`, `researchSuperCritDmg`, `prestigeCritDmg`, `prestigeSuperCritChance`, `runeCritChance`, `runeCritDmg`, `runeUltraCritChance`, `runeUltraCritDmg`, `ticketCritChance`, `ticketCritDamage`, `ticketSuperCritChance`, `ticketSuperCritDamage` |
| Boss/target | `prestigeBossDmg`, `techBossDmg`, tipo forte/fraco de dano (`strongDmgType`, `weakDmgType`), boss/PvP boss/rune boss/tech boss |
| Attack speed/range/DPS | `researchAttSpeed`, `researchAttSpeed2`, `prestigeRange`, map slots de attack speed/range, perks de range |
| Skill/spell | `researchSkillDuration`, `researchSpellDuration`, `prestigeSkillCd`, `prestigeSpellCd`, `prestigeSkillPower`, `prestigeSkillPower2`, `spellMapDmg`, `spellHeroDmg`, `spellHeroCritChance`, `spellHeroCritDmg`, `spellHeroSkillPower` |
| Mapas e slots | bonus fixos de mapa, `map5Perks_damage`, `map7Perks_dmgGroup1`, `mapNSlots_damage`, `mapNSlots_skillPowerPct`, `mapNSlots_synergyBonus` |
| Sinergias | sinergias pessoais/globais dos herois, `researchSynergyBonus`, `techSynergyBonus`, mastery de sinergia, bonus de slot de sinergia |
| Permanentes gerais | `iapDamage`, `bpDamage`, `communityEventDamageBonus`, `taskMasterPermDmg`, `giftcodeDamage` |
| Progressao avancada | `techDmg1`, `techDmg2`, `supTechDmg1Bonus`, `supTechDmg2Bonus`, `supTechDamage3`, `tournDmg1`, `tournDmg2`, `ticketDamage1..3`, `ultimusDmg`, `ultimusDmg2`, `gemsDmg`, `runeDmg1..6`, `masteryDamage`, `wavePerkDamage` |
| Funcoes/workshop | `functionEffectDamageLevel`, `workshopLevelIdleDamage*`, `workshopCooldownIdleDamage*` |

## Kill Gold

Metodos nucleares confirmados:

- `GameManager.getBaseGoldDrop(int _useWaveNum)`
- `Enemy.getKillGoldAmt(Hero _fromHero, bool includeEnemyTypeBonus)`

Upgrades pedidos que entram diretamente no `BaseGoldDrop`:

- Research: `researchKillGold1..6`
- Prestige: `prestigeKillGold1..7`

Outras familias que interagem com Gold/Kill Gold:

| Familia | Exemplos de campos/sistemas |
| --- | --- |
| Base por wave | wave atual/usada em `getBaseGoldDrop` |
| Heroi/inimigo | bonus de heroi, tipo de inimigo, boss, hoarder, mimic, golden enemies |
| Super/Ultra Gold | `prestigeUltraGoldChance`, `prestigeVideoAdUltraGoldChance`, `prestigeVideoAdUltraGoldAmount`, `ticketSuperGoldChance`, `ticketSuperGoldAmount`, `ticketUltraGoldChance`, `runeUltraGoldChance`, `runeUltraGoldAmt`, `ultimusUltraGoldChance`, `ultimusUltraGoldAmount` |
| Boss/Hoarder/Mimic | `prestigeBossGold`, `prestigeHoarderGold`, `prestigeMimicGold`, `researchMimicGold`, `techBossGold`, `techHoarderGold`, `masteryBossGold`, `masteryMimicEnergy` |
| Bonus chance/amount | `researchBonusGoldAmt`, `prestigeBonusGoldChance`, `tournBonusGoldChance`, `tournBonusGoldAmt`, `runeBonusGoldAmt` |
| Mapas e slots | `map5Perks_gold`, `map7Perks_goldGroup2`, `mapNSlots_gold`, bonus fixos de mapa |
| Permanentes gerais | `iapKillGold`, `bpKillGold`, `communityEventGoldBonus`, `taskMasterPermGold`, `giftcodeKillGold` |
| Progressao avancada | `techKillGold1`, `techKillGold2`, `supTechGold1Bonus`, `supTechGold2Bonus`, `supTechGold3`, `tournKillGold1`, `tournKillGold2`, `ticketGold1..3`, `ultimusKillGold`, `ultimusKillGold2`, `gemsKillGold`, `runeKillGold1..6`, `masteryKillGold`, `wavePerkKillGold` |
| Funcoes/workshop | `functionEffectGoldLevel`, `workshopLevelIdleGold*`, `workshopCooldownIdleGold*` |

## Prestige Power

Metodos nucleares confirmados:

- `GlobalMethods.getPrestigePointsReward(int _onWaveNum, bool _includeTempPerks)`
- `GlobalMethods.getPrestigePointsPermEffect(bool _includeTempPerks)`

Formula base confirmada:

```text
PrestigeReward(wave, includeTempPerks) =
  ROUND(
    (wave * (wave + 1) / 2)
    * (1 + 0.01 * wave)
    * PrestigePointsPermEffect(includeTempPerks)
  )
```

Upgrade pedido que entra diretamente no efeito permanente:

- Research: `researchPrestigePower1..5`

Outras familias que interagem com Prestige Power ou prestige recebido:

| Familia | Exemplos de campos/sistemas |
| --- | --- |
| Wave | `_onWaveNum`, `lastPrestigeWave`, funcoes/workshop que mexem com wave de prestige |
| Permanentes gerais | `iapPrestigePower`, `bpPrestigePower`, `communityEventPrestigeBonus`, `taskMasterPermPrestige`, `giftcodePrestige` |
| Mapas | `map4Perks_prestigePower`, bonus fixo de mapa, `map7Perks_*` quando afeta progressao/wave |
| Mimic/prestige drops | `researchMimicPrestigePts`, `mimicChestPrestigePower`, `statCurrRunMimicPrestigePts` |
| Progressao avancada | `techPrestigePower`, `supTechPrestige1Bonus`, `supTechPrestige2`, `ultimusPrestigePower`, `ultimusPrestigePower2`, `gemsPrestigePower`, `runePrestigePower1..4`, `masteryPrestigePower`, `wavePerkPrestigePower` |
| Funcoes/workshop | `functionEffectPrestigeWavePct`, `workshopLevelPrestigeWaves`, `workshopCooldownPrestigeWaves` |

## O que esta exato hoje

- Fator por nivel dos upgrades pedidos: `core_formulas_damage_gold_prestige.md`.
- Custo real dos upgrades pedidos: `core_upgrade_cost_formulas.md`.
- Parametros tabulares por upgrade: `csv/core_upgrade_formula_factors.csv`.
- Classe de formula de custo por upgrade: `csv/core_upgrade_cost_formula_classes.csv`.

## O que ainda exigiria outra passada se voce quiser simulador total

Um simulador total de run precisaria extrair e implementar tambem:

- formula completa de hero damage/skills/crit em `Hero` e `Enemy.dealDamage`;
- formula completa de `Enemy.getKillGoldAmt`;
- todas as familias permanentes acima, nao apenas Research/Prestige;
- mapas, slots, perks, sinergias e temporarios ativos;
- progressao de wave/inimigos/HP, porque Damage afeta ate onde voce chega, e wave afeta Gold/Prestige.
