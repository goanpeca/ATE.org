from masterApp.transition_sequence import TransitionSequence
from typing import List

IdList = List[int]

class SequenceContainer:
    def __init__(self, seq: list, ids: IdList, on_complete: callable, on_error: callable):
        self.sequences = dict(map(lambda x: (x , TransitionSequence(seq[:])), ids))
        print(self.sequences)
        self.on_complete = on_complete
        self.on_error = on_error
        

    def trigger_transition(self, id: int, transition: str) -> bool:
        seq = self.sequences.get(id)
        if seq is None:
            self.on_error(id, transition)
            return False
        if not seq.trigger_transition(transition):
            self.on_error(id, transition)
            return False
        
        if all(x.finished() for x in self.sequences.values()):
            self.on_complete()

        return True
