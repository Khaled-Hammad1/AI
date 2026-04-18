import math
import random
import copy
from os import remove

import matplotlib.pyplot as plt
population_size = 50
mutation_rate = 0.05
packeges={}
vehicle={}
BestState={}
Best =1000000000
# read first file and store in dictionay of packeges
with open("packeges.txt", "r") as file:
    for line in file:
        parts = line.strip().split(" ")
        key = parts[0]
        values = parts[1:]
        packeges[key] = values

print(packeges)
#read second file and store in dictionry of vehicle
with open("vehicles.txt", "r") as file:
    for line in file:
        name,size = line.strip().split(" ")
        vehicle[name] = {"size":size}

print(vehicle)

#############################################################################################################3
def plot_solution(state, packages):
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'cyan']
    plt.figure(figsize=(6, 6))

    for idx, (vehicle, pkg_list) in enumerate(state.items()):
        if not pkg_list:
            continue

        x_points = [0]
        y_points = [0]

        for pkg in pkg_list:
            x, y = map(int, packages[pkg][1].strip("()").split(','))
            x_points.append(x)
            y_points.append(y)

        x_points.append(0)
        y_points.append(0)

        plt.plot(x_points, y_points, marker='o', color=colors[idx % len(colors)],
                 label=f'{vehicle}')

        for i, pkg in enumerate(pkg_list):
            x, y = map(int, packages[pkg][1].strip("()").split(','))
            plt.text(x + 1, y + 1, pkg, fontsize=9)

    plt.title("Vehicle Routes to Deliver Packages")
    plt.xlabel("X Coordinate (km)")
    plt.ylabel("Y Coordinate (km)")
    plt.legend()
    plt.grid(True)
    plt.scatter(0, 0, c='black', marker='s', label='Shop (0,0)')
    plt.legend()
    plt.show()

##############################################Simulated #########################################################

def menu():
    for p in packeges:
        if int(packeges[p][0]) < 1 or int(packeges[p][0]) > 5:  # this for if file contains invaild proirty
            print("this priorty " + packeges[p][0] + " is invalid")
            return
        location = packeges[p][1]  # e.g., "(20,70)"
        x, y = map(int, location.strip('()').split(','))
        if x < 0 or x > 100 or y < 0 or y > 100:  # this for if file contains invaild location
            print("this (" + str(x) + ',' + str(y) + ")cooerdinate is invalid")
            return
        if int(packeges[p][2]) < 0:  # this for invaild weight
            print("this weight is invaild")
            return

    for v in vehicle:
        if vehicle[v]['size'] <= '0':  # this for invaild size
            print("this size is not valid for this vehicle")
            return
    cooling_rate = 0.97  # You can set between 0.90 and 0.99
    while True:
        print("Menu:")
        print("1. Simulated Aneeling")
        print("2. genteic algorithm")
        print("3. Exit")

        opration = input("Enter your opration: ")

        if opration == "1":
            print(simulated_annealing(cooling_rate))
        elif opration == "2":
            genetic_algorithm(packeges, vehicle)
        elif opration == "3":
            print("Goodbye!")
            break  # <--- this stops the while loop
        else:
            print("Invalid choice, try again")

#this function aims to select an initial random state
def random_initial_assignment(packages, vehicles):
    # Prepare assignment and track used capacity
    assignment = {vehicle: [] for vehicle in vehicles.keys()}
    used_capacity = {vehicle: 0 for vehicle in vehicles.keys()}

    package_list = list(packages.keys())
    random.shuffle(package_list)  # Shuffle to make it more random

    for package in package_list:
        weight = int(packages[package][2])  # get weight of the package
        possible_vehicles = []

        # Find vehicles that have enough free space
        for vehicle, info in vehicles.items():
            max_capacity = int(info['size'])
            if used_capacity[vehicle] + weight <= max_capacity:
                possible_vehicles.append(vehicle)

        if not possible_vehicles:
            raise Exception(f"No vehicle can carry package {package} with weight {weight}!")

        # Randomly pick one vehicle from possible vehicles
        chosen_vehicle = random.choice(possible_vehicles)
        assignment[chosen_vehicle].append(package)
        used_capacity[chosen_vehicle] += weight  # Update used capacity
    return assignment

#this to find random next space from first step to make delta function
def random_successor(current_state, packages, vehicles):
    # Deep copy the current state so we don't modify the original
    new_state = copy.deepcopy(current_state)

    # Track used capacity
    used_capacity = {vehicle: 0 for vehicle in vehicles}
    for vehicle, pkg_list in new_state.items():
        for pkg in pkg_list:
            used_capacity[vehicle] += int(packages[pkg][2])

    # Randomly pick a package
    vehicle_from = random.choice(list(new_state.keys()))
    if not new_state[vehicle_from]:
        return new_state  # No package to move

    package = random.choice(new_state[vehicle_from])

    # Find possible vehicles to move to (excluding the same vehicle)
    possible_vehicles = []
    weight = int(packages[package][2])

    for vehicle_to in new_state.keys():
        if vehicle_to != vehicle_from:
            max_capacity = int(vehicles[vehicle_to]['size'])
            if used_capacity[vehicle_to] + weight <= max_capacity:
                possible_vehicles.append(vehicle_to)

    if not possible_vehicles:
        return new_state  # No move possible, return same

    # Move the package
    vehicle_to = random.choice(possible_vehicles)
    new_state[vehicle_from].remove(package)
    new_state[vehicle_to].append(package)

    return new_state

def simulated_annealing(cooling_rate):
    initial_state = random_initial_assignment(packeges, vehicle)
   # current = problem.initial_state()
    T = 1000  # Initial temperature
    stopping_temperature = 1
    iterations_per_temperature = 100
    while T > stopping_temperature:
        for _ in range(iterations_per_temperature):
            next_state = random_successor(initial_state,packeges,vehicle)
            delta_E = objective_function(next_state,packeges) - objective_function(initial_state,packeges)

            if delta_E > 0:
                current = next_state
            else:
                probability = math.exp(delta_E / T)
                if random.random() < probability:
                    current = next_state

        T *= cooling_rate  # Decrease temperature after fixed iterations
    print(objective_function(current,packeges))
    plot_solution(current, packeges)
    return current

def objective_function(state, packages):
        total_distance = 0

        for vehicle, package_list in state.items():
            if not package_list:
                continue  # skip empty vehicles
            last_x, last_y = 0, 0

            def score(pkg):
                prio = int(packages[pkg][0])
                loc = packages[pkg][1]
                x, y = map(int, loc.strip('()').split(','))
                dist = distance(last_x, last_y, x, y)
                if dist == 0:
                    dist = 0.1  # prevent divide by zero
                return prio / dist  # lower score means delay

            # Sort packages by score: lower score = worse = delay
            sorted_packages = sorted(package_list, key=score, reverse=True)

            # Start from a fixed starting point (e.g., (0,0)) if needed

            for package in sorted_packages:
                location = packages[package][1]  # e.g., "(20,70)"
                x, y = map(int, location.strip('()').split(','))
                total_distance += distance(last_x, last_y, x, y)

                # Update last position
                last_x, last_y = x, y

            # Optionally: return to (0,0) if it's a delivery trip
            total_distance += distance(last_x, last_y, 0, 0)
        return total_distance

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


##############################################Genatic #########################################################
def total_distance(state, packages):
        total_distance = 0

        for vehicle, package_list in state.items():
            if not package_list:
                continue  # skip empty vehicles
            last_x, last_y = 0, 0

            for package in package_list:
                location = packages[package][1]  # e.g., "(20,70)"
                x, y = map(int, location.strip('()').split(','))
                total_distance += distance(last_x, last_y, x, y)

                # Update last position
                last_x, last_y = x, y

            # Optionally: return to (0,0) if it's a delivery trip
            total_distance += distance(last_x, last_y, 0, 0)
        return total_distance
def create_population(packeges, vehicle):    #We assume that populaiton Size is 50
    state= []
    for i in range(population_size):
        state.append(random_initial_assignment(packeges, vehicle))
    check_the_best(state, packeges)
    return state

def check_the_best(state,packeges):
    global Best
    global BestState
    min_distance =total_distance(state[0], packeges)
    min_state = BestState
    for i in range(1,population_size):
        state_distance= total_distance(state[i], packeges)
        if state_distance < min_distance:
            min_distance = state_distance
            min_state = state[i]
    if min_distance < Best :
        Best = min_distance
        BestState = min_state

def mutation(child):
    ran = random.random()
    if ran < mutation_rate:
        r = random.randint(1,len(child)-1)
        temp = child[0]
        child[0] = child[r]
        child[r] = temp
    return child

def fitnessFunction(state,packages):#to select the parent based on min distance which the min distance have the greater propbility
    fitness_list=[]
    distance_list =[]
    total_ditsance=0
    for  i in range(len(state)):
        distance_list.append(total_distance(state[i], packages))
    for i in range(len(distance_list)):
        total_ditsance +=(1/distance_list[i])
    for i in range(len(distance_list)):
        probability = (1/distance_list[i]) / (total_ditsance)
        fitness_list.append(probability)
    return fitness_list

def put_packege_after_crossover(child, packages, vehicles):
    state={}
    used_capacity ={}
    max_capacity={}
    v_list = list(vehicles)
    for v in vehicles:
        state[v] = []
    for v in vehicles:
        used_capacity[v] = 0
    for i in range(len(v_list)):
        max_capacity[v_list[i]] = int(vehicles[v_list[i]]['size'])

    child_sorted = sorted(child, key=lambda pkg: int(packages[pkg][0])) #to sort the packege based on proirty

    for pkg in child_sorted:
        weight = int(packages[pkg][2])
        best_vehicle = None
        min_used = 1000000000000000000

        for v in vehicles:
            if used_capacity[v] + weight <= max_capacity[v]:
                if used_capacity[v] < min_used:
                    best_vehicle = v
                    min_used = used_capacity[v]
        if best_vehicle is not None:
            state[best_vehicle].append(pkg)
            used_capacity[best_vehicle] += weight
        else:
            print("package couldn't be placed due to capacity.")
    return state


def genetic_algorithm(packeges, vehicle):
    global BestState, Best
    fitenssList= []
    state = create_population(packeges, vehicle)
    newGenerations = state
    for l in range(500):        #500 is Number of Generations
        state = newGenerations
        fitenssList = fitnessFunction(state, packeges)
        newGenerations=[]
        for k in range(0, len(state), 2):
            state1 = random.choices(state,weights=fitenssList,k=1)[0] #the parent that have greater propabilty will selcet randomly
            state2 = random.choices(state,weights=fitenssList,k=1)[0]
            s1 = list(state1.items())
            pa1 = []
            parent1 = []
            for i in range(len(s1)):#after we select state we put the package as list to make crossover
                pa1.append(s1[i][1])
            for i in range(len(pa1)):
                for j in range(len(pa1[i])):
                    parent1.append(pa1[i][j])
            s2 = list(state2.items())
            pa2 = []
            parent2 = []
            for i in range(len(s2)):#after we select state we put the package as list to make crossover
                pa2.append(s2[i][1])
            for i in range(len(pa1)):
                for j in range(len(pa2[i])):
                    parent2.append(pa2[i][j])

            cross = random.randint(1, len(parent1) - 1)  #choose the place of cut randomly
            child1 = []
            child2 = []
            #cross over between parent 1 and parent 2 to bulid child 1 and child 2
            for i in range(cross):
                if i < cross:
                    if parent1[i] not in child1:
                        child1.append(parent1[i])
            for i in range(cross, len(parent2)):
                if i >= cross:
                    if parent2[i] not in child1:
                        child1.append(parent2[i])

            for i in range(cross):
                if i < cross:
                    if parent2[i] not in child2:
                        child2.append(parent2[i])
            for i in range(cross, len(parent2)):
                if i >= cross:
                    if parent1[i] not in child2:
                        child2.append(parent1[i])

            pList = list(packeges)      #to add the lost packege
            for i in range(len(pList)):
                if pList[i] not in child1:
                    child1.append(pList[i])
                if pList[i] not in child2:
                    child2.append(pList[i])
            # after we make cross over we make mutaion based in mutaion rate
            child1 = mutation(child1)
            child2 = mutation(child2)
            newGenerations.append(put_packege_after_crossover(child1, packeges, vehicle))
            newGenerations.append(put_packege_after_crossover(child2, packeges, vehicle))
        check_the_best(newGenerations, packeges)
    print("The total distance " + str(Best))
    print(BestState)
    plot_solution(BestState, packeges)
    BestState = {}
    Best = 1000000000



menu()