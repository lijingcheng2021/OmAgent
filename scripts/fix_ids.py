import json
import re

def extract_finish_content(text):
    """从文本中提取 Finish[] 中的内容"""
    if not text:
        return ""
    
    # 使用正则表达式匹配 Finish[内容]
    match = re.search(r'Finish\[(.*?)\]', text)
    if match:
        return match.group(1)  # 返回括号中的内容
    return ""

def load_test_data(file_path):
    question_map = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data = json.loads(line)
                question_map[data['question']] = {
                    'id': data['id'],
                    #'answer': data['answer']
                }
    return question_map

def get_default_body(question):
    return {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": ""
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Solve a question-answering task using alternating Thought, Action, and Observation steps:\n\n- Thought: Reason about the current situation.\n- Action: Can be one of these three types:\n  1. Search[entity]: Search for the specified entity online. If it exists, return its first paragraph; if not, return some similar entities for further search.\n  2. Lookup[keyword]: From the last successfully found paragraph through Search, return the next sentence containing the specified keyword.\n  3. Finish[answer]: Return the final answer and end the task.\n\n- You can take as many steps as needed.\n\nHere are some examples:\n\nQuestion: What is the elevation range of the region where the Colorado orogeny extends to in its eastern area?\nThought 1: I need to search for the Colorado orogeny to find where it extends in its eastern area and then find the elevation range of that region.\nAction 1: Search[Colorado orogeny]\nObservation 1: The Colorado orogeny was an orogenic event in Colorado and surrounding areas.\nThought 2: It doesn't mention the eastern area. I need to look up \"eastern area\".\nAction 2: Lookup[eastern area]\nObservation 2: (Result 1/1) The eastern area extends into the High Plains region and is known as the Central Plains orogeny.\nThought 3: The Colorado orogeny's eastern area extends into the High Plains region. So I need to search for \"High Plains\" to find its elevation range.\nAction 3: Search[High Plains]\nObservation 3: The High Plains refers to one of two distinct landform regions.\nThought 4: I need to search specifically for \"High Plains (United States)\".\nAction 4: Search[High Plains (United States)]\nObservation 4: The High Plains is a subregion of the Great Plains. From east to west, the High Plains rises in elevation from around 1,800 to 7,000 feet (550 to 2,130 m).\nThought 5: The High Plains region has an elevation range from 1,800 to 7,000 feet.\nAction 5: Finish[1,800 to 7,000 feet]\n\nQuestion: Which president was the Simpsons character Milhouse named after, according to songwriter and satirist Allie Goertz who wrote a song about him?\nThought 1: I need to search for Milhouse and find out who he was named after.\nAction 1: Search[Milhouse]\nObservation 1: Milhouse Mussolini Van Houten is a recurring character in the Fox animated television series The Simpsons, voiced by Pamela Hayden and created by Matt Groening.\nThought 2: The paragraph doesn't mention who he was named after. Let me look up \"named after\".\nAction 2: Lookup[named after]\nObservation 2: (Result 1/1) Milhouse was named after U.S. President Richard Nixon, whose middle name was Milhous.\nThought 3: Milhouse was named after Richard Nixon.\nAction 3: Finish[Richard Nixon]\n\nQuestion: Which documentary is about a Finnish rock band, \"Adam Clayton Powell\" or \"Saimaa Gesture\"?\nThought 1: I need to search for both \"Adam Clayton Powell\" and \"Saimaa Gesture\" to find which one is about a Finnish rock band.\nAction 1: Search[Adam Clayton Powell]\nObservation 1: No results for [Adam Clayton Powell]. Similar results: [\"Adam Clayton Powell III\", \"Seventh Avenue (Manhattan)\", \"Adam Clayton Powell Jr. State Office Building\", \"Isabel Washington Powell\", \"Adam Powell\", \"Adam Clayton Powell (film)\", \"Giancarlo Esposito\"].\nThought 2: Let me search for \"Adam Clayton Powell (film)\" to find the documentary.\nAction 2: Search[Adam Clayton Powell (film)]\nObservation 2: \"Adam Clayton Powell\" is a 1989 American documentary film directed by Richard Kilberg. The film chronicles the rise and fall of African-American politician Adam Clayton Powell Jr. It later aired as part of the PBS series American Experience.\nThought 3: \"Adam Clayton Powell\" is a documentary about an African-American politician, not a Finnish rock band. Therefore, \"Saimaa Gesture\" must be the documentary about a Finnish rock band.\nAction 3: Finish[\"Saimaa Gesture\"]\n\n(Examples end)\n\nQuestion: " + question
                    }
                ]
            }
        ],
        "temperature": 0.0,
        "max_tokens": 2048
    }

def fix_missing_data(react_file, test_file, output_file):
    question_map = load_test_data(test_file)
    
    with open(react_file, 'r', encoding='utf-8') as f:
        react_data = json.load(f)
    
    fixed_ids = 0
    fixed_bodies = 0
    fixed_outputs = 0
    total_count = 0
    
    for item in react_data['model_result']:
        total_count += 1
        question = item['question']
        
        if question in question_map:
            # 修复缺失的ID
            if not item['id']:
                item['id'] = str(question_map[question]['id'])
                fixed_ids += 1
            
            # 修复缺失的body
            body = item.get('body')
            if body is None or (isinstance(body, str) and body.strip() == '') or (isinstance(body, dict) and not body):
                item['body'] = get_default_body(question)
                fixed_bodies += 1
            
            #处理 last_output
            if 'last_output' in item:
                original_output = item['last_output']
                new_output = extract_finish_content(original_output)
                if original_output != new_output:
                    item['last_output'] = new_output
                    fixed_outputs += 1
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(react_data, f, indent=2, ensure_ascii=False)
    
    return fixed_ids, fixed_bodies, fixed_outputs, total_count

if __name__ == "__main__":
    react_file = "/home/li_jingcheng/项目/OmAgent/data/aqua_gpt4o_pro_promptv1_merged.json"
    test_file = "/home/li_jingcheng/项目/OmAgent/data/aqua_test_processed.jsonl"
    output_file = "/home/li_jingcheng/项目/OmAgent/data/aqua_gpt4o_pro_promptv1_merged_finish.json"
    
    fixed_ids, fixed_bodies, fixed_outputs, total_count = fix_missing_data(react_file, test_file, output_file)
    print(f"Total items processed: {total_count}")
    print(f"IDs fixed: {fixed_ids}")
    print(f"Bodies fixed: {fixed_bodies}")
    print(f"Outputs fixed: {fixed_outputs}")
    print(f"Fixed file saved to: {output_file}")