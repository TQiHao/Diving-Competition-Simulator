# Full Name: Toh Qi Hao
# Tutorial Group: T04
# Declaration: It is my own work and i have not passed to my friends

import random

class DiverInfo:
    def __init__(self, country, name, age):
        self.country = country
        self.name = name
        self.age = age
    
    def get_country(self):
        return self.country
    
    def get_name(self):
        return self.name
    
    def get_age(self):
        return self.age
    
    def set_country(self, country):
        self.country = country
    
    def set_name(self, name):
        self.name = name
    
    def set_age(self, age):
        self.age = age
    
    def __str__(self):
        return f"Diver Name: {self.name}, Country: {self.country}, Age: {self.age}"

class Diving:
    def __init__(self, diver, scores, difficulty, cf=0):
        self.diver = diver
        self.scores = scores
        self.difficulty = difficulty
        self.cf = round(cf, 2)  # Ensure CF is rounded to 2 decimal places
        self.fs = self.calculate_final_score()
        self.initial_difficulty = difficulty
    
    def calculate_final_score(self):
        if len(self.scores) > 4:
            trimmed_scores = sorted(self.scores)[2:-2]
        else:
            trimmed_scores = self.scores 
        execution_score = sum(trimmed_scores)
        final_score = round((execution_score * self.difficulty) + self.cf, 2)  # Ensure final score is rounded to 2 decimal places
        return final_score
    
    def add_scores(self, scores, difficulty):
        self.scores = scores
        self.difficulty = difficulty
        self.fs = self.calculate_final_score()
    
    def update_carried_forward(self, cf):
        self.cf = round(cf, 2)  # Ensure CF is rounded to 2 decimal places
        self.fs = self.calculate_final_score()
    
    def display_info(self):
        print(f"{self.diver}, Scores: {self.scores}, Difficulty: {self.difficulty}, "
              f"Final Score: {self.fs}, Carried Forward: {self.cf:.2f}")
    
    def display_result(self):
        print(f"{self.diver.get_name()}: Final Score: {self.fs:.2f}")
    
    def get_final_score(self):
        return self.fs

    def get_initial_difficulty(self):
        return self.initial_difficulty

def generate_random_scores(num_scores=7):
    return [round(random.choice([x * 0.5 for x in range(21)]), 1) for _ in range(num_scores)]

def generate_random_difficulty():
    return round(random.uniform(2, 5), 1)

def generate_random_age():
    return random.randint(15, 30)

def generate_random_name(index):
    return f"Diver {index + 1}"

def display_starting_position(diving_instances):
    print("\nStarting Position\n")
    print(f"{'No':<5} {'Country':<15} {'Name':<20} {'DF':<5}")
    count = 1
    for diving in diving_instances:
        print(f"{count:<5} {diving.diver.get_country():<15} {diving.diver.get_name():<20} {diving.get_initial_difficulty():<5}")
        count += 1

def display_game_info(diving_instances):
    headers = ["Country", "Name", "Age", "DF", "J1", "J2", "J3", "J4", "J5", "J6", "J7", "C/f", "Total", "Final"]
    
    header_format = " ".join(["{:<10}" if header == "Country" else \
                              "{:<20}" if header == "Name" else \
                              "{:<3}" if header == "Age" or header == "DF" else \
                              "{:<4}" if header.startswith("J") else \
                              "{:<6}" for header in headers])
                              
    row_format = " ".join(["{:<10}" if header == "Country" else \
                           "{:<20}" if header == "Name" else \
                           "{:<3}" if header == "Age" or header == "DF" else \
                           "{:<4}" if header.startswith("J") else \
                           "{:<6}" for header in headers])
    
    print(header_format.format(*headers))
    for diving in diving_instances:
        # Ensure we always have 7 scores
        scores = diving.scores + [0] * (7 - len(diving.scores))  # Fill missing scores with 0
        trimmed_scores = sorted(scores)[2:-2] if len(scores) > 4 else scores
        row = [
            diving.diver.get_country(),
            diving.diver.get_name(),
            diving.diver.get_age(),
            diving.get_initial_difficulty(), 
            *[f"{score:.1f}" for score in scores],  # Format scores to 1 decimal place
            f"{diving.cf:.2f}",  # Format CF to 2 decimal places
            f"{sum(trimmed_scores):.2f}",  # Format total score to 2 decimal places
            f"{diving.get_final_score():.2f}"  # Format final score to 2 decimal places
        ]
        # Ensure the row has exactly the same number of items as headers
        row.extend([''] * (len(headers) - len(row)))  # Add empty strings if row has less than the headers
        print(row_format.format(*row))

def display_ranking(diving_instances, round_num):
    def sort_by_final_score(diving):
        return diving.get_final_score()
    
    ranked_divers = sorted(diving_instances, key=sort_by_final_score, reverse=True)
    print(f"\nRank after round {round_num}\n")
    print(f"{'Rank':<5} {'Country':<10} {'Name':<20} {'Score':<6}")
    rank = 1
    for diver in ranked_divers:
        print(f"{rank:<5} {diver.diver.get_country():<10} {diver.diver.get_name():<20} {diver.get_final_score():<6.2f}")
        rank += 1

# Example usage
countries = ["Korea", "China", "France", "China", "USA", "Spain", "Brazil", "Malaysia", "Thailand", "Japan"]
divers_info = [DiverInfo(country, generate_random_name(i), generate_random_age()) for i, country in enumerate(countries)]

diving_instances = []
for diver in divers_info:
    scores = generate_random_scores()
    difficulty = generate_random_difficulty()
    diving_instance = Diving(diver, scores, difficulty)
    diving_instances.append(diving_instance)

# Run the simulation for 5 rounds
previous_final_scores = [0] * len(diving_instances)  # Set initial CF for the first round to 0

for round_num in range(1, 6):
    print(f"\nRound {round_num}")
    display_starting_position(diving_instances)
    
    i = 0
    while i < len(diving_instances):
        diving = diving_instances[i]
        scores = generate_random_scores()
        difficulty = generate_random_difficulty()
        diving.add_scores(scores, difficulty)
        diving.update_carried_forward(previous_final_scores[i])  # Set CF to previous round's final score
        i += 1
    
    # Save the final scores for the next round's CF
    previous_final_scores = [diving.get_final_score() for diving in diving_instances]
    
    # Add a newline before displaying the game info
    print()
    display_game_info(diving_instances)
    display_ranking(diving_instances, round_num)

input("\nPress Enter to terminate")
