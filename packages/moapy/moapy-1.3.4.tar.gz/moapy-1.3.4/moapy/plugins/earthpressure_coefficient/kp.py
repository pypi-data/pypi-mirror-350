import numpy as np
import pandas as pd
from moapy.plugins.earthpressure_coefficient.base import EarthPressureInput, EarthPressureData, CubicSpline, get_interpolated_value

def calc(input: EarthPressureInput) -> tuple[EarthPressureData, EarthPressureData, float]:
    beta_input= input.beta
    phi_input = input.phi
    delta_input= input.delta

    beta_phi_input = beta_input/phi_input 
    delta_phi_input = delta_input/phi_input

    def func_beta_zero(x, delta_phi_input):
        coefficients_le_35 = {
            1: [-4.20170E-08, 6.05710E-06, -3.34164E-04, 9.34488E-03, -1.36589E-01, 1.08400E+00, -2.10790E+00],
            0.66: [-1.89186E-08, 2.49632E-06, -1.24475E-04, 3.20049E-03, -4.26100E-02, 3.62336E-01, 1.26456E-02],
            0: [-1.66184E-09, 1.96822E-07, -9.37189E-06, 2.70822E-04, -3.86453E-03, 8.05157E-02, 8.00769E-01],
        }
        coefficients_gt_35 = {
            1: [0, 0, 1.02406E-03, -1.50642E-01, 8.35517E+00, -2.06122E+02, 1.90980E+03],
            0.66: [0, 0, 4.59438E-04, -6.51446E-02, 3.48098E+00, -8.24696E+01, 7.33112E+02],
            0: [0, 0, -4.95794E-05, 7.42930E-03, -4.10696E-01, 1.00981E+01, -9.07469E+01],
        }
        
        if x <= 35:
            coef = coefficients_le_35[delta_phi_input]
        else:
            coef = coefficients_gt_35[delta_phi_input]
        
        return (
            coef[0] * x**6
            + coef[1] * x**5
            + coef[2] * x**4
            + coef[3] * x**3
            + coef[4] * x**2
            + coef[5] * x
            + coef[6]
        )


    # Defining the functions for δ/ϕ' = 0 group with various β/ϕ values
    def func_0(x, beta_phi):
        coefficients_le_25 = {
            1: [8.46826E-08, -6.88881E-06, 2.22095E-04, -3.49522E-03, 3.04344E-02, -5.64283E-02, 1.05895E+00],
            0.8: [-5.23309E-07, 5.64531E-05, -2.48887E-03, 5.75790E-02, -7.34009E-01, 4.96670E+00, -1.24705E+01],
            0.6: [2.61474E-07, -2.62274E-05, 1.07484E-03, -2.29073E-02, 2.69780E-01, -1.59035E+00, 5.01101E+00],
            0.4: [-8.78349E-08, 8.87506E-06, -3.64110E-04, 7.83815E-03, -9.16300E-02, 6.21626E-01, -5.27510E-01],
            0.2: [7.56666E-08, -7.68826E-06, 3.22284E-04, -7.09515E-03, 8.74880E-02, -5.03813E-01, 2.31948E+00],
            0: [-2.44901E-07, 2.62491E-05, -1.14762E-03, 2.61776E-02, -3.27169E-01, 2.17505E+00, -4.68429E+00],
            -0.2: [-1.47297E-07, 1.52615E-05, -6.41664E-04, 1.39894E-02, -1.66111E-01, 1.06076E+00, -1.58817E+00],
            -0.4: [-1.18566E-07, 1.28512E-05, -5.67345E-04, 1.30308E-02, -1.63870E-01, 1.10132E+00, -1.87321E+00],
            -0.6: [1.54839E-07, -1.65013E-05, 7.23710E-04, -1.66955E-02, 2.12805E-01, -1.40031E+00, 4.85447E+00],
            -0.8: [0,0,0,0,0,0,0]
        }

        coefficients_gt_25 = {
            1: [1.31986E-06, -2.60147E-04, 2.13762E-02, -9.34999E-01, 2.29524E+01, -2.99576E+02, 1.62599E+03],
            0.8: [0, 9.31132E-06, - 1.45507E-03, 9.15728E-02, - 2.87071E+00, 4.48553E+01, - 2.76617E+02],
            0.6: [1.78768E-07, -3.84220E-05, 3.43811E-03, -1.62432E-01, 4.26911E+00, -5.90288E+01, 3.37607E+02],
            0.4: [-5.62713E-07, 1.17675E-04, -1.01544E-02, 4.63470E-01, -1.18007E+01, 1.59048E+02, -8.84524E+02],
            0.2: [1.44658E-07, -3.20212E-05, 2.90211E-03, -1.37763E-01, 3.62088E+00, -4.99616E+01, 2.85121E+02],
            0: [-1.58305E-07, 3.12642E-05, -2.54669E-03, 1.09619E-01, -2.62843E+00, 3.33549E+01, -1.73270E+02],
            -0.2: [1.34037E-07, -2.79005E-05, 2.39517E-03, -1.08553E-01, 2.74125E+00, -3.65312E+01, 2.02402E+02],
            -0.4: [-3.90874E-08, 8.71058E-06, -7.98276E-04, 3.85013E-02, -1.03074E+00, 1.45602E+01, -8.32922E+01],
            -0.6: [-3.14010E-08, 6.41674E-06, -5.38686E-04, 2.37581E-02, -5.80393E-01, 7.45322E+00, -3.80370E+01],
            -0.8: [0,0,0,0,0,0,0]
        }

        if x <= 25:
            coef = coefficients_le_25[beta_phi]
        else:
            coef = coefficients_gt_25[beta_phi]
            
        return coef[0] * x**6 + coef[1] * x**5 + coef[2] * x**4 + coef[3] * x**3 + coef[4] * x**2 + coef[5] * x + coef[6]

    # Defining the functions for δ/ϕ' = 0.66 group with various β/ϕ values
    def func_066(x, beta_phi):
        coefficients_le_35 = {
            1: [1.47260E-07, -1.72701E-05, 8.85720E-04, -2.40215E-02, 3.65575E-01, -2.78862E+00, 9.99585E+00],
            0.8: [1.52673E-07, -1.63597E-05, 7.37253E-04, -1.72332E-02, 2.24992E-01, -1.43471E+00, 5.02773E+00],
            0.6: [1.85945E-07, -2.08750E-05, 9.57516E-04, -2.24138E-02, 2.86788E-01, -1.79983E+00, 5.82586E+00],
            0.4: [7.08685E-08, -8.56423E-06, 4.40437E-04, -1.18533E-02, 1.79598E-01, -1.33174E+00, 5.30353E+00],
            0.2: [6.01895E-08, -8.26919E-06, 4.81272E-04, -1.46966E-02, 2.49850E-01, -2.10844E+00, 8.39922E+00],
            0: [-9.71897E-08, 1.19085E-05, -5.71097E-04, 1.38207E-02, -1.74903E-01, 1.16840E+00, -1.82507E+00],
            -0.2: [2.07772E-08, -2.70251E-06, 1.45139E-04, -3.99810E-03, 6.12565E-02, -4.24311E-01, 2.40001E+00],
            -0.4: [-2.30220E-09, 6.67415E-07, -5.24836E-05, 1.84853E-03, -3.10441E-02, 2.94121E-01, 1.78021E-01],
            -0.6: [1.03127E-08, -1.53447E-06, 9.23474E-05, -2.85132E-03, 4.78790E-02, -3.74609E-01, 2.33209E+00],
            -0.8: [-1.30977E-09, 3.50473E-07, -2.98816E-05, 1.16043E-03, -2.24278E-02, 2.26021E-01, 2.58633E-01],
        }

        coefficients_gt_35 = {
            1: [0, 0, 2.20681E-02, -3.22603E+00, 1.77327E+02, -4.33908E+03, 3.98655E+04],
            0.8: [0, 0, -1.59317E-03, 2.80826E-01, -1.76855E+01, 4.82247E+02, -4.84433E+03],
            0.6: [0, 0, -4.01320E-04, 5.76405E-02, -2.75291E+00, 5.15640E+01, -2.85999E+02],
            0.4: [0, 0, 6.31102E-04, -8.91992E-02, 4.87634E+00, -1.20535E+02, 1.13451E+03],
            0.2: [0, 0, -1.09893E-03, 1.80250E-01, -1.09117E+01, 2.90946E+02, -2.88635E+03],
            0: [0, 0, -2.69135E-04, 4.51115E-02, -2.76534E+00, 7.45602E+01, -7.45189E+02],
            -0.2: [0, 0, -2.01650E-05, 4.51033E-03, -3.18760E-01, 9.53370E+00, -1.01084E+02],
            -0.4: [0, 0, -4.73930E-05, 7.28254E-03, -4.11982E-01, 1.03679E+01, -9.55590E+01],
            -0.6: [0, 0, -3.43678E-05, 5.33980E-03, -3.09533E-01, 8.01753E+00, -7.62412E+01],
            -0.8: [0, 0, 1.31603E-05, -2.13445E-03, 1.27364E-01, -3.32726E+00, 3.38037E+01],
        }

        if x <= 35:
            coef = coefficients_le_35[beta_phi]
        else:
            coef = coefficients_gt_35[beta_phi]

        return (
            coef[0] * x**6
            + coef[1] * x**5
            + coef[2] * x**4
            + coef[3] * x**3
            + coef[4] * x**2
            + coef[5] * x
            + coef[6]
        )
    


    # Defining the functions for δ/ϕ' = 1.00 group with various β/ϕ values
    def func_1(x, beta_phi):
        coefficients_le_35 = {
            1: [1.79908E-07, -1.82479E-05, 7.93663E-04, -1.79122E-02, 2.26245E-01, -1.37801E+00, 4.74880E+00],
            0.8: [-3.98553E-08, 6.78859E-06, -3.54877E-04, 8.89111E-03, -1.08877E-01, 7.45273E-01, -6.41145E-01],
            0.6: [2.28392E-07, -2.87419E-05, 1.51428E-03, -4.15091E-02, 6.25326E-01, -4.73921E+00, 1.57299E+01],
            0.4: [4.41923E-08, -5.11091E-06, 2.67731E-04, -7.26474E-03, 1.09488E-01, -7.27721E-01, 3.14273E+00],
            0.2: [2.50923E-08, -3.73366E-06, 2.39082E-04, -7.53290E-03, 1.26838E-01, -9.71235E-01, 4.24767E+00],
            0: [-1.44279E-07, 2.00987E-05, -1.10468E-03, 3.09090E-02, -4.60446E-01, 3.55603E+00, -9.61565E+00],
            -0.2: [-1.36195E-08, 1.34429E-06, -3.88564E-05, 1.67420E-04, 1.14553E-02, -1.09507E-01, 1.60496E+00],
            -0.4: [2.95824E-08, -4.00802E-06, 2.17268E-04, -5.86009E-03, 8.26081E-02, -5.06593E-01, 2.31060E+00],
            -0.6: [2.21340E-08, -3.09329E-06, 1.71618E-04, -4.75304E-03, 6.89011E-02, -4.48453E-01, 2.27055E+00],
            -0.8: [5.67044E-09, -7.05742E-07, 3.44578E-05, -8.01304E-04, 8.18744E-03, 5.23587E-03, 8.67223E-01],
        }

        coefficients_gt_35 = {
            1: [0, 0, -1.02772E-02, 1.70947E+00, -1.04492E+02, 2.80048E+03, -2.78571E+04],
            0.8: [0, 0, 1.07945E-02, -1.58517E+00, 8.79190E+01, -2.17765E+03, 2.03067E+04],
            0.6: [0, 0, 3.35488E-03, -4.76274E-01, 2.55772E+01, -6.12741E+02, 5.51848E+03],
            0.4: [0, 0, 2.11070E-03, -3.09809E-01, 1.72728E+01, -4.30991E+02, 4.05600E+03],
            0.2: [0, 0, -1.57761E-03, 2.64012E-01, -1.62735E+01, 4.41061E+02, -4.44280E+03],
            0: [0, 0, -1.37931E-04, 2.95920E-02, -2.10660E+00, 6.32671E+01, -6.86944E+02],
            -0.2: [0, 0, -1.72316E-04, 3.08923E-02, -1.99131E+00, 5.59328E+01, -5.77989E+02],
            -0.4: [0, 0, 1.00991E-04, -1.40267E-02, 7.35246E-01, -1.69825E+01, 1.47989E+02],
            -0.6: [0, 0, -2.49016E-05, 4.25365E-03, -2.66189E-01, 7.38701E+00, -7.45249E+01],
            -0.8: [0, 0, 9.86836E-08, -1.43467E-04, 1.55760E-02, -5.52041E-01, 8.03045E+00],
        }

        if x <= 35:
            coef = coefficients_le_35[beta_phi]
        else:
            coef = coefficients_gt_35[beta_phi]

        return (
            coef[0] * x**6
            + coef[1] * x**5
            + coef[2] * x**4
            + coef[3] * x**3
            + coef[4] * x**2
            + coef[5] * x
            + coef[6]
        )


    # 결과를 저장할 클래스 정의

    # Calculation functions for each δ/ϕ' level
    def calculate_values(delta_phi, func, beta_phi_values, phi_values):
        data = {}
        for beta_phi in beta_phi_values:
            results = [func(phi, beta_phi) for phi in phi_values]
            data[beta_phi] = results
        return pd.DataFrame(data, index=phi_values).T

    # 입력값 설정
    phi_values = np.array([10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5, 20, 20.5, 21, 21.5, 22, 22.5, 23, 23.5, 24, 24.5, 25, 25.5, 26, 26.5, 27, 27.5, 28, 28.5, 29, 29.5, 30, 30.5, 31, 31.5, 32, 32.5, 33, 33.5, 34, 34.5, 35, 35.5, 36, 36.5, 37, 37.5, 38, 38.5, 39, 39.5, 40, 40.5, 41, 41.5, 42, 42.5, 43, 43.5, 44, 44.5, 45])
    beta_phi_values = [1, 0.8, 0.6, 0.4, 0.2, 0, -0.2, -0.4, -0.6, -0.8]

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

    #--------------------------------------------------------------------------------------------------------------------
    # β/ϕ'_input 값
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