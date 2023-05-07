# Comparative Ranker

This repository contains a Python implementation of an algorithm designed to rank objects using (lower, higher) comparisons.
The algorithm aims to rank all objects relative to one another as accurately as possible, with the minimum number of comparisons required.
The result produced can be used to create a box-plot graph representing the relative ranking of compared objects.

## Description

### Modules:

- **main.py:**
- **comparison_ranker.py:**
- **comparison.py:**
- **visualisations.py**
- **comparison_ranker_test.py**

### main.py

the main.py script, given comparisons as JSON data, will produce a ranking result as JSON data.
the JSON input should be structured as:

UPDATE THIS!

### comparison_ranker.py

the comparison ranker object holds all comparisons in a dict. -> (lower, higher) : comparison

**Adding Comparisons**

comparisons can be added using the 'add_comparison' method.
when a comparison is added using 'add_comparison' the input comparison, along side any additional comparison links that can be identified are added to comparisons. Additionally any conficts in comparisons are resolved and comparison ratings are updated where needed.

The following GIF shows have links are added

![myGIF](https://user-images.githubusercontent.com/75681738/230832541-e14e797b-4a16-44e4-9485-58c28c980078.gif)

The rating of identified links is equal to the product of the comparisons combined to produce the link.
This ensures that as links become further removed from input comparisons, their rating is reduced.

When adding a new comparison, linking comparisons can be identfied and created where:

- The low of the new comparison is the high of an existing comaprison (branch down)
- The high of the new comparison is the low of an existing comparison (branch up)

![ H L ](https://user-images.githubusercontent.com/75681738/236701011-06b4e054-21d3-485b-b7d2-a251547e01bf.png)

the low of comparisons in branch down and the high of comparisons in branch up are then created.

all newly created linking comparisons are then added to comparisons
(if any identfied link already is an existing comparison its rating is updated if required)

**Conflict Resolution**
When a comparison is added that comes into conflict with another (example: [low=1, high=2] [low=2, high=1]) the comparison with the highest rating is the only comparison that is added to comparisons, however the rating of the conflicting comparison is subtracted from its rating.

**Creating Ranking Result**

UPDATE THIS!

**Identifying Next Best Reviews**

UPDATE THIS!

### comparison.py

Each Comparison object represents a comparison link between two objects, consisting of:

- **lower: The lower-rated object.
- **higher:** The higher-rated object.
- **rating:** A score from 0 to 1 representing how much trust can be placed in the comparison.

### visualisations.py

the draw_graphs function in visulisations.py is used to display the creation of a student ranking from rated pairs. A snippit is shown below:

https://user-images.githubusercontent.com/75681738/231398619-986319f3-c92a-4ff9-a796-09325ddfa69f.mp4

On the 'network graph' (left) each node represents a comparison object. Each line between the nodes represents a comparison, blue lines are input comparisons, green lines are identified linking comparisons.
On the right the box plot graph shows the range in which that object's rank can be estimated, given enough reviews, this range for each student can be reduced to its accurate placement.

## Dependencies

Python 3.6 or higher

No external dependencies are required.
