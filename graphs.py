import plotly.express as px
import pandas as pd
from data_reader import*
import plotly.graph_objects as go
import numpy as np


"""

Homepages -> Domains and metrics

"""

#Give to rows the proper color in pandas dataframe.
def giving_onthology_colors(domain):
    if domain in lifeScience:
        return "orange"
    elif domain in university:
        return "red"
    elif domain in generic:
        return "blue"
    elif domain in collections:
        return "green"
    else:
        return "yellow"

#Give to rows the correct onthology in pandas dataframe.
def giving_onthology(domain):
    if domain in lifeScience:
        return "Life Sciences"
    elif domain in university:
        return "Universities"
    elif domain in generic:
        return "Generic"
    elif domain in collections:
        return "Tools Collections"
    else:
        return "Institutional"

#Create px bar for domains
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

#Function create pie_chart in:
def create_pie_chart(values_list, labels_list, title_pie):
    pie = go.Figure(
        data=[go.Pie(labels=labels_list, values=values_list, hole=0.55)])
    pie.update_traces(hoverinfo='value', marker=dict(colors=colors))
    pie.update_layout(title=title_pie + " ("+str(sum(values_list))+")", title_x=0.5,
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
        return create_px_bar(df, "Count", "Domain","Primary classification about domains in tools", None, None)
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
    return create_px_bar(df, "Count", "Domain","Primary classification about domains in tools", 'Procedence', df.color.unique())


"""
Graphs for the tab Homepages -> Acces
"""
#Create bar for http codes in acces tab:
def create_px_bar_http_codes(array_x, array_y, x_value, y_value, title_given, color_given):
    df = pd.DataFrame(list(zip(array_x, array_y)), 
                    columns=[x_value, y_value]).sort_values(by=y_value, ascending=False).reset_index(drop=True)
    df['color'] = color_given
    fig = px.bar(df, x=x_value, y=y_value, log_y=True, 
                color_discrete_sequence=df.color.unique(),
                 template='simple_white',
                 hover_data={x_value: False, y_value: False},
                 hover_name=y_value)
    # fig.update_traces(texttemplate='%{Count}', textposition='outside', textfont_size=25)
    fig.update_layout(xaxis_type='category', bargap=0.7, uniformtext_minsize=25,
                      title=f"{title_given} ({df['Count'].sum()})", title_x=0.5)
    return fig

#This function create 
def create_px_bar_horizontal(array_x, array_y, x_value, y_value, title_given, color_given):
    df = pd.DataFrame(list(zip(array_y, array_x)), columns=[x_value, y_value]).sort_values(by=x_value, ascending=False).reset_index(drop=True)
    df['color'] = color_given
    fig = px.bar(df, x=x_value, y=y_value, log_x=True,
                 template='simple_white', orientation='h',
                 color_discrete_sequence=df.color.unique(),
                 hover_data={x_value: False, y_value: False},
                 hover_name=x_value)
    fig.update_layout(yaxis_categoryorder='total ascending', bargap=0.4,
                      title=f"{title_given} ({df['Count'].sum()})", title_x=0.5)
    return fig





"""
Graphs for the tab Homepages -> JavaScript

"""


# Create bins for histogram:
def create_df_and_fig_bar_dynamic_percentages(array_of_numbers, title_given):
    df_percentages = pd.DataFrame(array_of_numbers, columns=['Percentage']).sort_values(
    by="Percentage", ascending=False).reset_index(drop=True)
    total = len(df_percentages)
    counts, bins = np.histogram(df_percentages.Percentage, bins=range(0, 100, 5))
    counts = np.insert(counts, 0, 0, axis=None)
    fig_bar = px.bar(x=bins, y=counts, labels={'x': 'Percentage of change', 'y': 'Count'}, log_y=True, template="simple_white",
             hover_name=counts)
    fig_bar.update_traces(marker_color='#7bc0f7')
    fig_bar.update_layout(title=f"Percentage of change in {title_given}({total} websites)",
                      title_x=0.5, title_font_family="Arial", title_font_color="#383838")
    return fig_bar



# Function that creates box plot with args traces:
def create_box_plot(title_given, *args):
    total = 0
    fig = go.Figure()
    for arg in args:
        if list(arg.values())[0]:
            total_points = len(list(arg.values())[0])
            total_count_of_domain = get_count_of_a_domain(domains_count, list(arg.keys())[0])
            fig.add_trace(
                go.Box(y=(list(arg.values())[0]), name=f"{list(arg.keys())[0]} ({total_points}/{total_count_of_domain})", boxpoints="all"))
            total += len((list(arg.values())[0]))
    fig.update_layout(title=f"JavaScript usage of {title_given}({total} websites)",
                      title_x=0.5, title_font_family="Arial", title_font_color="#383838")
    return fig