import marimo

__generated_with = "0.11.6"
app = marimo.App(width="full")


@app.cell
def _():
    import graph_widget
    import marimo as mo
    return graph_widget, mo


@app.cell
def _():
    data = {'nodes':
            [{"id": 1, "kind": "sample", "value": -15},
            {"id": 2, "kind": "sample", "value": 0},
            {"id": 3, "kind": "OTU", "degree": 3, "value": 23},
            {"id": 4, "kind": "OTU", "degree": 2, "value": 1},
            {"id": 5, "kind": "OTU", "degree": 3, "value": 17}],
            "links": [
                {"source": 1, "target": 3},
                {"source": 1, "target": 4},
                {"source": 1, "target": 5},
                {"source": 2, "target": 3},
                {"source": 1, "target": 4},
                {"source": 1, "target": 5},
                {"source": 2, "target": 3},
                {"source": 2, "target": 5},
            ]}
    return (data,)


@app.cell
def _(data, mo):
    repulsion_slider = mo.ui.slider(
        start=-100, stop=500, step=10, value=1, debounce=False, label="Repulsion"
    )
    node_scale_slider = mo.ui.slider(
        start=1, stop=20, step=1, value=3, debounce=True, label="Node scale"
    )
    colour_feature_dropdown = mo.ui.dropdown(
        options=list(data["nodes"][3].keys()), value="kind", label="Colour by"
    )
    colour_scale_type_radio = mo.ui.radio(options=["diverging", "sequential"], value="diverging", label="Colour scale type")
    return (
        colour_feature_dropdown,
        colour_scale_type_radio,
        node_scale_slider,
        repulsion_slider,
    )


@app.cell
def _(data, graph_widget, mo):
    data_graph = mo.ui.anywidget(
        graph_widget.ForceGraphWidget(
            data=data,
            repulsion=2,
            node_scale=2,
            colour_feature="",
            colour_scale_type=""
        )
    )
    return (data_graph,)


@app.cell
def _(
    colour_feature_dropdown,
    colour_scale_type_radio,
    data_graph,
    node_scale_slider,
    repulsion_slider,
):
    data_graph.repulsion = repulsion_slider.value
    data_graph.node_scale = node_scale_slider.value
    data_graph.colour_feature = colour_feature_dropdown.value
    data_graph.colour_scale_type= colour_scale_type_radio.value
    return


@app.cell
def _(
    colour_feature_dropdown,
    colour_scale_type_radio,
    data_graph,
    mo,
    node_scale_slider,
    repulsion_slider,
):
    plot = mo.hstack([data_graph,
                mo.vstack([
                    repulsion_slider,
                    node_scale_slider,
                    colour_feature_dropdown,
                    colour_scale_type_radio])], justify="start")
    return (plot,)


@app.cell
def _(plot):
    plot
    return


@app.cell
def _(data_graph):
    selected = data_graph.selected_ids
    return (selected,)


@app.cell
def _(selected):
    selected
    return


@app.cell
def _(data, selected):
    filtered_nodes = [node for node in data["nodes"] if node["id"] in selected]
    filtered_nodes
    return (filtered_nodes,)


@app.cell
def _(data):
    type(data)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
