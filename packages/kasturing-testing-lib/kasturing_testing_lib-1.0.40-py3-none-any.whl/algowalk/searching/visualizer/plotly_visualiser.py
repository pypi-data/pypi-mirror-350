import plotly.graph_objects as go
import ipywidgets as widgets
from IPython.display import display, clear_output
from algowalk.searching.search_algo_visualizer import StepVisualizer
import nest_asyncio


class PlotlyStepVisualizer(StepVisualizer):
    def visualize(self, steps):
        self.steps = steps
        self.current_index = 0
        self.total_steps = len(steps)

        # Create interactive output
        self.output = widgets.Output()
        self.label = widgets.Label()
        self.build_controls()
        self.update_chart()

        display(widgets.VBox([self.plot_widget, self.label, self.controls, self.output]))

    def build_controls(self):
        self.plot_widget = go.FigureWidget()
        self.left_btn = widgets.Button(description="← Previous")
        self.right_btn = widgets.Button(description="Next →")
        self.play_btn = widgets.Button(description="▶ Play")
        self.pause_btn = widgets.Button(description="⏸ Pause")

        self.controls = widgets.HBox([self.left_btn, self.right_btn, self.play_btn, self.pause_btn])

        self.left_btn.on_click(self.on_prev)
        self.right_btn.on_click(self.on_next)
        self.play_btn.on_click(self.on_play)
        self.pause_btn.on_click(self.on_pause)

        self.is_playing = False

    def update_chart(self):
        step = self.steps[self.current_index]

        indices = list(range(len(self.steps)))
        values = [s['value'] for s in self.steps]
        colors = ['green' if i == self.current_index and s['match'] else
                  'blue' if i == self.current_index else
                  'red' for i, s in enumerate(self.steps)]

        with self.output:
            clear_output(wait=True)
            print(f"Step {self.current_index + 1} / {self.total_steps}")
            print(f"Index Checked: {step['index']}")
            print(f"Value Checked: {step['value']}")
            print(f"Target: {step['target']}")
            print(f"Match: {'Yes' if step['match'] else 'No'}")

        self.plot_widget.data = []  # Clear previous
        self.plot_widget.add_trace(go.Bar(
            x=indices,
            y=values,
            marker_color=colors,
            text=[f"Match: {s['match']}" for s in self.steps],
            hoverinfo="x+y+text"
        ))
        self.plot_widget.update_layout(
            title="Linear Search Interactive Visualization",
            xaxis_title="Index",
            yaxis_title="Value Checked",
            showlegend=False
        )

        self.label.value = f"🧠 Time: O(n)  |  Space: O(1)  |  Current Step: {self.current_index + 1}/{self.total_steps}"

    def on_prev(self, _):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_chart()

    def on_next(self, _):
        if self.current_index < self.total_steps - 1:
            self.current_index += 1
            self.update_chart()

    def on_play(self, _):
        if not self.is_playing:
            self.is_playing = True
            self.auto_play()

    def on_pause(self, _):
        self.is_playing = False

    def auto_play(self):
        import asyncio

        async def play_steps():
            while self.is_playing and self.current_index < self.total_steps - 1:
                await asyncio.sleep(0.7)
                self.current_index += 1
                self.update_chart()
            self.is_playing = False


        nest_asyncio.apply()
        asyncio.run(play_steps())