# Modelo de alocacao: Damage, Kill Gold e Prestige

Status: modelo critico consolidado a partir do fluxo IL2CPP. Este arquivo nao substitui as formulas de fator/custo; ele explica como os recursos interagem entre si no loop real do jogo e como uma IA/planilha deve decidir onde gastar.

## Conclusao curta

Da para ser exato em tres camadas:

- impacto direto de cada upgrade permanente: `core_formulas_damage_gold_prestige.md`;
- custo real de cada nivel: `core_upgrade_cost_formulas.md`;
- recompensa de prestige para uma wave conhecida: `GlobalMethods.getPrestigePointsReward`.

Nao da para ser exato no "melhor mix" usando so uma formula estatica de Damage, Gold e Prestige Power, porque o resultado final depende do estado da run:

- Damage muda clear speed, wave maxima e, por consequencia, gold/prestige obtidos;
- Kill Gold muda o gold ganho por inimigo, mas o valor real desse gold depende de ele virar level de heroi antes do prestige;
- Prestige Power nao ajuda a chegar mais longe diretamente; ele multiplica o prestige recebido em uma wave ja alcancada;
- Prestige Points compram upgrades de Damage/Kill Gold, entao Prestige Power vira Damage/Gold apenas em runs futuras;
- Energy e Prestige Points sao dois orcamentos separados. Nao trate os upgrades de Research e Prestige como se competissem pelo mesmo recurso.

O elo `Gold -> level -> DPS` existe no codigo, mas e uma decisao/politica de run, nao uma premissa fixa. O app so converte gold em DPS quando o jogador/automacao compra level de heroi.

## Elos validados no codigo

| Elo | Status | Evidencia | Papel no modelo |
| --- | --- | --- | --- |
| Research Damage + Prestige Damage -> dano permanente | Confirmado | `Hero.getDmgPermEffect()` | Multiplicador permanente `M_D`. |
| Research Kill Gold + Prestige Kill Gold -> base gold | Confirmado | `GameManager.getBaseGoldDrop(int)` | Multiplicador permanente `M_G` aplicado antes dos bonus de inimigo/heroi. |
| Research Prestige Power -> prestige recebido | Confirmado | `GlobalMethods.getPrestigePointsPermEffect()` chamado por `getPrestigePointsReward()` | Multiplicador permanente `M_PP`. |
| Wave -> prestige recebido | Confirmado | `GlobalMethods.getPrestigePointsReward(int,bool)` | Formula fechada: `round(w*(w+1)/2*(1+0.01*w)*M_PP*outros)`. |
| Kill Gold -> gold de inimigo -> recurso gold | Confirmado | `Enemy.getKillGoldAmt(...)`, depois `BigDouble.op_Addition` no recurso | Entrada de gold durante a run. |
| Gold -> level de heroi -> level DPS | Confirmado | `HeroSelectedLevelPanel.clickedLevelButton()` e `clickedLevelAllButton()` subtraem custo e chamam `HeroManager.addHeroLevelStatsAndCheckChallenges` | Conversao operacional, dependente de politica de compra. |
| Prestige end -> recurso Prestige Points | Confirmado | `GameManager.prestigeEnd()` chama `getPrestigePointsReward` e soma no recurso | Fecha o ciclo da run. |
| Prestige Points -> Prestige Damage/Kill Gold | Confirmado | `UpgradesPowerUpsCell.clickedUpgradeButton()`/formulas de custo | Realimenta `M_D` e `M_G` em runs futuras. |
| Energy -> Research Damage/Kill Gold/Prestige Power | Confirmado | `UpgradesResearchCell.clickedUpgradeButton()`/formulas de custo | Compra `M_D`, `M_G` e `M_PP` com outro orcamento. |

Tabela tabular curta: `csv/core_resource_interaction_edges.csv`.

## Variaveis

Use estas familias de variaveis para uma planilha ou script.

```text
eD_i = nivel do Research Damage i, i=1..6
eG_i = nivel do Research Kill Gold i, i=1..6
eP_i = nivel do Research Prestige Power i, i=1..5

pD_i = nivel do Prestige Damage i, i=1..7
pG_i = nivel do Prestige Kill Gold i, i=1..7

R_E = energia disponivel para Research
R_P = prestige points disponiveis para Prestige/PowerUps

h_j = estado do heroi j na run: level, levelDps, levelCost
g = gold atual da run
w = wave atual
W = wave maxima/ultima wave usada no prestige
theta = mapa, perks, slots, time, sinergias e temporarios fixos no cenario
```

## Fatores permanentes exatos

Para qualquer linha de upgrade com percentual por nivel `q`:

```text
F(level, q) = 1 + level * q
```

Damage:

```text
M_D(eD,pD) =
  PRODUCT_i F(eD_i, q_eD_i)
  * PRODUCT_i F(pD_i, q_pD_i)
```

Kill Gold:

```text
M_G(eG,pG) =
  PRODUCT_i F(eG_i, q_eG_i)
  * PRODUCT_i F(pG_i, q_pG_i)
```

Prestige Power:

```text
M_PP(eP) =
  PRODUCT_i F(eP_i, q_eP_i)
```

Os `q` exatos e os custos por nivel estao nos CSVs desta pasta.

## Gold vira DPS somente via compra de level

O painel de level do heroi pre-calcula os proximos estados e a compra grava esses estados no `HeroData`. A recorrencia observada no codigo e:

```text
useCostScale = 1 + 0.065 * getHeroLevelCostReduction()

nextLevelDps  = Round((currentLevelDps  + 10) * 1.05)
nextLevelCost = Round((currentLevelCost + 10) * useCostScale)
```

A compra:

```text
if gold >= totalCost:
  gold -= totalCost
  hero.level = newLevel
  hero.levelDps = newLevelDps
  hero.levelCost = newLevelCost
  Hero.updDamageStats()
  HeroManager.addHeroLevelStatsAndCheckChallenges(levelsBought)
```

Implicacao: Kill Gold so aumenta DPS se a politica de run gastar esse gold em levels relevantes antes do gargalo. Gold sobrando no fim da run tem valor marginal baixo para o objetivo de prestige, a menos que o jogo/automacao o converta antes do reset/progresso.

## Modelo de uma run

Trate a run como uma transicao de estado:

```text
s_0 = (upgrades permanentes, mapa/time/perks theta, estado inicial de herois, recursos)

para cada evento de jogo t:
  dano_t = DamageCode(theta, h_t, M_D)
  inimigos_t = SpawnAndHpCode(w_t, theta)
  kills_t = CombatCode(dano_t, inimigos_t)
  gold_t = GoldCode(kills_t, M_G, theta)
  g_{t+1} = g_t + gold_t - gold_gasto_em_levels_t
  h_{t+1} = HeroLevelCode(h_t, gold_gasto_em_levels_t)
  w_{t+1} = WaveProgressCode(w_t, kills_t, tempo_t)

W = wave final da run
PrestigeReward(W) =
  Round((W * (W + 1) / 2) * (1 + 0.01 * W) * M_PP * OtherPrestigeFactors(theta))
```

Como o combate, spawn, HP, skills, crit, mapas e sinergias entram no `DamageCode`/`CombatCode`, a forma correta para alocacao global e simular a transicao, nao tentar reduzir tudo a um unico multiplicador.

## Otimizacao para estado fixo

Se voce quer apenas maximizar um multiplicador isolado com os recursos atuais, sem mudar wave nem simular runs futuras, a solucao pode ser exata por busca inteira.

Para cada compra candidata `i`:

```text
gain_i = ln(F(level_i + 1, q_i) / F(level_i, q_i))
cost_i = nextCost_i(level_i)
roi_i = gain_i / cost_i
```

Depois de comprar um nivel, recalcule custo e ganho do proximo nivel. Para um otimo garantido com muitos niveis:

```text
max sum_i ln(F(level_i + bought_i, q_i) / F(level_i, q_i))
sujeito a sum_i cost_i(bought_i) <= recurso
bought_i inteiro >= 0
```

Isso serve para perguntas como:

- "Com esta energia, qual Research maximiza Damage permanente?"
- "Com este Prestige, qual Prestige PowerUp maximiza Kill Gold permanente?"

Nao serve sozinho para decidir entre Damage, Gold e Prestige Power com foco em progresso futuro, porque wave e gold gasto durante a run mudam o valor marginal.

## Otimizacao para progresso real

Para maximizar progresso, use um horizonte de runs:

```text
V_H(s) = max_a J(T_H(s, a, policy))
```

Onde:

- `s` e o estado atual;
- `a` e um pacote de compras permanentes permitido pelos orcamentos `R_E` e `R_P`;
- `policy` e a regra de compra de level de heroi durante a run;
- `T_H` simula H runs com prestige no fim de cada uma;
- `J` e o objetivo escolhido.

Objetivos recomendados:

```text
J_prestige_hour = ln(prestige_points_por_hora)
J_next_prestige = ln(prestige_points_na_proxima_run)
J_growth = alpha*ln(M_D) + beta*ln(M_G) + gamma*ln(prestige_points_por_run)
```

Para escolher o proximo upgrade:

```text
ROI_H(upgrade_i) =
  (J(T_H(s, comprar_i, policy)) - J(T_H(s, nao_comprar, policy)))
  / cost_i
```

Compre o maior `ROI_H`, atualize o estado e repita. Para uma planilha, faca isso com uma tabela de candidatos e recalculo iterativo. Para resultado mais robusto, use script/solver com branch-and-bound ou busca por feixe.

## Correlacoes praticas

Damage:

- valor direto quando aumenta clear speed, wave maxima ou reduz tempo ate prestige;
- valor baixo quando voce ja esta matando instantaneamente e o gargalo e spawn, mapa, cooldown, range ou outro limite;
- aumenta prestige indiretamente por aumentar `W`.

Kill Gold:

- valor direto no gold por kill;
- valor real depende de `policy`: se o gold extra compra levels que aumentam DPS antes da wall, ele tem efeito de progresso;
- se o gold extra fica parado ou chega tarde demais na run, o ROI real cai;
- pode ser superior a Damage quando um pequeno aumento de gold permite varios levels de heroi e esses levels mudam a wave final.

Prestige Power:

- nao muda DPS nem gold da run atual diretamente;
- multiplica a recompensa em uma wave ja alcancada;
- fica forte quando `W` ja esta alto e Prestige Points sao o gargalo dos upgrades permanentes;
- fica fraco no curto prazo quando o aumento de prestige ainda nao compra nenhum nivel relevante de Damage/Kill Gold.

Prestige Damage/Kill Gold:

- competem pelo mesmo recurso `R_P`;
- Damage tende a valer mais quando wave e o gargalo;
- Kill Gold tende a valer mais quando o gargalo e financiar levels/escala durante a run;
- o Prestige Power de Research aumenta a capacidade futura de comprar esses dois grupos.

Research Damage/Kill Gold/Prestige Power:

- competem pelo recurso `R_E`, separado de `R_P`;
- Research Prestige Power nao compete diretamente com Prestige Damage/Kill Gold, mas aumenta a velocidade com que `R_P` cresce;
- a decisao correta em Energy deve considerar o que esta faltando no ciclo: chegar mais longe, transformar gold em levels, ou gerar mais prestige por wave.

## Farm vs Push

Para push/progressao, mantenha Damage, Kill Gold e Prestige Power no modelo. Gold pode ser decisivo quando o gargalo e comprar levels suficientes para atravessar a wall.

Para farm estavel, trate Kill Gold como candidato secundario ou excluido, a menos que o simulador mostre pelo menos um destes efeitos:

- o gold extra compra levels uteis de heroi antes do fim da run;
- esses levels mudam DPS efetivo, wave final ou tempo da run;
- o objetivo de farm depende de gold acumulado dentro da propria run.

Se a run de farm ja atinge a wave alvo e o gold extra nao muda compra util de level, o ROI real de Kill Gold para prestige tende a zero. Nesse cenario, priorize:

- Damage, se reduzir tempo da run ou permitir farmar wave maior;
- Prestige Power, se a wave de farm ja esta definida e o objetivo e aumentar prestige por run;
- Prestige Damage, se os Prestige Points forem usados em upgrades permanentes que ainda mexem em wave/tempo.

Forma compacta:

```text
Push:
  avaliar Damage + Kill Gold + Prestige Power

Farm em wave/tempo estavel:
  avaliar Damage + Prestige Power
  incluir Kill Gold somente se delta_gold -> delta_level_util -> delta_wave_ou_tempo
```

## Script operacional para FARM

O script `../../../../scripts/optimize_farm_upgrades.py` aplica este corte de FARM usando os custos/fatores reais dos CSVs consolidados:

```bash
python3 "Idle Hero TD/scripts/optimize_farm_upgrades.py" --print-template
python3 "Idle Hero TD/scripts/optimize_farm_upgrades.py" --state estado_farm.json --output resultado_farm.json
```

Objetivo padrao:

```text
score =
  ln(Damage_final / Damage_inicial)
  + ln(PrestigePower_final / PrestigePower_inicial)
```

Kill Gold entra com peso `0` por padrao. Para testar uma politica de push/farm em que gold extra vira level util, use `--include-gold` ou `--gold-weight`.

Saida principal:

- `purchases`: quais upgrades comprar e ate qual nivel;
- `resources`: gasto e saldo por recurso;
- `factors`: multiplicador final de Damage, Prestige Power e Kill Gold;
- `final_levels`: estado final para alimentar planilha ou nova simulacao.

## Script operacional para Gold Prep / Push

Quando a decisao estrategica for preparar uma run de PUSH investindo somente em Kill Gold, use `../../../../scripts/optimize_gold_push_prep.py`.

```bash
python3 "Idle Hero TD/scripts/optimize_gold_push_prep.py" --print-template
python3 "Idle Hero TD/scripts/optimize_gold_push_prep.py" --state estado_gold.json --output resultado_gold.json
```

Objetivo:

```text
score =
  ln(KillGold_final / KillGold_inicial)
```

Pesos:

```text
Damage = 0
Prestige Power = 0
Kill Gold = 1
```

Este script so compra `researchKillGold1..6` e `prestigeKillGold1..7`. Ele nao prova que Gold e melhor que Damage para push; ele resolve a subpergunta "se o plano agora e investir tudo em Gold, qual distribuicao maximiza o fator permanente de Kill Gold?".

## Regra de decisao recomendada

1. Defina objetivo: proxima run, prestige por hora, ou crescimento em N prestiges.
2. Fixe o cenario `theta`: mapa, time, sinergias, perks, slots e temporarios considerados.
3. Rode baseline: wave final, tempo de run, gold gasto, gold sobrando, prestige recebido.
4. Para cada upgrade candidato, simule "comprar +1 nivel" usando custo real e fator real.
5. Compare `delta ln(objetivo) / custo`.
6. Compre o melhor candidato, atualize os recursos e niveis, e repita.
7. Se dois upgrades empatam, prefira o que move um gargalo observavel:
   - falta wave/clear speed: Damage;
   - falta level durante run: Kill Gold;
   - falta Prestige Points para upgrades permanentes: Prestige Power.

## Precisao esperada

Uma planilha que use apenas `M_D`, `M_G`, `M_PP` e custos reais sera precisa para multiplicadores permanentes, mas nao para o resultado final de uma run.

Para ficar no nivel de dado real do jogo, a proxima etapa e portar ou chamar no simulador:

- `Hero.getDmg`, `Hero.getAvgDps` e crit/super/ultra;
- `Enemy.dealDamage` e regras de clear;
- `Enemy.getKillGoldAmt` completo;
- `GameManager.getBaseGoldDrop` completo;
- spawn, enemy HP/scaling e wave progression;
- politica de compra de level dos herois durante a run;
- mapa, perks, slots e sinergias ativas.

Com isso, a otimizacao deixa de ser aproximacao por UI e passa a ser uma busca exata sobre as mesmas formulas do app, exceto por escolhas estocasticas que devem ser simuladas por valor esperado ou por Monte Carlo com seed/controlador.
