from  time import time
import models.memorymodel as memorymodel
import models.transitionmodel as transitionmodel

class MemoryModule:
    def __init__(self):
        self.seen = set()                    # Has the state been seen before?
        self.memory_transitions = {}         # Models, training data for transitions
        self.memory_evals = {}               # Models, training data for evals
    
    def get_info(self):
        print(len(self.seen), "states seen")
        print(len(self.memory))
        print(len(self.memory_transitions))
              
    
    def store(self, state, transition=None, eval=None):
        start = time()
        #print("Storing state:", state, transition, eval)
        # Either transition or eval must be provided
        assert transition is not None or eval is not None, "Either transition or eval must be provided"
        assert not (transition is None and eval is None), "Only one of transition or eval can be provided"
        # =======================================================================================
        # Check if state has been seen before
        if state in self.seen:
            # Check that eval is same
            if eval is not None:
                assert state in self.memory_evals[eval]["trn"], "Evaluation cannot change!"
        else:
            # Add state to seen
            self.seen.add(state)
        # =======================================================================================
        if transition is not None:
            datum = self.memory_transitions.get(transition)
            if datum is None:
                # Add to memory
                new_datum = {
                    "model": transitionmodel.TransitionModel([state], self.seen),
                    "trn": set([state]),
                }
                self.memory_transitions[transition] = new_datum
            else:
                # If state is not in memory, add it
                if state not in datum["trn"]:
                    datum["trn"].add(state)
                    datum["model"] = transitionmodel.TransitionModel(list(datum["trn"]), self.seen)
        if eval is not None:
            datum = self.memory_evals.get(eval)
            if datum is None:
                # Add to memory
                new_datum = {
                    "model": memorymodel.MemoryModel([state], self.seen),
                    "trn": set([state]),
                }
                self.memory_evals[eval] = new_datum
            else:
                # If state is not in memory, add it
                if state not in datum["trn"]:
                    datum["trn"].add(state)
                    datum["model"] = memorymodel.MemoryModel(list(datum["trn"]), self.seen)
        #print("Storing took:", time() - start)

    def retrieve_evals(self, state):
        evals = []
        for eval, datum in self.memory_evals.items():
            if datum['model'].test(state):
                evals.append(eval)
        return evals
    
    def retrieve_transitions(self, state):
        transitions = []
        for transition, datum in self.memory_transitions.items():
            if datum['model'].test(state):
                transitions.append(transition)
        return transitions