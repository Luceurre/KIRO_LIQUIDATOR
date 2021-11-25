# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json

from Instance import Instance


INSTANCE_FILES = {
    'tiny': './instances/KIRO-tiny.json',
    'small': './instances/KIRO-small.json',
    'medium': './instances/KIRO-medium.json',
    'large': './instances/KIRO-large.json'
}

def parse(filename):
    with open(filename, 'r') as instance_file:
        return json.load(instance_file)


def compute_score(instance_type, solution):
    file = INSTANCE_FILES[instance_type]
    instance = Instance(parse(file))
    score = 0
    productionCenters = {}
    productionCentersUsage = {}
    distributionCenters = {}

    ### BUILDING COSTS ###
    for productionCenter in solution["productionCenters"]:
        productionCenters[str(productionCenter["id"])] = productionCenter["automation"]
        score += instance.buildingCosts.productionCenter
        if productionCenter["automation"] == 1:
            score += instance.buildingCosts.automationPenalty
    for distributionCenter in solution["distributionCenters"]:
        distributionCenters[str(distributionCenter["id"])] = distributionCenter["parent"]
        score += instance.buildingCosts.distributionCenter

    ### PRODUCTION COSTS ###
    for client in solution["clients"]:
        if str(client["parent"]) in productionCenters.keys():
            productionCentersUsage[str(client["parent"])] = instance.clients[client["id"]-1] + productionCentersUsage.get(
                str(client["parent"]), 0)
            score += instance.clients[client["id"]-1] * instance.productionCosts.productionCenter
            if productionCenters[str(client["parent"])] == 1:
                score -= instance.clients[client["id"]-1] * instance.productionCosts.automationBonus
        if str(client["parent"]) in distributionCenters.keys():
            score += instance.clients[client["id"]-1] * instance.productionCosts.distributionCenter
            productionCenter = productionCenters[str(distributionCenters[str(client["parent"])])]
            productionCentersUsage[productionCenter] = instance.clients[client["id"]-1] + productionCentersUsage.get(
                productionCenter, 0)
            score += instance.productionCosts.productionCenter
            if productionCenter == 1:
                score -= instance.clients[client["id"]-1] * instance.productionCosts.automationBonus

    ### ROUTING COSTS ###
    for client in solution["clients"]:
        if str(client["parent"]) in productionCenters.keys():
            score += instance.clients[client["id"]-1] * instance.routingCosts.secondary * instance.siteClientDistances[client["parent"]-1, client["id"]-1]
        if str(client["parent"]) in distributionCenters.keys():
            score += instance.clients[client["id"]-1] * instance.routingCosts.secondary * instance.siteClientDistances[client["parent"], client["id"]]
            productionCenter = productionCenters[str(distributionCenters[str(client["parent"])])]
            score += instance.clients[client["id"]-1] * instance.routingCosts.primary * instance.siteClientDistances[
                str(client["parent"]), productionCenter]

    ### CAPACITY COSTS ###
    for productionCenter in productionCenters:
        if productionCenter == 1:
            capacity = instance.capacities.productionCenter + instance.capacities.automationBonus
        else:
            capacity = instance.capacities.productionCenter
        score += max(0, instance.capacityCost * (productionCentersUsage[productionCenter] - capacity))

    return score


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    size = 'large'
    tiny = parse(INSTANCE_FILES[size])
    tiny_instance = Instance(tiny)

    prod, client = solution(tiny_instance)
    sol = Solution(prod, client)

    compute_score(size, sol.to_dict())

    with open("./solutions/large.json", 'w') as file:
        json.dump(sol.to_dict(), file)