class RatedPair():
    
    def __init__(self, lower: int, higher: int, rating):
        
        self.lower = lower
        self.higher = higher
        self.rating = rating
        
    def square_rating(self):
        self.rating = self.rating ** 2
