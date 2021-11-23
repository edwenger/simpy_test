import itertools
import random

import simpy


def prob_fsw(t):
    return 1 if t > 20 else 0


def prob_fsw_client(t):
    return 1 if t > 20 else 0


def decide_FSW(self, env):

    if random.random() > prob_fsw(env.now):
        return

    yield env.timeout(random.uniform(0, 5))  # delay to enroll
    print('(t=%d) %s Starting FSW...' % (env.now, self))
    self.risk_state = 'HIGH'

    yield env.timeout(random.expovariate(5))  # delay to dropout
    print('(t=%d) %s Ending FSW...' % (env.now, self))
    self.risk_state = 'MEDIUM'


def decide_FSW_client(self, env):
    
    if random.random() > prob_fsw_client(env.now):
        return

    yield env.timeout(random.uniform(0, 10))  # delay to enroll
    print('(t=%d) %s Starting FSW client...' % (env.now, self))
    self.risk_state = 'HIGH'

    yield env.timeout(random.uniform(2, 30))  # delay to dropout
    print('(t=%d) %s Ending FSW client...' % (env.now, self))
    self.risk_state = 'MEDIUM'


class Individual(object):

    uid = itertools.count()  # unique index generator

    def __init__(self, env, sex=None):
        self.env = env
        self.risk_proc = env.process(self.fsw_cascade(env))
        self.birth_year = env.now
        self.sex = sex if sex is not None else random.choice(['M', 'F'])
        self.uid = next(Individual.uid)
        self.risk_state = 'LOW'

    def __str__(self):
        return '[%d: %d%s]' % (self.uid, self.age, self.sex)

    @property
    def age(self):
        return self.env.now - self.birth_year

    def fsw_cascade(self, env):
        
        # age 15 years (i.e. STIdebut)
        yield env.timeout(15)

        # decide FSW draw
        print('(t=%d) %s Deciding about FSW...' % (env.now, self))

        match self.sex:
            case 'F':
                env.process(decide_FSW(self, env))
            case 'M':
                env.process(decide_FSW_client(self, env))


def birth_demographics(env):

    while True:
        yield env.timeout(random.uniform(0, 5))
        next_individual = Individual(env)


if __name__ == '__main__':
    
    env = simpy.Environment()
    env.process(birth_demographics(env))
    env.run(until=30)
