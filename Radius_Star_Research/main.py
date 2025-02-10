import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import os
import compactobjects as cobj
from compactobjects import conversion_dict
from scipy.constants import speed_of_light, gravitational_constant, pi, hbar, m_n
import astropy.constants as const
from input_validator import InputValidatorApp
from file_validator import FileValidatorApp

# Useful constants
solar_mass = const.M_sun.value  # kg

C_SI = speed_of_light  # m s^-1
C_CGS = C_SI * 100  # cm s^-1
G_SI = gravitational_constant  # m^3 kg^-1 s^-2
G_CGS = G_SI * 1000  # cm^3 g^-1 s^-2
MSUN_SI = solar_mass  # kg
MSUN_CGS = solar_mass * 1000  # g
HBAR_SI = hbar  # J s
HBAR_CGS = HBAR_SI * 1e7  # ergs s

# Create the folder where to save the results
script_dir = os.path.dirname(__file__)
results_dir = os.path.join(script_dir, 'NSOutput/')
if not os.path.isdir(results_dir):
    os.makedirs(results_dir)

def run_main_process(inputs):
    gamma = inputs['gamma']
    radius = inputs['radius']

    # Set default value for k if conversion_dict keys are missing or invalid
    try:
        k = inputs['k'] * (conversion_dict['cgs']['length']['m'] ** 2) * (
                    conversion_dict['cgs']['energy']['geom'] ** (-2 / 3))
    except KeyError:
        k = inputs['k']  # Use the provided value of 'k' directly

    try:
        e0 = inputs['p0'] * conversion_dict['cgs']['pressure']['geom']
    except KeyError:
        e0 = inputs['p0']  # Use the provided value of 'p0' directly if conversion fails

    p0 = e0 * (1e-5)

    eos = cobj.PressureEdenPolytropic(k, gamma)
    ns = cobj.CompactStar(eos)

    # Use the validated radius input and dr_Max
    radius_range = np.arange(1e-6, 1e5, 0.1)
    ns.set_radii_range(radius_range)

    r_newton, m_newton, p_newton = ns.structure_solver('Newton', p0)
    R_newton = r_newton[-1]
    M_newton = m_newton[-1]

    r_tov, m_tov, p_tov = ns.structure_solver('TOV', p0)
    R_tov = r_tov[-1]
    M_tov = m_tov[-1]

    # Print the extracted values
    print("\nInput information:")
    print(f"Gamma: {gamma}")
    print(f"Radius: {radius}")
    print(f"K (converted): {k}")
    print(f"Pressure (p0): {p0}")
    print(f"Newtonian Radius: {R_newton}")
    print(f"Newtonian Mass: {M_newton}")
    print(f"TOV Radius: {R_tov}")
    print(f"TOV Mass: {M_tov}")

    try:
        p0_1 = 3.5e32 * conversion_dict['cgs']['pressure']['geom']
        p0_2 = 3.5e38 * conversion_dict['cgs']['pressure']['geom']
    except KeyError:
        p0_1 = 3.5e32
        p0_2 = 3.5e38

    p_range = np.linspace(p0_1, p0_2, 200)

    R_star_tov, M_star_tov = ns.mass_vs_radius('TOV', p_range)
    R_star_newton, M_star_newton = ns.mass_vs_radius('Newton', p_range)

    # Plotting
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))
    plt.rc('font', family='monospace')

    # Plot P(r)
    axes[0].plot(r_newton, p_newton, color="blue", linestyle="-", linewidth=1, label='P Newton')
    axes[0].plot(r_tov, p_tov, color="black", linestyle="-", linewidth=2, label='P TOV')
    axes[0].set_xlabel('r [km]', fontsize=16.5)
    axes[0].set_ylabel(r'P [$dyne/cm^2$]', fontsize=16.5)
    axes[0].minorticks_on()
    axes[0].set_title("P(r) of a pure neutron star", fontsize=16.5)

    # Plot m(r)
    axes[1].plot(r_newton, m_newton, color="blue", linestyle=":", label='m Newton')
    axes[1].plot(r_tov, m_tov, color="black", linestyle="-.", label='m TOV')
    axes[1].plot(R_newton, M_newton, marker='o', linestyle="", color='green', label='NS Newton mass')
    axes[1].plot(R_tov, M_tov, marker='o', linestyle="", color='red', label='NS TOV mass')
    axes[1].set_ylabel(r"m [$M_{\odot}$]", fontsize=16.5)
    axes[1].minorticks_on()
    axes[1].set_title("m(r) of a pure neutron star", fontsize=16.5)

    # Plot Mass-Radius
    axes[2].plot(R_star_newton, M_star_newton, color="blue", linestyle=":", linewidth=1, label='Newton')
    axes[2].plot(R_star_tov, M_star_tov, color="black", linestyle=":", linewidth=2, label='TOV')
    axes[2].set_xlabel('R [km]', fontsize=16.5)
    axes[2].set_ylabel(r"M [$M_{\odot}$]", fontsize=16.5)
    axes[2].minorticks_on()
    axes[2].set_title("Mass-Radius of a pure neutron star", fontsize=16.5)

    fig.tight_layout()

    # Save or display the plot
    plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = InputValidatorApp(root, process_callback=run_main_process)
    root.mainloop()
