import read, copy
from util import *
from logical_classes import *

verbose = 0

class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument

        Args:
            fact (Fact): Fact we're searching for

        Returns:
            Fact: matching fact
        """
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument

        Args:
            rule (Rule): Rule we're searching for

        Returns:
            Rule: matching rule
        """
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB
        Args:
            fact_rule (Fact|Rule) - the fact or rule to be added
        Returns:
            None
        """
        printv("Adding {!r}", 1, verbose, [fact_rule])
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True
        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)
                else:
                    ind = self.rules.index(fact_rule)
                    self.rules[ind].asserted = True

    def kb_assert(self, fact_rule):
        """Assert a fact or rule into the KB

        Args:
            fact_rule (Fact or Rule): Fact or Rule we're asserting
        """
        printv("Asserting {!r}", 0, verbose, [fact_rule])
        self.kb_add(fact_rule)

    def kb_ask(self, fact):
        """Ask if a fact is in the KB

        Args:
            fact (Fact) - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        print("Asking {!r}".format(fact))
        if factq(fact):
            f = Fact(fact.statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            return bindings_lst if bindings_lst.list_of_bindings else []

        else:
            print("Invalid ask:", fact.statement)
            return []

    def kb_retract(self, fact):
        """Retract a fact from the KB

        Args:
            fact (Fact) - Fact to be retracted

        Returns:
            None
        """
        printv("Retracting {!r}", 0, verbose, [fact])
        ####################################################
        # Student code goes here
        # Only can retract fact, check if fact to be retracted exists
        if isinstance(fact, Fact) and fact in self.facts:
            retract_fact = self._get_fact(fact)
            # if fact is unsupported
            if len(retract_fact.supported_by) == 0:
                self.kb_retract_supports(retract_fact)
    
    def kb_retract_supports(self, fact_rule):
        """Retract a fact or rule from the KB
        Args:
            fact_rule (Fact|Rule) - the fact or rule to be retracted
        Returns:
            None
        """
        # retract facts that are no longer supported
        if isinstance(fact_rule, Fact) and fact_rule in self.facts:
            # if fact unsupported, but doesn't matter if it is asserted or inferred
            if len(fact_rule.supported_by) == 0:
                # for each fact that it supports, remove supported_by then retract
                for supported_fact in fact_rule.supports_facts:
                    sf = self._get_fact(supported_fact)
                    for sb in sf.supported_by:
                        if sb[0] == fact_rule:
                            sf.supported_by.remove(sb)
                    # retract supports fact
                    self.kb_retract_supports(sf)

                # for each rule that it supports, remove supported_by then retract
                for supported_rule in fact_rule.supports_rules:
                    sr = self._get_rule(supported_rule)
                    for sb in sr.supported_by:
                        if sb[0] == fact_rule:
                            sr.supported_by.remove(sb)
                    # retract supports rule
                    self.kb_retract_supports(sr)

                # remove the fact from the KB
                self.facts.remove(fact_rule)

        # retract inferred rules that are no longer supported
        elif isinstance(fact_rule, Rule) and fact_rule in self.rules:
            # if rule not asserted and unsupported
            if not fact_rule.asserted and len(fact_rule.supported_by) == 0:
                # for each fact that it supports, remove supported_by then retract
                for supported_fact in fact_rule.supports_facts:
                    sf = self._get_fact(supported_fact)
                    for sb in sf.supported_by:
                        if sb[1] == fact_rule:
                            sf.supported_by.remove(sb)
                    # retract supports fact
                    self.kb_retract_supports(sf)

                # for each rule that it supports, remove supported_by then retract
                for supported_rule in fact_rule.supports_rules:
                    sr = self._get_rule(supported_rule)
                    for sb in sr.supported_by:
                        if sb[1] == fact_rule:
                            sr.supported_by.remove(sb)
                    # retract supports rule
                    self.kb_retract_supports(sr)

                # remove the rule from the KB
                self.rules.remove(fact_rule)


class InferenceEngine(object):
    def fc_infer(self, fact, rule, kb):
        """Forward-chaining to infer new facts and rules

        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase

        Returns:
            Nothing
        """
        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
            [fact.statement, rule.lhs, rule.rhs])
        ####################################################
        # Student code goes here
        bindings = match(fact.statement, rule.lhs[0])
        if bindings:
            # only one lhs, so infer a fact
            if len(rule.lhs) == 1:
                new_fact_statement = instantiate(rule.rhs, bindings)
                new_fact = Fact(new_fact_statement, [[fact, rule]])
                kb.kb_assert(new_fact)
                fact.supports_facts.append(new_fact)
                rule.supports_facts.append(new_fact)
            # more than one lhs, so infer a rule
            else:
                new_lhs_statement = []
                for item in rule.lhs:
                    if item != rule.lhs[0]:
                        new_lhs_statement.append(instantiate(item, bindings))
                new_rhs_statement = instantiate(rule.rhs, bindings)
                new_rule = Rule([new_lhs_statement, new_rhs_statement], [[fact, rule]])
                kb.kb_assert(new_rule)
                fact.supports_rules.append(new_rule)
                rule.supports_rules.append(new_rule)
