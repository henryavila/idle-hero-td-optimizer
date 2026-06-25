# Idle Hero TD Optimizer App

Aplicativo local para gerar comandos de macro a partir de screenshots do Idle Hero TD.

O app nao executa cliques no jogo. Ele apenas:

1. recebe prints por drag-and-drop;
2. roda OCR deterministico;
3. pede confirmacao dos levels, `maxed` e `locked`;
4. roda o otimizador FARM ou Gold Prep;
5. gera o texto no formato combinado para copiar para sua macro.

## Instalar

```bash
./install.sh
```

Se quiser instalar EasyOCR tambem:

```bash
./install.sh --with-easyocr
```

No macOS, o app tambem pode usar OCR via Vision quando `swiftc` estiver disponivel. Tesseract tambem funciona se estiver instalado no sistema.

Para melhor leitura automatica dos prints, especialmente quando a tela estiver recortada ou com texto pequeno, use EasyOCR:

```bash
./install.sh --with-easyocr
```

Sem EasyOCR, o modo `auto` pode cair para macOS Vision. Isso funciona sem dependencia pesada, mas pode deixar mais linhas em `review` para voce confirmar manualmente.

## Rodar

```bash
./run.sh
```

Ou abra `run.command` pelo Finder.

O Streamlit abrira um endereco local parecido com:

```text
http://localhost:8501
```

## Fluxo

1. Arraste o print de Research.
2. Arraste o print de Prestige.
3. Informe Energy e Prestige Points usando a escala do jogo, por exemplo `2,59M` e `1,21e20`.
4. Clique em `Ler imagens`.
5. Resolva apenas as pendencias exibidas. O app infere por familia/tier:
   - `locked`: item visivel com botao `Wave`/lock;
   - `locked`: item ausente que esta alem do limite visivel/destravado da familia;
   - `maxed`: item ausente antes de uma sequencia visivel consistente da mesma familia;
   - `review`: buraco ambiguo no meio dos tiers visiveis, para evitar confundir OCR falho com maxed;
   - `ignore`: item de uma tela que voce nao anexou.
6. Use `Ajustes avancados` apenas para override/debug:
   - `available`: upgrade disponivel e com level correto;
   - `locked`: upgrade bloqueado por wave;
   - `maxed`: upgrade omitido ou no maximo;
   - `ignore`: nao entra no estado;
   - `review`: precisa ser confirmado antes de gerar.
7. Clique em `Gerar macro`.
8. Copie o bloco da saida para seu app de macro.

## Passada residual

Se o jogo mostrou saldo arredondado antes da macro, como `2,59M`, o otimizador usa esse valor como entrada conservadora. Depois de executar a macro, se sobrar recurso real, informe o saldo em `Passada residual` e gere uma segunda macro curta.

## Estrutura

```text
ui/app.py                                      Streamlit UI
scripts/                                      motores validados de OCR, otimizacao e macro
IdleHeroTD-apk/apk_analysis/dados-consolidados referencias extraidas e consolidadas do APK
runs/                                         saidas locais geradas pela UI
```

## Dados incluidos

Este repositorio inclui os dados consolidados, nao os dumps brutos do APK. Os principais arquivos operacionais sao:

```text
IdleHeroTD-apk/apk_analysis/dados-consolidados/formulas/csv/core_upgrade_formula_factors.csv
IdleHeroTD-apk/apk_analysis/dados-consolidados/formulas/csv/core_upgrade_cost_formula_classes.csv
IdleHeroTD-apk/apk_analysis/dados-consolidados/formulas/e2e_otimizacao_recursos.md
IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/upgrade_ocr_to_optimizer_pipeline.md
```

## Testes

```bash
source .venv/bin/activate
python scripts/test_upgrade_cost_formulas.py
python -m compileall -q scripts ui
```
