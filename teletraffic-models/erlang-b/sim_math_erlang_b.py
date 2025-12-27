from sim_erlang_b import simulate_erlang_b
from math_erlang_b import recurrentErlangformula


C = 3          
mu = 2.0        
SIM_TIME = 100000
call_arrival_lambda = 4.0
alpha = call_arrival_lambda / mu

sim = simulate_erlang_b(C, alpha, mu, SIM_TIME)
mathematicalModel = recurrentErlangformula(C, alpha)

print(f"Simulated: {sim:.7f}, Mathematical: {mathematicalModel:.7f}")