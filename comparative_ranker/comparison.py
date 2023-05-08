class Comparison():
    
    creation_index = 0
    
    def __init__(self, lower, higher, rating=1, link=True) -> None:
        
        self.lower = lower
        self.higher = higher
        self.rating = rating
        self.link = link
        self.n = Comparison.creation_index
        Comparison.creation_index += 1