import numpy as np
import pandas as pd
from moapy.plugins.earthpressure_coefficient.base import CubicSpline, linear_interpolation, get_interpolated_value, EarthPressureInput, EarthPressureData

def func_beta_zero(x, delta_phi_input):
    coefficients = {
        0: [-8.36852E-10, 1.32454E-07, -8.18524E-06, 2.47154E-04, -3.48064E-03, -3.26639E-03, 9.19571E-01],
        0.66: [2.15184E-10, -3.37193E-08, 2.15365E-06, -7.68893E-05, 2.00657E-03, -5.22665E-02, 1.04280E+00],
        1: [-1.26968E-11, 1.78562E-09, 2.20842E-08, -1.50889E-05, 1.12310E-03, -4.65229E-02, 1.01300E+00]
    }
    coef = coefficients[delta_phi_input]
    return (
        coef[0] * x**6 +
        coef[1] * x**5 +
        coef[2] * x**4 +
        coef[3] * x**3 +
        coef[4] * x**2 +
        coef[5] * x +
        coef[6]
    )

# Calculation functions for each δ/ϕ' level
def calculate_values(delta_phi, func, beta_phi_values, phi_values):
    data = {}
    for beta_phi in beta_phi_values:
        results = [func(phi, beta_phi) for phi in phi_values]
        data[beta_phi] = results
    return pd.DataFrame(data, index=phi_values).T

# 각 β/ϕ 값별로 데이터프레임을 생성하여 저장
def create_beta_delta_tables(table_beta_zero, delta_phi_values, phi_values):
    beta_delta_tables = {}
    for delta_phi in delta_phi_values:
        # 각 δ/ϕ 값에 대한 데이터프레임 생성 후 transpose하여 φ를 열로 배치
        beta_table = pd.DataFrame({
            f"δ/ϕ' = {delta_phi}": table_beta_zero.loc[delta_phi],
        }, index=phi_values)

        # 이름 지정
        table_name = f'beta_delta_table_delta_phi_{str(delta_phi).replace(".", "")}'
        beta_delta_tables[table_name] = beta_table

    return beta_delta_tables

def calc(input: EarthPressureInput) -> tuple[EarthPressureData, EarthPressureData, float]:
    beta_input = input.beta
    phi_input  = input.phi
    delta_input= input.delta

    beta_phi_input = beta_input/phi_input 
    delta_phi_input = delta_input/phi_input

    # 입력값 설정
    phi_values = np.array([10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5, 20, 20.5, 21, 21.5, 22, 22.5, 23, 23.5, 24, 24.5, 25, 25.5, 26, 26.5, 27, 27.5, 28, 28.5, 29, 29.5, 30, 30.5, 31, 31.5, 32, 32.5, 33, 33.5, 34, 34.5, 35, 35.5, 36, 36.5, 37, 37.5, 38, 38.5, 39, 39.5, 40, 40.5, 41, 41.5, 42, 42.5, 43, 43.5, 44, 44.5, 45])
    delta_phi_values = [0, 0.66, 1 ]

    # 각각의 delta_phi에 대해 결과 계산
    table_results_delta_zero = calculate_values(0, func_beta_zero, delta_phi_values, phi_values)

    # β/ϕ 값에 따른 테이블 생성
    beta_delta_tables = create_beta_delta_tables(
        table_results_delta_zero,
        delta_phi_values,
        phi_values
    )

    #----------------------------δ/ϕ' 커브셋 찾기,β/ϕ커브 생성  보간 끝 -------------------------------
    phi_values_str = list(map(str, phi_values))  # ϕ 값을 문자열로 변환하여 사용


    #--------------------------------------------------------------------------------------------------------------------
    # β/ϕ'_input 값

    final_curve = pd.DataFrame(columns=phi_values_str, index=["final_curve"])

    # CubicSpline 인스턴스 생성
    spline = CubicSpline()

    # 각 φ 값에 대해 보간을 수행하여 final_curve 결과 저장
    for phi_str in phi_values_str:
        phi_value = float(phi_str)  # 문자열을 다시 숫자로 변환하여 접근
        x_values = np.array(delta_phi_values)  # δ/ϕ 값
        y_values = np.array([
            table_results_delta_zero.loc[delta_phi, phi_value]
            for delta_phi in delta_phi_values
        ])  # 해당 φ 값에 대한 모든 δ/ϕ 값을 가져옴

        # 보간 수행
        interpolated_value = spline.interpolate(x_values, y_values, delta_phi_input)
        final_curve[phi_str] = interpolated_value[0, 0]

    # final_curve를 이전 테이블 형식으로 변환
    final_curve.index = [delta_phi_input]
    final_curve.index.name = "δ/ϕ"
    final_curve.columns.name = "ϕ"

    # 입력값 설정
    # final_curve에서 데이터 추출
    phi_values = np.array([float(val) for val in final_curve.columns])
    final_curve_y_values = final_curve.values.flatten()

    # 보간된 값 계산
    try:
        coeff_result = get_interpolated_value(phi_input, phi_values, final_curve_y_values)
        print(f"Interpolated coeff_result for φ = {phi_input}: {coeff_result}")
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

    # 결과 생성
    phi_values = list(map(float, table_results_delta_zero.columns))  # x축 값 (phi_values)
    series = {index: table_results_delta_zero.loc[index].tolist() for index in table_results_delta_zero.index}  # y값들
    base_data = EarthPressureData(phi_values=phi_values, series=series)

    calced_phi_values = list(map(float, final_curve.columns))  # x축 값 (phi_values)
    calced_series = {index: final_curve.loc[index].tolist() for index in final_curve.index}  # y값들
    calculated_data = EarthPressureData(phi_values=calced_phi_values, series=calced_series)

    return base_data, calculated_data, coeff_result


if __name__ == "__main__":
    input = EarthPressureInput(beta=0, phi=32, delta=32)
    base_data, calculated_data, coeff_result = calc(input)
    print(base_data)
    print(calculated_data)
    print(coeff_result)