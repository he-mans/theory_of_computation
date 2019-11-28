from finite_automata import (
    FiniteAutomata,
    State,
    Edge,
    NullMove,
    DeadState,
    NoInitialStateError
)


class FiniteAutomataWithOutput(FiniteAutomata):
    def print_output(self, current_state=None, current_edge=None):
        pass

    def evaluate_input(self, input_string: str):
        print('output = ', end='')
        super().evaluate_input(input_string)


class MooreMachine(FiniteAutomataWithOutput):

    def add_state(self, name, output: str, is_initial=False, is_final=False):
        state = super().add_state(name, is_initial=is_initial, is_final=is_final)
        state.output = output
        return state

    def print_output(self, current_state=None, current_edge=None):
        if current_state is DeadState or self.input_accepted:
            pass
        else:
            print(current_state.output, end='')

    def evaluate_state(self, input_string, current_input_index, current_state):
        self.print_output(current_state=current_state)
        return super().evaluate_state(input_string, current_input_index, current_state)


class MealyState(State):
    def add_edge(self, end_state, valid_moves, output, name=None):
        edge = super().add_edge(end_state, valid_moves, name=name)
        edge.output = output
        return edge


class MealyMachine(FiniteAutomataWithOutput):

    def add_state(self, name: str, is_initial=False, is_final=False):
        if self.initial_state is not None and is_initial:
            raise NoInitialStateError

        state: MealyState = MealyState(name)
        self.vertices[name] = state
        self.initial_state = state if is_initial else self.initial_state
        if is_final:
            self.final_states.append(state)
        return state

    def print_output(self, current_state=None, current_edge=None):
        print(current_edge.output, end='')

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
                    self.print_output(current_state, edge)
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
    automata = MooreMachine()
    state1 = automata.add_state(name='A', output='1', is_initial=True)
    state2 = automata.add_state(name='B', output='0', is_final=True)
    state1.add_edge(state2, ['1'])
    state2.add_edge(state2, ['1'])
    automata.evaluate_input('1111111')

    automata = MealyMachine()
    state1 = automata.add_state('A', is_initial=True)
    state2 = automata.add_state('B', is_final=True)
    state1.add_edge(state2, ['1'], 0)
    state2.add_edge(state2, ['1'], 1)
    automata.evaluate_input('1111111')
