contents = [
    {
        # link : https://midastech.atlassian.net/wiki/spaces/~601b5cb3f564b600715ea99d/pages/88179032/EN1991-1-1+Nominal+Density+for+Construction+Materials
        "id": "1",
        "standardType": "EUROCODE",
        "codeName": "EN1991-1-1",
        "codeTitle": "Eurocode 1: Actions on structures — Part 1-1: General actions — Densities, self-weight, imposed loads for buildings",
        "title": "Nominal Density Guide for Construction Materials in Bridge Structures",
        "description": "[EN1991-1-1] This guide provides a comprehensive overview of the nominal density values for various construction materials commonly used in bridge structures. It is designed to assist engineers and designers in selecting appropriate materials based on their density characteristics, ensuring the structural integrity and longevity of bridge projects.",
        "edition": "2002 Incorporating Corrigendum No. 1",
        "targetComponents": ['G4_COMP_4', 'G4_COMP_5', 'G4_COMP_6', 'G4_COMP_7', 'G4_COMP_8', 'G4_COMP_9'],
        "testInput": [
            {'component': 'G4_COMP_1', 'value': 'Weight density (kN/m^{3})'}, # densitytype = Weight density
            # {'component': 'G4_COMP_1', 'value': 'Mass density (kg/m^{3})'}, # densitytype = Mass density
        ],
    },
    {
        # link : https://midastech.atlassian.net/wiki/spaces/~601b5cb3f564b600715ea99d/pages/92439183/EN1991-1-4+Peak+Velocity+Wind+Pressure
        "id": "2",
        "standardType": "EUROCODE",
        "codeName": "EN1991-1-4",
        "codeTitle": "Eurocode 1: Actions on structures — Part 1-4: General actions — Wind actions",
        "title": "Peak Velocity Pressure Calculation at Height",
        "description": "[EN1991-1-4] This guide provides a detailed approach for calculating the peak velocity pressure at a specific height by accounting for both mean wind velocity and short-term fluctuations caused by turbulence. The calculation includes determining key parameters such as air density, mean wind velocity, and the exposure factor. The peak velocity pressure is influenced by the turbulence intensity and the exposure factor, which take into account the effects of terrain and height on wind speed. This guide explains how to determine these parameters using the appropriate methods and values, ensuring that engineers can accurately assess wind loads on structures at various elevations.",
        "edition": "2005+A1:2010 Incorporating corrigenda July 2009 and January 2010",
        "targetComponents": ['G3_COMP_24'],
        "testInput": [
            {'component': 'G3_COMP_2', 'value': 27},
            {'component': 'G3_COMP_6', 'value': 50},
            {'component': 'G3_COMP_10', 'value': 6},
            {'component': 'G3_COMP_15', 'value': '[0] Sea or coastal area exposed to the open sea'}, # terrain = 0
            # {'component': 'G3_COMP_15', 'value': '[I] Lakes or flat and horizontal area with negligible vegetation and without obstacles'}, # terrain = I
            # {'component': 'G3_COMP_15', 'value': '[II] Area with low vegetation such as grass and isolated obstacles (trees, buildings) with separations of at least 20 obstacle heights'}, # terrain = II
            # {'component': 'G3_COMP_15', 'value': '[III] Area with regular cover of vegetation or buildings or with isolated obstacles with separations of maximum 20 obstacle heights (such as villages, suburban terrain, permanent forest)'}, # terrain = III
            # {'component': 'G3_COMP_15', 'value': '[IV] Area in which at least 15 % of the surface is covered with buildings and their average height exceeds 15 m'}, # terrain = IV
        ],
    },
    {
        # link : https://midastech.atlassian.net/wiki/spaces/~601b5cb3f564b600715ea99d/pages/86904369/EN1991-1-5+Uniform+bridge+temperature
        "id": "3",
        "standardType": "EUROCODE",
        "codeName": "EN1991-1-5",
        "codeTitle": "Eurocode 1: Actions on structures — Part 1-5: General actions — Thermal actions",
        "title": "Range of uniform bridge temperature component",
        "description": "[EN1991-1-5] This guide explains how to calculate the Range of Uniform Bridge Temperature Component by applying Isotherms of national minimum and maximum shade air temperatures, as provided in Eurocode. The guide uses national temperature maps to help determine the characteristic minimum and maximum temperatures for a specific site. These values are then applied to calculate the uniform temperature changes experienced by the bridge. The resulting data helps in assessing potential thermal expansion and contraction of the bridge, ensuring compliance with Eurocode temperature actions for structural safety.",
        "edition": "2003 Incorporating Corrigendum No. 1",
        "targetComponents": ['G1_COMP_16', 'G1_COMP_17'],
        "testInput": [
            {'component': 'G1_COMP_1', 'value': 'steel box girder'}, # Deck_types = Type1
            # {'component': 'G1_COMP_1', 'value': 'composite deck'}, # Deck_types = Type2
            # {'component': 'G1_COMP_1', 'value': 'concrete box girder'}, # Deck_types = Type3
            {'component': 'G1_COMP_3', 'value': 10.0},
            {'component': 'G1_COMP_4', 'value': 30},
            {'component': 'G1_COMP_6', 'value': -17},
            {'component': 'G1_COMP_7', 'value': 34},
        ],
    },
    {
        # link : https://midastech.atlassian.net/wiki/spaces/~601b5cb3f564b600715ea99d/pages/105185819/EN1992-1-1+Geometrical+Imperfection+in+Bridge+Design
        "id": "4",
        "standardType": "EUROCODE",
        "codeName": "EN1992-1-1",
        "codeTitle": "Eurocode 2: Design of concrete structures — Part 1-1: General rules and rules for buildings",
        "title": "Geometrical Imperfection Calculation in Bridge Design",
        "description": "[EN1992-1-1] Geometrical imperfections in bridge design account for deviations due to construction tolerances or fabrication errors. These imperfections are critical for components like girders, piers, and arches, affecting their stability and load-bearing capacity. In girders and piers, imperfections can lead to additional moments or instability, especially under axial compression, and must be included in the structural analysis to prevent buckling. For arch bridges, imperfections impact vertical and horizontal buckling behavior, requiring early consideration in design. Geometrical imperfections are primarily considered in ultimate limit state analysis, ensuring the structure can handle real-world loads while maintaining stability.",
        "edition": "2004",
        "targetComponents": ['G2_COMP_1', 'G2_COMP_5', 'G2_COMP_6'],
        "testInput": [
            {'component': 'G2_COMP_4', 'value': 30},
            {'component': 'G2_COMP_7', 'value': 650},
            {'component': 'G6_COMP_2', 'value': 'Pinned Ends'}, # buckmode = Pinned Ends
            # {'component': 'G6_COMP_2', 'value': 'Free - Fixed Ends'}, # buckmode = Free - Fixed Ends
            # {'component': 'G6_COMP_2', 'value': 'Pinned - Fixed Ends'}, # buckmode = Pinned - Fixed Ends
            # {'component': 'G6_COMP_2', 'value': 'Fixed Ends'}, # buckmode = Fixed Ends
            # {'component': 'G6_COMP_2', 'value': 'Guided - Fixed Ends'}, # buckmode = Guided - Fixed Ends
            {'component': 'G6_COMP_4', 'value': 14.5},
        ],
    },
    {
        # link : https://midastech.atlassian.net/wiki/spaces/~601b5cb3f564b600715ea99d/pages/92505071/EN1991-1-4+Wind+Forces+on+Bridge+Decks+Without+Traffic
        "id": "5",
        "standardType": "EUROCODE",
        "codeName": "EN1991-1-4",
        "codeTitle": "Eurocode 1: Actions on structures — Part 1-4: General actions — Wind actions",
        "title": "Wind Force Calculation on Bridge Decks Without Traffic",
        "description": "[EN1991-1-4] This guide outlines the steps for calculating wind forces acting on bridge decks without traffic in the x (perpendicular to the span), y (longitudinal along the span), and z (vertical) directions. For bridges without traffic, the wind force in the x-direction is calculated based on the width of the bridge deck and adjusted wind load factors to reflect the absence of vehicles. The y-direction wind force is a percentage of the x-direction force, considering the type of bridge and lack of dynamic load from traffic. In the z-direction, the forces account for both upward and downward actions (lift), emphasizing the changes due to no traffic load. Each calculation must consider factors such as deck geometry, wind exposure, and structural configuration to ensure the bridge’s stability under various wind conditions without the influence of traffic.",
        "edition": "2005+A1:2010 Incorporating corrigenda July 2009 and January 2010",
        "figureFile": "detail_content_5.png",
        "targetComponents": ['G5_COMP_1', 'G5_COMP_13', 'G5_COMP_16'],
        "testInput": [
            {'component': "G3_COMP_2", 'value': 27},
            {'component': "G3_COMP_6", 'value': 50},
            {'component': "G3_COMP_10", 'value': 6},
            {'component': "G3_COMP_15", 'value': '[0] Sea or coastal area exposed to the open sea'}, # terrain = 0
            {'component': "G5_COMP_6", 'value': 10},
            {'component': "G5_COMP_7", 'value': 1.9},
            {'component': "G5_COMP_8", 'value': 'Open parapet or safety barrier'}, # restop = Open parapet or safety barrier
            # {'component': "G5_COMP_8", 'value': 'Solid parapet or safety barrier'}, # restop = Solid parapet or safety barrier
            # {'component': "G5_COMP_8", 'value': 'Open parapet and safety barrier'}, # restop = Open parapet and safety barrier
            {'component': "G5_COMP_9", 'value': 'on one side'}, # restpla = on one side
            # {'component': "G5_COMP_9", 'value': 'on both sides'}, # restpla = on both sides
            {'component': "G5_COMP_11", 'value': 4.24},
            {'component': "G5_COMP_12", 'value': 'Plated bridges'}, # brigetype = Plated bridges
            # {'component': "G5_COMP_12", 'value': 'Truss bridges'}, # brigetype = Truss bridges
            {'component': "G5_COMP_17", 'value': 12.95},
        ],
    },
    {
        # link : https://midastech.atlassian.net/wiki/spaces/~601b5cb3f564b600715ea99d/pages/107479646/EN1992-1-1+Slenderness+of+Isolated+Members
        "id": "6",
        "standardType": "EUROCODE",
        "codeName": "EN1992-1-1",
        "codeTitle": "Eurocode 2: Design of concrete structures — Part 1-1: General rules and rules for buildings",
        "title": "Slenderness Calculation for Isolated Members with Constant Cross Section",
        "description": "[EN1992-1-1] This guide explains how to calculate the slenderness of isolated members with a constant cross section for five different cases. It covers the calculation of slenderness for both circular and rectangular cross sections. The slenderness ratio is determined using the effective length and the radius of gyration of the uncracked concrete section. This guide allows you to easily calculate and compare the slenderness for members with different cross sections.",
        "edition": "2004",
        "targetComponents": ['G6_COMP_1'],
        "testInput": [
            {'component': "G6_COMP_2", 'value': 'Pinned Ends'},
            # {'component': 'G6_COMP_2', 'value': 'Free - Fixed Ends'}, # buckmode = Free - Fixed Ends
            # {'component': 'G6_COMP_2', 'value': 'Pinned - Fixed Ends'}, # buckmode = Pinned - Fixed Ends
            # {'component': 'G6_COMP_2', 'value': 'Fixed Ends'}, # buckmode = Fixed Ends
            # {'component': 'G6_COMP_2', 'value': 'Guided - Fixed Ends'}, # buckmode = Guided - Fixed Ends
            {'component': "G6_COMP_4", 'value': 14.5},
            {'component': "G6_COMP_6", 'value': 'circular'},
            # {'component': "G6_COMP_6", 'value': 'rectangular'},
            {'component': "G6_COMP_9", 'value': 550},
            {'component': "G6_COMP_10", 'value': 250},
            {'component': "G6_COMP_11", 'value': 300},
        ],
    },
    {
        # link : https://midastech.atlassian.net/wiki/spaces/~601b5cb3f564b600715ea99d/pages/97749255/EN1991-2+Horizontal+Forces+on+Road+Bridges
        "id": "7",
        "standardType": "EUROCODE",
        "codeName": "EN1991-2",
        "codeTitle": "Eurocode 1: Actions on structures — Part 2: Traffic loads on bridges",
        "title": "Horizontal Force Calculation on Road Bridges",
        "description": "[EN1991-2] This guide provides a comprehensive approach to calculating horizontal forces acting on road bridges. It covers the calculation of braking and acceleration forces, as well as centrifugal and other transverse forces that impact the structure. By outlining the relevant load models, adjustment factors, and practical applications, this guide ensures that engineers can accurately assess the distribution of horizontal forces along the carriageway. The guide also includes step-by-step instructions and examples for applying these forces across different lanes and sections of the bridge, ensuring safety and structural integrity.",
        "edition": "2003 Incorporating Corrigendum No. 1",
        "figureFile": "detail_content_7.png",
        "targetComponents": ['G7_COMP_1', 'G7_COMP_2', 'G7_COMP_7', 'G7_COMP_9'],
        "testInput": [
            {'component': "G7_COMP_3", 'value': 35},
            # {'component': "G7_COMP_4", 'value': 4},
            # {'component': "G7_COMP_4", 'value': 5.5},
            {'component': "G7_COMP_4", 'value': 11},
            # {'component': "G7_COMP_8", 'value': 150},
            # {'component': "G7_COMP_8", 'value': 1100},
            {'component': "G7_COMP_8", 'value': 1500},
        ],
    },
    {
        # link : https://midastech.atlassian.net/wiki/spaces/~601b5cb3f564b600715ea99d/pages/98895143/EN1991-2+Dynamic+Factors+for+Railway+Bridges
        "id": "8",
        "standardType": "EUROCODE",
        "codeName": "EN1991-2",
        "codeTitle": "Eurocode 1: Actions on structures — Part 2: Traffic loads on bridges",
        "title": "Dynamic Factors for Railway Bridges with Multiple Spans",
        "description": "[EN1991-2] This guide provides a detailed approach to calculating dynamic factors for railway bridges with main girders that span multiple spans. It includes instructions for determining the dynamic factor used in static analysis, which accounts for general dynamic amplification, and the dynamic factor applied to real train movements, which considers the effects of train speed and resonance. By following this guide, engineers can ensure that the bridge design accommodates both standard dynamic loads and the specific dynamic effects of real trains operating at high speeds.",
        "edition": "2003 Incorporating Corrigendum No. 1",
        "figureFile": "detail_content_8.png",
        "targetComponents": ['G8_COMP_1', 'G8_COMP_2', 'G8_COMP_10', 'G8_COMP_11', 'G8_COMP_12', 'G8_COMP_13'],
        "testInput": [
            {'component': "G8_COMP_3", 'value':115},
            {'component': "G8_COMP_4", 'value':5},
            {'component': "G8_COMP_8", 'value':350},
        ],
    },
    {
        # link : https://midastech.atlassian.net/wiki/spaces/~601b5cb3f564b600715ea99d/pages/100206000/EN1991-2+Horizontal+Forces+in+Railway+Bridges
        "id": "9",
        "standardType": "EUROCODE",
        "codeName": "EN1991-2",
        "codeTitle": "Eurocode 1: Actions on structures — Part 2: Traffic loads on bridges",
        "title": "Horizontal Force Calculation on Railway Bridges",
        "description": "[EN1991-2] This guide provides detailed steps for calculating horizontal forces acting on railway bridges. It covers the evaluation of centrifugal forces, nosing force, and traction and braking forces, which are critical in assessing the structural stability and performance of railway bridges. These horizontal forces must be considered to ensure the safety and durability of bridges under various rail traffic conditions.",
        "edition": "2003 Incorporating Corrigendum No. 1",
        "targetComponents": ['G9_COMP_1', 'G9_COMP_2', 'G9_COMP_11', 'G9_COMP_13', 'G9_COMP_14'],
        "testInput": [
            {'component': "G8_COMP_8", 'value': 350},
            {'component': "G9_COMP_4", 'value': 1500},
            {'component': "G9_COMP_5", 'value': "Load Model 71"}, # rtmodel = Load Model 71
            # {'component': "G9_COMP_5", 'value': "Load Model SW/0"}, # rtmodel = Load Model SW/0
            # {'component': "G9_COMP_5", 'value': "Load Model SW/2"}, # rtmodel = Load Model SW/2
            # {'component': "G9_COMP_5", 'value': "Unloaded Train"}, # rtmodel = Unloaded Train
            {'component': "G9_COMP_8", 'value': 115},
            {'component': "G9_COMP_17", 'value': 25.4},
        ],
    },
    {
        # link : https://midastech.atlassian.net/wiki/spaces/~601b5cb3f564b600715ea99d/pages/96864191/EN1991-1-4+Wind+Forces+on+Rectangular+Bridge+Piers
        "id": "10",
        "standardType": "EUROCODE",
        "codeName": "EN1991-1-4",
        "codeTitle": "Eurocode 1: Actions on structures — Part 1-4: General actions — Wind actions",
        "title": "Wind Force Calculation on Rectangular Bridge Piers",
        "description": "[EN1991-1-4] This guide provides a detailed methodology for calculating wind loads on rectangular bridge piers. It covers essential factors such as the shape, orientation, and size of the piers, as well as wind speed, height, and pressure coefficients. The guide also explains how to apply appropriate force coefficients specifically for rectangular piers, ensuring accurate wind load assessment for bridge design and safety considerations.",
        "edition": "2005+A1:2010 Incorporating corrigenda July 2009 and January 2010",
        "figureFile": "detail_content_10.png",
        "targetComponents": ['G10_COMP_1'],
        "testInput": [
            {'component': 'G3_COMP_2', 'value': 27},
            {'component': 'G3_COMP_6', 'value': 50},
            {'component': 'G3_COMP_10', 'value': 6},
            {'component': 'G3_COMP_15', 'value': '[0] Sea or coastal area exposed to the open sea'}, # terrain = 0
            {'component': "G10_COMP_3", 'value': 6.5},
            {'component': "G10_COMP_4", 'value': 2.5},
            {'component': "G10_COMP_5", 'value': 3},
            {'component': "G10_COMP_6", 'value': 0},
        ],
    },
    {
        # link : https://midastech.atlassian.net/wiki/spaces/~601b5cb3f564b600715ea99d/pages/129106072/CHAPTER+3+Wind+Actions
        "id": "11",
        "standardType": "HK.SDM",
        "codeName": "HK.SDM2013",
        "codeTitle": "Structures Design Manual for Highways and Railways",
        "title": "Peak Velocity Pressure for Wind and Traffic Leading Combinations",
        "description": "[HK.SDM-2013] This guide provides comprehensive instructions for calculating the peak velocity pressure for wind leading and traffic leading combinations on highway and railway structures. It covers the General, Simplified, and Full procedures as outlined in the Structures Design Manual for Highways and Railways (2013 Edition) by the Highways Department of the Government of the Hong Kong Special Administrative Region. The guide includes methods for determining wind pressure, assessing upwind slope impacts, and applying terrain adjustments necessary for safe and effective structural design.",
        "edition": "5th revision of 2023",
        "targetComponents": ['G11_COMP_2', 'G11_COMP_3'],
        "testInput": [
            {'component': "G11_COMP_1", 'value': 'General'}, # windproce = General
            # {'component': "G11_COMP_1", 'value': 'Simplified'}, # windproce = Simplified
            # {'component': "G11_COMP_1", 'value': 'Full'}, # windproce = Full
            {'component': "G11_COMP_4", 'value': 'Waglan Island'}, # windlocat = Waglan Island
            # {'component': "G11_COMP_4", 'value': 'Hong Kong Observatory'}, # windlocat = Hong Kong Observatory
            {'component': "G11_COMP_5", 'value': 120},
            {'component': "G11_COMP_11", 'value': 1}, # degexpo = 1
            # {'component': "G11_COMP_11", 'value': 2}, # degexpo = 2
            # {'component': "G11_COMP_11", 'value': 3}, # degexpo = 3
            # {'component': "G11_COMP_11", 'value': 4}, # degexpo = 4
            {'component': "G11_COMP_14", 'value': 'Non-Significant Orography Site'}, # orosigsite = Non-Significant Orography Site
            # {'component': "G11_COMP_14", 'value': 'Significant Orography Site'}, # orosigsite = Significant Orography Site
            {'component': "G11_COMP_18", 'value': 40},
            {'component': "G11_COMP_19", 'value': 100},
            {'component': "G11_COMP_25", 'value': 80},
            {'component': "G11_COMP_26", 'value': 650},
            {'component': "G11_COMP_30", 'value': 'Cliffs and Escarpments'}, # terrtype = Cliffs and Escarpments
            # {'component': "G11_COMP_30", 'value': 'Hills and Ridges'}, # terrtype = Hills and Ridges
            {'component': "G11_COMP_33", 'value': 400},
            {'component': "G11_COMP_34", 'value': -150},
        ],
    },
    {
        # link : https://midastech.atlassian.net/wiki/spaces/~601b5cb3f564b600715ea99d/pages/129925752/CHAPTER+3+Temperature+Effect
        "id": "12",
        "standardType": "HK.SDM",
        "codeName": "HK.SDM2013",
        "codeTitle": "Structures Design Manual for Highways and Railways",
        "title": "Uniform Bridge Temperature Range Calculation for Hong Kong",
        "description": "[HK.SDM-2013] This guide explains how to calculate the uniform bridge temperature range components specific to Hong Kong, where the contraction range, expansion range, and overall range for the uniform bridge temperature are adjusted based on climate data and environmental conditions unique to Hong Kong. The minimum and maximum uniform bridge temperatures have been updated to account for climate change impacts in Hong Kong, ensuring that structural temperature ranges accurately reflect local conditions and capture the potential contraction, expansion, and overall variation of bridge temperatures within these localized parameters.",
        "edition": "5th revision of 2023",
        "targetComponents": ['G12_COMP_15', 'G12_COMP_16', 'G12_COMP_17'],
        "testInput": [
            {'component': "G12_COMP_1", 'value': 'Normal'}, # tempstruct = Normal
            # {'component': "G12_COMP_1", 'value': 'Minor'}, # tempstruct = Minor
            {'component': "G12_COMP_2", 'value': 'Steel deck on steel girders'}, # supertype = Steel deck on steel girders
            # {'component': "G12_COMP_2", 'value': 'Steel deck on steel truss or plate girders'}, # supertype = Steel deck on steel truss or plate girders
            # {'component': "G12_COMP_2", 'value': 'Concrete deck on steel box'}, # supertype = Concrete deck on steel box
            # {'component': "G12_COMP_2", 'value': 'Concrete deck on truss or plate girders'}, # supertype = Concrete deck on truss or plate girders
            # {'component': "G12_COMP_2", 'value': 'Concrete slab'}, # supertype = Concrete slab
            # {'component': "G12_COMP_2", 'value': 'Concrete beams'}, # supertype = Concrete beams
            # {'component': "G12_COMP_2", 'value': 'Concrete box girder'}, # supertype = Concrete box girder
            {'component': "G12_COMP_4", 'value': 'Unsurfaced Plain'}, # dsurftype = Unsurfaced Plain
            # {'component': "G12_COMP_4", 'value': 'Unsurfaced Trafficked or Waterproofed'}, # dsurftype = Unsurfaced Trafficked or Waterproofed
            # {'component': "G12_COMP_4", 'value': 'Surfacing Depths'}, # dsurftype = Surfacing Depths
            {'component': "G12_COMP_5", 'value': 120},
            {'component': "G12_COMP_6", 'value': 95.5},
        ],
    },
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/97748343/EN1991-1-4+Wind+Force+on+Circular+Bridge+Piers
        "id": "13",
        "standardType": "EUROCODE",
        "codeName": "EN1991-1-4",
        "codeTitle": "Eurocode 1: Actions on structures — Part 1-4: General actions — Wind actions",
        "title": "Wind Force Calculation on Circular Bridge Piers",
        "description": "[EN1991-1-4] This guide explains how to calculate the wind force acting on circular bridge piers. The wind force is determined using factors such as the force coefficient, structural factor, peak velocity pressure at the reference height, and the exposed reference area. The guide also considers the influence of surface roughness and Reynolds number, ensuring accurate estimation of wind loads on circular bridge piers.",
        "edition": "2005+A1:2010 Incorporating corrigenda July 2009 and January 2010",
        "figureFile": "detail_content_13.png",
        "targetComponents": ['G13_COMP_16'],
        "testInput": [
            {'component': "G3_COMP_2", 'value': 27},
            {'component': "G3_COMP_6", 'value': 50},
            {'component': "G3_COMP_10", 'value': 6},
            {'component': "G3_COMP_15", 'value': '[0] Sea or coastal area exposed to the open sea'}, # terrain = 0
            {'component': "G13_COMP_2", 'value': 11},
            {'component': "G13_COMP_3", 'value': 2.5},
            {'component': "G13_COMP_8", 'value': 'Smooth Concrete'}, # surftype = Smooth Concrete
            # {'component': "G13_COMP_8", 'value': 'Rough Concrete'}, # surftype = Smooth Concrete
            # {'component': "G13_COMP_8", 'value': 'Bright Steel'}, # surftype = Bright Steel
            # {'component': "G13_COMP_8", 'value': 'Cast Iron'}, # surftype = Cast Iron
            # {'component': "G13_COMP_8", 'value': 'Galvanised Steel'}, # surftype = Galvanised Steel
        ],
    },
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/88278010/EN1992-1-1+Concrete+Design+Parameters
        "id": "14",
        "standardType": "EUROCODE",
        "codeName": "EN1992-1-1",
        "codeTitle": "Eurocode 2: Design of concrete structures — Part 1-1: General rules and rules for buildings",
        "title": "Concrete Design Parameters Guide",
        "description": "[EN1992-1-1] This guide provides detailed explanations of the essential parameters for concrete design according to Eurocode standards. It covers important factors such as design compressive and tensile strengths, as well as the material properties of concrete, helping engineers gain a comprehensive understanding of the key elements necessary for safe and efficient concrete design.",
        "edition": "2004",
        "targetComponents": ['G14_COMP_15', 'G14_COMP_16', 'G14_COMP_17', 'G14_COMP_18', 'G14_COMP_19'],
        "testInput": [
            {'component': "G14_COMP_1", 'value': 1500},
            {'component': "G14_COMP_2", 'value': 'K^{-1} (Kelvin)'}, # tempunit = K (Kelvin)
            # {'component': "G14_COMP_2", 'value': '°C^{-1} (Celsius)'}, # tempunit = °C (Celsius)
            # {'component': "G14_COMP_2", 'value': '°F^{-1} (Fahrenheit)'}, # tempunit = °F (Fahrenheit)
            {'component': "G14_COMP_3", 'value': 'Persistent'}, # designsitu = Persistent
            # {'component': "G14_COMP_3", 'value': 'Transient'}, # designsitu = Transient
            # {'component': "G14_COMP_3", 'value': 'Accidental'}, # designsitu = Accidental
            {'component': "G14_COMP_4", 'value': 'C12/15'}, # C = C12/15
            # {'component': "G14_COMP_4", 'value': 'C50/60'}, # C = C50/60
        ],
    },
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/88179457/EN1992-1-1+Concrete+Design+Parameters+for+Early-Age
        "id": "15",
        "standardType": "EUROCODE",
        "codeName": "EN1992-1-1",
        "codeTitle": "Eurocode 2: Design of concrete structures — Part 1-1: General rules and rules for buildings",
        "title": "Concrete Design Parameters for Early-Age",
        "description": "[EN1992-1-1] This guide provides the necessary concrete design parameters for situations where the concrete compressive strength, fck(t), must be specified at an age less than 28 days. This is particularly important for various construction stages, such as demoulding or the transfer of prestress, where early-age strength is critical.",
        "edition": "2004",
        "targetComponents": ['G15_COMP_6', 'G15_COMP_8', 'G15_COMP_9'],
        "testInput": [
            {'component': "G14_COMP_4", 'value': 'C12/15'}, # C = C12/15
            {'component': "G15_COMP_1", 'value': 3},
            {'component': "G15_COMP_2", 'value': 'Class S'}, # cementtype = Class S
            # {'component': "G15_COMP_2", 'value': 'Class N'}, # cementtype = Class N
            # {'component': "G15_COMP_2", 'value': 'Class R'}, # cementtype = Class R
        ],
    },
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/88179638/EN1992-1-1+Creep+Coefficient
        "id": "16",
        "standardType": "EUROCODE",
        "codeName": "EN1992-1-1",
        "codeTitle": "Eurocode 2: Design of concrete structures — Part 1-1: General rules and rules for buildings",
        "title": "Creep Coefficient Calculation According to Eurocode",
        "description": "[EN1992-1-1] The creep coefficient measures the time-dependent deformation (creep) of concrete under sustained load. It is essential for predicting the long-term performance of concrete structures, particularly under constant compressive stress. This guide provides instructions for calculating the creep coefficient, understanding its relationship with the tangent modulus, and adjusting for non-linear effects when stress levels are high. Proper calculation of the creep coefficient ensures the durability and safety of concrete structures over time.",
        "edition": "2004",
        "targetComponents": ['G16_COMP_17', 'G16_COMP_19'],
        "testInput": [
            {'component': "G14_COMP_4", 'value': 'C12/15'}, # C = C12/15
            # {'component': "G14_COMP_4", 'value': 'C40/50'}, # C = C40/50
            {'component': "G15_COMP_2", 'value': 'Class S'}, # cementtype = Class S
            {'component': "G16_COMP_5", 'value': 10},
            {'component': "G16_COMP_6", 'value': 3},
            {'component': "G16_COMP_11", 'value': 534694.0},
            {'component': "G16_COMP_12", 'value': 5921.8},
            {'component': "G16_COMP_14", 'value': 'User Input'}, # rhtype = User Input
            # {'component': "G16_COMP_14", 'value': 'inside conditions'}, # rhtype = inside conditions
            # {'component': "G16_COMP_14", 'value': 'outside conditions'}, # rhtype = outside conditions
            {'component': "G16_COMP_23", 'value': 70},
        ],
    },
]