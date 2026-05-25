import pandas as pd
import numpy as np

def generate_sample_fatigue_data(filepath="sample_data.xlsx"):
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Target material Wöhler parameters (nominal)
    # k_1 = 5.0, ND = 2e6, SD = 200.0 MPa, scatter sigma in log10(cycles) = 0.2
    k_1 = 5.0
    ND = 2e6
    SD = 200.0
    sigma = 0.18
    
    # Load levels (MPa) and number of specimens per level
    load_levels = [350.0, 300.0, 250.0, 210.0, 180.0]
    specimens_per_level = 5
    
    data = []
    
    for load in load_levels:
        for _ in range(specimens_per_level):
            # Calculate nominal life using Basquin's relation
            # N = ND * (load / SD) ** (-k_1)
            nominal_cycles = ND * (load / SD) ** (-k_1)
            
            # Add log-normal scatter
            log_n = np.log10(nominal_cycles) + np.random.normal(0, sigma)
            cycles = 10**log_n
            
            # Define runout limit (e.g. 2,000,000 cycles)
            runout_limit = 2e6
            
            if cycles >= runout_limit or load <= 180.0:
                # Survived past runout limit or is at low load level
                # For runouts, cycles is set to the runout limit, and runout flag is 1
                data.append({
                    "Load (MPa)": load,
                    "Cycles to Failure": runout_limit,
                    "Is Runout": 1
                })
            else:
                # Failed before runout limit
                data.append({
                    "Load (MPa)": load,
                    "Cycles to Failure": int(round(cycles)),
                    "Is Runout": 0
                })
                
    df = pd.DataFrame(data)
    df.to_excel(filepath, index=False)
    print(f"Generated realistic fatigue test dataset at: {filepath}")

if __name__ == "__main__":
    generate_sample_fatigue_data()
