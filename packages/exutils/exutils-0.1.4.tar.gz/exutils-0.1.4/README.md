# exutils

扩展工具包。

当前包含：

- `catch_exception`：异常捕获装饰器，自动打印详细参数和堆栈信息。

## 安装

```bash
pip install exutils
```
```python
from exutils import catch_exception

@catch_exception(return_value="error", suppress=True)
def divide(x, y):
    return x / y

print(divide(10, 0))

```

---

### LICENSE

（MIT License，开放使用）

```text
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
...