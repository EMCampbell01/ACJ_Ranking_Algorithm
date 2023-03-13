ACJ ALGORITHM
Euan Campbell - 13/03/2023

1) DESCRIPTION

WORK IN PROGRESS
The ACJ algorithm accepts a list of students, which it then aims to rank students as accuratley as possible based upon peer reviews.

2) STUDENTS

Each student has a unique id (int)

Each student has a list of reviews. Each review in reviews is an ordered list which represents a ranking of other students, made by that student.

Example: 
student with the id 1 'reviews' == [[2,3],[4,5,6]]
This represents that student 1 has preformed 2 peer reviews. 
The first is a peer review of students 2 and 3. student 3 was ranked higher than student 2.
The second is a peer review of students 4, 5, and 6. student 5 was ranked higher than 4, and 6 higher than 5.

Each student has a rating. This is a number from 0 to 1 that represents how reliable a students review is. 1 = 100% reliable, 0 = 0% relliable.

Each Student has a RankingData object, this is used to store ACJ workings and resulting values.

3) RANKING DATA

The RankingData object is used to store ranking related data.

comparisons - for a student, stores all reviews that the student is present in.
comparison_scores - For each other student compared against the student, a score is calculated. Negative = lower ranked, positive = higher ranked
cumulative_ranking - Two lists, index [0] contains all lower (negative comparison score) ranked students, index [1] contains all higher (positive comparison score) ranked students 
extended_cumulative_ranking - similar to cumulative ranking, but holds all lower ranked students of lower ranked students, and higher ranked students of higher ranked students
high_low - holds the high and low for producing a box plot result
