"""Measure the scale effect of terrain slope using a Hurst-style exponent.

The exponent is estimated by fitting:
    log(RMS slope) = H * log(scale) + intercept

Scale is measured in metres. RMS slope values must use consistent units.
"""

import math


def measure_hurst(slope_by_scale: dict[float, float]) -> float:
    """
    Estimate a Hurst-style exponent from RMS slope measurements.

    Args:
        slope_by_scale: Mapping of scale in metres to RMS slope.

    Returns:
        Log-log regression slope (Hurst-style exponent).

    Raises:
        ValueError: If fewer than two valid measurements exist or
                    any scale/slope value is invalid.
    """
    if not isinstance(slope_by_scale, dict) or len(slope_by_scale) < 2:
        raise ValueError("At least two scale measurements are required.")

    points = []

    for scale, rms_slope in slope_by_scale.items():
        scale = float(scale)
        rms_slope = float(rms_slope)

        if not math.isfinite(scale) or scale <= 0:
            raise ValueError("Scale values must be positive and finite.")

        if not math.isfinite(rms_slope) or rms_slope <= 0:
            raise ValueError("RMS slope values must be positive and finite.")

        points.append((math.log(scale), math.log(rms_slope)))

    points.sort()

    x_values = [point[0] for point in points]
    y_values = [point[1] for point in points]

    x_mean = sum(x_values) / len(x_values)
    y_mean = sum(y_values) / len(y_values)

    denominator = sum((x - x_mean) ** 2 for x in x_values)

    if denominator == 0:
        raise ValueError("At least two distinct scales are required.")

    numerator = sum(
        (x - x_mean) * (y - y_mean)
        for x, y in zip(x_values, y_values)
    )

    return numerator / denominator