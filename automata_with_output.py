from finite_automata import (
    FiniteAutomata,
    State,
    Edge,
    NullMove,
    DeadState,
    InitialStateError
)


class FiniteAutomataWithOutput(FiniteAutomata):
    def print_output(self, current_state, current_edge):
        pass

    def evaluate_input(self, input_string):
        print('output = ', end='')
        return super().evaluate_input(input_string)

    def evaluate_state(self, input_string: str, current_input_index: int, current_state: State):
        if self.input_accepted:
            return

        current_input_char: str = None

        try:
            current_input_char: str = input_string[current_input_index]
        except IndexError:
            if current_state in self.final_states:
                print('')
                self.accept_input()
            else:
                return

        if current_state is DeadState:
            return

        for edge in current_state.edges:
            for move in edge.valid_moves:
                if move == current_input_char or move == NullMove:
                    next_vertix: State = edge.end_state
                    next_input_index = current_input_index if move is NullMove else current_input_index + 1
                    self.print_output(current_state, edge)
                    self.evaluate_state(
                        input_string, next_input_index, next_vertix
                    )
        return


class MooreMachine(FiniteAutomataWithOutput):

    def add_state(self, name, output: str, is_initial=False, is_final=False):
        vertix = super().add_state(name, is_initial=is_initial, is_final=is_final)
        vertix.output = output
        return vertix

    def print_output(self, current_state, current_edge):
        print(current_state.output, end='')


class MealyState(State):
    def add_edge(self, end_state, valid_moves, output, name=None):
        edge = super().add_edge(end_state, valid_moves, name=name)
        edge.output = output
        return edge


class MealyMachine(FiniteAutomataWithOutput):

    def add_state(self, name: str, is_initial=False, is_final=False):
        if self.initial_state is not None and is_initial:
            raise InitialStateError(
                "Initial state already exist"
            )

        vertix: MealyState = MealyState(name)
        self.vertices[name] = vertix
        self.initial_state = vertix if is_initial else self.initial_state
        if is_final:
            self.final_states.append(vertix)
        return vertix

    def print_output(self, current_state, current_edge):
        print(current_edge.output, end='')


if __name__ == "__main__":
    automata = MooreMachine()
    vertix1 = automata.add_state('A', '1', is_initial=True)
    vertix2 = automata.add_state('B', '0', is_final=True)
    vertix1.add_edge(vertix2, ['1'])
    vertix2.add_edge(vertix2, ['1'])
    automata.evaluate_input('1111111')

    automata = MealyMachine()
    vertix1 = automata.add_state('A', is_initial=True)
    vertix2 = automata.add_state('B', is_final=True)
    vertix1.add_edge(vertix2, ['1'], 0)
    vertix2.add_edge(vertix2, ['1'], 1)
    automata.evaluate_input('1111111')
