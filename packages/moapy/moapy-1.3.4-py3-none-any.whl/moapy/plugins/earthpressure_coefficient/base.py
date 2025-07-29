import numpy as np
from moapy.auto_convert import MBaseModel

class EarthPressureData(MBaseModel):
    # 그래프를 그리기 위한 데이터 클래스
    phi_values: list[float]  # ϕ 값들 (x축)
    series: dict[float, list[float]]  # 각 β/ϕ 값에 해당하는 y값들

class EarthPressureResult(MBaseModel):
    ka_base: EarthPressureData
    ka_calculated_curve: EarthPressureData
    calculated_ka: float
    kp_base: EarthPressureData
    kp_calculated_curve: EarthPressureData
    calculated_kp: float

class EarthPressureInput(MBaseModel):
    beta: float
    phi: float
    delta: float

class CubicSpline:
    """
    3차 스플라인 보간을 수행하는 클래스
    """
    
    @staticmethod
    def get_array(array_data, transpose_h=True):
        arr = np.array(array_data, dtype=float)
        if arr.ndim == 1:
            arr = arr.reshape(-1, 1)
        elif transpose_h and arr.ndim == 2 and arr.shape[0] < arr.shape[1]:
            arr = arr.T
        return arr

    @staticmethod
    def check_ascending(xa, ya):
        if xa[0, 0] > xa[-1, 0]:
            return np.flipud(xa), np.flipud(ya), True
        return xa, ya, False

    @staticmethod
    def solve_tridiagonal(a, b, c, r):
        n = len(b)
        u = np.zeros((n, 1))
        gam = np.zeros(n)
        bet = b[0, 0]
        u[0, 0] = r[0, 0] / bet

        for j in range(1, n):
            gam[j] = c[j-1, 0] / bet
            bet = b[j, 0] - a[j, 0] * gam[j]
            u[j, 0] = (r[j, 0] - a[j, 0] * u[j-1, 0]) / bet

        for j in range(n-2, -1, -1):
            u[j, 0] -= gam[j+1] * u[j+1, 0]

        return u

    def interpolate(self, xa, ya, x_int, output=1, end_type=1, end1=0, end2=0, transpose_h=True):
        xa = self.get_array(xa)
        ya = self.get_array(ya)
        x_int = np.array(x_int).reshape(-1, 1)  # x_int을 배열로 변환하여 형식 보장
        n = xa.shape[0]

        xa, ya, rev_x = self.check_ascending(xa, ya)
        
        h = np.diff(xa[:, 0])
        m = np.diff(ya[:, 0]) / h

        a = np.zeros((n, 1))
        b = np.zeros((n, 1))
        c = np.zeros((n, 1))
        r = np.zeros((n, 1))
        
        if end_type == 1:
            r[0, 0] = end1
            r[-1, 0] = end2
            b[0, 0] = 1
            b[-1, 0] = 1
        else:
            r[0, 0] = 6 * (m[0] - end1)
            r[-1, 0] = 6 * (end2 - m[-1])
            b[0, 0] = 2 * h[0]
            c[0, 0] = h[0]
            a[-1, 0] = h[-1]
            b[-1, 0] = 2 * h[-1]

        for i in range(1, n-1):
            a[i, 0] = h[i-1]
            b[i, 0] = 2 * (h[i-1] + h[i])
            c[i, 0] = h[i]
            r[i, 0] = 6 * (m[i] - m[i-1])

        y2 = np.zeros((n, 4))
        y2[:, 0] = self.solve_tridiagonal(a, b, c, r)[:, 0]

        for i in range(n-1):
            y2[i, 1] = ya[i, 0]
            y2[i, 2] = m[i] - (h[i]/6) * (2*y2[i, 0] + y2[i+1, 0])
            y2[i, 3] = y2[i, 0] / 2

        if output == 2:
            return y2
        elif output == 1:
            return self._interpolate_points(xa, ya, y2, x_int, transpose_h)
        else:
            raise ValueError('Invalid "output" value')

    def _interpolate_points(self, xa, ya, y2a, x_int, transpose_h=True):
        x_int = self.get_array(x_int, transpose_h)
        n = xa.shape[0]
        n_int = x_int.shape[0]

        y = np.zeros((n_int, 1))
        j = 0

        for i in range(n_int):
            x = x_int[i, 0]
            if x <= xa[0, 0]:
                j = 0
            else:
                while j < n-1 and not (xa[j, 0] <= x <= xa[j+1, 0]):
                    j += 1

            xi = x - xa[j, 0]
            h = xa[j+1, 0] - xa[j, 0]
            m = (ya[j+1, 0] - ya[j, 0]) / h
            
            a = y2a[j, 1]
            b = y2a[j, 2]
            c = y2a[j, 3]
            d = (y2a[j+1, 0] - y2a[j, 0]) / (6 * h)
            y[i, 0] = a + b*xi + c*xi**2 + d*xi**3

        return y

#--------------------------------------------------------------------------------------------------------------------
# 선형 보간 함수 정의
def linear_interpolation(x, x1, x2, y1, y2):
    """
    두 점 사이의 선형 보간을 수행하는 함수
    x: 보간하려는 x 값
    x1, y1: 첫 번째 점의 좌표
    x2, y2: 두 번째 점의 좌표
    """
    return y1 + (x - x1) * (y2 - y1) / (x2 - x1)

def get_interpolated_value(x, x_values, y_values):
    """
    주어진 x값에 대해 보간된 y값을 찾는 함수
    x: 보간하려는 x 값
    x_values: x 좌표 배열
    y_values: y 좌표 배열
    """
    # x가 범위를 벗어나는지 확인
    if x < x_values[0] or x > x_values[-1]:
        raise ValueError(f"ϕ 값 {x}이(가) 데이터 범위({x_values[0]}-{x_values[-1]})를 벗어났습니다.")

    # x값이 있는 구간 찾기
    for i in range(len(x_values)-1):
        if x_values[i] <= x <= x_values[i+1]:
            return linear_interpolation(x, x_values[i], x_values[i+1], 
                                     y_values[i], y_values[i+1])

    return None
#-----------------------