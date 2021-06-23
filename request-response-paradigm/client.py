import itertools
import sys
import zmq

# Custom imports
from utils.logger import Logger

from config import _Request, _Server


_Server['ENDPOINT'] = '{}://{}:{}'.format(_Server['PROTOCOL'],
                                          _Server['HOST'], _Server['PORT'])


if __name__ == '__main__':
    with zmq.Context() as context:
        Logger.info("Connecting to server…")

        client = context.socket(zmq.REQ)
        client.connect(_Server['ENDPOINT'])

        # Generate a dummy sequence of requests
        for sequence in itertools.count():
            request = str(sequence).encode()

            Logger.info("Sending request: (%s)", request)
            client.send(request)

            retries_left = _Request['RETRIES']

            while True:
                if (client.poll(_Request['TIMEOUT'])
                        & zmq.POLLIN) != 0:
                    reply = client.recv()

                    if int(reply.decode()) == sequence:
                        Logger.info("Server replied: (%s)", reply)
                        break
                    else:
                        Logger.error("Got malformed reply: %s", reply)
                        continue

                retries_left -= 1

                Logger.warning("No response from server")

                # Socket is confused by the noop.
                # Close and remove it.
                client.setsockopt(zmq.LINGER, 0)
                client.close()

                if retries_left == 0:
                    Logger.error("Server seems to be offline, abandoning...")
                    sys.exit()

                Logger.info("Reconnecting to server...")

                # Create new connection
                client = context.socket(zmq.REQ)
                client.connect(_Server['ENDPOINT'])

                Logger.info("Resending (%s)", request)

                client.send(request)
