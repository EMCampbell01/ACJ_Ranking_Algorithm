# Student Performance Ranker

This repository contains a Python implementation of an algorithm designed to estimate student performance rankings based on peer review data. The algorithm processes "rated pairs" representing peer reviews and generates a resulting data structure that can be used to create a box plot graph.

## Description
The main components of the code are:

main.py: The main script that takes JSON data as input and processes it to generate a ranking of student performance.
ranker.py: Contains the Ranker class, which implements the ranking algorithm using rated pairs.
ranker_test.py: A script to test the Ranker class by continuously adding random rated pairs and displaying the resulting ranking.
rated_pair.py: Defines the RatedPair class, which represents a peer review with a high, low, and rating.

### Rated Pair
Each "rated pair" represents a peer review, consisting of:

lower: The lower-performing student.
higher: The higher-performing student.
rating: A score from 0 to 1 representing how much trust can be placed in the review.

![myGIF](https://user-images.githubusercontent.com/75681738/230832541-e14e797b-4a16-44e4-9485-58c28c980078.gif)

## Usage

### main.py

Run main.py with the JSON data as a command-line argument:

python main.py '{"json_data": [{"lower": 1, "higher": 2, "rating": 0.8}, {"lower": 2, "higher": 3, "rating": 0.6}]}'

### ranker_test.py

Run ranker_test.py to test the Ranker class:

python ranker_test.py

## Dependencies

Python 3.6 or higher
No external dependencies are required.
