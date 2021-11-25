import json
from typing import Set, List, Dict

from Instance import Instance
from main import parse, INSTANCE_FILES, compute_score
from oceane import solution
from trivial_solution import update_solution


class Solution:
    def __init__(self, productionCenters: Set, clients: Dict, distributionCenters: Dict):
        self.productionCenters = productionCenters
        self.clients = clients
        self.distributionCenters = distributionCenters

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

        for index in self.distributionCenters.keys():
            result["distributionCenters"].append({
                "id": int(index + 1),
                "parent": int(self.distributionCenters[index] + 1)
            })

        return result

if __name__ == '__main__':
    for size in ['small', 'large', 'medium']:
        tiny = parse(INSTANCE_FILES[size])
        tiny_instance = Instance(tiny)

        prod, client = solution(tiny_instance)
        prod, client, dist = update_solution((prod, client, {}), tiny_instance)

        sol = Solution(prod, client, dist)

        #compute_score(size, sol.to_dict())

        with open(f"./solutions/{size}_reloaded_6.json", 'w') as file:
            json.dump(sol.to_dict(), file)

