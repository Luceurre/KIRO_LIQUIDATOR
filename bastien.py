from main import compute_score, json, parse, INSTANCE_FILES
from Instance import Instance
from oceane import solution
from Solution import Solution
from trivial_solution import update_solution

if __name__ == '__main__':
    size = 'large'
    file = parse(INSTANCE_FILES[size])
    instance = Instance(file)

    prod, client = solution(instance)
    prod, client, dist = update_solution((prod, client, {}), instance)
    sol = Solution(prod, client, dist)


    print(compute_score(size, sol.to_dict()))
