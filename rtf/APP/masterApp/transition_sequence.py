class TransitionSequence:
    def __init__(self, transitions: list):
        self.transitions = transitions[:]
        self.last_transition = ""

    def trigger_transition(self, transition: str) -> bool:
        if self.finished():
            return False

        if self.last_transition == transition:
            return True

        frontTransition = self.transitions[0]
        if frontTransition != transition:
            return False

        self.last_transition = self.transitions.pop(0)
        return True


    def finished(self):
        return len(self.transitions) == 0
