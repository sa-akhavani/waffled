import ast
import sys
# Output Format:
# {
#   "request-id": "",
#   "raw_request": b'',
#   "mutation-string": "",
#   "affected-wafs: "",
#   "seed": treqs_results_filename,
#   "category" : None,
# }

treqs_results_filename = sys.argv[1]
parsed_id_and_requests_and_mutations = treqs_results_filename + '_id_and_reqs_and_mutations'
parsed_id_and_wafs_list = treqs_results_filename + '_id_and_wafs_list'

# read parsed_id_and_requests_and_mutations
bypassed_requests_dict = {}
with open(parsed_id_and_requests_and_mutations, 'r') as f:
    for line in f:
        request_id, raw_request_string_rep , mutation_string = line.strip().split('  ||  ')
        raw_request_byte_string = ast.literal_eval(raw_request_string_rep)
        bypassed_requests_dict[request_id] = {
            "request-id": request_id,
            "raw_request_byte_string": raw_request_byte_string,
            "mutation-string": mutation_string,
            "affected-wafs": "",
            "seed": treqs_results_filename,
            "category": None,
        }

# read parsed_id_and_wafs_list and merge id_and_requests_and_mutations and id_and_wafs_list
id_and_wafs_list = {}
with open(parsed_id_and_wafs_list, 'r') as f:
    for line in f:
        parsed = line.strip().split(', ')
        request_id = parsed[0]
        wafs = parsed[1:]
        bypassed_requests_dict[request_id]["affected-wafs"] = wafs

for bypassed_request in bypassed_requests_dict.values():
    print(bypassed_request)

# write the final parsed results to a json file
# with open(treqs_results_filename + '.json', 'w') as f:
#     for bypassed_request in bypassed_requests_dict.values():
#         f.write(str(bypassed_request) + '\n')

