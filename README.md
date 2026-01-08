# SolProp_ML Automated Predictions

Automated solubility and thermodynamic property predictions using MIT's SolProp_ML.

## 🎯 What This Does

- Predicts **solubility** in organic solvents
- Calculates **thermodynamic properties** (Gsolv, Hsolv, Saq)
- Uses **machine learning models** trained on experimental data
- Automated via **GitHub Actions**

## 🚀 How to Use

### 1. Add Your Molecules

Edit `input/compounds.csv` with your molecules:
```csv
solute,solvent,temperature
CC(=O)O,CCO,298.15
c1ccccc1,CCCCCC,298.15
```

**Columns:**
- `solute` (required): SMILES notation of molecule
- `solvent` (optional): SMILES of solvent
- `temperature` (optional): Temperature in Kelvin

### 2. Run Predictions

**Option A - Automatic:**
```bash
git add input/compounds.csv
git commit -m "Add molecules for prediction"
git push
```

**Option B - Manual:**
1. Go to **Actions** tab
2. Click **SolProp ML Prediction (Real)**
3. Click **Run workflow**

### 3. Get Results

**Download from Artifacts:**
1. Go to **Actions** → Your workflow run
2. Scroll to **Artifacts**
3. Download `solprop-results-XXX`

**Or check the `output/` folder** (auto-committed)

## 📊 Output Files

| File | Description |
|------|-------------|
| `*_results_*.csv` | Main solubility predictions (logS) |
| `*_detailed_*.csv` | Detailed calculations |
| `*_properties_*.csv` | Molecular properties (Gsolv, Hsolv, Saq) |
| `*_log_*.log` | Execution log |
| `*_summary_*.txt` | Quick summary |

## 🔬 Supported Molecules

✅ Neutral organic compounds  
✅ Elements: H, B, C, N, O, S, P, F, Cl, Br, I  
❌ Ionic species  
❌ Mixtures  

## 📝 SMILES Examples

| Molecule | SMILES |
|----------|--------|
| Acetic acid | `CC(=O)O` |
| Benzene | `c1ccccc1` |
| Ethanol | `CCO` |
| Water | `O` |
| Hexane | `CCCCCC` |

## 🎓 Citation
