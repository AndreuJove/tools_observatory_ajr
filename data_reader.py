

# """

# Homepages -> Acces

# """

# # EXTRACT HTTP CODES AND EXCEPTIONS:
# path_json = "input_data/stats.json"
# with open(path_json, "r") as fp:
#     codes_and_exceptions = json.load(fp)

# # EXTRACT PROBLEMATIC URLS:
# path_problematic_url = "input_data/problematic_tools.json"
# with open(path_problematic_url, "r") as fp:
#     data_problematic = json.load(fp)

# # Extract two arrays from the problematic extensions and his respective count:
# def extract_problematic_extensions_from_json_file(data_problematic):
#     problematics_extensions = ['.bz2', 'ftp://', '.pdf', '.zip', '.gz']
#     problematic_extensions_count = [0]*len(problematics_extensions)
#     for t in data_problematic:
#         for problem in problematics_extensions:
#             if t['first_url_tool'].endswith(problem) or t['first_url_tool'].startswith(problem):
#                 problematic_extensions_count[problematics_extensions.index(problem)] += 1
#     d = {'Extensions':problematics_extensions,'Count':problematic_extensions_count}
#     df_extensions = pd.DataFrame(d, columns = ['Extensions','Count'])
#     return df_extensions

# # Extract the the arrays of the HTTP codes and exceptions and their respectives counts:
# def extract_http_codes_and_exceptions_from_json_file(data):
#     http_codes_scrapy, exceptions_scrapy = ({} for i in range(2))
#     for t in data:
#         for a in t.items():
#             if a[0].startswith("downloader/response_status_count"):
#                 http_codes_scrapy[a[0].split("/")[-1]] = a[1]
#             elif a[0].startswith("downloader/exception_type_count"):
#                 exceptions_scrapy[a[0].split(".")[-1]] = a[1]
#     df_codes = pd.DataFrame(list(http_codes_scrapy.items()),columns = ['HTTP Codes','Count']) 
#     df_exceptions = pd.DataFrame(list(exceptions_scrapy.items()),columns = ['Exceptions','Count'])
#     return df_codes, df_exceptions

# df_codes, df_exceptions = extract_http_codes_and_exceptions_from_json_file(codes_and_exceptions)
# df_extensions = extract_problematic_extensions_from_json_file(data_problematic)
"""

Homepages -> JavaScript

# """

# # Extract dynamic percentages:
# path_all_dynamic_percentages = "../websites_analysis/output_data/all_dynamic_percentages.json"
# with open(path_all_dynamic_percentages, "r") as fp:
#     total_dynamic_percentages = json.load(fp)

# percentages = [y["dynamic_percentages"]
#                for y in total_dynamic_percentages if "dynamic_percentages" in y][0]

# def get_the_count_of_one_domain(domain):
#     #The count of domains of the available websites:
#     path_to_domains_count = "../websites_analysis/output_data/domains_count_satisfactory_websites.json"
#     with open(path_to_domains_count, "r") as l:
#         domains_count = json.load(l)
#     index_domain = domains_count[0]['Domain'].index(domain)
#     return domains_count[1]['Count'][index_domain]

# #Extract percentages of change of primary classification:
# path_groupation_dynamic_percentages = "../websites_analysis/output_data/dynamic_percentages_domains.json"
# with open(path_groupation_dynamic_percentages, "r") as fp:
#     dynamic_percentages_groupation = json.load(fp)


# #Extract each number of percentages of the classification (universities, generic):
# def extract_number_of_domains(index, name):
#     final_list = []
#     for t in dynamic_percentages_groupation[0]['dynamic_percentages'][index][name]:
#         for a in list(t.values())[0]:
#             final_list.append(a)
#     return final_list


