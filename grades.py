"""Phys 267, Spring 2024 Marking Scheme Implementation

The marking schemes listed on the course outline will be adjusted to reduce the weight
of assignments and increase the weight of other components if that gives you a higher mark.

For example, suppose that you do well on 4 out of 5 of your assignments, but don't hand in an
assignment due to illness, self-declared absence, etc...  The scheme below, effectively
drops this assignment, uses your best 4 assignments, but reduces the weight of assignments in
your final mark.

Consider it a generalization of: "I will drop your worst assignment if it helps you."
I'll drop arbitrarily many assignments, but increase weight of everything else if it helps you.

(I reserve the right to alter to remove any unintentional bugs.)

Jim Martin, Spring 2024
"""

import numpy as np

# put all your marks here, normalized so that 1.0 is full marks on that component:
all_marks = {"as":[0.93, 0.92, 0.95, 0.9, 1.0, 0.6, 0.6, 0],
             "midterm":0.95,
             "final_exam":0.95
            }

n_problem_sets = 8
assert len(all_marks["as"]) == n_problem_sets
    
s_as = sorted(all_marks["as"], reverse=True)

candidates = []

# use schemes on course outline:
schemes = [{"midterm":0.25, "final_exam":0.5, "assignments":0.25},
           {"midterm":0.0, "final_exam":0.75, "assignments":0.25},
           {"midterm":0.0, "final_exam":1.0, "assignments":0.0},]
           
for weights in schemes:
    assert (1.0 == sum([w for _, w in weights.items()]))
    min_except_weight = sum([w for k, w in weights.items() if k != "assignments"])
    except_assignments = sum([all_marks[k] * w for k, w in weights.items() if k != "assignments"]) / min_except_weight

    for n_drop in range(0, n_problem_sets + 1):
        except_weight = min_except_weight + (1 - min_except_weight) * n_drop / n_problem_sets
        best_assignments = 0 if n_drop == n_problem_sets else np.average(s_as[0:n_problem_sets - n_drop])
        candidates.append(except_weight * except_assignments +
                          (1.0 - except_weight) * best_assignments)
    
candidates.sort(reverse=True)
print("candidate marks: ", candidates)
print("final mark: ", candidates[0])   
