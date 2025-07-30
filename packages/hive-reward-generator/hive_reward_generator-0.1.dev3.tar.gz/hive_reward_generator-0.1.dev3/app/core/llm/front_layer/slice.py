import inspect
from concurrent.futures import as_completed
from concurrent.futures import ThreadPoolExecutor

from core.llm.data_structure.pcap_analysis import multi_pcap_analysis
from tqdm import tqdm

# 设置最大长度常量
LENGTH = 4096
MAX_THREADS = 5


def split_string(s, length):
    """将字符串按指定长度切分"""
    return [s[i:i + length] for i in range(0, len(s), length)]


def section(func):
    def wrapper(*args, **kwargs):
        # 获取函数签名并绑定参数
        sig = inspect.signature(func)
        try:
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
        except TypeError as e:
            raise RuntimeError("参数绑定失败，请检查参数是否正确") from e

        # 存储每个参数的切片列表
        param_chunks = {}

        for name, value in bound_args.arguments.items():
            if isinstance(value, str):
                chunks = split_string(value, LENGTH)
            else:
                chunks = [value]
            param_chunks[name] = chunks

        # 计算最大切片数
        max_slices = max(len(chunks) for chunks in param_chunks.values()) if param_chunks else 0

        # 收集所有返回结果
        all_results = [None] * max_slices  # 预分配列表空间

        # 定义线程执行函数
        def do_work(i):
            current_kwargs = {}
            for name, chunks in param_chunks.items():
                idx = min(i, len(chunks) - 1)
                current_kwargs[name] = chunks[idx]
            result = func(**current_kwargs)
            return (i, result)

        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            # 提交所有任务
            futures = [executor.submit(do_work, i) for i in range(max_slices)]

            # 初始化进度条
            results = {}
            with tqdm(total=max_slices, desc="Processing") as pbar:
                # 遍历已完成的任务
                for future in as_completed(futures):
                    # 获取任务结果
                    i, result = future.result()
                    # 保存结果（按索引）
                    results[i] = result
                    # 更新进度条
                    pbar.update(1)

            # 按索引顺序填充结果到all_results
            for i in results:
                all_results[i] = results[i]

        # 返回结果列表
        return all_results

    return wrapper
