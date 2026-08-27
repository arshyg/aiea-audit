"""
Fuzzy Logic Tutorial: The Tipping Problem
Task 6- ArshiaGupta

Classic example (from official documentation).
Determine appropriate tip percentage using fuzzy rules instead of rigit if/else thresholds.
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

#fuzzy variables 
quality = ctrl.Antecedent(np.arange(0, 11, 1), 'quality')
service = ctrl.Antecedent(np.arange(0, 11, 1), 'service')
tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip')

#membership functions: good/avg/good
quality.automf(3, names=['poor', 'average', 'good'])
service.automf(3, names=['poor', 'average', 'good'])

#custom membership functions: low/med/high
tip['low'] = fuzz.trimf(tip.universe, [0, 0, 13])
tip['medium'] = fuzz.trimf(tip.universe, [0, 13, 25])
tip['high'] = fuzz.trimf(tip.universe, [13, 25, 25])

#fuzzy rules- aka when should you tip how much
rule1 = ctrl.Rule(quality['poor'] | service['poor'], tip['low'])
rule2 = ctrl.Rule(service['average'], tip['medium'])
rule3 = ctrl.Rule(service['good'] | quality['good'], tip['high'])

#control system
tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

#example run
tipping.input['quality'] = 6.5
tipping.input['service'] = 9.8
tipping.compute()

print(f"Food quality: 6.5/10")
print(f"Service quality: 9.8/10")
print(f"Computed tip: {tipping.output['tip']:.2f}%")

print("\n--- Additional test cases ---")
test_cases = [
    (2.0, 2.0),   # poor food, poor service
    (5.0, 5.0),   # average both
    (9.0, 9.0),   # great both
    (2.0, 9.0),   # poor food, great service
]

for q, s in test_cases:
    tipping.input['quality'] = q
    tipping.input['service'] = s
    tipping.compute()
    print(f"quality={q}, service={s}  ->  tip={tipping.output['tip']:.2f}%")

