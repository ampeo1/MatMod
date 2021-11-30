import numpy as np
import simpy as sp


class QueueSystem(object):
    def __init__(self, env, n, m, _lambda, mu, v):
        self.n = n
        self.m = m
        self._lambda = _lambda
        self.mu = mu
        self.v = v

        self.counts = []
        self.times = []
        self.queue_counts = []
        self.queue_times = []

        self.serve_items = []
        self.reject_items = []

        self.env = env
        self.resources = sp.Resource(env, n)

    def serve(self):
        yield self.env.timeout(np.random.exponential(1.0 / self.mu))

    def wait(self):
        yield self.env.timeout(np.random.exponential(1.0 / self.v))

    def get_workload(self):
        return self.resources.count

    def get_queue_len(self):
        return len(self.resources.queue)

    def start(self, action):
        while True:
            yield self.env.timeout(np.random.exponential(1 / self._lambda))
            self.env.process(action(self))