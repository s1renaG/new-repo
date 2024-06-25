import random
import pandas as pd


class RandomGenerator:

    def __init__(self):
        self.won = random.randint(0, 12)
        self.lost = random.randint(0, 12)
        self.k = random.randint(0, 40)
        self.a = random.randint(0, 20)
        self.total_rounds = self.lost + self.won
        self.d = random.randint(0, self.total_rounds)

    def stats(self, k, a, d):
        kd = k / d if d != 0 else k
        kr = k / self.total_rounds if self.total_rounds != 0 else 0
        assists = a
        survival_rate = d / self.total_rounds if self.total_rounds != 0 else 0
        return {
            'kd': kd,
            'kr': kr,
            'assists': assists,
            'survival_rate': survival_rate
        }


data = []
num_records = 1
for _ in range(num_records):
    generator = RandomGenerator()
    stats_data = generator.stats(generator.k, generator.a, generator.d)
    data.append(stats_data)

df = pd.DataFrame(data)
df.to_csv("results.csv", index=False)
