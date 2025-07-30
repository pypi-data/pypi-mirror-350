# hfsynpy

A Python package for high-frequency (HF) microstrip synthesis and analysis.

This package provides tools for the synthesis and analysis of microstrip transmission lines, using the same models as KiCad. Results are generally valid up to 40 GHz, but always verify with full-wave simulation tools for critical designs.

---

## Functional API Overview

This package provides two main functions for microstrip design:

- **synthesize_microstrip**: Synthesize the required trace width for a target impedance.
- **analyze_microstrip**: Analyze the electrical properties for a given trace width.

Both functions return results as dataclasses for clarity and type safety.

---

## Microstrip Synthesis and Analysis Example

This example demonstrates how to use the functional API of `hfsynpy` for microstrip synthesis and analysis, including the new features:
- Input of electrical angle in degrees for synthesis
- Input of physical length for analysis
- Output of phase shift (angle) in degrees for a given length
- All attenuation values are always per meter (dB/m)

### Synthesize Microstrip for Target Impedance and Angle

```python
from hfsynpy import synthesize_microstrip, analyze_microstrip

# Synthesize width for target Z0 and electrical angle (degrees)
syn_result = synthesize_microstrip(
    eps_r=3.66,        # Relative permittivity
    tand=0.0037,       # Loss tangent
    h=1.524e-3,        # Substrate height (1.524 mm)
    t=35e-6,           # Copper thickness (35 um)
    rough=0e-6,        # Surface roughness (0 um)
    sigma=1 / (1.72e-8), # Copper conductivity (5.814e7 S/m)
    mur=1.0,           # Relative permeability (substrate)
    murc=1.0,          # Relative permeability (conductor)
    frequency=2.45e9,  # Frequency (2.45 GHz)
    z0_target=50.0,    # Target impedance (ohms)
    ang_l_target=30.0, # Target angle for length synthesis (degrees)
)
print(f"Synthesized width: {syn_result.width * 1e3:.4f} mm")
print(f"Effective permittivity: {syn_result.epsilon_eff:.4f}")
print(f"Skin depth: {syn_result.skin_depth * 1e6:.4f} um")
print(f"Conductor attenuation: {syn_result.atten_cond:.4f} dB/m")
print(f"Dielectric attenuation: {syn_result.atten_diel:.4f} dB/m")
print(f"Physical length: {syn_result.length * 1e3:.4f} mm")
```

### Analyze Microstrip for Given Width and Length

```python
ana_result = analyze_microstrip(
    width=0.79e-3,     # Trace width (0.79 mm)
    eps_r=3.66,
    tand=0.0037,
    h=1.524e-3,
    t=35e-6,
    rough=0e-6,
    sigma=1 / (1.72e-8),
    mur=1.0,
    murc=1.0,
    frequency=2.45e9,
    length=50e-3,      # Physical length (50 mm)
)
print(f"Characteristic impedance: {ana_result.Z0_0:.4f} ohms")
print(f"Effective permittivity: {ana_result.epsilon_eff:.4f}")
print(f"Skin depth: {ana_result.skin_depth * 1e6:.4f} um")
print(f"Conductor attenuation: {ana_result.atten_cond:.4f} dB/m")
print(f"Dielectric attenuation: {ana_result.atten_diel:.4f} dB/m")
print(f"Angle shift: {ana_result.angle_deg:.4f} degrees")
```

---

## synthesize_microstrip

Synthesize the required microstrip width for a target impedance.

### Parameters
| Name         | Type   | Default     | Unit      | Description                                                                 |
|--------------|--------|-------------|-----------|-----------------------------------------------------------------------------|
| eps_r        | float  | required    | -         | Relative permittivity (dielectric constant) of the substrate.               |
| tand         | float  | required    | -         | Loss tangent of the substrate.                                              |
| h            | float  | required    | m         | Height of the substrate.                                                    |
| t            | float  | required    | m         | Thickness of the conductor.                                                 |
| rough        | float  | required    | m         | Surface roughness of the conductor.                                         |
| sigma        | float  | required    | S/m       | Electrical conductivity of the conductor.                                   |
| mur          | float  | required    | -         | Relative permeability of the substrate.                                     |
| murc         | float  | required    | -         | Relative permeability of the conductor.                                     |
| frequency    | float  | required    | Hz        | Frequency of operation.                                                     |
| z0_target    | float  | required    | Ω         | Target characteristic impedance for synthesis.                              |
| ang_l_target | float  | None        | rad       | Target electrical length for synthesis.                                     |
| h_top        | float  | 1e20        | m         | Height to top ground plane (very large for single ground plane).            |

### Returns
A `MicrostripSynthesisResult` dataclass:

| Name         | Type   | Unit      | Description                                 |
|--------------|--------|-----------|---------------------------------------------|
| width        | float  | m         | Synthesized trace width.                    |
| epsilon_eff  | float  | -         | Effective relative permittivity.            |
| skin_depth   | float  | m         | Skin depth of the conductor.                |
| atten_cond   | float  | dB/m      | Conductor attenuation per meter.            |
| atten_diel   | float  | dB/m      | Dielectric attenuation per meter.           |
| length       | float  | m         | Physical length to reach the target angle.  |

---

## analyze_microstrip

Analyze a microstrip line for given geometry and material parameters.

### Parameters
| Name         | Type   | Default     | Unit      | Description                                                                 |
|--------------|--------|-------------|-----------|-----------------------------------------------------------------------------|
| width        | float  | required    | m         | Trace width.                                                                |
| eps_r        | float  | required    | -         | Relative permittivity (dielectric constant) of the substrate.               |
| tand         | float  | required    | -         | Loss tangent of the substrate.                                              |
| h            | float  | required    | m         | Height of the substrate.                                                    |
| t            | float  | required    | m         | Thickness of the conductor.                                                 |
| rough        | float  | required    | m         | Surface roughness of the conductor.                                         |
| sigma        | float  | required    | S/m       | Electrical conductivity of the conductor.                                   |
| mur          | float  | required    | -         | Relative permeability of the substrate.                                     |
| murc         | float  | required    | -         | Relative permeability of the conductor.                                     |
| frequency    | float  | required    | Hz        | Frequency of operation.                                                     |
| ang_l_target | float  | None        | rad       | Target electrical length for analysis.                                      |
| h_top        | float  | 1e20        | m         | Height to top ground plane (very large for single ground plane).            |

### Returns
A `MicrostripAnalysisResult` dataclass:

| Name         | Type   | Unit      | Description                                 |
|--------------|--------|-----------|---------------------------------------------|
| epsilon_eff  | float  | -         | Effective relative permittivity.            |
| skin_depth   | float  | m         | Skin depth of the conductor.                |
| atten_cond   | float  | dB/m      | Conductor attenuation per meter.            |
| atten_diel   | float  | dB/m      | Dielectric attenuation per meter.           |
| Z0_0         | float  | Ω         | Characteristic impedance.                   |
| angle_deg    | float  | deg       | Phase shift for the given length.           |

---

## Attribution

This package is part of a Python translation of KiCad's C++ source code.

Original C++ code:
- © 2001 Gopal Narayanan <gopal@astro.umass.edu>
- © 2002 Claudio Girardi <claudio.girardi@ieee.org>
- © 2005, 2006 Stefan Jahn <stefan@lkcc.org>
- Modified for KiCad: 2018 Jean-Pierre Charras <jp.charras at wanadoo.fr>
- © The KiCad Developers, see AUTHORS.txt for contributors.

Python translation and modifications:
- © 2025 Dominik Mair <dominik.mair@uibk.ac.at>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.