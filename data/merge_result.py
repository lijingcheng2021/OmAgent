import json

def merge_gsm8k_results(file_paths):
    # Initialize with the structure from first file
    merged_data = {
        "dataset": "gsm8k",
        "model_id": "gpt-3.5-turbo", 
        "alg": "ReAct-Basic",
        "model_result": []
    }
    
    # Read and merge each file
    for file_path in file_paths:
        with open(file_path) as f:
            data = json.load(f)
            merged_data["model_result"].extend(data["model_result"])
            
    # Write merged results
    with open("/home/li_jingcheng/项目/OmAgent/data/merged_gsm8k_results.json", "w") as f:
        json.dump(merged_data, f, indent=2)

# Example usage
file_paths = [
    "/home/li_jingcheng/项目/OmAgent/data/gsm8k_react_basic_results_part1.json",
    "/home/li_jingcheng/项目/OmAgent/data/gsm8k_react_basic_results_part2.json",
    "/home/li_jingcheng/项目/OmAgent/data/gsm8k_react_basic_results_part3.json",
    "/home/li_jingcheng/项目/OmAgent/data/gsm8k_react_basic_results_part4.json",
    "/home/li_jingcheng/项目/OmAgent/data/gsm8k_react_basic_results_part5.json",
    "/home/li_jingcheng/项目/OmAgent/data/gsm8k_react_basic_results_part6.json",
    "/home/li_jingcheng/项目/OmAgent/data/gsm8k_react_basic_results_part7.json",
    "/home/li_jingcheng/项目/OmAgent/data/gsm8k_react_basic_results_part8.json",
    "/home/li_jingcheng/项目/OmAgent/data/gsm8k_react_basic_results_part9.json",
    "/home/li_jingcheng/项目/OmAgent/data/gsm8k_react_basic_results_part10.json"
]
merge_gsm8k_results(file_paths)