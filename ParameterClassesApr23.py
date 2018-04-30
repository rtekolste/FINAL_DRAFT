from enum import Enum
import numpy as np
import scipy.stats as stat
import math as math
import HW11.InputDataApr23 as Data
import scr.MarkovClasses as SupportLibrary
import scr.RandomVariantGenerators as Random

class HealthStats(Enum):
    """ health states of patients with HIV """
    WELL = 0
    HTN = 1
    SEVEREPE = 2
    ECLAMPSIA = 3

    
    ###NEED TO DISCUSS THE THERAPIES HERE#######
class Therapies(Enum):
    """ mono vs. combination therapy """
    BASELINE = 0
    SUPPLIES_NO_TRAINING = 1
    BETTER_TRAINING = 2
    BETTER_SUPPLIES_AND_TRAINING = 3


class ParametersFixed():
    def __init__(self, therapy):
        # selected therapy
        self._therapy = therapy
        # simulation time step
        self._delta_t = Data.DELTA_T
        self._adjDiscountRate = Data.DISCOUNT * Data.DELTA_T
        # initial health state
        self._initialHealthState = HealthStats.WELL

        ##THIS IS CHECKED
        # cost treatment per preg
        if self._therapy == Therapies.BASELINE:
            self._annualTreatmentCost = 0
        elif self._therapy == Therapies.SUPPLIES_NO_TRAINING:
            self._annualTreatmentCost = Data.COST_SUPPLIES
        elif self._therapy == Therapies.BETTER_TRAINING:
            self._annualTreatmentCost = Data.COST_TRAINING
        else:
            self._annualTreatmentCost = Data.COST_TRAINING + Data.COST_SUPPLIES
            

        # transition probability matrix of the selected therapy
        self._prob_matrix = []
        self._continuous_matrix = [ ]
        # calculate transition probabilities depending of which therapy options is in use
#        if therapy == Therapies.BASELINE:
#            self._prob_matrix = Data.BASELINE_MATRIX
#        elif therapy == Therapies.SUPPLIES_NO_TRAINING:
#            self._prob_matrix = Data.SUPPLIES_NO_TRAINING_MATRIX
#        elif therapy == Therapies.BETTER_TRAINING:
#            self._prob_matrix = Data.BETTER_TRAINING_MATRIX
#        else:
#            self._prob_matrix = Data.BETTER_SUPPLIES_AND_TRAINING_MATRIX
            
            
            #checked above

            # calculate transition probabilities depending of which therapy options is in use
        if therapy == Therapies.BASELINE:
            self._continuous_matrix = SupportLibrary.discrete_to_continuous(Data.BASELINE_MATRIX, Data.DELTA_T)
        elif therapy == Therapies.SUPPLIES_NO_TRAINING:
            self._continuous_matrix = SupportLibrary.discrete_to_continuous(Data.SUPPLIES_NO_TRAINING_MATRIX, Data.DELTA_T)
        elif therapy == Therapies.BETTER_TRAINING:
            self._continuous_matrix = SupportLibrary.discrete_to_continuous(Data.BETTER_TRAINING_MATRIX, Data.DELTA_T)
        else:
            self._continuous_matrix = SupportLibrary.discrete_to_continuous(Data.BETTER_SUPPLIES_AND_TRAINING_MATRIX, Data.DELTA_T)

        self._prob_matrix, p = SupportLibrary.continuous_to_discrete(self._continuous_matrix, Data.DELTA_T)

            
#annual state cvsots and utilities
        self._annualStateCosts = Data.HEALTH_COST
        self._annualStateUtilities = Data.HEALTH_UTILITY

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
        return self._annualStateCosts[state.value]

    def get_annual_state_utility(self, state):
        return self._annualStateUtilities[state.value]

    def get_annual_treatment_cost(self):
        return self._annualTreatmentCost
