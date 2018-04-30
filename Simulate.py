import ParameterClassesApr23 as P
import MarkovModelApr23 as MarkovCls
import SupportMarkovModelApr23 as SupportMarkov
import scr.SamplePathClasses as PathCls
import scr.FigureSupport as Figs

# create and cohort
cohort = MarkovCls.Cohort(
    id=0,
    therapy=P.Therapies.BASELINE)

output_baseline = cohort.simulate()

cohort2 = MarkovCls.Cohort(
    id=1,
    therapy=P.Therapies.BETTER_TRAINING)

output_training = cohort2.simulate()

cohort3 = MarkovCls.Cohort(
    id=2,
    therapy=P.Therapies.SUPPLIES_NO_TRAINING)

output_supplies = cohort3.simulate()

cohort4 = MarkovCls.Cohort(
    id=3,
    therapy=P.Therapies.BETTER_SUPPLIES_AND_TRAINING)

output_both = cohort4.simulate()


print("Successfully simulated")
