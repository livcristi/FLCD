class FiniteAutomaton:
    def __init__(self):
        self.__states = []
        self.__alphabet = []
        self.__transitions = {}
        self.__initial_state = None
        self.__final_states = []

    def get_states(self):
        return self.__states

    def get_alphabet(self):
        return self.__alphabet

    def get_transitions(self):
        return self.__transitions

    def get_initial_state(self):
        return self.__initial_state

    def get_final_states(self):
        return self.__final_states

    def read_from_file(self, filename):
        # Check if the file data is valid
        if not self.__is_file_data_valid(filename):
            return None
        self.__clear_fields()
        with open(filename) as inp_file:
            # Read the valid states, alphabet, initial state and final states
            self.__states = inp_file.readline().strip().split()
            self.__alphabet = inp_file.readline().strip().split()
            self.__initial_state = inp_file.readline().strip().split()[0]
            self.__final_states = inp_file.readline().strip().split()

            # Read the transition operations
            for line in inp_file.readlines():
                initial_state, term, final_state = line.strip().split()
                if (initial_state, term) not in self.__transitions:
                    self.__transitions[(initial_state, term)] = [final_state]
                else:
                    self.__transitions[(initial_state, term)].append(final_state)
        return self

    def is_dfa(self):
        return self.__initial_state and all(len(result) <= 1 for result in self.__transitions.values())

    def verify_sequence(self, sequence):
        # Check if the FA is a DFA
        if not self.is_dfa():
            return None
        current_state = self.__initial_state
        while len(sequence) > 0:
            # Get the current 'letter' (token) from the sequence
            current_token = sequence[0]
            sequence = sequence[1:]

            # Check if there is a transition with the current state and token
            if (current_state, current_token) not in self.__transitions.keys():
                return False
            current_state = self.__transitions[(current_state, current_token)][0]

        if current_state in self.__final_states:
            return True
        else:
            return False

    def __clear_fields(self):
        self.__states = []
        self.__alphabet = []
        self.__transitions = {}
        self.__initial_state = None
        self.__final_states = []

    @staticmethod
    def __is_file_data_valid(filename):
        with open(filename) as inp_file:
            lines = inp_file.readlines()

            # Retrieve the states
            if len(lines) < 4:
                # The file must have at least 4 rows (states, alphabet, initial, final state)
                return False

            valid_states = lines[0].strip().split()

            # Retrieve the alphabet
            alphabet = lines[1].strip().split()

            # Retrieve the initial states
            line = lines[2].strip().split()
            if len(line) > 1 or line[0] not in valid_states:
                # The line with the initial state must have one value only, which is a valid state
                return False

            # Retrieve the final states
            line = lines[3].strip().split()
            if any(state not in valid_states for state in line):
                # All final states must be valid
                return False

            # Retrieve the transitions
            for line in lines[4:]:
                tokens = line.strip().split()
                if len(tokens) != 3:
                    # Each transition must have 3 parts (start state, token, next state)
                    return False
                if (tokens[0] not in valid_states) or \
                        (tokens[1] not in alphabet) or \
                        (tokens[2] not in valid_states):
                    # Each part of the transition must be valid
                    return False
        return True
