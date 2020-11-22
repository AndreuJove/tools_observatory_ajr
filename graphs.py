import plotly.express as px
import pandas as pd
from data_reader import*
import plotly.graph_objects as go
import numpy as np

"""

Homepages -> Domains and metrics

"""

# Give to rows the proper color in pandas dataframe.


def giving_onthology_colors(domain):
    if domain in lifeScience:
        return "orange"
    elif domain in university:
        return "red"
    elif domain in generic:
        return "blue"
    elif domain in collections:
        return "green"
    elif domain in institucional:
        return "yellow"
    else:
        return "grey"

# Give to rows the correct onthology in pandas dataframe.

def giving_onthology(domain):
    if domain in lifeScience:
        return "Life Sciences"
    elif domain in university:
        return "Universities"
    elif domain in generic:
        return "Generic"
    elif domain in collections:
        return "Tools Collections"
    elif domain in institucional:
        return "Institutional"
    else:
        return "others"
# Create px bar for domains


def create_px_bar(df, x_value, y_value, title_given, color_given, discrete_sequence):
    fig = px.bar(df, x=x_value, y=y_value, log_x=True, color=color_given,
                 color_discrete_sequence=discrete_sequence,
                 template='simple_white', orientation='h',
                 hover_data={x_value: False, y_value: False},
                 hover_name=x_value)
    fig.update_layout(yaxis_categoryorder='total ascending', bargap=0.4,
                      title=title_given, title_x=0.5, title_font_family="Arial", title_font_color="#383838")
    fig.update_yaxes(showticklabels=True)
    return fig


# Colors for all pies chart:
colors = ['#1976d3', '#64b5f6']

# Function create pie_chart in:
def create_pie_chart(values_list, labels_list, title_pie):
    pie = go.Figure(
        data=[go.Pie(labels=labels_list, values=values_list, hole=0.55)])
    pie.update_traces(hoverinfo='value', marker=dict(colors=colors))
    pie.update_layout(title=f"<b>{title_pie} ({str(sum(values_list))})</b>", title_x=0.5,
                      legend_orientation="h", title_font_family="Arial", title_font_color="#383838")
    return pie

# Barplot for HTTP codes:

def create_bar_http_codes(dict_values_codes):
    df_http_codes = pd.DataFrame({"HTTP code": list(dict_values_codes.keys()), "Count": list(
        dict_values_codes.values()), "color": '#7bc0f7'}).sort_values('Count', ascending=False).reset_index(drop=True)
    fig_hist = px.bar(df_http_codes, x="HTTP code", y="Count", color_discrete_sequence=df_http_codes.color.unique(
    ), log_y=True, template='none', hover_data={'HTTP code': False, 'Count': False}, hover_name="Count")
    fig_hist.update_layout(xaxis_type='category', bargap=0.5, yaxis_visible=False, yaxis_showticklabels=False,
                           title="Resume HTTP Codes" + " ("+str(sum(dict_values_codes.values()))+")", title_x=0.5, title_font_family="Arial", title_font_color="#383838")
    return fig_hist

# Plot histogram domains:


def create_histogram_domains(values, values_col1, values_col2):
    if not values or values == ['others']:
        df = pd.DataFrame(
            {"Domain": values_col1, "Count": values_col2}).iloc[::-1]
        df['Count'] = 0
        return create_px_bar(df, "Count", "Domain", "Primary classification about domains in tools", None, None)
    for i, t in enumerate(values):
        if t == 'university':
            values[i] = "Universities"
        elif t == 'institucional':
            values[i] = "Institutional"
        elif t == 'collections':
            values[i] = "Tools Collections"
        elif t == 'lifeScience':
            values[i] = "Life Sciences"
        elif t == 'generic':
            values[i] = "Generic"
    df = pd.DataFrame({"Domain": values_col1, "Count": values_col2}).iloc[::-1]
    df['color'] = df['Domain'].apply(giving_onthology_colors)
    df['Procedence'] = df['Domain'].apply(giving_onthology)
    df = df[df['Procedence'].isin(values)]
    return create_px_bar(df, "Count", "Domain", "Primary classification about domains in tools", 'Procedence', df.color.unique())


"""
Graphs for the tab Homepages -> Acces
"""
# Create bar for http codes in acces tab:


def create_px_bar_http_codes(df, x_value, y_value, title_given, color_given):
    df = df.copy()
    df['color'] = color_given
    fig = px.bar(df, x=x_value, y=y_value, log_y=True,
                 color_discrete_sequence=df.color.unique(),
                 template='simple_white',
                 hover_data={x_value: False, y_value: False},
                 hover_name=y_value)
    # fig.update_xaxes(ticks="outside", 
    #                 tickfont=dict(family='Helvetica', color='black'),                                   
    #                 )
    fig.update_layout(xaxis_type='category', 
                        bargap=0.7,
                        xaxis = dict(
                            automargin=True,
                            tickfont=dict(family='Helvetica', size=10, color='black'),
                        ),
                      title=f"<b>{title_given} ({df[y_value].sum()})</b>", title_x=0.5
                      )
    return fig

def create_box_plot_time_access(df):
    fig = px.box(df, y="Access time", 
                    log_y=True, points="outliers", 
                    hover_data={"Website", "Redirections"},
                    template="simple_white",
                    labels={"Access time" : "Average Access Time (ms)", "x" : "websites"},
                )
    fig.update_layout(title=f"<b> Average Access Time (AAT)</b>", title_x=0.5,
                         xaxis_title='Websites'
                        )
    return fig

def create_px_bar_days_up(df, x_value, y_value, title_given, color_given):
    for i, t in df.iterrows():
        df.at[i, x_value] = int(t[0])
    df = df.sort_values(by=x_value, ascending=True).reset_index(drop=True)
    df['color'] = color_given
    fig = px.bar(   df, x=x_value, 
                    y=y_value, log_y=True,
                    template='simple_white', 
                    color_discrete_sequence=df.color.unique(),
                    hover_data={x_value: True, y_value: False},
                    hover_name=y_value
                )
    fig.update_layout(  bargap=0.4, 
                        title=f"<b> {title_given} ({df[y_value].sum()} websites) <b>", 
                      
                        title_x=0.5
                    )
    
    return fig


"""
Graphs for the tab Homepages -> JavaScript

"""

def create_scatter_plot(df):
    fig = px.scatter(df, x="year", 
                        y="percentage_of_change", 
                        color="Procedence", 
                        color_discrete_sequence=df.color.unique(),
                        labels={"percentage_of_change": "Percentage of change",
                         'year': 'Year'},
                         hover_name="first_url"
                    )
    fig.update_layout(bargap=0.4,title=f"<b>Correlationship between percentage of change and year of publication ({len(df)})</b>", title_x=0.5)
    return fig

def fill_df_color_procedence(df):
    df = df.copy()
    df['color'] = df['domain'].apply(giving_onthology_colors)
    df['Procedence'] = df['domain'].apply(giving_onthology)
    return df

# Create bins for histogram:
def create_fig_bar_percentage_of_change(df, title_given):
    df = df.sort_values(by="percentage_of_change",
                        ascending=False).reset_index(drop=True)
    total = len(df)
    counts, bins = np.histogram(df.percentage_of_change, bins=range(0, 100, 5))
    counts = np.insert(counts, 0, 0, axis=None)
    fig_bar = px.bar(x=bins, y=counts, labels={'x': 'Percentage of change', 'y': 'Count'}, log_y=True, template="simple_white",
                     hover_name=counts)
    fig_bar.update_traces(marker_color='#7bc0f7')
    fig_bar.update_layout(title=f"<b>Percentage of change of dynamic websites in {title_given} ({total})</b>",
                          title_x=0.5, title_font_family="Arial", title_font_color="#383838")
    return fig_bar


def crate_box_plot_from_df(title_given, df):
    total_df = len(df)
    fig = px.box(df, x="domain", y="percentage_of_change", color="domain",
                 points='all',
                 hover_data={"domain": False,
                             "percentage_of_change": False, "first_url": False},
                 hover_name="year",
                 template='simple_white',
                 labels={"percentage_of_change": "Percentage of change",
                         'domain': 'Domain'}
                 )

    list_change = list(fig['layout']['xaxis']['categoryarray'])
    for i, domain in enumerate(list_change):
        count_df = len(df[df['domain'] == domain])
        count_total = get_the_count_of_one_domain(domain)
        list_change[i] = f"{domain} ({count_df}/{count_total})"

    fig.update_layout(showlegend=False,
                      title=f"<b>Dynamic domains in {title_given} ({total_df}) + Year of Publication of the tool</b>",
                      title_x=0.5, title_font_family="Arial", 
                      title_font_color="#383838",
                      xaxis=dict(
                            ticktext=list_change,
                            tickvals=list(range(0, len(list_change))),
                            
                            
                                )
                    )

    fig.update_xaxes(ticks="outside", tickfont=dict(family='Arial', color='black'))
    # print(dir(fig['layout']['xaxis']['tickfont']))
    return fig
