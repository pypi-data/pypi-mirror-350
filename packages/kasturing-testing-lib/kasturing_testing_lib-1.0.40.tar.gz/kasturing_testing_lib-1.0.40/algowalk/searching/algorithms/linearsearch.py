from algowalk.searching.search_strategy import SearchStrategy
from algowalk.searching.tracker.search_algo_tracker import StepTracker


class LinearSearchStrategy(SearchStrategy):
    def search(self, data, target, tracker: StepTracker):
        tracker.start(data)
        for index, value in enumerate(data):
            match = (value == target)
            tracker.log(index, value, target, match)
            if match:
                tracker.end()
                return index
        tracker.end()
        return -1