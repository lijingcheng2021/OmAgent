import itertools
import operator

# Define the numbers and the target result
numbers = [4, 7, 8, 9]
target = 24

# Define the operations
operations = [operator.add, operator.sub, operator.mul, operator.truediv]
operation_symbols = ['+', '-', '*', '/']

# Function to evaluate expressions
def evaluate_expression(nums, ops):
    result = nums[0]
    for i in range(len(ops)):
        result = ops[i](result, nums[i + 1])
    return result

# Generate all permutations of numbers and operations
results = []
for num_perm in itertools.permutations(numbers):
    for ops in itertools.product(operations, repeat=len(numbers) - 1):
        try:
            if evaluate_expression(num_perm, ops) == target:
                expression = f'{num_perm[0]} {operation_symbols[operations.index(ops[0])]} {num_perm[1]} {operation_symbols[operations.index(ops[1])]} {num_perm[2]} {operation_symbols[operations.index(ops[2])]} {num_perm[3]}'
                results.append(expression)
        except ZeroDivisionError:
            continue

results