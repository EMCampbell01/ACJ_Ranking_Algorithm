from comparative_ranker.comparison_ranker import ComparisonRanker, Comparison
from comparative_ranker.visualisations import draw_graph, print_ranking
import random

COMPARISON_OBJECTS_COUNT = 40
INPUT_COMPARISONS_COUNT = 400
ERROR_PROBABILITY = 0.05

ranker = ComparisonRanker()
ranker.comparison_objects = [i for i in range(COMPARISON_OBJECTS_COUNT)]

added_comparisons = 0
while added_comparisons < INPUT_COMPARISONS_COUNT:
    
    ranker.get_next_best_comparisons(1)
    
    random_number_1 = random.randint(0, COMPARISON_OBJECTS_COUNT - 1)
    random_number_2 = random.randint(0, COMPARISON_OBJECTS_COUNT - 1)
    
    if random_number_1 == random_number_2:
        continue
    
    else:
        if 10 > abs(random_number_1 - random_number_2)  and random.random() < ERROR_PROBABILITY:
            ranker.add_comparison(Comparison(max(random_number_1, random_number_2), min(random_number_1, random_number_2), random.uniform(0.5, 1), link=False))
        else:
            ranker.add_comparison(Comparison(min(random_number_1, random_number_2), max(random_number_1, random_number_2), random.uniform(0.5, 1), link=False))
        
        added_comparisons += 1
        print_ranking(ranker.get_ranking())
        
draw_graph(ranker)