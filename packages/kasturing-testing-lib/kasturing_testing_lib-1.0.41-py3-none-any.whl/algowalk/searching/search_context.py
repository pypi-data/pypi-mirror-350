from algowalk.searching.tracker.search_algo_tracker import StepTracker

class SearchContext:
    def __init__(self, strategy, visualizer=None):
        self.strategy = strategy
        self.visualizer = visualizer

    def execute_search(self, data, target):

        tracker = StepTracker(visualizer=self.visualizer)
        result_index = self.strategy.search(data, target, tracker)
        tracker.print_steps()
        tracker.print_summary()
        tracker.visualize()

        if result_index != -1:
            print(f"\n✅ Target {target} found at index {result_index}\n")
        else:
            print(f"\n❌ Target {target} not found in the list\n")
        return result_index