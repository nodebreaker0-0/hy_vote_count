import json

input_file = '/data/out.json'  
output_file = '/data/out_parse.json'  
key_to_extract = 'c_staking'  

def find_key_with_subtree(data, target_key):
    results = []

    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                results.append({key: value})
            elif isinstance(value, (dict, list)):
                results.extend(find_key_with_subtree(value, target_key))

    elif isinstance(data, list):
        for item in data:
            results.extend(find_key_with_subtree(item, target_key))

    return results


with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

found_values = find_key_with_subtree(data, key_to_extract)


with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(found_values, file, ensure_ascii=False, indent=4)

print(f"'{key_to_extract}' > {output_file}")