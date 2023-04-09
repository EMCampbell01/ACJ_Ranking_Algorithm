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

STUDENT_COUNT = 20
ERROR_PROBABILITY = 0.1

class RankerTest():
    
    def __init__(self, student_total: int, error_probabiliy) -> None:
        
        self.ranker = Ranker()
        self.student_total = student_total
        self.error_probability = error_probabiliy
        
    def test(self):
        
        while True:
            self.add_random_pairs(10)
            self.display_ranking()
        
    def add_random_pairs(self, num):
        
        for _ in range(num):
            
            # Pick 2 unique random students
            student1, student2 = random.sample(range(1, self.student_total + 1), 2)
            print(f'{student1}, {student2}')
            
            
            # If random number within error probabilty, add inverted pair, otherwise add correct pair
            if random.random() > self.error_probability:
               new_pair = RatedPair(min(student1, student2), max(student1, student2), random.uniform(0.5, 1))
            else:
                new_pair = RatedPair(max(student1, student2), min(student1, student2), random.uniform(0.5, 1))
                new_pair.lower, new_pair.higher = new_pair.higher, new_pair.lower
            
            self.ranker.add_new_pair(new_pair)
    
    # Draws primative box plot in output
    def display_ranking(self):
        
        ranking = self.ranker.get_ranking()
        
        print("RATED PAIRS:")
        for rated_pair in self.ranker.data:
            print(f'{rated_pair.lower}, {rated_pair.higher}')
            
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
   
if __name__ == "__main__":                       
    tester = RankerTest(STUDENT_COUNT, ERROR_PROBABILITY)
    tester.test()      
