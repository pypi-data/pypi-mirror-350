from collections import defaultdict
import math

def steel_box(vSize, refSize):
    # Variable Initialization
    B1, B2, B3, B4, B5, B6, H, t1, t2, tw1, tw2 = vSize
    Top, Bot = refSize
    twx1 = tw1 * math.sqrt(H ** 2 + ((Bot + B4) - (Top + B1)) ** 2) / H
    twx2 = tw2 * math.sqrt(H ** 2 + ((Top + B1 + B2) - (Bot + B4 + B5)) ** 2) / H
    # Outer Cell - Left Side
    ycol = [0]
    zcol = [0]
    ycol.append(ycol[0] - B2 / 2 - B1)
    zcol.append(zcol[0])
    ycol.append(ycol[1])
    zcol.append(zcol[1] - t1)
    ycol.append(ycol[2] + B1 - twx1)
    zcol.append(zcol[2])
    ycol.append(-(Top + B1 + B2 / 2) + (Bot + B4 - twx1))
    zcol.append(zcol[3] - H)
    ycol.append(ycol[4] - B4 + twx1)
    zcol.append(zcol[4])
    ycol.append(ycol[5])
    zcol.append(zcol[5] - t2)
    ycol.append(ycol[6] + B4 + B5 / 2)
    zcol.append(zcol[6])
    # Outer Cell - Right Side
    ycor = [0]
    zcor = [0]
    ycor.append(ycor[0] + B2 / 2 + B3)
    zcor.append(zcor[0])
    ycor.append(ycor[1])
    zcor.append(zcor[1] - t1)
    ycor.append(ycor[2] - B3 + twx2)
    zcor.append(zcor[2])
    ycor.append(-(B2/2 + B1 + Top) + (Bot + B4 + B5 + twx2))
    zcor.append(zcor[3] - H)
    ycor.append(ycor[4] + B6 - twx2)
    zcor.append(zcor[4])
    ycor.append(ycor[5])
    zcor.append(zcor[5] - t2) 
    ycor.append(-(B2/2 + B1 + Top) + (Bot + B4 + B5/2))
    zcor.append(zcor[6])
    # Inner Cell - Left Side
    ycil = [0]
    zcil = [-t1]
    ycil.append(ycil[0] - B2 / 2)
    zcil.append(zcil[0])
    ycil.append(-(Top + B1 + B2 / 2) + (Bot + B4))
    zcil.append(zcil[1] - H)
    ycil.append(ycil[2] + B5 / 2)
    zcil.append(zcil[2])
    # Inner Cell - Right Side
    ycir = [0]
    zcir = [-t1]
    ycir.append(ycir[0] + B2 / 2)
    zcir.append(zcir[0])
    ycir.append(-(B2/2 + B1 + Top) + (Bot + B4 + B5))
    zcir.append(zcir[1] - H)
    ycir.append(ycir[2] - B5 / 2)
    zcir.append(zcir[2])
    # Reverse
    ycor.reverse()
    zcor.reverse()
    ycil.reverse()
    zcil.reverse()
    # Remove Origin
    ycor.pop(0)
    zcor.pop(0)
    ycil.pop(0)
    zcil.pop(0)
    # All Cell
    ycoAll = ycol + ycor
    zcoAll = zcol + zcor
    yciAll = ycir + ycil
    zciAll = zcir + zcil
    # Return
    outer = defaultdict(list)
    inner = defaultdict(list)
    comp = defaultdict(list)
    outer[0] = ycoAll
    outer[1] = zcoAll
    inner[0] = yciAll
    inner[1] = zciAll
    return outer, inner, comp

def steel_i(vSize, refSize) :
    # Variable Initialization
    B1, B2, B3, B4, H, t1, t2, tw = vSize
    Top, Bot = refSize
    twx = tw * math.sqrt(H ** 2 + ((Bot + B3) - (Top + B1)) ** 2) / H
    # Outer Cell - Left Side
    ycol = [0]
    zcol = [0]
    ycol.append(ycol[0] - B1)
    zcol.append(zcol[0])
    ycol.append(ycol[1])
    zcol.append(zcol[1] - t1)
    ycol.append(ycol[2] + B1 - twx / 2)
    zcol.append(zcol[2])
    ycol.append(-(B1 + Top) + (Bot + B3 - twx / 2))
    zcol.append(zcol[3] - H)
    ycol.append(ycol[4] - B3 + twx / 2)
    zcol.append(zcol[4])
    ycol.append(ycol[5])
    zcol.append(zcol[5] - t2)
    ycol.append(-(B1 + Top) + (Bot + B3))
    zcol.append(zcol[6])
    # Outer Cell - Right Side
    ycor = [0]
    zcor = [0]
    ycor.append(ycor[0] + B2)
    zcor.append(zcor[0])
    ycor.append(ycor[1])
    zcor.append(zcor[1] - t1)
    ycor.append(ycor[2] - B2 + twx / 2)
    zcor.append(zcor[2])
    ycor.append(-(B1 + Top) + (Bot + B3 + twx/2))
    zcor.append(zcor[3] - H)
    ycor.append(ycor[4] - twx/2 + B4)
    zcor.append(zcor[4])
    ycor.append(ycor[5])
    zcor.append(zcor[5] - t2)
    ycor.append(-(B1 + Top) + (Bot + B3))
    zcor.append(zcor[6])
    # Reverse
    ycor.reverse()
    zcor.reverse()
    # Remove Origin
    ycor.pop(0)
    zcor.pop(0)
    # All Cell
    ycoAll = ycol + ycor
    zcoAll = zcol + zcor
    # Return
    outer = defaultdict(list)
    inner = defaultdict(list)
    comp = defaultdict(list)
    outer[0] = ycoAll
    outer[1] = zcoAll
    return outer, inner, comp

def composite_steel_box(vSize, slab, refSize) :
    # Variable Initialization
    B1, B2, B3, B4, B5, B6, H, t1, t2, tw1, tw2 = vSize
    Bc, tc, Hh = slab
    Sg, Top, Bot = refSize
    twx1 = tw1 * math.sqrt(H ** 2 + ((Bot + B4) - (Top + B1)) ** 2) / H
    twx2 = tw2 * math.sqrt(H ** 2 + ((Top + B1 + B2) - (Bot + B4 + B5)) ** 2) / H
    # Outer Cell - Left Side
    ycol = [(B2 / 2 + B1 + Top) - (Sg + Bc / 2)]
    zcol = [-(tc + Hh)]
    ycol.append(ycol[0] - B2 / 2 - B1)
    zcol.append(zcol[0])
    ycol.append(ycol[1])
    zcol.append(zcol[1] - t1)
    ycol.append(ycol[2] + B1 - twx1)
    zcol.append(zcol[2])
    ycol.append((B5 / 2 + B4 + Bot) - (Sg + Bc / 2) - B5 / 2 - twx1)
    zcol.append(zcol[3] - H)
    ycol.append(ycol[4] - B4 + twx1)
    zcol.append(zcol[4])
    ycol.append(ycol[5])
    zcol.append(zcol[5] - t2)
    ycol.append((B5 / 2 + B4 + Bot) - (Sg + Bc / 2))
    zcol.append(zcol[6])
    # Outer Cell - Right Side
    ycor = [(B2 / 2 + B1 + Top) - (Sg + Bc / 2)]
    zcor = [-(tc + Hh)]
    ycor.append(ycor[0] + B2 / 2 + B3)
    zcor.append(zcor[0])
    ycor.append(ycor[1])
    zcor.append(zcor[1] - t1)
    ycor.append(ycor[2] - B3 + twx2)
    zcor.append(zcor[2])
    ycor.append((B5 / 2 + B4 + Bot) - (Sg + Bc / 2) + B5 / 2 + twx2)
    zcor.append(zcor[3] - H)
    ycor.append(ycor[4] + B6 - twx2)
    zcor.append(zcor[4])
    ycor.append(ycor[5])
    zcor.append(zcor[5] - t2) 
    ycor.append((B5 / 2 + B4 + Bot) - (Sg + Bc / 2))
    zcor.append(zcor[6])
    # Inner Cell - Left Side
    ycil = [(B2 / 2 + B1 + Top) - (Sg + Bc / 2)]
    zcil = [zcol[0] - t1]
    ycil.append(ycil[0] - B2 / 2)
    zcil.append(zcil[0])
    ycil.append((B5 / 2 + B4 + Bot) - (Sg + Bc / 2) - B5 / 2)
    zcil.append(zcil[1] - H)
    ycil.append((B5 / 2 + B4 + Bot) - (Sg + Bc / 2))
    zcil.append(zcil[2])
    # Inner Cell - Right Side
    ycir = [(B2 / 2 + B1 + Top) - (Sg + Bc / 2)]
    zcir = [zcor[0] - t1]
    ycir.append(ycir[0] + B2 / 2)
    zcir.append(zcir[0])
    ycir.append((B5 / 2 + B4 + Bot) - (Sg + Bc / 2) + B5 / 2)
    zcir.append(zcir[1] - H)
    ycir.append((B5 / 2 + B4 + Bot) - (Sg + Bc / 2))
    zcir.append(zcir[2])
    # Reverse
    ycor.reverse()
    zcor.reverse()
    ycil.reverse()
    zcil.reverse()
    # Remove Origin
    ycor.pop(0)
    zcor.pop(0)
    ycil.pop(0)
    zcil.pop(0)
    # All Cell
    ycoAll = ycol + ycor
    zcoAll = zcol + zcor
    yciAll = ycir + ycil
    zciAll = zcir + zcil
    # Slab
    slab_result = slab_coordinates(slab)
    # Return
    outer = defaultdict(list)
    inner = defaultdict(list)
    comp = defaultdict(list)
    outer[0] = ycoAll
    outer[1] = zcoAll
    inner[0] = yciAll
    inner[1] = zciAll
    comp[0] = slab_result[0]
    comp[1] = slab_result[1]
    return outer, inner, comp

def composite_steel_i(vSize, slab, refSize):
    # Variable Initialization
    B1, B2, B3, B4, H, t1, t2, tw = vSize
    Bc, tc, Hh = slab
    Sg, Top, Bot = refSize
    twx = tw * math.sqrt(H ** 2 + ((Bot + B3) - (Top + B1)) ** 2) / H
    # Outer Cell - Left Side
    ycol = [-(Bc / 2 + Sg) + (Top + B1)]
    zcol = [-(tc + Hh)]
    ycol.append(ycol[0] - B1)
    zcol.append(zcol[0])
    ycol.append(ycol[1])
    zcol.append(zcol[1] - t1)
    ycol.append(ycol[2] + B1 - twx / 2)
    zcol.append(zcol[2])
    ycol.append(-(Bc / 2 + Sg) + (Bot + B3 - twx / 2))
    zcol.append(zcol[3] - H)
    ycol.append(ycol[4] - B3 + twx / 2)
    zcol.append(zcol[4])
    ycol.append(ycol[5])
    zcol.append(zcol[5] - t2)
    ycol.append(-(Bc / 2 + Sg) + (Bot + B3))
    zcol.append(zcol[6])
    # Outer Cell - Right Side
    ycor = [-(Bc / 2 + Sg) + (Top + B1)]
    zcor = [-(tc + Hh)]
    ycor.append(ycor[0] + B2)
    zcor.append(zcor[0])
    ycor.append(ycor[1])
    zcor.append(zcor[1] - t1)
    ycor.append(ycor[2] - B2 + twx / 2)
    zcor.append(zcor[2])
    ycor.append(-(Bc / 2 + Sg) + (Bot + B3 + twx/2))
    zcor.append(zcor[3] - H)
    ycor.append(ycor[4] - twx/2 + B4)
    zcor.append(zcor[4])
    ycor.append(ycor[5])
    zcor.append(zcor[5] - t2)
    ycor.append(-(Bc / 2 + Sg) + (Bot + B3))
    zcor.append(zcor[6])
    # Reverse
    ycor.reverse()
    zcor.reverse()
    # Remove Origin
    ycor.pop(0)
    zcor.pop(0)
    # All Cell
    ycoAll = ycol + ycor
    zcoAll = zcol + zcor
    # Slab
    slab_result = slab_coordinates(slab)
    # Return
    outer = defaultdict(list)
    inner = defaultdict(list)
    comp = defaultdict(list)
    outer[0] = ycoAll
    outer[1] = zcoAll
    comp[0] = slab_result[0]
    comp[1] = slab_result[1]
    return outer, inner, comp

def composite_steel_tub(vSize, slab, refSize) :
    # Variable Initialization
    B1, B2, B3, B4, B5, B6, H, t1, t2, tw1, tw2, Bf1, Bf2 = vSize
    Bc, tc, Hh = slab
    Sg, Top, Bot = refSize
    twx1 = tw1 * math.sqrt(H ** 2 + ((Bot + B4) - (Top + Bf1)) ** 2) / H
    twx2 = tw2 * math.sqrt(H ** 2 + ((Top + B1 + B2 + B3 - Bf2) - (Bot + B4 + B5)) ** 2) / H
    # Outer Cell - Left Side
    ycol = [(Bot + B4 + B5 / 2) - (Sg + Bc / 2)]
    zcol = [-(tc + Hh + t1 + H)]
    ycol.append(ycol[0] - B5 / 2)
    zcol.append(zcol[0])
    ycol.append((Top + Bf1) - (Sg + Bc / 2))
    zcol.append(zcol[1] + H)
    ycol.append(ycol[2] + (B1 - Bf1))
    zcol.append(zcol[2])
    ycol.append(ycol[3])
    zcol.append(zcol[3] + t1)
    ycol.append(ycol[4] - B1)
    zcol.append(zcol[4])
    ycol.append(ycol[5])
    zcol.append(zcol[5] - t1)
    ycol.append(ycol[6] + Bf1 - twx1)
    zcol.append(zcol[6])
    ycol.append(ycol[0] - B5 / 2 - twx1)
    zcol.append(zcol[7] - H)
    ycol.append(ycol[0] - B5 / 2 - B4)
    zcol.append(zcol[8])
    ycol.append(ycol[9])
    zcol.append(zcol[9] - t2)
    ycol.append(ycol[0])
    zcol.append(zcol[10])
    # Outer Cell - Right Side
    ycor = [(Bot + B4 + B5 / 2) - (Sg + Bc / 2)]
    zcor = [-(tc + Hh + t1 + H)]
    ycor.append(ycor[0] + B5 / 2)
    zcor.append(zcor[0])
    ycor.append((Top + B1 + B2 + B3 - Bf2) - (Sg + Bc / 2))
    zcor.append(zcor[1] + H)
    ycor.append(ycor[2] - (B3 - Bf2))
    zcor.append(zcor[2])
    ycor.append(ycor[3])
    zcor.append(zcor[3] + t1)
    ycor.append(ycor[4] + B3)
    zcor.append(zcor[4])
    ycor.append(ycor[5])
    zcor.append(zcor[5] - t1)
    ycor.append(ycor[6] - Bf2 + twx2)
    zcor.append(zcor[6])
    ycor.append(ycor[0] + B5 / 2 + twx2)
    zcor.append(zcor[7] - H)
    ycor.append(ycor[0] + B5 / 2 + B6)
    zcor.append(zcor[8])
    ycor.append(ycor[9])
    zcor.append(zcor[9] - t2)
    ycor.append(ycor[0])
    zcor.append(zcor[10])
    # Reverse
    ycor.reverse()
    zcor.reverse()
    # Remove Origin
    ycor.pop(0)
    zcor.pop(0)
    # All Cell
    ycoAll = ycol + ycor
    zcoAll = zcol + zcor
    # Slab
    slab_result = slab_coordinates(slab)
    # Return
    outer = defaultdict(list)
    inner = defaultdict(list)
    comp = defaultdict(list)
    outer[0] = ycoAll
    outer[1] = zcoAll
    comp[0] = slab_result[0]
    comp[1] = slab_result[1]
    return outer, inner, comp

def psc_1cell(vSizeA, vSizeB, vSizeC, vSizeD, joint):
    # Variable Initialization
    HO10, HO20, HO21, HO22, HO30, HO31 = vSizeA
    BO10, BO11, BO12, BO20, BO21, BO30 = vSizeB
    HI10, HI20, HI21, HI22, HI30, HI31, HI40, HI41, HI42, HI50 = vSizeC
    BI10, BI11, BI12, BI21, BI30, BI31, BI32 = vSizeD
    JO1, JO2, JO3, JI1, JI2, JI3, JI4, JI5 = joint
    # Height Calculation
    heightO = HO10 + HO20 + HO30
    heightI = HI10 + HI20 + HI30 + HI40 + HI50
    heightM = max(heightO, heightI)
    # Outer Cell_Left Side
    ycol = [0]
    zcol = [heightI - heightM]
    ycol.append(-(BO10 + BO20 + BO30))
    zcol.append(heightO - heightM)
    ycol.append(ycol[1])
    zcol.append(zcol[1] - HO10)
    ycol.append(ycol[2] + BO10)
    zcol.append(zcol[2] - HO20)
    ycol.append(ycol[3] + BO20)
    zcol.append(zcol[3] - HO30)
    ycol.append(ycol[4] + BO30)
    zcol.append(zcol[4])
    # Added Vertex
    addedVertex = 0
    # Outer joint 1
    if JO1:
        ycol.insert(3, ycol[2] + BO11)
        zcol.insert(3, zcol[2] - HO21)
        addedVertex += 1
    # Outer joint 2
    if JO2:
        ycol.insert(3 + addedVertex, ycol[2] + BO12)
        zcol.insert(3 + addedVertex, zcol[2] - HO22)
        addedVertex += 1
    # Outer joint 3
    if JO3:
        ycol.insert(4 + addedVertex, ycol[4 + addedVertex] - BO21)
        zcol.insert(4 + addedVertex, zcol[4 + addedVertex] + HO31)
        addedVertex += 1
    # Inner Cell
    ycil = [ycol[0], ycol[0] - BI10, ycol[-1] - BI30, ycol[-1]]
    zcil = [zcol[0] - HI10, zcol[0] - HI10 - HI20,  zcol[0] - HI10 - HI20 - HI30, zcol[0] - HI10 - HI20 - HI30 - HI40]
    # Added Vertex
    addedVertex = 0
    # Inner joint 1
    if JI1:
        ycil.insert(1, ycil[0] - BI11)
        zcil.insert(1, zcil[0] - HI21)
        addedVertex += 1
    # Inner joint 2
    if JI2:
        ycil.insert(1 + addedVertex, ycil[0] - BI12)
        zcil.insert(1 + addedVertex, zcil[0] - HI22)
        addedVertex += 1
    # Inner joint 3
    if JI3:
        ycil.insert(2 + addedVertex, ycil[3 + addedVertex] - BI21)
        zcil.insert(2 + addedVertex, zcil[1 + addedVertex] - HI31)
        addedVertex += 1
    # Inner joint 4
    if JI4:
        ycil.insert(3 + addedVertex, ycil[-1] - BI32)
        zcil.insert(3 + addedVertex, zcil[-1] + HI42)
        addedVertex += 1
    # Inner joint 5
    if JI5:
        ycil.insert(3 + addedVertex, ycil[-1] - BI31)
        zcil.insert(3 + addedVertex, zcil[-1] + HI41)
        addedVertex += 1
    # Outer Cell_Right Side
    ycor = [-x for x in ycol]
    zcor = zcol.copy()
    # Inner Cell_Right Side
    ycir = [-x for x in ycil]
    zcir = zcil.copy()
    # Reverse
    ycor.reverse()
    zcor.reverse()
    ycil.reverse()
    zcil.reverse()
    # Remove Origin
    ycor.pop(0)
    zcor.pop(0)
    ycil.pop(0)
    zcil.pop(0)
    # All Cell
    ycoAll = ycol + ycor
    zcoAll = zcol + zcor
    yciAll = ycir + ycil
    zciAll = zcir + zcil
    # Return
    outer = defaultdict(list)
    inner = defaultdict(list)
    comp = defaultdict(list)
    outer[0] = ycoAll
    outer[1] = zcoAll
    inner[0] = yciAll
    inner[1] = zciAll
    return outer, inner, comp

def psc_2cell(vSizeA, vSizeB, vSizeC, vSizeD, joint):
    # Variable Initialization
    HO10, HO20, HO21, HO22, HO30, HO31 = vSizeA
    BO10, BO11, BO12, BO20, BO21, BO30 = vSizeB
    HI10, HI20, HI21, HI22, HI30, HI31, HI40, HI41, HI42, HI50 = vSizeC
    BI10, BI11, BI12, BI21, BI30, BI31, BI32, BI40 = vSizeD
    JO1, JO2, JO3, JI1, JI2, JI3, JI4, JI5 = joint
    # Height Calculation
    heightO = HO10 + HO20 + HO30
    heightI = HI10 + HI20 + HI30 + HI40 + HI50
    heightM = max(heightO, heightI)
    # Outer Cell_Left Side
    ycol = [0]
    zcol = [heightI - heightM]
    ycol.append(-(BO10 + BO20 + BO30))
    zcol.append(heightO - heightM)
    ycol.append(ycol[1])
    zcol.append(zcol[1] - HO10)
    ycol.append(ycol[2] + BO10)
    zcol.append(zcol[2] - HO20)
    ycol.append(ycol[3] + BO20)
    zcol.append(zcol[3] - HO30)
    ycol.append(ycol[4] + BO30)
    zcol.append(zcol[4])
    # Added Vertex
    addedVertex = 0
    # Outer joint 1
    if JO1:
        ycol.insert(3, ycol[2] + BO11)
        zcol.insert(3, zcol[2] - HO21)
        addedVertex += 1
    # Outer joint 2
    if JO2:
        ycol.insert(3 + addedVertex, ycol[2] + BO12)
        zcol.insert(3 + addedVertex, zcol[2] - HO22)
        addedVertex += 1
    # Outer joint 3
    if JO3:
        ycol.insert(4 + addedVertex, ycol[4 + addedVertex] - BO21)
        zcol.insert(4 + addedVertex, zcol[4 + addedVertex] + HO31)
        addedVertex += 1
    # Inner Cell
    ycill = [ycol[0] - BI40, ycol[0] - BI10, ycol[-1] - BI30, ycol[-1] - BI40]
    zcill = [zcol[0] - HI10, zcol[0] - HI10 - HI20, zcol[0] - HI10 - HI20 - HI30, zcol[-1] + HI50]
    # Added Vertex
    addedVertex = 0
    # Inner joint 1
    if JI1:
        ycill.insert(1, ycol[0] - BI11)
        zcill.insert(1, zcill[0] - HI21)
        addedVertex += 1
    # Inner joint 2
    if JI2:
        ycill.insert(1 + addedVertex, ycol[0] - BI12)
        zcill.insert(1 + addedVertex, zcill[0] - HI22)
        addedVertex += 1
    # Inner joint 3
    if JI3:
        ycill.insert(2 + addedVertex, ycol[0] - BI21)
        zcill.insert(2 + addedVertex, zcill[1 + addedVertex] - HI31)
        addedVertex += 1
    # Inner joint 4
    if JI4:
        ycill.insert(3 + addedVertex, ycol[0] - BI32)
        zcill.insert(3 + addedVertex, zcill[-1] + HI42)
        addedVertex += 1
    # Inner joint 5
    if JI5:
        ycill.insert(3 + addedVertex, ycol[0] - BI31)
        zcill.insert(3 + addedVertex, zcill[-1] + HI41)
        addedVertex += 1
    # Left Inner Cell_Right Side
    ycilr = [ycill[0], ycill[-1]]
    zcilr = [zcill[0], zcill[-1]]
    # Outer Cell_Right Side
    ycor = [-x for x in ycol]
    zcor = zcol.copy()
    # Right Inner Cell_Left Side
    ycirl = [-x for x in ycilr]
    zcirl = zcilr.copy()
    # Right Inner Cell_Right Side
    ycirr = [-x for x in ycill]
    zcirr = zcill.copy()
    # Reverse
    ycor.reverse()
    zcor.reverse()
    ycill.reverse()
    zcill.reverse()
    ycirl.reverse()
    zcirl.reverse()
    # Remove Origin
    ycor.pop(0)
    zcor.pop(0)
    ycill.pop(0)
    zcill.pop(0)
    ycirl.pop(0)
    zcirl.pop(0)
    # All Cell
    ycoAll = ycol + ycor
    zcoAll = zcol + zcor
    ycilAll = ycilr + ycill
    zcilAll = zcilr + zcill
    ycirAll = ycirr + ycirl
    zcirAll = zcirr + zcirl
    # Return
    outer = defaultdict(list)
    inner = defaultdict(list)
    comp = defaultdict(list)
    outer[0] = ycoAll
    outer[1] = zcoAll
    inner[0] = ycilAll
    inner[1] = zcilAll
    inner[2] = ycirAll
    inner[3] = zcirAll
    return outer, inner, comp

def psc_I(vSizeA, vSizeB, vSizeC, vSizeD, joint) :
    # Variable Initialization
    H10, HL10, HL20, HL21, HL22, HL30, HL40, HL41, HL42, HL50 = vSizeA
    BL10, BL20, BL21, BL22, BL40, BL41, BL42 = vSizeB
    HR10, HR20, HR21, HR22, HR30, HR40, HR41, HR42, HR50 = vSizeC
    BR10, BR20, BR21, BR22, BR40, BR41, BR42 = vSizeD
    J1, JL1, JL2, JL3, JL4, JR1, JR2, JR3, JR4 = joint
    # Height Calculation
    heightL = HL10 + HL20 + HL30 + HL40 + HL50
    heightR = HR10 + HR20 + HR30 + HR40 + HR50
    heightC = 0
    if J1 :
        heightC = H10
    else :
        if heightR > heightL :
            heightC = BL20 * (heightR - heightL) / (BL20 + BR20) + heightL
        elif heightR < heightL :
            heightC = BR20 * (heightL - heightR) / (BL20 + BR20) + heightR
        elif heightR == heightL :
            heightC = (heightL + heightR) / 2
    heightM = max(heightL, heightR, heightC)
    # Outer Cell_Left Side
    ycol = [0]
    zcol = [heightC - heightM]
    ycol.append(-BL20)
    zcol.append(heightL - heightM)
    ycol.append(ycol[1])
    zcol.append(zcol[1] - HL10)
    ycol.append(-BL10)
    zcol.append(zcol[2] - HL20)
    ycol.append(ycol[3])
    zcol.append(zcol[3] - HL30)
    ycol.append(-BL40)
    zcol.append(zcol[4] - HL40)
    ycol.append(ycol[5])
    zcol.append(zcol[5] - HL50)
    ycol.append(0)
    zcol.append(-heightM)
    # Added Vertex
    addedVertex = 0
    # Left joint 1
    if JL1:
        ycol.insert(3, ycol[2] + BL21)
        zcol.insert(3, zcol[2] - HL21)
        addedVertex += 1
    # Left joint 2
    if JL2:
        ycol.insert(3 + addedVertex, ycol[2] + BL22)
        zcol.insert(3 + addedVertex, zcol[2] - HL22)
        addedVertex += 1
    # Left joint 3
    if JL3:
        ycol.insert(5 + addedVertex, ycol[5 + addedVertex] + BL42)
        zcol.insert(5 + addedVertex, zcol[5 + addedVertex] + HL42)
        addedVertex += 1
    # Left joint 4
    if JL4:
        ycol.insert(5 + addedVertex, ycol[5 + addedVertex] + BL41)
        zcol.insert(5 + addedVertex, zcol[5 + addedVertex] + HL41)
        addedVertex += 1
    # Outer Cell_Right Side
    ycor = [0]
    zcor = [heightC - heightM]
    ycor.append(BR20)
    zcor.append(heightR - heightM)
    ycor.append(ycor[1])
    zcor.append(zcor[1] - HR10)
    ycor.append(BR10)
    zcor.append(zcor[2] - HR20)
    ycor.append(ycor[3])
    zcor.append(zcor[3] - HR30)
    ycor.append(BR40)
    zcor.append(zcor[4] - HR40)
    ycor.append(ycor[5])
    zcor.append(zcor[5] - HR50)
    ycor.append(0)
    zcor.append(-heightM)
    # Added Vertex
    addedVertex = 0
    # Right joint 1
    if JR1:
        ycor.insert(3, ycor[2] - BR21)
        zcor.insert(3, zcor[2] - HR21)
        addedVertex += 1
    # Right joint 2
    if JR2:
        ycor.insert(3 + addedVertex, ycor[2] - BR22)
        zcor.insert(3 + addedVertex, zcor[2] - HR22)
        addedVertex += 1
    # Right joint 3
    if JR3:
        ycor.insert(5 + addedVertex, ycor[5 + addedVertex] - BR42)
        zcor.insert(5 + addedVertex, zcor[5 + addedVertex] + HR42)
        addedVertex += 1
    # Right joint 4
    if JR4:
        ycor.insert(5 + addedVertex, ycor[5 + addedVertex] - BR41)
        zcor.insert(5 + addedVertex, zcor[5 + addedVertex] + HR41)
        addedVertex += 1
    # Reverse
    ycor.reverse()
    zcor.reverse()
    # Remove Origin
    ycor.pop(0)
    zcor.pop(0)
    # All Cell
    ycoAll = ycol + ycor
    zcoAll = zcol + zcor
    # Return
    outer = defaultdict(list)
    inner = defaultdict(list)
    comp = defaultdict(list)
    outer[0] = ycoAll
    outer[1] = zcoAll
    return outer, inner, comp

def psc_T(vSizeA, vSizeB, vSizeC, vSizeD, joint) :
    # Variable Initialization
    H10, HL10, HL20, HL30, BL10, BL20, BL30, BL40 = vSizeA
    HL21, HL22, HL31, HL32, BL21, BL22, BL31, BL32 = vSizeB
    HR10, HR20, HR30, BR10, BR20, BR30, BR40 = vSizeC
    HR21, HR22, HR31, HR32, BR21, BR22, BR31, BR32 = vSizeD
    J1, JL1, JL2, JL3, JL4, JR1, JR2, JR3, JR4 = joint
    # Height Calculation
    heightL = HL10 + HL20 + HL30
    heightR = HR10 + HR20 + HR30
    heightC = 0
    if J1 :
        heightC = H10
    else :
        if heightR > heightL :
            heightC = BL40 * (heightR - heightL) / (BL40 + BR40) + heightL
        elif heightR < heightL :
            heightC = BR40 * (heightL - heightR) / (BL40 + BR40) + heightR
        elif heightR == heightL :
            heightC = (heightL + heightR) / 2
    heightM = max(heightL, heightR, heightC)
    # Outer Cell_Left Side
    ycol = [0]
    zcol = [heightC - heightM]
    ycol.append(-BL40)
    zcol.append(heightL - heightM)
    ycol.append(-(BL10 + BL20 + BL30)) 
    zcol.append(zcol[1] - HL10)
    ycol.append(-(BL10 + BL20))
    zcol.append(zcol[2] - HL20)
    ycol.append(-BL10)
    zcol.append(zcol[3] - HL30)
    ycol.append(0)
    zcol.append(-heightM)
    # Added Vertex
    addedVertex = 0
    # Left joint 1
    if JL1:
        ycol.insert(3, ycol[2] + BL31)
        zcol.insert(3, zcol[2] - HL21)
        addedVertex += 1
    # Left joint 2
    if JL2:
        ycol.insert(3 + addedVertex, ycol[2] + BL32)
        zcol.insert(3 + addedVertex, zcol[2] - HL22)
        addedVertex += 1
    # Left joint 3
    if JL3:
        ycol.insert(4 + addedVertex, ycol[4 + addedVertex] - BL21)
        zcol.insert(4 + addedVertex, zcol[4 + addedVertex] + HL31)
        addedVertex += 1
    # Left joint 4
    if JL4:
        ycol.insert(4 + addedVertex, ycol[4 + addedVertex] - BL22)
        zcol.insert(4 + addedVertex, zcol[4 + addedVertex] + HL32)
        addedVertex += 1
    # Outer Cell_Right Side
    ycor = [0]
    zcor = [heightC - heightM]
    ycor.append(BR40)
    zcor.append(heightR - heightM)
    ycor.append(BR10 + BR20 + BR30)
    zcor.append(zcor[1] - HR10)
    ycor.append(BR10 + BR20)
    zcor.append(zcor[2] - HR20)
    ycor.append(BR10)
    zcor.append(zcor[3] - HR30)
    ycor.append(0)
    zcor.append(-heightM)
    # Added Vertex
    addedVertex = 0
    # Right joint 1
    if JR1:
        ycor.insert(3, ycor[2] - BR31)
        zcor.insert(3, zcor[2] - HR21)
        addedVertex += 1
    # Right joint 2
    if JR2:
        ycor.insert(3 + addedVertex, ycor[2] - BR32)
        zcor.insert(3 + addedVertex, zcor[2] - HR22)
        addedVertex += 1
    # Right joint 3
    if JR3:
        ycor.insert(4 + addedVertex, ycor[4 + addedVertex] + BR21)
        zcor.insert(4 + addedVertex, zcor[4 + addedVertex] + HR31)
        addedVertex += 1
    # Right joint 4
    if JR4:
        ycor.insert(4 + addedVertex, ycor[4 + addedVertex] + BR22)
        zcor.insert(4 + addedVertex, zcor[4 + addedVertex] + HR32)
        addedVertex += 1
    # Reverse
    ycor.reverse()
    zcor.reverse()
    # Remove Origin
    ycor.pop(0)
    zcor.pop(0)
    # All Cell
    ycoAll = ycol + ycor
    zcoAll = zcol + zcor
    # Return
    outer = defaultdict(list)
    inner = defaultdict(list)
    comp = defaultdict(list)
    outer[0] = ycoAll
    outer[1] = zcoAll
    return outer, inner, comp

def slab_coordinates(slab) :
    # Variable Initialization
    Bc, tc, _ = slab
    # Coordinates
    yco = [0, -Bc / 2, -Bc / 2, 0, Bc / 2, Bc / 2, 0]
    zco = [0, 0, -tc, -tc, -tc, 0, 0]
    # Return
    slab_coordinates_dict = defaultdict(list)
    slab_coordinates_dict[0] = yco
    slab_coordinates_dict[1] = zco
    return slab_coordinates_dict