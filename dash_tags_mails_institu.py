import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pickle
import ast
from dash.dependencies import Input, Output

frameworks_ordered = {'jQuery': 4495,
 'jQuery UI': 601,
 'Modernizr': 506,
 'RequireJS': 435,
 'Prototype': 368,
 'Handlebars': 293,
 'Underscore.js': 229,
 'Vue.js': 151,
 'AngularJS': 144,
 'Lightbox': 134,
 'Select2': 65,
 'React': 50,
 'Backbone.js': 45,
 'Twitter typeahead.js': 43,
 'MooTools': 43,
 'Moment.js': 40,
 'Lo-dash': 32,
 'spin.js': 30,
 'YUI': 28,
 'script.aculo.us': 24,
 'ExtJS': 12,
 'Hammer.js': 11,
 'prettyPhoto': 10,
 'math.js': 8,
 'Lazy.js': 7,
 'Reveal.js': 7,
 'HeadJS': 6,
 'Dojo': 6,
 'TweenMax': 5,
 'Socket.io': 4,
 'basket.js': 4,
 'RightJS': 3,
 'xui': 3,
 'Snap.svg': 3,
 'Polymer': 2,
 'Ramda': 2,
 'Mustache': 2,
 'Riot': 1,
 'Moment Timezone': 1,
 'MochiKit': 1,
 'Wink': 1,
 'Meteor': 1,
 'RxJS': 1}

languages_ordered_counter = {'R': 4630,
                             'Python': 2175,
                             'Java': 1851,
                             'C++': 1339,
                             'Perl': 1273,
                             'C': 1002,
                             'JavaScript': 692,
                             'MATLAB': 351,
                             'PHP': 271,
                             'Shell': 215,
                             'Ruby': 189,
                             'SQL': 175,
                             'Javascript': 171,
                             'C#': 130,
                             'Fortran': 89,
                             'Groovy': 69,
                             'Bash': 18,
                             'Visual Basic': 18,
                             'Pascal': 16,
                             'Mathematica': 10,
                             'Delphi': 10,
                             'Other': 9,
                             'Haskell': 7,
                             'Julia': 6,
                             'Scala': 6,
                             'D': 5,
                             'SAS': 5,
                             'Lua': 4,
                             'Lisp': 3,
                             'JSP': 3,
                             'ActionScript': 3,
                             'PyMOL': 2,
                             'Racket': 1,
                             'Ada': 1,
                             'Maple': 1,
                             'AWK': 1,
                             'Elm': 1,
                             'CWL': 1}

tags_ordered_counter = {'BioConductor': 4324,
                        'Proteomics': 1638,
                        'galaxyPasteur': 655,
                        'Animal and Crop Genomics': 565,
                        'EMBOSS': 512,
                        'ms-utils': 439,
                        'Rare Disease': 372,
                        'EBI Tools': 278,
                        'DRCAT': 274,
                        'UGent': 250,
                        'de.NBI': 244,
                        'BIG N2N': 242,
                        'VIB': 173,
                        'elixir-fr-sdp-2019': 161,
                        'RD-connect': 148,
                        'ELIXIR-CZ': 129,
                        'Institut Pasteur': 128,
                        'EBI Training Tools': 123,
                        'Instruct': 120,
                        'BioExcel': 116,
                        'REPET': 107,
                        'Czech Republic': 106,
                        'COVID-19': 94,
                        'BLAST': 92,
                        'Plant Systems Biology': 89,
                        'ELIXIR-ES': 79,
                        'Ensembl Tools': 75,
                        'Compomics': 70,
                        'Ensembl Genomes': 48,
                        'Rostlab tools': 46,
                        'FASTA utility': 46,
                        'Bologna Biocomputing group': 45,
                        'LCC NCBR': 41,
                        'Drug Research and Development': 41,
                        'Complex Disease': 41,
                        'Mendelian Disease': 41,
                        'BLAST utility': 39,
                        'JIB.tools': 39,
                        'ELIXIR Trainer Tools': 39,
                        'SAMtools': 38,
                        'BioMedBridges Tools': 36,
                        'Bioconductor': 36,
                        'Developed_RD-Connect': 35,
                        'gatk': 34,
                        'Galaxy Tools': 34,
                        'clustal': 33,
                        'EMBOSS at EBI Tools': 30,
                        'gdtools': 30,
                        'Cytoscape': 29,
                        'BiGi': 29,
                        'BioInfra.Prot': 29,
                        'FROGS': 26,
                        'PredictProtein': 26,
                        'Picard': 26,
                        'FR': 25}

mails_ordered_counter = {'gmail.com': 1937, 'emboss.open-bio.org': 767, 'pasteur.fr': 724, 'ebi.ac.uk': 326, 'ms-utils.org': 221, 'upf.edu': 188, 'cbs.dtu.dk': 122, 'inra.fr': 106, 'scilifelab.se': 105, 'bioconductor.org': 99, 'crg.eu': 85, 'embl.de': 83, 'unipd.it': 79, 'umich.edu': 78, '163.com': 78, 'mail.muni.cz': 78, 'uw.edu': 76, 'igh.cnrs.fr': 75, 'sanger.ac.uk': 72, 'stfc.ac.uk': 71, 'jhu.edu': 71, 'ugent.be': 71, 'stanford.edu': 62, 'ncbi.nlm.nih.gov': 62, 'fhcrc.org': 62, 'cam.ac.uk': 61, 'imperial.ac.uk': 59, 'wehi.edu.au': 59, 'inserm.fr': 56, 'jimmy.harvard.edu': 55, 'charite.de': 55, 'gene.com': 54, 'mssm.edu': 54, 'dkfz.de': 54, 'utoronto.ca': 53, 'biocomp.unibo.it': 52, 'ucsd.edu': 51, 'u.washington.edu': 51, 'yale.edu': 51, 'ut.ee': 51, 'hotmail.com': 49, 'irbbarcelona.org': 47, 'yahoo.com': 47, 'cnio.es': 47, 'rub.de': 47, 'psb.vib-ugent.be': 46, 'imtech.res.in': 46, 'googlegroups.com': 46, 'channing.harvard.edu': 45, 'ipk-gatersleben.de': 45, 'broadinstitute.org': 44,
                         'snsb.de': 44, 'binf.ku.dk': 42, 'mail.nih.gov': 41, 'soe.ucsc.edu': 41, 'bsc.es': 40, 'systemsbiology.org': 40, 'uni.lu': 40, 'univ-amu.fr': 40, 'helsinki.fi': 39, 'umassmed.edu': 39, 'univ-paris-diderot.fr': 38, 'cebitec.uni-bielefeld.de': 37, 'ki.se': 37, 'univie.ac.at': 37, 'pitt.edu': 36, 'zju.edu.cn': 36, 'oulouse.inra.fr': 36, 'princeton.edu': 34, 'imim.es': 34, 'unibo.it': 33, 'nih.gov': 33, 'bcm.edu': 32, 'ucl.ac.uk': 32, 'bcgsc.ca': 32, 'sjtu.edu.cn': 32, 'unisa.it': 32, 'jhsph.edu': 31, 'mit.edu': 31, 'isb-sib.ch': 31, 'mayo.edu': 30, 'upol.cz': 30, 'wustl.edu': 30, 'unimi.it': 29, 'usc.edu': 29, 'vu.nl': 29, 'uestc.edu.cn': 29, 'bsse.ethz.ch': 29, 'bu.edu': 28, 'uni-muenster.de': 28, 'monash.edu': 28, 'openanalytics.eu': 28, 'ulb.ac.be': 28, 'helmholtz-muenchen.de': 27, 'lbl.gov': 27, 'manchester.ac.uk': 27, 'emory.edu': 27, 'ens.fr': 27, 'ucdavis.edu': 26, 'bioinf.uni-leipzig.de': 26, 'uq.edu.au': 26, 'vanderbilt.edu': 26, 'genouest.org': 26, 'ensemblgenomes.org': 26, 'cpr.ku.dk': 26}


names_ordered_counter = {'Galaxy Support Team': 623, 'EMBOSS': 523, 'Support': 281, 'Wellcome Trust': 266, 'EMBOSS Contributors': 256, 'EMBL EBI': 256, 'UK MRC': 256, 'UK BBSRC': 256, 'BioCatalogue': 198, 'EMBL-EBI': 158, 'Contact Form': 150, 'DRCAT': 138, 'CBS': 124, 'ugent.be': 116, 'Web Production': 106, 'Contact form': 98, 'ELIXIR-CZ': 94, 'BioConductor Package Maintainer': 92, 'ELIXIR-ITA-PADOVA': 91, 'SIB Swiss Institute of Bioinformatics': 80, 'Instruct': 67, 'bils.se': 61, 'Maxime Garcia': 54, 'BioJS': 51, 'David Sehnal': 46, 'Laura I. Furlong': 45, 'Silvio C.E. Tosatto': 43, 'ELIXIR-ITA-BOLOGNA': 40, 'Ferran Sanz': 40, 'Janet Piñero': 40, 'Jacques van Helden': 37, 'IFB ELIXIR-FR': 34, 'Fabien JOURDAN': 33, 'MetaboHub': 33, 'Masaryk University, Brno, Czech Republic': 32, 'GenOuest': 32, 'Lukáš Pravda': 31, 'binf.ku.dk': 31, 'Australia': 31, 'Ensembl Genomes webteam': 31, 'Francesco Ronzano': 31, 'Morten Nielsen': 30, 'University of Padua, Department of Biomedical Sciences, BioComputing UP lab': 30, 'Josep Sauch Pitchard': 30, 'Juan Manuel Ramirez Anguita': 30, 'crg.eu': 28, 'Ensembl team': 28, 'RostLab': 28, 'Rolf Backofen': 28, 'unimelb.edu.au': 27, 'VJ Carey': 26, 'Burkhard Rost': 26, 'Laurent Gatto': 26, 'ExPASy helpdesk': 25, 'Patrice Duroux': 25, 'Lab Roderic Guigo Group': 24, 'BioMedBridges': 24, 'BiBiServ': 24, 'Bionode Team': 24, 'Nino Spataro': 24, 'Paolo Di Tommaso': 24, 'Szilvester Juhos': 24, 'Science for Life Laboratory': 24, 'National Genomics Infrastructure': 24, 'National Bioinformatics Infrastructure Sweden': 24, 'Barntumörbanken': 24, 'Castrense Savojardo': 23, 'Pierre Lindenbaum': 23, 'Hao Lin': 23, 'Zuguang Gu': 23, 'SNSB IT Center': 23,
                         'Deutsche Forschungsgemeinschaft (DFG)': 23, 'Mike Jiang': 22, 'Torsten Seemann': 21, 'CeBiTec': 21, 'bmb.sdu.dk': 21, 'Sofia Kossida': 21, 'PSB': 20, 'Bielefeld University': 20, 'Jan Baumbach': 20}


institutionals = {'EMBL EBI': 256,
                  'EMBOSS': 256,
                  'EMBL-EBI': 155,
                  'CBS': 124,
                  'ugent.be': 116,
                  'SIB Swiss Institute of Bioinformatics': 74,
                  'Instruct': 66,
                  'ELIXIR-ITA-PADOVA': 62,
                  'bils.se': 61,
                  'BioJS': 43,
                  'ELIXIR-CZ': 38,
                  'IFB ELIXIR-FR': 34,
                  'Masaryk University, Brno, Czech Republic': 32,
                  'binf.ku.dk': 31,
                  'crg.eu': 28,
                  'unimelb.edu.au': 27,
                  'ELIXIR-ITA-BOLOGNA': 27,
                  'RostLab': 27,
                  'GenOuest': 25,
                  'Lab Roderic Guigo Group': 24,
                  'BiBiServ': 24,
                  'Science for Life Laboratory': 24,
                  'Barntumörbanken': 24,
                  'University of Padua, Department of Biomedical Sciences, BioComputing UP lab': 23,
                  'CeBiTec': 21,
                  'bmb.sdu.dk': 21,
                  'PSB': 20,
                  'Bielefeld University': 20,
                  'Loschmidt Laboratories': 20,
                  'upf.edu': 19,
                  'ELIXIR-EE': 19,
                  'International Centre for Clinical Research, Brno, Czech Republic': 18,
                  'HD-HuB': 18,
                  'rnateam': 16,
                  'EMBL-EBI Databases': 16,
                  'ELIXIR-ITA-TORVERGATA': 15,
                  'NCBI': 15,
                  'European Molecular Biology Laboratory (EMBL)': 15,
                  'ELIXIR-ITA-CNR': 14,
                  'UiO': 14,
                  'birc.au.dk': 14,
                  'uma.es': 14,
                  'BioInfra.Prot': 14,
                  'ELIXIR-ITA-MILANO': 13,
                  'University Freiburg': 13,
                  'Institut Pasteur': 13,
                  'Identifiers.org': 13,
                  'AT-CUBE': 13,
                  'ELIXIR-ITA-SAPIENZA': 12,
                  'rki.de': 12,
                  'Vrije Universiteit Amsterdam': 12,
                  'ELIXIR-ITA-SALERNO': 11,
                  'Technische Universität München': 11,
                  'Brno University of Technology, Brno, Czech Republic': 11,
                  'Columbia University': 11,
                  'Inserm US14': 11,
                  'cnio.es': 10,
                  'ELIXIR-NL': 10,
                  'lumc.nl': 10,
                  'hdhub': 10,
                  'LIRMM': 10,
                  'Barcelona Supercomputing Center': 9,
                  'cs.manchester.ac.uk': 9,
                  'University of Cambridge': 9}


comparation_http_codes = {'200.0-200': 15822, '200.0-408': 2110, '200.0-301': 157,
                          '202.0-202': 49, '200.0-302': 42, '202.0-200': 5, '200.0-303': 2, '200.0-202': 1}
# df['normalized_values'] = df.apply(lambda row: row.Count/df['Count'].sum(), axis=1)

with open('/data_files/listfile.data', 'rb') as filehandle:
    languages_new = pickle.load(filehandle)

# Plot for langugages used in tools:
def create_bar_plot_languages(year_array):
    df = pd.DataFrame(data=languages_new, columns=[
                      "Language", "Year"]).reset_index(drop=True)
    new_interval = [i for i in range(year_array[0], year_array[1]+1, 1)]
    df = df[df['Year'].isin(new_interval)]
    df['count'] = df.groupby('Language')['Language'].transform('count')
    df = df.rename(columns={'count': 'Count'})
    df_len = len(df)
    df = df.drop_duplicates(['Language'], ignore_index=True).sort_values(
        by=['Count'], ascending=False)
    df = df.drop(['Year'], axis=1).reset_index(drop=True)
    fig_languages = px.bar(df, x="Count", y="Language", log_x=True, color='Language',
                           template='simple_white', orientation='h',
                           height=800,
                           hover_data={'Count': False, 'Language': False},
                           hover_name="Count")
    fig_languages.update_layout(yaxis_categoryorder='total ascending', bargap=0.4,
                                showlegend=False, title="Languages used in " + str(df_len) + " Tools", title_x=0.5)
    return fig_languages


fig_languages_all = create_bar_plot_languages([1980, 2020])


# ---------------------------------------------------------------------------------------------------------


# PLOT ANIMATION SALVA:
df = pd.DataFrame(data=languages_new, columns=[
                  "Language", "Year"]).reset_index(drop=True)
df_new = pd.DataFrame({'Count': df.groupby(
    ["Language", "Year"]).size()}).sort_values(by="Year", ascending=True)
df_new['Language'] = [i[0][0] for i in df_new.iterrows()]
df_new['Year'] = [i[0][1] for i in df_new.iterrows()]
df_new.reset_index(drop=True, inplace=True)
fig_animation = px.bar(df_new, x="Count", y="Language", log_x=True, color='Language',
                       height=800, animation_frame="Year",
                       hover_data={'Count': False,
                                   'Language': False, 'Year': False},
                       hover_name="Count")
fig_animation.update_layout(yaxis_categoryorder='total ascending', bargap=0.4, transition={'duration': 500},
                            showlegend=False, title="Languages used in " + str(df_new['Count'].sum()) + " Tools", title_x=0.5)
fig_animation.update_traces(marker_color='green')

# Plot for Tags Used in tools:
df_tags = pd.DataFrame(tags_ordered_counter.items(), columns=[
                       "Tag", "Count"]).reset_index(drop=True)

fig_tags = px.bar(df_tags, x="Count", y="Tag", log_x=True, color='Tag',
                  template='simple_white', orientation='h',
                  height=1000,
                  hover_data={'Count': False, 'Tag': False},
                  hover_name="Count")
fig_tags.update_layout(yaxis_categoryorder='total ascending', bargap=0.3,
                       showlegend=False, title="Tags more used in Tools (14200)", title_x=0.5)
                       
#Plot counting 200,408:
file = open("jupyter_notebooks/dict_count_402_408.txt", "r")
contents = file.read()
dictionary = ast.literal_eval(contents)
file.close()
df_codes = pd.DataFrame(dictionary.items(), columns=[
    "HTTPs", "Count"]).reset_index(drop=True)
df_codes = df_codes[:35]
fig_codes = px.bar(df_codes, x="Count", y="HTTPs", log_x=True, color='HTTPs',
                   template='simple_white', orientation='h',
                   height=1100,
                   hover_data={'Count': False, 'HTTPs': True},
                   hover_name="Count")
fig_codes.update_layout(yaxis_categoryorder='total ascending', bargap=0.3,
                        showlegend=False, title="HTTPs (200, 408) in the last 6 months (18254)", title_x=0.5)

# Plot for emails endings:
df_emails = pd.DataFrame(mails_ordered_counter.items(), columns=[
    "Email", "Count"]).reset_index(drop=True)
fig_email = px.bar(df_emails, x="Count", y="Email", log_x=True, color='Email',
                   template='simple_white', orientation='h',
                   height=1100,
                   hover_data={'Count': False, 'Email': True},
                   hover_name="Count")
fig_email.update_layout(yaxis_categoryorder='total ascending', bargap=0.3,
                        showlegend=False, title="Ending mails more found in Tools (18254)", title_x=0.5)


# Plot for names in tools:
df_names = pd.DataFrame(names_ordered_counter.items(), columns=[
    "Name", "Count"]).reset_index(drop=True)
fig_names = px.bar(df_names, x="Count", y="Name", log_x=True, color='Name',
                   template='simple_white', orientation='h',
                   height=1100,
                   hover_data={'Count': False, 'Name': True},
                   hover_name="Count")
fig_names.update_layout(yaxis_categoryorder='total ascending', bargap=0.4,
                        showlegend=False, title="All names found in Tools (22487)", title_x=0.5)


# Plot for institutional in tools:
df_institutional = pd.DataFrame(institutionals.items(), columns=[
    "Institutional", "Count"]).reset_index(drop=True)
fig_institutional = px.bar(df_institutional, x="Count", y="Institutional", log_x=True, color='Institutional',
                           template='simple_white', orientation='h',
                           height=1100,
                           hover_data={'Count': False, 'Institutional': True},
                           hover_name="Count")
fig_institutional.update_layout(yaxis_categoryorder='total ascending', bargap=0.4,
                                showlegend=False, title="Institutionals more found in Tools (3050)", title_x=0.5)


# Plot for comparation in tools:
df_comparation = pd.DataFrame(comparation_http_codes.items(), columns=[
    "Comparation", "Count"]).reset_index(drop=True)
fig_comparation = px.bar(df_comparation, x="Count", y="Comparation", log_x=True, color='Comparation',
                         template='simple_white', orientation='h',
                         height=1100,
                         hover_data={'Count': False, 'Comparation': True},
                         hover_name="Count")
fig_comparation.update_layout(yaxis_categoryorder='total ascending', bargap=0.4,
                              showlegend=False, title="Comparation (Andreu vs Operational)", title_x=0.5)


#PLOT FRAMEWORKS JS:
df_js = pd.DataFrame(frameworks_ordered.items(), columns=[
    "Framework", "Count"]).reset_index(drop=True)
fig_js = px.bar(df_js, x="Count", y="Framework", log_x=True, color='Framework',
                         template='simple_white', orientation='h',
                         height=1100,
                         hover_data={'Count': False, 'Framework': True},
                         hover_name="Count")
fig_js.update_layout(yaxis_categoryorder='total ascending', bargap=0.4,
                              showlegend=False, title="Framework JS (" + str(len(df_js)) + ")", title_x=0.5)


# Dash HTML:
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])


app.layout = html.Div(
    id='container_father',
    style={'display': 'flex', 'flex-direction': 'column'},
    children=[
        html.Div(
            style={'width': '60%'},
            children=[
                dcc.Graph(figure=fig_animation,
                          config={"displaylogo": False,
                                  'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
                          )]),


        html.Div(
            className='six columns',
            children=[
                html.Div([
                    html.Label(['Choose Years Interval:'],
                               style={'font-weight': 'bold'}),
                    html.P(),
                    dcc.RangeSlider(
                        id='my-range-slider',  # any name you'd like to give it
                        marks={
                            1980: {'label': '1980', 'style': {'font-weight': 'bold', 'size': '20px'}},
                            1985: '1985',
                            1990: '1990',
                            1995: '1995',
                            2000: '2000',
                            2005:  '2005',
                            2010:  '2010',
                            2015: '2015',
                            2020: {'label': '2020', 'style': {'font-weight': 'bold'}},
                        },
                        step=1,                # number of steps between values
                        min=1980,
                        max=2020,
                        # default value initially chosen
                        value=[1980, 2020],
                        dots=True,             # True, False - insert dots, only when step>1
                        allowCross=False,      # True,False - Manage handle crossover
                        disabled=False,        # True,False - disable handle
                        pushable=2,            # any number, or True with multiple handles
                        updatemode='mouseup',  # 'mouseup', 'drag' - update value method
                        included=True,         # True, False - highlight handle
                        vertical=False,        # True, False - vertical, horizontal slider
                        # hight of slider (pixels) when vertical=True
                        verticalHeight=900,
                        className='None',
                        # tooltip={'always visible': False,  # show current slider values
                        #          'placement': 'bottom'},
                    ),
                ]),

                html.Div(
                    children=[
                        dcc.Graph(id='languages_plot',
                                  figure=fig_languages_all,
                                  config={"displaylogo": False,
                                          'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
                                  )]),



            ]),

        html.Div(
            className='six columns',
            children=[
                dcc.Graph(
                    figure=fig_codes,
                    config={"displaylogo": False,
                            'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
                )]),
        html.Div(
            className='six columns',
            children=[
                dcc.Graph(
                    figure=fig_tags,
                    config={"displaylogo": False,
                            'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
                )]),

        html.Div(
            className='six columns',
            children=[
                dcc.Graph(figure=fig_email,
                          config={"displaylogo": False,
                                  'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
                          )]),

        html.Div(
            style={'width': '60%'},
            children=[
                dcc.Graph(figure=fig_names,
                          config={"displaylogo": False,
                                  'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
                          )]),
        html.Div(
            style={'width': '60%'},
            children=[
                dcc.Graph(figure=fig_institutional,
                          config={"displaylogo": False,
                                  'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
                          )]),


        html.Div(
            className='six columns',
            children=[
                dcc.Graph(
                    figure=fig_js,
                    config={"displaylogo": False,
                            'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
                )])
    ],
)


@app.callback(
    Output('languages_plot', 'figure'),
    [Input('my-range-slider', 'value')]
)
def build_graph(years):
    return create_bar_plot_languages(years)


if __name__ == '__main__':
    app.run_server(debug=True)
