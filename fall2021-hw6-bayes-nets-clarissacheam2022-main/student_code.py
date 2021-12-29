def ask(var, value, evidence, bn):
    # var - hypothesis variable
    # value - hypothesis value(True or False)
    # evidence - dict of evidence{variable:value(True or False)}

    # add hypothesis to evidence, use to calculate joint probability of hypothesis and evidence
    evidence_hypothesis = evidence.copy()
    evidence_hypothesis[var] = value

    # add negation hypothesis to evidence, use to calculate joint probability of ¬hypothesis and evidence in normalization constant
    evidence_negation_hypothesis = evidence.copy()
    evidence_negation_hypothesis[var] = not value

    # P(H,E) joint probability of hypothesis and evidence
    joint_probability = ask_recursive(bn.variable_names.copy(), evidence_hypothesis, bn)
    # P(¬H,E) joint probability of ¬hypothesis and evidence
    joint_probability_negation = ask_recursive(bn.variable_names.copy(), evidence_negation_hypothesis, bn)
    # normalization constant: P(H,E) + P(¬H,E)
    # joint probability of hypothesis and evidence plus joint probability of ¬hypothesis and evidence
    normalization = joint_probability + joint_probability_negation
    # P(H|E) probability of a hypothesis
    hypothesis_probability = joint_probability / normalization

    return hypothesis_probability

def ask_recursive(variable_names, evidence, bn):
    # variable_names - all variables
    # evidence - dict of evidence {variable:value(True or False)}

    var = variable_names.pop(0)
    variable_remaining = len(variable_names)
    # check if var is known variable
    if var in evidence:
        i = bn.variable_names.index(var)
        # P(var)
        probability = bn.variables[i].probability(evidence[var], evidence)
        if variable_remaining > 0:
            # P(var, v) = P(var) * P(v|var)
            return probability * ask_recursive(variable_names.copy(), evidence, bn)
        else:
            # no more next variable in the list, return current variable probability
            return probability
    else:
        # if the variable is unknown
        # we need to compute the sum of the joint probabilities when the unknown is True or False
        if variable_remaining > 0:
            # add unknown variable as True to evidence
            evidence_unknown_true = evidence.copy()
            evidence_unknown_true[var] = True
            # add unknown variable as False to evidence
            evidence_unknown_false = evidence.copy()
            evidence_unknown_false[var] = False

            i = bn.variable_names.index(var)

            # P(var)
            probability_unknown_true = bn.variables[i].probability(True, evidence)
            # P(¬var)
            probability_unknown_false = bn.variables[i].probability(False, evidence)
            # var is unknown, so need to find both P(var, v) and P(¬var, v)
            #  P(var, v)  = P(var) * P(v|var) + P(¬var) * (v|¬var)
            return (probability_unknown_true * ask_recursive(variable_names.copy(), evidence_unknown_true, bn)) + (
                        probability_unknown_false * ask_recursive(variable_names.copy(), evidence_unknown_false, bn))
        else:
            # no more next variable in the list, current unknown variable probability
            # unknown variable probability = probability_unknown_true + probability_unknown_false (which is always equal to 1)
            return 1

