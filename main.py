import random
import sys
from student import Student
from task import Task
from sample_data import generate_sample_dataset
from sample_data import generate_sample_review
from graph import create_graph


'''
PRINT OUTPUT FUNCTIONS
used to display debug/results in terminal 
'''
def printStudents(students):
    
    for student in students:
        print("-----------------------------------------------------------------------")
        print(f'Student:{student.student_id}')
        print(f'reviews = {student.review}')
        print(f'comparisions = {student.task.comparisons}')
        print(f'comparison scores = {student.task.comparison_scores}')
        print(f'cumulative ranking = {student.task.cumulative_ranking}')
        print(f'Extended ranking = {student.task.extended_cumulative_ranking}')
        
def printPlottingResult(plotting_result):
    
    print("-----------------------------------------------------------------------")
    print("<= Lower Ranking - Higher Ranking =>")
    
    student_id = 0
    for row in plotting_result:
        row = ''.join(row)
        if student_id < 10:
            print(f'Student  {student_id} : {row}')
        else:
            print(f'Student {student_id} : {row}')
        student_id += 1
        

'''
ACJ RANKING FUNCTION
'''
def acj(students, debug=False, graph=False):
    
    studentDict = {student.student_id: student for student in students}
    
    ranking_result = []
    groupings_result = []
    plotting_result = []

    set_comparisons(students, studentDict)
    set_comparison_scores(students)
    set_cumulative_ranks(students)
    set_extended_cumulative_ranks(students, studentDict)
    
    ranking_result = None #create_ranking_result(students)
    groupings_result = None #create_grouping_result(students, ranking_result)
    plotting_result = create_plotting_result(students)
    
    if debug == True:
        printStudents(students)
        printPlottingResult(plotting_result)
    
    if graph == True:
        create_graph(students)
        
    return [ranking_result, groupings_result, plotting_result, studentDict]

'''
INTERMEDIATE ACJ FUNCTIONS
'''
# For each student in students, adds its review to the task.comparisons of each student contained within its review
def set_comparisons(students, studentDict):
    
    for student in students:
        student.task.comparisons = []
    
    for student in students:
        for review in student.review:

            for num in review:
                if num == None:
                    continue                
                studentDict[num].task.comparisons.append([student.rating, review])

# For each student review in task.comparisons, A key (student_id) is added for each other student it is compared to
# The value for each key stores a score (int) representing if it is ranked higher/lower than the student (represented by being positive/negative int)
def set_comparison_scores(students):
    
    for student in students:
        student.task.comparison_scores = {}
    
    for student in students:
        for comparison in student.task.comparisons:
            passed_self = False
            for num in comparison[1]:
                if num == student.student_id:
                    passed_self = True
                    continue
                elif num in student.task.comparison_scores:
                    if passed_self:
                        student.task.comparison_scores[num] += get_rating_score(comparison[0])
                    else:
                        student.task.comparison_scores[num] -= get_rating_score(comparison[0])
                else:
                    if passed_self:
                        student.task.comparison_scores[num] = get_rating_score(comparison[0])
                    else:
                        student.task.comparison_scores[num] = -get_rating_score(comparison[0])
                        
# populates task.cumulative_ranking for each score
# a students cumulative_ranking is an list. index 0 holds list of student id's ranked lowers. index 1 holds list of student id's ranked higher                     
def set_cumulative_ranks(students):
    
    for student in students:
        student.task.cumulative_ranking[0] = []
        student.task.cumulative_ranking[1] = []
    
    for student in students:
        for comparison in student.task.comparison_scores.keys():
            if student.task.comparison_scores[comparison] < 0:
                student.task.cumulative_ranking[0].append(comparison)
            elif student.task.comparison_scores[comparison] > 0:
                student.task.cumulative_ranking[1].append(comparison)

# TODO - Keep/Discard? - Not currently used
def create_ranking_result(students):    
       
    ranking_result = []
    while len(ranking_result) != len(students):
        
        for student in students:
            
            if student.student_id in ranking_result:
                continue
            
            new_highest = True
            for studentID in student.task.extended_cumulative_ranking[1]:
                    if studentID not in ranking_result:
                        new_highest = False
                        break
                    
            if new_highest:    
                ranking_result.append(student.student_id) 
                
    return ranking_result

# TODO Keep/Discard? - Not currently used
def create_grouping_result(students, ranking_result):
    
    grouping_result = []
    current_grouping = []
    
    i = 0
    for num in ranking_result:
        if i+1 == len(ranking_result):
            current_grouping.append(num)
            grouping_result.append(current_grouping)
            break
        if check_for_comparison(num, ranking_result[i+1], students):
            current_grouping.append(num)
        else:
            current_grouping.append(num)
            grouping_result.append(current_grouping)
            current_grouping = []
        i +=1
        
    return grouping_result

# Populates student.task.extended_cumulative_ranking for each student
# Extended cumulative rank is similar to cumulative rank, however incorporates the cumulative ranks of students in a students cumulative rank
def set_extended_cumulative_ranks(students, studentDict):
    
    
    
    for student in students:
        
        student.task.extended_cumulative_ranking[0] = [] + student.task.cumulative_ranking[0]
        student.task.extended_cumulative_ranking[1] = [] + student.task.cumulative_ranking[1]
        
        extended_ids = set()
        while True:
            new_id = False
            for num in student.task.cumulative_ranking[0]:
                if num not in extended_ids:
                    extended_ids.add(num)
                    student.task.extended_cumulative_ranking[0].extend(studentDict[num].task.cumulative_ranking[0])
                    new_id = True
            if not new_id:
                break
                
        extended_ids.clear()
        while True:
            new_id = False
            for num in student.task.cumulative_ranking[1]:
                if num not in extended_ids:
                    extended_ids.add(num)
                    student.task.extended_cumulative_ranking[1].extend(studentDict[num].task.cumulative_ranking[1])
                    new_id = True
            if not new_id:
                break
            
        student.task.extended_cumulative_ranking[0] = list(set(student.task.extended_cumulative_ranking[0]))
        student.task.extended_cumulative_ranking[1] = list(set(student.task.extended_cumulative_ranking[1]))
        
    return studentDict

# TODO - Add comment
def create_plotting_result(students, real_ranking=None):
    plotting_result = []
    i = 0
    for student in students:
        plotting_result.append(["-" for _ in range(len(students))])
        
        start = len(student.task.extended_cumulative_ranking[0])
        stop =  len(students) - len(student.task.extended_cumulative_ranking[1])

        student.task.high_low = [stop,start]

        j = 0 + start
        while j < stop:
             plotting_result[i][j] = "#"
             j += 1
        
        i += 1
        
    for row in plotting_result:
        if row.count('#') == 1:
            index = row.index('#')
            for row2 in plotting_result:
                if row == row2:
                    continue
                else:
                    row2[index] = '-'
          
    if real_ranking != None:
        for num in real_ranking:
            plotting_result[num].insert(len(real_ranking)-(real_ranking.index(num)), "<") 
        
    return plotting_result

# Returns boolean for is student1 and student2 have been compared against each other in any review
def check_for_comparison(studentId1, studentId2, students):
    
    existing_comparison = False
    for student in students:
        
        if studentId1 in student.review and studentId2 in student.review:
            existing_comparison = True
            return existing_comparison
        
    return existing_comparison

# TODO - Add comment 
def get_rating_score(student_rating):
    
    return (student_rating / 1) ** 2
    

# Identifies the next two students that should be reviewed agaisnt each other to best improve results
# Students which have the largest number of unshared students in extended cumulative ranking are considered optimal
def get_next_best_review(student_data):
    
    working_dict = {}
    
    for student1 in student_data.values():
        working_dict[student1.student_id] = {}
        
        for student2 in student_data.values():
            
            if student1.student_id in student2.task.extended_cumulative_ranking[0] or student1.student_id in student2.task.extended_cumulative_ranking[1]:
                continue
            
            if student2.student_id in student1.task.extended_cumulative_ranking[0] or student2.student_id in student1.task.extended_cumulative_ranking[1]:
                continue
            
            if student1.student_id == student2.student_id:
                working_dict[student1.student_id][student2.student_id] = 0
                continue
            
            students_in_student1_extended_cumulative_rankings = set()
            students_in_student2_extended_cumulative_rankings = set()
            
            students_in_student1_extended_cumulative_rankings.update(student_data[student1.student_id].task.extended_cumulative_ranking[0])
            students_in_student1_extended_cumulative_rankings.update(student_data[student1.student_id].task.extended_cumulative_ranking[1])
            
            students_in_student2_extended_cumulative_rankings.update(student_data[student2.student_id].task.extended_cumulative_ranking[0])
            students_in_student2_extended_cumulative_rankings.update(student_data[student2.student_id].task.extended_cumulative_ranking[1])
            
            shared = students_in_student1_extended_cumulative_rankings.intersection(students_in_student2_extended_cumulative_rankings)
            total = (len(students_in_student1_extended_cumulative_rankings) - len(shared)) + (len(students_in_student2_extended_cumulative_rankings) - len(shared))
            
            working_dict[student1.student_id][student2.student_id] = total
    
    largest_total = 0
    student_1 = None
    student_2 = None
    
    for student1 in working_dict.keys():
        for student2 in working_dict[student1].keys():
                if working_dict[student1][student2] > largest_total:
                    largest_total = working_dict[student1][student2]
                    student_1 = student1
                    student_2 = student2
    
    return [student_1, student_2]

# Adds a review to the specfified reviewer
def add_additional_review (reviewer, review, student_data):
    
    student_data[reviewer].review.append(review)#
    
    return student_data
    
'''
TESTING
'''
studentCount = 25
additional_ranking_rounds = 50

pass_count = 0
fail_count = 0
total_attempts = 0

while total_attempts < 1:
    
    sample_data = generate_sample_dataset(studentCount=studentCount, error_probability=0.1)
    
    students = sample_data[0]
    real_ranking = sample_data[1]
    
    acj_results = acj(students, debug=True, graph=True)
    
    ranking_result = acj_results[0]
    grouping_result = acj_results[1]
    plotting_result = acj_results[2]
    student_data = acj_results[3]
    
    print("-----------------------------------------------------------------------")
    print(f"REAL RANKING = HIGH - {real_ranking} - LOW")
    
    added_reviews = []
    for round in range(additional_ranking_rounds):
        
        next_best_review = get_next_best_review(student_data)
        reviewer, review = generate_sample_review(next_best_review, real_ranking)
        student_data = add_additional_review(reviewer, review, student_data)
        acj_results = acj(student_data.values())
        student_data = acj_results[3]
    
    plotting_result = create_plotting_result(student_data.values(), real_ranking)
    printPlottingResult(plotting_result)
    
    total_attempts += 1
