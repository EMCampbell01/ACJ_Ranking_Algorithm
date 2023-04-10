from ranker import Ranker
from rated_pair import RatedPair
import argparse
import json
import sys

def main(json_data):
    
    rated_pairs = []
    for item in json_data:
        try:
            lower = item['lower']
            higher = item['higher']
            rating = item['rating']
            rated_pair = RatedPair(lower, higher, rating)
            rated_pairs.append(rated_pair)
        except KeyError:
            print("Error 2: Invalid JSON data format.")
            sys.exit(1)

    ranker = Ranker()
    for rated_pair in rated_pairs:
        ranker.add_new_pair(rated_pair)

    ranking_result = ranker.get_ranking()
    next_best_reviews = ranker.get_next_best_reviews()

    json_ranking_result = json.dumps(ranking_result)
    print(json_ranking_result)
    
    json_next_best_reviews = json.dumps(next_best_reviews)
    print(json_next_best_reviews)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("json_data", type=str, help="JSON data as a string")

    args = parser.parse_args()

    try:
        parsed_json_data = json.loads(args.json_data)
        main(parsed_json_data)
    except json.JSONDecodeError:
        print("Error 1: Invalid JSON data.")
        sys.exit(1)
