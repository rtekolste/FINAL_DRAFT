
#           Well    HTN     Stroke  Detect  No-Detect   Death
#
# Well       0        0       0     0           0         0
# HTN        0        0       0     0           0         0
# Detect     0        0       0     0           0         0
# Death      0        0       0     0           0         0


ALPHA = 0.05
DISCOUNT_RATE = 0.03
DISCOUNT=.03
DELTA_T = 1/2 #Every 6 hours
POP_SIZE = 2000
SIM_LENGTH = 20 #weeks

# transition matrix
TRANS_MATRIX = [
    [.80,  0.05,   0.05,   0.05,  0.05], #Well
    [0.05,  .80,   0.05,   0.05,  0.05], #HTN
    [0.05,  0.05,   .80,   0.05,  0.05], #Stroke
    [0.05,  0.05,   0.05,   0.05,  0.05], #Detect
    [0.00,  0.00,   0.00,   0.00,  1.00], #Death
    ]

# transition matrix
TRANS_MATRIX_MGSO4 = [
    [1.00,  0.00,   0.00,   0.00,  0.00], #Well
    [0.00,  1.00,   0.00,   0.00,  0.00], #HTN
    [0.00,  0.00,   1.00,   0.00,  0.00], #Stroke
    [0.00,  0.00,   0.00,   1.00,  0.00], #Detect
    [0.00,  0.00,   0.00,   0.00,  1.00], #Death
    ]

# transition matrix
TRANS_MATRIX_ANTICOAG = [
    [.80,  0.05,   0.05,   0.05,  0.05], #Well
    [0.05,  .80,   0.05,   0.05,  0.05], #HTN
    [0.05,  0.05,   .80,   0.05,  0.05], #Stroke
    [0.05,  0.05,   0.05,   0.8,  0.05], #Detect
    [0.00,  0.00,   0.00,   0.00,  1.00], #Death
    ]
# annual cost of medications
COST_MGSO4 = 10.50   #a drug

COST_ANTICOAG = 4.50 # a normal bp med/ checkup?
# cost of events
COST_STROKE = 12780    #heart attk

# annual cost
HEALTH_COST = [
    0,   # Well
    0,       # HTN
    0,       # Stroke
    0,   # Detect
    0,    # No Detect
    0,    # Death
]

HEALTH_UTILITY = [
    0,   # Well
    0,       # HTN
    0,       # Stroke
    0,   # Detect
    0,    # No Detect
    0,    # Death
]
