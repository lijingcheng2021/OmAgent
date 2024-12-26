import os
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)

# 配置代理
HTTP_PROXY = os.getenv('HTTP_PROXY', 'http://10.8.21.200:47890')
HTTPS_PROXY = os.getenv('HTTPS_PROXY', 'http://10.8.21.200:47890')
os.environ['HTTP_PROXY'] = HTTP_PROXY
os.environ['HTTPS_PROXY'] = HTTPS_PROXY

from langchain import Wikipedia
from langchain.agents.react.base import DocstoreExplorer


def format_step(step: str) -> str:
    return step.strip('\n').strip().replace('\n', '')


def test_wiki_search(search_term: str) -> str:
    # 初始化 Wikipedia docstore
    docstore = DocstoreExplorer(Wikipedia())
    
    try:
        # 执行搜索
        result = docstore.search(search_term)
        # 格式化结果
        formatted_result = format_step(result)
        return formatted_result
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        raise


if __name__ == "__main__":
    # 示例用法
    search_term = "毛泽东"  # 你可以更改以测试不同的搜索
    result = test_wiki_search(search_term)
    print(f"\nSearch term: {search_term}")
    print(f"Result: {result}")
