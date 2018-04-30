
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
    [0.895, 0.105, 0.00, 0], #Well
    [0.00, 0.626, 0.374, 0], #HTN
    [0, 0.00, 0.980, 0.020], #SeverePE
    [0, 0, 0, 1] #Eclampsia
    ]

# transition matrix
SUPPLIES_NO_TRAINING_MATRIX = [
    [0.895,	0.105,	0,	0],
    [0, 0.713,   0.287,	0],#HTN
    [0,	0,	0.981,	0.019], #SeverePE
    [0,	0,  0,	1] #Eclampsia
    ]

# transition matrix
BETTER_TRAINING_MATRIX = [
    [0.895,	0.105, 0, 0],#Well
    [0,	0.652, 0.348, 0], #HTN
    [0,	0,	0.980,	0.020], #SeverePE
    [0,	0,	0,	1] #Eclampsia
    ]


# transition matrix
BETTER_SUPPLIES_AND_TRAINING_MATRIX = [
    [0.895,	0.105, 0,	0],#Well
    [0,	0.791,	0.209,	0], #HTN
    [0,	0,	0.991,	0.009], #SeverePE
    [0,	0,	0,	1] #Eclampsia
    ]

# annual cost of medications
COST_MGSO4 = 5   #a drug
COST_MD = 4
COST_SUPPLIES = COST_MGSO4 + COST_MD
COST_TRAINING = 0

# annual cost
HEALTH_COST = [
    0,   # Well
    0,   # HTN
    0,   # SeverePE
    0,   # Eclampsia
]

HEALTH_UTILITY = [
    1.0,   # Well
    0.8,       # HTN
    0.6,       # SeverePE
    0.1,   # Eclampsia
]
