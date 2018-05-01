
#           Well    HTN   SeverePE Eclampsia    Death   
# Well       0        0       0       0           0    
# HTN        0        0       0       0           0    
# SeverePE   0        0       0       0           0    
# Eclampsia  0        0       0       0           0    
# Death      0        0       0       0           0    

ALPHA = 0.05
DISCOUNT_RATE = 0.03
DISCOUNT=.03
DELTA_T = 1/2 #Every 6 hours
POP_SIZE = 2000
SIM_LENGTH = 20 #weeks

BASELINE_MATRIX = [
    [895, 105, 0.00, 0], #Well
    [0.00, 626, 374, 0], #HTN
    [0, 0.00, 980, 20], #SeverePE
    [0, 0, 0, 1000] #Eclampsia
    ]

# transition matrix
SUPPLIES_NO_TRAINING_MATRIX = [
    [895,	105,	0,	0],
    [0, 713,   287,	0],#HTN
    [0,	0,	981,	19], #SeverePE
    [0,	0,  0,	1000] #Eclampsia
    ]

# transition matrix
BETTER_TRAINING_MATRIX = [
    [895,	105, 0, 0],#Well
    [0,	652, 348, 0], #HTN
    [0,	0,	980,	20], #SeverePE
    [0,	0,	0,	1000] #Eclampsia
    ]


# transition matrix
BETTER_SUPPLIES_AND_TRAINING_MATRIX = [
    [895,	105, 0,	0],#Well
    [0,	791, 209,	0], #HTN
    [0,	0,	991, 9], #SeverePE
    [0,	0,	0,	1000] #Eclampsia
    ]

# annual cost of medications
COST_MGSO4 = 13   #a drug
COST_MD = 18
COST_SUPPLIES = COST_MGSO4 + COST_MD
COST_TRAINING = 0

# annual cost
HEALTH_COST = [
    5000,   # Well
    5500,   # HTN
    8000,   # SeverePE
    9500,   # Eclampsia
]

HEALTH_UTILITY = [
    1.0,   # Well
    0.8,       # HTN
    0.6,       # SeverePE
    0.1,   # Eclampsia
]
