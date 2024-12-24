from omagent_core.utils.container import container
from pathlib import Path
from omagent_core.utils.registry import registry

CURRENT_PATH = Path(__file__).parents[0]
registry.import_module()

container.register_callback(callback='AppCallback')
container.register_input(input='AppInput')
container.register_stm("RedisSTM")
container.compile_config(CURRENT_PATH) 