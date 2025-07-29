from moapy.auto_convert import auto_schema, MBaseModel
import moapy.plugins.earthpressure_coefficient.ka_beta0 as ka_beta0
import moapy.plugins.earthpressure_coefficient.ka as ka
import moapy.plugins.earthpressure_coefficient.kp_beta0 as kp_beta0
import moapy.plugins.earthpressure_coefficient.kp as kp
from moapy.plugins.earthpressure_coefficient.base import EarthPressureInput, EarthPressureResult

@auto_schema(
    title="Earth Pressure Coefficient Estimator",
    description="Calculates the earth pressure coefficient based on the provided input parameters, which include soil properties, wall geometry, and other relevant factors. The result is an estimated coefficient that represents the ratio of lateral earth pressure to vertical stress, commonly used in geotechnical engineering to analyze the stability and design of retaining walls, foundations, and other structures subjected to soil pressure."
)
def calc_earthpressure_coefficient(inp: EarthPressureInput) -> EarthPressureResult:
    # ka 계산
    if inp.beta == 0:
        ka_base, ka_calced, ka_value = ka_beta0.calc(inp)
    else:
        ka_base, ka_calced, ka_value = ka.calc(inp)

    if inp.beta == 0:
        kp_base, kp_calced, kp_value = kp_beta0.calc(inp)
    else:
        kp_base, kp_calced, kp_value = kp.calc(inp)

    return EarthPressureResult(ka_base=ka_base, ka_calculated_curve=ka_calced, calculated_ka=ka_value,
                               kp_base=kp_base, kp_calculated_curve=kp_calced, calculated_kp=kp_value)


if __name__ == "__main__":
    data = {"inp": {
        "beta": 0,
        "phi": 40,
        "delta": 0
    }}
    res = calc_earthpressure_coefficient(**data)
    print(res.dict())