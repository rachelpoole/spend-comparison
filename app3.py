import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go

df = (pd.read_csv('data/rand.csv', parse_dates = ['date'])
        .drop(columns = 'Unnamed: 0', axis = 1))

daily = df.groupby('date')[['amount', 'bal']].agg({'amount':'sum', 'bal':'last'})

spend = (df.copy()
          .loc[df['amount']<0]
          .reset_index(drop=True)
          .assign(cumulative_annual = lambda x: x.groupby(x['date'].dt.year)['amount'].cumsum(),
                  cumulative_month = lambda x: x.groupby(x['date'].dt.month)['amount'].cumsum()))

daily_spend = (df.copy()
                 .loc[df['amount']<0]
                 .groupby('date')[['amount', 'bal']].agg({'amount':'sum', 'bal':'last'})
                 .reset_index()
                 .assign(cumulative_annual = lambda x: x.groupby(x['date'].dt.year)['amount'].cumsum(),
                         cumulative_month = lambda x: x.groupby(x['date'].dt.to_period('M'))['amount'].cumsum(), 
                         month = lambda x: x['date'].dt.to_period('M'), 
                         day = lambda x: x['date'].dt.day))

data = (daily_spend.pivot_table(values = 'cumulative_month', index = 'day', columns = 'month', aggfunc = 'sum')
                   .multiply(-1)
                   .replace(np.nan, method = 'ffill')
                   .assign(average_past_12_months = lambda x: x[x.columns[-12:]].mean(axis=1)))
data.columns = data.columns.astype('str')

report_data = data.copy()[data.columns[-3:]]
report_data.columns = ['2019-04', '2019-03', 'past_12_months_average']
report_data = report_data.rename(columns = {'2019-04': 'This month to date', '2019-03': 'Last month', 'past_12_months_average': 'Average month'})

# Set some values to np.nan for authenticity - as if the month hasn't finished
report_data.loc[21:, 'This month to date'] = np.nan

# Manually remove April 31 - work out the proper way to do this
report_data.loc[31, 'Last month'] = np.nan

import plotly.plotly as py
import plotly.graph_objs as go

# Properties
labels = ['This month to date', 'Last month', 'Average month']
colours = ['rgb(98, 29, 75)', 'rgb(61, 72, 73)', 'rgb(189,189,189)']
mode_size = [12, 8, 8]
line_size = [4, 2, 2]

# Add data 
traces = []

for i in range(len(labels)):
    traces.append(go.Scatter(x = report_data.index, 
                             y = report_data[report_data.columns[i]], 
                             name = labels[i],
                             mode = 'lines', 
                             line = dict(color = colours[i], 
                                         width = line_size[i]),
                             connectgaps=True))
    
for i in range(len(labels)):
    traces.append(go.Scatter(x= [report_data[report_data.columns[i]].idxmax()],
                             y= [report_data[report_data.columns[i]].max()],
                             hoverinfo = 'skip',
                             mode='markers',
                             marker= dict(color=colours[i], 
                                          size=mode_size[i])))

# Add layout
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
                        text='Spend comparison',
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
                        text='Compare this month to your average spend.',
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

# # Line labels
for i in range(len(labels)):
    annotations.append(dict(xref='paper', 
                            x=0.95, 
                            y=report_data[report_data.columns[i]].max(),
                            xanchor='left', 
                            yanchor='middle',
                            text='${0:,.2f}'.format(report_data[report_data.columns[i]].max()),
                            font=dict(family='Arial',
                                      size=16, 
                                      color = colours[i]),
                            showarrow=False))
    
for i in range(len(labels)):
    annotations.append(dict(xref='paper', 
                            x=0.95, 
                            y=report_data[report_data.columns[i]].max() + 1000,
#                             y=report_data[report_data.columns[i]].max() + (report_data.max().max() * 0.1),
                            xanchor='left', 
                            yanchor='middle',
                            text=labels[i],
                            font=dict(family='Arial',
                                      size=12, 
                                      color = colours[i]),
                            showarrow=False))

layout['annotations'] = annotations # This adds the annotations to the layout dictionary - otherwise gets a bit unwieldy

fig = go.Figure(data=traces, layout=layout)
plotly.offline.plot(fig, filename='spend-comparison.html')