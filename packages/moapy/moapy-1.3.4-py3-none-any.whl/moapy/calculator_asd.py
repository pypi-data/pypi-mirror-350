# 내용은 아래 참고요..
# https://midasitdev.atlassian.net/wiki/spaces/DGNDEV/pages/610730064/ASDEngine
import math

class CalculatorASDEngine:
    def __init__(self):
        self._nIterationNo = 0

        self._Fck = self._Fy = 0.0
        self._Ec = self._Es = 0.0
        self._Eyc = 0.0

        self._nConcrete = 0
        self._nRebar = 0
        self._arCon = []
        self._arBar = []

        self._CentroidX = self._CentroidY = 0.0
        self._PI = 0.0
        self._RotationAngle = 0.0
        self._OriginX = self._OriginY = 0.0
        self._Pn = self._Mnx = self._Mny = self._Mnxy = 0.0
        self._Xc = 0.0
        self._MnxCon = self._MnyCon = self._MnxBar = self._MnyBar = 0.0
        self._UseCompBar = False

        self._ASDEngineZero = 1.0e-7

        self._AxialOnly = False
        self._Area = 0.0
        self._Fx = 0.0

        self._Ix = self._Iy = 0.0

        self._MomentArea_x = self._MomentArea_y = 0.0
        self._AreaEff = 0.0
        self._AlreadyCalc = False

    def set_comp_bar_mode(self, b_use_comp_bar):
        self._UseCompBar = b_use_comp_bar

    def set_concrete_block_no(self, n_conc_no):
        assert n_conc_no > len(self._arCon)
        self._arCon = [None] * n_conc_no
        self._nConcrete = n_conc_no

    def add_concrete(self, _pos_x, _pos_y, _conc_b, _conc_h):
        conc = {'dWidth': _conc_b, 'dHeight': _conc_h, 'dX': _pos_x, 'dY': _pos_y}
        self._arCon.append(conc)
        self._nConcrete += 1

    def add_concrete_at_index(self, n_index, _pos_x, _pos_y, _conc_b, _conc_h):
        if n_index >= len(self._arCon):
            raise AssertionError("Index out of range")
        self._arCon[n_index] = {'dWidth': _conc_b, 'dHeight': _conc_h, 'dX': _pos_x, 'dY': _pos_y}

    def add_rebar(self, _pos_x, _pos_y, _area):
        r_bar = {'dX': _pos_x, 'dY': _pos_y, 'dArea': _area}
        self._arBar.append(r_bar)
        self._nRebar += 1

    def initialize(self, _fc, _fy, _ec, _es):
        from math import atan

        self._PI = 4.0 * atan(1.0)
        self._UseCompBar = True

        self._CentroidX = 0.0
        self._CentroidY = 0.0

        self._Fck = _fc
        self._Fy = _fy
        self._Ec = _ec
        self._Es = _es
        self._Eyc = _fc / _ec

        self._nIterationNo = 50

    def create_section(self, dH, dB):
        nDivideNo = 20

        if dB > dH:
            nDivideH = nDivideNo
            nDivideB = int(dB / dH * nDivideNo)
        else:
            nDivideB = nDivideNo
            nDivideH = int(dH / dB * nDivideNo)

        self.set_block_size(nDivideB * nDivideH, -1)

        dStepX = dB / nDivideB
        dStepY = dH / nDivideH

        nCountNo = 0
        for nX in range(nDivideB):
            for nY in range(nDivideH):
                self._arCon[nCountNo]['dWidth'] = dStepX
                self._arCon[nCountNo]['dHeight'] = dStepY
                self._arCon[nCountNo]['dX'] = -dB / 2 + dStepX * (nX + 0.5)
                self._arCon[nCountNo]['dY'] = -dH / 2 + dStepY * (nY + 0.5)
                nCountNo += 1

        self._Area = dH * dB

    def set_block_size(self, n_concrete, n_rebar):
        if n_concrete > 0:
            self._nConcrete = n_concrete
            # _arCon 리스트를 n_concrete 개수만큼 초기화
            self._arCon = [{'dWidth': 0, 'dHeight': 0, 'dX': 0, 'dY': 0} for _ in range(n_concrete)]

        if n_rebar > 0:
            self._nRebar = n_rebar
            # _arBar 리스트를 n_rebar 개수만큼 초기화
            self._arBar = [None] * n_rebar  # 적절한 초기화 값으로 대체 가능
    
    def calc_centroid(self):
        _ag = 0.0
        _sx = 0.0
        _sy = 0.0
        for i in range(self._nConcrete):
            asd_con = self._arCon[i]
            _ag += asd_con['dWidth'] * asd_con['dHeight']
            _sx += asd_con['dWidth'] * asd_con['dHeight'] * asd_con['dX']
            _sy += asd_con['dWidth'] * asd_con['dHeight'] * asd_con['dY']
        self._CentroidX = _sx / _ag
        self._CentroidY = _sy / _ag

    def calc(self):
        self._Mnxy = 0.0
        _pn_con = self.solve_concrete()
        _pn_bar = self.solve_rebar()

        self._Pn = _pn_con + _pn_bar
        self._Mnx = self._MnxCon + self._MnxBar
        self._Mny = self._MnyCon + self._MnyBar

    def calc_axial_only(self, _p):
        self._AxialOnly = True
        self._Fx = _p

        if _p < 0.0:
            return self.calc_tens_only(_p)
        else:
            return self.calc_comp_only(_p)

    def calc_tens_only(self, _p):
        n_bar = len(self._arBar)
        if n_bar < 1:
            raise AssertionError("No bars defined")
            return False

        _sum_abar = 0.0
        for i in range(n_bar):
            asd_bar = self._arBar[i]
            _sum_abar += asd_bar['dArea']

        for i in range(n_bar):
            r_asd_bar = self._arBar[i]
            r_asd_bar['dPn'] = _p * self.safe_div(r_asd_bar['dArea'], _sum_abar)

        return True

    def calc_comp_only(self, _p):
        n_con = len(self._arCon)
        if n_con < 1:
            raise AssertionError("No concrete blocks defined")
            return False

        _sum_acon = 0.0
        for i in range(n_con):
            asd_con = self._arCon[i]
            _sum_acon += asd_con['dWidth'] * asd_con['dHeight']

        for i in range(n_con):
            r_asd_con = self._arCon[i]
            _acon = r_asd_con['dWidth'] * r_asd_con['dHeight']
            r_asd_con['dPn'] = _p * self.safe_div(_acon, _sum_acon)

        return True

    def safe_div(self, num, denom):
        return num / denom if denom else 0.0

    def calc_rotation_angle(self, _p, _mx, _my):
        if not self.eq0(self._CentroidX):
            _my -= _p * self._CentroidX
            self._CentroidX = 0.0
        if not self.eq0(self._CentroidY):
            _mx -= _p * self._CentroidY
            self._CentroidY = 0.0

        _mn = math.hypot(_mx, _my)
        if self.eq0(_mn, self.get_radian_tolerance()):
            return self.calc_axial_only(_p)

        _angle = self.calc_moment_angle(_mx, _my)
        _rotation = _angle
        if math.fabs(_mn / _p) < 0.0001:
            self.rotate_section(_rotation)
            self.calc_strain_rebar(_p, _mx, _my)
            return True

        _angle_temp = 0.0
        _angle_max = self._PI
        _angle_min = -self._PI
        for i in range(self._nIterationNo):
            self.rotate_section(_rotation)
            self.calc_strain_rebar(_p, _mx, _my)

            if self._Pn == 0.0:
                _angle_temp = math.atan(1.0)
            else:
                _angle_temp = self.calc_moment_angle(self._Mnx, self._Mny)

            if math.fabs(_angle - _angle_temp) < 0.0001:
                break

            if _angle < _angle_temp:
                _angle_max = _rotation
            else:
                _angle_min = _rotation

            _rotation = (_angle_max + _angle_min) / 2.0

        if math.fabs(_angle - _angle_temp) > 0.1:
            return False
        if (math.fabs(_p / self._Pn) < 0.99) or (math.fabs(_p / self._Pn) > 1.01):
            return False
        return True

    def calc_neutralaxis(self, _p, _xmin, _xmax):
        if _xmin < self._ASDEngineZero:
            _xmin = self._ASDEngineZero
        if _xmax < self._ASDEngineZero:
            _xmax = self.calc_xmax()

        i_loop_count = 0
        while _p > self._Pn:
            self._Xc = _xmax
            self.calc()

            if _p > self._Pn:
                _xmax *= 1.5

            i_loop_count += 1
            if i_loop_count > self._nIterationNo:
                break

        for i in range(self._nIterationNo):
            self._Xc = (_xmin + _xmax) / 2.0
            self.calc()
            if 0.999 < self._Pn / _p < 1.001:
                return

            if self._Pn > _p:
                _xmax = self._Xc
            else:
                _xmin = self._Xc

    def calc_strain_rebar(self, _p, _mx, _my):
        _mn = math.sqrt(_mx**2 + _my**2)  # if _mn == 0.0, consider setting _mn to a small nonzero value

        self._Eyc = self._Fck / self._Ec
        for i in range(self._nIterationNo):
            self.calc_neutralaxis(_p, 0, 0)  # Assuming dXmin and dXmax need to be passed or determined within calc_neutralaxis
            if _mn < self._Mnxy:
                break

            self._Eyc *= 1.5

        _eyc_max = self._Eyc
        _eyc_min = self._ASDEngineZero
        if _p < self._ASDEngineZero:
            _eyc_min = -self._Fy / self._Es

        for i in range(self._nIterationNo):
            self._Eyc = (_eyc_min + _eyc_max) / 2.0

            self.calc_neutralaxis(_p, 0, 0)  # Adjusting for calc_neutralaxis signature

            if _mn != 0.0:
                if 0.999 < self._Mnxy / _mn < 1.001:
                    return

                if self._Mnxy > _mn:
                    _eyc_max = self._Eyc
                else:
                    _eyc_min = self._Eyc
            else:
                return

        self.calc_neutralaxis(_p, 0, 0)  # Final adjustment and run, considering default values for dXmin and dXmax

    def calc_moment_angle(self, _mx, _my):
        if _mx == 0.0:
            if _my == 0.0:
                _angle = 0.0
            elif _my < 0.0:
                _angle = -self._PI / 2.0
            else:
                _angle = self._PI / 2.0
        elif _my == 0.0:
            if _mx < 0.0:
                _angle = -self._PI
            else:
                _angle = 0.0
        elif _mx < 0.0:
            if _my < 0.0:
                _angle = -self._PI + math.atan(_my / _mx)
            else:
                _angle = self._PI + math.atan(_my / _mx)
        else:
            _angle = math.atan(_my / _mx)
        return _angle

    def rotate_section(self, _rotation):
        self._RotationAngle = _rotation

        _dist_x = _dist_y = _dist = 0.0
        _angle = _theta = _length_temp = _length_max = float('-inf')

        for asd_con in self._arCon:
            _dist_x = asd_con['dX']
            _dist_y = asd_con['dY']
            _dist = math.sqrt(_dist_x**2 + _dist_y**2)

            _angle = math.pi / 2.0 if _dist_x == 0.0 else math.atan(_dist_y / _dist_x)

            _length_temp = _dist * math.sin(_angle + _rotation)

            if _dist_x < 0.0:
                _length_temp *= -1.0

            if _length_temp > _length_max:
                _length_max = _length_temp
                self._OriginX = asd_con['dX'] + asd_con['dWidth'] / 2.0 if asd_con['dX'] > 0.0 else asd_con['dX'] - asd_con['dWidth'] / 2.0
                self._OriginY = asd_con['dY'] + asd_con['dHeight'] / 2.0 if asd_con['dY'] > 0.0 else asd_con['dY'] - asd_con['dHeight'] / 2.0

        _dist_x = self._OriginX - self._CentroidX
        _dist_y = self._OriginY - self._CentroidY
        _dist = math.sqrt(_dist_x**2 + _dist_y**2)
        _angle = math.pi / 2.0 if math.fabs(_dist_x) < self._ASDEngineZero else math.atan(_dist_y / _dist_x)
        _theta = _rotation + _angle
        _l_origin2centroid = math.fabs(_dist * math.sin(_theta))

        for asd_con in self._arCon:
            _dist_x = self._OriginX - asd_con['dX']
            _dist_y = self._OriginY - asd_con['dY']
            _dist = math.sqrt(_dist_x**2 + _dist_y**2)
            _angle = math.pi / 2.0 if math.fabs(_dist_x) < self._ASDEngineZero else math.atan(_dist_y / _dist_x)
            _theta = _rotation + _angle

            asd_con['dDorigin'] = math.fabs(_dist * math.sin(_theta))
            asd_con['dDcentroid'] = _l_origin2centroid - asd_con['dDorigin']

        _max_d = 0.0
        for asd_bar in self._arBar:
            _dist_x = self._OriginX - asd_bar['dX']
            _dist_y = self._OriginY - asd_bar['dY']
            _dist = math.sqrt(_dist_x**2 + _dist_y**2)
            _angle = math.pi / 2.0 if math.fabs(_dist_x) < self._ASDEngineZero else math.atan(_dist_y / _dist_x)
            _theta = _rotation + _angle

            asd_bar['dDorigin'] = math.fabs(_dist * math.sin(_theta))
            asd_bar['dDcentroid'] = _l_origin2centroid - asd_bar['dDorigin']

            if asd_bar['dDorigin'] > _max_d:
                _max_d = asd_bar['dDorigin']

        return _max_d

    def calc_xmax(self):
        _dist = max(asd_bar['dDorigin'] for asd_bar in self._arBar) if self._arBar else 0.0
        _dist_max = max(asd_con['dDorigin'] for asd_con in self._arCon) if self._arCon else 0.0

        if self._Eyc > self._Fy / self._Es:
            _xmax = self._Eyc * _dist / (self._Eyc - self._Fy / self._Es)
        else:
            _xmax = _dist * 1000.0

        if _xmax < _dist_max * 1.5:
            _xmax = _dist_max * 1.5

        return _xmax

    def solve_concrete(self):
        _area = _pn_con = _eyc = 0.0

        self._MnxCon = self._MnyCon = 0.0

        if self._Eyc < self._ASDEngineZero:
            for asd_con in self._arCon:
                asd_con['dPn'] = 0.0
            return _pn_con

        for asd_con in self._arCon:
            if asd_con['dDorigin'] > self._Xc:
                asd_con['dPn'] = 0.0
                continue

            _eyc = ((self._Xc - asd_con['dDorigin']) / self._Xc) * self._Eyc
            _area = asd_con['dHeight'] * asd_con['dWidth']

            asd_con['dPn'] = _area * _eyc * self._Ec
            _pn_con += asd_con['dPn']

            self._MnxCon += asd_con['dPn'] * (asd_con['dY'] - self._CentroidX)
            self._MnyCon += asd_con['dPn'] * (asd_con['dX'] - self._CentroidY)
            self._Mnxy += asd_con['dPn'] * asd_con['dDcentroid']

        return _pn_con

    def solve_rebar(self):
        _pn_bar = _fbar = 0.0

        if self._Xc == 0.0:
            self._Xc = self._ASDEngineZero

        self._MnxBar = self._MnyBar = 0.0

        if self._Eyc > 0.0:
            for asd_bar in self._arBar:
                if asd_bar['dDorigin'] < self._Xc:
                    _fbar = 0.0
                    if self._UseCompBar:
                        _fbar = (self._Es - self._Ec) * (self._Eyc * (self._Xc - asd_bar['dDorigin']) / self._Xc)
                else:
                    _fbar = self._Es * (self._Eyc * (self._Xc - asd_bar['dDorigin']) / self._Xc)

                asd_bar['dPn'] = _fbar * asd_bar['dArea']
                _pn_bar += asd_bar['dPn']

                self._MnxBar += asd_bar['dPn'] * (asd_bar['dY'] - self._CentroidY)
                self._MnyBar += asd_bar['dPn'] * (asd_bar['dX'] - self._CentroidX)
                self._Mnxy += asd_bar['dPn'] * asd_bar['dDcentroid']
        else:
            _eyc = abs(self._Eyc)
            for asd_bar in self._arBar:
                _eys = (_eyc * (self._Xc - asd_bar['dDorigin']) / self._Xc) + _eyc * 2.0
                _fbar = self._Es * _eys

                asd_bar['dPn'] = _fbar * asd_bar['dArea']
                _pn_bar += asd_bar['dPn']

                self._MnxBar += asd_bar['dPn'] * (asd_bar['dY'] - self._CentroidY)
                self._MnyBar += asd_bar['dPn'] * (asd_bar['dX'] - self._CentroidX)
                self._Mnxy += asd_bar['dPn'] * asd_bar['dDcentroid']

        return _pn_bar

    def get_sigma2(self, _point_x, _point_y):
        if self._AxialOnly:
            return self.safe_div(self._Fx, self._Area)

        _dist_x = self._OriginX - _point_x
        _dist_y = self._OriginY - _point_y
        _dist = math.sqrt(_dist_x**2 + _dist_y**2)
        _angle = self._PI / 2.0 if math.fabs(_dist_x) < self._ASDEngineZero else math.atan(_dist_y / _dist_x)
        _theta = self._RotationAngle + _angle

        _dorigin = math.fabs(_dist * math.sin(_theta))
        _eyc = ((self._Xc - _dorigin) / self._Xc) * math.fabs(self._Eyc)
        if self._Eyc < 0.0:
            _eyc += self._Eyc * 2.0

        _sigma = _eyc * self._Ec
        if _sigma < 0.0:
            _sigma = 0.0

        return _sigma

    def get_sigma_each_load_new(self, _point_x, _point_y, _p, _mx, _my):
        if not self._AlreadyCalc:
            self._MomentArea_x = self._MomentArea_y = self._AreaEff = 0.0
            for asd_con in self._arCon:
                if self.uq0(asd_con['dPn']):
                    self._MomentArea_x += asd_con['dWidth'] * asd_con['dHeight'] * asd_con['dX']
                    self._MomentArea_y += asd_con['dWidth'] * asd_con['dHeight'] * asd_con['dY']
                    self._AreaEff += asd_con['dWidth'] * asd_con['dHeight']

            self._Ix = self._Iy = 0.0
            for asd_con in self._arCon:
                if self.uq0(asd_con['dPn']):
                    self._Ix += asd_con['dWidth'] * (asd_con['dHeight']**3) / 12.0
                    self._Ix += asd_con['dWidth'] * asd_con['dHeight'] * ((asd_con['dX'] - self.safe_div(self._MomentArea_x, self._AreaEff))**2)

                    self._Iy += asd_con['dHeight'] * (asd_con['dWidth']**3) / 12.0
                    self._Iy += asd_con['dWidth'] * asd_con['dHeight'] * ((asd_con['dY'] - self.safe_div(self._MomentArea_y, self._AreaEff))**2)
            
            self._AlreadyCalc = True

        _center_to_dcentroid_x = self.safe_div(self._MomentArea_x, self._AreaEff)
        _center_to_dcentroid_y = self.safe_div(self._MomentArea_y, self._AreaEff)

        _zx = self.safe_div(self._Ix, _point_x - _center_to_dcentroid_x)
        _zy = self.safe_div(self._Iy, _point_y - _center_to_dcentroid_y)

        _sigma_p = self.safe_div(_p, self._AreaEff)
        _sigma_mx = self.safe_div(_my, _zx)
        _sigma_my = self.safe_div(_mx, _zy)
        _sigma_mx_byp = self.safe_div(_p * _center_to_dcentroid_x * -1.0, _zx)
        _sigma_my_byp = self.safe_div(_p * _center_to_dcentroid_y * -1.0, _zy)

        return _sigma_p + _sigma_mx + _sigma_my + _sigma_mx_byp + _sigma_my_byp

    def eq0(self, value, tolerance=1.0e-7):
        return math.fabs(value) < tolerance

    def get_radian_tolerance(self):
        # Assuming a placeholder value for radian tolerance
        return 1.0e-4
