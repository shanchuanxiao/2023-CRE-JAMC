# 日期：2022年05月12日

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time


def heavy_sampling_method(data, start_time, end_time, step, type=0):
    """
    重抽样函数（固定时间间隔的平均值）：
    data:输入待处理数据，其必须为DataFrame数组格式，索引为datetime格式的时间(年-月-日 时:分:秒);
    start_time:为重抽样开始时间，格式为'年-月-日 时:分:秒'，
    end_time:为重抽样开始时间，格式为'年-月-日 时:分:秒'，
    step:重抽样步长，需为字符串格式，eg."1Y/y","1M/m",“10D/d”,"30min","1H/h","30S/s";:M/m表示月，min表示分钟
    type:设置重抽样格式，0为向后重抽样00：30的值为(00:00,00:30],1为向后重抽样00：30的值为[00:00,00:30)，默认为0
    功能：对输入的以时间为索引的DataFrame数组中的所有列数据进行重抽样处理
    """
    time_begin = time.time()  # the time of program start

    # 生成重抽样时间标签，起止时间-按分钟生成时间
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')  # 将开始时间转化为datetime格式
    end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')  # 将结束时间转化为datetime格式
    if step[-1] == 'M' or step[-1] == 'm':  # if the step is month
        heavy_sampling_time = pd.date_range(start_time, end_time, freq=step[:-1] + 'MS')  # start month frequency
    else:
        heavy_sampling_time = pd.date_range(start_time, end_time, freq=step)
    print(heavy_sampling_time)

    # 将如果字符串step为月以下尺度，则将setp转换成以秒为单位
    # 将如果字符串step为月及以上尺度，则将setp转换成以月为单位
    if step[-1] == 'S' or step[-1] == 's':  # second
        step_ = float(step[:-1])
    elif step[-1] == 'n':  # minute
        step_ = float(step[:-3]) * 60
    elif step[-1] == 'H' or step[-1] == 'h':  # hour
        step_ = float(step[:-1]) * 60 * 60
    elif step[-1] == 'D' or step[-1] == 'd':  # day
        step_ = float(step[:-1]) * 24 * 60 * 60
    elif step[-1] == 'M' or step[-1] == 'm':  # month
        step_ = float(step[:-1])
    elif step[-1] == 'Y' or step[-1] == 'y':  # year
        step_ = float(step[:-1]) * 12
    else:
        print('The entering step is error!')

    # # 计算重抽样结果
    heavy_sampling = pd.DataFrame([], columns=data.columns)  # 创建空DataFrame数组，方便后面添加
    if type == 0:
        # 计算第一个时间点的重抽样值
        for i in range(len(heavy_sampling_time)):  # 按heavy_sampling_time循环，计算每个时间点的重抽样值
            if i == 0:  # 对于第一个时间，需要特殊处理，获得该时次与其前step时间之间的数据
                if step[-1] in ['S', 'n', 'H', 'D', 's', 'h', 'd']:
                    start = heavy_sampling_time[i] + timedelta(seconds=-1 * step_)
                elif step[-1] in ['M', 'Y', 'm', 'y']:
                    start = heavy_sampling_time[i] + relativedelta(months=-1 * step_)
            else:
                start = heavy_sampling_time[i - 1]
            end = heavy_sampling_time[i]
            heavy_range = data.loc[start:end]
            if len(heavy_range) > 0 and heavy_range.index[0] == start:
                heavy_range = heavy_range.drop(heavy_range.index[0], axis=0)  # 若heavy_range第一个时间为start，则删除
            if len(heavy_range) > 0:
                mean = heavy_range.mean(axis=0)  # 计算平均值
                heavy_sampling.loc[heavy_sampling_time[i]] = mean
                # # 重抽样计时
                time_new = time.time()
                print('重抽样计算:' + str(heavy_sampling_time[i])[:19] + '  用时:' + str(time_new - time_begin) + 's')

    if type == 1:
        for i in range(len(heavy_sampling_time)):  # 按heavy_sampling_time循环，计算每个时间点的重抽样值
            start = heavy_sampling_time[i]
            if i == len(heavy_sampling_time) - 1:  # 对于第一个时间，需要特殊处理，获得该时次与其前step时间之间的数据
                if step[-1] in ['S', 'n', 'H', 'D', 's', 'h', 'd']:
                    end = heavy_sampling_time[i] + timedelta(seconds=step_)
                elif step[-1] in ['M', 'Y', 'm', 'y']:
                    end = heavy_sampling_time[i] + relativedelta(months=step_)
            else:
                end = heavy_sampling_time[i + 1]
            heavy_range = data.loc[start:end]
            if len(heavy_range) > 0 and heavy_range.index[-1] == end:
                heavy_range = heavy_range.drop(heavy_range.index[-1], axis=0)  # 若heavy_range最后时间为end，则删除
            if len(heavy_range) > 0:
                mean = heavy_range.mean(axis=0)  # 计算平均值
                heavy_sampling.loc[heavy_sampling_time[i]] = mean
                # # 重抽样计时
                time_new = time.time()
                print('重抽样计算:' + str(heavy_sampling_time[i])[:19] + '  用时:' + str(time_new - time_begin) + 's')
    return heavy_sampling


def calculate_reserve(time_type):
    # 计算重抽样结果
    roof_ = heavy_sampling_method(roof, '2017-01-01 00:00:00', '2021-01-01 00:00:00', time_type, type=0)
    paint_ = heavy_sampling_method(paint, '2017-01-01 00:00:00', '2021-01-01 00:00:00', time_type)
    tpo_ = heavy_sampling_method(tpo, '2017-01-01 00:00:00', '2021-01-01 00:00:00', time_type)
    aa_ = heavy_sampling_method(aa, '2017-01-01 00:00:00', '2021-01-01 00:00:00', time_type)

    # 将索引(时间)添加成'TIMESTAMP'列
    roof_.insert(loc=0, column='TIMESTAMP', value=roof_.index)
    paint_.insert(loc=0, column='TIMESTAMP', value=paint_.index)
    tpo_.insert(loc=0, column='TIMESTAMP', value=tpo_.index)
    aa_.insert(loc=0, column='TIMESTAMP', value=aa_.index)

    # 将各屋顶材料辐射四分量的30min平均存入excel
    # path = r'C:\Users\NH4NO3nice\Desktop\2022 大创项目\实验数据处理\30min和1h平均数据\\'  # 存放目录
    path = './after_processing/'  # 存放目录
    with pd.ExcelWriter(path + time_type + '.xlsx') as f:
        roof_.to_excel(f, sheet_name='roof', index=False, header=True)
        paint_.to_excel(f, sheet_name='paint', index=False, header=True)
        tpo_.to_excel(f, sheet_name='tpo', index=False, header=True)
        aa_.to_excel(f, sheet_name='aa', index=False, header=True)

    # # 存为feather格式数据
    roof_.index = np.arange(len(roof_))
    paint_.index = np.arange(len(paint_))
    tpo_.index = np.arange(len(tpo_))
    aa_.index = np.arange(len(aa_))

    roof_.to_feather(path + time_type + '-roof.feather')
    paint_.to_feather(path + time_type + '-paint.feather')
    tpo_.to_feather(path + time_type + '-tpo.feather')
    aa_.to_feather(path + time_type + '-aa.feather')


"""分别读取roof、paint、tpo、aa的辐射四分量数据"""
start_time = time.time()  # 程序运行开始时间
# path = r'C:\Users\NH4NO3nice\Desktop\2022 大创项目\实验数据处理\原始数据\\'
path = './original_data/'
roof = pd.read_feather(path + 'roof.feather')
paint = pd.read_feather(path + 'paint.feather')
tpo = pd.read_feather(path + 'tpo.feather')
aa = pd.read_feather(path + 'aa.feather')

# # 数据质量处理（转化成numpy数组更方便）
roof_new, paint_new, tpo_new, aa_new = np.array(roof), np.array(paint), np.array(tpo), np.array(aa)  # 转化为numpy数组
# 将短波辐射值小于100的设置为nan，缺测
roof_new[:, 1:3][roof_new[:, 1:3] < 5] = 0
paint_new[:, 1:3][paint_new[:, 1:3] < 5] = 0
tpo_new[:, 1:3][tpo_new[:, 1:3] < 5] = 0
aa_new[:, 1:3][aa_new[:, 1:3] < 5] = 0
# 将向下短波辐射DR<向上短波辐射UR时刻的DR、UR设置为nan，缺测
roof_new[:, 1:3][roof_new[:, 1] < roof_new[:, 2]] = np.nan
paint_new[:, 1:3][paint_new[:, 1] < paint_new[:, 2]] = np.nan
tpo_new[:, 1:3][tpo_new[:, 1] < tpo_new[:, 2]] = np.nan
aa_new[:, 1:3][aa_new[:, 1] < aa_new[:, 2]] = np.nan
# 将numpy数组转回dataframe格式
roof = pd.DataFrame(roof_new, columns=['TIMESTAMP', 'DR', 'UR', 'DLR', 'ULR'])
paint = pd.DataFrame(paint_new, columns=['TIMESTAMP', 'DR', 'UR', 'DLR', 'ULR'])
tpo = pd.DataFrame(tpo_new, columns=['TIMESTAMP', 'DR', 'UR', 'DLR', 'ULR'])
aa = pd.DataFrame(aa_new, columns=['TIMESTAMP', 'DR', 'UR', 'DLR', 'ULR'])

# 将时间列设置成索引
roof.index, paint.index, tpo.index, aa.index = roof.TIMESTAMP, paint.TIMESTAMP, tpo.TIMESTAMP, aa.TIMESTAMP
# 删除原先的时间列
roof.drop('TIMESTAMP', axis=1, inplace=True)
paint.drop('TIMESTAMP', axis=1, inplace=True)
tpo.drop('TIMESTAMP', axis=1, inplace=True)
aa.drop('TIMESTAMP', axis=1, inplace=True)


# 计算重抽样结果(30min平均)
calculate_reserve('30min')
# # 计算重抽样结果(1h平均)
# calculate_reserve('1h')
# # 计算重抽样结果(1d平均)
# calculate_reserve('1d')
# # 计算重抽样结果(1mon平均)
# calculate_reserve('1m')

end_time = time.time()
print('程序总运行时间:' + str((end_time - start_time) / 3600) + 'h')


