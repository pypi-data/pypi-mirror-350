import copy
import math
import os
from pathlib import Path
from typing import List, Tuple, Union
Seq = Union[List, Tuple]
try:
    from wcwidth import wcswidth
except ImportError:
    raise ImportError("[table] 请先安装wcwidth库: pip install wcwidth")

class MyDict:
    def __init__(self, init_dict = None):
        self.dict = dict()
        if type(init_dict) is dict:
            self.dict = init_dict.copy()
        if type(init_dict) is MyDict:
            self.dict = init_dict.dict.copy()


    def update(self, other_dict):
        self.dict.update(other_dict)

    def items(self):
        return self.dict.items()
    def keys(self):
        return self.dict.keys()
    def values(self):
        return self.dict.values()
    def copy(self):
        return MyDict(self.dict.copy())
    def __getitem__(self, item):
        return self.dict[str(item)]

    def __setitem__(self, key, value):
        key, value = str(key), str(value)

        if key not in self.dict.keys():
            self.dict.update({key: ''})

        self.dict[key] = value

class BAutoTable:
    def __init__(self, x_name='x', y_name='y'):
        self.x_sidebars = []
        self.y_sidebars = []
        self.x_name = x_name
        self.y_name = y_name
        self.dict = dict()
        self._widths = dict()

    def set(self, x_sidebar, y_sidebar, content):
        x_sidebar, y_sidebar, content = str(x_sidebar), str(y_sidebar), str(content)
        self[x_sidebar][y_sidebar] = str(content)

    def get_str(self, x_sidebar, y_sidebar):
        return self[x_sidebar][y_sidebar]
    def get_int(self, x_sidebar, y_sidebar):
        return int(self[x_sidebar][y_sidebar])
    def get_float(self, x_sidebar, y_sidebar):
        return float(self[x_sidebar][y_sidebar])
    def get_bool(self, x_sidebar, y_sidebar):
        temp = self[x_sidebar][y_sidebar]
        if temp == "True" or temp == "1":
            return True
        else:
            return False
    def items(self):
        '''
        (key1, key2, value)
        '''
        result = [(x, y, self.dict[x][y]) for x in self.x_sidebars for y in self.y_sidebars]
        return result
    def copy_row(self, old_row:str, new_row:str):
        old_row, new_row = str(old_row), str(new_row)
        self[new_row] = self[old_row]
    def read_txt(self, path):
        with open(path, 'r') as f:
            lines = f.readlines()
            lines = [x.strip() for x in lines if x.startswith('|')]

        temp = []
        for string in lines:
            elements = string.split('|')[1:-1]
            elements = [x.strip() for x in elements]
            temp.append(elements)

        x_name, y_name = temp[0][0].split(' \\ ') if ('\\' in temp[0][0]) else ("x", "y")
        x_keys = [var[0] for var in temp[1:]]
        y_keys = temp[0][1:]

        self.x_sidebars = []
        self.y_sidebars = []
        self.x_name = x_name
        self.y_name = y_name
        self.dict = dict()
        self._widths = dict()

        for i, x_element in enumerate(x_keys):
            y_dict = MyDict()
            for j, y_element in enumerate(y_keys):
                y_dict.update({y_element: temp[i+1][j+1]})
            self.dict.update({x_element: y_dict})
        self._update_sidebars()

    def to_txt(self, path):
        '''
        将表格内容写入文件
        :param path:
        :return:
        '''
        dir = Path(path).resolve().parent
        os.makedirs(dir, exist_ok=True)
        with open(path, 'w') as f:
            f.write(self.get_table_by_str())

    def update_txt(self, path):
        '''
        更新表格内容\n
        如果文件不存在，则创建文件
        :param path:
        :return:
        '''
        # 是否存在该文件
        if not os.path.exists(path):
            self.to_txt(path)
        else:
            new_dict = self.dict
            self.read_txt(path)
            origin_dict = self.dict
            self.dict = self._merge_2d_dicts(origin_dict, new_dict)
            self._update_sidebars()

            self.to_txt(path)



    def get_table_by_strs(self) -> List[str]:
        results = self._create_prefix()

        self._update_widths()

        str_dash = ''
        str_head = ''
        for y in self.y_sidebars:
            pre_space, suf_space = self._get_prefix_suffix(y, self._widths[y], ' ')
            pre_dash, suf_dash = self._get_prefix_suffix('-', self._widths[y], '-')
            str_head += ' ' + pre_space + y + suf_space + ' |'
            str_dash += '-' + pre_dash + '-' + suf_dash + '-+'
        results[0] += str_dash
        results[1] += str_head
        results[2] += str_dash

        offset = 3
        for index, y_dicts in enumerate(self.dict.values()):
            for key in self.y_sidebars:
                value = y_dicts[key] if key in y_dicts.keys() else ''
                pre_space, suf_space = self._get_prefix_suffix(value, self._widths[key], ' ')
                str_content = ' ' + pre_space + value + suf_space + ' |'
                results[index+offset] += str_content

        results[-1] += str_dash

        return results

    def get_table_by_str(self) -> str:
        result = ""
        strs = self.get_table_by_strs()
        for x in strs[:-1]:
            result += x + '\n'
        result += strs[-1]

        return result
    def print_table(self):
        print(self.get_table_by_str())

    def _merge_2d_dicts(self, origin_dict, new_dict):
        """
        合并两个二维字典。
        如果两个字典的相同键存在重叠的子键，则 new_dict 的值覆盖 origin_dict。
        """
        merged_dict = {key: value.copy() for key, value in origin_dict.items()}  # 复制 origin_dict 避免修改原数据
        for key, sub_dict in new_dict.items():
            if key in merged_dict.keys():
                merged_dict[key].update(sub_dict)  # 合并子字典
            else:
                merged_dict[key] = sub_dict  # 直接添加新键

        return merged_dict
    def _update_sidebars(self):
        self.x_sidebars = list(self.dict.keys())

        temp = []
        for dict_y in self.dict.values():
            for key in dict_y.keys():
                if key not in temp:
                    temp.append(key)
        self.y_sidebars = temp

    def _create_prefix(self):
        '''
        得到
        +-------+
        | x \ y |
        +-------+
        |   1   |
        |   2   |
        |   3   |
        +-------+
        '''
        results = []

        title = self.x_name + " \ " + self.y_name
        self._update_sidebars()
        n = self._get_maxlength_from_list(self.x_sidebars)
        length = max(n, self._get_width(title))

        pre_dash, suf_dash = self._get_prefix_suffix("-", length, '-')
        str_dash = "+-" + pre_dash + "-" + suf_dash + "-+"
        results.append(str_dash)

        pre_space, suf_space = self._get_prefix_suffix(title, length, ' ')
        str_index = "| " + pre_space + title + suf_space + " |"
        results.append(str_index)
        results.append(str_dash)

        for x in self.x_sidebars:
            pre_space, suf_space = self._get_prefix_suffix(x, length, ' ')
            str_number = "| " + pre_space + x + suf_space + " |"
            results.append(str_number)
        results.append(str_dash)

        return results

    def _get_prefix_suffix(self, string, length, charactor=' '):
        prefix = ''
        suffix = ''
        str_len = self._get_width(string)

        delta = length - str_len
        if delta < 0:
            assert "string的宽度比length宽"
        elif delta == 0:
            pass
        else:
            prefix = charactor * math.floor(delta / 2)
            suffix = charactor * math.ceil(delta / 2)

        return prefix, suffix

    def _get_maxlength_from_list(self, lst: List[str]) -> int:
        temp = [self._get_width(x) for x in lst]
        if len(temp) == 0:
            return 0
        else:
            return max(temp)

    def _update_widths(self):
        temp = {key: self._get_width(key) for key in self.y_sidebars}

        # for dict_y in self.dict.values():
        #     for key, value in dict_y.items():
        #         width = self._get_width(value)
        #         if width > temp[key]:
        #             temp[key] = width

        matrix = self._get_width_matrix()
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] > temp[self.y_sidebars[j]]:
                    temp[self.y_sidebars[j]] = matrix[i][j]

        self._widths = temp
    def _get_width_matrix(self):
        results = [[0 for _ in self.y_sidebars] for _ in self.x_sidebars]
        for x, dict_y in self.dict.items():
            for y, value in dict_y.items():
                results[self.x_sidebars.index(x)][self.y_sidebars.index(y)] = self._get_width(value)
        return results

    def __repr__(self):
        print(self._widths)
    def _get_width(self, string):
        return wcswidth(string)

    def __len__(self):
        return len(self.x_sidebars) * len(self.y_sidebars)
    def __contains__(self, item):
        for x in self.x_sidebars:
            for y in self.y_sidebars:
                if str(item) == self.dict[x][y]:
                    return True
        return False
    def __str__(self):
        return self.get_table_by_str()

    def __getitem__(self, index):
        index = str(index)

        if index not in self.dict.keys():
            self.dict.update({index: MyDict()})
            self._update_sidebars()
            return self.dict[index]

        return self.dict[index]
    def __setitem__(self, index, value:MyDict|dict):
        index, value = str(index), MyDict(value)
        self.dict.update({index: value})

if __name__ == '__main__':
    my_table = BAutoTable("x", "y")

    my_table[1][3] = 123
    my_table[2][2] = 123
    my_table["awa"]["12133"] = 123
    my_table.copy_row('awa', 'qwq')
    my_table['qwq'][12133] = 333

    # my_table.read_txt(r'E:\byzh_workingplace\byzh-rc-to-pypi\awa.txt')
    print(my_table)
    repr(my_table)