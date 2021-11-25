import json
from typing import Set, List, Dict

from Instance import Instance
from main import parse, INSTANCE_FILES, compute_score
from oceane import solution


class Solution:
    def __init__(self, productionCenters: Set, clients: Dict):
        self.productionCenters = productionCenters
        self.clients = clients

    def to_dict(self):
        result = {
            "clients": [],
            "distributionCenters": [],
            "productionCenters": []
        }

        for index in self.clients.keys():
            result["clients"].append({
                "id": int(index + 1),
                "parent": int(self.clients[index] + 1)
            })

        for position in self.productionCenters:
            result["productionCenters"].append({
                "id": int(position + 1),
                "automation": 0
            })

        return result

if __name__ == '__main__':
    size = 'large'
    tiny = parse(INSTANCE_FILES[size])
    tiny_instance = Instance(tiny)

    prod, client = solution(tiny_instance)
    sol = Solution(prod, client)

    #compute_score(size, sol.to_dict())

    with open("./solutions/large.json", 'w') as file:
        json.dump(sol.to_dict(), file)

