# Referencias e aprendizados consolidados

Este app carrega apenas dados consolidados e scripts operacionais. Dumps brutos, arquivos temporarios e extracoes exploratorias ficam fora do repositorio do app.

## Aprendizados principais

- Research/Energy usa custo por nivel: `roundToEven(baseCost * targetLevel ^ multCost)`, somado nivel a nivel.
- Prestige/PowerUps normal usa `Round(baseCost * targetLevel ^ multCost * extraMultiplier)`.
- Prestige/PowerUps endgame usa `Round(baseCost * multCost ^ (targetLevel - 1) * extraMultiplier)`.
- FARM otimiza Damage e Prestige Power; Kill Gold fica com peso zero por padrao.
- Gold Prep e uma otimizacao separada que investe apenas em Kill Gold para preparar PUSH.
- Valores de UI como `2,59M` sao arredondados. O fluxo correto e macro principal + passada residual se sobrar recurso exato.
- O output final precisa ser a decomposicao em cliques do jogo: `x10k`, `x1k`, `x100`, `x10`, `x1`.
- A UI infere `locked` quando o OCR encontra botao `Wave`/lock no card.
- A UI infere estados ausentes por familia/tier: se um tier ausente vem antes de uma sequencia visivel consistente, ele e `maxed`; se vem depois do limite visivel/destravado, ele e `locked`.
- Buracos no meio de uma sequencia visivel viram `review`, porque podem ser falha de OCR em item que estava na imagem.
- A confirmacao manual vira override/revisao de excecoes, nao uma acao obrigatoria item a item.

## Referencias de formula

```text
IdleHeroTD-apk/apk_analysis/dados-consolidados/formulas/
```

Arquivos centrais:

```text
core_upgrade_cost_formulas.md
core_formulas_damage_gold_prestige.md
core_resource_allocation_model.md
e2e_otimizacao_recursos.md
farm_upgrade_optimizer.md
gold_push_prep_optimizer.md
csv/core_upgrade_formula_factors.csv
csv/core_upgrade_cost_formula_classes.csv
csv/core_resource_interaction_edges.csv
```

## Referencias de upgrade e OCR

```text
IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/
```

Arquivos centrais:

```text
upgrade_level_image_parser.md
upgrade_ocr_to_optimizer_pipeline.md
csv/catalogo_upgrades.csv
tabelas-validacao/
```

## Referencias auxiliares

O app tambem inclui dados consolidados de herois e mapas para consulta futura:

```text
IdleHeroTD-apk/apk_analysis/dados-consolidados/herois/
IdleHeroTD-apk/apk_analysis/dados-consolidados/mapas/
```
