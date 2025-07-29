import numpy as np

from moapy.plugins.temperature_gradient.eurocode.data_input import SurfaceType


# Eurocode 1 - Actions on structures - Part 1-5: General actions - Thermal actions
def data_group(group, sub_group=2):
    # 1a-Steel deck on steel girders
    data_type_1 = {
        "0": {"T1_h": 30, "T2_h": 16, "T3_h": 6, "T4_h": 3, "T1_c": -8},
        "20": {"T1_h": 27, "T2_h": 15, "T3_h": 9, "T4_h": 5, "T1_c": -6},
        "40": {"T1_h": 24, "T2_h": 14, "T3_h": 8, "T4_h": 4, "T1_c": -6},
    }

    # 1b-Steel deck on steel truss or plate girders
    data_type_2 = {
        "0": {"T1_h": 25, "T1_c": -6},
        "20": {"T1_h": 23, "T1_c": -5},
        "40": {"T1_h": 21, "T1_c": -5},
    }

    # 2-Composite decks
    data_type_31 = {
        "200": {"T1_h": 16.5, "T1_c": -5.9},
        "300": {"T1_h": 18.5, "T1_c": -9.0},
    }

    data_type_32 = {
        "200": {
            "0": {"T1_h": 23.0, "T1_c": -5.9},
            "50": {"T1_h": 18.0, "T1_c": -4.4},
            "100": {"T1_h": 13.0, "T1_c": -3.5},
            "150": {"T1_h": 10.5, "T1_c": -2.3},
            "200": {"T1_h": 8.5, "T1_c": -1.6},
        },
        "300": {
            "0": {"T1_h": 26.5, "T1_c": -9.0},
            "50": {"T1_h": 20.5, "T1_c": -6.8},
            "100": {"T1_h": 16.0, "T1_c": -5.0},
            "150": {"T1_h": 12.5, "T1_c": -3.7},
            "200": {"T1_h": 10.0, "T1_c": -2.7},
        },
    }

    # 3-Concrete decks
    data_type_41 = {
        "200" : {"T1_h": 12.0, "T2_h": 5.0, "T3_h": 0.1, "T1_c": -4.7,  "T2_c": -1.7, "T3_c":  0.0, "T4_c": -0.7},
        "400" : {"T1_h": 15.2, "T2_h": 4.4, "T3_h": 1.2, "T1_c": -9.0,  "T2_c": -3.5, "T3_c": -0.4, "T4_c": -2.9},
        "600" : {"T1_h": 15.2, "T2_h": 4.0, "T3_h": 1.4, "T1_c": -11.8, "T2_c": -4.0, "T3_c": -0.9, "T4_c": -4.6},
        "800" : {"T1_h": 15.4, "T2_h": 4.0, "T3_h": 2.0, "T1_c": -12.8, "T2_c": -3.3, "T3_c": -0.9, "T4_c": -5.6},
        "1000": {"T1_h": 15.4, "T2_h": 4.0, "T3_h": 2.0, "T1_c": -13.4, "T2_c": -3.0, "T3_c": -0.9, "T4_c": -6.4},
        "1500": {"T1_h": 15.4, "T2_h": 4.5, "T3_h": 2.0, "T1_c": -13.7, "T2_c": -1.0, "T3_c": -0.6, "T4_c": -6.7}
    }

    data_type_42 = {
        "200": {
            "0"  : {"T1_h": 19.5, "T2_h": 8.5, "T3_h": 0.0, "T1_c": -4.7, "T2_c": -1.7, "T3_c":  0.0, "T4_c": -0.7},
            "50" : {"T1_h": 13.2, "T2_h": 4.9, "T3_h": 0.3, "T1_c": -3.1, "T2_c": -1.0, "T3_c": -0.2, "T4_c": -1.2},
            "100": {"T1_h": 8.5,  "T2_h": 3.5, "T3_h": 0.5, "T1_c": -2.0, "T2_c": -0.5, "T3_c": -0.5, "T4_c": -1.5},
            "150": {"T1_h": 5.6,  "T2_h": 2.5, "T3_h": 0.2, "T1_c": -1.1, "T2_c": -0.3, "T3_c": -0.7, "T4_c": -1.7},
            "200": {"T1_h": 3.7,  "T2_h": 2.0, "T3_h": 0.5, "T1_c": -0.5, "T2_c": -0.2, "T3_c": -1.0, "T4_c": -1.8}
        },
        "400": {
            "0"  : {"T1_h": 23.6, "T2_h": 6.5, "T3_h": 1.0, "T1_c": -9.0, "T2_c": -3.5, "T3_c": -0.4, "T4_c": -2.9},
            "50" : {"T1_h": 17.2, "T2_h": 4.6, "T3_h": 1.4, "T1_c": -6.4, "T2_c": -2.3, "T3_c": -0.6, "T4_c": -3.2},
            "100": {"T1_h": 12.0, "T2_h": 3.0, "T3_h": 1.5, "T1_c": -4.5, "T2_c": -1.4, "T3_c": -1.0, "T4_c": -3.5},
            "150": {"T1_h": 8.5,  "T2_h": 2.0, "T3_h": 1.2, "T1_c": -3.2, "T2_c": -0.9, "T3_c": -1.4, "T4_c": -3.8},
            "200": {"T1_h": 6.2,  "T2_h": 1.3, "T3_h": 1.0, "T1_c": -2.2, "T2_c": -0.5, "T3_c": -1.9, "T4_c": -4.0}
        },
        "600": {
            "0"  : {"T1_h": 23.6, "T2_h": 6.0, "T3_h": 1.4, "T1_c": -11.8, "T2_c": -4.0, "T3_c": -0.9, "T4_c": -4.6},
            "50" : {"T1_h": 17.6, "T2_h": 4.0, "T3_h": 1.8, "T1_c": -8.7,  "T2_c": -2.7, "T3_c": -1.2, "T4_c": -4.9},
            "100": {"T1_h": 13.0, "T2_h": 3.0, "T3_h": 2.0, "T1_c": -6.5,  "T2_c": -1.8, "T3_c": -1.5, "T4_c": -5.0},
            "150": {"T1_h": 9.7,  "T2_h": 2.2, "T3_h": 1.7, "T1_c": -4.9,  "T2_c": -1.1, "T3_c": -1.7, "T4_c": -5.1},
            "200": {"T1_h": 7.2,  "T2_h": 1.5, "T3_h": 1.5, "T1_c": -3.6,  "T2_c": -0.6, "T3_c": -1.9, "T4_c": -5.1}
        },
        "800": {
            "0"  : {"T1_h": 23.6, "T2_h": 5.0, "T3_h": 1.4, "T1_c": -12.8, "T2_c": -3.3, "T3_c": -0.9, "T4_c": -5.6},
            "50" : {"T1_h": 17.8, "T2_h": 4.0, "T3_h": 2.1, "T1_c": -9.8,  "T2_c": -2.4, "T3_c": -1.2, "T4_c": -5.8},
            "100": {"T1_h": 13.5, "T2_h": 3.0, "T3_h": 2.5, "T1_c": -7.6,  "T2_c": -1.7, "T3_c": -1.5, "T4_c": -6.0},
            "150": {"T1_h": 10.0, "T2_h": 2.5, "T3_h": 2.0, "T1_c": -5.8,  "T2_c": -1.3, "T3_c": -1.7, "T4_c": -6.2},
            "200": {"T1_h": 7.5,  "T2_h": 2.1, "T3_h": 1.5, "T1_c": -4.5,  "T2_c": -1.0, "T3_c": -1.9, "T4_c": -6.0}
        },
        "1000": {
            "0"  : {"T1_h": 23.6, "T2_h": 5.0, "T3_h": 1.4, "T1_c": -13.4, "T2_c": -3.0, "T3_c": -0.9, "T4_c": -6.4},
            "50" : {"T1_h": 17.8, "T2_h": 4.0, "T3_h": 2.1, "T1_c": -10.3, "T2_c": -2.1, "T3_c": -1.2, "T4_c": -6.3},
            "100": {"T1_h": 13.5, "T2_h": 3.0, "T3_h": 2.5, "T1_c": -8.0,  "T2_c": -1.5, "T3_c": -1.5, "T4_c": -6.3},
            "150": {"T1_h": 10.0, "T2_h": 2.5, "T3_h": 2.0, "T1_c": -6.2,  "T2_c": -1.1, "T3_c": -1.7, "T4_c": -6.2},
            "200": {"T1_h": 7.5,  "T2_h": 2.1, "T3_h": 1.5, "T1_c": -4.8,  "T2_c": -0.9, "T3_c": -1.9, "T4_c": -5.8}
        },
        "1500": {
            "0"  : {"T1_h": 23.6, "T2_h": 5.0, "T3_h": 1.4, "T1_c": -13.7, "T2_c": -1.0, "T3_c": -0.6, "T4_c": -6.7},
            "50" : {"T1_h": 17.8, "T2_h": 4.0, "T3_h": 2.1, "T1_c": -10.6, "T2_c": -0.7, "T3_c": -0.8, "T4_c": -6.6},
            "100": {"T1_h": 13.5, "T2_h": 3.0, "T3_h": 2.5, "T1_c": -8.4,  "T2_c": -0.5, "T3_c": -1.0, "T4_c": -6.5},
            "150": {"T1_h": 10.0, "T2_h": 2.5, "T3_h": 2.0, "T1_c": -6.5,  "T2_c": -0.4, "T3_c": -1.1, "T4_c": -6.2},
            "200": {"T1_h": 7.5,  "T2_h": 2.1, "T3_h": 1.5, "T1_c": -5.0,  "T2_c": -0.3, "T3_c": -1.2, "T4_c": -5.6}
        }
    }

    if group == 1:
        return data_type_1
    elif group == 2:
        return data_type_2
    elif group == 3:
        if sub_group == 1:
            return data_type_31
        elif sub_group == 2:
            return data_type_32
    elif group == 4:
        if sub_group == 1:
            return data_type_41
        elif sub_group == 2:
            return data_type_42
    else:
        return None


# Function to interpolate between two values
def linear_interpolation(lower_value, upper_value, lower_key, upper_key, input_value):
    interpolated_value = {}
    for param in lower_value:
        lower_param_value = lower_value[param]
        upper_param_value = upper_value[param]
        interpolated_value[param] = lower_param_value + (
            upper_param_value - lower_param_value
        ) * ((input_value - lower_key) / (upper_key - lower_key))
    return interpolated_value


# Function to Data Merge
def merge_and_interpolate(A1, A2, B1, B2):
    # Merge A1 and B1 arrays and sort them in descending order
    C = sorted(set(A1 + B1), reverse=True)

    # Create new arrays for A2 and B2
    A2_new = [np.nan] * len(C)
    B2_new = [np.nan] * len(C)

    # Interpolate values for A2 and B2 arrays
    for index, c_val in enumerate(C):
        if c_val in A1:
            A2_new[index] = A2[A1.index(c_val)]
        if c_val in B1:
            B2_new[index] = B2[B1.index(c_val)]

    for index, val in enumerate(A2_new):
        if np.isnan(val):
            for i in range(index - 1, -1, -1):
                if not np.isnan(A2_new[i]):
                    y0 = A2_new[i]
                    x0 = C[i]
                    break
            for i in range(index, len(A2_new)):
                if not np.isnan(A2_new[i]):
                    y1 = A2_new[i]
                    x1 = C[i]
                    break
            A2_new[index] = y0 + (y1 - y0) * (C[index] - x0) / (x1 - x0)
    for index, val in enumerate(B2_new):
        if np.isnan(val):
            for i in range(index - 1, -1, -1):
                if not np.isnan(B2_new[i]):
                    y0 = B2_new[i]
                    x0 = C[i]
                    break
            for i in range(index, len(B2_new)):
                if not np.isnan(B2_new[i]):
                    y1 = B2_new[i]
                    x1 = C[i]
                    break
            B2_new[index] = y0 + (y1 - y0) * (C[index] - x0) / (x1 - x0)

    return C, A2_new, B2_new


# Function to interpolate temperature
def interpolate_temperature(group, height, thickness, slabdepth=None):
    # Check if group is valid
    if group not in [1, 2, 3, 4]:
        raise ValueError("Group must be either 1, 2, 3 or 4")
    # Check if thickness is valid
    if isinstance(thickness, str):
        if thickness != SurfaceType.UNSURFACED and thickness != SurfaceType.WATERPROOFED:
            raise ValueError("Thickness must be either unsurfaced or waterproofed")
    elif isinstance(thickness, (int, float)):
        if thickness < 0:
            raise ValueError("Thickness cannot be negative")
    else:
        raise ValueError("Thickness must be either string or number")

    # Temperature data for group 1 and 2
    if group == 1 or group == 2:
        # Get data for the group
        data = data_group(group)
        keys = [int(key) for key in data.keys()]
        max_thickness = max(keys)

        if thickness == SurfaceType.UNSURFACED:
            data = data["0"]
        elif thickness >= max_thickness:
            data = data[str(max_thickness)]
        else:
            for i in range(len(keys) - 1):
                if keys[i] <= thickness < keys[i + 1]:
                    lower_key, upper_key = keys[i], keys[i + 1]
                    lower_value, upper_value = (
                        data[str(lower_key)],
                        data[str(upper_key)],
                    )
                    data = linear_interpolation(
                        lower_value, upper_value, lower_key, upper_key, thickness
                    )

        # Create Return Value
        if height <= 500:
            raise ValueError("Slab depth must be greater than 500 for group 1")
        else:
            if group == 1:
                point_h = [0, -100, -300, -600, -height]
                temp_h = [data["T1_h"], data["T2_h"], data["T3_h"], data["T4_h"], 0]
                point_c = [0, -500, -height]
                temp_c = [data["T1_c"], 0, 0]
            else:
                point_h = [0, -500, -height]
                temp_h = [data["T1_h"], 0, 0]
                point_c = [0, -100, -height]
                temp_c = [data["T1_c"], 0, 0]

            inf_point, inf_temp_h, inf_temp_c = merge_and_interpolate(
                point_h, temp_h, point_c, temp_c
            )

    elif group == 3 or group == 4:
        # Slab depth must be provided
        if slabdepth is None or slabdepth < 0:
            raise ValueError(
                "Slab depth must be provided as positive value for group 3 and 4"
            )

        if thickness == SurfaceType.UNSURFACED:
            data = data_group(group, 1)
            keys = sorted([int(key) for key in data.keys()])
            max_slab = max(keys)
            min_slab = min(keys)

            if slabdepth >= max_slab:
                data = data[str(max_slab)]
            elif slabdepth <= min_slab:
                data = data[str(min_slab)]
            else:
                for i in range(len(keys) - 1):
                    if keys[i] <= slabdepth < keys[i + 1]:
                        lower_key, upper_key = keys[i], keys[i + 1]
                        lower_value, upper_value = (
                            data[str(lower_key)],
                            data[str(upper_key)],
                        )
                        data = linear_interpolation(
                            lower_value, upper_value, lower_key, upper_key, slabdepth
                        )
                        break
        else:
            data = data_group(group, 2)
            keys = sorted([int(key) for key in data.keys()])
            max_slab = max(keys)
            min_slab = min(keys)

            if slabdepth >= max_slab:
                data = data[str(max_slab)]
            elif slabdepth <= min_slab:
                data = data[str(min_slab)]
            else:
                for i in range(len(keys) - 1):
                    if keys[i] <= slabdepth < keys[i + 1]:
                        lower_key, upper_key = keys[i], keys[i + 1]
                        lower_value, upper_value = (
                            data[str(lower_key)],
                            data[str(upper_key)],
                        )
                        data = {}
                        for param in lower_value.keys():
                            data[param] = {}
                            for sub_param in lower_value[param].keys():
                                lower_param_value = lower_value[param][sub_param]
                                upper_param_value = upper_value[param][sub_param]
                                data[param][sub_param] = lower_param_value + (
                                    upper_param_value - lower_param_value
                                ) * ((slabdepth - lower_key) / (upper_key - lower_key))

            keys = sorted([int(key) for key in data.keys()])
            max_thickness = max(keys)
            min_thickness = min(keys)

            if thickness >= max_thickness:
                data = data[str(max_thickness)]
            elif thickness <= min_thickness:
                data = data[str(min_thickness)]
            else:
                for i in range(len(keys) - 1):
                    if keys[i] <= thickness < keys[i + 1]:
                        lower_key, upper_key = keys[i], keys[i + 1]
                        lower_value, upper_value = (
                            data[str(lower_key)],
                            data[str(upper_key)],
                        )
                        data = linear_interpolation(
                            lower_value, upper_value, lower_key, upper_key, thickness
                        )
                        break

        if group == 3:
            if height - slabdepth < 400:
                raise ValueError(
                    "Height must be greater than slab depth + 400 for group 3"
                )
            else:
                point_h = [0, -0.6 * slabdepth, -slabdepth - 400, -height]
                temp_h = [data["T1_h"], 4, 0, 0]
                point_c = [0, -0.6 * slabdepth, -slabdepth, -slabdepth - 400, -height]
                temp_c = [data["T1_c"], 0, 0, -8, -8]

                inf_point, inf_temp_h, inf_temp_c = merge_and_interpolate(
                    point_h, temp_h, point_c, temp_c
                )

        elif group == 4:
            # For Heating
            # Basic Values
            h_temp = 0.3 * height

            # h1 and h2
            # h1 = 0.3h but <= 0.15m
            # h2 = 0.3h but >= 0.1m but <= 0.25m
            h1 = 0.3 * height if 0.3 * height <= 150 else 150
            h2 = (
                0.3 * height
                if (0.3 * height >= 100 and 0.3 * height <= 250)
                else (250 if 0.3 * height >= 250 else 100)
            )

            # Valid height Check
            if height <= h1 + h2:
                raise ValueError(
                    "Height must be greater than h1 + h2 for group 3 (heating)"
                )

            # h3 defintions
            # h3 = 0.3h but <= (0.10m + surfacihng depth in metres) (for thin slabs, h3 is limited by h-h1-h2)
            slab = "Thick"
            if thickness == SurfaceType.UNSURFACED or thickness == SurfaceType.WATERPROOFED:
                h3 = 0.3 * height if 0.3 * height <= 100 else 100
            else:
                h3 = (
                    0.3 * height
                    if 0.3 * height <= (100 + thickness)
                    else (100 + thickness)
                )

            if height - h1 - h2 <= h3:
                slab = "Thin"
                h3 = height - h1 - h2

            if slab == "Thick":
                point_h = [0, -h1, -h1 - h2, -height + h3, -height]
                temp_h = [data["T1_h"], data["T2_h"], 0, 0, data["T3_h"]]
            elif slab == "Thin":
                point_h = [0, -h1, -h1 - h2, -height]
                temp_h = [data["T1_h"], data["T2_h"], 0, data["T3_h"]]

            # For Cooling
            # Basic Values
            h14 = 0.2 * height if 0.2 * height <= 250 else 250
            h23 = 0.25 * height if 0.25 * height <= 200 else 200

            point_c = [0, -h14, -h14 - h23, -height + h14 + h23, -height + h14, -height]
            temp_c = [data["T1_c"], data["T2_c"], 0, 0, data["T3_c"], data["T4_c"]]

            inf_point, inf_temp_h, inf_temp_c = merge_and_interpolate(
                point_h, temp_h, point_c, temp_c
            )

    return inf_point, inf_temp_h, inf_temp_c, point_h, temp_h, point_c, temp_c
