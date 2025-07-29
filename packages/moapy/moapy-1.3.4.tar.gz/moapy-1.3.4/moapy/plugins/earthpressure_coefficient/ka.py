import numpy as np
import pandas as pd
from moapy.plugins.earthpressure_coefficient.base import EarthPressureInput, EarthPressureData, CubicSpline, get_interpolated_value

def calc(input: EarthPressureInput) -> tuple[EarthPressureData, EarthPressureData, float]:
    beta_input= input.beta
    phi_input = input.phi
    delta_input= input.delta

    beta_phi_input = beta_input/phi_input 
    delta_phi_input = delta_input/phi_input

    # Defining the functions for δ/ϕ' = 0 group with various β/ϕ values
    def func_0(x, beta_phi):
        coefficients = {
            1: [1.46543E-09, -2.46616E-07, 1.67135E-05, -5.78393E-04, 1.04074E-02, -9.78409E-02, 1.41375E+00],
            0.8: [4.40794E-10, -6.97856E-08, 4.28877E-06, -1.25405E-04, 1.73229E-03, -2.68245E-02, 1.02752E+00],
            0.6: [-5.66977E-10, 9.24833E-08, -5.98705E-06, 1.95097E-04, -3.19698E-03, 4.17906E-03, 9.24494E-01],
            0.4: [6.98276E-10, -1.15127E-07, 7.40878E-06, -2.33567E-04, 3.86867E-03, -5.19226E-02, 1.05087E+00],
            0.2: [5.43893E-10, -9.84093E-08, 7.21423E-06, -2.74902E-04, 5.96424E-03, -8.94740E-02, 1.24324E+00],
            0: [5.67225E-10, -9.53165E-08, 6.51855E-06, -2.33656E-04, 4.87860E-03, -7.60361E-02, 1.15420E+00],
            -0.2: [-7.63132E-10, 1.23806E-07, -7.96991E-06, 2.55384E-04, -3.91257E-03, 2.68202E-03, 8.62274E-01],
            -0.4: [1.76828E-10, -3.37929E-08, 2.63943E-06, -1.10599E-04, 2.90393E-03, -6.21351E-02, 1.08784E+00],
            -0.6: [5.12518E-10, -8.85103E-08, 6.14205E-06, -2.21460E-04, 4.69137E-03, -7.53193E-02, 1.10372E+00],
            -0.8: [2.19281E-10, -3.80736E-08, 2.66644E-06, -9.96222E-05, 2.43978E-03, -5.52214E-02, 1.02719E+00],
            -1: [-1.15469E-10, 2.64066E-08, -2.23133E-06, 8.70027E-05, -1.29867E-03, -1.78384E-02, 8.70551E-01]
        }
        coef = coefficients[beta_phi]
        return coef[0] * x**6 + coef[1] * x**5 + coef[2] * x**4 + coef[3] * x**3 + coef[4] * x**2 + coef[5] * x + coef[6]

    # Defining the functions for δ/ϕ' = 0.66 group with various β/ϕ values
    def func_066(x, beta_phi):
        coefficients = {
            1: [1.13970E-09, -1.89661E-07, 1.26153E-05, -4.23516E-04, 7.25225E-03, -6.69810E-02, 1.24045E+00],
            0.8: [-6.43451E-10, 1.06287E-07, -7.05441E-06, 2.40048E-04, -4.27478E-03, 1.78439E-02, 8.69685E-01],
            0.6: [2.57380E-10, -4.25640E-08, 2.87026E-06, -1.02242E-04, 2.24467E-03, -4.82135E-02, 1.07826E+00],
            0.4: [-6.78836E-10, 1.05375E-07, -6.50559E-06, 2.01739E-04, -3.01306E-03, -3.00828E-03, 8.88545E-01],
            0.2: [-5.01586E-11, 9.41414E-09, -6.70893E-07, 2.00054E-05, 1.06748E-04, -3.15602E-02, 9.64908E-01],
            0: [-3.14206E-10, 5.28789E-08, -3.51212E-06, 1.11794E-04, -1.34679E-03, -2.18851E-02, 9.20737E-01],
            -0.2: [1.46174E-10, -2.23103E-08, 1.42300E-06, -5.41242E-05, 1.66190E-03, -4.96095E-02, 1.00070E+00],
            -0.4: [6.26886E-10, -1.01378E-07, 6.62197E-06, -2.28619E-04, 4.82212E-03, -7.89221E-02, 1.09221E+00],
            -0.6: [2.52717E-10, -3.78316E-08, 2.29506E-06, -7.82306E-05, 2.03050E-03, -5.26884E-02, 9.78363E-01],
            -0.8: [-2.13493E-10, 3.38432E-08, -1.99147E-06, 4.60796E-05, 2.75453E-04, -4.22970E-02, 9.50446E-01],
            -1: [1.10172E-10, -1.99091E-08, 1.53993E-06, -7.00649E-05, 2.26848E-03, -5.89581E-02, 9.93040E-01]
        }
        coef = coefficients[beta_phi]
        return coef[0] * x**6 + coef[1] * x**5 + coef[2] * x**4 + coef[3] * x**3 + coef[4] * x**2 + coef[5] * x + coef[6]

    # Defining the functions for δ/ϕ' = 1.00 group with various β/ϕ values
    def func_1(x, beta_phi):
        coefficients = {
            1: [0, 0, 0, 4.54094E-06, -5.26602E-04, 3.99463E-03, 9.73806E-01],
            0.8: [0, 0, 0, 2.79402E-06, -1.09345E-04, -1.72820E-02, 9.63949E-01],
            0.6: [0, 0, 0, -9.23451E-07, 2.75585E-04, -2.86209E-02, 9.87604E-01],
            0.4: [0, 0, 0, -2.32772E-06, 4.33753E-04, -3.32240E-02, 9.81982E-01],
            0.2: [0, 0, 0, -4.05770E-06, 6.08703E-04, -3.80504E-02, 9.88962E-01],
            0: [0, 0, 0, -3.52745E-06, 5.65433E-04, -3.63363E-02, 9.42154E-01],
            -0.2: [0, 0, 0, -4.06039E-06, 6.23223E-04, -3.79307E-02, 9.35393E-01],
            -0.4: [0, 0, 0, -5.71941E-06, 7.78942E-04, -4.20450E-02, 9.48074E-01],
            -0.6: [0, 0, 0, -5.69672E-06, 7.75904E-04, -4.15399E-02, 9.22472E-01],
            -0.8: [0, 0, 0, -6.33631E-06, 8.32722E-04, -4.28064E-02, 9.14288E-01],
            -1: [0, 0, 0, -6.64980E-06, 8.65950E-04, -4.36932E-02, 9.09637E-01]
        }
        coef = coefficients[beta_phi]
        return coef[3] * x**3 + coef[4] * x**2 + coef[5] * x + coef[6]

    # Calculation functions for each δ/ϕ' level
    def calculate_values(delta_phi, func, beta_phi_values, phi_values):
        data = {}
        for beta_phi in beta_phi_values:
            results = [func(phi, beta_phi) for phi in phi_values]
            data[beta_phi] = results
        return pd.DataFrame(data, index=phi_values).T

    # 입력값 설정
    phi_values = np.array([10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5, 20, 20.5, 21, 21.5, 22, 22.5, 23, 23.5, 24, 24.5, 25, 25.5, 26, 26.5, 27, 27.5, 28, 28.5, 29, 29.5, 30, 30.5, 31, 31.5, 32, 32.5, 33, 33.5, 34, 34.5, 35, 35.5, 36, 36.5, 37, 37.5, 38, 38.5, 39, 39.5, 40, 40.5, 41, 41.5, 42, 42.5, 43, 43.5, 44, 44.5, 45])
    beta_phi_values = [1, 0.8, 0.6, 0.4, 0.2, 0, -0.2, -0.4, -0.6, -0.8, -1]

    # Calculating results for each δ/ϕ' and storing them in separate DataFrames
    delta_phi_functions_000 = {0: func_0}
    delta_phi_functions_066 = {0.66: func_066}
    delta_phi_functions_100 = {1: func_1}

    # 각각의 delta_phi에 대해 결과 계산
    table_results_delta_phi000 = calculate_values(0, func_0, beta_phi_values, phi_values)
    table_results_delta_phi066 = calculate_values(0.66, func_066, beta_phi_values, phi_values)
    table_results_delta_phi100 = calculate_values(1, func_1, beta_phi_values, phi_values)

    # 결과 출력
    print("Results for δ/ϕ' = 0:")
    print(table_results_delta_phi000, "\n")

    print("Results for δ/ϕ' = 0.66:")
    print(table_results_delta_phi066, "\n")

    print("Results for δ/ϕ' = 1:")
    print(table_results_delta_phi100, "\n")

    # 각 β/ϕ 값별로 데이터프레임을 생성하여 저장
    def create_beta_delta_tables(table_000, table_066, table_100, beta_phi_values, phi_values):
        beta_delta_tables = {}
        for beta_phi in beta_phi_values:
            # 각 β/ϕ 값에 대한 데이터프레임 생성 후 transpose하여 δ/ϕ를 행 인덱스로, φ를 열로 배치
            beta_table = pd.DataFrame({
                "δ/ϕ' = 0": table_000.loc[beta_phi],
                "δ/ϕ' = 0.66": table_066.loc[beta_phi],
                "δ/ϕ' = 1": table_100.loc[beta_phi]
            }, index=phi_values).T
            
            # φ 값을 열로 설정하고, δ/ϕ를 행 인덱스로 만듦
            beta_table.index = [0.0000, 0.6600, 1.0000]
            beta_table.index.name = 'δ/ϕ'
            
            # 이름 지정
            table_name = f'beta_delta_table_{str(beta_phi).replace(".", "")}'
            beta_delta_tables[table_name] = beta_table

        return beta_delta_tables

    # β/ϕ 값에 따른 테이블 생성
    beta_delta_tables = create_beta_delta_tables(
        table_results_delta_phi000, 
        table_results_delta_phi066, 
        table_results_delta_phi100, 
        beta_phi_values, 
        phi_values
    )

    # 각 테이블을 출력
    for name, table in beta_delta_tables.items():
        print(f"\nResults for {name}:")
        print(table)
    #----------------------------δ/ϕ' 커브셋 찾기,β/ϕ커브 생성  보간 끝 -------------------------------

    phi_values_str = list(map(str, phi_values))  # ϕ 값을 문자열로 변환하여 사용

    # 보간을 위한 테이블들
    table_results_delta_phi000 = calculate_values(0, func_0, beta_phi_values, phi_values)
    table_results_delta_phi066 = calculate_values(0.66, func_066, beta_phi_values, phi_values)
    table_results_delta_phi100 = calculate_values(1, func_1, beta_phi_values, phi_values)

    # 각 테이블에 열 이름을 문자열 형태로 설정
    table_results_delta_phi000.columns = phi_values_str
    table_results_delta_phi066.columns = phi_values_str
    table_results_delta_phi100.columns = phi_values_str

    # 결과를 저장할 데이터프레임 생성

    result_table = pd.DataFrame(index=beta_phi_values, columns=phi_values_str)

    # CubicSpline 인스턴스 생성
    spline = CubicSpline()

    # 각 `β/ϕ` 값에 대해 각 `ϕ` 값에 대해 보간을 수행하여 결과 저장
    for beta_phi in beta_phi_values:
        for phi_str in phi_values_str:
            # 각 δ/ϕ 값을 x로 하고, 해당 β/ϕ와 φ에 대한 y값을 배열로 설정
            x_values = np.array([0.0, 0.66, 1.0])  # δ/ϕ 값
            y_values = np.array([
                table_results_delta_phi000.loc[beta_phi, phi_str],
                table_results_delta_phi066.loc[beta_phi, phi_str],
                table_results_delta_phi100.loc[beta_phi, phi_str]
            ])
            
            # 보간 수행
            interpolated_value = spline.interpolate(x_values, y_values, delta_phi_input)
            result_table.loc[beta_phi, phi_str] = interpolated_value[0, 0]  # 보간 결과를 결과 테이블에 저장

    # 최종 결과 출력
    result_table.index.name = 'β/ϕ'
    result_table.columns.name = 'ϕ'
    print("δ/ϕ’_resulttable:")
    print(result_table)

    phi_values = list(map(float, result_table.columns))  # x축 값 (phi_values)
    series = {index: result_table.loc[index].tolist() for index in result_table.index}  # y값들
    earth_pressure_data = EarthPressureData(phi_values=phi_values, series=series)
    #--------------------------------------------------------------------------------------------------------------------
    # β/ϕ'_input 값
    print(earth_pressure_data)
    final_curve = pd.DataFrame(columns=phi_values_str, index=["final_curve"])

    # CubicSpline 인스턴스 생성
    spline = CubicSpline()

    # 각 φ 값에 대해 보간을 수행하여 final_curve 결과 저장
    for phi_str in phi_values_str:
        # x와 y 값을 설정 (x: 기존 β/ϕ 값, y: δ/ϕ’_resulttable의 해당 열 값)
        x_values = np.array(beta_phi_values)
        y_values = result_table[phi_str].values.astype(float)

        # 보간 수행
        interpolated_value = spline.interpolate(x_values, y_values, beta_phi_input)
        final_curve[phi_str] = interpolated_value[0, 0]

    # final_curve를 이전 테이블 형식으로 변환
    final_curve.index = [beta_phi_input]
    final_curve.index.name = "β/ϕ"
    final_curve.columns.name = "ϕ"

    # 최종 결과 출력
    print("final_curve:")
    print(final_curve)
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
    phi_values = list(map(float, result_table.columns))  # x축 값 (phi_values)
    series = {index: result_table.loc[index].tolist() for index in result_table.index}  # y값들
    base_data = EarthPressureData(phi_values=phi_values, series=series)

    phi_values = list(map(float, final_curve.columns))  # x축 값 (phi_values)
    series = {index: final_curve.loc[index].tolist() for index in final_curve.index}  # y값들
    calculated_data = EarthPressureData(phi_values=phi_values, series=series)

    return base_data, calculated_data, coeff_result