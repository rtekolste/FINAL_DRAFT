import scr.SamplePathClasses as PathCls
import scr.StatisticalClasses as StatCls
import scr.RandomVariantGenerators as rndClasses
import scr.EconEvalClasses as EconCls
import ParameterClassesApr23 as P
import InputDataApr23 as Data

# patient class simulates patient, patient monitor follows patient, cohort simulates a cohort,
#  cohort outcome extracts info from simulation and returns it back


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
        while self._stateMonitor.get_if_eclampsia() and k*self._delta_t < sim_length:
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

    def get_eclampsia_time(self):
        """ returns the patient's eclampsia time"""
        return self._stateMonitor.get_eclampsia_time()

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
        self._eclampsiaTime = 0
        self._costUtilityOutcomes = PatientCostUtilityMonitor(parameters)
  
    def get_if_eclampsia(self):
        result = False
        if self._currentState in [P.HealthStats.ECLAMPSIA]:
            result = True
        return result

    def update(self, k, next_state):
        """
        :param k: current time step
        :param next_state: next state
        """
        # updates state of patient
        # if the patient has eclampsia, do nothing
        if not self.get_if_eclampsia():
            return

        # update time to eclampsia
        if next_state is P.HealthStats.ECLAMPSIA:
            self._eclampsiaTime = (k+0.5) * self._delta_t  # k is number of steps its been, delta t is length of time
            # step, the 0.5 is a half cycle correction

        self._costUtilityOutcomes.update(k, self._currentState, next_state)
        self._currentState = next_state

    def get_current_state(self):
        return self._currentState

    def get_total_discounted_cost(self):
        return self._costUtilityOutcomes.get_total_discounted_cost()

    def get_total_discounted_utility(self):
        return self._costUtilityOutcomes.get_total_discounted_utility()
    
    def get_eclampsia_time(self):
        """ returns the patient eclampsia time """
        # return survival time only if the patient has died
        if self.get_if_eclampsia():
            return self._eclampsiaTime
        else:
            return None


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

        self._eclampsiaTimes = []        # patients' eclampsia times
        self._utilities = []
        self._costs = []
        
        

        # eclampsia curve
        self._eclampsiaCurve = \
            PathCls.SamplePathBatchUpdate('Population size over time', id, simulated_cohort.get_initial_pop_size())

        # find patients' ec times
        for patient in simulated_cohort.get_patients():

            # get the patient EC time
            eclampsia_time = patient.get_eclampsia_time()
            if not (eclampsia_time is None):
                self._eclampsiaTimes.append(eclampsia_time)           # store the EC time of this patient
                self._eclampsiaCurve.record(eclampsia_time, -1)       # update the EC curve

            self._costs.append(patient.get_total_discounted_cost())
            self._utilities.append(patient.get_total_discounted_utility())

        # summary statistics
        self._sumStat_ECTime = StatCls.SummaryStat('Patient Eclampsia time', self._eclampsiaTimes)
        self._sumStat_cost = StatCls.SummaryStat('Patient discounted cost', self._costs)
        self._sumStat_utility = StatCls.SummaryStat('Patient discounted utility', self._utilities)


    def get_eclampsia_times(self):
        return self._eclampsiaTimes

    def get_sumStat_eclampsia_times(self):
        return self._sumStat_ECTime

    def get_eclampsia_curve(self):
        return self._eclampsiaCurve

    def get_costs(self):
        return self._costs

    def get_utilities(self):
        return self._utilities

    def get_sumStat_discounted_utility(self):
        return self._sumStat_utility

    def get_sumStat_discounted_cost(self):
        return self._sumStat_cost
