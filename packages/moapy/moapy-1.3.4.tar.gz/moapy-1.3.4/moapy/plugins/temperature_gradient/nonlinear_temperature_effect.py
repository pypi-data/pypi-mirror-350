from moapy.auto_convert import auto_schema
from moapy.plugins.temperature_gradient.eurocode.data_input import (
    NonlinearTemperatureInput,
)

from moapy.plugins.temperature_gradient.eurocode.data_post import (
    ResultNonlinearTemperatureEffect,
)

from moapy.plugins.temperature_gradient.eurocode.calc_nonlinear_temperature_effect import (
    calc_nonlinear_temperature_effect,
)


@auto_schema(
    title="Eurocode 0 Calculate Temperature Gradient",
    description="Calculate Temperature Gradient from Section",
)
def calc_eurocode(
    nonlinear_temperature_input: NonlinearTemperatureInput,
) -> ResultNonlinearTemperatureEffect:
    return calc_nonlinear_temperature_effect(nonlinear_temperature_input)
