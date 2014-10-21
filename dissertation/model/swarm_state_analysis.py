import json


output_location = r'I:\Users\Chase Stevens\Dropbox\Dissertation\swarm_state.json'

with open(output_location, 'r') as f:
    swarm_state = json.load(f)

particles = swarm_state['particles'].values()

best_found = max(particles, key=lambda x: x['best_fitness'])
print best_found['time']
print

print 'best'
fields = 'iterations initial_inertia cognitive_comp social_comp inertial_dampening velocity_dampening'.split()
print best_found['best_fitness']
for x, y in zip(fields, best_found['best_position']):
    print x, y

print 

n = 10
print 'top', n
p_bests = sorted(particles, key=lambda x: x['best_fitness'], reverse=True)[:n]
print sum(particle['best_fitness'] for particle in p_bests) / float(n)
for i, field in enumerate(fields):
    print field, sum(p['best_position'][i] for p in p_bests) / float(n)
#print sorted((particle['best_fitness'] for particle in particles), reverse=True)[:5]

print

print 'average'
p_bests = [particle['best_position'] for particle in particles]
p_num = float(len(p_bests))
print sum(particle['best_fitness'] for particle in particles) / p_num
for i, field in enumerate(fields):
    print field, sum(p[i] for p in p_bests) / p_num

print

print 'current average'
p_bests = [particle['position'] for particle in particles]
p_num = float(len(p_bests))
#print sum(particle['fitness'] for particle in particles) / p_num
for i, field in enumerate(fields):
    print field, sum(p[i] for p in p_bests) / p_num

raw_input()