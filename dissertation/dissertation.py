from swarm import optimize

a = optimize(lambda (x, y): -abs(((x * 10) ** 2) - (y * 10)) - (100 if x == 0 else 0), 2, 100, max_iterations=1000)