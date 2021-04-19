import random

# Velocidade média de tráfego (em m/s)
TRAFFIC_SPEED = 13.8

# Retorna o custo adicional que será adicionado no grafo de maneira dinâmica
# Está sendo implementado como um simples RNG, para simular os aspectos estocásticos
# da implementação.
# O algoritmo RNG aleatório segue uma distribuição na forma de:
# 50% -> 3
# 20% -> 2, 4
# 5% -> 1, 5 
def gen_traffic_cost():
  weighted_costs = [1, 5] * 1 + [2, 4] * 4 + [3] * 10
  return random.choice(weighted_costs)

# Calcula o tempo médio (em segundos) para percorrer uma distância
# assumindo velocidade média em todo o percurso de 50 km/h (13,8 m/s).
def get_expected_time(dist, traffic_cost):
  virtual_dist = dist * traffic_cost
  return virtual_dist / TRAFFIC_SPEED
