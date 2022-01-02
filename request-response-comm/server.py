from random import randint
import itertools
import simpy
import zmq

# Custom imports
from utils.logger import Logger

from config import _Server


_Server['ENDPOINT'] = '{}://*:{}'.format(_Server['PROTOCOL'],
                                         _Server['PORT'])


#
# Define the processes
#


def clock(_env: simpy.Environment,
          name: str, tick: int):
    while True:
        print(name, _env.now)
        yield _env.timeout(tick)


def master(_env: simpy.Environment):
    with zmq.Context() as context:
        server = context.socket(zmq.REP)
        server.bind(_Server['ENDPOINT'])

        try:
            for cycles in itertools.count():
                try:
                    if cycles == 10:
                        Logger.info("Starting slow process...")
                        _env.process(clock(_env, 'Slow', 10))

                    request = server.recv(flags=zmq.NOBLOCK)

                    # Simulate various problems
                    if cycles > 100 and randint(0, 6) == 0:
                        Logger.info("Simulating a crash...")
                        break
                    
                    if cycles > 50 and randint(0, 3) == 0:
                        Logger.info("Simulating CPU overload...")
                        yield _env.timeout(3)

                    # TODO: Do some heavy work
                    Logger.info("Normal request (%s)", request)
                    yield _env.timeout(1)

                    server.send(request)
                except zmq.Again:
                    yield _env.timeout(0.3)
        except Exception:
            pass
        finally:
            server.close()


Delta: int = 60
_step: int = Delta // 5

if __name__ == '__main__':
    env = simpy.rt.RealtimeEnvironment()

    env.process(master(env))
    env.process(clock(env, 'Fast', 1))

    # while env.now <= Delta:
    #     env.step()

    # for i in range(_step, Delta + _step,
    #                _step):
    #     env.run(until=i)

    env.run(until=Delta)
