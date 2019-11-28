from __future__ import annotations
from typing import List, Dict, Optional


class MultipleInitialStateError(Exception):
    def __init__(self, *args, **kwargs):
        message = 'Initial state already exist'
        super().__init__(message)


class NoFinalStatesError(Exception):
    def __init__(self, *args, **kwargs):
        message = 'No final states were found'
        super().__init__(message)


class NoInitialStateError(Exception):
    def __init__(self, *args, **kwargs):
        message = 'No initial state was found'
        super().__init__(message)


class NullMove:
    name = 'Null move'

    def __init__(self):
        self.name = NullMove.name

    def __str__(self):
        return NullMove.name

    def __repr__(self):
        return NullMove.name


class DeadState:
    name = 'Dead state'

    def __init__(self):
        self.name = DeadState.name

    def __str__(self):
        return DeadState.name

    def __repr__(self):
        return DeadState.name


class EvaluationSession:
    def __init__(self, input_string: str):
        self.input_accepted: bool = False
        self.input_string: str = input_string


class Edge:
    def __init__(self, start_state: 'State', end_state: 'State', valid_moves: List[str], name=None):
        self.valid_moves: List[str] = valid_moves
        self.end_state: 'State' = end_state
        self.start_state: 'State' = start_state
        self.name: str = name or f'Edge from {start_state.name} to {end_state.name}'

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class State:
    def __init__(self, name: str):
        self.name: str = name
        self.edges: List[Edge] = []

    def __str__(self):
        return f'State {self.name}'

    def __repr__(self):
        return f"State {self.name}"

    def add_edge(self, end_state: State, valid_moves: List[str], name: str = None):
        edge: Edge = Edge(self, end_state, valid_moves, name=name)
        self.edges.append(edge)
        return edge


class FiniteAutomata:
    def __init__(self):
        self.vertices: Dict[str, State] = {}
        self.initial_state: State = None
        self.final_states: List[State] = []
        self.is_evaluating: bool = False
        self.evaluation_session: EvaluationSession = None

    def add_state(self, name: str, is_initial: bool = False, is_final: bool = False):
        if self.initial_state is not None and is_initial:
            raise MultipleInitialStateError

        state: State = State(name)
        self.vertices[name] = state
        self.initial_state = state if is_initial else self.initial_state
        if is_final:
            self.final_states.append(state)
        return state

    def get_state_by_name(self, name: str):
        return self.vertices.get(name, 'State does not exist')

    def start_evaluation_session(self, input_string: str):
        self.is_evaluating: bool = True
        self.evaluation_session = EvaluationSession(input_string)

    def end_evaluations_session(self):
        self.is_evaluating: bool = False
        self.evaluation_session = None

    def accept_input(self):
        self.evaluation_session.input_accepted = True
        return None

    @property
    def input_accepted(self):
        return self.evaluation_session.input_accepted

    @property
    def input_string(self):
        return self.evaluation_session.input_string

    def evaluate_input(self, input_string: str):
        if self.initial_state is None:
            raise NoInitialStateError

        if self.final_states == []:
            raise NoFinalStatesError

        self.start_evaluation_session(input_string)
        self.evaluate_state(0, self.initial_state)

        if self.input_accepted:
            print("String accepted")
        else:
            print("String rejected")

        self.end_evaluations_session()

    def evaluate_state(self, current_input_index: int, current_state: State):
        if self.input_accepted or current_state is DeadState:
            return

        current_input_char = None
        valid_move = False

        try:
            current_input_char: str = self.input_string[current_input_index]
        except IndexError:
            return self.accept_input() if current_state in self.final_states else None

        for edge in current_state.edges:
            for move in edge.valid_moves:
                if move is NullMove or move == current_input_char:
                    valid_move = True
                    next_input_index = current_input_index if move is NullMove else current_input_index + 1
                    next_state: State = edge.end_state
                    self.evaluate_state(
                        next_input_index,
                        next_state
                    )
        if not valid_move:
            self.evaluate_state(
                current_input_index+1,
                DeadState
            )

        return


if __name__ == "__main__":
    # automata1 = FiniteAutomata()
    # state11 = automata1.add_state(name='A', is_initial=True)
    # state12 = automata1.add_state(name='B', is_final=True)
    # state11.add_edge(state12, ['a'])
    # automata1.evaluate_input('a')

    # automata for a*b
    # automata = FiniteAutomata()
    # state1 = automata.add_state(name='A', is_initial=True)
    # state2 = automata.add_state(name='B', is_final=True)
    # state1.add_edge(state1, ['a'])
    # state1.add_edge(state2, ['b'])
    # automata.evaluate_input('aaab')

    # automata for abb
    # automata = FiniteAutomata()
    # state1 = automata.add_state(name='A', is_initial=True)
    # state2 = automata.add_state(name='B')
    # state3 = automata.add_state(name='D',)
    # state4 = automata.add_state(name='C', is_final=True)
    # state1.add_edge(state2, ['a'])
    # state2.add_edge(state3, ['b'])
    # state3.add_edge(state4, ['b'])
    # automata.evaluate_input('abb')

    # nfa that accepts 00 and 11 at the end of a string containing 0, 1 in it
    nfa = FiniteAutomata()
    state1 = nfa.add_state(name='A', is_initial=True)
    state2 = nfa.add_state(name='A')
    state3 = nfa.add_state(name='A')
    state4 = nfa.add_state(name='A', is_final=True)

    state1.add_edge(state1, valid_moves=['0', '1'])
    state1.add_edge(state2, valid_moves=['0'])
    state1.add_edge(state3, valid_moves=['1'])
    state2.add_edge(state4, valid_moves=['0'])
    state3.add_edge(state4, valid_moves=['1'])

    nfa.evaluate_input('01010100')
