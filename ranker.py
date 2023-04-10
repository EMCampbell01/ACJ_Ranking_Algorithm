from ranker import Ranker
from rated_pair import RatedPair
import random

'''
ranker_test.py

Run this script to test the Ranker class

Parameters:
    student_total: Number of students in test
    error_probability: Number representing the % chance of error

Continously adds 10 random Rated Pairs to a Ranker object and displays the current result
Can add a error probability. 0 = % chance of error, 1 = 100% chance of error
Students 'correct ranking' is students in an ascending sequence (LOW 1, 2, 3, 4, 5 HIGH)
'''

STUDENT_COUNT = 25
ERROR_PROBABILITY = 0.1
NUM_REVIEWS = 100

class RankerTest():
    
    def __init__(self, student_total: int, error_probabiliy) -> None:
        
        self.ranker = Ranker()
        self.student_total = student_total
        self.error_probability = error_probabiliy
        self.real_ranking = list(range(STUDENT_COUNT))
        random.shuffle(self.real_ranking)
        
    def test(self, num_pairs: int):
        
        for student in range(STUDENT_COUNT):
            if student == STUDENT_COUNT - 1:
                ordered_pair = self.get_real_order(0, student)
                self.ranker.add_new_pair(RatedPair(ordered_pair[0], ordered_pair[1], random.uniform(0.5, 1)))
            else:
                ordered_pair = self.get_real_order(student, (student+1))
                self.ranker.add_new_pair(RatedPair(ordered_pair[0], ordered_pair[1], random.uniform(0.5, 1)))
        
        added_pairs = 0
        while added_pairs < num_pairs:
            next_best_reviews = self.ranker.get_next_best_reviews()
            
            if not next_best_reviews:
                self.add_random_pairs(1)
            else:
                ordered_pair = self.get_real_order(next_best_reviews[0][0], next_best_reviews[0][1])
                self.ranker.add_new_pair(RatedPair(ordered_pair[0], ordered_pair[1], random.uniform(0.5, 1)))
                
            ranking = self.ranker.get_ranking()
            
            if self.finished_ranking(ranking):
                print(f'Completed ranking after only {added_pairs} pairs')
                break
            
            added_pairs += 1
            
        self.display_ranking(ranking)    
        
    def add_random_pairs(self, num):
        
        for _ in range(num):
            
            # Pick 2 unique random students
            student1, student2 = random.sample(range(1, self.student_total + 1), 2)
            print(f'{student1}, {student2}')
            
            
            # If random number within error probabilty, add inverted pair, otherwise add correct pair
            ordered_pair = self.get_real_order(student1, student2)
            if random.random() > self.error_probability:
               new_pair = RatedPair(ordered_pair[0], ordered_pair[1], random.uniform(0.5, 1))
            else:
                new_pair = RatedPair(ordered_pair[1], ordered_pair[0], random.uniform(0.5, 1))
                new_pair.lower, new_pair.higher = new_pair.higher, new_pair.lower
            
            self.ranker.add_new_pair(new_pair)
    
    # Draws primative box plot in output
    def display_ranking(self, ranking):
            
        print("RANKING:")
        for student, result in ranking.items():
            
            row = ["Student ", str(student), ": "]
            
            for _ in range(result["low"]):
                row.append("-")
                
            for _ in range(self.student_total - result["low"] - (self.student_total - result["high"])):
                row.append("#")
                
            for _ in range(self.student_total - result["high"]):
                row.append("-")
                
            print(''.join(row))
            
    def finished_ranking(self, ranking):
        
        if len(ranking.items()) < STUDENT_COUNT:
            return False
        
        for student, result in ranking.items():
            if result["low"] + 2 != result["high"]:
                return False
        
        return True
    
    def get_real_order(self, student1, student2):
        for student in self.real_ranking:
            if student == student1:
                return (student1, student2)
            if student == student2:
                return (student2, student1)
   
if __name__ == "__main__":                       
    tester = RankerTest(STUDENT_COUNT, ERROR_PROBABILITY)
    print(f'Real ranking: {tester.real_ranking}')
    tester.test(NUM_REVIEWS)      

