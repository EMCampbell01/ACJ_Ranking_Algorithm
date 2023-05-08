from comparative_ranker.comparison import Comparison

class ComparisonRanker():
    
    def __init__(self) -> None:
        
        self.comparison_objects = set()
        self.comparisons = {}
        
    def add_comparison(self, comparison):
        
        comparison_key = (comparison.lower, comparison.higher)
        
        # If comparison does not exist, add it
        if comparison_key not in self.comparisons:
            self.comparisons[comparison_key] = comparison
        
        # If comparison already exists, update rating if new rating is higher
        elif comparison.rating > self.comparisons[comparison_key].rating:
            self.comparisons[comparison_key].rating = comparison.rating
        
        # If comparison already exists and new rating is lower, do nothing
        else:
            return
        
        branch_up = [comparison_up for comparison_up in self.comparisons.values() if comparison_up.lower == comparison.higher]
        branch_down = [comparison_down for comparison_down in self.comparisons.values() if comparison_down.higher == comparison.lower]
        
        links_up = []
        for comparison_up in branch_up:

            if (comparison.lower, comparison_up.higher) in self.comparisons.keys():
                if comparison.rating * comparison_up.rating > self.comparisons[(comparison.lower, comparison_up.higher)].rating:
                    self.comparisons[(comparison.lower, comparison_up.higher)].rating = comparison.rating * comparison_up.rating
            else:
                links_up.append(Comparison(comparison.lower, comparison_up.higher, comparison.rating * comparison_up.rating))
                
        links_down = []
        for comparison_down in branch_down:
            
            if (comparison_down.lower, comparison.higher) in self.comparisons.keys():
                if comparison_down.rating * comparison.rating > self.comparisons[(comparison_down.lower, comparison.higher)].rating:
                    self.comparisons[(comparison_down.lower, comparison.higher)].rating = comparison_down.rating * comparison.rating
            else:
                links_down.append(Comparison(comparison_down.lower, comparison.higher, comparison.rating * comparison_down.rating))
        
        all_links = links_down + links_up
        for link_high in links_up:
            for link_low in links_down:
                
                if link_high.higher == link_low.lower:
                    continue
                
                else:
                    if (link_low.lower, link_high.higher) in self.comparisons.keys():
                        if link_low.rating * link_high.rating > self.comparisons[(link_low.lower, link_high.higher)].rating:
                            self.comparisons[(link_low.lower, link_high.higher)].rating = link_low.rating * link_high.rating
                    else:
                        all_links.append(Comparison(link_low.lower, link_high.higher, link_low.rating * link_high.rating))
        
        for link in all_links:
            self.comparisons[(link.lower, link.higher)] = link
        
        # Conflict Resoluton, remove all comparisons where a higher rated conflicting comparison exists
        minor_comparisons = set()
        for comparison in self.comparisons.values():
            if (comparison.higher, comparison.lower) in self.comparisons.keys():
                if self.comparisons[(comparison.higher, comparison.lower)].rating > comparison.rating:
                    self.comparisons[(comparison.higher, comparison.lower)].rating -= comparison.rating
                    minor_comparisons.add((comparison.lower, comparison.higher))
                    
        for comparison in minor_comparisons:
            del self.comparisons[comparison]
    
    def get_comparison(self, object_1, object_2):
        
        if (object_1, object_2) in self.comparisons.keys():
            return self.comparisons[(object_1, object_2)]
        elif (object_2, object_1) in self.comparisons.keys():
            return self.comparisons[(object_2, object_1)]
        else:
            return None
        
    def get_higher_rated_comparison(self, object_1, object_2):
        
        if object_1.rating > object_2.rating:
            return object_1, object_2
        else:
            return object_2, object_1
    
    def get_next_best_comparisons(self, number_of_comparisons):
        
        next_comparisons = []
        
        for object_1 in self.comparison_objects:
            for object_2 in self.comparison_objects:
                
                if object_1 == object_2:
                    continue
                
                if (object_1, object_2) not in self.comparisons.keys() and (object_2, object_1) not in self.comparisons.keys():
                    next_comparisons.append(((object_1, object_2), 0))
                    
                else:
                    comparison = self.get_comparison(object_1, object_2)
                    next_comparisons.append(((object_1, object_2), comparison.rating))
        
        next_comparisons.sort(key=lambda x: x[1])
        
        return next_comparisons[:number_of_comparisons]
    
    def get_ranking(self):
                
        comparison_objects_ranking = {element: {'higher': [], 'lower': []} for pair in self.comparisons.keys() for element in pair}

        for comparison in self.comparisons.values():
            comparison_objects_ranking[comparison.lower]['higher'].append([comparison.higher, comparison.rating])
            comparison_objects_ranking[comparison.higher]['lower'].append([comparison.lower, comparison.rating])
            
        return comparison_objects_ranking
            
    def show_comparisons(self):
        print('\n')
        for comparison in self.comparisons.values():
            print(f"[low={comparison.lower}, high={comparison.higher}] rating={comparison.rating}")
