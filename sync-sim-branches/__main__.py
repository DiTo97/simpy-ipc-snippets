import os
import simpy
import time


def clock(_env: simpy.Environment,
          name: str, tick: int):
    while True:
        print(name, _env.now)
        yield _env.timeout(tick)


Delta: int = 5
t: float = 0.1

if __name__ == '__main__':
    env = simpy.Environment()

    env.process(clock(env, 'Fast', 1))
    env.run(until=Delta)

    print('    [Global] Environment clock: {} sec'
          .format(env.now))

    flags = os.O_NONBLOCK
    r, w = os.pipe2(flags)

    r, w = os.fdopen(r, 'r'), \
           os.fdopen(w, 'w')

    # Create a child process
    # using os.fork() method
    pid = os.fork()

    if pid > 0: # Parent process
        # Close file descriptor w
        # as it only has to listen
        w.close()

        t_no_response: float = 0

        # Read from child process
        print("\n    [Parent] Process is reading")

        while True:
            data = r.readline()

            if not data:
                if t_no_response % 10*t:
                    print('    [Parent] Nothing to read. Waiting...')

                t_no_response += t

                if t_no_response > 30*t:
                    print('    [Parent] No signs from the child '
                          'after {} sec. Exiting...'
                          .format(30*t))
                    break

                time.sleep(t)
                continue

            final_t = int(data.strip())

            print('    [Parent] Child final clock: {} sec'
                  .format(final_t))
            print('    [Parent] Environment clock: {} sec'
                  .format(env.now))

            env.run(until=final_t)

            print('    [Parent] Environment clock: {} sec'
                  .format(env.now))
    else:       # Child process
        # Closes file descriptor r
        # as it only has to emit
        r.close()

        env.run(until=Delta*3)

        # Write some text to file descriptor w
        print("    [Child] Process is writing")

        w.write("%d" % env.now)
        w.flush()

        print('    [Child] Environment clock: {} sec'
              .format(env.now))
