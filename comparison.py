import statistics

class Comparison():
    
    def __init__(self, lower, higher, rating) -> None:
        
        self.data = [RatedPair(lower, higher, [rating])] 
        self.reach = Reach().add_to_dict(lower, (higher, rating)) # ?
            
    def add_comparison(self, new_rated_pair):
        
        for existing_rated_pair in self.data:
            if new_rated_pair.lower == existing_rated_pair.lower and new_rated_pair.higher == existing_rated_pair.higher:
                existing_rated_pair.rating.append(new_rated_pair.rating)
                return
        
        self.data.append(new_rated_pair)
        
    def get_higher_lower(self, assignment1, assignment2):
        
        probability = None
        
        # len = 0, Neither assignments in self.data => return probability 50/50
        if len(self.data) == 0: 
            probability = 0.5
        
        # If single element in self.data AND assignemt1 and assignemt2 in self.data => return average of probability.
        if len(self.data) == 1:
            if assignment1 == self.data[0].lower and assignment2 == self.data[0].higher:
                probability = statistics.mean(self.data[0].rating)
            elif assignment2 == self.data[0].lower and assignment1 == self.data[0].higher:
                probability = 1 - (statistics.mean(self.data[0].rating))
                
        else:
            a1_reach = Reach(assignment1, assignment2, self.data)
            a2_reach = Reach(assignment2, assignment1, self.data)
                
                   
        return ((assignment1, assignment2), probability)
        
class Reach():
    
    def __init__(self, src, dest, data):
        
        self.src = src
        self.dest = dest
        self.connections_up = {} 
        self.connections_down = {}
        self.get_connections(data)
        
    def get_connections(self, data):
        
        for rated_pair in data:
            if rated_pair.lower == self.src:
                self.add_to_dict(self.connections_up, rated_pair.higher, rated_pair.rating, data)
            elif rated_pair.higher == self.src:
                self.add_to_dict(self.connections_down, rated_pair.lower, rated_pair.rating, data)
    
    def add_to_dict(self, dict, src, rating, data):
        
        if src in dict:
            dict[src][1].append(rating)
        else:
            dict[src] = [Reach(src, self.dest, data), [rating]]
            
    def get_paths(self):
        
        for src, data in self.connections_up.items():
            
            if src == self.dest:
                # Path Dest Found
                pass
            else:
                # Extend Path
                pass
            
        for src, data in self.connections_down.items():
            
            if src == self.dest:
                # Path Dest Found
                pass
            else:
                # Extend Path
                pass
        
class RatedPair():
    
    def __init__(self, lower, higher, rating):
        
        self.lower = lower
        self.higher = higher
        self.rating = rating
        
