import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

# Data file
df = (pd.read_csv('data/rand.csv', parse_dates = ['date'])
        .drop(columns = 'Unnamed: 0', axis = 1))

df = (df.copy()
        .loc[df['amount']<0]
        .set_index('date')
        .resample('D').agg({'amount':'sum', 'bal':'last'})
        .replace(np.nan, method = 'ffill')
        .reset_index()
        .assign(cumulative_annual = lambda x: x.groupby(x['date'].dt.year)['amount'].cumsum().multiply(-1),
                cumulative_month = lambda x: x.groupby(x['date'].dt.to_period('M'))['amount'].cumsum().multiply(-1),
                month = lambda x: x['date'].dt.to_period('M').astype('str'), 
                day = lambda x: x['date'].dt.day))

# General app structure
## Add titles etc in here
app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(id='yaxis-column-1',
                         options=[{'label': i, 'value': i} for i in df['month'].unique()], 
                         value='2019-04'
                         ),
        ],
        style={'width': '20%', 
               'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column-2',
                options=[{'label': i, 'value': i} for i in df['month'].unique()],
                value='2019-05'),
        ],
        style={'width': '20%', 
               'float': 'left', 
               'display': 'inline-block'})
    ]),

    dcc.Graph(id='months-graphic'),

])

# Formatting properties
labels = ['This month to date', 'Last month', 'Average month']
colours = ['rgb(98, 29, 75)', 'rgb(61, 72, 73)', 'rgb(189,189,189)']
mode_size = [12, 8, 8]
line_size = [4, 2, 2]

# Update graph based on callbacks
@app.callback(Output('months-graphic', 'figure'),
              [Input('yaxis-column-1', 'value'),
               Input('yaxis-column-2', 'value')])

def update_graph(yaxis_column_1_name, yaxis_column_2_name):
    traces = []
    traces.append(go.Scatter(
                x = df.loc[df['month'] == yaxis_column_1_name, 'day'],
                y = df.loc[df['month'] == yaxis_column_1_name, 'cumulative_month'],
                name = "{}".format(yaxis_column_1_name),
                mode = 'lines', 
                line = dict(color = colours[0], 
                            width = line_size[0]),
                connectgaps=True))
    traces.append(go.Scatter(
                x = df.loc[df['month'] == yaxis_column_2_name, 'day'],
                y = df.loc[df['month'] == yaxis_column_2_name, 'cumulative_month'],
                name = "{}".format(yaxis_column_2_name),
                mode = 'lines', 
                line = dict(color = colours[1], 
                            width = line_size[1]),
                connectgaps=True))


    layout = go.Layout(xaxis = dict(showline=True,
                                    showgrid=False,
                                    showticklabels=True,
                                    linecolor='rgb(204, 204, 204)',
                                    linewidth=2,
                                    ticks='outside',
                                    tickcolor='rgb(204, 204, 204)',
                                    tickwidth=2,
                                    ticklen=5,
                                    tickfont=dict(family='Arial',
                                                  size=12,
                                                  color='rgb(82, 82, 82)')),
                       yaxis = dict(showline=True,
                                    showgrid=False,
                                    zeroline=False,
                                    hoverformat = '$,.2f',
                                    showticklabels=True,
                                    linecolor='rgb(204, 204, 204)',
                                    linewidth=2,
                                    ticks='outside',
                                    tickcolor='rgb(204, 204, 204)',
                                    tickwidth=2,
                                    ticklen=5,
                                    tickfont=dict(family='Arial',
                                                  size=12,
                                                  color='rgb(82, 82, 82)')),
                        autosize = False,
                        margin = dict(autoexpand=False, 
                                      l=100,
                                      r=100,
                                      t=100,
                                      b=100),
                       showlegend=False)

    annotations = []

    # Title
    annotations.append(dict(xref='paper', #reference point to measure x from - 'paper' means the edges 
                            yref='paper', 
                            x=0.0, 
                            y=1.2,
                            xanchor='left', 
                            yanchor='bottom',
                            text='Hi Rachel',
                            font=dict(family='Arial',
                                      size=30,
                                      color='rgb(61, 72, 73)'),
                            showarrow=False))

    # Subtitle
    annotations.append(dict(xref='paper', #reference point to measure x from - 'paper' means the edges 
                            yref='paper', 
                            x=0.0, 
                            y=1.1,
                            xanchor='left', 
                            yanchor='bottom',
                            text='How is your spend tracking this month?',
                            font=dict(family='Arial',
                                      size=14,
                                      color='rgb(61, 72, 73)'),
                            showarrow=False))
    # Note
    annotations.append(dict(xref='paper', 
                            yref='paper', 
                            x=0, 
                            y=-0.2,
                            xanchor='left',
                            yanchor='top',
                            text='Note: All data is fabricated. This project was created in 2019.',
                            font=dict(family='Arial',
                                      size=12,
                                      color='rgb(150,150,150)'),
                                      showarrow=False))

# # # Line labels
# for i in range(len(labels)):
#     annotations.append(dict(xref='paper', 
#                             x=0.95, 
#                             y=report_data[report_data.columns[i]].max(),
#                             xanchor='left', 
#                             yanchor='middle',
#                             text='${0:,.2f}'.format(report_data[report_data.columns[i]].max()),
#                             font=dict(family='Arial',
#                                       size=16, 
#                                       color = colours[i]),
#                             showarrow=False))
    
# for i in range(len(labels)):
#     annotations.append(dict(xref='paper', 
#                             x=0.95, 
#                             y=report_data[report_data.columns[i]].max() + 1000,
# #                             y=report_data[report_data.columns[i]].max() + (report_data.max().max() * 0.1),
#                             xanchor='left', 
#                             yanchor='middle',
#                             text=labels[i],
#                             font=dict(family='Arial',
#                                       size=12, 
#                                       color = colours[i]),
#                             showarrow=False))

    layout['annotations'] = annotations # This adds the annotations to the layout dictionary - otherwise gets a bit unwieldy

    return {
        'data': traces,
        'layout' : layout
        }

if __name__ == '__main__':
    app.run_server(debug=True)




