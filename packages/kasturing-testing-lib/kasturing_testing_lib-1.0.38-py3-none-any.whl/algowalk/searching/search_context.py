from algowalk.searching.tracker.search_algo_tracker import StepTracker
from algowalk.searching.search_strategy import SearchStrategy


class SearchContext:
    def __init__(self, strategy: SearchStrategy):
        self.strategy = strategy

    def execute_search(self, data, target):
        tracker = StepTracker()
        result_index = self.strategy.search(data, target, tracker)
        tracker.print_steps()
        tracker.print_summary()

        if result_index != -1:
            print(f"\n✅ Target {target} found at index {result_index}\n")
        else:
            print(f"\n❌ Target {target} not found in the list\n")
        return result_index
