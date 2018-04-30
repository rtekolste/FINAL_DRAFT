
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

# transition matrix
BASELINE = [
    [.80,  0.05,   0.05,   0.05,  0.05], #Well
    [0.05,  .80,   0.05,   0.05,  0.05], #HTN
    [0.05,  0.05,   .80,   0.05,  0.05], #SeverePE
    [0.05,  0.05,   0.05,   0.05,  0.05], #Eclampsia
    [0.00,  0.00,   0.00,   0.00,  1.00], #Death
    ]

# transition matrix
SUPPLIES_NO_TRAINING = [
    [1.00,  0.00,   0.00,   0.00,  0.00], #Well
    [0.00,  1.00,   0.00,   0.00,  0.00], #HTN
    [0.00,  0.00,   1.00,   0.00,  0.00], #SeverePE
    [0.00,  0.00,   0.00,   1.00,  0.00], #Eclampsia
    [0.00,  0.00,   0.00,   0.00,  1.00], #Death
    ]

# transition matrix
BETTER_TRAINING = [
    [.80,  0.05,   0.05,   0.05,  0.05], #Well
    [0.05,  .80,   0.05,   0.05,  0.05], #HTN
    [0.05,  0.05,   .80,   0.05,  0.05], #SeverePE
    [0.05,  0.05,   0.05,   0.8,  0.05], #DEclampsia
    [0.00,  0.00,   0.00,   0.00,  1.00], #Death
    ]

# transition matrix
BETTER_SUPPLIES_AND_TRAINING = [
    [.80,  0.05,   0.05,   0.05,  0.05], #Well
    [0.05,  .80,   0.05,   0.05,  0.05], #HTN
    [0.05,  0.05,   .80,   0.05,  0.05], #SeverePE
    [0.05,  0.05,   0.05,   0.8,  0.05], #DEclampsia
    [0.00,  0.00,   0.00,   0.00,  1.00], #Death
    ]
# annual cost of medications
COST_MGSO4 = 10.50   #a drug

COST_ANTICOAG = 4.50 # a normal bp med/ checkup?
# cost of events
COST_ECLAMPSIA = 14080    #heart attack
COST_DEATH = 120780    #heart attack


# annual cost
HEALTH_COST = [
    0,   # Well
    0,       # HTN
    0,       # SeverePE
    0,   # Eclampsia
    0,    # Death
]

HEALTH_UTILITY = [
    0,   # Well
    0,       # HTN
    0,       # SeverePE
    0,   # Eclampsia
    0,    # Death
]
