import pytest
from masterApp.sequence_container import SequenceContainer


class TestSequenceContainer:

    def setup_method(self):
         self.hasError = False
         self.isFinished = False

    def TriggerError(self):
        self.hasError = True

    def TriggerFinished(self):
        self.isFinished = True

    def test_can_create_container(self):
        seq = SequenceContainer(["a", "b"], [1,2], None, None)

    def test_can_trigger_transition_for_all_members(self):
        seq = SequenceContainer(["a", "b"], [1,2], None, lambda x, y: self.TriggerError())
        assert( True == seq.trigger_transition(1, "a"))
        assert( True == seq.trigger_transition(2, "a"))

    def test_trigger_transition_calls_error_on_error(self):
        seq = SequenceContainer(["a", "b"], [1,2], None, lambda x, y: self.TriggerError())
        assert( False == seq.trigger_transition(1, "c"))
        assert( True == self.hasError)

    def test_trigger_transition_calls_finished_on_finish(self):
        seq = SequenceContainer(["a", "b"], [1,2], lambda: self.TriggerFinished(), lambda x, y: self.TriggerError())
        seq.trigger_transition(1, "a")
        seq.trigger_transition(1, "b")
        assert(False == self.isFinished)
        seq.trigger_transition(2, "a")
        seq.trigger_transition(2, "b")
        assert(True == self.isFinished)

    def test_trigger_transition_with_bad_id_triggers_error(self):
        self.hasError = False
        seq = SequenceContainer(["a", "b"], [1,2], lambda: self.TriggerFinished(), lambda x,y: self.TriggerError())
        seq.trigger_transition(7, "a")
        assert(True == self.hasError)