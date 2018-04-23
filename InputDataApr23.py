POP_SIZE = 2000     # cohort population size
SIM_LENGTH = 5   # length of simulation (years)
ALPHA = 0.05        # significance level for calculating confidence intervals
DELTA_T = 1         # years (length of time step, how frequently you look at the patient)
DISCOUNT = 0.03

# transition matrix
TRANS_MATRIX = [
    [0.00,  0.00,   0.00,   0.00], #Well
    [0.00,  0.00,   0.00,   0.00], #HTN
    [0.00,  0.00,   0.00,   0.00], #Stroke
    [0.00,  0.00,   0.00,   0.00], #Death
    [0.00,  0.00,   0.00,   0.00], #Detect
    [0.00,  0.00,   0.00,   0.00], #No Detect
    ]

# anticoagulation relative risk in reducing stroke incidence and stroke death while in “Post-Stroke”
RR_STROKE = 0.65
# anticoagulation relative risk in increasing mortality due to bleeding is 1.05.
RR_BLEEDING = 1.05

HEALTH_UTILITY = [
    1,  # well
    0.8865,  # stroke ONLY WHEN THE CYCLE LENGTH IS 1 YEAR
    0.9,  # post-stroke
    0  # dead
]

HEALTH_COST = [
    0,
    5000,  # stroke
    200,  # post-stroke /year
    0
]

DETECT_COST = 50
