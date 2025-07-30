# get logger
简化 logging 配置，统一格式

## 示例
```python
from lzhgetlogger import get_logger, get_file_logger

logger1 = get_logger(level = logging.INFO, name = "logger1")  # 定义一个普通`logger`
logger2 = get_logger(level = logging.INFO)  # 如果未指定`name`，则会生成一个`uuid`给`name`
logger3 = get_file_logger(filename="log.csv", level = logging.INFO, name = "logger3")  # 定义一个文件`logger`

logger1.info("log from logger1")
logger2.info("log from logger2")
logger3.info("log from logger3")
```

## 安装 - [PyPI](https://pypi.org/project/lzhgetlogger/)
```shell
pip install lzhgetlogger
```
