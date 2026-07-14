# Quick Start Guide

## Testing Locally

You can test the web app locally using a simple HTTP server:

```bash
cd cop-map-tool
python -m http.server 8000
```

Then open **http://localhost:8000** in your browser.

*Note: Pyodide requires HTTPS or localhost. It will fail if served via file:// protocol.*

## Deploying to GitHub Pages

### 1. Create a GitHub repository

```bash
cd cop-map-tool
git init
git add .
git commit -m "Heat pump COP map - initial commit"
git remote add origin https://github.com/YOUR_USERNAME/cop-map-tool.git
git branch -M main
git push -u origin main
```

### 2. Enable GitHub Pages

- Log in to GitHub
- Go to your **cop-map-tool** repository
- Click **Settings** → **Pages**
- Under "Build and deployment", select:
  - **Source**: Deploy from a branch
  - **Branch**: main
  - **Folder**: / (root)
- Click **Save**
- Wait 1–2 minutes for deployment

### 3. Access your live map

Your site will be available at:  
**https://YOUR_USERNAME.github.io/cop-map-tool/**

## Customising the Model

### Change supply-air temperature

Edit [index.html](index.html), line ~85:
```javascript
const T_SUPPLY = 12.0;   // Change this value
```

### Adjust grid resolution

Line ~86:
```javascript
const GRID_DEG = 5;      // Use 2.5, 5, 10, etc.
```

**Smaller grid** = more detail, longer computation.

### Regenerate the R410A lookup table

If you modify refrigerant selection or temperature range:

```bash
pip install CoolProp numpy
python generate_lookup.py
```

Edit [generate_lookup.py](generate_lookup.py) to change:
- Temperature range (line ~15)
- Saturation coverage (line ~18)
- Pressure range for superheated grid (line ~29)

## Troubleshooting

### "Pyodide not found"
- Ensure your site is served over **HTTPS** or from **localhost**
- File:// URLs won't work

### "Weather API error"
- Open-Meteo is public and free; check your internet connection
- The API returns NaN for locations with no data

### Map takes >10 seconds to load
- First-time Pyodide download is ~30–50 MB (cached)
- Subsequent loads are much faster

## Architecture

```
Browser (index.html)
  ├─ Leaflet (map rendering)
  ├─ Leaflet.heat (heatmap layer)
  ├─ Pyodide (Python runtime)
  │  └─ cop_model.py (loaded, initialised)
  │     └─ r410a_props.npz (loaded into Python)
  ├─ Turf.js (land filtering)
  └─ Open-Meteo API (current weather)

Local development
  ├─ generate_lookup.py  (CoolProp → .npz)
  └─ CoolProp + NumPy
```

## Files

| File | Purpose | Size |
|------|---------|------|
| `index.html` | Web interface | ~19 KB |
| `cop_model.py` | Thermodynamic model | ~7 KB |
| `r410a_props.npz` | R410A property tables (CoolProp) | ~96 KB |
| `generate_lookup.py` | Lookup table generator | ~3.5 KB |
| `README.md` | Overview | ~3 KB |
| `.nojekyll` | GitHub Pages config | 0 bytes |

**Total static size: ~130 KB**

---

**Questions?** Review the comments in [cop_model.py](cop_model.py) and [index.html](index.html).
