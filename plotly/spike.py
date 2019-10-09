import dash
import dash_core_components as dcc
import dash_html_components as html
import pathlib
import pandas as pandas
import plotly.graph_objs as go
from dash.dependencies import Input, Output

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

data_dict = {
    "mnist_3000": pandas.read_csv(DATA_PATH.joinpath("mnist_3000_input.csv"))
}

IMAGE_DATASETS = "mnist_3000"


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

server = app.server


def Card(children, **kwargs):
    return html.Section(children, className="card-style")
    
def NamedSlider(name, short, min, max, step, val, marks=None):
    if marks:
        step = None
    else:
        marks = {i: i for i in range(min, max + 1, step)}
        
    return html.Div(
        style={"margin": "25px 5px 30px 0px"},
        children=[
            f"{name}:",
            html.Div(
                style={"margin-left": "5px"},
                children=[
                    dcc.Slider(
                        id=f"slider-{short}",
                        min=min,
                        max=max,
                        marks=marks,
                        step=step,
                        value=val,
                    )
                ],
            ),
        ],
    )
    

app.layout = html.Div(
    className="row",
    style={"max-width": "100%", "font-size": "1.5rem", "padding": "0px 0px"},
    children=[
        html.Div(
            [
                html.H3(
                    "t-SNE Explorer",
                    className="header_title",
                    id="app-title"
                )
            ],
            className="nine columns header_title_container"
        ),
        html.Div(
            className="row background",
            style={"padding": "10px"},
            children=[
                html.Div(
                    className="three columns",
                    children=[
                        Card([
                            dcc.Dropdown(
                                id="dropdown-dataset",
                                searchable=False,
                                clearable=False,
                                options=[
                                    {
                                        "label": "MNIST Digits",
                                        "value": "mnist_3000"
                                    }
                                ],
                                placeholder="Select a dataset",
                                value="mnist_3000",
                            ),
                            NamedSlider(
                                name="Number of Iterations",
                                short="iterations",
                                min=250,
                                max=1000,
                                step=None,
                                val=500,
                                marks={
                                    i: str(i) for i in [250, 500, 750, 1000]
                                }
                            ),
                            NamedSlider(
                                name="Perplexity",
                                short="perplexity",
                                min=3,
                                max=100,
                                step=None,
                                val=30,
                                marks={i: str(i) for i in [3, 10, 30, 50, 100]},
                            ),
                            NamedSlider(
                                name="Initial PCA Dimensions",
                                short="pca-dimension",
                                min=25,
                                max=100,
                                step=None,
                                val=50,
                                marks={i: str(i) for i in [25, 50, 100]},
                            ),
                            NamedSlider(
                                name="Learning Rate",
                                short="learning-rate",
                                min=10,
                                max=200,
                                step=None,
                                val=100,
                                marks={i: str(i) for i in [10, 50, 100, 200]},
                            ),
                        ])
                    ]
                ),
                html.Div(
                    className="three columns",
                    children = [
                        dcc.Graph(id="graph-3d-plot-tsne", style={"height": "98vh"})
                    ]
                ),
                html.Div(
                    className="three columns",
                    children = [
                        dcc.Graph(id='graph-violin')
                    ]
                ),
                html.Div(
                    className="three columns",
                    id="euclidean-distance",
                    children=[
                        Card(
                            style={"padding": "5px"},
                            children=[
                                html.Div(
                                    id="div-plot-click-message",
                                    style={
                                        "text-align": "center",
                                        "margin-bottom": "7px",
                                        "font-weight": "bold",
                                    },
                                ),
                                html.Div(id="div-plot-click-image"),
                            ],
                        )
                    ],
                ),                
            ]
        )
    ]
)


def generate_figure_image(groups, layout):

    data = []

    for idx, val in groups:
        scatter = go.Scatter3d(
            name=idx,
            x=val["x"],
            y=val["y"],
            z=val["z"],
            text=[idx for _ in range(val["x"].shape[0])],
            textposition="top center",
            mode="markers",
            marker=dict(size=3, symbol="circle"),
        )
        data.append(scatter)

    figure = go.Figure(data=data, layout=layout)

    return figure



@app.callback(
    Output("graph-violin", "figure"),
    [
        Input("dropdown-dataset", "value"),
        Input("slider-iterations", "value"),
        Input("slider-perplexity", "value"),
        Input("slider-pca-dimension", "value"),
        Input("slider-learning-rate", "value"),
    ],
)
def display_violin_plot(
    dataset,
    iterations,
    perplexity,
    pca_dim,
    learning_rate):
    if dataset:
        path = f"data/iterations_{iterations}/perplexity_{perplexity}/pca_{pca_dim}/learning_rate_{learning_rate}"


        try:
                data_url = [
                    "data",
                    "iterations_" + str(iterations),
                    "perplexity_" + str(perplexity),
                    "pca_" + str(pca_dim),
                    "learning_rate_" + str(learning_rate),
                    "data.csv",
                ]
       
                full_path = PATH.joinpath(*data_url)
                embedding_df = pandas.read_csv(
                    full_path, index_col=0, encoding="ISO-8859-1"
                )
        #
        except FileNotFoundError as error:
            print(
                error,
                "\n The dataset was not found.  Please generate it using generate_demo_embeddings.py"
            )
            return go.Figure()

        if dataset in IMAGE_DATASETS:
            figure= go.Figure(data=go.Violin(y=embedding_df["x"]))

        else:
            figure = go.Figure()

        return figure



@app.callback(
    Output("graph-3d-plot-tsne", "figure"),
    [
        Input("dropdown-dataset", "value"),
        Input("slider-iterations", "value"),
        Input("slider-perplexity", "value"),
        Input("slider-pca-dimension", "value"),
        Input("slider-learning-rate", "value"),
    ],
)
def display_3d_scatter_plot(
    dataset,
    iterations,
    perplexity,
    pca_dim,
    learning_rate):
    if dataset:
        path = f"data/iterations_{iterations}/perplexity_{perplexity}/pca_{pca_dim}/learning_rate_{learning_rate}"

        try:
                data_url = [
                "data",
                "iterations_" + str(iterations),
                "perplexity_" + str(perplexity),
                "pca_" + str(pca_dim),
                "learning_rate_" + str(learning_rate),
                "data.csv",
                ]

                full_path = PATH.joinpath(*data_url)
                embedding_df = pandas.read_csv(
                    full_path, index_col=0, encoding="ISO-8859-1"
                )

        except FileNotFoundError as error:
            print(
                error,
                "\nThe dataset was not found. Please generate it using generate_demo_embeddings.py",
            )
            return go.Figure()

        # Plot layout
        axes = dict(title="", showgrid=True, zeroline=False, showticklabels=False)

        layout = go.Layout(
            margin=dict(l=0, r=0, b=0, t=0),
            scene=dict(xaxis=axes, yaxis=axes, zaxis=axes),
        )

        # For Image datasets
        if dataset in IMAGE_DATASETS:
            embedding_df["label"] = embedding_df.index
            groups = embedding_df.groupby("label")
            figure = generate_figure_image(groups, layout)

        else:
            figure = go.Figure()

        return figure


if __name__ == '__main__':
    app.run_server(debug=True)


