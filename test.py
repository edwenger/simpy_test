import simpy


class Individual(object):

    def __init__(self, env):
        self.env = env
        self.risk_proc = env.process(self.risk(env))

    def risk(self, env):
        # age 15 years
        yield env.timeout(15)

        # make CSW draw
        print('Deciding about CSW at t =', env.now)


if __name__ == '__main__':
    
    env = simpy.Environment()
    ind = Individual(env)
    env.run(until=20)
