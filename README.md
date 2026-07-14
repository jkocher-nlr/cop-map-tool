# Heat Pump COP Map

An interactive web tool that displays **R410A refrigerant heat pump coefficient of performance (COP)** across the globe using real-time weather data.

## Features

- **Leaflet-based map** with continuous heatmap overlay
- **Current weather integration** via Open-Meteo (free, no API key required)
- **Thermodynamic model** in Python (via Pyodide) running entirely in the browser
- **Click-to-query** any location for detailed cycle analysis
- **Land-only grid** (water points excluded) at 5° resolution

## Cycle Model

The tool models a **vapour-compression refrigeration cycle** with:
- Fixed **supply-air temperature: 12 °C** (user-selectable in principle)
- **Evaporator saturation** at T_supply − 4 °C
- **Condenser saturation** at T_ambient + 7 °C
- 5 °C superheat at evaporator inlet
- **75% isentropic efficiency** compressor
- Isenthalpic throttle (state 7 = state 6 enthalpy)

**COP = (h₂ − h₇) / (h₃ − h₂)**, where:
- h₂ = evaporator outlet (superheated)
- h₃ = compressor discharge (actual, 75% isentropic)
- h₇ = throttle inlet (subcooled liquid)

## Files

| File | Purpose |
|------|---------|
| **index.html** | Main web app; Leaflet + Pyodide + Open-Meteo |
| **cop_model.py** | Thermodynamic cycle model (numpy-only for Pyodide) |
| **r410a_props.npz** | Pre-computed R410A saturation & superheated tables (CoolProp) |
| **generate_lookup.py** | Script to regenerate .npz lookup table |
| **.nojekyll** | GitHub Pages signal to skip Jekyll (preserves .py files) |

## Building the Lookup Table

On your local machine (requires **CoolProp** + **numpy**):

```bash
pip install CoolProp numpy
python generate_lookup.py
```

This produces **r410a_props.npz** (~96 KB, compressed).

## Deployment

1. **Create a GitHub repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/cop-map-tool.git
   git push -u origin main
   ```

2. **Enable GitHub Pages**
   - Go to **Settings** → **Pages**
   - Select **Deploy from a branch**
   - Choose **main** branch, **root** folder
   - Click **Save**

3. **Wait for deployment** (~1–2 minutes)
   - Your site will be live at `https://YOUR_USERNAME.github.io/cop-map-tool/`

## Dependencies

### Browser (CDN)
- **Leaflet** + **Leaflet.heat** — interactive map + heatmap layer
- **Turf.js** — point-in-polygon (land masking)
- **TopoJSON** — world land shapes (110 m resolution)
- **Pyodide** — Python interpreter in WebAssembly
- **Open-Meteo API** — free weather data (no authentication)

### Local (development only)
- **Python 3.7+**
- **CoolProp 6.4+** — refrigerant properties
- **NumPy 1.14+** — array operations

## Color Scale

- **Blue** (intensity ≤ 0) — High COP (cool climate)
- **Red** (intensity ≥ 1) — Low COP (hot climate)
- Scale: COP 2–15

## Notes

- **Infeasible cycles** (ambient < ~0 °C) show as "N/A" on the map
- Lookup table covers **−50 to +71 °C saturation range** (COP model clips to valid region)
- **Superheated grid**: −45 to +199 °C, 60 pressure points (100 kPa – 5.1 MPa)

## License

This project is provided as-is. Refrigerant properties (CoolProp) are open-source under LGPL-2.1.
