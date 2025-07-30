import pandas as pd
import numpy as np
import os
from typing import Tuple

def get_water_property(temp: float, file_path: str) -> Tuple[float, float]:
    """
    Get the density (kg/m³) and vapour pressure (bar) of water at a given temperature.
    Uses interpolation/extrapolation for values not directly in the dataset.

    Args:
        temp (float): Temperature in degrees Celsius (0–374.15).
        file_path (str): Path to the CSV or Excel file.

    Returns:
        Tuple[float, float]: (density in kg/m³, vapour pressure in bar)

    Raises:
        ValueError: If temperature is outside 0–374.15°C.
        FileNotFoundError: If the file does not exist.
        KeyError: If required columns are missing.
    """
    if not (0 <= temp <= 374.15):
        raise ValueError("Temperature must be between 0 and 374.15 °C (liquid water only).")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.csv':
        df = pd.read_csv(file_path)
    elif ext in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Use .csv or .xlsx")

    required_cols = ['t (°C)', 'pp (bar)', 'ρ (kg/dm³)']
    for col in required_cols:
        if col not in df.columns:
            raise KeyError(f"Missing required column: '{col}'")

    df = df[['t (°C)', 'ρ (kg/dm³)', 'pp (bar)']].dropna()
    df['density'] = df['ρ (kg/dm³)'] * 1000  # kg/m³
    df['vapour_pressure'] = df['pp (bar)']   # bar (no conversion)

    temps = df['t (°C)'].values
    densities = df['density'].values
    vapour_pressures = df['vapour_pressure'].values

    # Interpolate or extrapolate
    density = float(np.interp(temp, temps, densities))
    vapour_pressure = float(np.interp(temp, temps, vapour_pressures))

    return round(density, 4), round(vapour_pressure, 4)
