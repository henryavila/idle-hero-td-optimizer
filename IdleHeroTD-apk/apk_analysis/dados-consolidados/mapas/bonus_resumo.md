# Map perks and placement bonuses

Dados extraidos dos MonoBehaviours `MapPerkUpgradeCell` e `MapPlacementUpgradeCell`.

Arquivos gerados:

- `csv/perks.csv`: perks por mapa (`map1` a `map7`).
- `csv/bonus_slots_posicionamento.csv`: upgrades de bonus de slot/posicionamento.

Leitura:

- `stat_amt` e o incremento principal por nivel do upgrade.
- `base_amt` aparece em perks de mapa e representa valor base quando aplicavel.
- `wave_req` e a wave exigida para desbloqueio quando o jogo define uma trava.
- `map_name` usa os nomes exibidos nos textos da UI dos mapas.
- Este arquivo inclui perks/upgrades extraidos de `MapPerkUpgradeCell`; os bonus fixos exibidos no painel do mapa ficam em `bonus_fixos.md`.

Total de perks de mapa: 56
Total de bonus de slot: 10
