import unittest
import time
import json

from model import swarm


class SwarmTests(unittest.TestCase):

    def test_serializability(self):
        s = swarm.Swarm(10, 10, 10)
        s1 = swarm.Swarm.from_dict(json.loads(json.dumps(s.to_dict())))


if __name__ == '__main__':
    unittest.main()
