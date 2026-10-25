# 用 PyBaMM 理解 P2D（Doyle–Fuller–Newman）锂离子电池模型

**English.** Scripts for a Chinese explainer (Zhihu article / Bilibili video) of the pseudo-two-dimensional Doyle–Fuller–Newman (P2D / DFN) lithium-ion model. Simulations use [PyBaMM](https://pybamm.org) ≥ 26.10 with the Chen2020 parameter set (LG M50, 5 Ah 21700). `python simulate.py` writes `data/final_data.npz`; `python make_figures.py` draws 18 figures into `figs/`; `python verify.py` recomputes the headline numbers on its own.

## 这是什么

P2D（也常称作 DFN）把多孔电极沿厚度方向看成一维坐标 \(x\)，再在每个 \(x\) 上挂一个只用半径 \(r\) 描述的活性颗粒，所以叫“伪二维”。电解液锂盐浓度 \(c_e\)、固相锂浓度 \(c_s\)、液相电势 \(\phi_e\)、固相电势 \(\phi_s\) 由四个守恒方程描述，并在颗粒表面用 Butler–Volmer 动力学连在一起。

本仓库用 PyBaMM 的 `lithium_ion.DFN` 和 Chen2020 参数集（LG M50，标称 5 Ah 的 21700 电芯）复现文章和视频里的仿真数字与 18 张图。图为白底、无网格，优先使用 Noto Sans CJK SC。

| 脚本 | 作用 |
| --- | --- |
| `simulate.py` | 跑完全部仿真，写出 `data/final_data.npz` |
| `make_figures.py` | 从 npz 画出 18 张图到 `figs/` |
| `verify.py` | 不读 npz，独立重算并打印关键数字 |

## 安装

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

中文标注需要 **Noto Sans CJK SC**。Debian / Ubuntu 可安装：

```bash
sudo apt install fonts-noto-cjk
```

未找到该字体时，`make_figures.py` 会给出警告并回退到 DejaVu Sans（中文可能显示为方框）。

## 运行

```bash
python simulate.py
python make_figures.py
python verify.py
```

先仿真、再作图。`verify.py` 会重新求解，不依赖 `data/final_data.npz`，用来核对下面的数字。PyBaMM 小版本不同时，容量大约会有 1%–2% 的差别，作图请与仿真使用同一版本。

路径可以用参数改掉（目录不存在时会自动创建）：

```bash
python simulate.py --output data/final_data.npz
python make_figures.py --data data/final_data.npz --figs figs
```

## 生成的图

| 文件 | 内容 |
| --- | --- |
| `figs/fig01_电池三明治结构.png` | 铜箔 / 负极 / 隔膜 / 正极 / 铝箔，以及多孔电极放大 |
| `figs/fig02_伪二维.png` | 厚度坐标 \(x\) 上每个位置挂一个只靠半径 \(r\) 描述的颗粒 |
| `figs/fig03_四守恒一连接.png` | \(c_s\)、\(c_e\)、\(\phi_s\)、\(\phi_e\) 与 Butler–Volmer |
| `figs/fig04_球壳控制体.png` | 薄球壳控制体：对 \(r^2 N\) 求导，以及球心、表面边界 |
| `figs/fig05_比表面积推导.png` | \(a_s = 3\varepsilon_s / R_p\) |
| `figs/fig06_两相电流交接.png` | 放电时固相电流与液相电流沿厚度交接（反应均匀的示意） |
| `figs/fig07_修正欧姆定律.png` | 2C、1500 s 时液相电势降拆成欧姆项与浓差项 |
| `figs/fig08_电解液锂守恒.png` | \(t_+\) 随电流带走、\(1-t_+\) 留在原地靠扩散 |
| `figs/fig09_ButlerVolmer.png` | Butler–Volmer 曲线，以及小过电位线性近似、大过电位 Tafel 近似 |
| `figs/fig10_边界条件.png` | 集流体与电极/隔膜界面：谁能过电子、谁能过离子 |
| `figs/fig11_P2D方程总览.png` | 五个方程的耦合矩阵；必须联立求解 DAE |
| `figs/fig12_倍率放电曲线.png` | 0.5C / 1C / 2C / 3C 恒流放电至 2.5 V |
| `figs/fig13_正极电解液浓度分布.png` | 3C 放电时正极集流体侧盐被抽干 |
| `figs/fig14_正极反应分布.png` | 3C 放电时反应挤向隔膜侧 |
| `figs/fig15_厚电极对比.png` | 正负极同时加厚一倍后，5 A 与 10 A 放电 |
| `figs/fig16_快充析锂判据.png` | 10% SOC 起充电至 4.2 V，负极 \(\min(\phi_s-\phi_e)\) |
| `figs/fig17_SPM_SPMe_DFN对比.png` | SPM、SPMe 与 DFN（P2D）在 0.5C、2C 的放电曲线 |
| `figs/fig18_混合超级电容界面.png` | 法拉第电流 \(j\) 与双电层电流 \(i_{dl}\)（示意图，不来自本次数值解） |

## 关键结果

PyBaMM 26.10，Chen2020，DFN，放电截止 2.5 V。容量取放电结束时的放电容量。

恒流放电容量：

| 倍率 | 0.5C | 1C | 2C | 3C |
| --- | --- | --- | --- | --- |
| 容量 | 5.02 Ah | 4.94 Ah | 4.73 Ah | 2.30 Ah |

正负极厚度同时加倍（标称容量改为 10 Ah，孔隙率与粒径不变），**10 A** 放电：加厚电芯 **3.33 Ah**，原电芯 **4.73 Ah**。同样的绝对电流下，更厚的电极更早被电解液输运限制住。

快充析锂判据为充电全程、负极各处的 \(\min(\phi_s - \phi_e)\)。从 10% SOC 恒流充电，端电压到达 4.2 V 为止：

| 工况 | \(\min(\phi_s-\phi_e)\) | 备注 |
| --- | --- | --- |
| 1C | −0.015 V | |
| 3C | −0.134 V | 235 s、0.98 Ah 时到达 4.2 V |
| 负极加厚一倍，3C | −0.218 V | |

2C 放电容量，三个模型：

| 模型 | SPM | SPMe | DFN (P2D) |
| --- | --- | --- | --- |
| 2C 容量 | 4.82 Ah | 4.76 Ah | 4.73 Ah |

低倍率下三者接近；2C 时电解液浓差和液相电势降开始把 SPMe、DFN 和最简单的 SPM 分开。

## 模型边界

这些数字是**等温**模型算出来的，没有热耦合。析锂只用作判据：\(\phi_s - \phi_e < 0\) 表示该处有析锂的热力学倾向，仿真里**没有**析锂副反应，锂也不会真的在表面上长出来。Chen2020 的负极是**单相石墨**，没有石墨的多级嵌锂平台。

## 参考文献

1. Doyle, M., Fuller, T. F., & Newman, J. (1993). Modeling of galvanostatic charge and discharge of the lithium/polymer/insertion cell. *Journal of The Electrochemical Society*, 140(6), 1526–1533.
2. Chen, C.-H., Brosa Planella, F., O'Regan, K., Gastol, D., Widanage, W. D., & Kendrick, E. (2020). Development of experimental techniques for parameterization of multi-scale lithium-ion battery models. *Journal of The Electrochemical Society*, 167, 080534.
3. Sulzer, V., Marquis, S. G., Timms, R., Robinson, M., & Chapman, S. J. (2021). Python Battery Mathematical Modelling (PyBaMM). *Journal of Open Research Software*, 9, 14.

## 许可

[MIT License](LICENSE). Copyright (c) 2026 Wangkai-prog.
