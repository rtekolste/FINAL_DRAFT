from enum import Enum
import InputDataApr23 as Data

class HealthStats(Enum):
    """ health states of patients with HIV """
    WELL = 0
    HTN = 1
    SEVEREPE = 2
    ECLAMPSIA = 3
    DEATH = 4

    
    ###NEED TO DISCUSS THE THERAPIES HERE#######
class Therapies(Enum):
    """ mono vs. combination therapy """
    NONE = 0
    MGSO4 = 1
    ANTICOAG = 2


class ParametersFixed():
    def __init__(self, therapy):
        # selected therapy
        self._therapy = therapy
        # simulation time step
        self._delta_t = Data.DELTA_T
        self._adjDiscountRate = Data.DISCOUNT * Data.DELTA_T
        # initial health state
        self._initialHealthState = HealthStats.WELL

        # annual treatment cost
        if self._therapy == Therapies.NONE:
            self._annualTreatmentCost = 0
        if self._therapy == Therapies.ANTICOAG:
            self._annualTreatmentCost = Data.COST_ANTICOAG

        # transition probability matrix of the selected therapy
        self._prob_matrix = []

        # calculate transition probabilities depending of which therapy options is in use
        if therapy == Therapies.NONE:
            self._prob_matrix = Data.TRANS_MATRIX
        elif therapy == Therapies.MGSO4:
            self._prob_matrix = Data.TRANS_MATRIX_MGSO4
        else:
            self._prob_matrix = Data.TRANS_MATRIX_ANTICOAG

#annual state cvsots and utilities
        self._annualStateCosts = Data.HEALTH_COST
        self._annualStateUtilities = Data.HEALTH_UTILITY

# annual treatment cost
        if self._therapy == Therapies.MGSO4:
            self._annualTreatmentCost = Data.COST_MGSO4
        elif self._therapy == Therapies.ANTICOAG:
            self._annualTreatmentCost = Data.COST_ANTICOAG

    # adjusted discount rate
        self._adjDiscountRate = Data.DISCOUNT_RATE * Data.DELTA_T

    def get_initial_health_state(self):
        return self._initialHealthState

    def get_delta_t(self):
        return self._delta_t

    def get_adj_discount_rate(self):
        return self._adjDiscountRate

    def get_transition_prob(self, state):
        return self._prob_matrix[state.value]

    def get_annual_state_cost(self, state):
        if state == HealthStats.DEATH:
            return 0
        else:
            return self._annualStateCosts[state.value]

    def get_annual_state_utility(self, state):
        if state == HealthStats.DEATH:
            return 0
        else:
            return self._annualStateUtilities[state.value]

    def get_annual_treatment_cost(self):
        return self._annualTreatmentCost

####Get this checked...#####

def calculate_prob_matrix_anticoag():
    """ :returns transition probability matrix under anticoagulation use"""

    # create an empty matrix populated with zeroes
    prob_matrix = []
    for s in HealthStats:
        prob_matrix.append([0] * len(HealthStats))

    
   
