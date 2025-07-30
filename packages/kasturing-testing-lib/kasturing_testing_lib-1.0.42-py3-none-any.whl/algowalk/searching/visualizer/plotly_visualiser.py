import plotly.graph_objects as go
from algowalk.searching.search_algo_visualizer import StepVisualizer


class PlotlyStepVisualizer(StepVisualizer):

    def visualize(self, steps):
        total = len(steps)

        fig = go.Figure(
            layout=go.Layout(
                title="🔍 Searching Algorithm - Stepwise Visualization",
                xaxis=dict(title="Index", range=[-1, total]),
                yaxis=dict(title="Value", range=[0, max(step['value'] for step in steps) + 5]),
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        buttons=[
                            dict(
                                label="▶ Play",
                                method="animate",
                                args=[None, {
                                    "frame": {"duration": 1000, "redraw": True},
                                    "fromcurrent": True,
                                    "transition": {"duration": 1000, "easing": "linear"}
                                }]
                            ),
                            dict(
                                label="⏸ Pause",
                                method="animate",
                                args=[[None], {
                                    "mode": "immediate",
                                    "frame": {"duration": 0, "redraw": False},
                                    "transition": {"duration": 0}
                                }]
                            )
                        ]
                    )
                ]
            )
        )

        # Initial view
        initial_colors = ['blue'] + ['gray'] * (total - 1)
        fig.add_trace(go.Bar(
            x=[step['index'] for step in steps],
            y=[step['value'] for step in steps],
            marker_color=initial_colors,
            text=[f"Match: {step['match']}" for step in steps],
            hoverinfo="x+y+text"
        ))

        # Animation frames
        frames = []
        for i in range(total):
            colors = []
            for j in range(total):
                if j < i:
                    colors.append("red" if not steps[j]['match'] else "green")
                elif j == i:
                    colors.append("green" if steps[j]['match'] else "blue")
                else:
                    colors.append("gray")
            frames.append(go.Frame(
                data=[go.Bar(
                    x=[step['index'] for step in steps],
                    y=[step['value'] for step in steps],
                    marker_color=colors,
                    text=[f"Match: {step['match']}" for step in steps]
                )],
                name=f"frame{i}"
            ))
        fig.frames = frames
        fig.show()
