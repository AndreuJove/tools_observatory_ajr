import json
import pandas as pd

# Return a list of the value of a key in a list of dictionaries.
def extract_value_from_list_of_dicts(list_dicts, key):
    return [y[key] for y in list_dicts if key in y][0]

"""

Homepages -> Domains and metrics

"""

# Open file of all bisochemas ssl https numbers by domains classification:
path_bioschemas_ssl_https = "input_data/bioschemas_ssl_https_license_by_classification.json"
with open(path_bioschemas_ssl_https, "r") as l:
    metrics_bioschemas_ssl_https_by_classification = json.load(l)

# Open file of all http codes by classification domains:
http_codes_by_classification = "input_data/http_codes_by_classification.json"
with open(http_codes_by_classification, "r") as l:
    http_codes_by_classification = json.load(l)

# Extract the domains and his respective count from json and save in 2 different lists.
path_to_domains_count = "input_data/count_domains_tools_unique_url.json"
with open(path_to_domains_count, "r") as l:
    domains_count = json.load(l)
domains =domains_count[0]["Domain"]
values_36 = domains_count[1]["Count"]

# Extract the primary classification from json.
path_to_primary_classification = "input_data/primary_classification_domains.json"
with open(path_to_primary_classification, "r") as p:
    primary_classification = json.load(p)
university = extract_value_from_list_of_dicts(
    primary_classification, 'university')
institucional = extract_value_from_list_of_dicts(
    primary_classification, 'institucional')
lifeScience = extract_value_from_list_of_dicts(
    primary_classification, 'lifeScience')
collections = extract_value_from_list_of_dicts(
    primary_classification, 'collections')
generic = extract_value_from_list_of_dicts(primary_classification, 'generic')

#Get initial values from the results for the pie charts plots for the domains tab:
def get_initial_values_for_update():
    all_http_codes = {
        'university': metrics_bioschemas_ssl_https_by_classification[0]["university"]["https"],
        'institucional': metrics_bioschemas_ssl_https_by_classification[1]["institucional"]["https"],
        'lifeScience': metrics_bioschemas_ssl_https_by_classification[2]["lifeScience"]["https"],
        'collections': metrics_bioschemas_ssl_https_by_classification[3]["collections"]["https"],
        'generic': metrics_bioschemas_ssl_https_by_classification[4]["generic"]["https"],
        'others': metrics_bioschemas_ssl_https_by_classification[5]["others"]["https"],
    }
    all_ssl_results = {
        'university': metrics_bioschemas_ssl_https_by_classification[0]["university"]["ssl"],
        'institucional': metrics_bioschemas_ssl_https_by_classification[1]["institucional"]["ssl"],
        'lifeScience': metrics_bioschemas_ssl_https_by_classification[2]["lifeScience"]["ssl"],
        'collections': metrics_bioschemas_ssl_https_by_classification[3]["collections"]["ssl"],
        'generic': metrics_bioschemas_ssl_https_by_classification[4]["generic"]["ssl"],
        'others': metrics_bioschemas_ssl_https_by_classification[5]["others"]["ssl"]
    }
    all_bioschema_results = {
        'university': metrics_bioschemas_ssl_https_by_classification[0]["university"]["bioschemas"],
        'institucional': metrics_bioschemas_ssl_https_by_classification[1]["institucional"]["bioschemas"],
        'lifeScience': metrics_bioschemas_ssl_https_by_classification[2]["lifeScience"]["bioschemas"],
        'collections': metrics_bioschemas_ssl_https_by_classification[3]["collections"]["bioschemas"],
        'generic': metrics_bioschemas_ssl_https_by_classification[4]["generic"]["bioschemas"],
        'others': metrics_bioschemas_ssl_https_by_classification[5]["others"]["bioschemas"]
    }
    all_http_codes_for_hist = {
        'university': http_codes_by_classification[0]["university"],
        'institucional': http_codes_by_classification[1]["institucional"],
        'lifeScience': http_codes_by_classification[2]["lifeScience"],
        'collections': http_codes_by_classification[3]["collections"],
        'generic': http_codes_by_classification[4]["generic"],
        'others': http_codes_by_classification[5]["others"],
    }
    all_http_codes_for_hist = {
        'university': http_codes_by_classification[0]["university"],
        'institucional': http_codes_by_classification[1]["institucional"],
        'lifeScience': http_codes_by_classification[2]["lifeScience"],
        'collections': http_codes_by_classification[3]["collections"],
        'generic': http_codes_by_classification[4]["generic"],
        'others': http_codes_by_classification[5]["others"],
    }
    return all_http_codes, all_ssl_results, all_bioschema_results, all_http_codes_for_hist, all_http_codes_for_hist


"""

Homepages -> Acces

"""
# EXTRACT HTTP CODES AND EXCEPTIONS:
path_json = "input_data/stats.json"
with open(path_json, "r") as fp:
    codes_and_exceptions = json.load(fp)

# EXTRACT PROBLEMATIC URLS:
path_problematic_url = "input_data/problematic_tools.json"
with open(path_problematic_url, "r") as fp:
    data_problematic = json.load(fp)

#Extract two arrays from the problematic extensions and his respective count:
def extract_problematic_extensions_from_json_file(data_problematic):
    problematics_extensions = ['.bz2', 'ftp://', '.pdf', '.zip', '.gz']
    problematic_extensions_count = [0]*len(problematics_extensions)
    for t in data_problematic:
        for problem in problematics_extensions:
            if t['first_url_tool'].endswith(problem) or t['first_url_tool'].startswith(problem):
                problematic_extensions_count[problematics_extensions.index(problem)] += 1
    d = {'Extensions':problematics_extensions,'Count':problematic_extensions_count}
    df_extensions = pd.DataFrame(d, columns = ['Extensions','Count'])
    return df_extensions

#Extract the the arrays of the HTTP codes and exceptions and their respectives counts:
def extract_http_codes_and_exceptions_from_json_file(data):
    http_codes_scrapy, exceptions_scrapy = ({} for i in range(2))
    for t in data:
        for a in t.items():
            if a[0].startswith("downloader/response_status_count"):
                http_codes_scrapy[a[0].split("/")[-1]] = a[1]
            elif a[0].startswith("downloader/exception_type_count"):
                exceptions_scrapy[a[0].split(".")[-1]] = a[1]
    df_codes = pd.DataFrame(list(http_codes_scrapy.items()),columns = ['HTTP Codes','Count']) 
    df_exceptions = pd.DataFrame(list(exceptions_scrapy.items()),columns = ['Exceptions','Count'])
    return df_codes, df_exceptions

df_codes, df_exceptions = extract_http_codes_and_exceptions_from_json_file(codes_and_exceptions)
df_extensions = extract_problematic_extensions_from_json_file(data_problematic)

"""

Homepages -> JavaScript

"""

# Extract dynamic percentages:
path_all_dynamic_percentages = "../websites_analysis/output_data/all_dynamic_percentages.json"
with open(path_all_dynamic_percentages, "r") as fp:
    total_dynamic_percentages = json.load(fp)

percentages = [y["dynamic_percentages"]
               for y in total_dynamic_percentages if "dynamic_percentages" in y][0]

def get_the_count_of_one_domain(domain):
    #The count of domains of the available websites:
    path_to_domains_count = "../websites_analysis/output_data/domains_count_satisfactory_websites.json"
    with open(path_to_domains_count, "r") as l:
        domains_count = json.load(l)
    index_domain = domains_count[0]['Domain'].index(domain)
    return domains_count[1]['Count'][index_domain]

#Extract percentages of change of primary classification:
path_groupation_dynamic_percentages = "../websites_analysis/output_data/dynamic_percentages_domains.json"
with open(path_groupation_dynamic_percentages, "r") as fp:
    dynamic_percentages_groupation = json.load(fp)


#Extract each number of percentages of the classification (universities, generic):
def extract_number_of_domains(index, name):
    final_list = []
    for t in dynamic_percentages_groupation[0]['dynamic_percentages'][index][name]:
        for a in list(t.values())[0]:
            final_list.append(a)
    return final_list



"""
New homepages -> JavaScript!

"""


metrics = "../api_extraction/output_data/metrics_api_v.json"
with open(metrics, "r") as fp:
    metrics = json.load(fp)

df_total_percentages = pd.read_json("new_input_data/final_df_years_percentages.json")