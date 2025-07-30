<!-- filepath: c:\Users\Dominik\Documents\GitHub\hfsynpy\README.md -->
# hfsynpy

A modern Python package for high-frequency (HF) microstrip synthesis and analysis, inspired by the models used in KiCad. This library provides accurate, user-friendly tools for PCB and RF design, supporting both synthesis (width/length for target impedance and angle) and analysis (impedance, losses, phase shift for given geometry).

See the [full documentation](https://generativeantennadesign.github.io/hfsynpy/) for all parameters, advanced usage, and API details.

---

## Features
- **Synthesize** microstrip width for a target impedance and electrical angle (input in degrees)
- **Analyze** microstrip properties for a given width and physical length (input in meters)
- Returns all results as well-documented dataclasses
- Outputs attenuation per meter (dB/m), effective permittivity, skin depth, and more
- Computes and returns phase shift (angle in degrees) for a given length
- No external dependencies required
- Well-documented, pip-installable, and tested

---

## Installation

```bash
pip install hfsynpy
```

---

## Quick Start

### Synthesize Microstrip for Target Impedance and Angle

```python
from hfsynpy import synthesize_microstrip

result = synthesize_microstrip(
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
print(f"Synthesized width: {result.width * 1e3:.4f} mm")
print(f"Physical length: {result.length * 1e3:.4f} mm")
```

### Analyze Microstrip for Given Width and Length

```python
from hfsynpy import analyze_microstrip

result = analyze_microstrip(
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
print(f"Characteristic impedance: {result.Z0_0:.4f} ohms")
print(f"Angle shift: {result.angle_deg:.4f} degrees")
```

---

## API Overview

### synthesize_microstrip(...)
- Synthesize width for target impedance and angle (degrees)
- Returns: `MicrostripSynthesisResult` dataclass

### analyze_microstrip(...)
- Analyze for given width and length (meters)
- Returns: `MicrostripAnalysisResult` dataclass (includes `angle_deg` if length is given)

---

## License

This project is licensed under the GNU General Public License v2 or later (GPL-2.0-or-later). See the LICENSE file for details.

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

---

For bug reports, feature requests, or contributions, please use the [GitHub repository](https://github.com/GenerativeAntennaDesign/hfsynpy).