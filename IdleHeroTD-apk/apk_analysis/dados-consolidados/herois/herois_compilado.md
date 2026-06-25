# Compilado de herois - Idle Hero TD

Compilado unico gerado dos dados extraidos do APK. Usa os valores base dos prefabs/MonoBehaviours; a UI do save pode mostrar valores diferentes por efeitos dinamicos de mapa, slot, pesquisas, upgrades, eventos ou bonus ativos.

## Fontes

- `csv/detalhes_herois.csv`: stats base, skill, cooldown, mastery, milestones e backstory.
- `csv/sinergias_por_heroi.csv`: sinergias extraidas dos MonoBehaviours `Hero`.
- `il2cpp_enums.csv`: nomes dos enums `HeroClass`, `HeroId` e `HeroUpgrade`.

## Resumo

- Herois: 42
- Sinergias: 672
- Classes: `0=Melee`, `1=Mage`, `2=Range`
- Rarity: valor numerico cru extraido do jogo.

## Indice rapido

| ID | Heroi | Classe | Rarity | Custo | DPS ratio | Atk speed | Range | Crit | Skill | Ativa | Cooldown | Efeito skill |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---|
| 0 | [#0 Militia](#0-militia) | Melee (0) | 1 | 5 | 1 | 1 | 0.9 | 1 | Spin Attack | 1s | 24s | +30% |
| 1 | [#1 Viking](#1-viking) | Melee (0) | 1 | 10 | 1.2 | 1.25 | 0.9 | 3 | Berserk | 10s | 24s | +10% |
| 2 | [#2 Ninja](#2-ninja) | Melee (0) | 2 | 50 | 1 | 1.75 | 0.8 | 8 | Sneak Attack | 10s | 20s | +50% |
| 3 | [#3 Assassin](#3-assassin) | Melee (0) | 2 | 100 | 1.2 | 1.5 | 0.8 | 5 | Execute | 10s | 32s | +1% |
| 4 | [#4 Peacekeeper](#4-peacekeeper) | Melee (0) | 3 | 500 | 0.9 | 0.9 | 1 | 5 | Incarcerate | 10s | 24s | +0.5% |
| 5 | [#5 Samurai](#5-samurai) | Melee (0) | 3 | 1000 | 1.2 | 1 | 0.9 | 5 | Immolation | 10s | 24s | +3% |
| 6 | [#6 Paladin](#6-paladin) | Melee (0) | 4 | 5000 | 1.4 | 0.5 | 1 | 3 | Splash | 10s | 28s | +3% |
| 7 | [#7 Gladiator](#7-gladiator) | Melee (0) | 4 | 10000 | 1.1 | 0.7 | 0.9 | 1 | Killjoy | 10s | 24s | +4% |
| 8 | [#8 Berserker](#8-berserker) | Melee (0) | 5 | 40000 | 1.4 | 1.5 | 0.8 | 5 | Cleave | 10s | 28s | +0.3x |
| 9 | [#9 Chieftain](#9-chieftain) | Melee (0) | 5 | 80000 | 1.3 | 0.8 | 1 | 5 | Ground Slam | 3s | 28s | +25% / +1% |
| 10 | [#10 Champion](#10-champion) | Melee (0) | 6 | 250000 | 1.3 | 1 | 0.9 | 3 | Lightning Storm | 3s | 24s | +0.5x / +10% |
| 11 | [#11 Warlord](#11-warlord) | Melee (0) | 6 | 500000 | 1.2 | 0.9 | 0.9 | 3 | Avatar | 10s | 24s | +10% / +5% / +1% |
| 12 | [#12 Apprentice](#12-apprentice) | Mage (1) | 1 | 5 | 1.1 | 0.75 | 1 | 1 | Slow | 10s | 24s | -3% |
| 13 | [#13 Druid](#13-druid) | Mage (1) | 1 | 10 | 1 | 0.9 | 1 | 1 | Damage Boost | 10s | 28s | +5% |
| 14 | [#14 Sorcerer](#14-sorcerer) | Mage (1) | 2 | 50 | 0.6 | 1 | 1.1 | 1 | Stun | 3s | 32s | +0.3x |
| 15 | [#15 Witch](#15-witch) | Mage (1) | 2 | 100 | 1.3 | 1 | 1 | 5 | Curse | 10s | 28s | +5% |
| 16 | [#16 Wizard](#16-wizard) | Mage (1) | 3 | 500 | 1.2 | 0.6 | 1 | 1 | Speed Boost | 10s | 28s | +5% |
| 17 | [#17 Elementalist](#17-elementalist) | Mage (1) | 3 | 1000 | 0.8 | 0.9 | 1.1 | 1 | Confuse | 3s | 32s | +0.3x |
| 18 | [#18 Battlemage](#18-battlemage) | Mage (1) | 4 | 5000 | 1.3 | 0.75 | 1 | 5 | Critical Boost | 10s | 28s | +1% |
| 19 | [#19 Spelldancer](#19-spelldancer) | Mage (1) | 4 | 10000 | 0.6 | 1 | 0.9 | 1 | Power Boost | 10s | 28s | +5% |
| 20 | [#20 Skymage](#20-skymage) | Mage (1) | 5 | 40000 | 0.8 | 0.5 | 1.1 | 1 | Teleport | 1s | 32s | +0.3x |
| 21 | [#21 Warlock](#21-warlock) | Mage (1) | 5 | 80000 | 1.4 | 0.75 | 1 | 3 | Cooldown Boost | 10s | 28s | +5% |
| 22 | [#22 Templar](#22-templar) | Mage (1) | 6 | 250000 | 0.8 | 0.6 | 1 | 1 | Splash Boost | 10s | 28s | +1% |
| 23 | [#23 Necromancer](#23-necromancer) | Mage (1) | 6 | 500000 | 0.9 | 0.9 | 1 | 1 | Chaos | 10s | 32s | +5% |
| 24 | [#24 Scout](#24-scout) | Range (2) | 1 | 5 | 1.3 | 1 | 1 | 3 | Pierce Shot | 1s | 20s | +75% |
| 25 | [#25 Hunter](#25-hunter) | Range (2) | 1 | 10 | 1 | 0.5 | 1.2 | 3 | Gold Lust | 1s | 20s | +20% |
| 26 | [#26 Forester](#26-forester) | Range (2) | 2 | 50 | 0.8 | 1 | 1.1 | 3 | Bleed | 10s | 20s | +15% |
| 27 | [#27 Archer](#27-archer) | Range (2) | 2 | 100 | 1 | 0.6 | 1.1 | 1 | Exp Bonus | 1s | 20s | +20% |
| 28 | [#28 Ranger](#28-ranger) | Range (2) | 3 | 500 | 1 | 0.5 | 1.2 | 5 | Gamble Shot | 10s | 24s | +25% |
| 29 | [#29 Arbalest](#29-arbalest) | Range (2) | 3 | 1000 | 1.2 | 0.9 | 1.1 | 1 | Energy Source | 1s | 28s | +1 |
| 30 | [#30 Sniper](#30-sniper) | Range (2) | 4 | 5000 | 1.3 | 0.5 | 1.2 | 3 | Explosive Shot | 1s | 24s | +50% |
| 31 | [#31 Rogue](#31-rogue) | Range (2) | 4 | 10000 | 0.9 | 1.3 | 1 | 3 | Gold Aura | 10s | 28s | +5% |
| 32 | [#32 Ballista](#32-ballista) | Range (2) | 5 | 40000 | 1.2 | 0.65 | 1.2 | 3 | Exp Aura | 10s | 28s | +5% |
| 33 | [#33 Crusader](#33-crusader) | Range (2) | 5 | 80000 | 0.7 | 0.9 | 1.1 | 1 | Golden Arrows | 10s | 24s | +5% |
| 34 | [#34 Captain](#34-captain) | Range (2) | 6 | 250000 | 0.8 | 1 | 1.2 | 1 | Energy Aura | 10s | 32s | +0.25 |
| 35 | [#35 Warden](#35-warden) | Range (2) | 6 | 500000 | 1.1 | 1 | 1.1 | 5 | Gatling Gun | 10s | 24s | +10% / +5% / +2% |
| 36 | [#36 Praetorian](#36-praetorian) | Melee (0) | 7 | 2500000 | 1.1 | 1 | 1 | 5 | Ion Blades | 10s | 28s | +1% / +5% |
| 37 | [#37 Titan](#37-titan) | Melee (0) | 7 | 5000000 | 1.2 | 0.8 | 0.9 | 5 | Super Aura | 10s | 32s | +0.2% / +1% |
| 38 | [#38 Sovereign](#38-sovereign) | Mage (1) | 7 | 2500000 | 0.8 | 0.8 | 1 | 1 | Jackpot | 10s | 28s | +0.2% / +1% |
| 39 | [#39 Dicemaster](#39-dicemaster) | Mage (1) | 7 | 5000000 | 1 | 0.7 | 1 | 5 | Feeling Lucky | 10s | 32s | +2% / +1% / +0.5% |
| 40 | [#40 Deadeye](#40-deadeye) | Range (2) | 7 | 2500000 | 1.1 | 1 | 1.2 | 5 | Divine Aim | 10s | 28s | +15% / +10% / +0.3% |
| 41 | [#41 Veteran](#41-veteran) | Range (2) | 7 | 5000000 | 1 | 0.8 | 1.1 | 3 | Exp Share | 10s | 32s | +0.2% / +0.5% |

## Herois detalhados

<a id="0-militia"></a>
### 0 - Militia

| Campo | Valor |
|---|---|
| GameObject | militia (1h sword medium) |
| Classe | Melee (0) |
| Rarity | 1 |
| Pronoun | him |
| Base cost | 5 |
| Base DPS ratio | 1 |
| Base attack speed | 1 |
| Base range ratio | 0.9 |
| Base crit chance | 1 |
| Skill | Spin Attack |
| Skill active time | 1s |
| Skill cooldown | 24s |
| Skill power bonus/effect | +30% |
| Skill duration effect | 0 |
| Skill mastery base req | 35000 |
| GameObject path id | 50703 |
| Hero behaviour path id | 306419 |
| Prefab hero path id | 306419 |
| Head icon path id | 2530 |
| Full icon path id | 2481 |

**Milestone upgrades**

1:damage_personal, 9:skillPower_personal, 8:critDmg_personal, 4:range_personal, 14:killExp_global, 9:skillPower_personal, 12:skillCd_personal, 2:attSpeed_global, 16:superCritChance_global, 26:goldSuperAmount_global, 0:damage_global, 35:expUltraAmount_global, 40:energyIncome_global, 38:energyUltraChance_global, 2:attSpeed_global, 23:ultraCritDmg_personal, 19:superCritDmg_personal

**Backstory**

Militia, originally a humble farmer, was thrust into the role of a soldier when his village faced imminent threat. Adapting quickly to his new life, he mastered the art of swordplay, particularly a devastating spinning attack that damages all nearby enemies. This self-taught technique, born from his days using farm tools, became his signature move on the battlefield, making him a whirlwind of steel in close combat. Despite his rough transition from plowshares to swords, Militia's resilience and quick learning have earned him respect among his peers. He stands as a fierce protector of his fellow villagers, embodying the spirit of a warrior who rose from the soil to defend his home.

**Sinergias**

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

<a id="1-viking"></a>
### 1 - Viking

| Campo | Valor |
|---|---|
| GameObject | viking (1h sword medium) |
| Classe | Melee (0) |
| Rarity | 1 |
| Pronoun | her |
| Base cost | 10 |
| Base DPS ratio | 1.2 |
| Base attack speed | 1.25 |
| Base range ratio | 0.9 |
| Base crit chance | 3 |
| Skill | Berserk |
| Skill active time | 10s |
| Skill cooldown | 24s |
| Skill power bonus/effect | +10% |
| Skill duration effect | 1 |
| Skill mastery base req | 25000 |
| GameObject path id | 70971 |
| Hero behaviour path id | 305535 |
| Prefab hero path id | 305535 |
| Head icon path id | 2592 |
| Full icon path id | 2605 |

**Milestone upgrades**

3:attSpeed_personal, 7:critDmg_global, 13:killGold_global, 0:damage_global, 9:skillPower_personal, 6:critChance_personal, 10:skillDuration_personal, 32:expSuperChance_global, 12:skillCd_personal, 4:range_personal, 1:damage_personal, 20:ultraCritChance_global, 31:goldUltraAmount_personal, 17:superCritChance_personal, 41:skillPower_global, 44:bossExp_global, 23:ultraCritDmg_personal

**Backstory**

Viking is an intrepid explorer and fierce warrior whose reputation extends far beyond her northern shores. Her explorations into unknown lands are matched only by her prowess in battle, where she employs a frenzy attack style that overwhelms her enemies with sheer ferocity and speed. Viking's adventures have not only charted new territories but also tested her mettle against a myriad of foes, earning her the respect and fear of all who hear her name. Her fearless nature and relentless combat style make her a legendary figure, as she carves a path of discovery and conquest across the world. Viking's spirit is as untamable as the wild seas she sails, embodying the true essence of her warrior ancestors.

**Sinergias**

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

<a id="2-ninja"></a>
### 2 - Ninja

| Campo | Valor |
|---|---|
| GameObject | ninja (dual daggers fast) |
| Classe | Melee (0) |
| Rarity | 2 |
| Pronoun | him |
| Base cost | 50 |
| Base DPS ratio | 1 |
| Base attack speed | 1.75 |
| Base range ratio | 0.8 |
| Base crit chance | 8 |
| Skill | Sneak Attack |
| Skill active time | 10s |
| Skill cooldown | 20s |
| Skill power bonus/effect | +50% |
| Skill duration effect | 1 |
| Skill mastery base req | 35000 |
| GameObject path id | 75441 |
| Hero behaviour path id | 312627 |
| Prefab hero path id | 312627 |
| Head icon path id | 2702 |
| Full icon path id | 2615 |

**Milestone upgrades**

4:range_personal, 5:critChance_global, 10:skillDuration_personal, 3:attSpeed_personal, 11:skillCd_global, 14:killExp_global, 9:skillPower_personal, 19:superCritDmg_personal, 25:goldSuperChance_personal, 0:damage_global, 40:energyIncome_global, 34:expUltraChance_global, 30:goldUltraAmount_global, 40:energyIncome_global, 26:goldSuperAmount_global, 37:energySuperAmount_global, 39:energyUltraAmount_global

**Backstory**

Ninja is a master of stealth and precision, wielding dual daggers with deadly expertise. His signature move, a swift and silent sneak attack, allows him to disable foes before they even realize he's there. Trained in the ancient arts of infiltration and assassination, Ninja moves like a shadow through the night, leaving no trace but the whisper of his blades. His reputation as a ghostly figure who strikes without warning has become a tale of caution among his enemies. With each mission, Ninja further cements his status as a formidable and elusive warrior, feared by those who stand against him and revered by those who seek his skills.

**Sinergias**

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

<a id="3-assassin"></a>
### 3 - Assassin

| Campo | Valor |
|---|---|
| GameObject | assassin (dual daggers fast) |
| Classe | Melee (0) |
| Rarity | 2 |
| Pronoun | her |
| Base cost | 100 |
| Base DPS ratio | 1.2 |
| Base attack speed | 1.5 |
| Base range ratio | 0.8 |
| Base crit chance | 5 |
| Skill | Execute |
| Skill active time | 10s |
| Skill cooldown | 32s |
| Skill power bonus/effect | +1% |
| Skill duration effect | 1 |
| Skill mastery base req | 25000 |
| GameObject path id | 57436 |
| Hero behaviour path id | 296877 |
| Prefab hero path id | 296877 |
| Head icon path id | 2609 |
| Full icon path id | 2567 |

**Milestone upgrades**

9:skillPower_personal, 0:damage_global, 6:critChance_personal, 11:skillCd_global, 3:attSpeed_personal, 4:range_personal, 7:critDmg_global, 26:goldSuperAmount_global, 32:expSuperChance_global, 10:skillDuration_personal, 21:ultraCritChance_personal, 0:damage_global, 35:expUltraAmount_global, 12:skillCd_personal, 1:damage_personal, 22:ultraCritDmg_global, 10:skillDuration_personal

**Backstory**

Assassin is renowned for her ability to execute enemies without a sound. Her lethal prowess is matched only by her ghost-like ability to vanish into the shadows immediately after striking, making her a whispered legend among the elite circles of espionage and sabotage. Trained from a young age in the dark arts of assassination, her movements are fluid and almost invisible, her attacks calculated to be fatal and swift. Her reputation as a flawless executioner makes her a highly sought-after figure for the most delicate and dangerous missions. Assassin embodies the essence of a shadow warrior, her very presence—or lack thereof—striking fear into the hearts of those marked by her chilling touch.

**Sinergias**

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

<a id="4-peacekeeper"></a>
### 4 - Peacekeeper

| Campo | Valor |
|---|---|
| GameObject | peacekeeper (1h sword medium) |
| Classe | Melee (0) |
| Rarity | 3 |
| Pronoun | him |
| Base cost | 500 |
| Base DPS ratio | 0.9 |
| Base attack speed | 0.9 |
| Base range ratio | 1 |
| Base crit chance | 5 |
| Skill | Incarcerate |
| Skill active time | 10s |
| Skill cooldown | 24s |
| Skill power bonus/effect | +0.5% |
| Skill duration effect | 1 |
| Skill mastery base req | 25000 |
| GameObject path id | 87791 |
| Hero behaviour path id | 316916 |
| Prefab hero path id | 316916 |
| Head icon path id | 2593 |
| Full icon path id | 2455 |

**Milestone upgrades**

10:skillDuration_personal, 8:critDmg_personal, 14:killExp_global, 5:critChance_global, 4:range_personal, 0:damage_global, 15:killGold_personal, 9:skillPower_personal, 12:skillCd_personal, 40:energyIncome_global, 22:ultraCritDmg_global, 28:goldUltraChance_global, 1:damage_personal, 26:goldSuperAmount_global, 30:goldUltraAmount_global, 50:battlepassExp_global, 23:ultraCritDmg_personal

**Backstory**

Peacekeeper is a seasoned warrior known for his role in decisively ending conflicts by targeting and neutralizing weakened enemies. His strategic prowess and combat efficiency ensure that battles are concluded quickly, minimizing further casualties. Trained to maintain order and peace, Peacekeeper operates with a blend of compassion and ruthlessness, choosing to strike only when necessary to prevent greater chaos. His nickname, "Merciful," reflects his method of sparing the strong from needless battle, while swiftly ending the suffering of the already defeated. In the eyes of many, Peacekeeper stands as both a harbinger of resolution and a protector, embodying a unique balance between mercy and warrior's duty.

**Sinergias**

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

<a id="5-samurai"></a>
### 5 - Samurai

| Campo | Valor |
|---|---|
| GameObject | samurai (1h sword fast) |
| Classe | Melee (0) |
| Rarity | 3 |
| Pronoun | her |
| Base cost | 1000 |
| Base DPS ratio | 1.2 |
| Base attack speed | 1 |
| Base range ratio | 0.9 |
| Base crit chance | 5 |
| Skill | Immolation |
| Skill active time | 10s |
| Skill cooldown | 24s |
| Skill power bonus/effect | +3% |
| Skill duration effect | 1 |
| Skill mastery base req | 35000 |
| GameObject path id | 22477 |
| Hero behaviour path id | 280121 |
| Prefab hero path id | 280121 |
| Head icon path id | 2745 |
| Full icon path id | 2753 |

**Milestone upgrades**

6:critChance_personal, 12:skillCd_personal, 9:skillPower_personal, 4:range_personal, 1:damage_personal, 13:killGold_global, 2:attSpeed_global, 10:skillDuration_personal, 18:superCritDmg_global, 33:expSuperAmount_global, 29:goldUltraChance_personal, 1:damage_personal, 34:expUltraChance_global, 17:superCritChance_personal, 9:skillPower_personal, 22:ultraCritDmg_global, 58:skillDuration_global

**Backstory**

Samurai is a master swordsman whose unparalleled skill allows her to strike multiple enemies with a single, fluid motion. Her technique, honed through years of disciplined training in the way of the sword, is both beautiful and deadly, a dance of blades that leaves foes bewildered and defeated. Her reputation as a fearsome warrior has spread far beyond her homeland, earning her respect and fear on any battlefield. Her ability to assess and react to the movements of several adversaries simultaneously makes her an invaluable asset in large skirmishes. Samurai embodies the spirit of the warrior, combining grace, precision, and lethal efficiency in every battle she enters.

**Sinergias**

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

<a id="6-paladin"></a>
### 6 - Paladin

| Campo | Valor |
|---|---|
| GameObject | paladin (2h hammer very slow) |
| Classe | Melee (0) |
| Rarity | 4 |
| Pronoun | her |
| Base cost | 5000 |
| Base DPS ratio | 1.4 |
| Base attack speed | 0.5 |
| Base range ratio | 1 |
| Base crit chance | 3 |
| Skill | Splash |
| Skill active time | 10s |
| Skill cooldown | 28s |
| Skill power bonus/effect | +3% |
| Skill duration effect | 1 |
| Skill mastery base req | 25000 |
| GameObject path id | 34840 |
| Hero behaviour path id | 283139 |
| Prefab hero path id | 283139 |
| Head icon path id | 2828 |
| Full icon path id | 2635 |

**Milestone upgrades**

15:killGold_personal, 10:skillDuration_personal, 1:damage_personal, 9:skillPower_personal, 2:attSpeed_global, 8:critDmg_personal, 11:skillCd_global, 16:superCritChance_global, 4:range_personal, 32:expSuperChance_global, 40:energyIncome_global, 30:goldUltraAmount_global, 0:damage_global, 2:attSpeed_global, 40:energyIncome_global, 26:goldSuperAmount_global, 13:killGold_global

**Backstory**

Paladin wields a massive, rune-etched hammer that devastates multiple enemies with each sweeping blow. Her strength and skill in battle are legendary, allowing her to control the flow of combat with thunderous strikes that resonate across the front lines. Trained as a knight in an ancient order, Paladin has adapted her order's teachings to maximize the destructive potential of her chosen weapon. Her presence in a fight is both a rallying point for her allies and a harbinger of defeat for her foes, as she embodies the relentless courage and unyielding force of a true paladin. With every swing of her hammer, she enforces justice and protects the innocent, her name synonymous with valor and power.

**Sinergias**

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

<a id="7-gladiator"></a>
### 7 - Gladiator

| Campo | Valor |
|---|---|
| GameObject | gladiator (1h axe slow) |
| Classe | Melee (0) |
| Rarity | 4 |
| Pronoun | him |
| Base cost | 10000 |
| Base DPS ratio | 1.1 |
| Base attack speed | 0.7 |
| Base range ratio | 0.9 |
| Base crit chance | 1 |
| Skill | Killjoy |
| Skill active time | 10s |
| Skill cooldown | 24s |
| Skill power bonus/effect | +4% |
| Skill duration effect | 1 |
| Skill mastery base req | 25000 |
| GameObject path id | 29879 |
| Hero behaviour path id | 295526 |
| Prefab hero path id | 295526 |
| Head icon path id | 2599 |
| Full icon path id | 2659 |

**Milestone upgrades**

7:critDmg_global, 3:attSpeed_personal, 4:range_personal, 10:skillDuration_personal, 13:killGold_global, 9:skillPower_personal, 6:critChance_personal, 0:damage_global, 33:expSuperAmount_global, 40:energyIncome_global, 23:ultraCritDmg_personal, 1:damage_personal, 29:goldUltraChance_personal, 17:superCritChance_personal, 3:attSpeed_personal, 18:superCritDmg_global, 23:ultraCritDmg_personal

**Backstory**

Gladiator rose from the harsh life of a slave to become a fearsome warrior, his strength growing with each enemy he defeats. In the arena, his prowess became legend, each victory fueling a physical transformation that enhanced his already formidable abilities. Now free, he channels the pain of his past into the heat of battle, where his increasing might serves as both a weapon and a shield. As he travels the lands, seeking to right the injustices of his former life, each confrontation adds to his strength, making him an ever more unstoppable force. Gladiator's journey from bondage to freedom is marked by the scars of battle and the countless foes he has overcome, his name echoing as a symbol of resilience and power.

**Sinergias**

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

<a id="8-berserker"></a>
### 8 - Berserker

| Campo | Valor |
|---|---|
| GameObject | berserker (dual axe fast) |
| Classe | Melee (0) |
| Rarity | 5 |
| Pronoun | her |
| Base cost | 40000 |
| Base DPS ratio | 1.4 |
| Base attack speed | 1.5 |
| Base range ratio | 0.8 |
| Base crit chance | 5 |
| Skill | Cleave |
| Skill active time | 10s |
| Skill cooldown | 28s |
| Skill power bonus/effect | +0.3x |
| Skill duration effect | 1 |
| Skill mastery base req | 25000 |
| GameObject path id | 35577 |
| Hero behaviour path id | 289330 |
| Prefab hero path id | 289330 |
| Head icon path id | 2814 |
| Full icon path id | 2761 |

**Milestone upgrades**

8:critDmg_personal, 14:killExp_global, 12:skillCd_personal, 5:critChance_global, 10:skillDuration_personal, 15:killGold_personal, 1:damage_personal, 4:range_personal, 2:attSpeed_global, 9:skillPower_personal, 31:goldUltraAmount_personal, 20:ultraCritChance_global, 0:damage_global, 41:skillPower_global, 30:goldUltraAmount_global, 23:ultraCritDmg_personal, 2:attSpeed_global

**Backstory**

Berserker wields dual axes with unmatched ferocity, unleashing a whirlwind of destruction upon her enemies. Her battle style is characterized by a relentless frenzy that allows her to strike multiple foes simultaneously, her axes slicing through the chaos of combat with lethal precision. This fearsome warrior draws on her intense rage and battle lust to overwhelm her opponents, turning the tide of battle with her sheer force of will and physical prowess. As she moves through the battlefield, her enemies falter under the storm of her attacks, marking her as a formidable presence feared and respected in equal measure. Berserker's reputation precedes her, a warning to any who would stand against her wild fury.

**Sinergias**

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

<a id="9-chieftain"></a>
### 9 - Chieftain

| Campo | Valor |
|---|---|
| GameObject | chieftan (1h sword slow) |
| Classe | Melee (0) |
| Rarity | 5 |
| Pronoun | him |
| Base cost | 80000 |
| Base DPS ratio | 1.3 |
| Base attack speed | 0.8 |
| Base range ratio | 1 |
| Base crit chance | 5 |
| Skill | Ground Slam |
| Skill active time | 3s |
| Skill cooldown | 28s |
| Skill power bonus/effect | +25% / +1% |
| Skill duration effect | 0.5 |
| Skill mastery base req | 35000 |
| GameObject path id | 10650 |
| Hero behaviour path id | 314374 |
| Prefab hero path id | 314374 |
| Head icon path id | 2840 |
| Full icon path id | 2693 |

**Milestone upgrades**

2:attSpeed_global, 1:damage_personal, 9:skillPower_personal, 7:critDmg_global, 14:killExp_global, 12:skillCd_personal, 4:range_personal, 25:goldSuperChance_personal, 10:skillDuration_personal, 17:superCritChance_personal, 0:damage_global, 30:goldUltraAmount_global, 35:expUltraAmount_global, 33:expSuperAmount_global, 0:damage_global, 40:energyIncome_global, 39:energyUltraAmount_global

**Backstory**

Chieftain commands respect as a formidable warrior chief renowned for his powerful ground slam attack that sends shockwaves through the ranks of his enemies. Leading his tribe with a mix of stern authority and unwavering courage, Chieftain's signature move is both a battle tactic and a symbol of his leadership, crushing the earth and enemy morale alike. His presence on the battlefield is magnetic, rallying his warriors with roars as deep as the tremors he creates. This ability not only devastates his foes but also fortifies the spirits of his tribe, reinforcing their belief in their chief's might and their cause. His legacy is written in the dust of shattered ground, a testament to his strength and the fierce loyalty he inspires.

**Sinergias**

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

<a id="10-champion"></a>
### 10 - Champion

| Campo | Valor |
|---|---|
| GameObject | champion (1h sword medium) |
| Classe | Melee (0) |
| Rarity | 6 |
| Pronoun | her |
| Base cost | 250000 |
| Base DPS ratio | 1.3 |
| Base attack speed | 1 |
| Base range ratio | 0.9 |
| Base crit chance | 3 |
| Skill | Lightning Storm |
| Skill active time | 3s |
| Skill cooldown | 24s |
| Skill power bonus/effect | +0.5x / +10% |
| Skill duration effect | 0 |
| Skill mastery base req | 35000 |
| GameObject path id | 63040 |
| Hero behaviour path id | 300301 |
| Prefab hero path id | 300301 |
| Head icon path id | 2472 |
| Full icon path id | 2476 |

**Milestone upgrades**

4:range_personal, 9:skillPower_personal, 2:attSpeed_global, 11:skillCd_global, 8:critDmg_personal, 15:killGold_personal, 5:critChance_global, 9:skillPower_personal, 1:damage_personal, 33:expSuperAmount_global, 22:ultraCritDmg_global, 0:damage_global, 29:goldUltraChance_personal, 34:expUltraChance_global, 40:energyIncome_global, 9:skillPower_personal, 12:skillCd_personal

**Backstory**

Champion stands as a formidable knight capable of summoning fierce lightning to strike down her enemies. Clad in armor that shimmers like storm clouds, she rides into battle, her sword crackling with electric energy that mirrors the intensity of her resolve. This rare ability to harness the storm not only devastates her foes but also bolsters the morale of her allies, who view her as a harbinger of victory. Champion's mastery of lightning and valorous heart have earned her prestigous titles, a knight revered not just for her power but for her unwavering commitment to justice. In every clash, her presence is as impactful as the thunderbolts she commands, leaving a trail of awe and respect in her wake.

**Sinergias**

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

<a id="11-warlord"></a>
### 11 - Warlord

| Campo | Valor |
|---|---|
| GameObject | warlord (1h sword medium) |
| Classe | Melee (0) |
| Rarity | 6 |
| Pronoun | him |
| Base cost | 500000 |
| Base DPS ratio | 1.2 |
| Base attack speed | 0.9 |
| Base range ratio | 0.9 |
| Base crit chance | 3 |
| Skill | Avatar |
| Skill active time | 10s |
| Skill cooldown | 24s |
| Skill power bonus/effect | +10% / +5% / +1% |
| Skill duration effect | 1 |
| Skill mastery base req | 25000 |
| GameObject path id | 65292 |
| Hero behaviour path id | 301908 |
| Prefab hero path id | 301908 |
| Head icon path id | 2757 |
| Full icon path id | 2451 |

**Milestone upgrades**

11:skillCd_global, 4:range_personal, 10:skillDuration_personal, 0:damage_global, 6:critChance_personal, 3:attSpeed_personal, 14:killExp_global, 9:skillPower_personal, 26:goldSuperAmount_global, 18:superCritDmg_global, 1:damage_personal, 40:energyIncome_global, 34:expUltraChance_global, 35:expUltraAmount_global, 2:attSpeed_global, 17:superCritChance_personal, 23:ultraCritDmg_personal

**Backstory**

Warlord is a seasoned military commander whose presence on the battlefield inspires both fear and awe. With each enemy encounter, he harnesses the chaos of combat to fuel his own formidable strength, growing more powerful as the battle rages on. His strategic genius and unbreakable will are manifest in his ability to turn the tide of war, rallying his troops with his escalating prowess. Warlord's reputation as an unstoppable force grows with each victory, solidifying his status as a legend among soldiers and adversaries alike. His knack for seizing the momentum of battle and converting it into raw power makes him a unique and daunting leader, truly deserving of the title Warlord.

**Sinergias**

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

<a id="12-apprentice"></a>
### 12 - Apprentice

| Campo | Valor |
|---|---|
| GameObject | apprentice (battle) |
| Classe | Mage (1) |
| Rarity | 1 |
| Pronoun | him |
| Base cost | 5 |
| Base DPS ratio | 1.1 |
| Base attack speed | 0.75 |
| Base range ratio | 1 |
| Base crit chance | 1 |
| Skill | Slow |
| Skill active time | 10s |
| Skill cooldown | 24s |
| Skill power bonus/effect | -3% |
| Skill duration effect | 1 |
| Skill mastery base req | 25000 |
| GameObject path id | 24321 |
| Hero behaviour path id | 277314 |
| Prefab hero path id | 277314 |
| Head icon path id | 2791 |
| Full icon path id | 2594 |

**Milestone upgrades**

3:attSpeed_personal, 11:skillCd_global, 6:critChance_personal, 9:skillPower_personal, 10:skillDuration_personal, 0:damage_global, 7:critDmg_global, 4:range_personal, 27:goldSuperAmount_personal, 33:expSuperAmount_global, 20:ultraCritChance_global, 34:expUltraChance_global, 1:damage_personal, 30:goldUltraAmount_global, 34:expUltraChance_global, 18:superCritDmg_global, 22:ultraCritDmg_global

**Backstory**

Apprentice is a young wizard in the early stages of mastering the arcane arts. His burgeoning ability to slow the movement and reactions of his enemies makes him a unique asset in conflicts, giving his more experienced allies a critical advantage. Under the tutelage of a sorceress, Apprentice is honing his skills, focusing on perfecting his time-altering spells. Despite his novice status, his eagerness to learn and innate talent for manipulating temporal energies inspire both curiosity and respect in his magical community. His journey is marked by rapid growth and the potential to become a formidable wizard, as he weaves slow magic with increasing confidence and precision.

**Sinergias**

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

<a id="13-druid"></a>
### 13 - Druid

| Campo | Valor |
|---|---|
| GameObject | druid (battle) |
| Classe | Mage (1) |
| Rarity | 1 |
| Pronoun | him |
| Base cost | 10 |
| Base DPS ratio | 1 |
| Base attack speed | 0.9 |
| Base range ratio | 1 |
| Base crit chance | 1 |
| Skill | Damage Boost |
| Skill active time | 10s |
| Skill cooldown | 28s |
| Skill power bonus/effect | +5% |
| Skill duration effect | 1 |
| Skill mastery base req | 25000 |
| GameObject path id | 75730 |
| Hero behaviour path id | 285341 |
| Prefab hero path id | 285341 |
| Head icon path id | 2790 |
| Full icon path id | 2678 |

**Milestone upgrades**

10:skillDuration_personal, 1:damage_personal, 13:killGold_global, 8:critDmg_personal, 4:range_personal, 9:skillPower_personal, 14:killExp_global, 11:skillCd_global, 16:superCritChance_global, 2:attSpeed_global, 29:goldUltraChance_personal, 40:energyIncome_global, 0:damage_global, 35:expUltraAmount_global, 30:goldUltraAmount_global, 9:skillPower_personal, 18:superCritDmg_global

**Backstory**

Druid is a battlemage whose mystical powers amplify the destructive force of his allies. With a deep connection to ancient forces, he casts spells that infuse his army's weapons with elemental fury, turning simple blows into devastating strikes. His ability to enhance combat effectiveness has made him a revered figure in battles, where his presence alone can shift the dynamics in favor of his side. Druid's strategic use of his magic, coupled with his calm demeanor under pressure, earns him the loyalty and trust of those he leads. His unique blend of wizardry and battlefield command ensures that any force he accompanies is a formidable threat to its foes.

**Sinergias**

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

<a id="14-sorcerer"></a>
### 14 - Sorcerer

| Campo | Valor |
|---|---|
| GameObject | sorcerer (support) |
| Classe | Mage (1) |
| Rarity | 2 |
| Pronoun | her |
| Base cost | 50 |
| Base DPS ratio | 0.6 |
| Base attack speed | 1 |
| Base range ratio | 1.1 |
| Base crit chance | 1 |
| Skill | Stun |
| Skill active time | 3s |
| Skill cooldown | 32s |
| Skill power bonus/effect | +0.3x |
| Skill duration effect | 0.3 |
| Skill mastery base req | 25000 |
| GameObject path id | 79830 |
| Hero behaviour path id | 311478 |
| Prefab hero path id | 311478 |
| Head icon path id | 2776 |
| Full icon path id | 2837 |

**Milestone upgrades**

9:skillPower_personal, 7:critDmg_global, 0:damage_global, 14:killExp_global, 13:killGold_global, 3:attSpeed_personal, 12:skillCd_personal, 17:superCritChance_personal, 4:range_personal, 10:skillDuration_personal, 1:damage_personal, 35:expUltraAmount_global, 31:goldUltraAmount_personal, 30:goldUltraAmount_global, 2:attSpeed_global, 22:ultraCritDmg_global, 10:skillDuration_personal

**Backstory**

Sorcerer commands the rare and formidable power to incapacitate her enemies with bolts of stunning magic. With precision and grace, she weaves spells that disrupt her adversaries' senses, leaving them dazed and vulnerable to further attack. Her unique ability not only makes her a pivotal figure in combat but also a guardian of her mystical community, where her skills ensure safety and order. Sorcerer's mastery of stunning spells, combined with her strategic acumen, has earned her both respect and a touch of fear from those who know of her capabilities. Her presence on any battlefield is a signal of control and dominance, making her an indispensable ally in any conflict.

**Sinergias**

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

<a id="15-witch"></a>
### 15 - Witch

| Campo | Valor |
|---|---|
| GameObject | witch (support) |
| Classe | Mage (1) |
| Rarity | 2 |
| Pronoun | her |
| Base cost | 100 |
| Base DPS ratio | 1.3 |
| Base attack speed | 1 |
| Base range ratio | 1 |
| Base crit chance | 5 |
| Skill | Curse |
| Skill active time | 10s |
| Skill cooldown | 28s |
| Skill power bonus/effect | +5% |
| Skill duration effect | 1 |
| Skill mastery base req | 35000 |
| GameObject path id | 89428 |
| Hero behaviour path id | 318062 |
| Prefab hero path id | 318062 |
| Head icon path id | 2802 |
| Full icon path id | 2738 |

**Milestone upgrades**

2:attSpeed_global, 5:critChance_global, 4:range_personal, 1:damage_personal, 12:skillCd_personal, 15:killGold_personal, 8:critDmg_personal, 10:skillDuration_personal, 32:expSuperChance_global, 9:skillPower_personal, 28:goldUltraChance_global, 0:damage_global, 21:ultraCritChance_personal, 41:skillPower_global, 30:goldUltraAmount_global, 16:superCritChance_global, 22:ultraCritDmg_global

**Backstory**

Witch wields the dark art of cursing with unnerving precision. Her ability to cast spells that bring misfortune, confusion, and fear upon her enemies has made her a figure of both awe and dread. From her secluded hut in the dark forests, she concocts potions and incantations that weave destinies of despair for those who cross her path. Witch's mastery of curses is not only a weapon but also a shield, deterring those who would dare threaten her solitude. Her reputation ensures that she is approached with caution and respect, for to invoke her wrath is to court disaster.

**Sinergias**

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

<a id="16-wizard"></a>
### 16 - Wizard

| Campo | Valor |
|---|---|
| GameObject | wizard (battle) |
| Classe | Mage (1) |
| Rarity | 3 |
| Pronoun | him |
| Base cost | 500 |
| Base DPS ratio | 1.2 |
| Base attack speed | 0.6 |
| Base range ratio | 1 |
| Base crit chance | 1 |
| Skill | Speed Boost |
| Skill active time | 10s |
| Skill cooldown | 28s |
| Skill power bonus/effect | +5% |
| Skill duration effect | 1 |
| Skill mastery base req | 25000 |
| GameObject path id | 62437 |
| Hero behaviour path id | 300064 |
| Prefab hero path id | 300064 |
| Head icon path id | 2487 |
| Full icon path id | 2707 |

**Milestone upgrades**

4:range_personal, 14:killExp_global, 7:critDmg_global, 10:skillDuration_personal, 6:critChance_personal, 11:skillCd_global, 2:attSpeed_global, 9:skillPower_personal, 24:goldSuperChance_global, 1:damage_personal, 40:energyIncome_global, 22:ultraCritDmg_global, 35:expUltraAmount_global, 2:attSpeed_global, 10:skillDuration_personal, 41:skillPower_global, 0:damage_global

**Backstory**

Wizard possesses a remarkable magical talent for accelerating the actions and reactions of his allies. With carefully crafted spells, he can enhance the speed and agility of those around him, allowing them to move and think faster than their adversaries during critical moments. This ability has made him an invaluable asset in both battles and strategic operations, where split-second decisions can mean the difference between victory and defeat. Wizard's mastery of time-altering magic not only boosts his companions' effectiveness but also turns the tide in tight situations, earning him the respect and admiration of generals and soldiers alike. His presence on the battlefield is a promise of swift action, giving his side a palpable advantage.

**Sinergias**

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

<a id="17-elementalist"></a>
### 17 - Elementalist

| Campo | Valor |
|---|---|
| GameObject | elementalist (support) |
| Classe | Mage (1) |
| Rarity | 3 |
| Pronoun | her |
| Base cost | 1000 |
| Base DPS ratio | 0.8 |
| Base attack speed | 0.9 |
| Base range ratio | 1.1 |
| Base crit chance | 1 |
| Skill | Confuse |
| Skill active time | 3s |
| Skill cooldown | 32s |
| Skill power bonus/effect | +0.3x |
| Skill duration effect | 0.3 |
| Skill mastery base req | 25000 |
| GameObject path id | 19467 |
| Hero behaviour path id | 274390 |
| Prefab hero path id | 274390 |
| Head icon path id | 2471 |
| Full icon path id | 2799 |

**Milestone upgrades**

0:damage_global, 10:skillDuration_personal, 9:skillPower_personal, 4:range_personal, 3:attSpeed_personal, 5:critChance_global, 15:killGold_personal, 19:superCritDmg_personal, 33:expSuperAmount_global, 40:energyIncome_global, 1:damage_personal, 34:expUltraChance_global, 30:goldUltraAmount_global, 26:goldSuperAmount_global, 16:superCritChance_global, 54:goblinHoarderGold_global, 13:killGold_global

**Backstory**

Elementalist wields her profound mastery over elemental magic to disorient and confuse her adversaries in battle. With a mere flick of her wrist, she can manipulate air to distort sounds, water to blur visions, and earth to shift unexpectedly underfoot, leaving her enemies bewildered and vulnerable. Her ability to intertwine her spells with the natural elements creates chaotic battlefields where only her allies stand firm, guided by her subtle signals. Elementalist's reputation as a cunning and unpredictable mage precedes her, making her a respected figure in any strategy council. Her unique approach to combat, which turns the environment itself into a labyrinth of confusion, has thwarted many would-be conquerors and established her as a formidable protector of her homeland.

**Sinergias**

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

<a id="18-battlemage"></a>
### 18 - Battlemage

| Campo | Valor |
|---|---|
| GameObject | battlemage (battle) |
| Classe | Mage (1) |
| Rarity | 4 |
| Pronoun | him |
| Base cost | 5000 |
| Base DPS ratio | 1.3 |
| Base attack speed | 0.75 |
| Base range ratio | 1 |
| Base crit chance | 5 |
| Skill | Critical Boost |
| Skill active time | 10s |
| Skill cooldown | 28s |
| Skill power bonus/effect | +1% |
| Skill duration effect | 1 |
| Skill mastery base req | 25000 |
| GameObject path id | 76357 |
| Hero behaviour path id | 309008 |
| Prefab hero path id | 309008 |
| Head icon path id | 2695 |
| Full icon path id | 2662 |

**Milestone upgrades**

6:critChance_personal, 9:skillPower_personal, 2:attSpeed_global, 15:killGold_personal, 1:damage_personal, 14:killExp_global, 10:skillDuration_personal, 12:skillCd_personal, 18:superCritDmg_global, 4:range_personal, 28:goldUltraChance_global, 40:energyIncome_global, 0:damage_global, 30:goldUltraAmount_global, 35:expUltraAmount_global, 20:ultraCritChance_global, 9:skillPower_personal

**Backstory**

Battlemage wields magic that fortifies and amplifies the strength of his comrades during combat. His presence on the battlefield is a beacon of power, as he casts intricate spells that envelop his allies in auras of might and resilience. With a deep understanding of both arcane energies and martial tactics, Battlemage strategically positions himself to maximize the effectiveness of his enhancements, turning ordinary soldiers into formidable warriors. Revered for his leadership and feared for his battlefield acumen, Battlemage's abilities not only ensure the upper hand in skirmishes but also inspire courage and unity among those he fights alongside. His role as a force multiplier has made him a key figure in many historic victories, securing his legend as both protector and enhancer.

**Sinergias**

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

<a id="19-spelldancer"></a>
### 19 - Spelldancer

| Campo | Valor |
|---|---|
| GameObject | spelldancer (support) |
| Classe | Mage (1) |
| Rarity | 4 |
| Pronoun | her |
| Base cost | 10000 |
| Base DPS ratio | 0.6 |
| Base attack speed | 1 |
| Base range ratio | 0.9 |
| Base crit chance | 1 |
| Skill | Power Boost |
| Skill active time | 10s |
| Skill cooldown | 28s |
| Skill power bonus/effect | +5% |
| Skill duration effect | 1 |
| Skill mastery base req | 25000 |
| GameObject path id | 14745 |
| Hero behaviour path id | 271770 |
| Prefab hero path id | 271770 |
| Head icon path id | 2731 |
| Full icon path id | 2746 |

**Milestone upgrades**

12:skillCd_personal, 4:range_personal, 10:skillDuration_personal, 14:killExp_global, 9:skillPower_personal, 8:critDmg_personal, 13:killGold_global, 3:attSpeed_personal, 0:damage_global, 16:superCritChance_global, 34:expUltraChance_global, 1:damage_personal, 31:goldUltraAmount_personal, 2:attSpeed_global, 0:damage_global, 22:ultraCritDmg_global, 9:skillPower_personal

**Backstory**

Spelldancer is a mesmerizing mage whose dances enhance the abilities of her allies. As she moves gracefully through intricate routines, her motions weave potent spells that elevate strength, speed, and magical power, turning the tide of any encounter. Her performances, both in battle and during ceremonial rites, are not only beautiful but also strategic, fostering unity and amplifying the collective might of those around her. Spelldancer's unique blend of art and magic has made her a beloved figure, celebrated for turning combat into a ballet of enhanced prowess and shared victories. Her presence is a symbol of hope and strength, inspiring all who witness her dance to reach beyond their limits.

**Sinergias**

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

<a id="20-skymage"></a>
### 20 - Skymage

| Campo | Valor |
|---|---|
| GameObject | skymage (support) |
| Classe | Mage (1) |
| Rarity | 5 |
| Pronoun | her |
| Base cost | 40000 |
| Base DPS ratio | 0.8 |
| Base attack speed | 0.5 |
| Base range ratio | 1.1 |
| Base crit chance | 1 |
| Skill | Teleport |
| Skill active time | 1s |
| Skill cooldown | 32s |
| Skill power bonus/effect | +0.3x |
| Skill duration effect | 0 |
| Skill mastery base req | 35000 |
| GameObject path id | 24773 |
| Hero behaviour path id | 280408 |
| Prefab hero path id | 280408 |
| Head icon path id | 2670 |
| Full icon path id | 2782 |

**Milestone upgrades**

7:critDmg_global, 14:killExp_global, 9:skillPower_personal, 6:critChance_personal, 11:skillCd_global, 4:range_personal, 0:damage_global, 9:skillPower_personal, 40:energyIncome_global, 25:goldSuperChance_personal, 23:ultraCritDmg_personal, 1:damage_personal, 34:expUltraChance_global, 26:goldSuperAmount_global, 2:attSpeed_global, 18:superCritDmg_global, 22:ultraCritDmg_global

**Backstory**

Skymage is a sorceress with the rare ability to teleport herself and others across vast distances in the blink of an eye. Her talent for spatial magic makes her an invaluable ally in times of crisis, allowing her to whisk away those in danger or position forces strategically in battle. Beyond her tactical uses, Skymage’s powers have made her a bridge between isolated communities, enhancing trade and communication. Her unique skillset, coupled with a benevolent spirit, has earned her a reputation as a guardian of peace and a pioneer in magical transportation.

**Sinergias**

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

<a id="21-warlock"></a>
### 21 - Warlock

| Campo | Valor |
|---|---|
| GameObject | warlock (battle) |
| Classe | Mage (1) |
| Rarity | 5 |
| Pronoun | him |
| Base cost | 80000 |
| Base DPS ratio | 1.4 |
| Base attack speed | 0.75 |
| Base range ratio | 1 |
| Base crit chance | 3 |
| Skill | Cooldown Boost |
| Skill active time | 10s |
| Skill cooldown | 28s |
| Skill power bonus/effect | +5% |
| Skill duration effect | 1 |
| Skill mastery base req | 25000 |
| GameObject path id | 40729 |
| Hero behaviour path id | 287059 |
| Prefab hero path id | 287059 |
| Head icon path id | 2521 |
| Full icon path id | 2551 |

**Milestone upgrades**

14:killExp_global, 1:damage_personal, 5:critChance_global, 2:attSpeed_global, 8:critDmg_personal, 10:skillDuration_personal, 4:range_personal, 11:skillCd_global, 9:skillPower_personal, 26:goldSuperAmount_global, 40:energyIncome_global, 21:ultraCritChance_personal, 38:energyUltraChance_global, 16:superCritChance_global, 5:critChance_global, 39:energyUltraAmount_global, 61:instantSpell_accelerate

**Backstory**

Warlock, born in the mystical reaches of the Shadowlands, stands apart with his unique magical prowess as a shaman who can drastically increase the speed of spellcasting. This rare ability allows him to weave complex spells faster than his adversaries can react, making him a formidable foe in battle and a highly valued ally. His deep connection to the spiritual realm enhances this power, granting him insights that guide his tribe through both mystical and mundane challenges. Revered for his strategic mind and mystical skills, Warlock is not only a protector but also a visionary, leading his people with a blend of ancient wisdom and innovative magic.

**Sinergias**

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

<a id="22-templar"></a>
### 22 - Templar

| Campo | Valor |
|---|---|
| GameObject | templar (support) |
| Classe | Mage (1) |
| Rarity | 6 |
| Pronoun | her |
| Base cost | 250000 |
| Base DPS ratio | 0.8 |
| Base attack speed | 0.6 |
| Base range ratio | 1 |
| Base crit chance | 1 |
| Skill | Splash Boost |
| Skill active time | 10s |
| Skill cooldown | 28s |
| Skill power bonus/effect | +1% |
| Skill duration effect | 1 |
| Skill mastery base req | 25000 |
| GameObject path id | 64014 |
| Hero behaviour path id | 304679 |
| Prefab hero path id | 304679 |
| Head icon path id | 2763 |
| Full icon path id | 2504 |

**Milestone upgrades**

4:range_personal, 3:attSpeed_personal, 12:skillCd_personal, 9:skillPower_personal, 14:killExp_global, 0:damage_global, 6:critChance_personal, 24:goldSuperChance_global, 10:skillDuration_personal, 18:superCritDmg_global, 35:expUltraAmount_global, 1:damage_personal, 40:energyIncome_global, 2:attSpeed_global, 30:goldUltraAmount_global, 57:range_global, 60:instantSpell_agility

**Backstory**

Templar serves as a distinguished mage within the royal guard. Her unique magical expertise allows her to enchant her allies' weapons with splash damage, amplifying their effectiveness in battle. This rare ability makes her an invaluable asset in group combat, where she strategically positions herself to maximize the impact of her spells. Beyond her combat roles, Templar is respected among her peers for her keen intellect and unwavering loyalty to the crown. Her presence not only bolsters the kingdom's defenses but also inspires her fellow mages to explore new magical synergies.

**Sinergias**

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

<a id="23-necromancer"></a>
### 23 - Necromancer

| Campo | Valor |
|---|---|
| GameObject | necromancer (battle) |
| Classe | Mage (1) |
| Rarity | 6 |
| Pronoun | him |
| Base cost | 500000 |
| Base DPS ratio | 0.9 |
| Base attack speed | 0.9 |
| Base range ratio | 1 |
| Base crit chance | 1 |
| Skill | Chaos |
| Skill active time | 10s |
| Skill cooldown | 32s |
| Skill power bonus/effect | +5% |
| Skill duration effect | 1 |
| Skill mastery base req | 25000 |
| GameObject path id | 26880 |
| Hero behaviour path id | 278537 |
| Prefab hero path id | 278537 |
| Head icon path id | 2492 |
| Full icon path id | 2612 |

**Milestone upgrades**

8:critDmg_personal, 15:killGold_personal, 4:range_personal, 10:skillDuration_personal, 2:attSpeed_global, 14:killExp_global, 9:skillPower_personal, 1:damage_personal, 16:superCritChance_global, 12:skillCd_personal, 0:damage_global, 28:goldUltraChance_global, 32:expSuperChance_global, 30:goldUltraAmount_global, 34:expUltraChance_global, 41:skillPower_global, 0:damage_global

**Backstory**

Necromancer wields the dark art of summoning chaos, casting a shadow over the lands he traverses. This enigmatic wizard harnesses the turbulent energies of the void, conjuring storms of entropy that disrupt order and bend the fabric of reality. His presence alone can unsettle the most serene settings, making him both feared and revered in the arcane community. Known for his deep, haunting voice and the ever-present swirl of dark mist around him, Necromancer is a figure of intrigue and power, drawing both curiosity and caution from those who cross his path. His mastery of chaos not only makes him a formidable adversary but also a catalyst for change wherever he goes.

**Sinergias**

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

<a id="24-scout"></a>
### 24 - Scout

| Campo | Valor |
|---|---|
| GameObject | scout (fast) |
| Classe | Range (2) |
| Rarity | 1 |
| Pronoun | him |
| Base cost | 5 |
| Base DPS ratio | 1.3 |
| Base attack speed | 1 |
| Base range ratio | 1 |
| Base crit chance | 3 |
| Skill | Pierce Shot |
| Skill active time | 1s |
| Skill cooldown | 20s |
| Skill power bonus/effect | +75% |
| Skill duration effect | 0 |
| Skill mastery base req | 35000 |
| GameObject path id | 88985 |
| Hero behaviour path id | 317780 |
| Prefab hero path id | 317780 |
| Head icon path id | 2576 |
| Full icon path id | 2532 |

**Milestone upgrades**

13:killGold_global, 3:attSpeed_personal, 0:damage_global, 12:skillCd_personal, 9:skillPower_personal, 9:skillPower_personal, 5:critChance_global, 19:superCritDmg_personal, 40:energyIncome_global, 32:expSuperChance_global, 1:damage_personal, 28:goldUltraChance_global, 35:expUltraAmount_global, 3:attSpeed_personal, 0:damage_global, 30:goldUltraAmount_global, 26:goldSuperAmount_global

**Backstory**

Scout is a novice archer whose natural talent and keen eye make his pierce shot attack particularly deadly. Despite his youth and relative inexperience, he has quickly gained a reputation for his ability to hit targets at impressive distances, often piercing through the thickest armor with a single arrow. His agility and sharp instincts are complemented by a growing prowess with the bow, making him a valuable asset in any skirmish or battle. As he traverses the battlefield, Scout’s swift movements and precise shots instill both hope in his allies and dread in his foes. His dedication to mastering archery promises a future where his name will be synonymous with the legends of great marksmen.

**Sinergias**

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

<a id="25-hunter"></a>
### 25 - Hunter

| Campo | Valor |
|---|---|
| GameObject | hunter (slow) |
| Classe | Range (2) |
| Rarity | 1 |
| Pronoun | him |
| Base cost | 10 |
| Base DPS ratio | 1 |
| Base attack speed | 0.5 |
| Base range ratio | 1.2 |
| Base crit chance | 3 |
| Skill | Gold Lust |
| Skill active time | 1s |
| Skill cooldown | 20s |
| Skill power bonus/effect | +20% |
| Skill duration effect | 0 |
| Skill mastery base req | 35000 |
| GameObject path id | 71439 |
| Hero behaviour path id | 294026 |
| Prefab hero path id | 294026 |
| Head icon path id | 2821 |
| Full icon path id | 2596 |

**Milestone upgrades**

6:critChance_personal, 7:critDmg_global, 2:attSpeed_global, 9:skillPower_personal, 4:range_personal, 14:killExp_global, 1:damage_personal, 24:goldSuperChance_global, 11:skillCd_global, 9:skillPower_personal, 20:ultraCritChance_global, 0:damage_global, 34:expUltraChance_global, 9:skillPower_personal, 27:goldSuperAmount_personal, 53:instantSkillChance_personal, 30:goldUltraAmount_global

**Backstory**

Hunter is an archer renowned for his uncanny ability to turn each successful kill into a bounty of gold. His prowess with the bow is not just a means of defense but a profitable venture, as he expertly tracks and eliminates high-value targets. This unique skill has made him a legend among mercenaries and treasure seekers alike. As he navigates through dangerous terrains, his keen eyes and steady hands ensure that no opportunity for gain is missed. Hunter's reputation as both a deadly archer and a cunning opportunist continues to grow, as he skillfully blends the art of survival with the lucrative business of bounty hunting.

**Sinergias**

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

<a id="26-forester"></a>
### 26 - Forester

| Campo | Valor |
|---|---|
| GameObject | forester (fast) |
| Classe | Range (2) |
| Rarity | 2 |
| Pronoun | her |
| Base cost | 50 |
| Base DPS ratio | 0.8 |
| Base attack speed | 1 |
| Base range ratio | 1.1 |
| Base crit chance | 3 |
| Skill | Bleed |
| Skill active time | 10s |
| Skill cooldown | 20s |
| Skill power bonus/effect | +15% |
| Skill duration effect | 1 |
| Skill mastery base req | 25000 |
| GameObject path id | 81140 |
| Hero behaviour path id | 314946 |
| Prefab hero path id | 314946 |
| Head icon path id | 2680 |
| Full icon path id | 2687 |

**Milestone upgrades**

8:critDmg_personal, 9:skillPower_personal, 15:killGold_personal, 0:damage_global, 5:critChance_global, 3:attSpeed_personal, 4:range_personal, 32:expSuperChance_global, 10:skillDuration_personal, 12:skillCd_personal, 31:goldUltraAmount_personal, 22:ultraCritDmg_global, 40:energyIncome_global, 34:expUltraChance_global, 16:superCritChance_global, 18:superCritDmg_global, 9:skillPower_personal

**Backstory**

Forester is a ranger whose arrows cause grievous wounds that bleed her enemies dry. Her mastery of the bow is paired with a deep understanding of nature's subtleties, allowing her to track and strike her prey with lethal efficiency. The slow, relentless bleed from her arrows ensures that once marked, her targets rarely escape the forest's embrace. Her reputation among her peers is that of a silent guardian, feared by those who threaten the balance of her domain. Forester's deadly precision and the haunting inevitability of her attacks make her a formidable protector of the wilds, respected and revered as the embodiment of nature’s unforgiving side.

**Sinergias**

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

<a id="27-archer"></a>
### 27 - Archer

| Campo | Valor |
|---|---|
| GameObject | archer (slow) |
| Classe | Range (2) |
| Rarity | 2 |
| Pronoun | her |
| Base cost | 100 |
| Base DPS ratio | 1 |
| Base attack speed | 0.6 |
| Base range ratio | 1.1 |
| Base crit chance | 1 |
| Skill | Exp Bonus |
| Skill active time | 1s |
| Skill cooldown | 20s |
| Skill power bonus/effect | +20% |
| Skill duration effect | 0 |
| Skill mastery base req | 35000 |
| GameObject path id | 37510 |
| Hero behaviour path id | 284600 |
| Prefab hero path id | 284600 |
| Head icon path id | 2462 |
| Full icon path id | 2816 |

**Milestone upgrades**

1:damage_personal, 14:killExp_global, 4:range_personal, 15:killGold_personal, 9:skillPower_personal, 7:critDmg_global, 9:skillPower_personal, 11:skillCd_global, 17:superCritChance_personal, 2:attSpeed_global, 0:damage_global, 40:energyIncome_global, 31:goldUltraAmount_personal, 9:skillPower_personal, 33:expSuperAmount_global, 53:instantSkillChance_personal, 35:expUltraAmount_global

**Backstory**

Archer possesses a rare talent that allows her and her allies to gain additional experience from each enemy she fells with her bow. Her precise and deadly shots not only dispatch foes with startling efficiency but also serve as crucial lessons in combat for her comrades, enhancing their skills on the battlefield. Archer's leadership and archery prowess inspire those around her to sharpen their own abilities, fostering a formidable and rapidly advancing team. Her reputation as a mentor and a marksman grows with every skirmish, as she expertly transforms each encounter into a valuable teaching moment. In the heat of battle, Archer stands as both a deadly weapon and a catalyst for growth, her arrows ensuring victory and wisdom in equal measure.

**Sinergias**

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

<a id="28-ranger"></a>
### 28 - Ranger

| Campo | Valor |
|---|---|
| GameObject | ranger (medium) |
| Classe | Range (2) |
| Rarity | 3 |
| Pronoun | him |
| Base cost | 500 |
| Base DPS ratio | 1 |
| Base attack speed | 0.5 |
| Base range ratio | 1.2 |
| Base crit chance | 5 |
| Skill | Gamble Shot |
| Skill active time | 10s |
| Skill cooldown | 24s |
| Skill power bonus/effect | +25% |
| Skill duration effect | 1 |
| Skill mastery base req | 25000 |
| GameObject path id | 11012 |
| Hero behaviour path id | 304705 |
| Prefab hero path id | 304705 |
| Head icon path id | 2822 |
| Full icon path id | 2836 |

**Milestone upgrades**

3:attSpeed_personal, 5:critChance_global, 9:skillPower_personal, 8:critDmg_personal, 13:killGold_global, 10:skillDuration_personal, 12:skillCd_personal, 33:expSuperAmount_global, 0:damage_global, 4:range_personal, 21:ultraCritChance_personal, 28:goldUltraChance_global, 1:damage_personal, 35:expUltraAmount_global, 34:expUltraChance_global, 33:expSuperAmount_global, 41:skillPower_global

**Backstory**

Ranger is an archer whose exceptional skill allows his arrows to occasionally strike with devastating extra damage. His years spent honing his craft in the dense forests have endowed him with a sharp eye and an unerring aim. His ability to land critical shots makes him a formidable opponent, as each enhanced strike can turn the tide of battle. His reputation as a precise and deadly marksman precedes him, earning him respect and caution from both allies and enemies. Ranger combines his survival instincts with lethal precision, making every arrow count and leaving a lasting impact on the battlefield.

**Sinergias**

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

<a id="29-arbalest"></a>
### 29 - Arbalest

| Campo | Valor |
|---|---|
| GameObject | arbalest (medium) |
| Classe | Range (2) |
| Rarity | 3 |
| Pronoun | her |
| Base cost | 1000 |
| Base DPS ratio | 1.2 |
| Base attack speed | 0.9 |
| Base range ratio | 1.1 |
| Base crit chance | 1 |
| Skill | Energy Source |
| Skill active time | 1s |
| Skill cooldown | 28s |
| Skill power bonus/effect | +1 |
| Skill duration effect | 0 |
| Skill mastery base req | 35000 |
| GameObject path id | 70718 |
| Hero behaviour path id | 305299 |
| Prefab hero path id | 305299 |
| Head icon path id | 2835 |
| Full icon path id | 2539 |

**Milestone upgrades**

11:skillCd_global, 7:critDmg_global, 6:critChance_personal, 9:skillPower_personal, 1:damage_personal, 4:range_personal, 2:attSpeed_global, 9:skillPower_personal, 32:expSuperChance_global, 27:goldSuperAmount_personal, 23:ultraCritDmg_personal, 35:expUltraAmount_global, 40:energyIncome_global, 37:energySuperAmount_global, 40:energyIncome_global, 39:energyUltraAmount_global, 62:instantSpell_powerPlant

**Backstory**

Arbalest is a skilled archer whose precision kills grant vital energy to her team. With each enemy she fells, a surge of rejuvenating force spreads through her allies, invigorating them for the fight ahead. Her mastery of the bow is unparalleled, her bolts striking true and ensuring that every shot counts. Her unique ability to convert her prowess into a tangible benefit for her team has made her an invaluable asset in any skirmish. Revered for her calm under pressure and her unwavering aim, Arbalest stands as both a deadly combatant and a beacon of support, driving her comrades to greater heights with every kill.

**Sinergias**

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

<a id="30-sniper"></a>
### 30 - Sniper

| Campo | Valor |
|---|---|
| GameObject | sniper (slow) |
| Classe | Range (2) |
| Rarity | 4 |
| Pronoun | him |
| Base cost | 5000 |
| Base DPS ratio | 1.3 |
| Base attack speed | 0.5 |
| Base range ratio | 1.2 |
| Base crit chance | 3 |
| Skill | Explosive Shot |
| Skill active time | 1s |
| Skill cooldown | 24s |
| Skill power bonus/effect | +50% |
| Skill duration effect | 0 |
| Skill mastery base req | 35000 |
| GameObject path id | 81813 |
| Hero behaviour path id | 312907 |
| Prefab hero path id | 312907 |
| Head icon path id | 2737 |
| Full icon path id | 2715 |

**Milestone upgrades**

4:range_personal, 1:damage_personal, 9:skillPower_personal, 2:attSpeed_global, 14:killExp_global, 9:skillPower_personal, 5:critChance_global, 12:skillCd_personal, 26:goldSuperAmount_global, 19:superCritDmg_personal, 34:expUltraChance_global, 40:energyIncome_global, 0:damage_global, 34:expUltraChance_global, 23:ultraCritDmg_personal, 17:superCritChance_personal, 18:superCritDmg_global

**Backstory**

Sniper is a marksman whose precision shots create explosive impacts, damaging nearby enemies. His exceptional aim and steady hand allow him to target critical points with pinpoint accuracy, causing devastating chain reactions on the battlefield. Trained in the art of stealth and patience, Sniper waits for the perfect moment to strike, turning the tide of combat with a single, powerful shot. His unique ability to blend pinpoint precision with explosive force has earned him a fearsome reputation among both allies and foes. Sniper combines lethal skill with strategic prowess, ensuring that each shot counts and leaves a lasting mark on the battlefield.

**Sinergias**

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

<a id="31-rogue"></a>
### 31 - Rogue

| Campo | Valor |
|---|---|
| GameObject | rogue (fast) |
| Classe | Range (2) |
| Rarity | 4 |
| Pronoun | her |
| Base cost | 10000 |
| Base DPS ratio | 0.9 |
| Base attack speed | 1.3 |
| Base range ratio | 1 |
| Base crit chance | 3 |
| Skill | Gold Aura |
| Skill active time | 10s |
| Skill cooldown | 28s |
| Skill power bonus/effect | +5% |
| Skill duration effect | 1 |
| Skill mastery base req | 35000 |
| GameObject path id | 87564 |
| Hero behaviour path id | 316887 |
| Prefab hero path id | 316887 |
| Head icon path id | 2550 |
| Full icon path id | 2616 |

**Milestone upgrades**

14:killExp_global, 4:range_personal, 7:critDmg_global, 3:attSpeed_personal, 15:killGold_personal, 0:damage_global, 11:skillCd_global, 17:superCritChance_personal, 9:skillPower_personal, 40:energyIncome_global, 28:goldUltraChance_global, 1:damage_personal, 35:expUltraAmount_global, 13:killGold_global, 9:skillPower_personal, 53:instantSkillChance_personal, 30:goldUltraAmount_global

**Backstory**

Rogue is an archer whose sharp aim and quick reflexes not only dispatch her enemies with deadly precision but also earn her extra gold from each kill. Her years spent navigating the shadows and honing her skills in the wilds have made her both a lethal combatant and a shrewd opportunist. Rogue's unique talent for turning the tide of battle to her advantage ensures that she emerges from every skirmish not just victorious but richer. Her reputation as a master archer and a cunning strategist precedes her, making her both respected and envied among her peers. Rogue strikes a perfect balance between deadly efficiency and keen resourcefulness, thriving in the chaos of combat.

**Sinergias**

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

<a id="32-ballista"></a>
### 32 - Ballista

| Campo | Valor |
|---|---|
| GameObject | ballista (slow) |
| Classe | Range (2) |
| Rarity | 5 |
| Pronoun | him |
| Base cost | 40000 |
| Base DPS ratio | 1.2 |
| Base attack speed | 0.65 |
| Base range ratio | 1.2 |
| Base crit chance | 3 |
| Skill | Exp Aura |
| Skill active time | 10s |
| Skill cooldown | 28s |
| Skill power bonus/effect | +5% |
| Skill duration effect | 1 |
| Skill mastery base req | 35000 |
| GameObject path id | 66541 |
| Hero behaviour path id | 317683 |
| Prefab hero path id | 317683 |
| Head icon path id | 2743 |
| Full icon path id | 2797 |

**Milestone upgrades**

10:skillDuration_personal, 8:critDmg_personal, 14:killExp_global, 5:critChance_global, 4:range_personal, 12:skillCd_personal, 15:killGold_personal, 1:damage_personal, 2:attSpeed_global, 9:skillPower_personal, 40:energyIncome_global, 34:expUltraChance_global, 22:ultraCritDmg_global, 33:expSuperAmount_global, 34:expUltraChance_global, 53:instantSkillChance_personal, 35:expUltraAmount_global

**Backstory**

Ballista is a heavy bowman whose powerful shots not only decimate his enemies but also grant his allies additional experience with each kill. His immense strength allows him to draw a massive bow, sending arrows that pierce through the toughest armor and strike fear into the hearts of his foes. Trained in the harsh wilderness, Ballista has perfected his technique to turn every battle into a learning opportunity for his comrades. His presence on the battlefield is both inspiring and formidable, as each of his strikes serves to elevate the skills of those fighting alongside him. Ballista stands as a pillar of strength and wisdom, ensuring that his team grows stronger with every victory.

**Sinergias**

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

<a id="33-crusader"></a>
### 33 - Crusader

| Campo | Valor |
|---|---|
| GameObject | crusader (medium) |
| Classe | Range (2) |
| Rarity | 5 |
| Pronoun | her |
| Base cost | 80000 |
| Base DPS ratio | 0.7 |
| Base attack speed | 0.9 |
| Base range ratio | 1.1 |
| Base crit chance | 1 |
| Skill | Golden Arrows |
| Skill active time | 10s |
| Skill cooldown | 24s |
| Skill power bonus/effect | +5% |
| Skill duration effect | 1 |
| Skill mastery base req | 550000 |
| GameObject path id | 85218 |
| Hero behaviour path id | 314873 |
| Prefab hero path id | 314873 |
| Head icon path id | 2830 |
| Full icon path id | 2755 |

**Milestone upgrades**

0:damage_global, 9:skillPower_personal, 11:skillCd_global, 4:range_personal, 6:critChance_personal, 13:killGold_global, 10:skillDuration_personal, 3:attSpeed_personal, 18:superCritDmg_global, 33:expSuperAmount_global, 1:damage_personal, 30:goldUltraAmount_global, 34:expUltraChance_global, 27:goldSuperAmount_personal, 9:skillPower_personal, 31:goldUltraAmount_personal, 10:skillDuration_personal

**Backstory**

Crusader is an archer whose every arrow brings not just defeat to her enemies but also gold to her coffers. Her precise and relentless attacks are legendary, each shot meticulously aimed to maximize both damage and profit. Trained in the art of warfare and strategy, Crusader has turned her skill with the bow into a lucrative endeavor, funding her kingdom with the spoils of battle. Her ability to earn gold with each attack makes her a valuable asset in prolonged campaigns, providing resources that sustain her cause. Crusader embodies the blend of martial prowess and economic savvy, driving her mission forward with both her deadly aim and strategic mind.

**Sinergias**

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

<a id="34-captain"></a>
### 34 - Captain

| Campo | Valor |
|---|---|
| GameObject | captain (medium) |
| Classe | Range (2) |
| Rarity | 6 |
| Pronoun | him |
| Base cost | 250000 |
| Base DPS ratio | 0.8 |
| Base attack speed | 1 |
| Base range ratio | 1.2 |
| Base crit chance | 1 |
| Skill | Energy Aura |
| Skill active time | 10s |
| Skill cooldown | 32s |
| Skill power bonus/effect | +0.25 |
| Skill duration effect | 1 |
| Skill mastery base req | 35000 |
| GameObject path id | 50456 |
| Hero behaviour path id | 313636 |
| Prefab hero path id | 313636 |
| Head icon path id | 2859 |
| Full icon path id | 2460 |

**Milestone upgrades**

2:attSpeed_global, 5:critChance_global, 1:damage_personal, 13:killGold_global, 9:skillPower_personal, 8:critDmg_personal, 14:killExp_global, 4:range_personal, 10:skillDuration_personal, 12:skillCd_personal, 0:damage_global, 20:ultraCritChance_global, 31:goldUltraAmount_personal, 40:energyIncome_global, 38:energyUltraChance_global, 45:powerMageEnergy_global, 63:instantSpell_timeWarp

**Backstory**

Captain is an armored bowman whose very presence radiates an aura of energy and power, invigorating his allies on the battlefield. Encased in gleaming armor, he expertly combines his skills in archery with the resilience of a frontline warrior. His arrows are precise and deadly, but it is the empowering aura he exudes that truly distinguishes him, boosting the strength and stamina of those around him with each enemy slayed. Trained in both combat and leadership, his role as a sharpshooter and motivator makes him a cornerstone of any military unit. Captain stands as a beacon of fortitude and inspiration, his unwavering spirit driving his team to greater heights in the heat of battle.

**Sinergias**

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

<a id="35-warden"></a>
### 35 - Warden

| Campo | Valor |
|---|---|
| GameObject | warden (fast) |
| Classe | Range (2) |
| Rarity | 6 |
| Pronoun | her |
| Base cost | 500000 |
| Base DPS ratio | 1.1 |
| Base attack speed | 1 |
| Base range ratio | 1.1 |
| Base crit chance | 5 |
| Skill | Gatling Gun |
| Skill active time | 10s |
| Skill cooldown | 24s |
| Skill power bonus/effect | +10% / +5% / +2% |
| Skill duration effect | 1 |
| Skill mastery base req | 25000 |
| GameObject path id | 65364 |
| Hero behaviour path id | 302043 |
| Prefab hero path id | 302043 |
| Head icon path id | 2727 |
| Full icon path id | 2520 |

**Milestone upgrades**

9:skillPower_personal, 10:skillDuration_personal, 7:critDmg_global, 11:skillCd_global, 3:attSpeed_personal, 6:critChance_personal, 4:range_personal, 25:goldSuperChance_personal, 33:expSuperAmount_global, 0:damage_global, 35:expUltraAmount_global, 1:damage_personal, 23:ultraCritDmg_personal, 3:attSpeed_personal, 17:superCritChance_personal, 18:superCritDmg_global, 21:ultraCritChance_personal

**Backstory**

Warden is a royal archer famed for her extraordinary speed and precision in battle. Trained in the king's elite guard, her ability to unleash a flurry of arrows in the blink of an eye has earned her both respect and fear on the battlefield. Each shot she fires is a testament to her unparalleled skill, striking her targets with uncanny accuracy. Her swift, relentless attacks keep enemies at bay and protect the realm from impending threats. Warden embodies the pinnacle of archery, her rapid-fire technique ensuring that no enemy escapes the reach of her bow.

**Sinergias**

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

<a id="36-praetorian"></a>
### 36 - Praetorian

| Campo | Valor |
|---|---|
| GameObject | praetorian |
| Classe | Melee (0) |
| Rarity | 7 |
| Pronoun | her |
| Base cost | 2500000 |
| Base DPS ratio | 1.1 |
| Base attack speed | 1 |
| Base range ratio | 1 |
| Base crit chance | 5 |
| Skill | Ion Blades |
| Skill active time | 10s |
| Skill cooldown | 28s |
| Skill power bonus/effect | +1% / +5% |
| Skill duration effect | 1 |
| Skill mastery base req | 25000 |
| GameObject path id | 90035 |
| Hero behaviour path id | 318494 |
| Prefab hero path id | 318494 |
| Head icon path id | 2522 |
| Full icon path id | 2617 |

**Milestone upgrades**

0:damage_global, 13:killGold_global, 7:critDmg_global, 14:killExp_global, 4:range_personal, 10:skillDuration_personal, 6:critChance_personal, 2:attSpeed_global, 9:skillPower_personal, 12:skillCd_personal, 1:damage_personal, 21:ultraCritChance_personal, 40:energyIncome_global, 9:skillPower_personal, 23:ultraCritDmg_personal, 17:superCritChance_personal, 1:damage_personal

**Backstory**

Praetorian is an elite knight celebrated for her precision and deadly critical strike attacks. In her royal armor, she stands as a formidable protector of the crown, her swordplay both graceful and lethal. Her reputation is built on her uncanny ability to find and exploit the weakest point in an enemy's armor, ensuring that her strikes are as effective as they are swift. As a key figure in the kingdom's defense, Praetorian's skills not only maintain the peace but also deter potential threats with just the whisper of her name. Her presence in any conflict assures her allies of victory, her precision in battle as reliable as it is feared.

**Sinergias**

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

<a id="37-titan"></a>
### 37 - Titan

| Campo | Valor |
|---|---|
| GameObject | titan |
| Classe | Melee (0) |
| Rarity | 7 |
| Pronoun | him |
| Base cost | 5000000 |
| Base DPS ratio | 1.2 |
| Base attack speed | 0.8 |
| Base range ratio | 0.9 |
| Base crit chance | 5 |
| Skill | Super Aura |
| Skill active time | 10s |
| Skill cooldown | 32s |
| Skill power bonus/effect | +0.2% / +1% |
| Skill duration effect | 1 |
| Skill mastery base req | 25000 |
| GameObject path id | 54543 |
| Hero behaviour path id | 299058 |
| Prefab hero path id | 299058 |
| Head icon path id | 2843 |
| Full icon path id | 2483 |

**Milestone upgrades**

10:skillDuration_personal, 6:critChance_personal, 1:damage_personal, 15:killGold_personal, 9:skillPower_personal, 7:critDmg_global, 11:skillCd_global, 4:range_personal, 17:superCritChance_personal, 3:attSpeed_personal, 34:expUltraChance_global, 28:goldUltraChance_global, 0:damage_global, 0:damage_global, 41:skillPower_global, 22:ultraCritDmg_global, 20:ultraCritChance_global

**Backstory**

Titan is a towering figure among soldiers, wielding a heavy sword with unmatched skill and strength. His very presence on the battlefield enhances the precision of his fellow soldiers, his keen eye and steady hand inspiring and guiding their strikes. As a veteran warrior, Titan not only excels in direct combat but also plays a crucial role in shaping the effectiveness of his unit, making each member sharper and more focused. His reputation for turning the tide of battle with his strategic prowess and powerful swordplay has earned him the respect of allies and the fear of enemies. In every fight, Titan stands as a pillar of strength and precision, his leadership turning ordinary soldiers into formidable warriors under his command.

**Sinergias**

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

<a id="38-sovereign"></a>
### 38 - Sovereign

| Campo | Valor |
|---|---|
| GameObject | sovereign |
| Classe | Mage (1) |
| Rarity | 7 |
| Pronoun | her |
| Base cost | 2500000 |
| Base DPS ratio | 0.8 |
| Base attack speed | 0.8 |
| Base range ratio | 1 |
| Base crit chance | 1 |
| Skill | Jackpot |
| Skill active time | 10s |
| Skill cooldown | 28s |
| Skill power bonus/effect | +0.2% / +1% |
| Skill duration effect | 1 |
| Skill mastery base req | 35000 |
| GameObject path id | 46968 |
| Hero behaviour path id | 309440 |
| Prefab hero path id | 309440 |
| Head icon path id | 2733 |
| Full icon path id | 2795 |

**Milestone upgrades**

9:skillPower_personal, 14:killExp_global, 7:critDmg_global, 12:skillCd_personal, 4:range_personal, 2:attSpeed_global, 13:killGold_global, 17:superCritChance_personal, 1:damage_personal, 0:damage_global, 35:expUltraAmount_global, 40:energyIncome_global, 20:ultraCritChance_global, 26:goldSuperAmount_global, 30:goldUltraAmount_global, 55:instantSpell_gold, 9:skillPower_personal

**Backstory**

Sovereign is a royal mage renowned for her unique alchemical talents that turn ordinary metals into precious gold. Her rare gift not only sustains her kingdom's economy but also funds expansive projects and philanthropic efforts, earning her deep respect among her peers. With a sharp intellect and a keen understanding of both the mystical and the material, she deftly balances her political influence with her magical duties. Sovereign's presence in court is marked by a blend of grace and authority, inspiring admiration and respect. Her ability to generate wealth through alchemy has made her an indispensable asset to the crown, ensuring her legacy as both a benefactor and a leader.

**Sinergias**

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

<a id="39-dicemaster"></a>
### 39 - Dicemaster

| Campo | Valor |
|---|---|
| GameObject | dicemaster |
| Classe | Mage (1) |
| Rarity | 7 |
| Pronoun | him |
| Base cost | 5000000 |
| Base DPS ratio | 1 |
| Base attack speed | 0.7 |
| Base range ratio | 1 |
| Base crit chance | 5 |
| Skill | Feeling Lucky |
| Skill active time | 10s |
| Skill cooldown | 32s |
| Skill power bonus/effect | +2% / +1% / +0.5% |
| Skill duration effect | 1 |
| Skill mastery base req | 25000 |
| GameObject path id | 86033 |
| Hero behaviour path id | 319449 |
| Prefab hero path id | 319449 |
| Head icon path id | 2759 |
| Full icon path id | 2464 |

**Milestone upgrades**

15:killGold_personal, 6:critChance_personal, 14:killExp_global, 0:damage_global, 10:skillDuration_personal, 8:critDmg_personal, 11:skillCd_global, 4:range_personal, 3:attSpeed_personal, 9:skillPower_personal, 22:ultraCritDmg_global, 29:goldUltraChance_personal, 1:damage_personal, 19:superCritDmg_personal, 22:ultraCritDmg_global, 41:skillPower_global, 16:superCritChance_global

**Backstory**

Dicemaster is a charismatic mage who thrives in the enigmatic world of luck and gambling. With his mastery over chance, he can tilt the odds in his favor or curse others with a streak of misfortune, making him a legendary figure in casinos and battlefields alike. His flair for dramatics and a penchant for risk make him a thrilling companion and a daunting adversary. Dicemaster’s reputation for manipulating outcomes has earned him both wealth and notoriety, as he wanders from town to town, leaving tales of miraculous wins and bewildering losses in his wake. His unique magic, often seen in the roll of his enchanted dice, is as much a spectacle as it is a powerful tool in his ever-unpredictable arsenal.

**Sinergias**

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

<a id="40-deadeye"></a>
### 40 - Deadeye

| Campo | Valor |
|---|---|
| GameObject | deadeye |
| Classe | Range (2) |
| Rarity | 7 |
| Pronoun | her |
| Base cost | 2500000 |
| Base DPS ratio | 1.1 |
| Base attack speed | 1 |
| Base range ratio | 1.2 |
| Base crit chance | 5 |
| Skill | Divine Aim |
| Skill active time | 10s |
| Skill cooldown | 28s |
| Skill power bonus/effect | +15% / +10% / +0.3% |
| Skill duration effect | 1 |
| Skill mastery base req | 25000 |
| GameObject path id | 77968 |
| Hero behaviour path id | 310314 |
| Prefab hero path id | 310314 |
| Head icon path id | 2741 |
| Full icon path id | 2507 |

**Milestone upgrades**

6:critChance_personal, 2:attSpeed_global, 15:killGold_personal, 10:skillDuration_personal, 0:damage_global, 12:skillCd_personal, 9:skillPower_personal, 18:superCritDmg_global, 4:range_personal, 1:damage_personal, 29:goldUltraChance_personal, 23:ultraCritDmg_personal, 34:expUltraChance_global, 9:skillPower_personal, 22:ultraCritDmg_global, 19:superCritDmg_personal, 1:damage_personal

**Backstory**

Deadeye is an elite archer whose divine aim has made her a legend among her peers. Her arrows never miss their mark, guided by a seemingly supernatural precision that turns the tide of any battle. Trained in the secluded monasteries of the highlands, Deadeye honed her skills to perfection, blending discipline with an innate gift. Her presence on the battlefield is both a reassurance to allies and a harbinger of doom to enemies. Deadeye embodies the pinnacle of archery, her every shot a testament to her unparalleled talent and unwavering focus.

**Sinergias**

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

<a id="41-veteran"></a>
### 41 - Veteran

| Campo | Valor |
|---|---|
| GameObject | veteran |
| Classe | Range (2) |
| Rarity | 7 |
| Pronoun | him |
| Base cost | 5000000 |
| Base DPS ratio | 1 |
| Base attack speed | 0.8 |
| Base range ratio | 1.1 |
| Base crit chance | 3 |
| Skill | Exp Share |
| Skill active time | 10s |
| Skill cooldown | 32s |
| Skill power bonus/effect | +0.2% / +0.5% |
| Skill duration effect | 1 |
| Skill mastery base req | 35000 |
| GameObject path id | 29349 |
| Hero behaviour path id | 280126 |
| Prefab hero path id | 280126 |
| Head icon path id | 2552 |
| Full icon path id | 2568 |

**Milestone upgrades**

4:range_personal, 11:skillCd_global, 3:attSpeed_personal, 5:critChance_global, 8:critDmg_personal, 1:damage_personal, 10:skillDuration_personal, 9:skillPower_personal, 0:damage_global, 16:superCritChance_global, 35:expUltraAmount_global, 40:energyIncome_global, 29:goldUltraChance_personal, 41:skillPower_global, 33:expSuperAmount_global, 56:instantspell_exp, 34:expUltraChance_global

**Backstory**

Veteran is an elite bowman whose vast battlefield experience has become a guiding light for his fellow soldiers. With every draw of his bowstring, he combines decades of combat wisdom with unmatched precision, ensuring his arrows always find their mark. Beyond his skill with the bow, Veteran is revered for his mentorship, sharing tactical insights and survival strategies that have saved countless lives. His calm demeanor and steady leadership instill confidence in his troops, making them stronger and more cohesive in the heat of battle. Veteran's legacy is one of excellence and camaraderie, his presence a powerful force that elevates the entire unit.

**Sinergias**

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
