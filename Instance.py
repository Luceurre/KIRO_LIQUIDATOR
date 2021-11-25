import numpy as np

class BuildingCosts:
    def __init__(self, buildingCosts):
        self.productionCenter = buildingCosts['productionCenter']
        self.automationPenalty = buildingCosts['automationPenalty']
        self.distributionCenter = buildingCosts['distributionCenter']


class ProductionCosts:
    def __init__(self, productionCosts):
        self.productionCenter = productionCosts['productionCenter']
        self.automationBonus = productionCosts['automationBonus']
        self.distributionCenter = productionCosts['distributionCenter']


class RoutingCosts:
    def __init__(self, routingCosts):
        self.primary = routingCosts['primary']
        self.secondary = routingCosts['secondary']

class Capacities:
    def __init__(self, capacities):
        self.productionCenter = capacities['productionCenter']
        self.automationBonus = capacities['automationBonus']

class Client:
    def __init__(self, client):
        self.id = client['id']
        self.demand = client['demand']


class Instance:
    def __init__(self, instance_content):
        parameters = instance_content['parameters']

        self.buildingCosts = BuildingCosts(parameters['buildingCosts'])
        self.productionCosts = ProductionCosts(parameters['productionCosts'])
        self.routingCosts = RoutingCosts(parameters['routingCosts'])
        self.capacityCost = parameters['capacityCost']
        self.capacities = Capacities(parameters['capacities'])

        self.clients = np.zeros(len(instance_content['clients']))
        for index, client in enumerate(instance_content['clients']):
            self.clients[index] = client['demand']

        self.site_count = len(instance_content['sites'])
        self.siteSiteDistances = np.array(instance_content['siteSiteDistances'])
        self.siteClientDistances = np.array(instance_content['siteClientDistances'])
