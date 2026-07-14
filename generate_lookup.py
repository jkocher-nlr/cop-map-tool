#!/usr/bin/env python3
"""
Generate R410A refrigerant property lookup tables using CoolProp.

Run this script (with CoolProp installed) to produce r410a_props.npz,
which is served as a static asset by the GitHub Pages web tool.

Usage:
    python generate_lookup.py
"""
import numpy as np
import CoolProp.CoolProp as CP

FLUID = "R410A"

T_crit_K = CP.PropsSI("Tcrit", FLUID)
P_crit   = CP.PropsSI("Pcrit", FLUID)
print(f"R410A  Tcrit = {T_crit_K - 273.15:.2f} °C   Pcrit = {P_crit/1e6:.3f} MPa")

# ── Saturation table ─────────────────────────────────────────────────────────
# Cover -50 °C to 71 °C (0.5 °C steps) — safely below Tcrit ≈ 72.1 °C
T_sat_C = np.arange(-50.0, 71.5, 0.5)
T_sat_K = T_sat_C + 273.15
n_sat   = len(T_sat_C)

P_sat = np.empty(n_sat)
h_f   = np.empty(n_sat)
h_g   = np.empty(n_sat)
s_f   = np.empty(n_sat)
s_g   = np.empty(n_sat)

print(f"Saturation table: {n_sat} points …")
for i, T in enumerate(T_sat_K):
    P_sat[i] = CP.PropsSI("P", "T", T, "Q", 0, FLUID)   # Q=0 or 1 both give P_sat
    h_f[i]   = CP.PropsSI("H", "T", T, "Q", 0, FLUID)
    h_g[i]   = CP.PropsSI("H", "T", T, "Q", 1, FLUID)
    s_f[i]   = CP.PropsSI("S", "T", T, "Q", 0, FLUID)
    s_g[i]   = CP.PropsSI("S", "T", T, "Q", 1, FLUID)
print("  done.")

# ── Superheated vapour table ──────────────────────────────────────────────────
# Temperature axis: -45 °C to 200 °C in 2 °C steps
# Pressure axis:  100 kPa to 5 100 kPa, 60 log-spaced points
#
# Cells where T <= T_sat(P) are left as NaN (two-phase / subcooled).
T_super_C = np.arange(-45.0, 201.0, 2.0)
T_super_K = T_super_C + 273.15
P_super   = np.logspace(np.log10(100e3), np.log10(5100e3), 60)

n_T = len(T_super_C)
n_P = len(P_super)

h_super = np.full((n_T, n_P), np.nan)
s_super = np.full((n_T, n_P), np.nan)

print(f"Superheated vapour table: {n_T} × {n_P} = {n_T * n_P} cells …")
for j, P in enumerate(P_super):
    try:
        T_bub_K = CP.PropsSI("T", "P", P, "Q", 1, FLUID)
    except Exception:
        continue
    for i, T_K in enumerate(T_super_K):
        if T_K <= T_bub_K:
            continue
        try:
            h_super[i, j] = CP.PropsSI("H", "T", T_K, "P", P, FLUID)
            s_super[i, j] = CP.PropsSI("S", "T", T_K, "P", P, FLUID)
        except Exception:
            pass
    if (j + 1) % 10 == 0:
        print(f"  P col {j+1:3d}/{n_P}: {P/1e6:.3f} MPa")

print(f"  done.  NaN fraction: {np.isnan(h_super).mean():.1%}")

# ── Save ──────────────────────────────────────────────────────────────────────
out = "r410a_props.npz"
np.savez_compressed(
    out,
    T_sat_C   = T_sat_C,
    P_sat     = P_sat,
    h_f       = h_f,
    h_g       = h_g,
    s_f       = s_f,
    s_g       = s_g,
    T_super_C = T_super_C,
    P_super   = P_super,
    h_super   = h_super,
    s_super   = s_super,
)
import os
size_kb = os.path.getsize(out) / 1024
print(f"\nSaved {out}  ({size_kb:.0f} KB)")
print(f"  Saturation : {n_sat} pts, {T_sat_C[0]:.0f} – {T_sat_C[-1]:.0f} °C")
print(f"  Superheated: T {T_super_C[0]:.0f} – {T_super_C[-1]:.0f} °C  |"
      f"  P {P_super[0]/1e6:.3f} – {P_super[-1]/1e6:.2f} MPa")
