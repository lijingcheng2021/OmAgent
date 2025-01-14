import os
import math
import time
import signal
from functools import partial
# 设置代理环境变量
os.environ['HTTP_PROXY'] = 'http://10.8.21.200:47890'
os.environ['HTTPS_PROXY'] = 'http://10.8.21.200:47890'

from omagent_core.utils.container import container
from omagent_core.engine.workflow.conductor_workflow import ConductorWorkflow
from pathlib import Path
from omagent_core.utils.registry import registry
from omagent_core.clients.devices.programmatic.client import ProgrammaticClient
from omagent_core.utils.logger import logging
from omagent_core.advanced_components.workflow.react_pro.workflow import ReactProWorkflow
import json

def read_input_texts(file_path):
    """从 jsonl 文件读取问题"""
    input_texts = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():  # 跳过空行
                data = json.loads(line)
                input_texts.append((data['question'], str(data['id'])))
    return input_texts

def split_input_data(input_texts, num_splits):
    """将输入数据切分成n份"""
    total_items = len(input_texts)
    items_per_split = math.ceil(total_items / num_splits)
    
    splits = []
    for i in range(num_splits):
        start_idx = i * items_per_split
        end_idx = min((i + 1) * items_per_split, total_items)
        splits.append(input_texts[start_idx:end_idx])
    
    return splits

def process_results(results, dataset_name="aqua"):
    """将结果转换为标准格式"""
    formatted_output = {
        "dataset": dataset_name,
        "model_id": "gpt-3.5-turbo",
        "alg": "ReAct",
        "model_result": []
    }
    
    for result in results:
        # Skip None results or invalid entries
        if result is None:
            print("Warning: Skipping None result")
            continue
            
        try:
            output_data = result.get('output', {})
            
            model_result = {
                "id": output_data.get('id'),
                "question": output_data.get('query'),
                "body": output_data.get('body', {}),
                "last_output": output_data.get('output', ''),
                "ground_truth": "",
                "step_number": output_data.get('step_number', 0),
                "prompt_tokens": output_data.get('token_usage', {}).get('prompt_tokens', 0),
                "completion_tokens": output_data.get('token_usage', {}).get('completion_tokens', 0)
            }
            
            formatted_output["model_result"].append(model_result)
        except Exception as e:
            print(f"Warning: Error processing result: {e}")
            continue
    
    return formatted_output



# 设置参数
input_file = "/home/li_jingcheng/项目/OmAgent/data/aqua_test_processed.jsonl"
num_splits = 100  # 设置要切分的份数

# 创建输出目录
output_dir = "/home/li_jingcheng/项目/OmAgent/data/aqua_gpt4o_pro_promptv1"
os.makedirs(output_dir, exist_ok=True)

# 读取并切分输入数据
input_texts = read_input_texts(input_file)
data_splits = split_input_data(input_texts, num_splits)


# programmatic_client = ProgrammaticClient(
#     processor=workflow,
#     config_path=config_path,
#     workers=[]  # React workflow 不需要额外的 workers
# )

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Processing took too long!")


for j in range(10):
# 按顺序处理每一份数据
    for i, split_data in enumerate(data_splits, 1):
        try:
            print(f"\nProcessing split {i}/{num_splits}...")
            if i in []:
                continue

            # 检查已处理的文件
            output_file = os.path.join(output_dir, f"aqua_gpt4o_pro_promptv1_part{i}.json")
            if os.path.exists(output_file):
                with open(output_file, 'r', encoding='utf-8') as f:
                    formatted_results = json.load(f)
                if len(formatted_results["model_result"]) > 10:
                    print(f"Split {i} already processed, skipping...")
                    continue    

            logging.init_logger("omagent", "omagent", level="INFO")

            # 设置当前工作目录路径
            CURRENT_PATH = Path(__file__).parents[0]

            # 导入注册的模块
            registry.import_module(CURRENT_PATH.joinpath('agent'))

            # 加载 container 配置从 YAML 文件
            container.register_stm("RedisSTM")
            container.from_config(CURRENT_PATH.joinpath('container.yaml'))

            # 初始化工作流
            workflow = ConductorWorkflow(name='react_pro_example')

            # 配置 React 工作流
            react_workflow = ReactProWorkflow()
            react_workflow.set_input(
                query=workflow.input('query'),
                id=workflow.input('id')
            )

            # 配置工作流执行流程
            workflow >> react_workflow 

            # 初始化 programmatic client
            config_path = CURRENT_PATH.joinpath('configs')

            # 注册工作流
            workflow.register(overwrite=True)
            programmatic_client = ProgrammaticClient(
                processor=workflow,
                config_path=config_path,
                workers=[]
            )
            
            # 准备输入数据
            workflow_input_list = [
                {"query": text[0], "id": text[1]} for text in split_data
            ]
            
            print(f"Processing {len(workflow_input_list)} queries in this split...")
            
            # 设置超时信号处理
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(350)  # 设置10分钟超时
            
            try:
                # 处理数据
                res = programmatic_client.start_batch_processor(
                    workflow_input_list=workflow_input_list
                )
                
                # 处理结果
                formatted_results = process_results(res, dataset_name="aqua")
                
                # 关闭超时警报
                signal.alarm(0)
                
            except TimeoutError:
                print(f"Processing split {i} timed out after 10 minutes, skipping...")
                programmatic_client.stop_processor()
                time.sleep(10)
                continue
            except Exception as e:
                print(f"Error during processing: {e}")
                programmatic_client.stop_processor()
                time.sleep(10)
                continue
            finally:
                # 确保关闭超时警报
                signal.alarm(0)

            if not formatted_results["model_result"]:
                print(f"No results for split {i}, skipping...")
                programmatic_client.stop_processor()
                time.sleep(10)
                continue    
            
            # 保存结果到文件
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(formatted_results, f, ensure_ascii=False, indent=2)
            
            print(f"Results for split {i} saved to {output_file}")

            programmatic_client.stop_processor()
            time.sleep(10)

        except Exception as e:
            print(f"Error processing split {i}: {e}")
            time.sleep(30)  # 错误后等待更长时间
            continue

print("\nAll splits processed successfully!")