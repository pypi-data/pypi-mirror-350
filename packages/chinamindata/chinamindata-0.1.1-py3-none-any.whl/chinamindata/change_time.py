
from dateutil.relativedelta import relativedelta


def get_monthly_first_days(start_date_str, end_date_str,freq='1min'):
    """
    生成日期范围内每月首日的列表

    :param start_date_str: 起始日期字符串，格式'YYYY-MM-DD'
    :param end_date_str: 结束日期字符串，格式'YYYY-MM-DD'
    :return: 按日期升序排列的每月首日列表，格式['YYYY-MM-DD', ...]
    """
    try:
        # 日期格式校验与转换
        from datetime import datetime

        if isinstance(start_date_str, datetime):
            date_st = start_date_str.strftime('%Y-%m-%d %H:%M:%S')
        else:
            date_st = str(start_date_str)

        if isinstance(end_date_str, datetime):
            date_end = end_date_str.strftime('%Y-%m-%d %H:%M:%S')
        else:
            date_end = str(end_date_str)


        start_date = datetime.strptime(date_st.split()[0], '%Y-%m-%d')
        end_date = datetime.strptime(date_end.split()[0], '%Y-%m-%d')

        # 计算首尾月份首日
        first_day = start_date.replace(day=1)
        last_day = end_date.replace(day=1)

        # 处理无效日期范围
        if first_day > last_day:
            return []

        # 生成月份序列
        month_list = []
        current_day = first_day
        while current_day <= last_day:
            month_list.append(current_day)
            current_day += relativedelta(months=1)

        # 转换为字符串列表
        resut= [day.strftime('%Y-%m-%d') for day in month_list]

        # 使用示例
        # 1min
        # result = get_monthly_first_days()+["2025-03-15"]
        result5 = resut
        # print(result5)

        from datetime import datetime

        # 原始日期列表

        # 转换日期格式并排序（确保输入已排序）
        converted = [datetime.strptime(d, "%Y-%m-%d") for d in result5]

        # 初始化结果列表（保留第一个元素）
        filtered_dates = [converted[0]]
        last_date = converted[0]

        # 筛选每隔5个月的日期
        for current_date in converted[1:]:
            # 计算月份差
            month_diff = (current_date.year - last_date.year) * 12 + (current_date.month - last_date.month)

            if month_diff == int(freq.split("min")[0]):
                filtered_dates.append(current_date)
                last_date = current_date

        # 转换回字符串格式
        result2 = [d.strftime("%Y-%m-%d") for d in filtered_dates]


        # print(result2)

        result2[0]=result2[0] + " 00:00:01"
        # print(result2)
        if len(result2) == 1:
            result2.append(date_end)

        else:
            result2.append((datetime.strptime(result2[-1], '%Y-%m-%d')+relativedelta(months=int(freq.split("min")[0]))).strftime('%Y-%m-%d'))
        # print(result2)



        return result2



    except ValueError as e:
        raise ValueError(f"日期格式错误: {e}")


if __name__ == '__main__':
    get_monthly_first_days()