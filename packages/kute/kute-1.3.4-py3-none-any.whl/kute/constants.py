# Copyright (c) 2024 The KUTE contributors

# Constants (in S.I. units)
NA = 6.02214076e23 # Avogadro's number
KB = 1.380649e-23 # Boltzmann constant in J/K
EPSILON_0 = 8.8541878128e-12 # Vacuum permittivity in F/m
ELEMENTARY_CHARGE = 1.602176634e-19 # Elementary charge in Coulombs

# Transformations
KG_TO_AMU = 1 / 1.66053906660e-27 # Kilograms to atomic mass units
AMU_TO_KG = 1 / KG_TO_AMU
J_TO_KCAL = 1 / 4184 # Joules to kilocalories
KCAL_TO_J = 1 / J_TO_KCAL
J_TO_ERGS = 1e7 # Joules to ergs
ERGS_TO_J = 1 / J_TO_ERGS
J_TO_EV = 1 / 1.602176634e-19 # Joules to electron volts
EV_TO_J = 1 / J_TO_EV
METERS_TO_NANOMETERS = 1e9 # Meters to nanometers
NANOMETERS_TO_METERS = 1  / METERS_TO_NANOMETERS
METERS_TO_ANGSTROMS = 1e10 # Meters to angstroms
ANGSTROMS_TO_METERS = 1 / METERS_TO_ANGSTROMS
SEC_TO_PS = 1e12 # Seconds to picoseconds
PS_TO_SEC = 1 / SEC_TO_PS
SEC_TO_FS = 1e15 # Seconds to femtoseconds
FS_TO_SEC = 1 / SEC_TO_FS
PAS_TO_POISE = 1e1 # Pascal-seconds to 
POISE_TO_PAS = 1 / PAS_TO_POISE
NEWTONS_TO_DYNES = 1e5 # Newtons to dynes
DYNES_TO_NEWTONS = 1 / NEWTONS_TO_DYNES
PA_TO_PSI = 0.000145038 # Pascals to pounds per square inch
PSI_TO_PA = 1 / PA_TO_PSI

# Atomic masses (in atomic mass units)
ATOMIC_MASSES = {
    "H": 1.00784,
    "He": 4.0026,
    "Li": 6.9410,
    "Be": 9.0121831,
    "B": 10.811,
    "C": 12.011,
    "N": 14.007,
    "O": 15.999,
    "F": 18.998,
    "Ne": 20.180,
    "Na": 22.990,
    "Mg": 24.305,
    "Al": 26.982,
    "Si": 28.086,
    "P": 30.974,
    "S": 32.065,
    "Cl": 35.453,
    "Ar": 39.948,
    "K": 39.098,
    "Ca": 40.078,
    "Sc": 44.956,
    "Se": 78.960,
    "Ti": 47.867,
    "Br": 79.904,
    "Ag": 107.87,
    "Au": 196.967,
    "Hg": 200.59,
    "Rn": 222.0,
}