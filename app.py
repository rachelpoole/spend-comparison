# -*- coding: utf-8 -*-
# Modifed for git
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


colors = {
    'background': '#FEFEFE',
    'text': '#000000'
    }

markdown_text = '''
### Hello Rachel

The spend comparison app shows you how your spending today compares to your
spending over the past two years. You may find this helpful to manage your
budget.
'''

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')


app.layout = html.Div(style = {'backgroundColor' : colors['background']}, children = [
    # html.H1(
    #     children='Hello Rachel',
    #     style = {
    #         'textAlign' : 'left',
    #         'color': colors['text']
    #     }
    # ),

    # html.Div(
    # 	children='This is how your spending has changed over the last three years.', 
    # 	style = {
    #     	'textAlign' : 'left',
    #     	'color' : colors['text']
    # 	}
    # ),

    dcc.Markdown(children = markdown_text),

    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                go.Scatter(
                    x=df[df['continent'] == i]['gdp per capita'],
                    y=df[df['continent'] == i]['life expectancy'],
                    text=df[df['continent'] == i]['country'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.continent.unique()
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                yaxis={'title': 'Life Expectancy'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
                )
            }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
