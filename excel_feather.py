# 日期：2022年07月04日

"""将原始的excel数据转成feather格式数据，方便下次读取（速度快）"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os


def transform(old_time, step):
    """ 定义转化日期戳的函数,date为原始日期戳,step为时间间隔
        输出为修正后日期"""
    delta = timedelta(days=step)  # 将时间间隔转换成时间格式，以天为单位
    new_time = []  # 储存修订后的时间
    for i in range(len(old_time)):
        new = datetime.strptime(str(old_time[i])[:19], '%Y-%m-%dT%H:%M:%S') + delta  # 在原始时间基础上加上setp
        new_time.append(new)
    return new_time  # 制定输出日期的格式


"""分别读取roof、paint、tpo、aa的辐射四分量数据 170401-170815"""
"""分别读取roof、tpo、aa的辐射四分量数据 180122-190306,190427-200108,200219-201011 (17年的数据中有四个变量，所以分来读取)"""

# 整合所有时间数据
roof_all, paint_all, tpo_all, aa_all = pd.DataFrame([]), pd.DataFrame([]), pd.DataFrame([]), pd.DataFrame([])

# # 读取数据
# path = r'C:\Users\NH4NO3nice\Desktop\2022 大创项目\实验数据处理\原始数据\\'
path = './original_data/'
files = os.listdir(path)  # 读取各原始辐射四分量文件地址
files = list(filter(lambda x: x[-5:] == '.xlsx', files))

for file in files:
    if file == '1min-170401-170815原始.xlsx':
        head_name = ['TIMESTAMP', 'DR', 'UR', 'DLR', 'ULR']  # 命名表头
        roof = pd.read_excel(path + file, skiprows=[0, 2, 3], usecols=np.arange(5), names=head_name, na_values='NAN', index_col=0)
        paint = pd.read_excel(path + file, skiprows=[0, 2, 3], usecols=np.arange(6, 11), names=head_name, na_values='NAN', index_col=0)
        tpo = pd.read_excel(path + file, skiprows=[0, 2, 3], usecols=np.arange(12, 17), names=head_name, na_values='NAN', index_col=0)
        aa = pd.read_excel(path + file, skiprows=[0, 2, 3], usecols=np.arange(18, 23), names=head_name, na_values='NAN', index_col=0)
        print('完成数据读取')
        """删除roof、paint、tpo、aa中所有值为空值的行"""
        # axis=0：行；axis=1：列
        # how='all'：全部为空值才删除；how='any'：有空值就删除
        # inplace：是否在原数组上操作
        roof.dropna(axis=0, how='all', inplace=True)
        paint.dropna(axis=0, how='all', inplace=True)
        tpo.dropna(axis=0, how='all', inplace=True)
        aa.dropna(axis=0, how='all', inplace=True)

        # 整合所有时间
        roof_all = pd.concat([roof_all, roof], axis=0)
        paint_all = pd.concat([paint_all, paint], axis=0)
        tpo_all = pd.concat([tpo_all, tpo], axis=0)
        aa_all = pd.concat([aa_all, aa], axis=0)
        print('完成时间整合')

    elif file == '1min-180122-190306原始.xlsx':
        head_name = ['TIMESTAMP', 'DR', 'UR', 'DLR', 'ULR']  # 命名表头
        roof = pd.read_excel(path + file, skiprows=[0, 2, 3], usecols=np.arange(5), names=head_name, na_values='NAN', index_col=0)
        tpo = pd.read_excel(path + file, skiprows=[0, 2, 3], usecols=np.arange(6, 11), names=head_name, na_values='NAN', index_col=0)
        aa = pd.read_excel(path + file, skiprows=[0, 2, 3], usecols=np.arange(12, 17), names=head_name, na_values='NAN', index_col=0)
        print('完成数据读取')
        """删除roof、paint、tpo、aa中所有值为空值的行"""
        # axis=0：行；axis=1：列
        # how='all'：全部为空值才删除；how='any'：有空值就删除
        # inplace：是否在原数组上操作
        roof.dropna(axis=0, how='all', inplace=True)
        tpo.dropna(axis=0, how='all', inplace=True)
        aa.dropna(axis=0, how='all', inplace=True)

        # 整合所有时间
        roof_all = pd.concat([roof_all, roof], axis=0)
        tpo_all = pd.concat([tpo_all, tpo], axis=0)
        aa_all = pd.concat([aa_all, aa], axis=0)
        print('完成时间整合')

    elif file == '1min-190427-200108原始.xlsx':
        head_name = ['TIMESTAMP', 'DR', 'UR', 'DLR', 'ULR']  # 命名表头
        roof = pd.read_excel(path + file, skiprows=[0, 2, 3], usecols=[0, 2, 3, 4, 5], names=head_name, na_values='NAN', index_col=0)
        tpo = pd.read_excel(path + file, skiprows=[0, 2, 3], usecols=[7, 9, 10, 11, 12], names=head_name, na_values='NAN', index_col=0)
        aa = pd.read_excel(path + file, skiprows=[0, 2, 3], usecols=[14, 16, 17, 18, 19], names=head_name, na_values='NAN', index_col=0)

        """删除roof、paint、tpo、aa中所有值为空值的行"""
        # axis=0：行；axis=1：列
        # how='all'：全部为空值才删除；how='any'：有空值就删除
        # inplace：是否在原数组上操作
        roof.dropna(axis=0, how='all', inplace=True)
        tpo.dropna(axis=0, how='all', inplace=True)
        aa.dropna(axis=0, how='all', inplace=True)

        # # # 修订时间计算
        # step_roof, step_tpo, step_aa = roof.index[0], tpo.index[0], aa.index[0]  # 时间修正系数
        # new_time_roof = transform(roof.old_time[1:].values, step_roof)  # 订正之后的日期
        # new_time_tpo = transform(tpo.old_time[1:].values, step_tpo)  # 订正之后的日期
        # new_time_aa = transform(aa.old_time[1:].values, step_aa)  # 订正之后的日期
        # # # 删除修订指数行(第一行)
        # roof.drop(roof.index[0], axis=0, inplace=True)
        # tpo.drop(tpo.index[0], axis=0, inplace=True)
        # aa.drop(aa.index[0], axis=0, inplace=True)
        # # # 用修订好的时间替换索引
        # roof.index, tpo.index, aa.index = new_time_roof, new_time_tpo, new_time_aa

        # # # 删除原始时间列
        # roof.drop('old_time', axis=1, inplace=True)
        # tpo.drop('old_time', axis=1, inplace=True)
        # aa.drop('old_time', axis=1, inplace=True)
        print('完成读取')

        # 整合所有时间
        roof_all = pd.concat([roof_all, roof], axis=0)
        tpo_all = pd.concat([tpo_all, tpo], axis=0)
        aa_all = pd.concat([aa_all, aa], axis=0)
        print('完成时间整合')

    elif file == '1min-200219-201011原始.xlsx':
        head_name = ['TIMESTAMP', 'DR', 'UR', 'DLR', 'ULR']  # 命名表头
        roof = pd.read_excel(path + file, skiprows=[0, 2, 3], usecols=[0, 2, 3, 4, 5], names=head_name, na_values='NAN', index_col=0)
        tpo = pd.read_excel(path + file, skiprows=[0, 2, 3], usecols=[0, 9, 10, 11, 12], names=head_name, na_values='NAN', index_col=0)
        aa = pd.read_excel(path + file, skiprows=[0, 2, 3], usecols=[0, 16, 17, 18, 19], names=head_name, na_values='NAN', index_col=0)
        print('完成数据读取')
        """删除roof、paint、tpo、aa中所有值为空值的行"""
        # axis=0：行；axis=1：列
        # how='all'：全部为空值才删除；how='any'：有空值就删除
        # inplace：是否在原数组上操作
        roof.dropna(axis=0, how='all', inplace=True)
        tpo.dropna(axis=0, how='all', inplace=True)
        aa.dropna(axis=0, how='all', inplace=True)

        # 整合所有时间
        roof_all = pd.concat([roof_all, roof], axis=0)
        tpo_all = pd.concat([tpo_all, tpo], axis=0)
        aa_all = pd.concat([aa_all, aa], axis=0)
        print('完成时间整合')


# # # 将个别缺测替换成-9999.9
# roof_all.fillna(-9999.9, inplace=True)
# paint_all.fillna(-9999.9, inplace=True)
# tpo_all.fillna(-9999.9, inplace=True)
# aa_all.fillna(-9999.9, inplace=True)

# # 将索引换成默认索引，并新增时间列
roof_all.insert(0, 'TIMESTAMP', roof_all.index)
paint_all.insert(0, 'TIMESTAMP', paint_all.index)
tpo_all.insert(0, 'TIMESTAMP', tpo_all.index)
aa_all.insert(0, 'TIMESTAMP', aa_all.index)

roof_all.index = np.arange(len(roof_all))
paint_all.index = np.arange(len(paint_all))
tpo_all.index = np.arange(len(tpo_all))
aa_all.index = np.arange(len(aa_all))

# 存放feather格式数据
roof_all.to_feather(path + 'roof.feather')
paint_all.to_feather(path + 'paint.feather')
tpo_all.to_feather(path + 'tpo.feather')
aa_all.to_feather(path + 'aa.feather')


