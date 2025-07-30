def fuzzy_relation():
    print('''
import numpy as np

R = {
          
    "Low Temp": [0.8, 0.5, 0.3],
          
    "Medium Temp": [0.6, 0.7, 0.4],
          
    "High Temp": [0.3, 0.6, 0.9]
          
}

S = {
          
    "Dry": [0.7, 0.4, 0.3],
          
    "Normal": [0.5, 0.6, 0.4],
          
    "Humid": [0.2, 0.5, 0.8]
          
}

temperature_input = "Low Temp"
          
humidity_input = "Dry"

mu_R = R[temperature_input]
          
mu_S = S[humidity_input]

def min_max_composition(mu_R, mu_S):
          
    result = []

    for z in range(3):
          
        min_value = min(mu_R[0], mu_S[0]) if z == 0 else \\
          
                    min(mu_R[1], mu_S[1]) if z == 1 else \\
          
                    min(mu_R[2], mu_S[2])
          
        result.append(min_value)

    return result

composed_result = min_max_composition(mu_R, mu_S)

cooling_action = ["Low Cooling", "Medium Cooling", "High Cooling"]
          
max_membership_value = max(composed_result)
          
action_index = composed_result.index(max_membership_value)

print(f"Input: Temperature = {temperature_input}, Humidity = {humidity_input}")
          
print(f"Membership values for Cooling Actions: {composed_result}")
          
print(f"The system selects: {cooling_action[action_index]} with a membership value of {max_membership_value:.2f}")
          

OR

import numpy as np

def max_min_composition(R1, R2):
    m, n1 = R1.shape
    n2, p = R2.shape
    if n1 != n2:
        raise ValueError("Incompatible shapes for Max-Min composition.")
    result = np.zeros((m, p))
    for i in range(m):
        for j in range(p):
            result[i, j] = np.max(np.minimum(R1[i, :], R2[:, j]))
    
    return result
R1 = np.array([
    [0.2, 0.8],
    [0.6, 0.4]
])
R2 = np.array([
    [0.5, 0.7],
    [0.9, 0.3]
])
composition = max_min_composition(R1, R2)
print("Max-Min Composition:", composition)
          
import numpy as np
def max_min(R,S):
  m,n1=R.shape
  n2,p=S.shape
  if n1!=n2:
    print("incompatible max min compositon")
  else:
    res=np.zeros((m,p))
    for i in range(m):
      for j in range(p):
        res[i,j]=max(np.minimum(R[i,:],S[:,j]))
  return res
R=np.array([[0.6,0.3],[0.2,0.9]])
S=np.array([[1,0.5,0.3],[0.8,0.4,0.7]])

display("max min relation",max_min(R,S))
          
''')
    
def fuzzy_relation_run():
    import numpy as np

    R = {
        "Low Temp": [0.8, 0.5, 0.3],
        "Medium Temp": [0.6, 0.7, 0.4],
        "High Temp": [0.3, 0.6, 0.9]
    }

    S = {
        "Dry": [0.7, 0.4, 0.3],
        "Normal": [0.5, 0.6, 0.4],
        "Humid": [0.2, 0.5, 0.8]
    }

    temperature_input = "Low Temp"
    humidity_input = "Dry"

    mu_R = R[temperature_input]
    mu_S = S[humidity_input]

    def min_max_composition(mu_R, mu_S):
        result = []

        for z in range(3):
            min_value = min(mu_R[0], mu_S[0]) if z == 0 else \
                        min(mu_R[1], mu_S[1]) if z == 1 else \
                        min(mu_R[2], mu_S[2])
            result.append(min_value)

        return result

    composed_result = min_max_composition(mu_R, mu_S)

    cooling_action = ["Low Cooling", "Medium Cooling", "High Cooling"]
    max_membership_value = max(composed_result)
    action_index = composed_result.index(max_membership_value)

    print(f"Input: Temperature = {temperature_input}, Humidity = {humidity_input}")
    print(f"Membership values for Cooling Actions: {composed_result}")
    print(f"The system selects: {cooling_action[action_index]} with a membership value of {max_membership_value:.2f}")
    

def defuzzification():
    print('''
          
LAMBDA CUT METHOD
          
fuzzy_set = {'x': 4.5, 'y': 3.5, 'z':4.33}

lambda_value = 4

def lambda_cut(fuzzy_set, lambda_value):
          
    cut_set = []

    for element, membership_value in fuzzy_set.items():
          
        if membership_value >= lambda_value:
          
            cut_set.append(element)

    return cut_set

result = lambda_cut(fuzzy_set, lambda_value)

print(f"Elements in the fuzzy set with membership >= {lambda_value}: {result}")
          

          
MEAN OF MAXIMUM METHOD
          
def mean_of_maximum(fuzzy_set):
          
    max_membership = max(fuzzy_set.values())

    max_x_values = [x for x, mu in fuzzy_set.items() if mu == max_membership]

    return sum(max_x_values) / len(max_x_values)

fuzzy_set = {1: 0.2, 2: 0.5, 3: 0.8, 4: 1.0, 5: 1.0, 6: 0.7, 7: 0.3}

result = mean_of_maximum(fuzzy_set)

print(f"Mean of Maximum (MOM) defuzzified value: {result}")
          


CENTER OF GRAVITY METHOD
          
def center_of_gravity(fuzzy_set):
    numerator = sum(x * mu for x, mu in fuzzy_set.items())

    denominator = sum(fuzzy_set.values())

    return numerator / denominator if denominator != 0 else 0

fuzzy_set = {1: 0.2, 2: 0.5, 3: 0.8, 4: 1.0, 5: 0.7}

result = center_of_gravity(fuzzy_set)

print(f"Center of Gravity (COG) defuzzified value: {result}")
          
          ''')
    
def defuzzification_run_lambda():
    fuzzy_set = {'x': 4.5, 'y': 3.5, 'z':4.33}

    lambda_value = 4

    def lambda_cut(fuzzy_set, lambda_value):
            
        cut_set = []

        for element, membership_value in fuzzy_set.items():
            
            if membership_value >= lambda_value:
            
                cut_set.append(element)

        return cut_set

    result = lambda_cut(fuzzy_set, lambda_value)

    print(f"Elements in the fuzzy set with membership >= {lambda_value}: {result}")

def defuzzification_run_MOM():
    def mean_of_maximum(fuzzy_set):
            
        max_membership = max(fuzzy_set.values())

        max_x_values = [x for x, mu in fuzzy_set.items() if mu == max_membership]

        return sum(max_x_values) / len(max_x_values)

    fuzzy_set = {1: 0.2, 2: 0.5, 3: 0.8, 4: 1.0, 5: 1.0, 6: 0.7, 7: 0.3}

    result = mean_of_maximum(fuzzy_set)

    print(f"Mean of Maximum (MOM) defuzzified value: {result}")

def defuzzification_run_COG():
    def center_of_gravity(fuzzy_set):
        numerator = sum(x * mu for x, mu in fuzzy_set.items())

        denominator = sum(fuzzy_set.values())

        return numerator / denominator if denominator != 0 else 0

    fuzzy_set = {1: 0.2, 2: 0.5, 3: 0.8, 4: 1.0, 5: 0.7}

    result = center_of_gravity(fuzzy_set)

    print(f"Center of Gravity (COG) defuzzified value: {result}")


def genetic_algorithm():
    print('''
import random

# Fitness function
def fitness(x): 
    return x**2

# Decode binary string to integer
def decode(chrom): 
    return int(chrom, 2)

# Create random chromosome
def random_chrom(): 
    return ''.join(random.choice('01') for _ in range(5))

# Selection (tournament)
def select(pop): 
    return max(random.sample(pop, 2), key=lambda c: fitness(decode(c)))

# Crossover (single point)
def crossover(p1, p2):
    point = random.randint(1, 4)
    return p1[:point] + p2[point:], p2[:point] + p1[point:]

# Mutation (flip bit)
def mutate(chrom, rate=0.1):
    return ''.join(b if random.random() > rate else str(1-int(b)) for b in chrom)

# Genetic Algorithm
pop = [random_chrom() for _ in range(10)]
for gen in range(20):  # 20 generations
    pop = [mutate(c) for _ in range(5) for c in crossover(select(pop), select(pop))]
    best = max(pop, key=lambda c: fitness(decode(c)))
    print(f"Gen {gen+1:2d}: Best = {decode(best)} (Fitness = {fitness(decode(best))})")

# Final best result
best = max(pop, key=lambda c: fitness(decode(c)))
print("Final Best solution:", decode(best), "Fitness:", fitness(decode(best)))


''')
    
def genetic_algorithm_run():
    import random

    # Fitness function
    def fitness(x): 
        return x**2

    # Decode binary string to integer
    def decode(chrom): 
        return int(chrom, 2)

    # Create random chromosome
    def random_chrom(): 
        return ''.join(random.choice('01') for _ in range(5))

    # Selection (tournament)
    def select(pop): 
        return max(random.sample(pop, 2), key=lambda c: fitness(decode(c)))

    # Crossover (single point)
    def crossover(p1, p2):
        point = random.randint(1, 4)
        return p1[:point] + p2[point:], p2[:point] + p1[point:]

    # Mutation (flip bit)
    def mutate(chrom, rate=0.1):
        return ''.join(b if random.random() > rate else str(1-int(b)) for b in chrom)

    # Genetic Algorithm
    pop = [random_chrom() for _ in range(10)]
    for gen in range(20):  # 20 generations
        pop = [mutate(c) for _ in range(5) for c in crossover(select(pop), select(pop))]
        best = max(pop, key=lambda c: fitness(decode(c)))
        print(f"Gen {gen+1:2d}: Best = {decode(best)} (Fitness = {fitness(decode(best))})")

    # Final best result
    best = max(pop, key=lambda c: fitness(decode(c)))
    print("Final Best solution:", decode(best), "Fitness:", fitness(decode(best)))

def distributive_parallel():
    print('''
MERGE SORT
def merge_sort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(a, b):
    res = []
    while a and b:
        res.append(a.pop(0) if a[0] < b[0] else b.pop(0))
    return res + a + b

# Example
arr = [5, 2, 9, 1, 3]
print("Sorted:", merge_sort(arr))

          

PARALLEL SYSTEM
          
import concurrent.futures                        # Import the concurrent.futures module for parallel execution using processes
def merge(left, right):                          # Define the merge function to combine two sorted lists
    result = []                                  # Initialize an empty list to hold the merged result
    i = j = 0                                     # Set up two pointers for traversing left and right lists
    while i < len(left) and j < len(right):      # Loop until either list is fully traversed
        if left[i] < right[j]:                   # Compare elements from both lists
            result.append(left[i])               # Append the smaller element to the result list
            i += 1                               # Move the pointer in the left list
        else:
            result.append(right[j])              # Append the smaller element from right list
            j += 1                               # Move the pointer in the right list
    result.extend(left[i:])                      # Add any remaining elements from the left list
    result.extend(right[j:])                     # Add any remaining elements from the right list
    return result                                # Return the merged, sorted list
def parallel_merge_sort(arr):                    # Define the parallel merge sort function
    if len(arr) <= 1:                            # Base case: a list of 1 or 0 is already sorted
        return arr                               # Return the list as is
    mid = len(arr) // 2                          # Calculate the middle index to divide the list
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:  # Create a pool of 8 parallel processes
        left_future = executor.submit(parallel_merge_sort, arr[:mid])        # Submit left half of the list for sorting in a subprocess
        right_future = executor.submit(parallel_merge_sort, arr[mid:])       # Submit right half of the list for sorting in a subprocess
        left = left_future.result()               # Get the sorted result from the left subprocess
        right = right_future.result()             # Get the sorted result from the right subprocess

    return merge(left, right)                    # Merge the two sorted halves and return the result

arr = [38, 27, 43, 3, 9, 82, 10]                 # Define an unsorted list
sorted_arr = parallel_merge_sort(arr)           # Call the parallel merge sort function to sort the list
print(sorted_arr)
''')
    

def distributive_parallel_run():
    def merge_sort(arr):
        if len(arr) <= 1: return arr
        mid = len(arr) // 2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])
        return merge(left, right)

    def merge(a, b):
        res = []
        while a and b:
            res.append(a.pop(0) if a[0] < b[0] else b.pop(0))
        return res + a + b

    # Example
    arr = [5, 2, 9, 1, 3]
    print("Sorted:", merge_sort(arr))

def ant_colony_optimization():
    print('''
import numpy as np

# Distance matrix between 4 cities
dist = np.array([[0, 2, 2, 5],
                 [2, 0, 3, 4],
                 [2, 3, 0, 1],
                 [5, 4, 1, 0]])

n_ants = 4
n_iterations = 10
alpha = 1      # pheromone importance
beta = 2       # distance importance
evaporation = 0.5
Q = 100        # pheromone deposit factor

n_cities = len(dist)
pheromone = np.ones((n_cities, n_cities))  # initial pheromones

def probability(from_city, visited):
    probs = []
    for to_city in range(n_cities):
        if to_city in visited: probs.append(0)
        else:
            tau = pheromone[from_city][to_city] ** alpha
            eta = (1 / dist[from_city][to_city]) ** beta
            probs.append(tau * eta)
    probs = np.array(probs)
    return probs / probs.sum()

def build_tour():
    tour = [np.random.randint(n_cities)]
    while len(tour) < n_cities:
        probs = probability(tour[-1], tour)
        next_city = np.random.choice(range(n_cities), p=probs)
        tour.append(next_city)
    return tour + [tour[0]]  # return to start

def tour_length(tour):
    return sum(dist[tour[i]][tour[i+1]] for i in range(n_cities))

for it in range(n_iterations):
    all_tours = [build_tour() for _ in range(n_ants)]
    pheromone *= (1 - evaporation)
    for tour in all_tours:
        length = tour_length(tour)
        for i in range(n_cities):
            a, b = tour[i], tour[i+1]
            pheromone[a][b] += Q / length
            pheromone[b][a] += Q / length  # symmetric

    best = min(all_tours, key=tour_length)
    print(f"Iter {it+1}: Best tour = {best}, Length = {tour_length(best)}")

          


OR
          

import numpy as np

d = np.array([  [0,2,2,5],
                [2,0,3,4],
                [2,3,0,1],
                [5,4,1,0]])  # Distance matrix
n = len(d); p = np.ones((n,n))  # Pheromones

def tour():
    t = [np.random.randint(n)]
    while len(t) < n:
        r = t[-1]; u = [i for i in range(n) if i not in t]
        prob = [(p[r][j] / d[r][j])**2 for j in u]
        prob = prob / np.sum(prob)
        t.append(np.random.choice(u, p=prob))
    return t + [t[0]]

def length(t): return sum(d[t[i]][t[i+1]] for i in range(n))

for _ in range(10):
    T = [tour() for _ in range(n)]
    p *= 0.5
    for t in T:
        l = length(t)
        for i in range(n): p[t[i]][t[i+1]] += 100 / l
    b = min(T, key=length)
    print("Best tour:", b, "Length:", length(b))

          
''')



def ant_colony_optimization_run():
    import numpy as np

    # Distance matrix between 4 cities
    dist = np.array([[0, 2, 2, 5],
                    [2, 0, 3, 4],
                    [2, 3, 0, 1],
                    [5, 4, 1, 0]])

    n_ants = 4
    n_iterations = 10
    alpha = 1      # pheromone importance
    beta = 2       # distance importance
    evaporation = 0.5
    Q = 100        # pheromone deposit factor

    n_cities = len(dist)
    pheromone = np.ones((n_cities, n_cities))  # initial pheromones

    def probability(from_city, visited):
        probs = []
        for to_city in range(n_cities):
            if to_city in visited: probs.append(0)
            else:
                tau = pheromone[from_city][to_city] ** alpha
                eta = (1 / dist[from_city][to_city]) ** beta
                probs.append(tau * eta)
        probs = np.array(probs)
        return probs / probs.sum()

    def build_tour():
        tour = [np.random.randint(n_cities)]
        while len(tour) < n_cities:
            probs = probability(tour[-1], tour)
            next_city = np.random.choice(range(n_cities), p=probs)
            tour.append(next_city)
        return tour + [tour[0]]  # return to start

    def tour_length(tour):
        return sum(dist[tour[i]][tour[i+1]] for i in range(n_cities))

    for it in range(n_iterations):
        all_tours = [build_tour() for _ in range(n_ants)]
        pheromone *= (1 - evaporation)
        for tour in all_tours:
            length = tour_length(tour)
            for i in range(n_cities):
                a, b = tour[i], tour[i+1]
                pheromone[a][b] += Q / length
                pheromone[b][a] += Q / length  # symmetric

        best = min(all_tours, key=tour_length)
        print(f"Iter {it+1}: Best tour = {best}, Length = {tour_length(best)}")



def particle_swarm_optimization():
    print('''
          

import numpy as np

def f(x): return x**2  # Objective function

n_particles = 10
n_iterations = 20
x = np.random.uniform(-10, 10, n_particles)  # positions
v = np.zeros(n_particles)                   # velocities
pbest = x.copy()
pbest_val = f(x)
gbest = x[np.argmin(pbest_val)]

for i in range(n_iterations):
    r1, r2 = np.random.rand(), np.random.rand()
    v = 0.5*v + r1*(pbest - x) + r2*(gbest - x)
    x += v
    fx = f(x)
    mask = fx < pbest_val
    pbest[mask] = x[mask]
    pbest_val[mask] = fx[mask]
    gbest = x[np.argmin(pbest_val)]
    
    print(f"Iter {i+1}: gbest = {gbest:.4f}, f(gbest) = {f(gbest):.4f}")
    print("        pbest =", np.round(pbest, 4))

          
''')



def particle_swarm_optimization_run():
    import numpy as np

    def f(x): return x**2  # Objective function

    n_particles = 10
    n_iterations = 20
    x = np.random.uniform(-10, 10, n_particles)  # positions
    v = np.zeros(n_particles)                   # velocities
    pbest = x.copy()
    pbest_val = f(x)
    gbest = x[np.argmin(pbest_val)]

    for i in range(n_iterations):
        r1, r2 = np.random.rand(), np.random.rand()
        v = 0.5*v + r1*(pbest - x) + r2*(gbest - x)
        x += v
        fx = f(x)
        mask = fx < pbest_val
        pbest[mask] = x[mask]
        pbest_val[mask] = fx[mask]
        gbest = x[np.argmin(pbest_val)]
        
        print(f"Iter {i+1}: gbest = {gbest:.4f}, f(gbest) = {f(gbest):.4f}")
        print("        pbest =", np.round(pbest, 4))


def grey_wolf_optimization():
    print('''

import numpy as np

def f(x): return x**2  # Objective function

wolves = np.random.uniform(-10, 10, 5)  # 5 grey wolves (1D)
alpha, beta, delta = None, None, None

for iter in range(20):
    sorted_idx = np.argsort(f(wolves))
    alpha, beta, delta = wolves[sorted_idx[:3]]

    a = 2 - iter * (2 / 20)  # linearly decrease from 2 to 0
    for i in range(len(wolves)):
        for leader in [alpha, beta, delta]:
            r1, r2 = np.random.rand(), np.random.rand()
            A = a * (2*r1 - 1)
            C = 2 * r2
            D = abs(C * leader - wolves[i])
            X = leader - A * D
            wolves[i] = (wolves[i] + X) / 2  # average with current position

    best = alpha
    print(f"Iter {iter+1}: Best = {best:.4f}, f(Best) = {f(best):.4f}")


''')




def grey_wolf_optimization_run():
    import numpy as np

    def f(x): return x**2  # Objective function

    wolves = np.random.uniform(-10, 10, 5)  # 5 grey wolves (1D)
    alpha, beta, delta = None, None, None

    for iter in range(20):
        sorted_idx = np.argsort(f(wolves))
        alpha, beta, delta = wolves[sorted_idx[:3]]

        a = 2 - iter * (2 / 20)  # linearly decrease from 2 to 0
        for i in range(len(wolves)):
            for leader in [alpha, beta, delta]:
                r1, r2 = np.random.rand(), np.random.rand()
                A = a * (2*r1 - 1)
                C = 2 * r2
                D = abs(C * leader - wolves[i])
                X = leader - A * D
                wolves[i] = (wolves[i] + X) / 2  # average with current position

        best = alpha
        print(f"Iter {iter+1}: Best = {best:.4f}, f(Best) = {f(best):.4f}")


def crisp_partition():
    print('''

from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Load Iris dataset
data = load_iris()
X = data.data[:, :2]  # Use first two features for easy 2D plotting

# Apply K-Means with 3 clusters
kmeans = KMeans(n_clusters=3, random_state=0)
labels = kmeans.fit_predict(X)
centers = kmeans.cluster_centers_

# Plot the clustered data
plt.figure(figsize=(6, 4))
for i in range(3):
    plt.scatter(X[labels == i, 0], X[labels == i, 1], label=f"Cluster {i}")
plt.scatter(centers[:, 0], centers[:, 1], c='black', marker='x', label='Centroids')
plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')
plt.title('Crisp Partitioning of Iris Data (K-Means)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


''')



def crisp_partition_run():
    from sklearn.datasets import load_iris
    from sklearn.cluster import KMeans
    import matplotlib.pyplot as plt

    # Load Iris dataset
    data = load_iris()
    X = data.data[:, :2]  # Use first two features for easy 2D plotting

    # Apply K-Means with 3 clusters
    kmeans = KMeans(n_clusters=3, random_state=0)
    labels = kmeans.fit_predict(X)
    centers = kmeans.cluster_centers_

    # Plot the clustered data
    plt.figure(figsize=(6, 4))
    for i in range(3):
        plt.scatter(X[labels == i, 0], X[labels == i, 1], label=f"Cluster {i}")
    plt.scatter(centers[:, 0], centers[:, 1], c='black', marker='x', label='Centroids')
    plt.xlabel('Sepal Length')
    plt.ylabel('Sepal Width')
    plt.title('Crisp Partitioning of Iris Data (K-Means)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def perceptron():
    print('''

HEBBS RULE
import numpy as np

# AND gate dataset
X = np.array([[0,0], [0,1], [1,0], [1,1]])
y = np.array([-1, -1, -1, 1])  # AND logic (-1 for 0, 1 for 1)

# Add bias term
Xb = np.hstack((X, np.ones((4,1))))

# Hebb's learning rule: w += x * y
w = np.zeros(3)
for i in range(len(Xb)):
    w += Xb[i] * y[i]

# Test
print("Hebb's Rule Weights:", w)
for i in range(len(Xb)):
    out = np.sign(np.dot(Xb[i], w))
    print(f"Input: {X[i]}, Output: {out}")

          
DELTA RULE
import numpy as np

# AND gate dataset
X = np.array([[0,0], [0,1], [1,0], [1,1]])
y = np.array([0, 0, 0, 1])  # Output for AND

# Add bias term
Xb = np.hstack((X, np.ones((4,1))))

# Delta rule training
w = np.zeros(3)
lr = 0.1
for epoch in range(10):
    for i in range(len(Xb)):
        out = np.dot(Xb[i], w)
        error = y[i] - out
        w += lr * error * Xb[i]

# Test
print("Delta Rule Weights:", w)
for i in range(len(Xb)):
    out = np.dot(Xb[i], w)
    print(f"Input: {X[i]}, Output: {round(out)}")


''')
    
def perceptron_hebbs_run():
    import numpy as np

    # AND gate dataset
    X = np.array([[0,0], [0,1], [1,0], [1,1]])
    y = np.array([-1, -1, -1, 1])  # AND logic (-1 for 0, 1 for 1)

    # Add bias term
    Xb = np.hstack((X, np.ones((4,1))))

    # Hebb's learning rule: w += x * y
    w = np.zeros(3)
    for i in range(len(Xb)):
        w += Xb[i] * y[i]

    # Test
    print("Hebb's Rule Weights:", w)
    for i in range(len(Xb)):
        out = np.sign(np.dot(Xb[i], w))
        print(f"Input: {X[i]}, Output: {out}")

def perceptron_delta_run():
    import numpy as np

    # AND gate dataset
    X = np.array([[0,0], [0,1], [1,0], [1,1]])
    y = np.array([0, 0, 0, 1])  # Output for AND

    # Add bias term
    Xb = np.hstack((X, np.ones((4,1))))

    # Delta rule training
    w = np.zeros(3)
    lr = 0.1
    for epoch in range(10):
        for i in range(len(Xb)):
            out = np.dot(Xb[i], w)
            error = y[i] - out
            w += lr * error * Xb[i]

    # Test
    print("Delta Rule Weights:", w)
    for i in range(len(Xb)):
        out = np.dot(Xb[i], w)
        print(f"Input: {X[i]}, Output: {round(out)}")


def ensemble():
    print('''

VOTING
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

model = VotingClassifier(estimators=[
    ('lr', LogisticRegression()), 
    ('knn', KNeighborsClassifier()), 
    ('dt', DecisionTreeClassifier())],
    voting='hard')

model.fit(X_train, y_train)
print("Voting Accuracy:", accuracy_score(y_test, model.predict(X_test)))

          

          
BAGGING
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier

model = BaggingClassifier(estimator=DecisionTreeClassifier(), n_estimators=10)
model.fit(X_train, y_train)
print("Bagging Accuracy:", accuracy_score(y_test, model.predict(X_test)))
y_pred = model.predict(X_test)
print("Bagging Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:", classification_report(y_test, y_pred))
print("Confusion Matrix:", confusion_matrix(y_test, y_pred))

          



BOOSTING
from sklearn.ensemble import AdaBoostClassifier

model = AdaBoostClassifier(n_estimators=50)
model.fit(X_train, y_train)
print("Boosting Accuracy:", accuracy_score(y_test, model.predict(X_test)))


          
SPAM DETECTION
          

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import StackingClassifier
from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import MultinomialNB,CategoricalNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
df = pd.read_csv("https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv", sep='\\t', names=['label', 'message'])
df['label'] = df['label'].map({'ham': 0, 'spam': 1})
X_train, X_test, y_train, y_test = train_test_split(df['message'], df['label'], test_size=0.2, random_state=42)
pipeline = make_pipeline(
    TfidfVectorizer(),
    StackingClassifier(
        estimators=[('nb', MultinomialNB()), ('svc', SVC(probability=True)), ('rf', RandomForestClassifier(n_estimators=100, random_state=42))],
        final_estimator=LogisticRegression()
    )
)
pipeline.fit(X_train, y_train)
print(classification_report(y_test, pipeline.predict(X_test)))
''')
    
def ensemble_voting_run():
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import VotingClassifier
    from sklearn.metrics import accuracy_score

    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    model = VotingClassifier(estimators=[
        ('lr', LogisticRegression()), 
        ('knn', KNeighborsClassifier()), 
        ('dt', DecisionTreeClassifier())],
        voting='hard')

    model.fit(X_train, y_train)
    print("Voting Accuracy:", accuracy_score(y_test, model.predict(X_test)))

def ensemble_bagging_run():
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import BaggingClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.metrics import accuracy_score

    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    model = BaggingClassifier(estimator=DecisionTreeClassifier(), n_estimators=10)
    model.fit(X_train, y_train)
    print("Bagging Accuracy:", accuracy_score(y_test, model.predict(X_test)))


def ensemble_boosting_run():
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import AdaBoostClassifier
    from sklearn.metrics import accuracy_score

    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)


    model = AdaBoostClassifier(n_estimators=50)
    model.fit(X_train, y_train)
    print("Boosting Accuracy:", accuracy_score(y_test, model.predict(X_test)))

def all():
    print('''
LAB 1:
          

import numpy as np

R = {
          
    "Low Temp": [0.8, 0.5, 0.3],
          
    "Medium Temp": [0.6, 0.7, 0.4],
          
    "High Temp": [0.3, 0.6, 0.9]
          
}

S = {
          
    "Dry": [0.7, 0.4, 0.3],
          
    "Normal": [0.5, 0.6, 0.4],
          
    "Humid": [0.2, 0.5, 0.8]
          
}

temperature_input = "Low Temp"
          
humidity_input = "Dry"

mu_R = R[temperature_input]
          
mu_S = S[humidity_input]

def min_max_composition(mu_R, mu_S):
          
    result = []

    for z in range(3):
          
        min_value = min(mu_R[0], mu_S[0]) if z == 0 else \\
          
                    min(mu_R[1], mu_S[1]) if z == 1 else \\
          
                    min(mu_R[2], mu_S[2])
          
        result.append(min_value)

    return result

composed_result = min_max_composition(mu_R, mu_S)

cooling_action = ["Low Cooling", "Medium Cooling", "High Cooling"]
          
max_membership_value = max(composed_result)
          
action_index = composed_result.index(max_membership_value)

print(f"Input: Temperature = {temperature_input}, Humidity = {humidity_input}")
          
print(f"Membership values for Cooling Actions: {composed_result}")
          
print(f"The system selects: {cooling_action[action_index]} with a membership value of {max_membership_value:.2f}")


OR
          
import numpy as np

def max_min_composition(R1, R2):
    m, n1 = R1.shape
    n2, p = R2.shape
    if n1 != n2:
        raise ValueError("Incompatible shapes for Max-Min composition.")
    result = np.zeros((m, p))
    for i in range(m):
        for j in range(p):
            result[i, j] = np.max(np.minimum(R1[i, :], R2[:, j]))
    
    return result
R1 = np.array([
    [0.2, 0.8],
    [0.6, 0.4]
])
R2 = np.array([
    [0.5, 0.7],
    [0.9, 0.3]
])
composition = max_min_composition(R1, R2)
print("Max-Min Composition:", composition)

import numpy as np
def max_min(R,S):
  m,n1=R.shape
  n2,p=S.shape
  if n1!=n2:
    print("incompatible max min compositon")
  else:
    res=np.zeros((m,p))
    for i in range(m):
      for j in range(p):
        res[i,j]=max(np.minimum(R[i,:],S[:,j]))
  return res
R=np.array([[0.6,0.3],[0.2,0.9]])
S=np.array([[1,0.5,0.3],[0.8,0.4,0.7]])

display("max min relation",max_min(R,S))







LAB 2:
          

          
LAMBDA CUT METHOD
          
fuzzy_set = {'x': 4.5, 'y': 3.5, 'z':4.33}

lambda_value = 4

def lambda_cut(fuzzy_set, lambda_value):
          
    cut_set = []

    for element, membership_value in fuzzy_set.items():
          
        if membership_value >= lambda_value:
          
            cut_set.append(element)

    return cut_set

result = lambda_cut(fuzzy_set, lambda_value)

print(f"Elements in the fuzzy set with membership >= {lambda_value}: {result}")
          

          
MEAN OF MAXIMUM METHOD
          
def mean_of_maximum(fuzzy_set):
          
    max_membership = max(fuzzy_set.values())

    max_x_values = [x for x, mu in fuzzy_set.items() if mu == max_membership]

    return sum(max_x_values) / len(max_x_values)

fuzzy_set = {1: 0.2, 2: 0.5, 3: 0.8, 4: 1.0, 5: 1.0, 6: 0.7, 7: 0.3}

result = mean_of_maximum(fuzzy_set)

print(f"Mean of Maximum (MOM) defuzzified value: {result}")
          


CENTER OF GRAVITY METHOD
          
def center_of_gravity(fuzzy_set):
    numerator = sum(x * mu for x, mu in fuzzy_set.items())

    denominator = sum(fuzzy_set.values())

    return numerator / denominator if denominator != 0 else 0

fuzzy_set = {1: 0.2, 2: 0.5, 3: 0.8, 4: 1.0, 5: 0.7}

result = center_of_gravity(fuzzy_set)

print(f"Center of Gravity (COG) defuzzified value: {result}")
          

          








LAB 3:
          

import random

# Fitness function
def fitness(x): 
    return x**2

# Decode binary string to integer
def decode(chrom): 
    return int(chrom, 2)

# Create random chromosome
def random_chrom(): 
    return ''.join(random.choice('01') for _ in range(5))

# Selection (tournament)
def select(pop): 
    return max(random.sample(pop, 2), key=lambda c: fitness(decode(c)))

# Crossover (single point)
def crossover(p1, p2):
    point = random.randint(1, 4)
    return p1[:point] + p2[point:], p2[:point] + p1[point:]

# Mutation (flip bit)
def mutate(chrom, rate=0.1):
    return ''.join(b if random.random() > rate else str(1-int(b)) for b in chrom)

# Genetic Algorithm
pop = [random_chrom() for _ in range(10)]
for gen in range(20):  # 20 generations
    pop = [mutate(c) for _ in range(5) for c in crossover(select(pop), select(pop))]
    best = max(pop, key=lambda c: fitness(decode(c)))
    print(f"Gen {gen+1:2d}: Best = {decode(best)} (Fitness = {fitness(decode(best))})")

# Final best result
best = max(pop, key=lambda c: fitness(decode(c)))
print("Final Best solution:", decode(best), "Fitness:", fitness(decode(best)))


          







LAB 4:
          
MERGE SORT
def merge_sort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(a, b):
    res = []
    while a and b:
        res.append(a.pop(0) if a[0] < b[0] else b.pop(0))
    return res + a + b

# Example
arr = [5, 2, 9, 1, 3]
print("Sorted:", merge_sort(arr))

          













LAB 5:
          

import numpy as np

# Distance matrix between 4 cities
dist = np.array([[0, 2, 2, 5],
                 [2, 0, 3, 4],
                 [2, 3, 0, 1],
                 [5, 4, 1, 0]])

n_ants = 4
n_iterations = 10
alpha = 1      # pheromone importance
beta = 2       # distance importance
evaporation = 0.5
Q = 100        # pheromone deposit factor

n_cities = len(dist)
pheromone = np.ones((n_cities, n_cities))  # initial pheromones

def probability(from_city, visited):
    probs = []
    for to_city in range(n_cities):
        if to_city in visited: probs.append(0)
        else:
            tau = pheromone[from_city][to_city] ** alpha
            eta = (1 / dist[from_city][to_city]) ** beta
            probs.append(tau * eta)
    probs = np.array(probs)
    return probs / probs.sum()

def build_tour():
    tour = [np.random.randint(n_cities)]
    while len(tour) < n_cities:
        probs = probability(tour[-1], tour)
        next_city = np.random.choice(range(n_cities), p=probs)
        tour.append(next_city)
    return tour + [tour[0]]  # return to start

def tour_length(tour):
    return sum(dist[tour[i]][tour[i+1]] for i in range(n_cities))

for it in range(n_iterations):
    all_tours = [build_tour() for _ in range(n_ants)]
    pheromone *= (1 - evaporation)
    for tour in all_tours:
        length = tour_length(tour)
        for i in range(n_cities):
            a, b = tour[i], tour[i+1]
            pheromone[a][b] += Q / length
            pheromone[b][a] += Q / length  # symmetric

    best = min(all_tours, key=tour_length)
    print(f"Iter {it+1}: Best tour = {best}, Length = {tour_length(best)}")

          


OR
          

import numpy as np

d = np.array([  [0,2,2,5],
                [2,0,3,4],
                [2,3,0,1],
                [5,4,1,0]])  # Distance matrix
n = len(d); p = np.ones((n,n))  # Pheromones

def tour():
    t = [np.random.randint(n)]
    while len(t) < n:
        r = t[-1]; u = [i for i in range(n) if i not in t]
        prob = [(p[r][j] / d[r][j])**2 for j in u]
        prob = prob / np.sum(prob)
        t.append(np.random.choice(u, p=prob))
    return t + [t[0]]

def length(t): return sum(d[t[i]][t[i+1]] for i in range(n))

for _ in range(10):
    T = [tour() for _ in range(n)]
    p *= 0.5
    for t in T:
        l = length(t)
        for i in range(n): p[t[i]][t[i+1]] += 100 / l
    b = min(T, key=length)
    print("Best tour:", b, "Length:", length(b))

          










LAB 6:
          

import numpy as np

def f(x): return x**2  # Objective function

n_particles = 10
n_iterations = 20
x = np.random.uniform(-10, 10, n_particles)  # positions
v = np.zeros(n_particles)                   # velocities
pbest = x.copy()
pbest_val = f(x)
gbest = x[np.argmin(pbest_val)]

for i in range(n_iterations):
    r1, r2 = np.random.rand(), np.random.rand()
    v = 0.5*v + r1*(pbest - x) + r2*(gbest - x)
    x += v
    fx = f(x)
    mask = fx < pbest_val
    pbest[mask] = x[mask]
    pbest_val[mask] = fx[mask]
    gbest = x[np.argmin(pbest_val)]
    
    print(f"Iter {i+1}: gbest = {gbest:.4f}, f(gbest) = {f(gbest):.4f}")
    print("        pbest =", np.round(pbest, 4))


          







LAB 7:
          
import numpy as np

def f(x): return x**2  # Objective function

wolves = np.random.uniform(-10, 10, 5)  # 5 grey wolves (1D)
alpha, beta, delta = None, None, None

for iter in range(20):
    sorted_idx = np.argsort(f(wolves))
    alpha, beta, delta = wolves[sorted_idx[:3]]

    a = 2 - iter * (2 / 20)  # linearly decrease from 2 to 0
    for i in range(len(wolves)):
        for leader in [alpha, beta, delta]:
            r1, r2 = np.random.rand(), np.random.rand()
            A = a * (2*r1 - 1)
            C = 2 * r2
            D = abs(C * leader - wolves[i])
            X = leader - A * D
            wolves[i] = (wolves[i] + X) / 2  # average with current position

    best = alpha
    print(f"Iter {iter+1}: Best = {best:.4f}, f(Best) = {f(best):.4f}")



          







LAB 8:
          

from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Load Iris dataset
data = load_iris()
X = data.data[:, :2]  # Use first two features for easy 2D plotting

# Apply K-Means with 3 clusters
kmeans = KMeans(n_clusters=3, random_state=0)
labels = kmeans.fit_predict(X)
centers = kmeans.cluster_centers_

# Plot the clustered data
plt.figure(figsize=(6, 4))
for i in range(3):
    plt.scatter(X[labels == i, 0], X[labels == i, 1], label=f"Cluster {i}")
plt.scatter(centers[:, 0], centers[:, 1], c='black', marker='x', label='Centroids')
plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')
plt.title('Crisp Partitioning of Iris Data (K-Means)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


          










LAB 9:
          

HEBBS RULE
import numpy as np

# AND gate dataset
X = np.array([[0,0], [0,1], [1,0], [1,1]])
y = np.array([-1, -1, -1, 1])  # AND logic (-1 for 0, 1 for 1)

# Add bias term
Xb = np.hstack((X, np.ones((4,1))))

# Hebb's learning rule: w += x * y
w = np.zeros(3)
for i in range(len(Xb)):
    w += Xb[i] * y[i]

# Test
print("Hebb's Rule Weights:", w)
for i in range(len(Xb)):
    out = np.sign(np.dot(Xb[i], w))
    print(f"Input: {X[i]}, Output: {out}")

          
DELTA RULE
import numpy as np

# AND gate dataset
X = np.array([[0,0], [0,1], [1,0], [1,1]])
y = np.array([0, 0, 0, 1])  # Output for AND

# Add bias term
Xb = np.hstack((X, np.ones((4,1))))

# Delta rule training
w = np.zeros(3)
lr = 0.1
for epoch in range(10):
    for i in range(len(Xb)):
        out = np.dot(Xb[i], w)
        error = y[i] - out
        w += lr * error * Xb[i]

# Test
print("Delta Rule Weights:", w)
for i in range(len(Xb)):
    out = np.dot(Xb[i], w)
    print(f"Input: {X[i]}, Output: {round(out)}")


          









LAB 10:


VOTING
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

model = VotingClassifier(estimators=[
    ('lr', LogisticRegression()), 
    ('knn', KNeighborsClassifier()), 
    ('dt', DecisionTreeClassifier())],
    voting='hard')

model.fit(X_train, y_train)
print("Voting Accuracy:", accuracy_score(y_test, model.predict(X_test)))

          

          
BAGGING
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier

model = BaggingClassifier(estimator=DecisionTreeClassifier(), n_estimators=10)
model.fit(X_train, y_train)
print("Bagging Accuracy:", accuracy_score(y_test, model.predict(X_test)))
y_pred = model.predict(X_test)
print("Bagging Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:", classification_report(y_test, y_pred))
print("Confusion Matrix:", confusion_matrix(y_test, y_pred))

          



BOOSTING
from sklearn.ensemble import AdaBoostClassifier

model = AdaBoostClassifier(n_estimators=50)
model.fit(X_train, y_train)
print("Boosting Accuracy:", accuracy_score(y_test, model.predict(X_test)))


          
SPAM DETECTION
          
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import StackingClassifier
from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import MultinomialNB,CategoricalNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
df = pd.read_csv("https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv", sep='\\t', names=['label', 'message'])
df['label'] = df['label'].map({'ham': 0, 'spam': 1})
X_train, X_test, y_train, y_test = train_test_split(df['message'], df['label'], test_size=0.2, random_state=42)
pipeline = make_pipeline(
    TfidfVectorizer(),
    StackingClassifier(
        estimators=[('nb', MultinomialNB()), ('svc', SVC(probability=True)), ('rf', RandomForestClassifier(n_estimators=100, random_state=42))],
        final_estimator=LogisticRegression()
    )
)
pipeline.fit(X_train, y_train)
print(classification_report(y_test, pipeline.predict(X_test)))

          
''')
    


def help():
    print('''
          
fuzzy_relation()
fuzzy_relation_run()
defuzzification()
defuzzification_run_lambda()
defuzzification_run_MOM()
defuzzification_run_COG()
genetic_algorithm()
genetic_algorithm_run()
distributive_parallel()
distributive_parallel_run()
ant_colony_optimization()
ant_colony_optimization_run()
particle_swarm_optimization()
particle_swarm_optimization_run()
grey_wolf_optimization()
grey_wolf_optimization_run()
crisp_partition()
crisp_partition_run()
perceptron()
perceptron_hebbs_run()
perceptron_delta_run()
ensemble()
ensemble_voting_run()
ensemble_bagging_run()
ensemble_boosting_run()
all()
help()
''')