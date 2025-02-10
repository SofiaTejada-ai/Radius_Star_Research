import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

def process_file(file_path, window_size=5):
    # Load data, skipping the first row (header)
    data = np.loadtxt(file_path, skiprows=1)

    # Assuming the relevant columns are 0 (baryon density), 1 (pressure), and 2 (energy density) after header
    baryon_density = data[:, 0]
    pressure = data[:, 1]  # Convert Pressure (dyne/cm^2) to MeV/fm^3
    energy_density = data[:, 2]  # Convert Energy density (g/cm^3) to MeV/fm^3

    # Smooth the data using a moving average
    pressure = np.convolve(pressure, np.ones(window_size)/window_size, mode='valid')
    energy_density = np.convolve(energy_density, np.ones(window_size)/window_size, mode='valid')
    baryon_density = np.convolve(baryon_density, np.ones(window_size)/window_size, mode='valid')

    return energy_density, pressure, baryon_density

# Define file paths
file_paths = [
    r"C:\Users\emibe\OneDrive\Desktop\data\eos_npem_bps_bbg.eos",
    r"C:\Users\emibe\OneDrive\Desktop\data\eos_npem_bps_dbhf.eos"
]

# Process each file and store results
all_energy_density = []
all_pressure = []
all_baryon_density = []

for file_path in file_paths:
    ed, p, bd = process_file(file_path)
    all_energy_density.append(ed)
    all_pressure.append(p)
    all_baryon_density.append(bd)

# Plotting the smoothed Pressure vs. Energy Density graph
plt.figure(figsize=(8, 6))
for i, file_path in enumerate(file_paths):
    plt.plot(all_energy_density[i], all_pressure[i], label=f'File {i+1}')
plt.xlabel('Energy Density (MeV/fm^3)')
plt.ylabel('Pressure (MeV/fm^3)')
plt.title('Pressure vs. Energy Density')
plt.legend()
plt.grid(True)
plt.show()

# Plotting the smoothed Baryon Density vs. Energy Density graph
plt.figure(figsize=(8, 6))
for i, file_path in enumerate(file_paths):
    plt.plot(all_energy_density[i], all_baryon_density[i], label=f'File {i+1}')
plt.xlabel('Energy Density (MeV/fm^3)')
plt.ylabel('Baryon Density (1/fm^3)')
plt.title('Baryon Density vs. Energy Density')
plt.legend()
plt.grid(True)
plt.show()

# Plotting the smoothed Baryon Density vs. Pressure graph
plt.figure(figsize=(8, 6))
for i, file_path in enumerate(file_paths):
    plt.plot(all_pressure[i], all_baryon_density[i], label=f'File {i+1}')
plt.xlabel('Pressure (MeV/fm^3)')
plt.ylabel('Baryon Density (1/fm^3)')
plt.title('Baryon Density vs. Pressure')
plt.legend()
plt.grid(True)
plt.show()
