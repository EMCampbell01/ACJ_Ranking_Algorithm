import random
from student import Student

# Returns custom student sample
def generate_sample_dataset(studentCount=10, error_probability=None):
      
    student_ranking = []
      
    for num in range(studentCount):
        student_ranking.append(num)
    
    random.shuffle(student_ranking)
    
    d1 = {}
    for i in range(studentCount):
        values = [(i+j+1)%studentCount for j in range(4)]
        d1[i] = values
    
    for num in student_ranking:
        for key, value in d1.items():
            if num in value:
                value.append(num)
    
    if error_probability != None:
        for review in d1.values():
            if random.uniform(0, 1) < error_probability:
                index_1 = random.randint(0, len(review)-2)
                index_2 = index_1 + 1
                review[index_1], review[index_2] = review[index_2], review[index_1]
    
    student_list = []
    
    for key, value in d1.items():
        value = value[4:]
        student_list.append(Student(key, [value], 1))

    student_ranking.reverse()
        
    return [student_list, student_ranking]

# TODO - Add comment
def generate_sample_review(review, real_ranking):
    
    while True:
        reviewer = random.choice(real_ranking)
        if reviewer not in review:
            break
    
    higher = None
    lower = None
    
    for student_id in real_ranking:
        
        if student_id == review[0]:
            higher = review[0]
            lower = review[1]
            break
        
        if student_id == review[1]:
            higher = review[1]
            lower = review[0]
            break
        
    return reviewer, [lower,higher,]
        
# Returns most simple student test sample of 10 students
def create_ten_sample_students():
    
    student1 = Student(1, [2,3,4,5], 1)
    student2 = Student(2, [3,4,5,6], 1)
    student3 = Student(3, [4,5,6,7], 1)
    student4 = Student(4, [5,6,7,8], 1)
    student5 = Student(5, [6,7,8,9], 1)
    student6 = Student(6, [7,8,9,10], 1)
    student7 = Student(7, [1,8,9,10], 1)
    student8 = Student(8, [1,2,9,10], 1)
    student9 = Student(9, [1,2,3,10], 1)
    student10 = Student(10, [1,2,3,4], 1)
    
    return [student1, student2, student3, student4, student5, student6, student7, student8, student9, student10]