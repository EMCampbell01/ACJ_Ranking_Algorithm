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

    result = ranker.get_ranking()

    json_result = json.dumps(result)
    print(json_result)

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
