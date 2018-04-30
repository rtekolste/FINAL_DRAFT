
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


BASELINE = [
    [0.8946394843,  0.1053605157,   0.00,   0], #Well
    [0.00,  0.6264736985,   0.3735263015,   0], #HTN
    [0, 0.00,   0.9799769454,   0.02002305456], #SeverePE
    [0, 0,  0,  1] #Eclampsia
    ]


# transition matrix
SUPPLIES_NO_TRAINING = [    
    [0.8946394843,	0.1053605157,	0,	0],
    [0, 0.7131609604,   0.2868390396,	0],#HTN
    [0,	0,	0.9814844583,	0.01851554169], #SeverePE
    [0,	0,  0,	1] #Eclampsia
    ]

# transition matrix
BETTER_TRAINING = [
    [0.9,	0.1,	0,	0],#Well
    [0,	0.710065,	0.289935,	0], #HTN
    [0,	0,	0.9801838858,	0.0198161142], #SeverePE
    [0,	0,	0,	1] #Eclampsia
    ]


# transition matrix
BETTER_SUPPLIES_AND_TRAINING = [
    [0.8946394843,	0.1053605157, 0,	0],#Well
    [0,	0.7913247999,	0.2086752001,	0], #HTN
    [0,	0,	0.9913507665,	0.008649233463], #SeverePE
    [0	0,	0,	1] #Eclampsia
    ]


# annual cost of medications
COST_MGSO4 = 5   #a drug
COST_MD = 4

COST_ANTICOAG = 4.50 # a normal bp med/ checkup?
# cost of events
COST_ECLAMPSIA = 14080    #need to confirm. 
COST_DEATH = 120780    #heart attack


# annual cost
HEALTH_COST = [
    0,   # Well
    0,       # HTN
    0,       # SeverePE
    0,   # Eclampsia
]

HEALTH_UTILITY = [
    1.0,   # Well
    0.8,       # HTN
    0.6,       # SeverePE
    0.1,   # Eclampsia
]
