import json

def load_test_ids(test_file):
    test_ids = {}
    test_count = 0
    with open(test_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data = json.loads(line)
                test_ids[data['question']] = data['id']
                test_count += 1
    return test_ids, test_count

def check_id_alignment(react_file, test_file):
    # 加载测试文件中的ID
    test_ids, test_count = load_test_ids(test_file)
    
    # 加载修复后的文件
    with open(react_file, 'r', encoding='utf-8') as f:
        react_data = json.load(f)
    
    mismatches = []
    null_entries = []
    react_questions = set()
    react_count = len(react_data['model_result'])
    valid_count = 0
    null_count = 0
    
    # 检查每个条目
    for item in react_data['model_result']:
        if item['question'] is None:
            null_count += 1
            null_entries.append({'query': None, 'id': str(item['id'])})
        else:
            valid_count += 1
            react_questions.add(item['question'])
            if item['question'] in test_ids:
                if str(item['id']) != str(test_ids[item['question']]):
                    mismatches.append({
                        'query': item['question'],
                        'id': str(test_ids[item['question']])
                    })
    
    # 找出缺失的问题
    missing_questions = [{'query': q, 'id': str(id)} for q, id in test_ids.items() if q not in react_questions]
    
    return mismatches, null_entries, react_count, test_count, valid_count, null_count, missing_questions

if __name__ == "__main__":
    react_file = "/home/li_jingcheng/项目/OmAgent/data/hotpot_dev_select_500_data_test_0107_part5.json"
    test_file = "/home/li_jingcheng/项目/OmAgent/data/hotpot_dev_select_500_data_test_0107.jsonl"
    
    mismatches, null_entries, react_count, test_count, valid_count, null_count, missing_questions = check_id_alignment(react_file, test_file)
    
    print(f"React file total items: {react_count}")
    print(f"- Valid entries: {valid_count}")
    print(f"- Null entries: {null_count}")
    print(f"Test file items: {test_count}")
    print(f"Number of mismatches found: {len(mismatches)}")
    print(f"Number of missing questions: {len(missing_questions)}")
    
    if null_entries:
        print("\nNull entries:")
        print(json.dumps(null_entries, indent=2))
    
    if mismatches:
        print("\nMismatched entries:")
        print(json.dumps(mismatches, indent=2))
    
    if missing_questions:
        print("\nMissing questions:")
        print(json.dumps(missing_questions, indent=2))
