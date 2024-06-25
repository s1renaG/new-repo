import unittest
from random_generator import RandomGenerator


class TestRandomGenerator(unittest.TestCase):

    def test_stats_generation(self):
        num_records = 1

        for _ in range(num_records):
            generator = RandomGenerator()
            stats_data = generator.stats(generator.k, generator.a, generator.d)

            # Retrieve stats from stats_data dictionary
            kd = stats_data['kd']
            kr = stats_data['kr']
            assists = stats_data['assists']
            survival_rate = stats_data['survival_rate']

            # Calculate expected values
            expected_kd = generator.k / generator.d if generator.d != 0 else generator.k
            expected_kr = generator.k / generator.total_rounds if generator.total_rounds != 0 else 0
            expected_survival_rate = generator.d / generator.total_rounds if generator.total_rounds != 0 else 0

            # Assert each statistic value
            self.assertAlmostEqual(kd, expected_kd, delta=0.0001)
            self.assertAlmostEqual(kr, expected_kr, delta=0.0001)
            self.assertEqual(assists, generator.a)
            self.assertAlmostEqual(survival_rate, expected_survival_rate, delta=0.0001)

            print(f"kd: {kd}, expected_kd: {expected_kd}")
            print(f"kr: {kr}, expected_kr: {expected_kr}")
            print(f"assists: {assists}")
            print(f"survival_rate: {survival_rate}, expected_survival_rate: {expected_survival_rate}")


if __name__ == '__main__':
    unittest.main()
