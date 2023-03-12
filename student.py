from task import Task

class Student():
    
    def __init__(self, id, review, rating):
        self.student_id = id
        self.review = review
        self.rating = rating
        self.task = Task()