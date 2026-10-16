"""Independent semantic examples. No bpy dependency and no claim of backend coverage."""
from math import isclose, sqrt
import json


def repeat(initial, count, body, border=None):
    state = initial
    trace = [initial]
    for iteration in range(max(0, count)):
        state = body(state, iteration, border)
        trace.append(state)
    return state, trace


def affine(initial, count, a, b):
    return repeat(initial, count, lambda x, i, p: p[0]*x+p[1], (a, b))


def fibonacci(count):
    return repeat((0, 1), count, lambda old, i, _: (old[1], old[0]+old[1]))


def index_sum(count):
    return repeat(0, count, lambda total, i, _: total+i)


def sqrt_newton(c, initial, count):
    if c < 0 or initial <= 0:
        raise ValueError('This example requires c >= 0 and initial > 0')
    return repeat(initial, count, lambda x, i, _: (x+c/x)*0.5)


def accumulate_positions(count):
    # Tuple state encodes simultaneous update from old values.
    return repeat((0, ()), count, lambda old, i, _: (old[0]+1, old[1]+(old[0],)))


def nested_sum(outer_count, inner_count):
    def outer(total, i, _):
        return repeat(total, inner_count, lambda value, j, outer_i: value+10*outer_i+j, i)[0]
    return repeat(0, outer_count, outer)


def border_usage(iteration_flags):
    return any(iteration_flags)


def side_effect_indices(iteration_count, registered):
    return [i for i in registered if 0 <= i < max(0, iteration_count)]


def parameter_maps(state_items, border_links):
    # Simplified interface with no reference sets.
    # Wrapper inputs: [N, states..., borders..., output_usage...]
    # Wrapper outputs: [states..., input_usage(N, states...), border_usage...]
    inputs_num = 1+state_items+border_links+state_items
    iteration_usage_index = state_items
    outputs_num = state_items+1+state_items+border_links
    return {
        'inputs': list(range(1, inputs_num)),
        'outputs': [i for i in range(outputs_num) if i != iteration_usage_index],
        'iteration_usage_index': iteration_usage_index,
    }


def validate():
    checks = []
    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    for n in (-8, -1, 0, 1, 2, 3, 10):
        result, trace = repeat(7, n, lambda x, i, _: x+1)
        check(f'count/{n}', result == 7+max(0, n))
        check(f'trace/{n}', len(trace) == max(0, n)+1)
    check('zero_identity', repeat((2, 7), 0, lambda s, i, _: (0, 0))[0] == (2, 7))
    check('affine/3', affine(1, 3, 2, 1) == (15, [1, 3, 7, 15]))
    check('fibonacci/5', fibonacci(5)[0] == (5, 8))
    check('index_sum/3', index_sum(3)[0] == 3)
    check('index_sum/5', index_sum(5)[0] == 10)
    check('sqrt_newton/5', isclose(sqrt_newton(2, 1, 5)[0], sqrt(2), abs_tol=1e-12))
    check('accumulation/0', accumulate_positions(0)[0] == (0, ()))
    check('accumulation/3', accumulate_positions(3)[0] == (3, (0, 1, 2)))
    check('nested/2x3', nested_sum(2, 3)[0] == 36)
    check('nested/empty_outer', nested_sum(0, 3)[0] == 0)
    check('nested/empty_inner', nested_sum(2, 0)[0] == 0)
    check('border/or', border_usage([False, True, False]))
    check('border/none', not border_usage([False, False]))
    check('border/zero', not border_usage([]))
    check('side_effect/filter', side_effect_indices(2, [-1, 0, 99]) == [0])
    check('side_effect/zero', side_effect_indices(0, [0, 1]) == [])
    check('mapping/2x1', parameter_maps(2, 1) == {
        'inputs': [1, 2, 3, 4, 5], 'outputs': [0, 1, 3, 4, 5], 'iteration_usage_index': 2})
    # Counterexample: repeatedly using initial instead of the preceding result.
    wrong = 0
    for _ in range(3):
        wrong = 0+1
    check('counterexample/broken_chain', wrong != repeat(0, 3, lambda x, i, _: x+1)[0])
    a, b = 0, 1
    for _ in range(5):
        a = b
        b = a+b
    check('counterexample/sequential_update', (a, b) != fibonacci(5)[0])
    return {'scope': 'independent semantic model, not Blender integration',
            'passed': len(checks), 'checks': checks,
            'examples': {'affine': affine(1, 3, 2, 1), 'fibonacci': fibonacci(5),
                         'nested': nested_sum(2, 3), 'parameter_maps': parameter_maps(2, 1)}}


if __name__ == '__main__':
    print(json.dumps(validate(), ensure_ascii=False, indent=2))
