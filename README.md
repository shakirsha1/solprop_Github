# SolProp ML GitHub Automation

Automated solubility prediction pipeline using SolProp_ML and GitHub Actions.

## 📁 Repository Structure

```
your-repo/
├── .github/
│   └── workflows/
│       └── solprop_prediction.yml    # GitHub Actions workflow
├── input/
│   └── input.csv                      # Your input files go here
├── output/                            # Results will be saved here
│   └── .gitkeep
├── scripts/
│   └── run_prediction.py              # Python prediction script
└── README.md
```

## 🚀 Quick Start

### 1. Set Up Your Repository

1. Create a new GitHub repository
2. Create the following folder structure:
   ```bash
   mkdir -p .github/workflows input output scripts
   touch output/.gitkeep
   ```

3. Add all files from this setup to your repository

### 2. Prepare Your Input File

Create a CSV file in the `input/` folder with the following columns:

| Column | Required | Description |
|--------|----------|-------------|
| `solute` | ✅ Yes | SMILES or InChI of solute compound |
| `solvent` | ❌ No | SMILES or InChI of solvent |
| `temperature` | ❌ No | Temperature in Kelvin (default: 298.15) |
| `reference_solubility` | ❌ No | Reference solubility value |
| `reference_solvent` | ❌ No | Reference solvent for calculations |

**Example:**
```csv
solute,solvent,temperature,reference_solubility,reference_solvent
CC(=O)O,CCO,298.15,,
c1ccccc1,CCCCCC,298.15,,
CC(C)O,O,298.15,,
```

### 3. Run Predictions

#### Method 1: Automatic (on file push)
Simply push your input CSV file to the `input/` folder:
```bash
git add input/your_input.csv
git commit -m "Add input file for prediction"
git push
```

#### Method 2: Manual trigger
1. Go to your repository on GitHub
2. Click on "Actions" tab
3. Select "SolProp ML Prediction" workflow
4. Click "Run workflow"
5. Enter the name of your input file (e.g., `input.csv`)
6. Click "Run workflow"

### 4. Download Results

After the workflow completes:

1. Go to the "Actions" tab
2. Click on your workflow run
3. Scroll down to "Artifacts"
4. Download the "prediction-results" artifact

Or, check the `output/` folder in your repository (results are automatically committed).

## 📊 Output Files

The automation generates several output files:

| File | Description |
|------|-------------|
| `*_results_*.csv` | Main solubility prediction results |
| `*_detailed_*.csv` | Detailed calculation results |
| `*_properties_*.csv` | Predicted molecular properties |
| `*_log_*.log` | Execution log with details |

## 🔧 Customization

### Modify Prediction Settings

Edit `scripts/run_prediction.py` to change prediction parameters:

```python
# Change these options
calculate_solubility(
    path=str(input_file),
    validate_smiles=True,        # Validate SMILES
    calculate_aqueous=False,     # Use aqueous solubility
    reduced_number=False,        # Use reduced model ensemble
    export_csv=str(results_file)
)
```

### Change Workflow Trigger

Edit `.github/workflows/solprop_prediction.yml`:

```yaml
# Run on schedule (daily at midnight)
on:
  schedule:
    - cron: '0 0 * * *'
  
# Or run on pull request
on:
  pull_request:
    paths:
      - 'input/**'
```

## 🧪 Supported Molecules

- **Solutes**: Electrically neutral compounds containing H, B, C, N, O, S, P, F, Cl, Br, I
- **Solvents**: Non-ionic liquid solvents
- **Not supported**: Mixture solvents/solutes, ionic compounds

## ⚠️ Important Notes

1. **First run**: The first workflow run may take 10-15 minutes as it installs dependencies
2. **File size**: Keep input files under 100 MB
3. **Processing time**: Large files may take several minutes
4. **API limits**: GitHub Actions has usage limits (2000 minutes/month for free tier)

## 📝 Input Format Examples

### Minimum required (solute only):
```csv
solute
CC(=O)O
c1ccccc1
CCO
```

### With solvent and temperature:
```csv
solute,solvent,temperature
CC(=O)O,CCO,298.15
c1ccccc1,CCCCCC,310.15
```

### With reference solubility:
```csv
solute,solvent,temperature,reference_solubility,reference_solvent
c1ccccc1O,CCO,298.15,-0.5,
```

## 🐛 Troubleshooting

**Workflow fails:**
- Check that your CSV file is properly formatted
- Ensure SMILES strings are valid
- Check the workflow logs in the Actions tab

**No output files:**
- Verify the input file is in the `input/` folder
- Check that the file has a `.csv` extension
- Review the error log in the output folder

**Invalid predictions:**
- Ensure molecules are within supported types
- Check that temperature is in Kelvin
- Verify SMILES/InChI strings are correct

## 📚 References

- [SolProp_ML Repository](https://github.com/fhvermei/SolProp_ML)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 📄 License

This automation setup is provided as-is. SolProp_ML is distributed under Creative Commons Attribution 4.0 International.

## 🤝 Contributing

Issues and pull requests are welcome to improve this automation setup!
