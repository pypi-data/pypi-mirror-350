# This file is part of a Python translation of KiCad's C++ source code.

# Original C++ code:
# - © 2001 Gopal Narayanan <gopal@astro.umass.edu>
# - © 2002 Claudio Girardi <claudio.girardi@ieee.org>
# - © 2005, 2006 Stefan Jahn <stefan@lkcc.org>
# - Modified for KiCad: 2018 Jean-Pierre Charras <jp.charras at wanadoo.fr>
# - © The KiCad Developers, see AUTHORS.txt for contributors.

# Python translation and modifications:
# - © 2025 Dominik Mair <dominik.mair@uibk.ac.at>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from dataclasses import dataclass, field
from typing import Optional
import math


@dataclass
class MicrostripAnalysisResult:
    epsilon_eff: float
    skin_depth: float
    atten_cond: float
    atten_diel: float
    Z0_0: float
    angle_deg: float = None  # Optional: phase shift in degrees for the given length


@dataclass
class MicrostripSynthesisResult:
    width: float
    epsilon_eff: float
    skin_depth: float
    atten_cond: float
    atten_diel: float
    length: float  # Physical length to reach the target electrical angle (meters)


@dataclass
class Microstrip:
    """
    Microstrip transmission line model for PCB design.

    This class models and analyzes microstrip transmission lines, supporting both synthesis (finding trace width for a target impedance) and analysis (computing electrical properties from geometry and material parameters).

    Parameters
    ----------
    eps_r : float
        Relative permittivity (dielectric constant) of the substrate.
    tand : float
        Loss tangent of the substrate.
    h : float
        Height of the substrate (meters).
    t : float
        Thickness of the conductor (meters).
    rough : float
        Surface roughness of the conductor (meters).
    sigma : float
        Electrical conductivity of the conductor (S/m).
    mur : float
        Relative permeability of the substrate.
    murc : float
        Relative permeability of the conductor.
    frequency : float
        Frequency of operation (Hz).
    z0_target : float, optional
        Target characteristic impedance for synthesis (Ohms).
    ang_l_target : float, optional
        Target electrical length for synthesis (radians).
    h_top : float, optional
        Height to top ground plane (meters, very large for single ground plane).

    Usage
    -----
    Synthesis:
        Call `Synthesize()` to compute the required width for a target impedance. Returns a `MicrostripSynthesisResult` dataclass.
    Analysis:
        Set the desired width via the `width` property, then call `Analyze()` to compute all properties. Returns a `MicrostripAnalysisResult` dataclass.
    """

    # Physical constants
    _MU0: float = 12.566370614e-7  # Permeability of free space (H/m)
    _C0: float = 299792458.0  # Speed of light in vacuum (m/s)
    _ZF0: float = 376.730313668  # Impedance of free space (ohms)

    eps_r: float = 1.0
    tand: float = 0.0
    h: float = 1e-3
    t: float = 35e-6
    rough: float = 0.0
    sigma: float = 5.8e7
    mur: float = 1.0
    murc: float = 1.0
    frequency: float = 1e9
    z0_target: float = 50.0
    ang_l_target: float = None
    h_top: float = 1e20

    params: dict = field(init=False, default_factory=dict)

    def __post_init__(self):
        self.h_top = self.h_top if self.h_top is not None else self.h
        self.params = {
            "EPSILONR": self.eps_r,
            "TAND": self.tand,
            "H": self.h,
            "H_T": self.h_top,
            "T": self.t,
            "PHYS_WIDTH": 0.001,
            "Z0": self.z0_target if self.z0_target is not None else float("nan"),
            "ANG_L": self.ang_l_target if self.ang_l_target is not None else 0.0,
            "FREQUENCY": self.frequency,
            "SIGMA": self.sigma,
            "ROUGH": self.rough,
            "MUR": self.mur,
            "MURC": self.murc,
            "PHYS_LEN": 0.0,
        }

    @staticmethod
    def _filling_factor(u, eps_r):
        """Calculate the filling factor for the microstrip geometry."""
        u2 = u * u
        u3 = u2 * u
        u4 = u3 * u
        a = (
            1.0
            + math.log((u4 + u2 / 2704) / (u4 + 0.432)) / 49.0
            + math.log(1.0 + u3 / 5929.741) / 18.7
        )
        b = 0.564 * pow((eps_r - 0.9) / (eps_r + 3.0), 0.053)
        return pow(1.0 + 10.0 / u, -a * b)

    @staticmethod
    def _delta_q_cover(h2h):
        """Correction factor for cover height."""
        return math.tanh(1.043 + 0.121 * h2h - 1.164 / h2h)

    @staticmethod
    def _delta_q_thickness(u, t_h):
        """Correction factor for conductor thickness."""
        return (2.0 * math.log(2.0) / math.pi) * (t_h / math.sqrt(u))

    @staticmethod
    def _delta_u_thickness(u, t_h, eps_r):
        """Correction for effective width due to conductor thickness."""
        if t_h > 0.0:
            delta_u = (t_h / math.pi) * math.log(
                1.0 + (4.0 * math.e) * pow(math.tanh(math.sqrt(6.517 * u)), 2.0) / t_h
            )
            delta_u = 0.5 * delta_u * (1.0 + 1.0 / math.cosh(math.sqrt(eps_r - 1.0)))
        else:
            delta_u = 0.0
        return delta_u

    @staticmethod
    def _e_r_effective(eps_r, q):
        """Calculate effective permittivity."""
        return 0.5 * (eps_r + 1.0) + 0.5 * q * (eps_r - 1.0)

    @staticmethod
    def _Z0_homogeneous(u):
        """Characteristic impedance for homogeneous microstrip."""
        if u <= 0:
            return float("inf")
        freq_term = 6.0 + (2.0 * math.pi - 6.0) * math.exp(-pow(30.666 / u, 0.7528))
        return (Microstrip._ZF0 / (2.0 * math.pi)) * math.log(
            freq_term / u + math.sqrt(1.0 + 4.0 / (u * u))
        )

    @staticmethod
    def _e_r_dispersion(u, eps_r, f_n):
        """Dispersion correction for effective permittivity."""
        P_1 = (
            0.27488
            + u * (0.6315 + 0.525 / pow(1.0 + 0.0157 * f_n, 20.0))
            - 0.065683 * math.exp(-8.7513 * u)
        )
        P_2 = 0.33622 * (1.0 - math.exp(-0.03442 * eps_r))
        P_3 = 0.0363 * math.exp(-4.6 * u) * (1.0 - math.exp(-pow(f_n / 38.7, 4.97)))
        P_4 = 1.0 + 2.751 * (1.0 - math.exp(-pow(eps_r / 15.916, 8.0)))
        return P_1 * P_2 * pow((P_3 * P_4 + 0.1844) * f_n, 1.5763)

    @staticmethod
    def _Z0_dispersion(u, eps_r, eps_eff_0, eps_eff_f, f_n):
        """Dispersion correction for characteristic impedance."""
        R1 = 0.03891 * pow(eps_r, 1.4)
        R2 = 0.267 * pow(u, 7.0)
        R3 = 4.766 * math.exp(-3.228 * pow(u, 0.641))
        R4 = 0.016 + pow(0.0514 * eps_r, 4.524)
        R5 = pow(f_n / 28.843, 12.0)
        R6 = 22.2 * pow(u, 1.92)
        R7 = 1.206 - 0.3144 * math.exp(-R1) * (1.0 - math.exp(-R2))
        R8 = 1.0 + 1.275 * (
            1.0
            - math.exp(-0.004625 * R3 * pow(eps_r, 1.674) * pow(f_n / 18.365, 2.745))
        )
        tmpf = pow(eps_r - 1.0, 6.0)
        R9 = (
            5.086
            * R4
            * (R5 / (0.3838 + 0.386 * R4))
            * (math.exp(-R6) / (1.0 + 1.2992 * R5))
            * (tmpf / (1.0 + 10.0 * tmpf))
        )
        R10 = 0.00044 * pow(eps_r, 2.136) + 0.0184
        tmpf = pow(f_n / 19.47, 6.0)
        R11 = tmpf / (1.0 + 0.0962 * tmpf)
        R12 = 1.0 / (1.0 + 0.00245 * u * u)
        R13 = 0.9408 * pow(eps_eff_f, R8) - 0.9603
        R14 = (0.9408 - R9) * pow(eps_eff_0, R8) - 0.9603
        R15 = 0.707 * R10 * pow(f_n / 12.3, 1.097)
        R16 = 1.0 + 0.0503 * eps_r * eps_r * R11 * (1.0 - math.exp(-pow(u / 15.0, 6.0)))
        R17 = R7 * (
            1.0 - 1.1241 * (R12 / R16) * math.exp(-0.026 * pow(f_n, 1.15656) - R15)
        )
        return pow(R13 / R14, R17)

    def _SynthesizeWidth(self):
        """Estimate initial trace width for a target impedance."""
        e_r = self.eps_r
        Z0 = self.z0_target
        if Z0 == 0:
            return 0.0
        a = (Z0 / self._ZF0) / (2 * math.pi) * math.sqrt((e_r + 1) / 2.0) + (
            (e_r - 1) / (e_r + 1)
        ) * (0.23 + (0.11 / e_r))
        b = (self._ZF0 / 2) * math.pi / (Z0 * math.sqrt(e_r))
        if a > 1.52:
            w_h = 8.0 * math.exp(a) / (math.exp(2.0 * a) - 2.0)
        else:
            w_h = (2.0 / math.pi) * (
                b
                - 1.0
                - math.log(2.0 * b - 1.0)
                + ((e_r - 1) / (2.0 * e_r)) * (math.log(b - 1.0) + 0.39 - 0.61 / e_r)
            )
        return w_h * self.h if self.h > 0 else 0.0

    def _mur_eff_ms(self):
        """Calculate effective permeability for the microstrip."""
        mur = self.mur
        h = self.h
        w = self.params["PHYS_WIDTH"]
        self.mur_eff = (2.0 * mur) / (
            (1.0 + mur) + (1.0 - mur) * pow(1.0 + 10.0 * h / w, -0.5)
        )
        self.mur = mur
        return self.mur_eff

    def _microstrip_Z0(self):
        e_r = self.eps_r
        h = self.h
        h2h = (self.h_top / h) if h > 0 else 0.0
        w = self.params["PHYS_WIDTH"]
        u = w / h if h > 0 else 0.0
        t_h = self.t / h if h > 0 else 0.0

        delta_u_1 = self._delta_u_thickness(u, t_h, 1.0)
        self.Z0_h_1 = self._Z0_homogeneous(u + delta_u_1)
        delta_u_r = self._delta_u_thickness(u, t_h, e_r)
        u += delta_u_r
        Z0_h_r = self._Z0_homogeneous(u)

        q_inf = self._filling_factor(u, e_r)
        q_c = self._delta_q_cover(h2h)
        q_t = self._delta_q_thickness(u, t_h)
        q = (q_inf - q_t) * q_c

        e_r_eff_t = self._e_r_effective(e_r, q)
        e_r_eff = e_r_eff_t * pow(self.Z0_h_1 / Z0_h_r, 2.0)

        Z0_stat = Z0_h_r / math.sqrt(e_r_eff_t)
        self.z0_target = Z0_stat
        self.w_eff = u * h
        self.er_eff_0 = e_r_eff
        self.Z0_0 = Z0_stat
        self.epsilon_eff = e_r_eff_t
        return Z0_stat

    def _dispersion(self):
        e_r = self.eps_r
        e_r_eff_0 = self.er_eff_0
        u = self.params["PHYS_WIDTH"] / self.h
        f_n = self.frequency * self.h / 1e6  # GHz*mm
        P = self._e_r_dispersion(u, e_r, f_n)
        e_r_eff_f = e_r - (e_r - e_r_eff_0) / (1.0 + P)
        D = self._Z0_dispersion(u, e_r, e_r_eff_0, e_r_eff_f, f_n)
        Z0_f = self.Z0_0 * D

        self.prop_delay = math.sqrt(e_r_eff_f) * (1.0e10 / self._C0)
        self.epsilon_eff = e_r_eff_f
        self.z0_target = Z0_f

    def _attenuation(self):
        # Skin depth (m)
        if self.frequency > 0:
            depth = 1.0 / math.sqrt(
                math.pi * self.frequency * (self.murc * Microstrip._MU0) * self.sigma
            )
        else:
            depth = 0.0
        self.skin_depth = depth  # keep in meters

        # Conductor losses (dB/m) -- C++ style
        Z0_h_1 = self.Z0_h_1
        e_r_eff_0 = self.er_eff_0
        width = self.params["PHYS_WIDTH"]
        freq = self.frequency
        delta = depth  # skin depth
        Rs = 1.0 / (self.sigma * delta) if delta > 0 else float("inf")
        Rs *= 1.0 + (2.0 / math.pi) * math.atan(1.40 * pow(self.rough / delta, 2.0))
        K = math.exp(-1.2 * pow(Z0_h_1 / self._ZF0, 0.7))
        if freq > 0 and width > 0 and Z0_h_1 > 0:
            Q_c = (math.pi * Z0_h_1 * width * freq) / (Rs * self._C0 * K)
            alpha_c = (
                (20.0 * math.pi / math.log(10.0))
                * freq
                * math.sqrt(e_r_eff_0)
                / (self._C0 * Q_c)
            )
        else:
            alpha_c = 0.0
        self.atten_cond = alpha_c

        # Dielectric losses (dB/m)
        eps_eff_0 = self.er_eff_0
        e_r = self.eps_r
        if eps_eff_0 != 0 and (e_r - 1.0) != 0:
            alpha_d = (
                (20 * math.pi / math.log(10))
                * (self.frequency / Microstrip._C0)
                * (e_r / math.sqrt(eps_eff_0))
                * ((eps_eff_0 - 1.0) / (e_r - 1.0))
                * self.tand
            )
        else:
            alpha_d = 0.0
        self.atten_diel = alpha_d

    def _line_angle(self):
        if self.epsilon_eff is None or self.epsilon_eff <= 0 or self.mur_eff is None:
            return
        v = Microstrip._C0 / math.sqrt(self.epsilon_eff * self.mur_eff)
        lambda_g = v / self.frequency

    def _MinimiseZ0Error1D(self):
        z0_dest = self.z0_target
        angl_dest = self.params["ANG_L"]
        w = self.params["PHYS_WIDTH"]
        if not math.isfinite(z0_dest):
            self.params["PHYS_WIDTH"] = float("nan")
            return False
        if not math.isfinite(w) or w == 0.0:
            w = 0.001
        self.params["PHYS_WIDTH"] = w
        self.Analyze()
        Z0_current = self.z0_target
        error = abs(z0_dest - Z0_current)

        iter_count = 0
        m_maxError = 1e-6
        while error > m_maxError and iter_count < 250:
            iter_count += 1
            increment = w / 100.0
            w += increment
            self.params["PHYS_WIDTH"] = w
            self.Analyze()
            Z0_new = self.z0_target
            slope = (Z0_new - Z0_current) / increment if increment != 0 else 0
            slope = (z0_dest - Z0_current) / slope - increment
            w += slope

            self.params["PHYS_WIDTH"] = w
            self.Analyze()
            Z0_current = self.z0_target
            error = abs(z0_dest - Z0_current)
        self.z0_target = z0_dest
        self.params["ANG_L"] = angl_dest
        er_eff = self.epsilon_eff
        if er_eff and self.mur_eff:
            self.params["PHYS_LEN"] = (
                Microstrip._C0
                / (self.frequency * math.sqrt(er_eff * self.mur_eff))
                * angl_dest
                / (2.0 * math.pi)
            )
        self.Analyze()
        return error <= m_maxError

    @property
    def width(self) -> float:
        """Get or set the physical width (in meters) for analysis."""
        return self.params["PHYS_WIDTH"]

    @width.setter
    def width(self, value: float):
        self.params["PHYS_WIDTH"] = value

    def Analyze(self) -> MicrostripAnalysisResult:
        """
        Computes all output properties for the current geometry and material parameters.

        Note
        ----
        The width used for analysis must be set via the `width` property before calling this method. The returned result object echoes this width for clarity.

        Returns
        -------
        MicrostripAnalysisResult
            Dataclass containing all computed output properties (width is the input value).
        """
        self._mur_eff_ms()
        self._microstrip_Z0()
        self._dispersion()
        self._line_angle()
        self._attenuation()
        # Compute angle_deg if ANG_L is set
        angle_deg = None
        if hasattr(self, "params") and "ANG_L" in self.params and self.params["ANG_L"]:
            angle_deg = math.degrees(self.params["ANG_L"])
        return MicrostripAnalysisResult(
            epsilon_eff=self.epsilon_eff,
            skin_depth=self.skin_depth,
            atten_cond=self.atten_cond,
            atten_diel=self.atten_diel,
            Z0_0=self.Z0_0,
            angle_deg=angle_deg,
        )

    def Synthesize(self) -> MicrostripSynthesisResult:
        """
        Synthesizes the trace width for the target impedance and computes all output properties.

        Returns
        -------
        MicrostripSynthesisResult
            Dataclass containing all computed output properties after synthesis.
        """
        if self.z0_target is None:
            if self.params["PHYS_WIDTH"] > 0:
                return self.Analyze()
            raise ValueError("z0_target must be set for synthesis.")
        w_guess = self._SynthesizeWidth()
        self.params["PHYS_WIDTH"] = w_guess
        self.z0_target = self.z0_target
        self._MinimiseZ0Error1D()
        # Store final results
        L = self.params["PHYS_LEN"]
        # Do NOT divide attenuation by length! Attenuation is already per meter.
        return MicrostripSynthesisResult(
            width=self.params["PHYS_WIDTH"],
            epsilon_eff=self.epsilon_eff,
            skin_depth=self.skin_depth,
            atten_cond=self.atten_cond,
            atten_diel=self.atten_diel,
            length=L,
        )


def synthesize_microstrip(
    eps_r: float,
    tand: float,
    h: float,
    t: float,
    rough: float,
    sigma: float,
    mur: float,
    murc: float,
    frequency: float,
    z0_target: float,
    ang_l_target: float = None,
    h_top: float = 1e20,
) -> MicrostripSynthesisResult:
    """
    Synthesize the required microstrip width for a target impedance.

    Parameters
    ----------
    eps_r : float
        Relative permittivity (dielectric constant) of the substrate.
    tand : float
        Loss tangent of the substrate.
    h : float
        Height of the substrate (meters).
    t : float
        Thickness of the conductor (meters).
    rough : float
        Surface roughness of the conductor (meters).
    sigma : float
        Electrical conductivity of the conductor (S/m).
    mur : float
        Relative permeability of the substrate.
    murc : float
        Relative permeability of the conductor.
    frequency : float
        Frequency of operation (Hz).
    z0_target : float
        Target characteristic impedance for synthesis (Ohms).
    ang_l_target : float, optional
        Target electrical length for synthesis (degrees).
    h_top : float, optional
        Height to top ground plane (meters, very large for single ground plane).

    Returns
    -------
    MicrostripSynthesisResult
        Dataclass containing all computed output properties after synthesis.
    """
    # Convert angle from degrees to radians if provided
    if ang_l_target is not None:
        ang_l_target_rad = math.radians(ang_l_target)
    else:
        ang_l_target_rad = None
    ms = Microstrip(
        eps_r=eps_r,
        tand=tand,
        h=h,
        t=t,
        rough=rough,
        sigma=sigma,
        mur=mur,
        murc=murc,
        frequency=frequency,
        z0_target=z0_target,
        ang_l_target=ang_l_target_rad,
        h_top=h_top,
    )
    return ms.Synthesize()


def analyze_microstrip(
    width: float,
    eps_r: float,
    tand: float,
    h: float,
    t: float,
    rough: float,
    sigma: float,
    mur: float,
    murc: float,
    frequency: float,
    length: float = None,  # Physical length (meters), optional
    h_top: float = 1e20,
) -> MicrostripAnalysisResult:
    """
    Analyze a microstrip line for given geometry and material parameters.

    Parameters
    ----------
    width : float
        Trace width (meters).
    eps_r : float
        Relative permittivity (dielectric constant) of the substrate.
    tand : float
        Loss tangent of the substrate.
    h : float
        Height of the substrate (meters).
    t : float
        Thickness of the conductor (meters).
    rough : float
        Surface roughness of the conductor (meters).
    sigma : float
        Electrical conductivity of the conductor (S/m).
    mur : float
        Relative permeability of the substrate.
    murc : float
        Relative permeability of the conductor.
    frequency : float
        Frequency of operation (Hz).
    length : float, optional
        Physical length of the line (meters). If provided, the electrical angle is calculated and used.
    h_top : float, optional
        Height to top ground plane (meters, very large for single ground plane).

    Returns
    -------
    MicrostripAnalysisResult
        Dataclass containing all computed output properties for the given width, including:
        - epsilon_eff: Effective permittivity
        - skin_depth: Skin depth (meters)
        - atten_cond: Conductor attenuation (dB/m)
        - atten_diel: Dielectric attenuation (dB/m)
        - Z0_0: Characteristic impedance (ohms)
        - angle_deg: Phase shift in degrees for the given length (if length is specified, else None)
    """
    ang_l_target_rad = None
    if length is not None:
        # Calculate the electrical angle from the given length
        ms_tmp = Microstrip(
            eps_r=eps_r,
            tand=tand,
            h=h,
            t=t,
            rough=rough,
            sigma=sigma,
            mur=mur,
            murc=murc,
            frequency=frequency,
            h_top=h_top,
        )
        ms_tmp.width = width
        ms_tmp._mur_eff_ms()
        ms_tmp._microstrip_Z0()
        ms_tmp._dispersion()
        er_eff = ms_tmp.epsilon_eff
        mur_eff = ms_tmp.mur_eff
        if er_eff and mur_eff:
            lambda_g = ms_tmp._C0 / (frequency * (er_eff * mur_eff) ** 0.5)
            ang_l_target_rad = 2 * math.pi * length / lambda_g
    ms = Microstrip(
        eps_r=eps_r,
        tand=tand,
        h=h,
        t=t,
        rough=rough,
        sigma=sigma,
        mur=mur,
        murc=murc,
        frequency=frequency,
        ang_l_target=ang_l_target_rad,
        h_top=h_top,
    )
    ms.width = width
    return ms.Analyze()
