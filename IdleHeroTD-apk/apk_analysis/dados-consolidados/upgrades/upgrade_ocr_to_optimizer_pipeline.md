# Fluxo OCR -> estado -> otimizador

Status: fluxo consolidado para transformar screenshots dos upgrades em input real dos otimizadores de FARM e Gold Prep.

Este guia junta quatro partes:

- OCR local deterministico para ler levels atuais;
- merge dos levels extraidos de varias telas;
- recursos em escala do jogo (`K`, `M`, `B`, `T`, `e15`, `1,5B`);
- execucao do otimizador correto para FARM ou preparacao de PUSH com Gold.

Nos comandos abaixo aparece `rtk` porque este workspace do Codex exige esse prefixo. Fora do Codex, use os mesmos comandos sem `rtk` se necessario.

## Arquivos envolvidos

Scripts:

```text
../../../../scripts/extract_upgrade_levels_from_image.py
../../../../scripts/merge_optimizer_states.py
../../../../scripts/generate_research_cost_table.py
../../../../scripts/optimize_farm_upgrades.py
../../../../scripts/optimize_gold_push_prep.py
../../../../scripts/format_optimizer_clicks.py
```

Guias de referencia:

```text
upgrade_level_image_parser.md
../formulas/farm_upgrade_optimizer.md
../formulas/gold_push_prep_optimizer.md
../formulas/core_upgrade_cost_formulas.md
../formulas/e2e_otimizacao_recursos.md
```

Artefatos reais de OCR/otimizacao devem ser gerados localmente e mantidos fora do Git publico, por exemplo em `runs/`.

## 1. Extrair levels de Research/Energy

Use a screenshot da tela de Energy/Research:

```bash
rtk python3 "Idle Hero TD/scripts/extract_upgrade_levels_from_image.py" \
  --engine auto \
  --image "/caminho/para/research.png" \
  --screen research-core \
  --format json \
  --output "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/research_atual.json"
```

O output tem um objeto `levels`, por exemplo:

```json
{
  "levels": {
    "researchDmg1": 446,
    "researchKillGold1": 446,
    "researchPrestigePower1": 765
  }
}
```

O parser retorna apenas o que esta visivel na screenshot. Se a tela estiver rolada ou incompleta, tire mais screenshots e gere mais JSONs.

## 2. Extrair levels de Prestige/PowerUps

Use a screenshot da tela de Prestige/PowerUps:

```bash
rtk python3 "Idle Hero TD/scripts/extract_upgrade_levels_from_image.py" \
  --engine auto \
  --image "/caminho/para/prestige.png" \
  --screen prestige-core \
  --format json \
  --output "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/prestige_atual.json"
```

## 3. Consolidar em um estado de FARM

Depois de extrair todos os levels visiveis, gere um unico estado para o otimizador. Preencha `--energy` e `--prestige-points` com o saldo atual mostrado no jogo.

```bash
rtk python3 "Idle Hero TD/scripts/merge_optimizer_states.py" \
  --state "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/research_atual.json" \
  --state "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/prestige_atual.json" \
  --objective FARM \
  --energy 850K \
  --prestige-points 1,5B \
  --output "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/estado_farm_atual.json"
```

O estado consolidado fica neste formato:

```json
{
  "objective": "FARM",
  "resources": {
    "energy": "850000",
    "prestige_points": "1500000000"
  },
  "levels": {
    "researchDmg1": 446,
    "prestigeDmg2": 332689
  },
  "warnings": []
}
```

Use `--set upgrade_key=level` para corrigir manualmente algum level que nao apareceu ou que voce queira travar:

```bash
rtk python3 "Idle Hero TD/scripts/merge_optimizer_states.py" \
  --state research_atual.json \
  --state prestige_atual.json \
  --objective FARM \
  --energy 850K \
  --prestige-points 1,5B \
  --set researchDmg6=0 \
  --output estado_farm_atual.json
```

Use `--conflict error` quando quiser falhar se dois JSONs trouxerem valores diferentes para o mesmo upgrade.

Importante: upgrade omitido no print nao significa automaticamente level `0`. Existem pelo menos tres casos:

- visivel: usar o level lido pelo OCR;
- oculto porque esta maxado: usar `--maxed upgrade_key`;
- ausente ou visivel com botao de wave porque ainda esta bloqueado: usar `--locked upgrade_key`.

Exemplo:

```bash
rtk python3 "Idle Hero TD/scripts/merge_optimizer_states.py" \
  --state research_atual.json \
  --state prestige_atual.json \
  --objective FARM \
  --energy 2,2M \
  --prestige-points 1,11e20 \
  --maxed prestigeDmg1 \
  --locked prestigeDmg5,prestigeDmg6,prestigeDmg7,researchDmg6 \
  --output estado_farm_atual.json
```

Upgrades em `locked_upgrades` continuam no estado, mas o otimizador nao compra esses itens.

## 3.5. Gerar tabela de custo para validar UI

Antes de confiar em qualquer otimizacao, gere uma tabela de custo com o saldo atual de Energy e compare na UI os botoes `+1`, `+10` e `+100` dos upgrades principais.

```bash
rtk python3 "Idle Hero TD/scripts/generate_research_cost_table.py" \
  --state "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/estado_farm_atual.json" \
  --energy 2,57M \
  --output-md "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/tabelas-validacao/research_dmg_gold_prestige_costs_energy_2p57M.md" \
  --output-csv "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/tabelas-validacao/research_dmg_gold_prestige_costs_energy_2p57M.csv"
```

Essa tabela cobre apenas o escopo aprovado para otimizacao atual: Damage, Kill Gold e Prestige Power. Rank Exp, Crit Chance e Super Crit Damage ficam fora.

## 4. Rodar FARM

FARM estavel usa Damage + Prestige Power. Kill Gold fica com peso zero por padrao porque Gold so vale se virar level util de heroi durante a run.

```bash
rtk python3 "Idle Hero TD/scripts/optimize_farm_upgrades.py" \
  --state "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/estado_farm_atual.json" \
  --output "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/resultado_farm_atual.json"
```

Saida importante:

- `purchases`: compras recomendadas;
- `resources`: gasto e saldo por recurso;
- `factors`: multiplicador inicial/final de Damage, Prestige Power e Kill Gold;
- `final_levels`: levels finais para copiar para planilha ou simular novamente.

Converta a lista de compras para cliques da macro:

```bash
rtk python3 "Idle Hero TD/scripts/format_optimizer_clicks.py" \
  --result "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/resultado_farm_atual.json" \
  --output "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/macro_clicks_farm_atual.txt"
```

O formato de saida usa os multiplicadores do jogo:

```text
Research/Energy:
dmg1: 2×100 + 5×10

Prestige/PowerUps:
dmg2: 16×10k + 5×1k + 2×100 + 6×10
```

Use `--no-headers` quando precisar colar apenas as linhas de comando.

## 4.5. Rodar passada residual se sobrar recurso

Se a UI mostrou um saldo arredondado (`M`, `B`, `T`, `e20`) antes da macro, o otimizador nao conhece o valor interno exato do jogo. A recomendacao principal continua valida para o valor informado, mas pode sobrar recurso real depois da execucao.

Quando isso acontecer:

- use os `final_levels` do resultado anterior como novo estado;
- coloque o saldo residual exato na UI como novo recurso;
- zere o outro recurso se ele nao deve ser reotimizado;
- rode FARM ou Gold Prep novamente;
- gere um novo arquivo de cliques com `format_optimizer_clicks.py`.

Exemplo: sobrou `39.584` Energy depois de uma macro FARM.

```bash
rtk jq '{
  objective: "FARM",
  resources: {energy: "39584", prestige_points: "0"},
  levels: .final_levels,
  locked_upgrades: .diagnostics.locked_upgrades,
  warnings: ["post-macro residual Energy pass; prestige_points set to 0"]
}' resultado_farm_atual.json > estado_farm_residual_energy.json

rtk python3 "Idle Hero TD/scripts/optimize_farm_upgrades.py" \
  --state estado_farm_residual_energy.json \
  --output resultado_farm_residual_energy.json

rtk python3 "Idle Hero TD/scripts/format_optimizer_clicks.py" \
  --result resultado_farm_residual_energy.json \
  --output macro_clicks_farm_residual_energy.txt
```

Nao escolha tier visualmente. O desempate correto e pelo score marginal: ganho logaritmico ponderado dividido pelo custo do proximo nivel, respeitando se o upgrade cabe no saldo residual.

## 5. Consolidar e rodar Gold Prep

Gold Prep e uma segunda otimizacao separada. Ela responde apenas:

```text
Se eu vou preparar PUSH investindo so em Kill Gold,
qual distribuicao maximiza Kill Gold permanente?
```

Gere o mesmo estado com `--objective GOLD_PREP`:

```bash
rtk python3 "Idle Hero TD/scripts/merge_optimizer_states.py" \
  --state "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/research_atual.json" \
  --state "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/prestige_atual.json" \
  --objective GOLD_PREP \
  --energy 850K \
  --prestige-points 1,5B \
  --output "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/estado_gold_prep_atual.json"
```

Depois rode:

```bash
rtk python3 "Idle Hero TD/scripts/optimize_gold_push_prep.py" \
  --state "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/estado_gold_prep_atual.json" \
  --output "Idle Hero TD/IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/testes-ocr/resultado_gold_prep_atual.json"
```

## Validacao feita

O parser foi validado com screenshots reais de Research/Energy e Prestige/PowerUps.

Levels extraidos da tela Research/Energy:

```text
researchDmg1=446
researchDmg2=112
researchDmg3=31
researchDmg4=10
researchDmg5=10
researchKillGold1=446
researchKillGold2=112
researchKillGold3=30
researchKillGold4=9
researchKillGold5=3
researchPrestigePower1=765
researchPrestigePower2=195
researchPrestigePower3=38
researchPrestigePower4=11
```

Levels extraidos da tela Prestige/PowerUps:

```text
prestigeDmg2=332689
prestigeDmg3=10936
prestigeDmg4=638
prestigeDmg5=0
prestigeKillGold2=338755
prestigeKillGold3=10938
prestigeKillGold4=638
prestigeKillGold5=0
prestigeKillGold6=0
```

Tambem foram validados:

- `merge_optimizer_states.py` gera um estado unico sem conflitos;
- `optimize_farm_upgrades.py` aceita o estado `FARM`;
- `optimize_gold_push_prep.py` aceita o estado `GOLD_PREP`;
- os recursos em escala `850K` e `1,5B` foram convertidos para `850000` e `1500000000`.

## Limites importantes

- OCR visual nao e save game. Ele le apenas o texto que aparece no print.
- Se um upgrade nao estiver visivel, ele nao entra no JSON, a menos que voce use `--set`.
- A UI do jogo arredonda valores; os otimizadores nao usam a UI para custo/fator. Eles usam os CSVs extraidos do APK em `../formulas/csv/`.
- FARM e Gold Prep sao objetivos diferentes. Nao use `objective: FARM` no otimizador de Gold Prep.
