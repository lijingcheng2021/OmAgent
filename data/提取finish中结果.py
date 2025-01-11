import json
import re

def extract_finish_content(last_output):
    """从last_output中提取Finish[]中的内容，如果没有Finish则返回原值"""
    if last_output is None:  # 处理 null 值
        return None
    if 'Finish[' in last_output:
        # 使用正则表达式匹配Finish[...]中的内容
        match = re.search(r'Finish\[(.*?)\]', last_output)
        if match:
            return match.group(1)
    return last_output

# 加载结果文件
with open('/home/li_jingcheng/项目/OmAgent/data/aqua_react_pro_doubao_results_part2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    print(f"Loaded file successfully")

# 处理每个样本的last_output
processed = 0
finish_extracted = 0
null_outputs = 0

for item in data['model_result']:
    processed += 1
    
    # 处理last_output
    if 'last_output' in item:
        original_output = item['last_output']
        if original_output is None:
            null_outputs += 1
            continue
            
        item['last_output'] = extract_finish_content(original_output)
        if item['last_output'] != original_output:
            finish_extracted += 1
            print(f"Item {processed}: Extracted '{item['last_output']}' from '{original_output}'")

print(f"\nSummary:")
print(f"Total items processed: {processed}")
print(f"Finish[] contents extracted: {finish_extracted}")
print(f"Null last_outputs found: {null_outputs}")

# 将结果写入新的JSON文件
with open('/home/li_jingcheng/项目/OmAgent/data/aqua_react_pro_doubao_results_part2_finish.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\nProcessing complete. Results written to hotpot_dev_select_500_results_with_id_null_finish.json")
