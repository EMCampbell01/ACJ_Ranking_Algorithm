from ranking_data import RankingData

class Student():
    
    def __init__(self, id, review, rating):
        self.student_id = id
        self.reviews = review
        self.rating = rating
        self.ranking_data = RankingData()
