import statistics

class Comparison():
    
    def __init__(self, lower, higher, rating) -> None:
        
        self.data = [((lower, higher), [rating])]
        self.reach = Reach().add_to_dict(lower, (higher, rating))
            
    def add_comparison(self, comparison):
        
        for element in self.data:
            if comparison[0] == element[0]:
                element[1].appennd(comparison[1])
                return
        
        self.data.append(comparison)
        
    def get_higher_lower(self, assignment1, assignment2):
        
        probability = None
        if not self.data: 
            probability = 0.5
        if len(self.data) == 1:
            if assignment1 == self.data[0][0][0] and assignment2 == self.data[0][0][1]:
                probability = statistics.mean(self.data[0][1])
            elif assignment2 == self.data[0][0][0] and assignment1 == self.data[0][0][1]:
                probability = 1 - (statistics.mean(self.data[0][1]))
        else:
            a1_lower = [el for el in self.data if assignment1 == el[0][0]]
            a2_lower = [el for el in self.data if assignment2 == el[0][0]]
            
            # Add rating
            a1_reach = Reach().add_to_dict([el[1] for el in a1_lower])
            
            
            
        
        return ((assignment1, assignment2), probability)
        
    def tail(self):
        
        data = self.data
        
        
class Reach():
    
    def __init__(self) -> None:
        self.dict = {}
        
    def add_to_dict(self, src, dests):
        
        self.dict.setdefault(src, []).append(dests)
