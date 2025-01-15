import os
import json
from pathlib import Path

def merge_result_files(input_dir, output_file):
    """合并指定目录下的所有结果文件"""
    # 初始化合并后的数据结构
    merged_results = {
        "dataset": "aqua",
        "model_id": "gpt-3.5-turbo",
        "alg": "ReAct",
        "model_result": []
    }
    
    # 获取目录下所有json文件
    input_path = Path(input_dir)
    json_files = list(input_path.glob("*.json"))
    
    print(f"Found {len(json_files)} files to merge")
    
    # 读取并合并每个文件
    for file_path in json_files:
        try:
            print(f"Processing {file_path.name}")
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data.get("model_result"):
                    merged_results["model_result"].extend(data["model_result"])
        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")
            continue
    
    # 保存合并后的结果
    print(f"\nTotal results: {len(merged_results['model_result'])}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_results, f, ensure_ascii=False, indent=2)
    
    print(f"Merged results saved to {output_file}")

if __name__ == "__main__":
    # 设置输入输出路径
    input_dir = "/home/li_jingcheng/项目/OmAgent/data/aqua_doubao_pro_promptv1"
    output_file = "/home/li_jingcheng/项目/OmAgent/data/aqua_doubao_pro_promptv1_merged.json"
    
    # 执行合并
    merge_result_files(input_dir, output_file) 