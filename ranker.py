from rated_pair import RatedPair
import statistics     
   
class Ranker():
    
    def __init__(self) -> None:
        
        self.data = [] # holds all rated pairs
    
    # Given (lower, higher) returns the associated RatedPair in data, Returns None if it does not exist
    def get_pair(self, lower, higher):
        
        pair_list = [ x for x in self.data if x.lower == lower and x.higher == higher ]
        
        if not pair_list:
            return None
        else:
            return pair_list[0]
    
    # Adds new pair to data
    def add_new_pair(self, new_pair: RatedPair):
        
        new_pair.square_rating()
        
        # First add/update new pair
        pre_existing_pair = self.get_pair(new_pair.lower, new_pair.higher)
        if pre_existing_pair:
            if new_pair.rating > pre_existing_pair.rating:
                pre_existing_pair.rating = new_pair.rating
        else:
            self.data.append(new_pair)
        
        # Add new identifiable linking pairs
        while True:
            updated_data = False
            
            for rated_pair_1 in self.data:
                for rated_pair_2 in self.data:
                    
                    if rated_pair_1.lower == rated_pair_2.higher:
                        pre_existing_pair = self.get_pair(rated_pair_2.lower, rated_pair_1.higher)
                        new_rating = (rated_pair_1.rating * rated_pair_2.rating)
                        
                        if pre_existing_pair:
                            
                            if new_rating > pre_existing_pair.rating:
                                pre_existing_pair.rating = new_rating
                                
                        else:
                            self.data.append(RatedPair(rated_pair_2.lower, rated_pair_1.higher, new_rating))
                            updated_data = True
                            
            if updated_data == False:
                break
    
    # Used to generate final resuts. Returns a a dict of students which each have a high/low (for box plot graph)      
    def get_ranking(self):

        results = {}
        
        for rated_pair in self.data:
            
            opposite_pair = self.get_pair(rated_pair.higher, rated_pair.lower)
            if opposite_pair:
                if opposite_pair.rating > rated_pair.rating:
                    continue
                    
            results[rated_pair.lower] = None
            results[rated_pair.higher] = None
            
        for student in results.keys():
            
            lower_count = 0
            higher_count = 0
            
            for rated_pair in self.data:
                
                if rated_pair.higher == student:
                    lower_count += 1
                elif rated_pair.lower == student:
                    higher_count += 1
                    
            results[student] = {"low": lower_count, "high": len(results) - higher_count}
            
        return results
    
    def get_next_best_reviews(self):
        
        sorted_rated_pairs = sorted(self.data, key=lambda rp: rp.rating)
        
        next_best_reviews = []
        
        for rated_pair in sorted_rated_pairs:
            next_best_reviews.append((rated_pair.lower, rated_pair.higher))
        
        all_students = set()
        for rated_pair in self.data:
            all_students.add(rated_pair.lower)
            all_students.add(rated_pair.higher)
            
        for student1 in all_students:
            for student2 in all_students:
                if student1 == student2:
                    continue
                if not self.get_pair(student1, student2) and not self.get_pair(student2, student1):
                    next_best_reviews.insert(0, (student1, student2))
                    
        return next_best_reviews  
    
    # TODO - Not currently in use
    def get_higher_lower(self, assignment1, assignment2):
        
        probability = None
        
        # len = 0, Neither assignments in self.data => return probability 50/50
        if len(self.data) == 0: 
            probability = 0.5
        
        # If single element in self.data AND assignemt1 and assignemt2 in self.data => return average of probability.
        elif len(self.data) == 1:
            if assignment1 == self.data[0].lower and assignment2 == self.data[0].higher:
                probability = statistics.mean(self.data[0].rating)
            elif assignment2 == self.data[0].lower and assignment1 == self.data[0].higher:
                probability = 1 - (statistics.mean(self.data[0].rating))
        
        # Identify pair with assignment 1 & 2, return probability, If no such pair return 50/50
        else:
            for rated_pair in self.data:
                if rated_pair.lower == assignment1 and rated_pair.higher == assignment2:
                    probability = rated_pair.rating
                elif rated_pair.lower == assignment2 and rated_pair.higher == assignment1:
                    probability = 0 - rated_pair.rating
            if probability == None:
                probability = 0.5
                    
        return ((assignment1, assignment2), probability)
