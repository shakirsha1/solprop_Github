#!/usr/bin/env python
"""
SolProp ML Prediction Script
Processes input CSV files and generates prediction results
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def main():
    # Set up paths
    input_dir = Path('input')
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    # Find all CSV files in input directory
    input_files = list(input_dir.glob('*.csv'))
    
    if not input_files:
        print("No input CSV files found in 'input/' directory")
        sys.exit(1)
    
    print(f"Found {len(input_files)} input file(s)")
    
    # Import SolProp_ML
    try:
        from solvation_predictor import calculate_solubility, predict_property
    except ImportError:
        print("Error: SolProp_ML not properly installed")
        sys.exit(1)
    
    # Process each input file
    for input_file in input_files:
        print(f"\nProcessing: {input_file.name}")
        
        # Generate output filenames with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = input_file.stem
        
        results_file = output_dir / f"{base_name}_results_{timestamp}.csv"
        detailed_file = output_dir / f"{base_name}_detailed_{timestamp}.csv"
        log_file = output_dir / f"{base_name}_log_{timestamp}.log"
        
        try:
            # Run solubility calculations
            print("  Running solubility calculations...")
            results = calculate_solubility(
                path=str(input_file),
                validate_smiles=True,
                export_csv=str(results_file),
                export_detailed_csv=str(detailed_file),
                logger=str(log_file)
            )
            
            print(f"  ✓ Results saved to: {results_file.name}")
            print(f"  ✓ Detailed results saved to: {detailed_file.name}")
            print(f"  ✓ Log saved to: {log_file.name}")
            
            # Also run property predictions
            properties_file = output_dir / f"{base_name}_properties_{timestamp}.csv"
            print("  Running property predictions...")
            
            predictions = predict_property(
                path=str(input_file),
                gsolv=True,
                hsolv=True,
                saq=True,
                solute_parameters=True,
                validate_smiles=True,
                export_csv=str(properties_file)
            )
            
            print(f"  ✓ Properties saved to: {properties_file.name}")
            
        except Exception as e:
            print(f"  ✗ Error processing {input_file.name}: {str(e)}")
            with open(output_dir / f"{base_name}_error_{timestamp}.txt", 'w') as f:
                f.write(f"Error processing {input_file.name}\n")
                f.write(f"Error: {str(e)}\n")
            continue
    
    print("\n✓ All files processed successfully!")
    print(f"Results available in '{output_dir}/' directory")

if __name__ == "__main__":
    main()
