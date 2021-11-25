from Instance import Instance
import numpy as np

from main import INSTANCE_FILES, parse


def solution(instance: Instance):
    production_center_capacities = {}
    for index in range(instance.site_count):
        production_center_capacities[index] = instance.capacities.productionCenter

    selected_production_center_id = set()

    nb_clients = len(instance.clients)
    client_production_center_map = {}

    demands = np.copy(instance.clients)

    for i in range(nb_clients):
        client_with_most_demand = np.argmax(demands)
        distance_between_client_and_production_center = instance.siteClientDistances[:, client_with_most_demand]
        sorted_distance_indexes = np.argsort(distance_between_client_and_production_center)

        k = 0
        prod_center = sorted_distance_indexes[k]
        while production_center_capacities[prod_center] - demands[client_with_most_demand] < 0:
            k += 1
            prod_center = sorted_distance_indexes[k]
        production_center_capacities[k] -= demands[client_with_most_demand]
        demands[client_with_most_demand] = 0
        selected_production_center_id.add(prod_center)
        client_production_center_map[client_with_most_demand] = prod_center

    return selected_production_center_id, client_production_center_map

if __name__ == '__main__':
    tiny = parse(INSTANCE_FILES['large'])
    tiny_instance = Instance(tiny)

    print(solution(tiny_instance))
