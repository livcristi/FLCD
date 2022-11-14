from FiniteAutomaton import FiniteAutomaton
from UI import UI

if __name__ == '__main__':
    FA = FiniteAutomaton()
    ui = UI(FA)
    ui.run()
