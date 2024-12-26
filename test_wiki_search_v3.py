import os
import json
import logging
from typing import Optional, Dict
from functools import lru_cache
from pathlib import Path
import time
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wiki_search.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WikiSearchConfig:
    def __init__(self):
        # 从环境变量获取代理设置，如果没有则使用默认值
        self.http_proxy = os.getenv('HTTP_PROXY', 'http://10.8.21.200:47890')
        self.https_proxy = os.getenv('HTTPS_PROXY', 'http://10.8.21.200:47890')
        self.cache_dir = Path('wiki_cache')
        self.max_retries = 3
        self.retry_delay = 1  # seconds

    def setup_proxy(self):
        """设置代理环境变量"""
        os.environ['HTTP_PROXY'] = self.http_proxy
        os.environ['HTTPS_PROXY'] = self.https_proxy

class WikiSearcher:
    def __init__(self, config: WikiSearchConfig = None):
        self.config = config or WikiSearchConfig()
        self.config.setup_proxy()
        
        # 确保缓存目录存在
        self.config.cache_dir.mkdir(exist_ok=True)
        
        try:
            from langchain import Wikipedia
            from langchain.agents.react.base import DocstoreExplorer
            self.docstore = DocstoreExplorer(Wikipedia())
        except ImportError as e:
            logger.error(f"Failed to import required modules: {e}")
            raise

    def _get_cache_path(self, search_term: str) -> Path:
        """获取缓存文件路径"""
        return self.config.cache_dir / f"{hash(search_term)}.json"

    def _read_cache(self, search_term: str) -> Optional[Dict]:
        """从缓存中读取搜索结果"""
        cache_path = self._get_cache_path(search_term)
        if cache_path.exists():
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                logger.info(f"Cache hit for search term: {search_term}")
                return cache_data
            except Exception as e:
                logger.warning(f"Failed to read cache: {e}")
        return None

    def _write_cache(self, search_term: str, result: str):
        """将搜索结果写入缓存"""
        cache_path = self._get_cache_path(search_term)
        try:
            cache_data = {
                'search_term': search_term,
                'result': result,
                'timestamp': time.time()
            }
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            logger.info(f"Cached result for search term: {search_term}")
        except Exception as e:
            logger.warning(f"Failed to write cache: {e}")

    @staticmethod
    def format_step(step: str) -> str:
        """格式化搜索结果"""
        return step.strip('\n').strip().replace('\n', '')

    def search(self, search_term: str, use_cache: bool = True) -> str:
        """
        执行维基百科搜索
        
        Args:
            search_term: 搜索关键词
            use_cache: 是否使用缓存
        
        Returns:
            str: 搜索结果
        """
        if not search_term:
            raise ValueError("Search term cannot be empty")

        # 检查缓存
        if use_cache:
            cached_result = self._read_cache(search_term)
            if cached_result:
                return cached_result['result']

        # 执行搜索，带重试机制
        for attempt in range(self.config.max_retries):
            try:
                result = self.docstore.search(search_term)
                formatted_result = self.format_step(result)
                
                # 缓存结果
                if use_cache:
                    self._write_cache(search_term, formatted_result)
                
                return formatted_result

            except Exception as e:
                logger.error(f"Search attempt {attempt + 1} failed: {e}")
                if attempt < self.config.max_retries - 1:
                    time.sleep(self.config.retry_delay)
                else:
                    raise RuntimeError(f"Failed to search after {self.config.max_retries} attempts") from e

def main():
    try:
        # 创建 WikiSearcher 实例
        searcher = WikiSearcher()
        
        # 示例搜索
        search_term = "毛泽东"
        logger.info(f"Searching for: {search_term}")
        
        result = searcher.search(search_term)
        print(f"\nSearch term: {search_term}")
        print(f"Result: {result}")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()
