from pathlib import Path
from omagent_core.utils.container import container

CURRENT_PATH = Path(__file__).parents[0]

# 加载 container 配置从 YAML 文件
container.register_stm("RedisSTM")
container.from_config(CURRENT_PATH.joinpath('container.yaml'))

# 编译配置
container.compile() 