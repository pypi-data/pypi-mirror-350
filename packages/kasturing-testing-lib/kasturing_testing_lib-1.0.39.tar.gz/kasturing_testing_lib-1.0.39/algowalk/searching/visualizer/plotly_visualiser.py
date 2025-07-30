import plotly.graph_objects as go
from algowalk.searching.search_algo_visualizer import StepVisualizer


class PlotlyStepVisualizer(StepVisualizer):
    def visualize(self, steps):
        indices = [step['index'] for step in steps]
        values = [step['value'] for step in steps]
        colors = ['green' if step['match'] else 'red' for step in steps]

        fig = go.Figure(data=[
            go.Bar(x=indices, y=values, marker_color=colors, text=[f"Match: {step['match']}" for step in steps])
        ])

        fig.update_layout(
            title="Linear Search Steps Visualization",
            xaxis_title="Index",
            yaxis_title="Value Checked",
            showlegend=False
        )
        fig.show()
