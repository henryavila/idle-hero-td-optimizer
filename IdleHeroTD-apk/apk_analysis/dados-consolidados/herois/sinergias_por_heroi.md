# Sinergias de herois

Mapa limpo das sinergias extraidas dos MonoBehaviours `Hero`.

- `Tier`: duas sinergias por tier.
- `Rank min`: rank minimo exigido para todos os herois da sinergia.
- `Requer`: herois que precisam ficar proximos do heroi principal.
- `Bonus base`: valor estatico calculado de `GlobalMethods.GetSynergyValue` antes de modificadores dinamicos de save/mapa/slot.
- `Scope`: `personal` afeta o heroi principal; `global` afeta todos os herois.
- `Effect key`: enum raw `HeroUpgrade` extraida do jogo.

Nota: a UI do seu save pode mostrar um valor maior que o base se houver multiplicadores dinamicos. Ex.: base `+10% Attack Speed` pode aparecer como `+11%` com bonus global ativo.

## Militia

- Hero ID: 0
- Class: 0
- Rarity: 1

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Apprentice | +10% Damage | global | `damage_global` |
| 2 | 1 | 0+ | Viking + Scout | -10% Skill Cooldown | personal | `skillCd_personal` |
| 3 | 2 | 15+ | Peacekeeper | +100% Kill Gold | personal | `killGold_personal` |
| 4 | 2 | 15+ | Druid + Battlemage | +60% Damage | global | `damage_global` |
| 5 | 3 | 50+ | Gladiator | +16% Crit Chance | global | `critChance_global` |
| 6 | 3 | 50+ | Warlock + Captain | +100% Attack Speed | personal | `attSpeed_personal` |
| 7 | 4 | 100+ | Witch | +1 Energy Income | global | `energyIncome_global` |
| 8 | 4 | 100+ | Champion + Crusader | +6% Gold Super Chance | global | `goldSuperChance_global` |
| 9 | 5 | 150+ | Praetorian | +10% Exp Super Amount | global | `expSuperAmount_global` |
| 10 | 5 | 150+ | Necromancer + Arbalest | +25% Super Crit Chance | personal | `superCritChance_personal` |
| 11 | 6 | 250+ | Warden | +500% Kill Gold | personal | `killGold_personal` |
| 12 | 6 | 250+ | Titan + Archer | +600% Damage | personal | `damage_personal` |
| 13 | 7 | 500+ | Ballista | +20% Exp Super Amount | global | `expSuperAmount_global` |
| 14 | 7 | 500+ | Spelldancer + Arbalest | +8 Energy Income | global | `energyIncome_global` |
| 15 | 8 | 1000+ | Gladiator + Sorcerer + Captain | +10 Energy Income | global | `energyIncome_global` |
| 16 | 8 | 1000+ | Ninja + Arbalest + Captain | +75% Energy Ultra Amount | global | `energyUltraAmount_global` |

## Viking

- Hero ID: 1
- Class: 0
- Rarity: 1

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Druid | +10% Attack Speed | personal | `attSpeed_personal` |
| 2 | 1 | 0+ | Militia + Scout | +3% Kill Exp | global | `killExp_global` |
| 3 | 2 | 15+ | Spelldancer | +100% Crit Damage | personal | `critDmg_personal` |
| 4 | 2 | 15+ | Assassin + Arbalest | -7% Skill Cooldown | global | `skillCd_global` |
| 5 | 3 | 50+ | Hunter | +1% Skill Power | global | `skillPower_global` |
| 6 | 3 | 50+ | Sorcerer + Dicemaster | +250% Damage | personal | `damage_personal` |
| 7 | 4 | 100+ | Gladiator | +850% Super Crit Damage | personal | `superCritDmg_personal` |
| 8 | 4 | 100+ | Titan + Necromancer | +150% Kill Gold | global | `killGold_global` |
| 9 | 5 | 150+ | Deadeye | +8% Super Crit Chance | global | `superCritChance_global` |
| 10 | 5 | 150+ | Samurai + Elementalist | +1250% Gold Super Amount | personal | `goldSuperAmount_personal` |
| 11 | 6 | 250+ | Chieftain | +250% Damage | global | `damage_global` |
| 12 | 6 | 250+ | Ranger + Crusader | +6% Skill Power | global | `skillPower_global` |
| 13 | 7 | 500+ | Warlord | +1400% Ultra Boss Damage | global | `ultraBossDmg_global` |
| 14 | 7 | 500+ | Forester + Veteran | +8% Skill Power | global | `skillPower_global` |
| 15 | 8 | 1000+ | Wizard + Necromancer + Ballista | +40% Boss Exp | global | `bossExp_global` |
| 16 | 8 | 1000+ | Archer + Ballista + Veteran | +15% Skill Power | global | `skillPower_global` |

## Ninja

- Hero ID: 2
- Class: 0
- Rarity: 2

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Assassin | +25% Damage | personal | `damage_personal` |
| 2 | 1 | 0+ | Sorcerer + Witch | +50% Crit Damage | personal | `critDmg_personal` |
| 3 | 2 | 15+ | Rogue | +8% Crit Chance | global | `critChance_global` |
| 4 | 2 | 15+ | Berserker + Scout | +6 Skill Duration | personal | `skillDuration_personal` |
| 5 | 3 | 50+ | Wizard | +80% Kill Gold | global | `killGold_global` |
| 6 | 3 | 50+ | Archer + Rogue | +30% Attack Speed | global | `attSpeed_global` |
| 7 | 4 | 100+ | Praetorian | +125% Damage | global | `damage_global` |
| 8 | 4 | 100+ | Peacekeeper + Spelldancer | +4% Exp Super Chance | global | `expSuperChance_global` |
| 9 | 5 | 150+ | Ranger | +3% Skill Power | global | `skillPower_global` |
| 10 | 5 | 150+ | Chieftain + Veteran | +4% Energy Super Chance | global | `energySuperChance_global` |
| 11 | 6 | 250+ | Apprentice | +2% Gold Ultra Chance | global | `goldUltraChance_global` |
| 12 | 6 | 250+ | Gladiator + Warlock | +600% Kill Gold | personal | `killGold_personal` |
| 13 | 7 | 500+ | Arbalest | +5% Energy Super Chance | global | `energySuperChance_global` |
| 14 | 7 | 500+ | Assassin + Rogue | +14% Gold Super Chance | global | `goldSuperChance_global` |
| 15 | 8 | 1000+ | Assassin + Elementalist + Warden | +2250% Boss Gold | personal | `bossGold_personal` |
| 16 | 8 | 1000+ | Militia + Arbalest + Captain | +15 Energy Income | global | `energyIncome_global` |

## Assassin

- Hero ID: 3
- Class: 0
- Rarity: 2

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Ninja | +5% Crit Chance | personal | `critChance_personal` |
| 2 | 1 | 0+ | Forester + Archer | -10% Skill Cooldown | personal | `skillCd_personal` |
| 3 | 2 | 15+ | Gladiator | +10% Attack Speed | global | `attSpeed_global` |
| 4 | 2 | 15+ | Viking + Arbalest | +150% Crit Damage | personal | `critDmg_personal` |
| 5 | 3 | 50+ | Ranger | +200% Damage | personal | `damage_personal` |
| 6 | 3 | 50+ | Apprentice + Spelldancer | +250% Kill Gold | personal | `killGold_personal` |
| 7 | 4 | 100+ | Peacekeeper | +125% Kill Gold | global | `killGold_global` |
| 8 | 4 | 100+ | Berserker + Sorcerer | +2 Energy Income | global | `energyIncome_global` |
| 9 | 5 | 150+ | Dicemaster | +175% Damage | global | `damage_global` |
| 10 | 5 | 150+ | Hunter + Captain | +625% Super Crit Damage | global | `superCritDmg_global` |
| 11 | 6 | 250+ | Skymage | +2% Exp Ultra Chance | global | `expUltraChance_global` |
| 12 | 6 | 250+ | Warlord + Wizard | +7% Ultra Crit Chance | personal | `ultraCritChance_personal` |
| 13 | 7 | 500+ | Deadeye | +300% Damage | global | `damage_global` |
| 14 | 7 | 500+ | Ninja + Rogue | +1600% Ultra Boss Damage | global | `ultraBossDmg_global` |
| 15 | 8 | 1000+ | Ninja + Elementalist + Warden | +3000% Ultra Crit Damage | global | `ultraCritDmg_global` |
| 16 | 8 | 1000+ | Praetorian + Wizard + Spelldancer | +75% Attack Speed | global | `attSpeed_global` |

## Peacekeeper

- Hero ID: 4
- Class: 0
- Rarity: 3

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Ranger | +10% Kill Gold | global | `killGold_global` |
| 2 | 1 | 0+ | Samurai + Wizard | +20% Crit Damage | global | `critDmg_global` |
| 3 | 2 | 15+ | Militia | +5% Skill Power | personal | `skillPower_personal` |
| 4 | 2 | 15+ | Warlord + Ballista | +60% Damage | global | `damage_global` |
| 5 | 3 | 50+ | Chieftain | -8% Skill Cooldown | global | `skillCd_global` |
| 6 | 3 | 50+ | Berserker + Forester | +1% Exp Super Chance | global | `expSuperChance_global` |
| 7 | 4 | 100+ | Assassin | +300% Damage | personal | `damage_personal` |
| 8 | 4 | 100+ | Ninja + Spelldancer | +7% Exp Super Amount | global | `expSuperAmount_global` |
| 9 | 5 | 150+ | Witch | +400% Kill Gold | personal | `killGold_personal` |
| 10 | 5 | 150+ | Apprentice + Rogue | +4% Skill Power | global | `skillPower_global` |
| 11 | 6 | 250+ | Scout | +2000% Ultra Crit Damage | global | `ultraCritDmg_global` |
| 12 | 6 | 250+ | Sovereign + Warden | +3% Energy Ultra Chance | global | `energyUltraChance_global` |
| 13 | 7 | 500+ | Captain | +300% Damage | global | `damage_global` |
| 14 | 7 | 500+ | Gladiator + Warlord | +20% Energy Super Amount | global | `energySuperAmount_global` |
| 15 | 8 | 1000+ | Warlord + Apprentice + Arbalest | +1000% Damage | personal | `damage_personal` |
| 16 | 8 | 1000+ | Gladiator + Berserker + Warden | +3% Alien Tech | global | `alienTech_global` |

## Samurai

- Hero ID: 5
- Class: 0
- Rarity: 3

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Arbalest | +10% Damage | global | `damage_global` |
| 2 | 1 | 0+ | Peacekeeper + Wizard | +10% Crit Chance | personal | `critChance_personal` |
| 3 | 2 | 15+ | Witch | +5 Skill Duration | personal | `skillDuration_personal` |
| 4 | 2 | 15+ | Skymage + Templar | +60% Kill Gold | global | `killGold_global` |
| 5 | 3 | 50+ | Deadeye | +80% Crit Damage | global | `critDmg_global` |
| 6 | 3 | 50+ | Necromancer + Hunter | +100% Attack Speed | personal | `attSpeed_personal` |
| 7 | 4 | 100+ | Ballista | +2% Exp Super Chance | global | `expSuperChance_global` |
| 8 | 4 | 100+ | Scout + Warden | +950% Super Crit Damage | personal | `superCritDmg_personal` |
| 9 | 5 | 150+ | Berserker | +8% Gold Super Chance | global | `goldSuperChance_global` |
| 10 | 5 | 150+ | Viking + Elementalist | +450% Damage | personal | `damage_personal` |
| 11 | 6 | 250+ | Praetorian | +5 Energy Income | global | `energyIncome_global` |
| 12 | 6 | 250+ | Paladin + Champion | +275% Kill Gold | global | `killGold_global` |
| 13 | 7 | 500+ | Gladiator | +5% Energy Super Chance | global | `energySuperChance_global` |
| 14 | 7 | 500+ | Druid + Captain | +8% Skill Power | global | `skillPower_global` |
| 15 | 8 | 1000+ | Berserker + Forester + Ranger | +12% Skill Power | global | `skillPower_global` |
| 16 | 8 | 1000+ | Paladin + Champion + Battlemage | +3250% Ultra Crit Damage | global | `ultraCritDmg_global` |

## Paladin

- Hero ID: 6
- Class: 0
- Rarity: 4

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Gladiator | +2% Skill Power | personal | `skillPower_personal` |
| 2 | 1 | 0+ | Spelldancer + Sniper | +50% Kill Gold | personal | `killGold_personal` |
| 3 | 2 | 15+ | Scout | +10% Attack Speed | global | `attSpeed_global` |
| 4 | 2 | 15+ | Sorcerer + Crusader | +10% Kill Exp | global | `killExp_global` |
| 5 | 3 | 50+ | Witch | +8 Skill Duration | personal | `skillDuration_personal` |
| 6 | 3 | 50+ | Praetorian + Veteran | +250% Crit Damage | personal | `critDmg_personal` |
| 7 | 4 | 100+ | Templar | +10% Gold Super Chance | personal | `goldSuperChance_personal` |
| 8 | 4 | 100+ | Chieftain + Sniper | +4% Energy Super Amount | global | `energySuperAmount_global` |
| 9 | 5 | 150+ | Forester | +10% Exp Super Amount | global | `expSuperAmount_global` |
| 10 | 5 | 150+ | Warlord + Druid | +450% Kill Gold | personal | `killGold_personal` |
| 11 | 6 | 250+ | Battlemage | +500% Damage | personal | `damage_personal` |
| 12 | 6 | 250+ | Samurai + Champion | +6% Skill Power | global | `skillPower_global` |
| 13 | 7 | 500+ | Sorcerer | +850% Gold Super Amount | global | `goldSuperAmount_global` |
| 14 | 7 | 500+ | Berserker + Templar | +6% Energy Super Chance | global | `energySuperChance_global` |
| 15 | 8 | 1000+ | Scout + Hunter + Rogue | +3000% Gold Ultra Amount | global | `goldUltraAmount_global` |
| 16 | 8 | 1000+ | Samurai + Champion + Battlemage | +2% Shadow Runes | personal | `shadowRunes_personal` |

## Gladiator

- Hero ID: 7
- Class: 0
- Rarity: 4

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Paladin | +25% Crit Damage | personal | `critDmg_personal` |
| 2 | 1 | 0+ | Battlemage + Rogue | +50% Damage | personal | `damage_personal` |
| 3 | 2 | 15+ | Assassin | -5% Skill Cooldown | global | `skillCd_global` |
| 4 | 2 | 15+ | Forester + Ranger | +60% Attack Speed | personal | `attSpeed_personal` |
| 5 | 3 | 50+ | Militia | +200% Kill Gold | personal | `killGold_personal` |
| 6 | 3 | 50+ | Champion + Elementalist | +20% Crit Chance | global | `critChance_global` |
| 7 | 4 | 100+ | Viking | +125% Kill Gold | global | `killGold_global` |
| 8 | 4 | 100+ | Apprentice + Archer | +150% Damage | global | `damage_global` |
| 9 | 5 | 150+ | Templar | +3 Energy Income | global | `energyIncome_global` |
| 10 | 5 | 150+ | Skymage + Deadeye | +625% Gold Super Amount | global | `goldSuperAmount_global` |
| 11 | 6 | 250+ | Ballista | +45% Exp Ultra Amount | global | `expUltraAmount_global` |
| 12 | 6 | 250+ | Ninja + Warlock | +4250% Ultra Crit Damage | personal | `ultraCritDmg_personal` |
| 13 | 7 | 500+ | Samurai | +15% Energy Super Amount | global | `energySuperAmount_global` |
| 14 | 7 | 500+ | Peacekeeper + Warlord | +8 Energy Income | global | `energyIncome_global` |
| 15 | 8 | 1000+ | Militia + Sorcerer + Captain | +7% Energy Ultra Chance | global | `energyUltraChance_global` |
| 16 | 8 | 1000+ | Peacekeeper + Berserker + Warden | +75% Attack Speed | global | `attSpeed_global` |

## Berserker

- Hero ID: 8
- Class: 0
- Rarity: 5

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Skymage | +10% Damage | global | `damage_global` |
| 2 | 1 | 0+ | Chieftain + Ballista | +20% Crit Damage | global | `critDmg_global` |
| 3 | 2 | 15+ | Veteran | +1% Exp Super Chance | global | `expSuperChance_global` |
| 4 | 2 | 15+ | Ninja + Scout | +6% Skill Power | personal | `skillPower_personal` |
| 5 | 3 | 50+ | Apprentice | +22% Attack Speed | global | `attSpeed_global` |
| 6 | 3 | 50+ | Peacekeeper + Forester | +35% Kill Exp | global | `killExp_global` |
| 7 | 4 | 100+ | Arbalest | +4% Super Crit Chance | global | `superCritChance_global` |
| 8 | 4 | 100+ | Assassin + Sorcerer | +2% Skill Power | global | `skillPower_global` |
| 9 | 5 | 150+ | Samurai | +400% Damage | personal | `damage_personal` |
| 10 | 5 | 150+ | Titan + Wizard | +450% Kill Gold | personal | `killGold_personal` |
| 11 | 6 | 250+ | Sovereign | +5% Gold Ultra Chance | personal | `goldUltraChance_personal` |
| 12 | 6 | 250+ | Druid + Hunter | +35% Energy Ultra Amount | global | `energyUltraAmount_global` |
| 13 | 7 | 500+ | Battlemage | +300% Damage | global | `damage_global` |
| 14 | 7 | 500+ | Paladin + Templar | +8 Energy Income | global | `energyIncome_global` |
| 15 | 8 | 1000+ | Samurai + Forester + Ranger | +400% Damage | global | `damage_global` |
| 16 | 8 | 1000+ | Peacekeeper + Gladiator + Warden | +8% Ultra Crit Chance | global | `ultraCritChance_global` |

## Chieftain

- Hero ID: 9
- Class: 0
- Rarity: 5

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Warlock | -2% Skill Cooldown | global | `skillCd_global` |
| 2 | 1 | 0+ | Berserker + Ballista | +25% Attack Speed | personal | `attSpeed_personal` |
| 3 | 2 | 15+ | Archer | +8% Crit Chance | global | `critChance_global` |
| 4 | 2 | 15+ | Sovereign + Captain | +60% Crit Damage | global | `critDmg_global` |
| 5 | 3 | 50+ | Peacekeeper | +80% Kill Gold | global | `killGold_global` |
| 6 | 3 | 50+ | Arbalest + Sniper | +250% Damage | personal | `damage_personal` |
| 7 | 4 | 100+ | Druid | +2% Energy Super Amount | global | `energySuperAmount_global` |
| 8 | 4 | 100+ | Paladin + Sniper | +950% Gold Super Amount | personal | `goldSuperAmount_personal` |
| 9 | 5 | 150+ | Battlemage | +175% Kill Gold | global | `killGold_global` |
| 10 | 5 | 150+ | Ninja + Veteran | +7% Exp Super Chance | global | `expSuperChance_global` |
| 11 | 6 | 250+ | Viking | +5% Skill Power | global | `skillPower_global` |
| 12 | 6 | 250+ | Witch + Spelldancer | +275% Damage | global | `damage_global` |
| 13 | 7 | 500+ | Forester | +850% Gold Super Amount | global | `goldSuperAmount_global` |
| 14 | 7 | 500+ | Elementalist + Sovereign | +350% Kill Gold | global | `killGold_global` |
| 15 | 8 | 1000+ | Druid + Warlock + Archer | +400% Damage | global | `damage_global` |
| 16 | 8 | 1000+ | Druid + Elementalist + Ranger | -20% Skill Cooldown | global | `skillCd_global` |

## Champion

- Hero ID: 10
- Class: 0
- Rarity: 6

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Warlord | +25% Kill Gold | personal | `killGold_personal` |
| 2 | 1 | 0+ | Templar + Warden | +6% Attack Speed | global | `attSpeed_global` |
| 3 | 2 | 15+ | Sorcerer | +40% Damage | global | `damage_global` |
| 4 | 2 | 15+ | Praetorian + Rogue | -20% Skill Cooldown | personal | `skillCd_personal` |
| 5 | 3 | 50+ | Spelldancer | +35% Crit Chance | personal | `critChance_personal` |
| 6 | 3 | 50+ | Gladiator + Elementalist | +100% Crit Damage | global | `critDmg_global` |
| 7 | 4 | 100+ | Hunter | +4% Gold Super Chance | global | `goldSuperChance_global` |
| 8 | 4 | 100+ | Militia + Crusader | +350% Damage | personal | `damage_personal` |
| 9 | 5 | 150+ | Ballista | +400% Kill Gold | personal | `killGold_personal` |
| 10 | 5 | 150+ | Warlock + Archer | +10% Super Crit Chance | global | `superCritChance_global` |
| 11 | 6 | 250+ | Sniper | +5 Energy Income | global | `energyIncome_global` |
| 12 | 6 | 250+ | Samurai + Paladin | +3% Exp Ultra Chance | global | `expUltraChance_global` |
| 13 | 7 | 500+ | Scout | +20% Exp Super Amount | global | `expSuperAmount_global` |
| 14 | 7 | 500+ | Apprentice + Deadeye | +8% Skill Power | global | `skillPower_global` |
| 15 | 8 | 1000+ | Skymage + Sniper + Veteran | +40% Boss Exp | global | `bossExp_global` |
| 16 | 8 | 1000+ | Samurai + Paladin + Battlemage | +75% Attack Speed | global | `attSpeed_global` |

## Warlord

- Hero ID: 11
- Class: 0
- Rarity: 6

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Champion | +10% Attack Speed | personal | `attSpeed_personal` |
| 2 | 1 | 0+ | Necromancer + Captain | +3 Skill Duration | personal | `skillDuration_personal` |
| 3 | 2 | 15+ | Crusader | +10% Attack Speed | global | `attSpeed_global` |
| 4 | 2 | 15+ | Peacekeeper + Ballista | +150% Crit Damage | personal | `critDmg_personal` |
| 5 | 3 | 50+ | Sniper | +80% Damage | global | `damage_global` |
| 6 | 3 | 50+ | Witch + Wizard | +50% Crit Chance | personal | `critChance_personal` |
| 7 | 4 | 100+ | Scout | +300% Damage | personal | `damage_personal` |
| 8 | 4 | 100+ | Skymage + Veteran | +2% Skill Power | global | `skillPower_global` |
| 9 | 5 | 150+ | Titan | +8% Super Crit Chance | global | `superCritChance_global` |
| 10 | 5 | 150+ | Paladin + Druid | +200% Kill Gold | global | `killGold_global` |
| 11 | 6 | 250+ | Dicemaster | +5% Ultra Crit Chance | personal | `ultraCritChance_personal` |
| 12 | 6 | 250+ | Assassin + Wizard | +4250% Gold Ultra Amount | personal | `goldUltraAmount_personal` |
| 13 | 7 | 500+ | Viking | +300% Damage | global | `damage_global` |
| 14 | 7 | 500+ | Peacekeeper + Gladiator | +1600% Ultra Boss Damage | global | `ultraBossDmg_global` |
| 15 | 8 | 1000+ | Peacekeeper + Apprentice + Arbalest | +10 Energy Income | global | `energyIncome_global` |
| 16 | 8 | 1000+ | Titan + Warlock + Warlock | +75% Energy Ultra Amount | global | `energyUltraAmount_global` |

## Apprentice

- Hero ID: 12
- Class: 1
- Rarity: 1

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Militia | +3% Attack Speed | global | `attSpeed_global` |
| 2 | 1 | 0+ | Druid + Hunter | -4% Skill Cooldown | global | `skillCd_global` |
| 3 | 2 | 15+ | Skymage | +40% Crit Damage | global | `critDmg_global` |
| 4 | 2 | 15+ | Elementalist + Sniper | +60% Damage | global | `damage_global` |
| 5 | 3 | 50+ | Berserker | +200% Kill Gold | personal | `killGold_personal` |
| 6 | 3 | 50+ | Assassin + Spelldancer | +20% Crit Chance | global | `critChance_global` |
| 7 | 4 | 100+ | Titan | +2% Exp Super Chance | global | `expSuperChance_global` |
| 8 | 4 | 100+ | Gladiator + Archer | +4% Energy Super Amount | global | `energySuperAmount_global` |
| 9 | 5 | 150+ | Necromancer | +1100% Gold Super Amount | personal | `goldSuperAmount_personal` |
| 10 | 5 | 150+ | Peacekeeper + Rogue | +200% Damage | global | `damage_global` |
| 11 | 6 | 250+ | Ninja | +5% Skill Power | global | `skillPower_global` |
| 12 | 6 | 250+ | Praetorian + Sniper | +275% Kill Gold | global | `killGold_global` |
| 13 | 7 | 500+ | Dicemaster | +15% Skill Power | personal | `skillPower_personal` |
| 14 | 7 | 500+ | Champion + Deadeye | +350% Damage | global | `damage_global` |
| 15 | 8 | 1000+ | Peacekeeper + Warlord + Arbalest | +1000% Super Crit Damage | global | `superCritDmg_global` |
| 16 | 8 | 1000+ | Witch + Skymage + Dicemaster | +15% Skill Power | global | `skillPower_global` |

## Druid

- Hero ID: 13
- Class: 1
- Rarity: 1

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Viking | +2 Skill Duration | personal | `skillDuration_personal` |
| 2 | 1 | 0+ | Apprentice + Hunter | +3% Skill Power | personal | `skillPower_personal` |
| 3 | 2 | 15+ | Arbalest | +40% Damage | global | `damage_global` |
| 4 | 2 | 15+ | Militia + Battlemage | +12% Crit Chance | global | `critChance_global` |
| 5 | 3 | 50+ | Skymage | +200% Crit Damage | personal | `critDmg_personal` |
| 6 | 3 | 50+ | Templar + Scout | +250% Kill Gold | personal | `killGold_personal` |
| 7 | 4 | 100+ | Chieftain | +300% Damage | personal | `damage_personal` |
| 8 | 4 | 100+ | Dicemaster + Rogue | +6% Super Crit Chance | global | `superCritChance_global` |
| 9 | 5 | 150+ | Captain | +400% Kill Gold | personal | `killGold_personal` |
| 10 | 5 | 150+ | Paladin + Warlord | +4 Energy Income | global | `energyIncome_global` |
| 11 | 6 | 250+ | Witch | +2000% Ultra Crit Damage | global | `ultraCritDmg_global` |
| 12 | 6 | 250+ | Berserker + Hunter | +3% Gold Ultra Chance | global | `goldUltraChance_global` |
| 13 | 7 | 500+ | Spelldancer | +300% Damage | global | `damage_global` |
| 14 | 7 | 500+ | Samurai + Captain | +8 Energy Income | global | `energyIncome_global` |
| 15 | 8 | 1000+ | Chieftain + Warlock + Archer | +105% Exp Ultra Amount | global | `expUltraAmount_global` |
| 16 | 8 | 1000+ | Chieftain + Elementalist + Ranger | +8% Energy Ultra Chance | global | `energyUltraChance_global` |

## Sorcerer

- Hero ID: 14
- Class: 1
- Rarity: 2

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Archer | +25% Kill Gold | personal | `killGold_personal` |
| 2 | 1 | 0+ | Ninja + Witch | +4% Crit Chance | global | `critChance_global` |
| 3 | 2 | 15+ | Champion | +40% Damage | global | `damage_global` |
| 4 | 2 | 15+ | Paladin + Crusader | -20% Skill Cooldown | personal | `skillCd_personal` |
| 5 | 3 | 50+ | Necromancer | +80% Attack Speed | personal | `attSpeed_personal` |
| 6 | 3 | 50+ | Viking + Dicemaster | +250% Crit Damage | personal | `critDmg_personal` |
| 7 | 4 | 100+ | Elementalist | +125% Kill Gold | global | `killGold_global` |
| 8 | 4 | 100+ | Assassin + Berserker | +2% Energy Super Chance | global | `energySuperChance_global` |
| 9 | 5 | 150+ | Scout | +3% Skill Power | global | `skillPower_global` |
| 10 | 5 | 150+ | Praetorian + Crusader | +25% Gold Super Chance | personal | `goldSuperChance_personal` |
| 11 | 6 | 250+ | Templar | +250% Damage | global | `damage_global` |
| 12 | 6 | 250+ | Skymage + Ballista | +3% Exp Ultra Chance | global | `expUltraChance_global` |
| 13 | 7 | 500+ | Paladin | +12% Gold Super Chance | global | `goldSuperChance_global` |
| 14 | 7 | 500+ | Wizard + Skymage | +350% Damage | global | `damage_global` |
| 15 | 8 | 1000+ | Militia + Gladiator + Captain | +3000% Ultra Crit Damage | global | `ultraCritDmg_global` |
| 16 | 8 | 1000+ | Necromancer + Forester + Deadeye | +15% Skill Power | global | `skillPower_global` |

## Witch

- Hero ID: 15
- Class: 1
- Rarity: 2

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Forester | -5% Skill Cooldown | personal | `skillCd_personal` |
| 2 | 1 | 0+ | Ninja + Sorcerer | +20% Crit Damage | global | `critDmg_global` |
| 3 | 2 | 15+ | Samurai | +10% Attack Speed | global | `attSpeed_global` |
| 4 | 2 | 15+ | Necromancer + Hunter | +10% Kill Exp | global | `killExp_global` |
| 5 | 3 | 50+ | Paladin | +80% Kill Gold | global | `killGold_global` |
| 6 | 3 | 50+ | Warlord + Wizard | +100% Damage | global | `damage_global` |
| 7 | 4 | 100+ | Militia | +10% Super Crit Chance | personal | `superCritChance_personal` |
| 8 | 4 | 100+ | Ranger + Ballista | +2% Skill Power | global | `skillPower_global` |
| 9 | 5 | 150+ | Peacekeeper | +400% Damage | personal | `damage_personal` |
| 10 | 5 | 150+ | Battlemage + Sovereign | +450% Kill Gold | personal | `killGold_personal` |
| 11 | 6 | 250+ | Druid | +25% Energy Ultra Amount | global | `energyUltraAmount_global` |
| 12 | 6 | 250+ | Chieftain + Spelldancer | +2250% Gold Ultra Amount | global | `goldUltraAmount_global` |
| 13 | 7 | 500+ | Titan | +300% Damage | global | `damage_global` |
| 14 | 7 | 500+ | Necromancer + Warden | +15 Skill Duration | personal | `skillDuration_personal` |
| 15 | 8 | 1000+ | Battlemage + Spelldancer + Templar | +30% Skill Power | personal | `skillPower_personal` |
| 16 | 8 | 1000+ | Apprentice + Skymage + Dicemaster | +3250% Ultra Crit Damage | global | `ultraCritDmg_global` |

## Wizard

- Hero ID: 16
- Class: 1
- Rarity: 3

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Elementalist | +10% Damage | global | `damage_global` |
| 2 | 1 | 0+ | Peacekeeper + Samurai | +20% Kill Gold | global | `killGold_global` |
| 3 | 2 | 15+ | Battlemage | +8% Crit Chance | global | `critChance_global` |
| 4 | 2 | 15+ | Titan + Dicemaster | +15% Attack Speed | global | `attSpeed_global` |
| 5 | 3 | 50+ | Ninja | +20% Kill Exp | global | `killExp_global` |
| 6 | 3 | 50+ | Warlord + Witch | +100% Crit Damage | global | `critDmg_global` |
| 7 | 4 | 100+ | Deadeye | +125% Kill Gold | global | `killGold_global` |
| 8 | 4 | 100+ | Praetorian + Battlemage | +40% Attack Speed | global | `attSpeed_global` |
| 9 | 5 | 150+ | Warlock | +3 Energy Income | global | `energyIncome_global` |
| 10 | 5 | 150+ | Berserker + Titan | +450% Damage | personal | `damage_personal` |
| 11 | 6 | 250+ | Ranger | +25% Energy Ultra Amount | global | `energyUltraAmount_global` |
| 12 | 6 | 250+ | Assassin + Warlord | +7% Ultra Crit Chance | personal | `ultraCritChance_personal` |
| 13 | 7 | 500+ | Crusader | +40% Attack Speed | global | `attSpeed_global` |
| 14 | 7 | 500+ | Sorcerer + Skymage | +350% Damage | global | `damage_global` |
| 15 | 8 | 1000+ | Viking + Necromancer + Ballista | +105% Exp Ultra Amount | global | `expUltraAmount_global` |
| 16 | 8 | 1000+ | Assassin + Praetorian + Spelldancer | +15% Skill Power | global | `skillPower_global` |

## Elementalist

- Hero ID: 17
- Class: 1
- Rarity: 3

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Wizard | +2% Crit Chance | global | `critChance_global` |
| 2 | 1 | 0+ | Ranger + Arbalest | +50% Damage | personal | `damage_personal` |
| 3 | 2 | 15+ | Hunter | +6% Kill Exp | global | `killExp_global` |
| 4 | 2 | 15+ | Apprentice + Sniper | +6 Skill Duration | personal | `skillDuration_personal` |
| 5 | 3 | 50+ | Forester | +22% Attack Speed | global | `attSpeed_global` |
| 6 | 3 | 50+ | Gladiator + Champion | +100% Crit Damage | global | `critDmg_global` |
| 7 | 4 | 100+ | Sorcerer | +2% Energy Super Amount | global | `energySuperAmount_global` |
| 8 | 4 | 100+ | Warlock + Deadeye | +350% Kill Gold | personal | `killGold_personal` |
| 9 | 5 | 150+ | Warden | +10% Exp Super Amount | global | `expSuperAmount_global` |
| 10 | 5 | 150+ | Viking + Samurai | +200% Damage | global | `damage_global` |
| 11 | 6 | 250+ | Necromancer | +3750% Gold Ultra Amount | personal | `goldUltraAmount_personal` |
| 12 | 6 | 250+ | Dicemaster + Scout | +6% Skill Power | global | `skillPower_global` |
| 13 | 7 | 500+ | Rogue | +850% Gold Super Amount | global | `goldSuperAmount_global` |
| 14 | 7 | 500+ | Chieftain + Sovereign | +20% Skill Power | personal | `skillPower_personal` |
| 15 | 8 | 1000+ | Ninja + Assassin + Warden | +3000% Gold Ultra Amount | global | `goldUltraAmount_global` |
| 16 | 8 | 1000+ | Chieftain + Druid + Ranger | +8% Energy Ultra Chance | global | `energyUltraChance_global` |

## Battlemage

- Hero ID: 18
- Class: 1
- Rarity: 4

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Spelldancer | +1% Kill Exp | global | `killExp_global` |
| 2 | 1 | 0+ | Gladiator + Rogue | +25% Attack Speed | personal | `attSpeed_personal` |
| 3 | 2 | 15+ | Wizard | +5% Skill Power | personal | `skillPower_personal` |
| 4 | 2 | 15+ | Militia + Druid | +60% Crit Damage | global | `critDmg_global` |
| 5 | 3 | 50+ | Veteran | +80% Damage | global | `damage_global` |
| 6 | 3 | 50+ | Ballista + Warden | -30% Skill Cooldown | personal | `skillCd_personal` |
| 7 | 4 | 100+ | Ranger | +450% Gold Super Amount | global | `goldSuperAmount_global` |
| 8 | 4 | 100+ | Praetorian + Wizard | +150% Damage | global | `damage_global` |
| 9 | 5 | 150+ | Chieftain | +20% Gold Super Chance | personal | `goldSuperChance_personal` |
| 10 | 5 | 150+ | Witch + Sovereign | +625% Super Crit Damage | global | `superCritDmg_global` |
| 11 | 6 | 250+ | Paladin | +250% Kill Gold | global | `killGold_global` |
| 12 | 6 | 250+ | Forester + Deadeye | +6 Energy Income | global | `energyIncome_global` |
| 13 | 7 | 500+ | Berserker | +40% Attack Speed | global | `attSpeed_global` |
| 14 | 7 | 500+ | Sniper + Crusader | +350% Damage | global | `damage_global` |
| 15 | 8 | 1000+ | Witch + Spelldancer + Templar | +3000% Ultra Crit Damage | global | `ultraCritDmg_global` |
| 16 | 8 | 1000+ | Samurai + Paladin + Champion | +15% Skill Power | global | `skillPower_global` |

## Spelldancer

- Hero ID: 19
- Class: 1
- Rarity: 4

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Battlemage | +10% Kill Gold | global | `killGold_global` |
| 2 | 1 | 0+ | Paladin + Sniper | +25% Attack Speed | personal | `attSpeed_personal` |
| 3 | 2 | 15+ | Viking | +40% Crit Damage | global | `critDmg_global` |
| 4 | 2 | 15+ | Archer + Warden | -7% Skill Cooldown | global | `skillCd_global` |
| 5 | 3 | 50+ | Champion | +80% Damage | global | `damage_global` |
| 6 | 3 | 50+ | Assassin + Apprentice | +12% Skill Power | personal | `skillPower_personal` |
| 7 | 4 | 100+ | Warlock | +450% Super Crit Damage | global | `superCritDmg_global` |
| 8 | 4 | 100+ | Ninja + Peacekeeper | +4% Exp Super Chance | global | `expSuperChance_global` |
| 9 | 5 | 150+ | Sniper | +3% Skill Power | global | `skillPower_global` |
| 10 | 5 | 150+ | Scout + Ballista | +4% Energy Super Chance | global | `energySuperChance_global` |
| 11 | 6 | 250+ | Veteran | +5% Skill Power | global | `skillPower_global` |
| 12 | 6 | 250+ | Chieftain + Witch | +275% Damage | global | `damage_global` |
| 13 | 7 | 500+ | Druid | +850% Super Crit Damage | global | `superCritDmg_global` |
| 14 | 7 | 500+ | Militia + Arbalest | +6% Energy Super Chance | global | `energySuperChance_global` |
| 15 | 8 | 1000+ | Witch + Battlemage + Templar | +20 Skill Duration | personal | `skillDuration_personal` |
| 16 | 8 | 1000+ | Assassin + Praetorian + Wizard | +3250% Ultra Crit Damage | global | `ultraCritDmg_global` |

## Skymage

- Hero ID: 20
- Class: 1
- Rarity: 5

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Berserker | +10% Crit Damage | global | `critDmg_global` |
| 2 | 1 | 0+ | Warlock + Crusader | -10% Skill Cooldown | personal | `skillCd_personal` |
| 3 | 2 | 15+ | Apprentice | +40% Kill Gold | global | `killGold_global` |
| 4 | 2 | 15+ | Samurai + Templar | +10% Kill Exp | global | `killExp_global` |
| 5 | 3 | 50+ | Druid | +35% Crit Chance | personal | `critChance_personal` |
| 6 | 3 | 50+ | Ranger + Crusader | +250% Damage | personal | `damage_personal` |
| 7 | 4 | 100+ | Dicemaster | +4% Gold Super Chance | global | `goldSuperChance_global` |
| 8 | 4 | 100+ | Warlord + Veteran | +2% Skill Power | global | `skillPower_global` |
| 9 | 5 | 150+ | Hunter | +175% Damage | global | `damage_global` |
| 10 | 5 | 150+ | Gladiator + Deadeye | +8% Energy Super Amount | global | `energySuperAmount_global` |
| 11 | 6 | 250+ | Assassin | +2% Ultra Crit Chance | global | `ultraCritChance_global` |
| 12 | 6 | 250+ | Sorcerer + Ballista | +275% Kill Gold | global | `killGold_global` |
| 13 | 7 | 500+ | Warden | +12% Super Crit Chance | global | `superCritChance_global` |
| 14 | 7 | 500+ | Sorcerer + Wizard | +350% Damage | global | `damage_global` |
| 15 | 8 | 1000+ | Champion + Sniper + Veteran | +105% Exp Ultra Amount | global | `expUltraAmount_global` |
| 16 | 8 | 1000+ | Apprentice + Witch + Dicemaster | +75% Attack Speed | global | `attSpeed_global` |

## Warlock

- Hero ID: 21
- Class: 1
- Rarity: 5

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Chieftain | +5% Crit Chance | personal | `critChance_personal` |
| 2 | 1 | 0+ | Crusader + Skymage | +20% Kill Gold | global | `killGold_global` |
| 3 | 2 | 15+ | Praetorian | -5% Skill Cooldown | global | `skillCd_global` |
| 4 | 2 | 15+ | Deadeye + Veteran | +60% Damage | global | `damage_global` |
| 5 | 3 | 50+ | Sovereign | +8 Skill Duration | personal | `skillDuration_personal` |
| 6 | 3 | 50+ | Militia + Captain | +35% Kill Exp | global | `killExp_global` |
| 7 | 4 | 100+ | Spelldancer | +1% Skill Power | global | `skillPower_global` |
| 8 | 4 | 100+ | Elementalist + Deadeye | +500% Gold Super Amount | global | `goldSuperAmount_global` |
| 9 | 5 | 150+ | Wizard | +550% Super Crit Damage | global | `superCritDmg_global` |
| 10 | 5 | 150+ | Champion + Archer | +450% Damage | personal | `damage_personal` |
| 11 | 6 | 250+ | Forester | -30% Skill Cooldown | personal | `skillCd_personal` |
| 12 | 6 | 250+ | Ninja + Gladiator | +275% Kill Gold | global | `killGold_global` |
| 13 | 7 | 500+ | Sovereign | +850% Gold Super Amount | global | `goldSuperAmount_global` |
| 14 | 7 | 500+ | Titan + Archer | +25% Exp Super Amount | global | `expSuperAmount_global` |
| 15 | 8 | 1000+ | Chieftain + Druid + Archer | +30% Skill Power | personal | `skillPower_personal` |
| 16 | 8 | 1000+ | Warlord + Titan + Warlock | +15 Energy Income | global | `energyIncome_global` |

## Templar

- Hero ID: 22
- Class: 1
- Rarity: 6

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Captain | +2% Skill Power | personal | `skillPower_personal` |
| 2 | 1 | 0+ | Champion + Warden | +50% Crit Damage | personal | `critDmg_personal` |
| 3 | 2 | 15+ | Deadeye | +40% Damage | global | `damage_global` |
| 4 | 2 | 15+ | Samurai + Skymage | +60% Kill Gold | global | `killGold_global` |
| 5 | 3 | 50+ | Arbalest | -8% Skill Cooldown | global | `skillCd_global` |
| 6 | 3 | 50+ | Druid + Scout | +100% Attack Speed | personal | `attSpeed_personal` |
| 7 | 4 | 100+ | Paladin | +300% Damage | personal | `damage_personal` |
| 8 | 4 | 100+ | Sovereign + Forester | +15% Super Crit Chance | personal | `superCritChance_personal` |
| 9 | 5 | 150+ | Gladiator | +3 Energy Income | global | `energyIncome_global` |
| 10 | 5 | 150+ | Dicemaster + Sniper | +12% Exp Super Amount | global | `expSuperAmount_global` |
| 11 | 6 | 250+ | Sorcerer | +250% Kill Gold | global | `killGold_global` |
| 12 | 6 | 250+ | Necromancer + Rogue | +3% Gold Ultra Chance | global | `goldUltraChance_global` |
| 13 | 7 | 500+ | Veteran | +20% Exp Super Amount | global | `expSuperAmount_global` |
| 14 | 7 | 500+ | Paladin + Berserker | +20% Energy Super Amount | global | `energySuperAmount_global` |
| 15 | 8 | 1000+ | Witch + Battlemage + Spelldancer | +30% Skill Power | personal | `skillPower_personal` |
| 16 | 8 | 1000+ | Templar + Scout + Sniper | +15 Energy Income | global | `energyIncome_global` |

## Necromancer

- Hero ID: 23
- Class: 1
- Rarity: 6

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Warden | +25% Damage | personal | `damage_personal` |
| 2 | 1 | 0+ | Warlord + Captain | +3 Skill Duration | personal | `skillDuration_personal` |
| 3 | 2 | 15+ | Sniper | +10% Attack Speed | global | `attSpeed_global` |
| 4 | 2 | 15+ | Witch + Hunter | +12% Crit Chance | global | `critChance_global` |
| 5 | 3 | 50+ | Sorcerer | +200% Kill Gold | personal | `killGold_personal` |
| 6 | 3 | 50+ | Samurai + Hunter | +100% Crit Damage | global | `critDmg_global` |
| 7 | 4 | 100+ | Veteran | +1% Energy Super Chance | global | `energySuperChance_global` |
| 8 | 4 | 100+ | Viking + Titan | +150% Damage | global | `damage_global` |
| 9 | 5 | 150+ | Apprentice | +400% Kill Gold | personal | `killGold_personal` |
| 10 | 5 | 150+ | Militia + Arbalest | +1250% Gold Super Amount | personal | `goldSuperAmount_personal` |
| 11 | 6 | 250+ | Elementalist | +3750% Ultra Crit Damage | personal | `ultraCritDmg_personal` |
| 12 | 6 | 250+ | Templar + Rogue | +6 Energy Income | global | `energyIncome_global` |
| 13 | 7 | 500+ | Praetorian | +1400% Ultra Boss Damage | global | `ultraBossDmg_global` |
| 14 | 7 | 500+ | Witch + Warden | +20% Skill Power | personal | `skillPower_personal` |
| 15 | 8 | 1000+ | Viking + Wizard + Ballista | +800% Boss Damage | global | `bossDmg_global` |
| 16 | 8 | 1000+ | Sorcerer + Forester + Deadeye | +3250% Ultra Crit Damage | global | `ultraCritDmg_global` |

## Scout

- Hero ID: 24
- Class: 2
- Rarity: 1

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Hunter | +25% Damage | personal | `damage_personal` |
| 2 | 1 | 0+ | Militia + Viking | +4% Crit Chance | global | `critChance_global` |
| 3 | 2 | 15+ | Paladin | +100% Kill Gold | personal | `killGold_personal` |
| 4 | 2 | 15+ | Ninja + Berserker | +60% Attack Speed | personal | `attSpeed_personal` |
| 5 | 3 | 50+ | Ballista | +80% Crit Damage | global | `critDmg_global` |
| 6 | 3 | 50+ | Druid + Templar | -30% Skill Cooldown | personal | `skillCd_personal` |
| 7 | 4 | 100+ | Warlord | +450% Gold Super Amount | global | `goldSuperAmount_global` |
| 8 | 4 | 100+ | Samurai + Warden | +150% Damage | global | `damage_global` |
| 9 | 5 | 150+ | Sorcerer | +3 Energy Income | global | `energyIncome_global` |
| 10 | 5 | 150+ | Spelldancer + Ballista | +25% Super Crit Chance | personal | `superCritChance_personal` |
| 11 | 6 | 250+ | Peacekeeper | +250% Kill Gold | global | `killGold_global` |
| 12 | 6 | 250+ | Elementalist + Dicemaster | +60% Exp Ultra Amount | global | `expUltraAmount_global` |
| 13 | 7 | 500+ | Champion | +850% Gold Super Amount | global | `goldSuperAmount_global` |
| 14 | 7 | 500+ | Praetorian + Hunter | +14% Gold Super Chance | global | `goldSuperChance_global` |
| 15 | 8 | 1000+ | Paladin + Hunter + Rogue | +7% Gold Ultra Chance | global | `goldUltraChance_global` |
| 16 | 8 | 1000+ | Templar + Templar + Sniper | +1% Battlepass Exp | global | `battlepassExp_global` |

## Hunter

- Hero ID: 25
- Class: 2
- Rarity: 1

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Scout | +10% Kill Gold | global | `killGold_global` |
| 2 | 1 | 0+ | Apprentice + Druid | -10% Skill Cooldown | personal | `skillCd_personal` |
| 3 | 2 | 15+ | Elementalist | +100% Damage | personal | `damage_personal` |
| 4 | 2 | 15+ | Witch + Necromancer | +60% Kill Gold | global | `killGold_global` |
| 5 | 3 | 50+ | Viking | +8% Skill Power | personal | `skillPower_personal` |
| 6 | 3 | 50+ | Samurai + Necromancer | +50% Crit Chance | personal | `critChance_personal` |
| 7 | 4 | 100+ | Champion | +125% Damage | global | `damage_global` |
| 8 | 4 | 100+ | Arbalest + Captain | +15% Gold Super Chance | personal | `goldSuperChance_personal` |
| 9 | 5 | 150+ | Skymage | +8% Super Crit Chance | global | `superCritChance_global` |
| 10 | 5 | 150+ | Assassin + Captain | +450% Kill Gold | personal | `killGold_personal` |
| 11 | 6 | 250+ | Crusader | +5% Skill Power | global | `skillPower_global` |
| 12 | 6 | 250+ | Berserker + Druid | +2250% Gold Ultra Amount | global | `goldUltraAmount_global` |
| 13 | 7 | 500+ | Sniper | +7% Skill Power | global | `skillPower_global` |
| 14 | 7 | 500+ | Praetorian + Scout | +2000% Gold Super Amount | personal | `goldSuperAmount_personal` |
| 15 | 8 | 1000+ | Paladin + Scout + Rogue | +30% Skill Power | personal | `skillPower_personal` |
| 16 | 8 | 1000+ | Sovereign + Rogue + Crusader | +3250% Gold Ultra Amount | global | `goldUltraAmount_global` |

## Forester

- Hero ID: 26
- Class: 2
- Rarity: 2

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Witch | -5% Skill Cooldown | personal | `skillCd_personal` |
| 2 | 1 | 0+ | Assassin + Archer | +25% Attack Speed | personal | `attSpeed_personal` |
| 3 | 2 | 15+ | Captain | +40% Crit Damage | global | `critDmg_global` |
| 4 | 2 | 15+ | Gladiator + Ranger | +6 Skill Duration | personal | `skillDuration_personal` |
| 5 | 3 | 50+ | Elementalist | +200% Kill Gold | personal | `killGold_personal` |
| 6 | 3 | 50+ | Peacekeeper + Berserker | +3% Exp Super Amount | global | `expSuperAmount_global` |
| 7 | 4 | 100+ | Rogue | +450% Super Crit Damage | global | `superCritDmg_global` |
| 8 | 4 | 100+ | Templar + Sovereign | +2% Skill Power | global | `skillPower_global` |
| 9 | 5 | 150+ | Paladin | +10% Exp Super Amount | global | `expSuperAmount_global` |
| 10 | 5 | 150+ | Ranger + Warden | +450% Damage | personal | `damage_personal` |
| 11 | 6 | 250+ | Warlock | +3750% Gold Ultra Amount | personal | `goldUltraAmount_personal` |
| 12 | 6 | 250+ | Battlemage + Deadeye | +275% Kill Gold | global | `killGold_global` |
| 13 | 7 | 500+ | Chieftain | +850% Super Crit Damage | global | `superCritDmg_global` |
| 14 | 7 | 500+ | Viking + Veteran | +350% Damage | global | `damage_global` |
| 15 | 8 | 1000+ | Samurai + Berserker + Ranger | +3000% Gold Ultra Amount | global | `goldUltraAmount_global` |
| 16 | 8 | 1000+ | Sorcerer + Necromancer + Deadeye | +8% Ultra Crit Chance | global | `ultraCritChance_global` |

## Archer

- Hero ID: 27
- Class: 2
- Rarity: 2

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Sorcerer | +10% Kill Gold | global | `killGold_global` |
| 2 | 1 | 0+ | Assassin + Forester | +3% Kill Exp | global | `killExp_global` |
| 3 | 2 | 15+ | Chieftain | +8% Crit Chance | global | `critChance_global` |
| 4 | 2 | 15+ | Spelldancer + Warden | +60% Damage | global | `damage_global` |
| 5 | 3 | 50+ | Warden | +22% Attack Speed | global | `attSpeed_global` |
| 6 | 3 | 50+ | Ninja + Rogue | +250% Crit Damage | personal | `critDmg_personal` |
| 7 | 4 | 100+ | Captain | +1% Energy Super Chance | global | `energySuperChance_global` |
| 8 | 4 | 100+ | Gladiator + Apprentice | +350% Kill Gold | personal | `killGold_personal` |
| 9 | 5 | 150+ | Crusader | +3% Skill Power | global | `skillPower_global` |
| 10 | 5 | 150+ | Champion + Warlock | +625% Gold Super Amount | global | `goldSuperAmount_global` |
| 11 | 6 | 250+ | Deadeye | +500% Damage | personal | `damage_personal` |
| 12 | 6 | 250+ | Militia + Titan | +2250% Ultra Crit Damage | global | `ultraCritDmg_global` |
| 13 | 7 | 500+ | Ranger | +20% Exp Super Amount | global | `expSuperAmount_global` |
| 14 | 7 | 500+ | Titan + Warlock | +10% Exp Super Chance | global | `expSuperChance_global` |
| 15 | 8 | 1000+ | Chieftain + Druid + Warlock | +7% Exp Ultra Chance | global | `expUltraChance_global` |
| 16 | 8 | 1000+ | Viking + Ballista + Veteran | +40% Skill Power | personal | `skillPower_personal` |

## Ranger

- Hero ID: 28
- Class: 2
- Rarity: 3

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Peacekeeper | +2% Skill Power | personal | `skillPower_personal` |
| 2 | 1 | 0+ | Elementalist + Arbalest | +3 Skill Duration | personal | `skillDuration_personal` |
| 3 | 2 | 15+ | Dicemaster | +10% Attack Speed | global | `attSpeed_global` |
| 4 | 2 | 15+ | Gladiator + Forester | +10% Kill Exp | global | `killExp_global` |
| 5 | 3 | 50+ | Assassin | +200% Damage | personal | `damage_personal` |
| 6 | 3 | 50+ | Skymage + Crusader | +250% Kill Gold | personal | `killGold_personal` |
| 7 | 4 | 100+ | Battlemage | +1 Energy Income | global | `energyIncome_global` |
| 8 | 4 | 100+ | Witch + Ballista | +15% Super Crit Chance | personal | `superCritChance_personal` |
| 9 | 5 | 150+ | Ninja | +8% Gold Super Chance | global | `goldSuperChance_global` |
| 10 | 5 | 150+ | Forester + Warden | +625% Super Crit Damage | global | `superCritDmg_global` |
| 11 | 6 | 250+ | Wizard | +250% Kill Gold | global | `killGold_global` |
| 12 | 6 | 250+ | Viking + Crusader | +275% Damage | global | `damage_global` |
| 13 | 7 | 500+ | Archer | +7% Skill Power | global | `skillPower_global` |
| 14 | 7 | 500+ | Dicemaster + Ballista | +10% Exp Super Chance | global | `expSuperChance_global` |
| 15 | 8 | 1000+ | Samurai + Berserker + Forester | +800% Boss Gold | global | `bossGold_global` |
| 16 | 8 | 1000+ | Chieftain + Druid + Elementalist | +75% Attack Speed | global | `attSpeed_global` |

## Arbalest

- Hero ID: 29
- Class: 2
- Rarity: 3

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Samurai | -2% Skill Cooldown | global | `skillCd_global` |
| 2 | 1 | 0+ | Elementalist + Ranger | +10% Crit Chance | personal | `critChance_personal` |
| 3 | 2 | 15+ | Druid | +40% Damage | global | `damage_global` |
| 4 | 2 | 15+ | Viking + Assassin | +1 Energy Income | global | `energyIncome_global` |
| 5 | 3 | 50+ | Templar | +20% Kill Exp | global | `killExp_global` |
| 6 | 3 | 50+ | Chieftain + Sniper | +100% Attack Speed | personal | `attSpeed_personal` |
| 7 | 4 | 100+ | Berserker | +850% Gold Super Amount | personal | `goldSuperAmount_personal` |
| 8 | 4 | 100+ | Hunter + Captain | +350% Kill Gold | personal | `killGold_personal` |
| 9 | 5 | 150+ | Sovereign | +400% Damage | personal | `damage_personal` |
| 10 | 5 | 150+ | Militia + Necromancer | +8% Energy Super Amount | global | `energySuperAmount_global` |
| 11 | 6 | 250+ | Titan | +2% Exp Ultra Chance | global | `expUltraChance_global` |
| 12 | 6 | 250+ | Captain + Veteran | +6% Skill Power | global | `skillPower_global` |
| 13 | 7 | 500+ | Ninja | +15% Energy Super Amount | global | `energySuperAmount_global` |
| 14 | 7 | 500+ | Militia + Spelldancer | +12% Power Mage Energy | global | `powerMageEnergy_global` |
| 15 | 8 | 1000+ | Peacekeeper + Warlord + Apprentice | +65% Energy Ultra Amount | global | `energyUltraAmount_global` |
| 16 | 8 | 1000+ | Militia + Ninja + Captain | +40% Skill Power | personal | `skillPower_personal` |

## Sniper

- Hero ID: 30
- Class: 2
- Rarity: 4

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Rogue | +25% Damage | personal | `damage_personal` |
| 2 | 1 | 0+ | Paladin + Spelldancer | +20% Crit Damage | global | `critDmg_global` |
| 3 | 2 | 15+ | Necromancer | +17% Crit Chance | personal | `critChance_personal` |
| 4 | 2 | 15+ | Apprentice + Elementalist | +15% Attack Speed | global | `attSpeed_global` |
| 5 | 3 | 50+ | Warlord | -25% Skill Cooldown | personal | `skillCd_personal` |
| 6 | 3 | 50+ | Chieftain + Arbalest | +100% Kill Gold | global | `killGold_global` |
| 7 | 4 | 100+ | Warden | +125% Kill Gold | global | `killGold_global` |
| 8 | 4 | 100+ | Paladin + Chieftain | +950% Super Crit Damage | personal | `superCritDmg_personal` |
| 9 | 5 | 150+ | Spelldancer | +400% Damage | personal | `damage_personal` |
| 10 | 5 | 150+ | Templar + Dicemaster | +200% Damage | global | `damage_global` |
| 11 | 6 | 250+ | Champion | +2% Ultra Crit Chance | global | `ultraCritChance_global` |
| 12 | 6 | 250+ | Praetorian + Apprentice | +4250% Ultra Crit Damage | personal | `ultraCritDmg_personal` |
| 13 | 7 | 500+ | Hunter | +850% Gold Super Amount | global | `goldSuperAmount_global` |
| 14 | 7 | 500+ | Battlemage + Crusader | +1600% Ultra Boss Damage | global | `ultraBossDmg_global` |
| 15 | 8 | 1000+ | Champion + Skymage + Veteran | +175% Attack Speed | personal | `attSpeed_personal` |
| 16 | 8 | 1000+ | Templar + Templar + Scout | +3250% Ultra Crit Damage | global | `ultraCritDmg_global` |

## Rogue

- Hero ID: 31
- Class: 2
- Rarity: 4

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Sniper | +3% Attack Speed | global | `attSpeed_global` |
| 2 | 1 | 0+ | Gladiator + Battlemage | +20% Damage | global | `damage_global` |
| 3 | 2 | 15+ | Ninja | -15% Skill Cooldown | personal | `skillCd_personal` |
| 4 | 2 | 15+ | Champion + Praetorian | +60% Kill Gold | global | `killGold_global` |
| 5 | 3 | 50+ | Captain | +16% Crit Chance | global | `critChance_global` |
| 6 | 3 | 50+ | Ninja + Archer | +35% Kill Exp | global | `killExp_global` |
| 7 | 4 | 100+ | Forester | +1% Skill Power | global | `skillPower_global` |
| 8 | 4 | 100+ | Druid + Dicemaster | +7% Exp Super Amount | global | `expSuperAmount_global` |
| 9 | 5 | 150+ | Veteran | +3% Energy Super Chance | global | `energySuperChance_global` |
| 10 | 5 | 150+ | Peacekeeper + Apprentice | +25% Gold Super Chance | personal | `goldSuperChance_personal` |
| 11 | 6 | 250+ | Captain | +500% Kill Gold | personal | `killGold_personal` |
| 12 | 6 | 250+ | Templar + Necromancer | +600% Damage | personal | `damage_personal` |
| 13 | 7 | 500+ | Elementalist | +850% Gold Super Amount | global | `goldSuperAmount_global` |
| 14 | 7 | 500+ | Ninja + Assassin | +20% Skill Power | personal | `skillPower_personal` |
| 15 | 8 | 1000+ | Paladin + Scout + Hunter | +800% Boss Gold | global | `bossGold_global` |
| 16 | 8 | 1000+ | Sovereign + Hunter + Crusader | +3250% Gold Ultra Amount | global | `goldUltraAmount_global` |

## Ballista

- Hero ID: 32
- Class: 2
- Rarity: 5

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Crusader | +25% Kill Gold | personal | `killGold_personal` |
| 2 | 1 | 0+ | Berserker + Chieftain | -4% Skill Cooldown | global | `skillCd_global` |
| 3 | 2 | 15+ | Sovereign | +100% Crit Damage | personal | `critDmg_personal` |
| 4 | 2 | 15+ | Peacekeeper + Warlord | +150% Damage | personal | `damage_personal` |
| 5 | 3 | 50+ | Scout | +8% Skill Power | personal | `skillPower_personal` |
| 6 | 3 | 50+ | Battlemage + Warden | +100% Attack Speed | personal | `attSpeed_personal` |
| 7 | 4 | 100+ | Samurai | +2% Exp Super Chance | global | `expSuperChance_global` |
| 8 | 4 | 100+ | Witch + Ranger | +150% Damage | global | `damage_global` |
| 9 | 5 | 150+ | Champion | +175% Kill Gold | global | `killGold_global` |
| 10 | 5 | 150+ | Spelldancer + Scout | +4% Skill Power | global | `skillPower_global` |
| 11 | 6 | 250+ | Gladiator | +25% Energy Ultra Amount | global | `energyUltraAmount_global` |
| 12 | 6 | 250+ | Sorcerer + Skymage | +3% Gold Ultra Chance | global | `goldUltraChance_global` |
| 13 | 7 | 500+ | Militia | +8% Exp Super Chance | global | `expSuperChance_global` |
| 14 | 7 | 500+ | Dicemaster + Ranger | +25% Exp Super Amount | global | `expSuperAmount_global` |
| 15 | 8 | 1000+ | Viking + Wizard + Necromancer | +30% Skill Power | personal | `skillPower_personal` |
| 16 | 8 | 1000+ | Viking + Archer + Veteran | +10% Exp Ultra Chance | global | `expUltraChance_global` |

## Crusader

- Hero ID: 33
- Class: 2
- Rarity: 5

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Ballista | -2% Skill Cooldown | global | `skillCd_global` |
| 2 | 1 | 0+ | Skymage + Warlock | +6% Attack Speed | global | `attSpeed_global` |
| 3 | 2 | 15+ | Warlord | +40% Kill Gold | global | `killGold_global` |
| 4 | 2 | 15+ | Paladin + Sorcerer | +150% Damage | personal | `damage_personal` |
| 5 | 3 | 50+ | Titan | +8 Skill Duration | personal | `skillDuration_personal` |
| 6 | 3 | 50+ | Skymage + Ranger | +50% Crit Chance | personal | `critChance_personal` |
| 7 | 4 | 100+ | Sovereign | +12% Skill Power | personal | `skillPower_personal` |
| 8 | 4 | 100+ | Militia + Champion | +4% Energy Super Amount | global | `energySuperAmount_global` |
| 9 | 5 | 150+ | Archer | +1100% Gold Super Amount | personal | `goldSuperAmount_personal` |
| 10 | 5 | 150+ | Praetorian + Sorcerer | +450% Kill Gold | personal | `killGold_personal` |
| 11 | 6 | 250+ | Hunter | +10 Skill Duration | personal | `skillDuration_personal` |
| 12 | 6 | 250+ | Viking + Ranger | +6% Skill Power | global | `skillPower_global` |
| 13 | 7 | 500+ | Wizard | +15% Skill Power | personal | `skillPower_personal` |
| 14 | 7 | 500+ | Battlemage + Sniper | +2000% Gold Super Amount | personal | `goldSuperAmount_personal` |
| 15 | 8 | 1000+ | Sovereign + Crusader + Crusader | +7% Gold Ultra Chance | global | `goldUltraChance_global` |
| 16 | 8 | 1000+ | Sovereign + Hunter + Rogue | +200% Attack Speed | personal | `attSpeed_personal` |

## Captain

- Hero ID: 34
- Class: 2
- Rarity: 6

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Templar | +10% Crit Damage | global | `critDmg_global` |
| 2 | 1 | 0+ | Warlord + Necromancer | +3% Skill Power | personal | `skillPower_personal` |
| 3 | 2 | 15+ | Forester | +5 Skill Duration | personal | `skillDuration_personal` |
| 4 | 2 | 15+ | Chieftain + Sovereign | +150% Kill Gold | personal | `killGold_personal` |
| 5 | 3 | 50+ | Rogue | +80% Attack Speed | personal | `attSpeed_personal` |
| 6 | 3 | 50+ | Militia + Warlock | +100% Damage | global | `damage_global` |
| 7 | 4 | 100+ | Archer | +10% Gold Super Chance | personal | `goldSuperChance_personal` |
| 8 | 4 | 100+ | Hunter + Arbalest | +150% Kill Gold | global | `killGold_global` |
| 9 | 5 | 150+ | Druid | +10% Exp Super Amount | global | `expSuperAmount_global` |
| 10 | 5 | 150+ | Assassin + Hunter | +10% Super Crit Chance | global | `superCritChance_global` |
| 11 | 6 | 250+ | Rogue | +5 Energy Income | global | `energyIncome_global` |
| 12 | 6 | 250+ | Arbalest + Veteran | +600% Damage | personal | `damage_personal` |
| 13 | 7 | 500+ | Peacekeeper | +15% Skill Power | personal | `skillPower_personal` |
| 14 | 7 | 500+ | Samurai + Druid | +6% Energy Super Chance | global | `energySuperChance_global` |
| 15 | 8 | 1000+ | Militia + Gladiator + Sorcerer | +30% Skill Power | personal | `skillPower_personal` |
| 16 | 8 | 1000+ | Militia + Ninja + Arbalest | +75% Attack Speed | global | `attSpeed_global` |

## Warden

- Hero ID: 35
- Class: 2
- Rarity: 6

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Necromancer | +2% Crit Chance | global | `critChance_global` |
| 2 | 1 | 0+ | Champion + Templar | +3% Kill Exp | global | `killExp_global` |
| 3 | 2 | 15+ | Titan | +40% Damage | global | `damage_global` |
| 4 | 2 | 15+ | Spelldancer + Archer | +6% Skill Power | personal | `skillPower_personal` |
| 5 | 3 | 50+ | Archer | +200% Kill Gold | personal | `killGold_personal` |
| 6 | 3 | 50+ | Battlemage + Ballista | -10% Skill Cooldown | global | `skillCd_global` |
| 7 | 4 | 100+ | Sniper | +850% Super Crit Damage | personal | `superCritDmg_personal` |
| 8 | 4 | 100+ | Samurai + Scout | +2% Skill Power | global | `skillPower_global` |
| 9 | 5 | 150+ | Elementalist | +400% Kill Gold | personal | `killGold_personal` |
| 10 | 5 | 150+ | Forester + Ranger | +450% Damage | personal | `damage_personal` |
| 11 | 6 | 250+ | Militia | +5% Gold Ultra Chance | personal | `goldUltraChance_personal` |
| 12 | 6 | 250+ | Peacekeeper + Sovereign | +3% Energy Ultra Chance | global | `energyUltraChance_global` |
| 13 | 7 | 500+ | Skymage | +850% Super Crit Damage | global | `superCritDmg_global` |
| 14 | 7 | 500+ | Witch + Necromancer | +150% Attack Speed | personal | `attSpeed_personal` |
| 15 | 8 | 1000+ | Ninja + Assassin + Elementalist | +12% Skill Power | global | `skillPower_global` |
| 16 | 8 | 1000+ | Peacekeeper + Gladiator + Berserker | +3250% Ultra Crit Damage | global | `ultraCritDmg_global` |

## Praetorian

- Hero ID: 36
- Class: 0
- Rarity: 7

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Sovereign | +2% Crit Chance | global | `critChance_global` |
| 2 | 1 | 0+ | Titan + Deadeye | +20% Kill Gold | global | `killGold_global` |
| 3 | 2 | 15+ | Warlock | +100% Damage | personal | `damage_personal` |
| 4 | 2 | 15+ | Champion + Rogue | +15% Attack Speed | global | `attSpeed_global` |
| 5 | 3 | 50+ | Dicemaster | +8% Skill Power | personal | `skillPower_personal` |
| 6 | 3 | 50+ | Paladin + Veteran | -30% Skill Cooldown | personal | `skillCd_personal` |
| 7 | 4 | 100+ | Ninja | +1 Energy Income | global | `energyIncome_global` |
| 8 | 4 | 100+ | Wizard + Battlemage | +15% Super Crit Chance | personal | `superCritChance_personal` |
| 9 | 5 | 150+ | Militia | +550% Super Crit Damage | global | `superCritDmg_global` |
| 10 | 5 | 150+ | Sorcerer + Crusader | +200% Damage | global | `damage_global` |
| 11 | 6 | 250+ | Samurai | +2000% Gold Ultra Amount | global | `goldUltraAmount_global` |
| 12 | 6 | 250+ | Apprentice + Sniper | +2250% Ultra Crit Damage | global | `ultraCritDmg_global` |
| 13 | 7 | 500+ | Necromancer | +125% Attack Speed | personal | `attSpeed_personal` |
| 14 | 7 | 500+ | Scout + Hunter | +8% Skill Power | global | `skillPower_global` |
| 15 | 8 | 1000+ | Titan + Dicemaster + Deadeye | +3000% Ultra Crit Damage | global | `ultraCritDmg_global` |
| 16 | 8 | 1000+ | Assassin + Wizard + Spelldancer | +20% Ultra Crit Chance | personal | `ultraCritChance_personal` |

## Titan

- Hero ID: 37
- Class: 0
- Rarity: 7

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Veteran | +2 Skill Duration | personal | `skillDuration_personal` |
| 2 | 1 | 0+ | Praetorian + Deadeye | -4% Skill Cooldown | global | `skillCd_global` |
| 3 | 2 | 15+ | Warden | +10% Attack Speed | global | `attSpeed_global` |
| 4 | 2 | 15+ | Wizard + Dicemaster | +150% Kill Gold | personal | `killGold_personal` |
| 5 | 3 | 50+ | Crusader | +200% Crit Damage | personal | `critDmg_personal` |
| 6 | 3 | 50+ | Sovereign + Deadeye | +100% Damage | global | `damage_global` |
| 7 | 4 | 100+ | Apprentice | +850% Super Crit Damage | personal | `superCritDmg_personal` |
| 8 | 4 | 100+ | Viking + Necromancer | +150% Kill Gold | global | `killGold_global` |
| 9 | 5 | 150+ | Warlord | +12% Skill Power | personal | `skillPower_personal` |
| 10 | 5 | 150+ | Berserker + Wizard | +4 Energy Income | global | `energyIncome_global` |
| 11 | 6 | 250+ | Arbalest | +500% Damage | personal | `damage_personal` |
| 12 | 6 | 250+ | Militia + Archer | +600% Kill Gold | personal | `killGold_personal` |
| 13 | 7 | 500+ | Witch | +300% Damage | global | `damage_global` |
| 14 | 7 | 500+ | Warlock + Archer | +8% Skill Power | global | `skillPower_global` |
| 15 | 8 | 1000+ | Praetorian + Dicemaster + Deadeye | +30% Skill Power | personal | `skillPower_personal` |
| 16 | 8 | 1000+ | Warlord + Warlock + Warlock | +3250% Ultra Crit Damage | global | `ultraCritDmg_global` |

## Sovereign

- Hero ID: 38
- Class: 1
- Rarity: 7

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Praetorian | -5% Skill Cooldown | personal | `skillCd_personal` |
| 2 | 1 | 0+ | Dicemaster + Veteran | +20% Damage | global | `damage_global` |
| 3 | 2 | 15+ | Ballista | +40% Crit Damage | global | `critDmg_global` |
| 4 | 2 | 15+ | Chieftain + Captain | +150% Kill Gold | personal | `killGold_personal` |
| 5 | 3 | 50+ | Warlock | +8% Skill Power | personal | `skillPower_personal` |
| 6 | 3 | 50+ | Titan + Deadeye | +1% Skill Power | global | `skillPower_global` |
| 7 | 4 | 100+ | Crusader | +125% Kill Gold | global | `killGold_global` |
| 8 | 4 | 100+ | Templar + Forester | +6% Gold Super Chance | global | `goldSuperChance_global` |
| 9 | 5 | 150+ | Arbalest | +8% Super Crit Chance | global | `superCritChance_global` |
| 10 | 5 | 150+ | Witch + Battlemage | +4 Energy Income | global | `energyIncome_global` |
| 11 | 6 | 250+ | Berserker | +45% Exp Ultra Amount | global | `expUltraAmount_global` |
| 12 | 6 | 250+ | Peacekeeper + Warden | +600% Damage | personal | `damage_personal` |
| 13 | 7 | 500+ | Warlock | +7% Skill Power | global | `skillPower_global` |
| 14 | 7 | 500+ | Chieftain + Elementalist | +925% Gold Super Amount | global | `goldSuperAmount_global` |
| 15 | 8 | 1000+ | Crusader + Crusader + Crusader | +3000% Gold Ultra Amount | global | `goldUltraAmount_global` |
| 16 | 8 | 1000+ | Hunter + Rogue + Crusader | +40% Skill Power | personal | `skillPower_personal` |

## Dicemaster

- Hero ID: 39
- Class: 1
- Rarity: 7

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Deadeye | +10% Attack Speed | personal | `attSpeed_personal` |
| 2 | 1 | 0+ | Sovereign + Veteran | -4% Skill Cooldown | global | `skillCd_global` |
| 3 | 2 | 15+ | Ranger | +5 Skill Duration | personal | `skillDuration_personal` |
| 4 | 2 | 15+ | Titan + Wizard | +150% Damage | personal | `damage_personal` |
| 5 | 3 | 50+ | Praetorian | +16% Crit Chance | global | `critChance_global` |
| 6 | 3 | 50+ | Viking + Sorcerer | +100% Kill Gold | global | `killGold_global` |
| 7 | 4 | 100+ | Skymage | +1 Energy Income | global | `energyIncome_global` |
| 8 | 4 | 100+ | Druid + Rogue | +500% Super Crit Damage | global | `superCritDmg_global` |
| 9 | 5 | 150+ | Assassin | +175% Damage | global | `damage_global` |
| 10 | 5 | 150+ | Templar + Sniper | +450% Kill Gold | personal | `killGold_personal` |
| 11 | 6 | 250+ | Warlord | +5% Gold Ultra Chance | personal | `goldUltraChance_personal` |
| 12 | 6 | 250+ | Elementalist + Scout | +3% Ultra Crit Chance | global | `ultraCritChance_global` |
| 13 | 7 | 500+ | Apprentice | +700% Damage | personal | `damage_personal` |
| 14 | 7 | 500+ | Ranger + Ballista | +25% Exp Super Amount | global | `expSuperAmount_global` |
| 15 | 8 | 1000+ | Praetorian + Titan + Deadeye | +60% Attack Speed | global | `attSpeed_global` |
| 16 | 8 | 1000+ | Apprentice + Witch + Skymage | +6500% Ultra Crit Damage | personal | `ultraCritDmg_personal` |

## Deadeye

- Hero ID: 40
- Class: 2
- Rarity: 7

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Dicemaster | -5% Skill Cooldown | personal | `skillCd_personal` |
| 2 | 1 | 0+ | Praetorian + Titan | +50% Damage | personal | `damage_personal` |
| 3 | 2 | 15+ | Templar | +5% Skill Power | personal | `skillPower_personal` |
| 4 | 2 | 15+ | Warlock + Veteran | +25% Crit Chance | personal | `critChance_personal` |
| 5 | 3 | 50+ | Samurai | +80% Kill Gold | global | `killGold_global` |
| 6 | 3 | 50+ | Titan + Sovereign | +30% Attack Speed | global | `attSpeed_global` |
| 7 | 4 | 100+ | Wizard | +125% Damage | global | `damage_global` |
| 8 | 4 | 100+ | Elementalist + Warlock | +500% Gold Super Amount | global | `goldSuperAmount_global` |
| 9 | 5 | 150+ | Viking | +175% Damage | global | `damage_global` |
| 10 | 5 | 150+ | Gladiator + Skymage | +10% Super Crit Chance | global | `superCritChance_global` |
| 11 | 6 | 250+ | Archer | +5% Ultra Crit Chance | personal | `ultraCritChance_personal` |
| 12 | 6 | 250+ | Battlemage + Forester | +275% Kill Gold | global | `killGold_global` |
| 13 | 7 | 500+ | Assassin | +15% Skill Power | personal | `skillPower_personal` |
| 14 | 7 | 500+ | Champion + Apprentice | +2000% Super Crit Damage | personal | `superCritDmg_personal` |
| 15 | 8 | 1000+ | Praetorian + Titan + Dicemaster | +7% Ultra Crit Chance | global | `ultraCritChance_global` |
| 16 | 8 | 1000+ | Sorcerer + Necromancer + Forester | +200% Attack Speed | personal | `attSpeed_personal` |

## Veteran

- Hero ID: 41
- Class: 2
- Rarity: 7

| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |
|---:|---:|---:|---|---|---|---|
| 1 | 1 | 0+ | Titan | +2 Skill Duration | personal | `skillDuration_personal` |
| 2 | 1 | 0+ | Sovereign + Dicemaster | +50% Kill Gold | personal | `killGold_personal` |
| 3 | 2 | 15+ | Berserker | +5% Skill Power | personal | `skillPower_personal` |
| 4 | 2 | 15+ | Warlock + Deadeye | +150% Crit Damage | personal | `critDmg_personal` |
| 5 | 3 | 50+ | Battlemage | +80% Damage | global | `damage_global` |
| 6 | 3 | 50+ | Paladin + Praetorian | -10% Skill Cooldown | global | `skillCd_global` |
| 7 | 4 | 100+ | Necromancer | +300% Damage | personal | `damage_personal` |
| 8 | 4 | 100+ | Warlord + Skymage | +7% Exp Super Amount | global | `expSuperAmount_global` |
| 9 | 5 | 150+ | Rogue | +1100% Super Crit Damage | personal | `superCritDmg_personal` |
| 10 | 5 | 150+ | Ninja + Chieftain | +7% Exp Super Chance | global | `expSuperChance_global` |
| 11 | 6 | 250+ | Spelldancer | +500% Kill Gold | personal | `killGold_personal` |
| 12 | 6 | 250+ | Arbalest + Captain | +6 Energy Income | global | `energyIncome_global` |
| 13 | 7 | 500+ | Templar | +20% Boss Exp | global | `bossExp_global` |
| 14 | 7 | 500+ | Viking + Forester | +25% Exp Super Amount | global | `expSuperAmount_global` |
| 15 | 8 | 1000+ | Champion + Skymage + Sniper | +12% Skill Power | global | `skillPower_global` |
| 16 | 8 | 1000+ | Viking + Archer + Ballista | +125% Exp Ultra Amount | global | `expUltraAmount_global` |
