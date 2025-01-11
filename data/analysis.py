import json

def analyze_ids(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        
    # 初始化计数器和列表
    id_count = 0
    total_items = 0
    missing_ids = []
    
    # 遍历所有结果
    for i, item in enumerate(data['model_result']):
        total_items += 1
        if not item.get('id'):  # 如果 id 为空
            # 安全地获取问题预览
            question = item.get('question')
            if question:
                question_preview = question[:50] + '...'
            else:
                question_preview = 'No question'
            missing_ids.append((i, question_preview))
        else:
            id_count += 1
            
    # 打印统计信息
    print(f"Items with IDs: {id_count}")
    print(f"Total items: {total_items}")
    print(f"Percentage with IDs: {(id_count/total_items)*100:.1f}%")
    
    # 打印缺失ID的详细信息
    print("\nMissing IDs in following items:")
    for index, preview in missing_ids:
        print(f"Index {index}: {preview}")

# 使用脚本
file_path = 'data/gsm8k_all_react_results.json'
analyze_ids(file_path)
