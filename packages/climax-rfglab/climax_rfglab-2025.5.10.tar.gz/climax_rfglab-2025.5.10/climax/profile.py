import time
from climax.climax import climax
  
a = climax('./tests/cells_movie.tif')
a.action_zoom()
a.action_zoom()

# We are going to increase this as the code gets faster and faster.
NUM_ITER = 10

t0 = time.perf_counter()
for _ in range(NUM_ITER):
    a.action_next_slice()
    
t1 = time.perf_counter()

took = (t1 - t0) / NUM_ITER
print(f"Took and avg of {took * 1000:.2f}ms per iteration")