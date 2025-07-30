def linear_gradient(
    temperature, temperature_height, hub_height, gradient=0.0065
):
    return temperature - gradient * (hub_height - temperature_height)
