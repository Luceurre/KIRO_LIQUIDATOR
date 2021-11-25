from typing import Set, Dict

import numpy as np

from Instance import Instance
from main import parse, INSTANCE_FILES
from oceane import solution


def get_transport_cost_of_site(solution, instance, site_index):
    _, client_map, _ = solution
    cost = 0

    for client_index in client_map.keys():
        if client_map[client_index] == site_index:
            cost += instance.clients[client_index] * instance.routingCosts.secondary * instance.siteClientDistances[site_index, client_index]
    return cost

def swap_production_with_distribution(solution, site_index, instance):
    prod: Set = solution[0]
    distrib: Dict = solution[2]
    prod.remove(site_index)

    sites = set(range(0, instance.site_count))
    used_sites = prod.union(distrib.keys())
    used_sites.add(site_index)
    free_sites = list(sites.difference(used_sites))

    new_production_center = [site for site in np.argsort(instance.siteSiteDistances[site_index, :]) if site in free_sites][0]
    # new_production_center = np.argmin(instance.siteSiteDistances[site_index, free_sites])
    prod.add(new_production_center)
    distrib[site_index] = new_production_center
    print(prod, solution, distrib)
    return prod, solution[1], distrib

def update_solution(solution, instance):
    production_sites, client_map, distrib = solution
    transport_cost = {}
    for production_site in production_sites:
        transport_cost[production_site] = get_transport_cost_of_site(solution, instance, production_site)
    iter_count = instance.site_count - len(production_sites)
    for k in range(0, min(iter_count, len(transport_cost))):
        site_index = max(transport_cost, key=transport_cost.get)
        production_sites, client_map, distrib = swap_production_with_distribution((production_sites, client_map, distrib), site_index, instance)
        del transport_cost[site_index]

    return production_sites, client_map, distrib

if __name__ == '__main__':
    tiny = parse(INSTANCE_FILES['tiny'])
    instance = Instance(tiny)
    dist, client_map = solution(instance)
    #
    # print(update_solution((dist, client_map, {}), instance))
    swap_production_with_distribution((dist, client_map, {}), 0, instance)
