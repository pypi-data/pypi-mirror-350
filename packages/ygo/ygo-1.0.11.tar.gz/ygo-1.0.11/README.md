# ygo
并发执行(加入进度条)以及延迟调用（基于joblib），以及获取对应函数的相关信息

### 安装
```shell
pip install -U git+https://github.com/link-yundi/ygo.git
```

### 示例

```
├── a
│   ├── __init__.py
│   └── b
│       ├── __init__.py
│       └── c.py
└── test.py

c.py 中定义了目标函数
def test_fn(a, b=2):
    return a+b
```

#### 场景1: 并发

```python
import ygo
import ylog
from a.b.c import test_fn

with ygo.pool(job_name="test parallel", show_progress=True) as go:
    for i in range(10):
        go.submit(test_fn)(a=i, b=2*i)
    for res in go.do():
        ylog.info(res)
```

#### 场景2: 延迟调用

```
>>> fn = delay(test_fn)(a=1, b=2)
>>> fn()
3
>>> # 逐步传递参数
>>> fn1 = delay(lambda a, b, c: a+b+c)(a=1)
>>> fn2 = delay(fn1)(b=2)
>>> fn2(c=3)
6
>>> # 参数更改
>>> fn1 = delay(lambda a, b, c: a+b+c)(a=1, b=2)
>>> fn2 = delay(fn1)(c=3, b=5)
>>> fn2()
9
```

#### 场景3: 获取目标函数信息

```
>>> ygo.fn_info(test_fn)
=============================================================
    a.b.c.test_fn(a, b=2)
=============================================================
    def test_fn(a, b=2):
    return a+b
```

#### 场景4: 通过字符串解析函数并执行

```
>>> ygo.fn_from_str("a.b.c.test_fn")(a=1, b=5)
6
```

