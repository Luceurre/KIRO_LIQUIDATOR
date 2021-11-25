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
    distributionCenters = {}

    ### BUILDING COSTS ###
    for productionCenter in solution["productionCenters"]:
        productionCenters[str(productionCenter["id"])] = productionCenter["automation"]
        score += instance.BuildingCosts.productionCenter
        if productionCenter["automation"] == 1:
            score += instance.BuildingCosts.automationPenalty
    for distributionCenter in solution["distributionCenters"]:
        distributionCenters[str(distributionCenter["id"])] = distributionCenter["parent"]
        score += instance.BuildingCosts.distributionCenter

    ### PRODUCTION COSTS ###
    for client in solution["clients"]:
        if str(client["parent"]) in productionCenters.keys():
            score += instance.productionCosts.productionCenter
            if productionCenters[str(client["parent"])] == 1:
                score -= instance.ProductionCosts.automationBonus
        if str(client["parent"]) in distributionCenters.keys():
            score += instance.productionCosts.distributionCenter
            productionCenter = productionCenters[str(distributionCenters[str(client["parent"])])]
            score += instance.productionCosts.productionCenter
            if productionCenter == 1:
                score -= instance.ProductionCosts.automationBonus

    ### ROUTING COSTS ###
    for client in solution["clients"]:
        if str(client["parent"]) in productionCenters.keys():
            score += instance.RoutingCosts.secondary * instance.siteClientDistances[str(client["parent"]), client["id"]]
        if str(client["parent"]) in distributionCenters.keys():
            score += instance.RoutingCosts.secondary * instance.siteClientDistances[str(client["parent"]), client["id"]]
            productionCenter = productionCenters[str(distributionCenters[str(client["parent"])])]
            score += instance.RoutingCosts.primary * instance.siteClientDistances[str(client["parent"]), productionCenter]

    ### CAPACITY COSTS ###




if __name__ == '__main__':
    print("test")