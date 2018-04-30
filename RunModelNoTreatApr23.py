import ParameterClassesApr23 as P
import MarkovModelApr23 as MarkovCls
import SupportMarkovModelApr23 as SupportMarkov
import scr.SamplePathClasses as PathCls
import scr.FigureSupport as Figs

# create and cohort
cohort = MarkovCls.Cohort(
    id=0,
    therapy=P.Therapies.BASELINE)

simOutputs = cohort.simulate()
