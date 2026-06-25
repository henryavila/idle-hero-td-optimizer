# E2E de otimizacao de recursos

Status: conhecimento operacional consolidado para sair de screenshots e saldos atuais ate uma recomendacao reproduzivel de distribuicao de recursos.

## Objetivo

Este fluxo existe para responder, com dados reais do APK:

- quanto custa subir cada upgrade de Research/Energy em `+1`, `+10`, `+100`, `+1k`, `+10k` e `MAX`;
- como validar a formula de custo contra a UI antes de confiar no otimizador;
- como rodar a otimizacao FARM;
- como rodar a segunda otimizacao Gold Prep para preparar PUSH.

## Escopo aprovado

Para o ciclo atual, considerar apenas:

- Damage: `researchDmg*` e `prestigeDmg*`;
- Kill Gold: `researchKillGold*` e `prestigeKillGold*`;
- Prestige Power: `researchPrestigePower*`.

Fora do escopo atual:

- Rank Exp;
- Crit Chance;
- Super Crit Damage;
- Ultra Crit;
- stats de heroi, mapa, temporarios, sinergias e run simulation.

## Guardrails

Antes de usar qualquer recomendacao do otimizador:

1. Gere a tabela de custo de Research/Energy com o saldo atual.
2. Compare na UI pelo menos `+1`, `+10` e `+100` dos upgrades principais.
3. Se algum custo nao bater, pare: o otimizador ainda nao e confiavel para aquele estado.
4. Upgrade omitido no print nao e automaticamente `0`.
5. Upgrade maxado deve entrar como max level.
6. Upgrade bloqueado por wave deve entrar em `locked_upgrades`.

O erro antigo invalidado foi tratar Research como custo constante/eixo de potencia errado. A formula real validada e:

```text
Research/Energy:
roundToEven(baseCost * targetLevel ^ multCost)
```

somada nivel a nivel.

## Artefatos principais

Scripts:

```text
../../../../scripts/extract_upgrade_levels_from_image.py
../../../../scripts/merge_optimizer_states.py
../../../../scripts/generate_research_cost_table.py
../../../../scripts/optimize_farm_upgrades.py
../../../../scripts/optimize_gold_push_prep.py
../../../../scripts/format_optimizer_clicks.py
../../../../scripts/test_upgrade_cost_formulas.py
```

Documentos-base:

```text
core_upgrade_cost_formulas.md
re-auditoria_custo_upgrades_2026-06-25.md
farm_upgrade_optimizer.md
gold_push_prep_optimizer.md
../upgrades/upgrade_ocr_to_optimizer_pipeline.md
```

## Fluxo E2E

### 1. OCR de Research/Energy

```bash
rtk python3 "Idle Hero TD/scripts/extract_upgrade_levels_from_image.py" \
  --engine auto \
  --image "/caminho/para/research.png" \
  --screen research-core \
  --format json \
  --output "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/research_atual.json"
```

### 2. OCR de Prestige/PowerUps

```bash
rtk python3 "Idle Hero TD/scripts/extract_upgrade_levels_from_image.py" \
  --engine auto \
  --image "/caminho/para/prestige.png" \
  --screen prestige-core \
  --format json \
  --output "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/prestige_atual.json"
```

### 3. Merge do estado

```bash
rtk python3 "Idle Hero TD/scripts/merge_optimizer_states.py" \
  --state "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/research_atual.json" \
  --state "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/prestige_atual.json" \
  --objective FARM \
  --energy 2,57M \
  --prestige-points 1,11e20 \
  --maxed prestigeDmg1 \
  --locked researchDmg6,researchKillGold6,researchPrestigePower5,prestigeDmg5,prestigeDmg6,prestigeDmg7,prestigeKillGold5,prestigeKillGold6,prestigeKillGold7 \
  --output "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/estado_farm_atual.json"
```

### 4. Tabela de custo para validar UI

```bash
rtk python3 "Idle Hero TD/scripts/generate_research_cost_table.py" \
  --state "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/estado_farm_atual.json" \
  --energy 2,57M \
  --output-md "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/tabelas-validacao/research_dmg_gold_prestige_costs_energy_2p57M.md" \
  --output-csv "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/tabelas-validacao/research_dmg_gold_prestige_costs_energy_2p57M.csv"
```

Validacao esperada do estado aprovado:

```text
researchDmg1 Lv 446:
+1  = 2.235
+10 = 22.575
+100 = 248.250
MAX com 2,57M = +661 levels, custo 2.567.985
```

### 5. Otimizacao FARM

FARM usa, por padrao:

```text
Damage weight = 1
Prestige Power weight = 1
Kill Gold weight = 0
```

Kill Gold fica fora porque so tem valor para FARM se virar level util de heroi durante a run.

```bash
rtk python3 "Idle Hero TD/scripts/optimize_farm_upgrades.py" \
  --state "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/estado_farm_atual.json" \
  --output "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/resultado_farm_atual.json"
```

### 6. Otimizacao Gold Prep

Gold Prep e separada e serve para preparar PUSH. Ela aloca recursos somente em Kill Gold.

```bash
rtk python3 "Idle Hero TD/scripts/merge_optimizer_states.py" \
  --state "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/research_atual.json" \
  --state "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/prestige_atual.json" \
  --objective GOLD_PREP \
  --energy 2,57M \
  --prestige-points 1,11e20 \
  --maxed prestigeDmg1 \
  --locked researchDmg6,researchKillGold6,researchPrestigePower5,prestigeDmg5,prestigeDmg6,prestigeDmg7,prestigeKillGold5,prestigeKillGold6,prestigeKillGold7 \
  --output "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/estado_gold_prep_atual.json"

rtk python3 "Idle Hero TD/scripts/optimize_gold_push_prep.py" \
  --state "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/estado_gold_prep_atual.json" \
  --output "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/resultado_gold_prep_atual.json"
```

### 7. Converter resultado em cliques para macro

Depois de qualquer otimizacao, converta `levels_bought` para a decomposicao de cliques do jogo: `x10k`, `x1k`, `x100`, `x10`, `x1`.

```bash
rtk python3 "Idle Hero TD/scripts/format_optimizer_clicks.py" \
  --result "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/resultado_farm_atual.json" \
  --output "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/macro_clicks_farm_atual.txt"
```

A saida separa `Research/Energy` de `Prestige/PowerUps`, porque nomes como `dmg2` existem nas duas telas. Se a macro precisar somente das linhas, use `--no-headers`.

### 8. Passada residual quando a UI arredonda saldo

Quando o saldo inicial aparece abreviado na UI (`2,59M`, `1,21e20`, etc.), o valor interno exato do jogo nao e conhecido. Nesse caso, o plano principal deve usar o numero informado como valor conservador e nao deve prometer zerar o recurso.

Processo aprovado:

1. Rode a macro principal gerada pelo otimizador.
2. Veja se sobrou recurso com numero exato ou mais preciso na UI.
3. Gere um novo estado usando os `final_levels` da rodada anterior.
4. Coloque apenas o saldo residual no recurso que sobrou.
5. Rode o otimizador novamente para gerar uma macro residual.

Exemplo para sobra de Energy depois de FARM:

```bash
rtk jq '{
  objective: "FARM",
  resources: {energy: "39584", prestige_points: "0"},
  levels: .final_levels,
  locked_upgrades: .diagnostics.locked_upgrades,
  warnings: ["post-macro residual Energy pass; prestige_points set to 0"]
}' \
  "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/resultado_farm_atual.json" \
  > "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/estado_farm_residual_energy.json"

rtk python3 "Idle Hero TD/scripts/optimize_farm_upgrades.py" \
  --state "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/estado_farm_residual_energy.json" \
  --output "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/resultado_farm_residual_energy.json"

rtk python3 "Idle Hero TD/scripts/format_optimizer_clicks.py" \
  --result "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/resultado_farm_residual_energy.json" \
  --output "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/macro_clicks_farm_residual_energy.txt"
```

Interprete a passada residual pelo score marginal, nao pelo tier visual: o otimizador compra o proximo nivel com maior `log(gain) / custo` entre os itens compraveis. Um tier maior pode ter score alto, mas se nao couber no saldo residual ele nao entra; entre os compraveis, tiers menores podem continuar sendo a melhor compra.

## Criterios de aceite

O E2E so deve ser considerado confiavel quando:

- `test_upgrade_cost_formulas.py` passa;
- tabela de custo bate com a UI nos upgrades conferidos;
- estado consolidado tem `locked_upgrades` correto;
- estado consolidado tem upgrades maxados manuais corretos;
- otimizador termina com `hit_step_limit = false`;
- cliques para macro foram gerados com `format_optimizer_clicks.py`;
- se o saldo inicial estava arredondado e sobrou recurso, a passada residual foi salva separadamente;
- outputs JSON e tabelas MD/CSV ficam salvos em `dados-consolidados`.
