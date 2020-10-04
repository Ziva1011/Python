
import random
import numpy as np

"""
    n - number of objects to choose
    w - maximum carrying capacity of the knapsack
    s . maximum kanpsack siza
    output - name of the file into which the task is to be saved
"""

class object:
    def __init__(self,weight, size, cost):
        self.w = int(weight)
        self.s = int(size)
        self.c = int(cost)


class ind:
    def __init__(self, n_obj):
        self.active_obj=[]
        self.n_obj=n_obj
        self.fitness_v=0

    def fitness(self,task):
        w_total=0
        s_total=0
        c_total=0
        for i in range(len(self.active_obj)):
            if self.active_obj[i]==1:
                w_total+=task[i].w
                s_total+=task[i].s
                c_total+=task[i].c
        if w_total<w and s_total<s:
            return c_total
        else:
            return 0


class population:
    def __init__(self, size):
        self.size=size
        self.pop=[]


def generate_variables():
    n = random.randint(1000,2000)
    w = random.randint(10000,20000)
    s = random.randint(10000,20000)

    return n,w,s


def generate(output_file):
    total_w=0
    total_s=0

    n,w,s = generate_variables();

    file = open(output_file,"w")

    file.write(str(n)+","+ str(w)+","+ str(s)+"\n")

    while total_w<2*w or total_s<2*s:
        total_w=0
        total_s=0
        i=0
        obj=[]

        while i< n:
            w_i= random.randrange(1,int(10*w/n))
            s_i= random.randrange(1, int(10*s/n))
            c_i = random.randrange(1,n)

            obj.append((w_i,s_i,c_i))

            total_w += w_i
            total_s += s_i
            i+=1

    for x in obj:
        file.write(str(x[0])+","+ str(x[1])+","+ str(x[2])+"\n")
    file.close()

    return n,w,s


def read(input_file):
    file = open(input_file,"r")
    _,_,_= file.readline().strip("\n").split(",")
    new_task = []
    for i in range (int(n)):
        wi,si,ci = file.readline().strip("\n").split(",")
        new_obj = object(wi,si,ci)
        new_task.append(new_obj)
    return new_task


def init_individual(n,n_items,task):
    new_ind = ind(n_items)

    curr_ind=[0]*n

    for i in range (n_items):
        curr_ind[i]=1

    np.random.shuffle(curr_ind)

    new_ind.active_obj=curr_ind

    new_ind.fitness_v=new_ind.fitness(task)

    return new_ind


def init_population (n_items, size, n,task):
    new_pop=population(size)
    for i in range(size):
        new_pop.pop.append(init_individual(n,n_items,task))
    return new_pop


def tournament (population, tournament_size,task):

    winner_ind = random.randrange(1,population.size-1)
    max_fitness = population.pop[winner_ind].fitness_v


    i=1
    for i in range (tournament_size):
        new_ind=random.randrange(1,population.size-1)
        ind_fitness = population.pop[new_ind].fitness_v

        if ind_fitness>max_fitness:
            winner_ind=new_ind
            max_fitness=ind_fitness

    return population.pop[winner_ind]


def crossover(parent1, parent2, crossover_rate):
    child=ind(parent1.n_obj)

    if random.uniform(0,1)> crossover_rate:
        return parent1
    else:
        cut=random.randrange(0,n)
        child.active_obj=parent1.active_obj[0:cut]
        child.active_obj.extend(parent2.active_obj[cut:])
        return child


def mutation(individual, mutation_rate, n):
    n_changes = int(n*mutation_rate)

    for i in range (n_changes):
        pos=random.randint(0,n-1)
        individual.active_obj[pos]=int(not individual.active_obj[pos])
    return individual


def genetic_algorithm(input_file):
    n_items = 100
    size = 100
    iterations = 1000
    tournament_size = int(0.05*size)
    crossover_rate = 0.7
    mutation_rate = 0.001

    file = open("fitness.csv","w")

    task = read (input_file)
    pop=init_population(n_items,size,n,task)
    i=0

    best_ind=pop.pop[0]
    best_ind_gen=pop.pop[0]

    for i in range(0, iterations):
        new_pop = population(size)

        max_fitness_gen=0

        for j in range (size):
            parent1 = tournament(pop, tournament_size,task)
            parent2 = tournament(pop, tournament_size,task)
            child = crossover(parent1,parent2,crossover_rate)
            child = mutation(child,mutation_rate,n)
            child.fitness_v = child.fitness(task)
            new_pop.pop.append(child)

            if max_fitness_gen<child.fitness_v:
                max_fitness_gen=child.fitness_v
                best_ind_gen.active_obj=child.active_obj
                best_ind_gen.fitness_v=child.fitness_v


        pop=new_pop
        file.write(str(best_ind_gen.fitness_v)+"\n")
        if best_ind_gen.fitness_v > best_ind.fitness_v:
            best_ind=best_ind_gen


    file.close()
    return best_ind


"""---Begining of program---"""
input_file = "test.csv"
n,w,s = generate(input_file)

best=genetic_algorithm(input_file)
