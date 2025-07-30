from ..windsim.presets import wind_power_plant_preset


def wind_presets(
    pn_max_kw,
    wind_profile: str = "hellmann",
    temperature_profile: str = "linear_gradient",
    air_density_profile: str = "barometric",
    power_method: str = "power_curve",
    rng=None,
    turbine_type=None,
    force_type=False,
    cos_phi=0.9,
    q_control="prioritize_p",
    inverter_mode="inductive",
    **kwargs,
):
    # print(pn_max_kw, cos_phi, q_control, inverter_mode, kwargs)
    wparams, winit = wind_power_plant_preset(
        pn_max_kw,
        wind_profile,
        temperature_profile,
        air_density_profile,
        power_method,
        rng,
        turbine_type,
        force_type,
        **kwargs,
    )

    params = {
        "wind": wparams,
        "inverter": {
            "sn_kva": pn_max_kw / cos_phi,
            "q_control": q_control,
            "cos_phi": cos_phi,
            "inverter_mode": inverter_mode,
        },
        "sign_convention": "active",
    }

    inits = {"wind": winit, "inverter": None}

    return params, inits
