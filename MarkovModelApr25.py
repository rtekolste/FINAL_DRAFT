import scr.SamplePathClasses as PathCls
import scr.StatisticalClasses as StatCls
import scr.RandomVariantGenerators as rndClasses
import scr.EconEvalClasses as EconCls
import ParameterClassesApr23 as P
import InputDataApr23 as Data

# patient class simulates patient, patient monitor follows patient, cohort simulates a cohort,
#  cohort outcome extracts info from simulation and returns it back

####NOTHING CHANGED HERE FROM CLASS NOTES######
class Patient:  # when you store in self then all the things in that class have access to it
    def __init__(self, id, parameters):
        """ initiates a patient
        :param id: ID of the patient
        :param parameters: parameter object
        """

        self._id = id
        # random number generator
        self._rng = None
        # parameters
        self._param = parameters
        # state monitor
        self._stateMonitor = PatientStateMonitor(parameters)
        # simulate time step
        self._delta_t = parameters.get_delta_t() # length of time step!

    def simulate(self, sim_length):
        """ simulate the patient over the specified simulation length """
        # random number generator for this patient
        self._rng = rndClasses.RNG(self._id)  # from now on use random number generator from support library

        k = 0  # current time step

        # while the patient is alive and simulation length is not yet reached
        while self._stateMonitor.get_if_alive() and k*self._delta_t < sim_length:
            # find transition probabilities of future state
            trans_prob = self._param.get_transition_prob(self._stateMonitor.get_current_state())
            # create an empirical distribution
            empirical_dist = rndClasses.Empirical(trans_prob)
            # sample from the empirical distribution to get a new state
            # (return an intger from {0, 1, 2, ...}
            new_state_index = empirical_dist.sample(self._rng) # pass RNG

            # update health state
            self._stateMonitor.update(k, P.HealthStats(new_state_index))

            # increment time step
            k += 1

####NOTHING CHANGED HERE FROM CLASS NOTES######
    def get_survival_time(self):
        """ returns the patient's survival time"""
        return self._stateMonitor.get_survival_time()

#####NEW ADDINS....
    def get_number_of_severePE(self):
        """ returns the patient's time to the Severe_PE state """
        return self._stateMonitor.get_num_of_severePE()
    def get_number_of_eclampsia(self):
        """ returns the patient's time to the EC state """
        return self._stateMonitor.get_num_of_Eclampsia()


####NOTHING CHANGED HERE FROM CLASS NOTES######
    def get_total_discounted_cost(self):
        return self._stateMonitor.get_total_discounted_cost()

    def get_total_discounted_utility(self):
        return self._stateMonitor.get_total_discounted_utility()


class PatientStateMonitor:
    """ to update patient outcomes (years survived, cost, etc.) throughout the simulation """
    def __init__(self, parameters):
        """
        :param parameters: patient parameters
        """
        # current health state
        self._currentState = parameters.get_initial_health_state()
        self._delta_t = parameters.get_delta_t()
        self._survivalTime = 0
        self._ifDevelopedPE = False
        self._ifDevelopedEC = False
        self._PEcount = 0
        self._ECcount = 0

        self._costUtilityOutcomes = PatientCostUtilityMonitor(parameters)

    def update(self, k, next_state):
        """
        :param k: current time step
        :param next_state: next state
        """
        # updates state of patient
        # if the patient has died, do nothing
        if not self.get_if_alive():
            return

        # update survival time
        if next_state is P.HealthStats.DEATH:
            self._survivalTime = (k+0.5) * self._delta_t  # k is number of steps its been, delta t is length of time
            # step, the 0.5 is a half cycle correction

        # update PE count
        if self._currentState == P.HealthStats.SEVEREPE:
            self._ifDevelopedPE = True
            self._PEcount += 1

        # update EC (eclampsia) count
        if self._currentState == P.HealthStats.ECLAMPSIA:
            self._ifDevelopedEC = True
            self._ECcount += 1

        self._costUtilityOutcomes.update(k, self._currentState, next_state)

        self._currentState = next_state

    def get_if_alive(self):
        result = True
        if self._currentState == P.HealthStats.DEATH:
            result = False
        return result

    def get_current_state(self):
        return self._currentState

    def get_survival_time(self):
        """ returns the patient survival time """
        # return survival time only if the patient has died
        if not self.get_if_alive():
            return self._survivalTime
        else:
            return None

    def get_num_of_severePE(self):
        return self._PEcount
    def get_num_of_Eclampsia(self):
        return self._ECcount



    def get_total_discounted_cost(self):
        return self._costUtilityOutcomes.get_total_discounted_cost()

    def get_total_discounted_utility(self):
        return self._costUtilityOutcomes.get_total_discounted_utility()


class PatientCostUtilityMonitor:

    def __init__(self, parameters):
        self._param = parameters
        self._totalDiscountedCost = 0
        self._totalDiscountedUtility = 0

    def update(self, k, current_state, next_state):
        cost = 0.5*(self._param.get_annual_state_cost(current_state)+(self._param.get_annual_state_cost(next_state))) \
               * self._param.get_delta_t()

        utility = 0.5 * (self._param.get_annual_state_utility(current_state) +
                         (self._param.get_annual_state_utility(next_state))) * self._param.get_delta_t()
        if next_state is P.HealthStats.DEATH:
            cost += 0.5*self._param.get_annual_treatment_cost() * self._param.get_delta_t()
        else:
            cost += 1*self._param.get_annual_treatment_cost() * self._param.get_delta_t()
        self._totalDiscountedCost += EconCls.pv(cost, self._param.get_adj_discount_rate()/2, 2*k+1)
        self._totalDiscountedUtility += EconCls.pv(utility, self._param.get_adj_discount_rate()/2, 2*k+1)

    def get_total_discounted_cost(self):
        return self._totalDiscountedCost

    def get_total_discounted_utility(self):
        return self._totalDiscountedUtility


class Cohort:

    def __init__(self, id, therapy):
        """ create a cohort of patients
        :param id: an integer to specify the seed of the random number generator
        """
        self._initial_pop_size = Data.POP_SIZE
        self._patients = []      # list of patients

        # populate the cohort
        for i in range(self._initial_pop_size):
            # create a new patient (use id * pop_size + i as patient id)
            patient = Patient(id * self._initial_pop_size + i, P.ParametersFixed(therapy))
            # add the patient to the cohort
            self._patients.append(patient)

    def simulate(self):
        """ simulate the cohort of patients over the specified number of time-steps
        :returns outputs from simulating this cohort
        """

        # simulate all patients
        for patient in self._patients:
            patient.simulate(Data.SIM_LENGTH)

        # return the cohort outputs
        return CohortOutputs(self)

    def get_initial_pop_size(self):
        return self._initial_pop_size

    def get_patients(self):
        return self._patients


class CohortOutputs:
    def __init__(self, simulated_cohort):
        """ extracts outputs from a simulated cohort
        :param simulated_cohort: a cohort after being simulated
        """

        self._survivalTimes = []        # patients' survival times
        self._times_to_PE = []        # patients' times to PE
        self._count = []
        self._count_PE = []         #patients' # of PE count
        self._count_EC = []             #patients' EC count
        self._utilities = []
        self._utilitiesPE = []
        self._utilitiesEC = []

        self._costs = []
        self._costsPE = []
        self._costsEC = []


        # survival curve
        self._survivalCurve = \
            PathCls.SamplePathBatchUpdate('Population size over time', id, simulated_cohort.get_initial_pop_size())

        # find patients' survival times
        for patient in simulated_cohort.get_patients():

            # get the patient survival time
            survival_time = patient.get_survival_time()
            if not (survival_time is None):
                self._survivalTimes.append(survival_time)           # store the survival time of this patient
                self._survivalCurve.record(survival_time, -1)       # update the survival curve


###Normal Counter####
            #count = patient.get_number_of_stroke()
            #self._count.append(count_PE)
            #self._costs.append(patient.get_total_discounted_costPE())
            #self._utilities.append(patient.get_total_discounted_utilityPE())


###PE Counter####
            count_PE = patient.get_number_of_severePE()
            self._count_PE.append(count_PE)
            self._costsPE.append(patient.get_total_discounted_costPE())
            self._utilitiesPE.append(patient.get_total_discounted_utilityPE())

###Eclampsia Counter####
            count_EC = patient.get_number_of_eclampsia()
            self._count_EC.append(count_EC)
            self._costsEC.append(patient.get_total_discounted_costEC())
            self._utilities.append(patient.get_total_discounted_utilityPE())



 # NEW###### PE Summary statistics
        self._sumStat_survivalTime = StatCls.SummaryStat('Patient survival time', self._survivalTimes)
        self._sumState_number_PE = StatCls.SummaryStat('Time until Severe Pre-Eclampsia', self._count_PE)
        self._sumStat_costPE = StatCls.SummaryStat('Patient discounted cost', self._costsPE)
        self._sumStat_utilityPE = StatCls.SummaryStat('Patient discounted utility', self._utilitiesPE)


# NEW###### EC Summary statistics
        self._sumStat_survivalTime = StatCls.SummaryStat('Patient survival time', self._survivalTimes)
        self._sumState_number_EC = StatCls.SummaryStat('Time until EC', self._count_EC)
        self._sumStat_costEC = StatCls.SummaryStat('Patient discounted cost', self._costsEC)
        self._sumStat_utilityEC = StatCls.SummaryStat('Patient discounted utility', self._utilitiesEC)

    ##Counts
    def get_if_developed_severePE(self): #PE
        return self._count_PE
    def get_if_developed_eclampsia(self): #EC
        return self._count_EC

#survival times---- ####NEED TO ASK ABOUT THIS ONE!!!!!#######
    def get_survival_times(self):
        return self._survivalTimes
    def get_sumStat_survival_times(self):
        return self._sumStat_survivalTime
    def get_survival_curve(self):
        return self._survivalCurve

#counts
    def get_sumStat_count_PE(self):
        return self._sumState_number_PE
    def get_sumStat_count_EC(self):
        return self._sumState_number_EC

#costs per
    def get_costsPE(self):
        return self._costsPE
    def get_costsEC(self):
        return self._costsEC

##Utility
    def get_utilitiesPE(self):
        return self._utilitiesPE
    def get_utilitiesEC(self):
        return self._utilitiesEC


###SumStatUtil
    def get_sumStat_discounted_utilityPE(self):
        return self._sumStat_utilityPE
    def get_sumStat_discounted_utilityEC(self):
        return self._sumStat_utilityEC


###SumStatCost
    def get_sumStat_discounted_costPE(self):
        return self._sumStat_costPE
    def get_sumStat_discounted_costEC(self):
        return self._sumStat_costEC
    
