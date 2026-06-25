# Hero synergy map

Mapa completo de sinergias extraido dos MonoBehaviours `Hero` do Unity.

Arquivos gerados:

- `csv/sinergias_mapa.csv`: uma linha por heroi e numero de sinergia.
- `csv/sinergias_arestas.csv`: uma linha por relacao heroi -> parceiro exigido.
- `csv/sinergias_matriz.csv`: uma linha por heroi, com as 16 sinergias em colunas.

Leitura:

- `required_hero_names` lista os parceiros exigidos alem do proprio heroi.
- `active_heroes_needed_including_self` inclui o proprio heroi na contagem.
- `tier` agrupa duas sinergias por tier; `rank_required` e o rank minimo de todos os herois exigidos.
- `synergy_upgrade_name` e o efeito aplicado quando a sinergia esta ativa.
- `base_bonus_text` e o valor base estatico calculado do APK antes de modificadores dinamicos de save/mapa/slot.

Total de herois: 42
Total de sinergias: 672
Total de arestas/parceiros exigidos: 1134
Total de linhas na matriz: 42
