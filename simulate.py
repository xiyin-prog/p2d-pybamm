"""Final-article simulations. PyBaMM 26.10.1.1, Chen2020.

Writes data/final_data.npz by default. Override with --output.
"""
import argparse
from pathlib import Path
import numpy as np, pybamm

parser = argparse.ArgumentParser(description="P2D/DFN simulations (PyBaMM, Chen2020)")
parser.add_argument(
    "--output",
    default="data/final_data.npz",
    help="npz output path (default: data/final_data.npz)",
)
args = parser.parse_args()
out_path = Path(args.output)
out_path.parent.mkdir(parents=True, exist_ok=True)

PV = pybamm.ParameterValues("Chen2020"); out = {}
def solve(model, step, pv=None, soc=None, period="10 seconds"):
    exp = pybamm.Experiment([step], period=period)
    return pybamm.Simulation(model, parameter_values=(pv or PV).copy(), experiment=exp).solve(initial_soc=soc)
DFN = pybamm.lithium_ion.DFN
for c in [0.5, 1, 2, 3]:
    s = solve(DFN(), f"Discharge at {c}C until 2.5 V")
    out[f"Q_{c}"] = s["Discharge capacity [A.h]"].entries; out[f"V_{c}"] = s["Voltage [V]"].entries
    if c in (2, 3):
        out[f"t_{c}"] = s["Time [s]"].entries; out["x"] = s["x [m]"].entries[:, 0]; out["xp"] = s["x_p [m]"].entries[:, 0]
        out[f"ce_{c}"] = s["Electrolyte concentration [mol.m-3]"].entries
        out[f"jp_{c}"] = s["Positive electrode interfacial current density [A.m-2]"].entries
        out[f"phie_{c}"] = s["Electrolyte potential [V]"].entries
        out[f"sp_{c}"] = s["Positive particle surface stoichiometry"].entries
pv2 = PV.copy()
for k in ["Negative electrode thickness [m]", "Positive electrode thickness [m]"]: pv2[k] = 2 * PV[k]
pv2["Nominal cell capacity [A.h]"] = 10.0
for I in [5, 10]:
    for tag, pv in [("thin", PV), ("thick", pv2)]:
        s = solve(DFN(), f"Discharge at {I} A until 2.5 V", pv=pv)
        out[f"{tag}_Q_{I}"] = s["Discharge capacity [A.h]"].entries; out[f"{tag}_V_{I}"] = s["Voltage [V]"].entries
for c in [0.5, 2]:
    for n, M in [("SPM", pybamm.lithium_ion.SPM), ("SPMe", pybamm.lithium_ion.SPMe), ("DFN", DFN)]:
        s = solve(M(), f"Discharge at {c}C until 2.5 V")
        out[f"{n}_Q_{c}"] = s["Discharge capacity [A.h]"].entries; out[f"{n}_V_{c}"] = s["Voltage [V]"].entries
pv3 = PV.copy(); pv3["Negative electrode thickness [m]"] = 2 * PV["Negative electrode thickness [m]"]
for tag, pv, c in [("1C", PV, 1), ("3C", PV, 3), ("3Cthick", pv3, 3)]:
    s = solve(DFN(), f"Charge at {c}C until 4.2 V", pv=pv, soc=0.1)
    d = s["Negative electrode potential [V]"].entries - s["Negative electrolyte potential [V]"].entries
    out[f"pl_{tag}"] = d; out[f"plt_{tag}"] = s["Time [s]"].entries; out[f"plx_{tag}"] = s["x_n [m]"].entries[:, 0]
    out[f"plQ_{tag}"] = s["Discharge capacity [A.h]"].entries
# old-setup check: no experiment, current function, t_end 900 s, upper cutoff 4.4 V (as in old sim.py)
for c in [1, 3]:
    p = PV.copy(); p["Current function [A]"] = -c * 5.0; p["Upper voltage cut-off [V]"] = 4.4; p["Lower voltage cut-off [V]"] = 2.0
    s = pybamm.Simulation(DFN(), parameter_values=p).solve([0, 900], initial_soc=0.1)
    d = s["Negative electrode potential [V]"].entries - s["Negative electrolyte potential [V]"].entries
    print(f"OLD setup {c}C: ran {s['Time [s]'].entries[-1]:.0f} s, V_end {s['Voltage [V]'].entries[-1]:.3f}, min {d.min():+.3f} V")
    p["Upper voltage cut-off [V]"] = 4.2
    s = pybamm.Simulation(DFN(), parameter_values=p).solve([0, 900], initial_soc=0.1)
    d = s["Negative electrode potential [V]"].entries - s["Negative electrolyte potential [V]"].entries
    print(f"OLD setup but 4.2V cutoff {c}C: ran {s['Time [s]'].entries[-1]:.0f} s, min {d.min():+.3f} V")
np.savez(out_path, **out)
t = out["t_2"]; k = np.argmin(abs(t - 1500)); ce = out["ce_2"][:, k]
print("2C@%.0fs ce max %.0f min %.0f ; conc term %.3f V" % (t[k], ce.max(), ce.min(), 2*8.314*298.15/96485*(1-0.2594)*np.log(ce.max()/ce.min())))
ce = out["ce_2"][:, -1]; print("2C end ce max %.0f min %.0f ; conc term %.3f V" % (ce.max(), ce.min(), 2*8.314*298.15/96485*(1-0.2594)*np.log(ce.max()/ce.min())))
De = PV["Electrolyte diffusivity [m2.s-1]"]
print("De(1000)", PV.evaluate(De(pybamm.Scalar(1000), pybamm.Scalar(298.15))))
