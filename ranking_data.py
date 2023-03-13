class RankingData():
    
    def __init__(self):
        self.comparisons = []
        self.comparison_scores = {}
        self.cumulative_ranking = [[],[]]
        self.extended_cumulative_ranking = [[],[]]
        self.high_low = None
