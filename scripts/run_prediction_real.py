#!/usr/bin/env python
"""
Real SolProp ML Prediction Script
Uses actual SolProp_ML package for solubility predictions
"""

import os
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime

# Add SolProp_ML to path
sys.path.insert(0, str(Path.cwd() / 'SolProp_ML'))

def main():
    print("="*60)
    print("SolProp ML - Solubility Prediction")
    print("="*60)
    
    # Set up paths
    input_dir = Path('input')
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    # Find all CSV files in input directory
    input_files = list(input_dir.glob('*.csv'))
    
    if not input_files:
        print("❌ ERROR: No input CSV files found in 'input/' directory")
        print("\nPlease add a CSV file with the following columns:")
        print("  - solute (required): SMILES or InChI of solute")
        print("  - solvent (optional): SMILES or InChI of solvent")
        print("  - temperature (optional): Temperature in Kelvin")
        sys.exit(1)
    
    print(f"\n✓ Found {len(input_files)} input file(s)")
    
    # Import SolProp_ML
    try:
        from solvation_predictor.calculate_solubility import calculate_solubility, predict_property
        print("✓ SolProp_ML successfully imported")
    except ImportError as e:
        print(f"❌ ERROR: Failed to import SolProp_ML: {e}")
        print("\nMake sure SolProp_ML is installed correctly.")
        sys.exit(1)
    
    # Process each input file
    all_success = True
    
    for input_file in input_files:
        print(f"\n{'='*60}")
        print(f"📄 Processing: {input_file.name}")
        print(f"{'='*60}")
        
        # Generate output filenames with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = input_file.stem
        
        results_file = output_dir / f"{base_name}_results_{timestamp}.csv"
        detailed_file = output_dir / f"{base_name}_detailed_{timestamp}.csv"
        properties_file = output_dir / f"{base_name}_properties_{timestamp}.csv"
        log_file = output_dir / f"{base_name}_log_{timestamp}.log"
        
        try:
            # Read input CSV
            df = pd.read_csv(input_file)
            
            # Run solubility calculations
            print("\n🔬 Running solubility calculations...")
            results = calculate_solubility(
                path=str(input_file),
                export_csv=str(results_file),
                export_detailed_csv=str(detailed_file),
                logger=str(log_file)
            )
            
            print(f"  ✓ Main results: {results_file.name}")
            print(f"  ✓ Detailed results: {detailed_file.name}")
            print(f"  ✓ Log file: {log_file.name}")
            
            # Run property predictions
            print("\n🧪 Running property predictions...")
            predictions = predict_property(
                df=df,
                gsolv=True,
                hsolv=True,
                saq=True,
                solute_parameters=True,
                export_csv=str(properties_file),
                logger=str(log_file)
            )
            
            print(f"  ✓ Properties: {properties_file.name}")
            
            # Create summary
            summary_file = output_dir / f"{base_name}_summary_{timestamp}.txt"
            with open(summary_file, 'w') as f:
                f.write("SolProp ML - Prediction Summary\n")
                f.write("="*60 + "\n\n")
                f.write(f"Input file: {input_file.name}\n")
                f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"\nOutput files:\n")
                f.write(f"  - {results_file.name}\n")
                f.write(f"  - {detailed_file.name}\n")
                f.write(f"  - {properties_file.name}\n")
                f.write(f"  - {log_file.name}\n")
                f.write(f"\nStatus: SUCCESS ✓\n")
            
            print(f"\n📋 Summary: {summary_file.name}")
            print(f"✅ Successfully processed {input_file.name}")
            
        except Exception as e:
            all_success = False
            print(f"\n❌ ERROR processing {input_file.name}")
            print(f"Error message: {str(e)}")
            
            # Save error details
            error_file = output_dir / f"{base_name}_error_{timestamp}.txt"
            with open(error_file, 'w') as f:
                f.write(f"Error processing {input_file.name}\n")
                f.write(f"Timestamp: {datetime.now()}\n")
                f.write(f"Error: {str(e)}\n")
                f.write(f"\nFull traceback:\n")
                import traceback
                f.write(traceback.format_exc())
            
            print(f"Error details saved to: {error_file.name}")
            continue
    
    # Final summary
    print(f"\n{'='*60}")
    if all_success:
        print("✅ ALL FILES PROCESSED SUCCESSFULLY!")
    else:
        print("⚠️  Some files had errors. Check error logs.")
    print(f"{'='*60}")
    print(f"\n📁 All results saved to: {output_dir}/")
    print("\nYou can download results from:")
    print("  1. GitHub Actions Artifacts")
    print("  2. The 'output/' folder in your repository")

if __name__ == "__main__":
    main()
