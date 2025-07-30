import concurrent.futures
from tqdm import tqdm


class Bar:
    """在多线程中打印进度条
    要求实例化时传入总数total_num,desc为进度条描述,color为进度条颜色
    func: 需要执行的函数
    args_list: 参数列表
    args_list中的每个元素为一个元组,表示func的若干输入参数

    调用实例:
    bar = Bar(len(img_paths), desc='Resizing', color="#CD8500")
    bar(main_work, [(img_path,) for img_path in img_paths])
    """

    def __init__(self, total_num, desc="", color="#CD8500"):
        self.pbar = tqdm(total=total_num, desc=desc, dynamic_ncols=True, colour=color)
        self.error_num = 0

    def callback(self, future):
        try:
            future.result()
        except Exception as e:
            self.error_num += 1
        finally:
            self.pbar.update(1)

    def __call__(self, func, args_list):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for args in args_list:
                future = executor.submit(func, *args)
                future.add_done_callback(self.callback)

            # 等待所有任务完成
            executor.shutdown(wait=True)
