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
        new_spawn=[]
        for person in self.People:
            new_spawn.append(person.mutate(mutation_coefficient))
        self.People=self.People+new_spawn
        self.Generation+=1

    def __repr__(self):
        return_object= 'Gen = ' + str(self.Generation)
        for i in self.People:
            return_object = return_object + ' ' + '{' + str(i.__repr__()) + '}'
        return(return_object)


# Need a class to represent a person in my population
class Person:
    def __init__(self,chromosomes,score,name=''):
        self.Name=name
        self.Chromosomes=chromosomes
        self.Score=score

    # Need a function that will mutate the chromosomes of a person with a
    # given mutation coefficient
    def mutate(self,mutation_coefficient):
        new_chromes=[]
        for chrome in self.Chromosomes:
            new_chromosome=chrome.mutate(mutation_coefficient)
            new_chromes.append(new_chromosome)
        return(Person(new_chromes,self.Score,self.Name))

    def __repr__(self):
        return_object='Name = ' + self.Name + ', '
        for i in self.Chromosomes:
            return_object=return_object + str(i.__repr__()) + ' '
        return_object=return_object + 'Score = ' + str(self.Score)
        return(return_object)




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
            new_chromosome=Chromosome(self.Name,self.Potential_values,self.Potential_values[random.randint(0,len(self.Potential_values)-1)])
            return(new_chromosome)
        return(self)

    def __repr__(self):
        return(self.Name + ' = ' + str(self.Value))




