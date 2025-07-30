from hfsynpy import synthesize_microstrip, analyze_microstrip

# Synthesize width for target Z0 using the functional API
syn_result = synthesize_microstrip(
    eps_r=3.66,  # Relative permittivity (3.66)
    tand=0.0037,  # Loss tangent (0.0037)
    h=1.524e-3,  # Substrate height (1.524 mm)
    t=35e-6,  # Copper thickness (35 um)
    rough=0e-6,  # Surface roughness (0 um)
    sigma=1 / (1.72e-8),  # Copper conductivity (5.814e7 S/m)
    mur=1.0,  # Relative permeability (substrate, 1.0)
    murc=1.0,  # Relative permeability (conductor, 1.0)
    frequency=2.45e9,  # Frequency (2.45 GHz)
    z0_target=50.0,  # Target impedance (50 ohms)
    ang_l_target=30.0,  # Target angle for length synthesis (degrees)
)
print("Synthesis result:")
print(f"Synthesized width: {syn_result.width * 1e3:.4f} mm")
print(f"Effective permittivity: {syn_result.epsilon_eff:.4f}")
print(f"Skin depth: {syn_result.skin_depth * 1e6:.4f} um")
print(f"Conductor attenuation: {syn_result.atten_cond:.4f} dB/m")
print(f"Dielectric attenuation: {syn_result.atten_diel:.4f} dB/m")
print(f"Physical length: {syn_result.length * 1e3:.4f} mm")

# Analyze for a specific width using the functional API
ana_result = analyze_microstrip(
    width=0.79e-3,  # 0.79 mm
    eps_r=3.66,
    tand=0.0037,
    h=1.524e-3,
    t=35e-6,
    rough=0e-6,
    sigma=1 / (1.72e-8),
    mur=1.0,
    murc=1.0,
    frequency=2.45e9,
    length=50e-3,  # 50 mm
)
print("\nAnalysis result:")
print(f"Characteristic impedance: {ana_result.Z0_0:.4f} ohms")
print(f"Effective permittivity: {ana_result.epsilon_eff:.4f}")
print(f"Skin depth: {ana_result.skin_depth * 1e6:.4f} um")
print(f"Conductor attenuation: {ana_result.atten_cond:.4f} dB/m")
print(f"Dielectric attenuation: {ana_result.atten_diel:.4f} dB/m")
print(f"Angle shift: {ana_result.angle_deg:.4f} degrees")
