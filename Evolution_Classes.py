import random

#Basic population for the evolution method
class Population:
    def __init__(self,people,chromosomes,generation = 1):
        # Need a list of the 'people' in my population
        self.People=people
        # Number to tell me what generation my population is up to
        self.Generation=generation
        self.Chromosomes=chromosomes

    # Need a function that will kill of the weakest half of the population
    def kill(self):
        # Create an iteration with length equal to the number of people
        # we want to kill of (in this case half)
        for i in range(int(len(self.People)/2)):
            # Create a list of scores and then find the minimum one
            scores=[]
            for j in self.People:
                scores.append(j.Score)
            min_score=min(scores)
            n=0
            while n>-1:
                # Remove a person from the population with a score equal
                # to that of the minimum one
                if self.People[n].Score==min_score:
                    self.People.remove(self.People[n])
                    n=-1
                else:
                    n+=1

    def mutate(self,mutation_coefficient):
        new_spawn=self.People
        for i in new_spawn:
            i.mutate(mutation_coefficient)
            self.People.append(i)



# Need a class to represent a person in my population
class Person:
    def __init__(self,chromosomes,name,score):
        self.Name=name
        self.Chromosomes=chromosomes
        self.Score=score

    # Need a function that will mutate the chromosomes of a person with a
    # given mutation coefficient
    def mutate(self,mutation_coefficient):
        for i in self.Chromosomes:
            i.mutate(mutation_coefficient)


# Creating a class to represent a Chromosome
class Chromosome:
    def __init__(self,name,potential_values, value):
        # Each Chromosome must have a name and a set of values it
        # can take
        self.Name=name
        self.Potential_values=potential_values
        self.Value=value

    # Want a function that mutates the chromosomes with a given coefficient.
    # Will use a simple bernoulli variable for the mutations
    def mutate(self,mutation_coefficient):
        mutation_number= random.randint(1,1000)
        if mutation_number<=1000*mutation_coefficient:
            self.Value=self.Potential_values[random.randint(0,len(self.Potential_values)-1)]





