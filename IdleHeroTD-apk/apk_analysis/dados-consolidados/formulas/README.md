# Formulas consolidadas

Pasta dedicada aos arquivos de formulas reversas do jogo.

## Arquivos

- `core_formulas_damage_gold_prestige.md`: explicacao das formulas de Damage, Kill Gold e Prestige Power, com foco no impacto de Research/Energy e Prestige.
- `core_upgrade_cost_formulas.md`: formulas reais de custo extraidas do IL2CPP/binario, incluindo arredondamento, BigDouble, thresholds e regras endgame.
- `core_result_dependency_map_damage_gold_prestige.md`: mapa das familias que interagem com Damage, Kill Gold e Prestige alem dos upgrades centrais.
- `core_resource_allocation_model.md`: analise critica e modelo matematico para distribuir Energy/Prestige entre Damage, Kill Gold e Prestige Power considerando o ciclo real da run.
- `e2e_otimizacao_recursos.md`: runbook E2E para OCR, merge, validacao de custo, FARM e Gold Prep.
- `farm_upgrade_optimizer.md`: uso do script `scripts/optimize_farm_upgrades.py` para distribuir Energy/Prestige em objetivo FARM, com Gold excluido por padrao.
- `gold_push_prep_optimizer.md`: uso do script `scripts/optimize_gold_push_prep.py` para alocar recursos somente em Kill Gold, preparando PUSH.
- `../upgrades/upgrade_ocr_to_optimizer_pipeline.md`: fluxo completo para extrair levels de screenshots, consolidar estado e rodar FARM/Gold Prep.

## Referencia tabular

Os CSVs ficam em `csv/` e servem para planilha, scripts e auditoria:

- `core_upgrade_formula_factors.csv`: fatores por nivel, campos do `DataManager`, custos extraidos e metodos IL2CPP usados como evidencia.
- `core_upgrade_cost_formula_classes.csv`: classe de formula de custo por upgrade central.
- `core_resource_interaction_edges.csv`: tabela curta dos elos validados no codigo entre upgrades, gold, level, wave e prestige.

## Escopo

Estes arquivos sao dados consolidados. Os dumps brutos e indices usados como fonte continuam em `../../scripts-extraidos/`, especialmente:

- `indices/il2cpp_assembly_csharp_methods.csv`
- `indices/il2cpp_assembly_csharp_fields.csv`
- `il2cpp/Cpp2IL-isil/IsilDump/Assembly-CSharp/`

Use esta pasta quando o objetivo for montar planilha, simular ROI ou alimentar uma IA com as formulas finais. Use `scripts-extraidos/` quando precisar auditar a origem no APK.

## Script operacional

O otimizador de FARM fica fora desta pasta, em:

```text
../../../../scripts/optimize_farm_upgrades.py
../../../../scripts/merge_optimizer_states.py
../../../../scripts/generate_research_cost_table.py
../../../../scripts/format_optimizer_clicks.py
```

Ele le os CSVs desta pasta e recebe um JSON com recursos/niveis atuais:

```bash
python3 "Idle Hero TD/scripts/optimize_farm_upgrades.py" --print-template
python3 "Idle Hero TD/scripts/optimize_farm_upgrades.py" --state estado_farm.json --output resultado_farm.json
```

Os campos `resources.energy` e `resources.prestige_points` aceitam escala do jogo: `K`, `M`, `B`, `T`, `1e15`, `2.4e16` e atalho `e15`.

O otimizador exclusivo de Kill Gold para preparar PUSH fica em:

```text
../../../../scripts/optimize_gold_push_prep.py
```

Uso:

```bash
python3 "Idle Hero TD/scripts/optimize_gold_push_prep.py" --print-template
python3 "Idle Hero TD/scripts/optimize_gold_push_prep.py" --state estado_gold.json --output resultado_gold.json
```

Depois de rodar FARM ou Gold Prep, gere o arquivo colavel na macro:

```bash
python3 "Idle Hero TD/scripts/format_optimizer_clicks.py" --result resultado_farm.json --output macro_clicks_farm.txt
```

Ele converte `levels_bought` em cliques `x10k`, `x1k`, `x100`, `x10` e `x1`, separado por tela (`Research/Energy` e `Prestige/PowerUps`).
