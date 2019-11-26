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
    def __init__(self):
        self.input_accepted: bool = False


class Edge:
    def __init__(self, start_state: 'Vertix', end_state: 'Vertix', valid_moves: List[str], name=None):
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

        vertix: State = State(name)
        self.vertices[name] = vertix
        self.initial_state = vertix if is_initial else self.initial_state
        if is_final:
            self.final_states.append(vertix)
        return vertix

    def get_vertix_by_name(self, name: str):
        return self.vertices.get(name, 'Vertix does not exist')

    def start_evaluation_session(self):
        self.is_evaluating: bool = True
        self.evaluation_session = EvaluationSession()

    def end_evaluations_session(self):
        self.is_evaluating: bool = False
        self.evaluation_session = None

    def accept_input(self):
        self.evaluation_session.input_accepted = True
        return None

    @property
    def input_accepted(self):
        return self.evaluation_session.input_accepted

    def evaluate_input(self, input_string: int):
        if self.initial_state is None:
            raise NoInitialStateError

        if self.final_states == []:
            raise NoFinalStatesError

        self.start_evaluation_session()
        self.evaluate_state(input_string, 0, self.initial_state)

        if self.evaluation_session.input_accepted:
            print("String accepted")
        else:
            print("String rejected")

        self.end_evaluations_session()

    def evaluate_state(self, input_string: str, current_input_index: int, current_state: State):
        if self.input_accepted or current_state is DeadState:
            return

        current_input_char = None

        try:
            current_input_char: str = input_string[current_input_index]
        except IndexError:
            return self.accept_input() if current_state in self.final_states else None

        for edge in current_state.edges:
            for move in edge.valid_moves:
                if move is NullMove or move == current_input_char:
                    next_input_index = current_input_index if move is NullMove else current_input_index + 1
                    next_state: State = edge.end_state
                    self.evaluate_state(
                        input_string,
                        next_input_index,
                        next_state
                    )

        return


if __name__ == "__main__":
    automata = FiniteAutomata()
    vertix1 = automata.add_state('A', is_initial=True)
    # vertix2 = graph.add_vertix('B')
    vertix3 = automata.add_state('C', is_final=True)
    # vertix4 = graph.add_vertix('D', is_final=True)
    vertix1.add_edge(DeadState, ['1'])
    # vertix2.add_edge(DeadState, ['1'])
    vertix1.add_edge(vertix3, [NullMove])
    # vertix3.add_edge(vertix3, ['1'])
    vertix3.add_edge(vertix3, ['2'])
    # vertix4.add_edge(vertix4, ['1'])
    automata.evaluate_input('22')
