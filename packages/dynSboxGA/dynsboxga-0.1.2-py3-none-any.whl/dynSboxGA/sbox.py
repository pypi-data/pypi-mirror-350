import numpy as np
import random
import pandas as pd

class DynamicAESSBoxGA:
    def __init__(self, population_size=50, generations=100, mutation_rate=0.1):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

    def generate_sbox(self):
        return np.random.permutation(256).tolist()

    def evaluate_sbox(self, sbox):
        non_linearity = self.compute_non_linearity(sbox)
        avalanche = self.compute_avalanche(sbox)
        return non_linearity + avalanche

    def compute_non_linearity(self, sbox):
        diff_table = np.zeros((256, 256), dtype=int)
        for x in range(256):
            for y in range(256):
                diff_table[x ^ y][sbox[x] ^ sbox[y]] += 1
        return np.sum(diff_table == 0)

    def compute_avalanche(self, sbox):
        flips = 0
        for x in range(256):
            for bit in range(8):
                flipped_x = x ^ (1 << bit)
                if sbox[x] != sbox[flipped_x]:
                    flips += 1
        return flips / (256 * 8)

    def crossover(self, parent1, parent2):
        cut = random.randint(1, 255)
        child = np.concatenate((parent1[:cut], parent2[cut:]))
        return self.repair_sbox(child)

    def mutate(self, sbox):
        if random.random() < self.mutation_rate:
            i, j = random.sample(range(256), 2)
            sbox[i], sbox[j] = sbox[j], sbox[i]
        return sbox

    def repair_sbox(self, sbox):
        missing_values = set(range(256)) - set(sbox)
        duplicates = {x for x in sbox if list(sbox).count(x) > 1}
        sbox_fixed = list(sbox)
        for i, value in enumerate(sbox):
            if value in duplicates:
                sbox_fixed[i] = missing_values.pop()
                duplicates.remove(value)
        return sbox_fixed

    def apply_ga(self):
        population = [self.generate_sbox() for _ in range(self.population_size)]
        for generation in range(self.generations):
            scores = [self.evaluate_sbox(sbox) for sbox in population]
            ranked_population = sorted(zip(scores, population), reverse=True)
            best_sbox = ranked_population[0][1]
            best_score = ranked_population[0][0]
            print(f"Generation {generation+1}: Best Score = {best_score}")
            survivors = [sbox for _, sbox in ranked_population[:self.population_size // 2]]
            new_population = []
            for _ in range(self.population_size // 2):
                parent1, parent2 = random.sample(survivors, 2)
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)
            population = survivors + new_population
        return best_sbox

    def export_sbox(self, sbox, filename="dynamic_sbox.txt"):
        with open(filename, "w") as f:
            f.write(",".join(map(str, sbox)))
        print(f"S-box saved to {filename}")

def display_sbox_hex_table(sbox):
    hex_sbox = [f"{val:02X}" for val in sbox]
    hex_matrix = np.array(hex_sbox).reshape((16, 16))
    df = pd.DataFrame(hex_matrix)

    # Set bold labels for columns and index
    df.columns = [f"Col {i}" for i in range(16)]
    df.index = [f"Row {i}" for i in range(16)]

    # Style the DataFrame
    styled_df = df.style.set_table_styles(
        [{'selector': 'th', 'props': [('font-weight', 'bold')]}]  # bold for headers
    ).set_properties(**{'text-align': 'center'})  # optional: center the text

    display(styled_df)

# Main execution

def main():
    sbox_generator = DynamicAESSBoxGA()
    best_sbox = sbox_generator.apply_ga()
    sbox_generator.export_sbox(best_sbox)
    display_sbox_hex_table(best_sbox)
