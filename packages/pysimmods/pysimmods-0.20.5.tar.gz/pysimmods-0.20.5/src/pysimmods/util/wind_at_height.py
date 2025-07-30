import numpy as np


def logarithmic_profile(
    wind_speed,
    wind_speed_height,
    hub_height,
    roughness_length=0.15,
    obstacle_height=0.0,
):
    return (
        wind_speed
        * np.log((hub_height - 0.7 * obstacle_height) / roughness_length)
        / np.log(
            (wind_speed_height - 0.7 * obstacle_height) / roughness_length
        )
    )


# Calculate the wind speed at altitude h using hellmann formula
def hellman(wind_speed, wind_speed_height, hub_height, hellman_exponent=1 / 7):
    return wind_speed * (hub_height / wind_speed_height) ** hellman_exponent
