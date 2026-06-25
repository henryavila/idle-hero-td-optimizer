# Tabela de custo Research - Damage, Gold e Prestige Power

Energy disponivel para MAX: `2,57M` (`2.570.000`).

Formula: `roundToEven(baseCost * targetLevel ^ multCost)`, somada nivel a nivel.

`MAX` simula gastar toda a Energy apenas naquele upgrade. Status `locked` significa bloqueado por wave no estado atual; os custos fixos sao teoricos.

| Grupo | Upgrade | Lv | Status | +1 | +10 | +100 | +1k | +10k | MAX com Energy | Sobra |
| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| Damage | `researchDmg1` | 446 | available | 2.235 | 22.575 | 248.250 | 4.732.500 | 272.325.000 | +661 lv -> 1107 / custo 2.567.985 | 2.015 |
| Damage | `researchDmg2` | 112 | available | 8.475 | 88.125 | 1.218.750 | 45.937.500 | 3.834.375.000 | +172 lv -> 284 / custo 2.560.650 | 9.350 |
| Damage | `researchDmg3` | 31 | available | 32.000 | 365.000 | 8.150.000 | 531.500.000 | 50.315.000.000 | +46 lv -> 77 / custo 2.507.000 | 63.000 |
| Damage | `researchDmg4` | 10 | available | 110.000 | 1.550.000 | 60.500.000 | 5.105.000.000 | 501.050.000.000 | +14 lv -> 24 / custo 2.450.000 | 120.000 |
| Damage | `researchDmg5` | 10 | available | 1.100.000 | 15.500.000 | 605.000.000 | 51.050.000.000 | 5.010.500.000.000 | +2 lv -> 12 / custo 2.300.000 | 270.000 |
| Damage | `researchDmg6` | 0 | locked | 1.500.000.026.624 | 4.537500080538E+15 | 3.825375067898E+19 | 3.757503816693E+23 | 3.750750104073E+27 | +0 lv -> 0 / custo 0 | 2.570.000 |
| Gold | `researchKillGold1` | 446 | available | 2.235 | 22.575 | 248.250 | 4.732.500 | 272.325.000 | +661 lv -> 1107 / custo 2.567.985 | 2.015 |
| Gold | `researchKillGold2` | 112 | available | 8.475 | 88.125 | 1.218.750 | 45.937.500 | 3.834.375.000 | +172 lv -> 284 / custo 2.560.650 | 9.350 |
| Gold | `researchKillGold3` | 30 | available | 31.000 | 355.000 | 8.050.000 | 530.500.000 | 50.305.000.000 | +47 lv -> 77 / custo 2.538.000 | 32.000 |
| Gold | `researchKillGold4` | 9 | available | 100.000 | 1.450.000 | 59.500.000 | 5.095.000.000 | 500.950.000.000 | +15 lv -> 24 / custo 2.550.000 | 20.000 |
| Gold | `researchKillGold5` | 3 | available | 400.000 | 8.500.000 | 535.000.000 | 50.350.000.000 | 5.003.500.000.000 | +4 lv -> 7 / custo 2.200.000 | 370.000 |
| Gold | `researchKillGold6` | 0 | locked | 1.500.000.026.624 | 4.537500080538E+15 | 3.825375067898E+19 | 3.757503816693E+23 | 3.750750104073E+27 | +0 lv -> 0 / custo 0 | 2.570.000 |
| Prestige | `researchPrestigePower1` | 765 | available | 7.660 | 77.050 | 815.500 | 12.655.000 | 576.550.000 | +283 lv -> 1048 / custo 2.566.810 | 3.190 |
| Prestige | `researchPrestigePower2` | 195 | available | 29.400 | 300.750 | 3.682.500 | 104.325.000 | 7.793.250.000 | +73 lv -> 268 / custo 2.540.400 | 29.600 |
| Prestige | `researchPrestigePower3` | 38 | available | 97.500 | 1.087.500 | 22.125.000 | 1.346.250.000 | 125.962.500.000 | +20 lv -> 58 / custo 2.425.000 | 145.000 |
| Prestige | `researchPrestigePower4` | 11 | available | 480.000 | 6.600.000 | 246.000.000 | 20.460.000.000 | 2.004.600.000.000 | +4 lv -> 15 / custo 2.160.000 | 410.000 |
| Prestige | `researchPrestigePower5` | 0 | locked | 24.999.999.488 | 75.624.998.451.200 | 6.375624869427E+17 | 6.262506121744E+21 | 6.251249934474E+25 | +0 lv -> 0 / custo 0 | 2.570.000 |
