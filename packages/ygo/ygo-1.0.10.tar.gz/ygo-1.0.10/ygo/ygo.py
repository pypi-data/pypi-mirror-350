# -*- coding: utf-8 -*-
"""
---------------------------------------------
Created on 2024/11/4 下午2:10
@author: ZhangYundi
@email: yundi.xxii@outlook.com
---------------------------------------------
"""
import functools
import importlib
import inspect
import multiprocessing
import os
import threading
import warnings
from pathlib import Path

from joblib import Parallel, delayed

import ylog
from .exceptions import WarnException, FailTaskError

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from tqdm.auto import tqdm


class DelayedFunction:

    def __init__(self, func):
        self.func = func
        self._fn_params_k = inspect.signature(self.func).parameters.keys()
        self.stored_kwargs = self._get_default_args(func)
        if hasattr(func, 'stored_kwargs'):
            self.stored_kwargs.update(func.stored_kwargs)

    def _get_default_args(self, func):
        signature = inspect.signature(func)
        return {
            k: v.default
            for k, v in signature.parameters.items()
            if v.default is not inspect.Parameter.empty
        }

    def __call__(self, *args, **kwargs):
        def delayed(*args, **_kwargs):
            new_kwargs = {k: v for k, v in self.stored_kwargs.items()}
            for k, v in _kwargs.items():
                if k not in self._fn_params_k:
                    continue
                new_kwargs[k] = v
            return self.func(*args, **new_kwargs)

        self._stored_kwargs(**kwargs)
        new_fn = functools.wraps(self.func)(delayed)
        new_fn.stored_kwargs = self.stored_kwargs
        return new_fn

    def _stored_kwargs(self, **kwargs):
        for k, v in kwargs.items():
            if k not in self._fn_params_k:
                continue
            self.stored_kwargs[k] = v


def delay(func):
    """
    延迟执行
    Parameters
    ----------
    func: Callable
        需要延迟执行的对象, 必须是一个Callable对象

    Returns
    -------
    DelayedFunction
        将预先设置好的参数包装进原始的Callable对象中

    Examples
    --------

    场景1：基本使用

    >>> fn = delay(lambda a, b: a+b)(a=1, b=2)
    >>> fn()
    3

    场景2: 逐步传递参数

    >>> fn1 = delay(lambda a, b, c: a+b+c)(a=1)
    >>> fn2 = delay(fn1)(b=2)
    >>> fn2(c=3)
    6

    场景3: 参数更改

    >>> fn1 = delay(lambda a, b, c: a+b+c)(a=1, b=2)
    >>> fn2 = delay(fn1)(c=3, b=5)
    >>> fn2()
    9
    """
    return DelayedFunction(func)


def fn_params(func: callable):
    """
    获取fn的参数
    Parameters
    ----------
    func: callable
        需要获取参数的callable对象
    Returns
    -------
    list[tuple]

    """
    # signatured = sorted(list(inspect.signature(func).parameters.keys()))
    # stored = delay(func)().stored_kwargs
    # return [(param, stored.get(param)) for param in signatured]
    stored = delay(func)().stored_kwargs.items()
    return sorted(stored)

def fn_signature_params(func: callable):
    """获取fn所有定义的参数"""
    return sorted(list(inspect.signature(func).parameters.keys()))

def fn_path(fn: callable) -> str:
    """
    获取func所在的模块层级结构
    Parameters
    ----------
    fn: callable
        需要获取结构的callable对象
    Returns
    -------
    str
        用 `.` 连接各级层级
    """
    module = fn.__module__
    # 检查模块是否有 __file__ 属性
    if module.startswith('__main__'):
        if hasattr(module, '__file__'):
            module = module.__file__
        else:
            # 如果在交互式环境中，返回 None 或者一个默认值
            module = "<interactive environment>"
    if module.endswith('.py'):
        module = module.split('.py')[0].split(str(Path(__file__).parent.parent.absolute()))[-1]
        module = '.'.join(module.strip(os.sep).split(os.sep))
    return module


def fn_code(fn: callable) -> str:
    """
    返回fn具体的定义代码

    Parameters
    ----------
    fn: callable
        需要获取具体定义代码的callable对象

    Returns
    -------
    str
        以字符串封装定义代码

    Examples
    --------

    >>> def test_fn(a, b=2):
    >>>     return a+b
    >>> print(fn_code())
    def test_fn(a, b=2):
        return a+b
    """
    return inspect.getsource(fn)


def fn_info(fn: callable) -> str:
    """获取函数的fn_mod, params, code"""
    # mod = fn_path(fn)
    params = fn_params(fn)
    code = fn_code(fn)
    all_define_params = sorted(list(inspect.signature(fn).parameters.keys()))

    default_params = {k: v for k, v in params}
    params_infos = list()
    for p in all_define_params:
        if p in default_params:
            params_infos.append(f'{p}={default_params[p]}')
        else:
            params_infos.append(p)
    params_infos = ', '.join(params_infos)

    s = f"""
=============================================================
{fn.__name__}({params_infos})
=============================================================
{code}
    """
    return s


def fn_from_str(s):
    """
    字符串导入对应fn
    s: a.b.c.func
    Parameters
    ----------
    s: str
        模块的路径，分隔符 `.`
    """
    *m_path, func = s.split(".")
    m_path = ".".join(m_path)
    mod = importlib.import_module(m_path)
    _callable = getattr(mod, func)
    return _callable


def module_from_str(s):
    """字符串导入模块"""
    m_path = ".".join(s.split('.'))
    mod = importlib.import_module(m_path)
    return mod

def run_job(job, task_id, queue):
    """执行任务并更新队列"""
    try:
        result = job()
    except WarnException as e:
        ylog.warning(FailTaskError(task_name=job.task_name, error=e))
        result = None
    except Exception as e:
        ylog.error(FailTaskError(task_name=job.task_name, error=e))
        result = None
    queue.put((task_id, 1))
    return result


def update_progress_bars(tqdm_objects: list[tqdm],
                         task_ids,
                         queue: multiprocessing.Queue,
                         num_tasks: int,
                         task_counts: dict):
    """根据队列中的消息更新 tqdm 进度条"""
    completed_tasks = 0
    completed_task_jobs = {id_: 0 for id_ in task_ids}
    while completed_tasks < num_tasks:
        task_id, progress_value = queue.get()  # 从队列获取进度更新
        completed_task_jobs[task_id] += 1
        if completed_task_jobs[task_id] >= task_counts[task_id]:
            completed_tasks += 1
        tqdm_objects[task_id].update(progress_value)
    [tqdm_object.close() for tqdm_object in tqdm_objects]


class pool:
    """
    每个fn运行一次算一个job，每个job需要指定job_name, 如果没有job_name, 则默认分配 TaskDefault
    相同 job_name 的fn归到同一个task, 同时该task命名为job_name
    即一个task中包含了多个需要运行的 job fn
    task1 <job_fn1, job_fn2, ...>
    task2 <job_fn3, job_fn4, ...>
    所有的job_fn都会通过joblib并行运行
    """

    def __init__(self, n_jobs=5, show_progress=True, backend='loky', ):
        """backend: loky/threading/multiprocessing"""
        self.show_progress = show_progress
        self._n_jobs = n_jobs
        self._parallel = Parallel(n_jobs=self._n_jobs, verbose=0, backend=backend) if self._n_jobs > 0 else None
        self._default_task_name = "TaskDefault"
        self._all_jobs = list()  # list[job]
        self._all_tasks = list()  # list[task_name]
        self._task_ids = dict()  # {task_name1: 0, task_name2: 1, ...}
        self._task_counts = dict()
        self._id_counts = dict()

    def submit(self, fn, job_name=""):
        """
        提交并行任务
        Parameters
        ----------
        fn: callable
            需要并行的callable对象
        job_name: str
            提交到的任务名, 不同的任务对应不同的进度条
        Returns
        -------
        """

        # 提交任务，对任务进行分类，提交到对应的task id中，并且封装新的功能：使其在运行完毕后将任务进度更新放入队列
        @functools.wraps(fn)
        def collect(**kwargs):
            """归集所有的job到对应的task"""
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                job = delay(fn)(**kwargs)
                task_name = self._default_task_name if not job_name else job_name
                if task_name not in self._task_ids:
                    self._task_ids[task_name] = len(self._all_tasks)
                    self._task_counts[task_name] = 0
                    self._all_tasks.append(task_name)
                    self._id_counts[self._task_ids[task_name]] = 0
                self._task_counts[task_name] += 1
                self._id_counts[self._task_ids[task_name]] += 1
                job.task_id = self._task_ids[task_name]
                job.job_id = self._task_counts[task_name]
                job.task_name = task_name
                self._all_jobs.append(job)
                return job

        return collect

    def do(self, *args, **kwargs):
        if self.show_progress:
            # if job_name is not None:
            #     ylog.info(f"{job_name} Start")
            # 消息队列进行通信
            manager = multiprocessing.Manager()
            queue = manager.Queue()
            tqdm_bars = [tqdm(total=self._task_counts[task_name],
                              desc=f"{str(task_name)}", leave=False) for task_name in
                         self._all_tasks]
            # 初始化多个任务的进度条，每个任务一个
            task_ids = [task_id for task_id in range(len(self._all_tasks))]
            # 创建并启动用于更新进度条的线程
            progress_thread = threading.Thread(target=update_progress_bars, args=(
                tqdm_bars, task_ids, queue, len(self._all_tasks), self._id_counts))
            progress_thread.start()
            if self._parallel is not None:
                # 执行并行任务
                result = self._parallel(delayed(run_job)(job=job,
                                                         task_id=job.task_id,
                                                         queue=queue) for job in self._all_jobs)
            else:
                result = [run_job(job=job, task_id=job.task_id, queue=queue) for job in self._all_jobs]
            # time.sleep(.3)
            # 等待进度更新线程执行完毕
            progress_thread.join()
            # if job_name is not None:
            #     ylog.info(f"{job_name} Done")
        else:
            if self._parallel is not None:
                result = self._parallel(delayed(job)() for job in self._all_jobs)
            else:
                result = [job() for job in self._all_jobs]
        self._all_jobs = list()  # list[job]
        self._all_tasks = list()  # list[task_name]
        self._task_ids = dict()  # {task_name1: 0, task_name2: 1, ...}
        self._task_counts = dict()
        self._id_counts = dict()
        return result

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 释放进程
        pass
