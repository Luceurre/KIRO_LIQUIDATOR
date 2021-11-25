if __name__ == '__main__':
    size = 'large'
    tiny = parse(INSTANCE_FILES[size])
    tiny_instance = Instance(tiny)

    prod, client = solution(tiny_instance)
    sol = Solution(prod, client)

    compute_score(size, sol.to_dict())

    with open("./solutions/large.json", 'w') as file:
        json.dump(sol.to_dict(), file)