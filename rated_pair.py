class RatedPair():
    
    index = 0
    
    def __init__(self, lower: int, higher: int, rating):
        
        self.lower = lower
        self.higher = higher
        self.rating = rating
        self.reviewed = False
        self.number = self.index
        self.index += 1
        
        
    def square_rating(self):
        
        self.rating = self.rating ** 2
