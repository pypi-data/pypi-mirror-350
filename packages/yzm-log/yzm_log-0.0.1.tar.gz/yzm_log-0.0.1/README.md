# yzm_log

> **`Print and save a simple log to a file`**

This is a simple log package. You can see
[Github-yzm_log](https://github.com/YuZhengM/yzm_log)
[PyPI-yzm_log](https://pypi.org/project/yzm_log/)

> upload

```shell
py -m build
twine check dist/*
twine upload dist/*
```

## Use

> install

```shell
pip install yzm_log
```

> use

```python
# -*- coding: utf-8 -*-

from yzm_log import Logger

log = Logger("name", "log")

if __name__ == '__main__':
    print("run...")
    log.debug("info......")
    log.info("info......")
    log.warning("info......")
    log.error("info......")
```

> output

```shell
2023-03-17 09:21:36 root name[34768] DEBUG info......
2023-03-17 09:21:36 root name[34768] INFO info......
2023-03-17 09:21:36 root name[34768] WARNING info......
2023-03-17 09:21:36 root name[34768] ERROR info......

```

## Introduction

> **main function**

> yzm_log.`Logger`(
>> name: str = None,
>
>> log_path: str = None,
>
>> level: str = "INFO",
>
>> is_solitary: bool = True,
>
>> is_form_file: bool = False,
>
>> size: int = 104857600,
>
>> backup_count: int = 10,
>
>> encoding: str = "UTF-8"
>
> )

```
:param name: Project Name
:param log_path: Log file output path. Default is log_%Y%m%d.log.
:param level: Log printing level. Default is INFO.
:param is_solitary: When the file path is consistent (here, the log_path parameter is not a specific file name, but a file path), whether the file is formed independently according to the name parameter. Default is True.
:param is_form_file: Whether to form a log file. Default is False.
:param size: Setting the file size if a file is formed. Default is 104857600. (100MB)
:param backup_count: Setting the number of rotating files if a file is formed. Default is 10.
:param encoding: Setting of file encoding if a file is formed. Default is UTF-8.
```
