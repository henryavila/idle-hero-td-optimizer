# Parser deterministico de levels por imagem

Status: script criado para extrair niveis de upgrades a partir de screenshots sem usar LLM.

## Script

```text
../../../../scripts/extract_upgrade_levels_from_image.py
```

O script usa OCR local e depois aplica regras fixas:

- recebe uma imagem;
- le o TSV gerado pelo engine OCR;
- agrupa palavras/linhas por coordenada;
- procura `Lv`, `Lvl`, `Level`, `123/999999` ou equivalentes;
- associa o numero ao upgrade por texto detectado, ROI fixa ou grade fixa.
- quando o OCR do numeral romano falha, usa o incremento exibido no card, por exemplo `(+10%)`, para identificar o tier.
- quando o OCR do level falha de forma conhecida na fonte do jogo, aplica correcoes deterministicas, como `1Z -> 112`.

## Dependencias

Engine recomendado:

```bash
python3 -m pip install --user pillow numpy opencv-python-headless easyocr
```

`easyocr` e OCR local baseado em modelo de reconhecimento de texto. Nao e LLM e nao gera texto livre; ele detecta texto na imagem e o parser faz o resto por regex/regras.

O modo automatico nao depende de dimensao fixa do print. Ele usa as caixas detectadas pelo OCR e o texto do proprio card. Quando usar `--grid` ou `--config`, prefira retangulos normalizados `0..1`, porque assim a mesma calibracao sobrevive a screenshots em tamanhos diferentes.

Engines opcionais:

- `tesseract`, se o binario existir no sistema;
- `vision`, helper experimental para macOS Vision.

Para Tesseract no macOS:

```bash
brew install tesseract
```

Isso nao usa LLM. O parser final e deterministico: OCR local + regex + normalizacao + coordenadas.

## Modos de uso

### 1. Auto por texto

Tenta achar os nomes dos upgrades e seus levels no OCR completo.

```bash
python3 "Idle Hero TD/scripts/extract_upgrade_levels_from_image.py" \
  --engine easyocr \
  --image screenshot.png \
  --screen research-core \
  --output levels_research.json
```

Presets:

- `research-core`: `researchDmg1..6`, `researchKillGold1..6`, `researchPrestigePower1..5`
- `prestige-core`: `prestigeDmg1..7`, `prestigeKillGold1..7`
- `all-core`: os dois grupos

### 2. Grade fixa

Use quando a tela mostra os upgrades em grid previsivel. O retangulo pode ser normalizado `0..1`.

```bash
python3 "Idle Hero TD/scripts/extract_upgrade_levels_from_image.py" \
  --engine easyocr \
  --image screenshot.png \
  --screen research-core \
  --grid 0.05,0.18,0.95,0.90 \
  --cols 2 \
  --rows 9 \
  --output levels_research.json
```

Se a tela mostrar apenas uma parte dos upgrades, defina a ordem visivel:

```bash
python3 "Idle Hero TD/scripts/extract_upgrade_levels_from_image.py" \
  --engine easyocr \
  --image screenshot.png \
  --grid 0.05,0.18,0.95,0.90 \
  --cols 2 \
  --rows 3 \
  --visible-keys researchDmg1,researchDmg2,researchDmg3,researchDmg4,researchDmg5,researchDmg6 \
  --output levels_visible.json
```

### 3. ROI calibrada

Modo mais confiavel. Gere um template:

```bash
python3 "Idle Hero TD/scripts/extract_upgrade_levels_from_image.py" \
  --print-config-template \
  --screen research-core \
  --output roi_research.json
```

Edite os `rect` para cada upgrade:

```json
{
  "upgrade_key": "researchDmg1",
  "rect": [0.05, 0.18, 0.48, 0.28]
}
```

Depois rode:

```bash
python3 "Idle Hero TD/scripts/extract_upgrade_levels_from_image.py" \
  --engine easyocr \
  --image screenshot.png \
  --config roi_research.json \
  --output levels_research.json
```

## Saidas

Relatorio completo:

```bash
python3 "Idle Hero TD/scripts/extract_upgrade_levels_from_image.py" \
  --engine easyocr \
  --image screenshot.png \
  --screen research-core \
  --format json \
  --output levels_full.json
```

CSV:

```bash
python3 "Idle Hero TD/scripts/extract_upgrade_levels_from_image.py" \
  --engine easyocr \
  --image screenshot.png \
  --screen research-core \
  --format csv \
  --output levels.csv
```

Estado pronto para otimizador:

```bash
python3 "Idle Hero TD/scripts/extract_upgrade_levels_from_image.py" \
  --engine easyocr \
  --image screenshot.png \
  --screen research-core \
  --format state \
  --objective FARM \
  --output optimizer_state.json
```

Esse formato gera:

```json
{
  "objective": "FARM",
  "resources": {
    "energy": "0",
    "prestige_points": "0"
  },
  "levels": {
    "researchDmg1": 123
  }
}
```

Preencha os recursos em escala do jogo (`K`, `M`, `B`, `T`, `1e15`) e use nos otimizadores.

Para juntar varias telas extraidas em um unico input, use:

```bash
python3 "Idle Hero TD/scripts/merge_optimizer_states.py" \
  --state levels_research.json \
  --state levels_prestige.json \
  --objective FARM \
  --energy 850K \
  --prestige-points 1,5B \
  --output estado_farm.json
```

O fluxo completo esta em `upgrade_ocr_to_optimizer_pipeline.md`.

## Debug

Para auditar o OCR:

```bash
python3 "Idle Hero TD/scripts/extract_upgrade_levels_from_image.py" \
  --image screenshot.png \
  --screen research-core \
  --dump-tsv ocr.tsv \
  --dump-ocr-text ocr_lines.txt \
  --output levels.json
```

Se algum level vier `null`, use `ocr_lines.txt` para ver o texto reconhecido e reduza/aumente a ROI.

## Casos de OCR cobertos

Casos corrigidos deterministicamente no teste:

- `Damage III (Lv 31)` lido como `Lv J1`, corrigido por bônus `+775% (+25%)`.
- `Kill Gold II (Lv 112)` lido como `Kill Gold I (Lv 1Z)`, corrigido por `(+10%)` e regra `1Z -> 112`.
- `Prestige Power IV (Lv 11)` lido como `Lv IW`, corrigido por bônus `+825% (+75%)`.
- `Kill Gold I` lido como `KILL Goup I` e `Kill Gold V` lido como `Ki COlD V`, corrigidos por normalizacao deterministica de texto OCR.

## Validador interno

```bash
python3 "Idle Hero TD/scripts/extract_upgrade_levels_from_image.py" --self-test
```

O self-test nao precisa de imagem nem de Tesseract; ele valida apenas o parser de TSV/regex.

## Limites

- OCR nao e leitura direta do save; e leitura visual.
- Fonte estilizada, baixa resolucao ou screenshot comprimido podem exigir ROI calibrada.
- O script nao tenta adivinhar com IA; se o texto nao for reconhecido ou a ROI estiver errada, retorna `null` e aviso.
- Para alta confiabilidade, use uma captura sempre na mesma resolucao e uma config ROI por tela.
