import json
import pytest
import moapy.plugins.baseplate_KDS41_30_2022.baseplate_KDS41_30_2022_calc

def test_baseplate_KDS41_30_2022_calc():
    input = {
                'B' : 240, 'H' : 240, 'Fc' :24 , 'Fy' : 400,
                'Ec': 25811.006260943130 , 'Es' : 210000,
                'bolt' : [
                    { 'X' : 90, 'Y' : 0, 'Area' : 314.15926535897933 },
                    { 'X' : -90, 'Y' : 0, 'Area' : 314.15926535897933 } ],
                'P' : -3349.9999999999964, 'Mx' : 0, 'My' : 51009999.999999985
    }

    JsonData = json.dumps(input)
    result = moapy.plugins.baseplate_KDS41_30_2022.baseplate_KDS41_30_2022_calc.calc_ground_pressure(JsonData)

    assert pytest.approx(result['bolt'][0]['Load']) == 0.0
    assert pytest.approx(result['bolt'][1]['Load']) == -269182.84245616524
