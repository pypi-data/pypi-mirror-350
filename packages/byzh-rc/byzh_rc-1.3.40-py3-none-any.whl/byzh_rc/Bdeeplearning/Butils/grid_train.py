from ...Btools.Bwriter import B_Writer
from ...Bbasic.Btext_style import B_Color
from ...Btools.Btable import B_RowTable, B_XYTable
from typing import Union
import time

Iter = Union[list, set, tuple]

def b_grid_trains_1d(func, x_name:str, iters:Iter, log_path):
    """
    x从iters中取
    :param func: 只有一个输入参数x, 返回值将转化为str并记录
    :param iters:
    :param log_path:
    :return:
    """
    print(f"{B_Color.CYAN}=====================")
    print("grid_trains_1d 将在3秒后开始:")
    print(f"====================={B_Color.RESET}")
    time.sleep(3)

    my_writer = B_Writer(log_path, ifTime=False)
    my_table = B_RowTable([x_name, "result"])

    for x in iters:
        result = func(x)
        my_table.append([x, result])

        string = my_table.get_table_by_str()
        my_writer.clearFile()
        my_writer.toFile("[grid_trains] 运行中", ifTime=True)
        my_writer.toFile(string)

    string = my_table.get_table_by_str()
    my_writer.clearFile()
    my_writer.toFile("[grid_trains] 运行结束", ifTime=True)
    my_writer.toFile(string)

def grid_trains_2d(func, x_name:str, x_iters:Iter, y_name:str, y_iters:Iter, log_path):
    print(f"{B_Color.CYAN}=====================")
    print("grid_trains_2d 将在3秒后开始:")
    print(f"====================={B_Color.RESET}")
    time.sleep(3)

    my_writer = B_Writer(log_path, ifTime=False)
    my_table = B_XYTable(x_name, y_name, x_iters, y_iters)
    for x in x_iters:
        for y in y_iters:
            result = func(x, y)
            my_table[x][y] = result

            string = my_table.get_table_by_str()
            my_writer.clearFile()
            my_writer.toFile("[grid_trains] 运行结束", ifTime=True)
            my_writer.toFile(string)

    string = my_table.get_table_by_str()
    my_writer.clearFile()
    my_writer.toFile("[grid_trains] 运行结束", ifTime=True)
    my_writer.toFile(string)

if __name__ == '__main__':
    def function(x):
        return x

    b_grid_trains_1d(function, [1, 2, 3], './awa.txt')
