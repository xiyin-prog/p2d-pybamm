"""
复现《P2D 模型》知乎文章中所有仿真数字的脚本。
运行环境：PyBaMM 26.10，参数集 Chen2020（LG M50, 5 Ah 21700）。
不同 PyBaMM 版本的数字会有 ~1–2% 的差异，作图时请与本脚本同一版本。
"""
import numpy as np
import pybamm

PV = pybamm.ParameterValues("Chen2020")
A = PV["Electrode height [m]"] * PV["Electrode width [m]"]  # 电极面积 m^2


def solve(model, step, pv=None, soc=None):
    exp = pybamm.Experiment([step], period="10 seconds")
    sim = pybamm.Simulation(model, parameter_values=(pv or PV).copy(), experiment=exp)
    return sim.solve(initial_soc=soc)


def cap(sol):
    return abs(sol["Discharge capacity [A.h]"].entries[-1])


print("== 1. 倍率性能（DFN）==")
for c in [0.5, 1, 2, 3]:
    print(f"{c}C: {cap(solve(pybamm.lithium_ion.DFN(), f'Discharge at {c}C until 2.5 V')):.2f} Ah")

print("\n== 2. 2C / 3C 放电：电解液浓度与正极反应分布 ==")
for c in [2, 3]:
    s = solve(pybamm.lithium_ion.DFN(), f"Discharge at {c}C until 2.5 V")
    t = s["Time [s]"].entries
    ce = s["Electrolyte concentration [mol.m-3]"].entries
    jp = s["Positive electrode interfacial current density [A.m-2]"].entries
    sp = s["Positive particle surface stoichiometry"].entries
    print(f"{c}C 结束于 {t[-1]:.0f} s, c_e 最高 {ce.max():.0f}, 最低 {ce.min():.0f} mol/m3")
    for k in np.linspace(0, len(t) - 1, 5).astype(int):
        print(f"   t={t[k]:5.0f}s  c_e min={ce[:, k].min():6.0f}  "
              f"j_p(隔膜侧)={jp[0, k]:6.2f}  j_p(集流体侧)={jp[-1, k]:6.2f} A/m2")
    print(f"   结束时正极表面化学计量比：隔膜侧 {sp[0, -1]:.2f}，集流体侧 {sp[-1, -1]:.2f}")

print("\n== 3. 电极加厚一倍（正负极同时加厚，孔隙率/粒径不变）==")
pv2 = PV.copy()
for k in ["Negative electrode thickness [m]", "Positive electrode thickness [m]"]:
    pv2[k] = 2 * PV[k]
pv2["Nominal cell capacity [A.h]"] = 2 * PV["Nominal cell capacity [A.h]"]
for I in [5, 10, 20]:
    thin = cap(solve(pybamm.lithium_ion.DFN(), f"Discharge at {I} A until 2.5 V"))
    thick = cap(solve(pybamm.lithium_ion.DFN(), f"Discharge at {I} A until 2.5 V", pv=pv2))
    print(f"{I:>2} A: 原电池 {thin:.2f} Ah | 加厚电池 {thick:.2f} Ah")

print("\n== 4. SPM / SPMe / DFN 对比 ==")
for c in [0.5, 2]:
    out = []
    for name, M in [("SPM", pybamm.lithium_ion.SPM), ("SPMe", pybamm.lithium_ion.SPMe),
                    ("DFN", pybamm.lithium_ion.DFN)]:
        out.append(f"{name} {cap(solve(M(), f'Discharge at {c}C until 2.5 V')):.2f}")
    print(f"{c}C: " + " | ".join(out) + " Ah")

print("\n== 5. 析锂判据 phi_s - phi_e（10% SOC 起恒流充电至 4.2 V）==")


def plating(pv, c, label):
    s = solve(pybamm.lithium_ion.DFN(), f"Charge at {c}C until 4.2 V", pv=pv, soc=0.1)
    d = (s["Negative electrode potential [V]"].entries
         - s["Negative electrolyte potential [V]"].entries)
    xn = s["x_n [m]"].entries[:, 0] * 1e6
    t = s["Time [s]"].entries
    m = d.min(axis=1)  # 每个位置在整个充电过程中的最小值
    msg = (f"{label} {c}C: 充电 {t[-1]:.0f} s / {cap(s):.2f} Ah 后触及 4.2 V；"
           f"最低 {m.min():+.3f} V（x={xn[m.argmin()]:.0f}/{xn[-1]:.0f} μm）；"
           f"跌破 0 的区域占负极厚度 {np.mean(m < 0):.0%}")
    below = np.where(d.min(axis=0) < 0)[0]
    if len(below):
        k = below[0]
        msg += f"；首次跌破 0：t={t[k]:.0f} s, x={xn[np.argmin(d[:, k])]:.0f} μm"
    print(msg)


plating(PV, 1, "原电池")
plating(PV, 3, "原电池")
pv3 = PV.copy()
pv3["Negative electrode thickness [m]"] = 2 * PV["Negative electrode thickness [m]"]
plating(pv3, 3, "负极加厚")

print("\n== 6. 量级估算用参数 ==")
for k in ["Negative particle radius [m]", "Negative particle diffusivity [m2.s-1]",
          "Positive particle radius [m]", "Positive particle diffusivity [m2.s-1]",
          "Positive electrode thickness [m]", "Positive electrode porosity",
          "Cation transference number"]:
    print(k, PV[k])
print("电极面积 [m2]", A, "；1C 面电流密度 [A/m2]", 5 / A)
