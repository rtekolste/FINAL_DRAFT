import ParameterClassesApr23 as P
import MarkovModelApr23 as MarkovCls
import SupportMarkovModelApr23 as SupportMarkov

# simulate no therapy
# create a cohort
cohort_none = MarkovCls.Cohort(id=0, therapy=P.Therapies.NONE)
# simulate cohort
simOutputs_none = cohort_none.simulate()

# simulate anticoagulation therapy
cohort_anticoag = MarkovCls.Cohort(id=1, therapy=P.Therapies.MGSO4)
simOutputs_anticoag = cohort_anticoag.simulate()

SupportMarkov.draw_survival_curves_and_histograms(simOutputs_none, simOutputs_anticoag)

SupportMarkov.print_outcomes(simOutputs_none, "No therapy")
SupportMarkov.print_outcomes(simOutputs_anticoag, "Anticoagulation theraoy")

SupportMarkov.print_comparative_outcomes(simOutputs_none, simOutputs_anticoag)

SupportMarkov.report_CEA_CBA(simOutputs_none, simOutputs_anticoag)

print("When the estimates of cost and utility are based on 2,000 simulated patients, "
      "the confidence interval of the net monetary benefit curve is too wide to make a "
      "recommendation.",
      "\nIncreasing the number of simulated patients to 20,000 or larger provides suficient confidence "
      "to recommend adopting this Anticoagulation drug "
      "if the decision maker's willingness-to-pay is at least $23,000 per QALY gained.")
