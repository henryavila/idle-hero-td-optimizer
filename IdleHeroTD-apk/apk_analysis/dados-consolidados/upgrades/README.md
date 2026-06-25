# Upgrades

Categoria consolidada para upgrades e objetos relacionados.

## Referencia tabular

Os CSVs ficam em `csv/` e servem para planilha, scripts e auditoria:

- `catalogo_upgrades.csv`
- `objetos_upgrades.csv`
- `referencias_upgrade_manager.csv`

## Parser visual de levels

- `upgrade_level_image_parser.md`: guia do script deterministico `scripts/extract_upgrade_levels_from_image.py`, que usa OCR local, regex, contexto de card e ROI/grade para extrair niveis de upgrades de screenshots sem LLM.
- `upgrade_ocr_to_optimizer_pipeline.md`: fluxo completo para transformar screenshots em estado consolidado e rodar os otimizadores FARM/Gold Prep.
- Artefatos de OCR gerados localmente devem ficar fora do Git publico, em `runs/` ou outra pasta ignorada.
