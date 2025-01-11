import json

def analyze_empty_ids(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # 初始化计数器
    empty_id_count = 0
    total_items = 0
    empty_id_items = []
    
    # 遍历所有结果
    for i, item in enumerate(data['model_result']):
        total_items += 1
        if item.get('id') == "":  # 检查 id 是否为空字符串
            empty_id_count += 1
            # 保存问题预览
            question = item.get('question', 'No question')
            question_preview = question[:100] + '...' if question else 'No question'
            empty_id_items.append((i, question_preview))
    
    # 打印统计信息
    print(f"Items with empty ID (\"\")： {empty_id_count}")
    print(f"Total items: {total_items}")
    print(f"Percentage of empty IDs: {(empty_id_count/total_items)*100:.1f}%")
    
    # 打印空ID项的详细信息
    print("\nItems with empty IDs:")
    for index, preview in empty_id_items:
        print(f"\nIndex {index}:")
        print(f"Question: {preview}")

if __name__ == "__main__":
    file_path = "/home/li_jingcheng/项目/OmAgent/data/gsm8k_all_react_results.json"
    analyze_empty_ids(file_path)