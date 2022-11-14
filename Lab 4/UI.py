class UI:
    def __init__(self, FA):
        self.__FA = FA

    def __read_from_file(self):
        filename = input('Enter the filename: ')
        response = self.__FA.read_from_file(filename)
        if response is not None:
            print('The Finite Automaton was read from the file')
        else:
            print('The given file does not have data in a valid format. The FA was not read')

    def __display_states(self):
        print('The states are: ' + str(self.__FA.get_states()))

    def __display_alphabet(self):
        print('The alphabet is: ' + str(self.__FA.get_alphabet()))

    def __display_transitions(self):
        transitions = self.__FA.get_transitions()
        print('The transitions are: ')
        for state_transitions in transitions:
            for result in transitions[state_transitions]:
                print('({}, {}) -> {}'.format(state_transitions[0], state_transitions[1], result))

    def __display_initial_state(self):
        print(self.__FA.get_initial_state())

    def __display_final_states(self):
        print(self.__FA.get_final_states())

    def __check_dfa(self):
        if self.__FA.is_dfa():
            print('The FA is DFA')
        else:
            print('The FA is not DFA')

    def __verify_sequence(self):
        user_sequence = input('Enter a sequence: ')
        result = self.__FA.verify_sequence(user_sequence)
        if result is None:
            print('The FA is not a DFA. Cannot check sequence')
        elif result:
            print('The sequence is accepted by the DFA')
        else:
            print('The sequence is not accepted by the DFA')

    @staticmethod
    def __print_menu():
        print('0. Close the menu')
        print('1. Read FA from file')
        print('2. Display the states of the FA')
        print('3. Display the alphabet of the FA')
        print('4. Display the transitions of the FA')
        print('5. Display the initial state of the FA')
        print('6. Display the final states of the FA')
        print('7. Check if the FA is a DFA')
        print('8. Verify a sequence')

    def run(self):
        options = {'1': self.__read_from_file, '2': self.__display_states, '3': self.__display_alphabet,
                   '4': self.__display_transitions, '5': self.__display_initial_state, '6': self.__display_final_states,
                   '7': self.__check_dfa, '8': self.__verify_sequence}

        is_over = False

        while not is_over:
            self.__print_menu()
            user_input = input('Enter your option: ').strip()
            if user_input == '0':
                is_over = True
            elif user_input in options:
                options[user_input]()
            else:
                print('Incorrect input! Please try again')
