# -*- coding: utf-8 -*-
# @Time    : 2025/5/15 上午10:54
# @Author  : 车小炮
import pandas as pd

def clear_str(target_str):
    target_str = target_str.replace('/', '_')
    target_str = target_str.replace(' ', '_')
    target_str = target_str.replace("'", '')
    target_str = target_str.replace('-', '_')
    target_str = target_str.replace('(', '_')
    target_str = target_str.replace(')', '')
    target_str = target_str.lower()
    return target_str


def read_file(file_path):
    datas = []
    if '.csv' in file_path:
        try:
            try:
                try:
                    df = pd.read_csv(file_path, dtype=str, encoding='gbk')
                except:
                    df = pd.read_csv(file_path, dtype=str, encoding='gb18030')
            except:
                df = pd.read_csv(file_path, dtype=str, encoding='utf-8')
        except:
            print('read_csv_file_error: ', file_path)
            return []
        df.fillna('', inplace=True)
        df.columns = [clear_str(col) for col in df.columns]
        datas = df.to_dict(orient='records')

    elif '.txt' in file_path:
        try:
            f = open(file_path, mode='r', encoding='gbk')
        except:
            print('read_txt_file_error: ', file_path)
            return []
        data_item = f.read().strip().split('\n')
        keys = [clear_str(col) for col in data_item[1].split('|')]
        for data in data_item[2:]:
            datas.append(dict(zip(keys, data.split('|'))))
        f.close()

    return datas


def create_table(table_name, insert_item, str_length=255):
    key_list = []
    for a in insert_item.keys():
        if not insert_item[a]:
            key_list.append(f'"{a}" varchar({str_length}),')
        elif len(str(insert_item[a])) < 255:
            key_list.append(f'"{a}" varchar({str_length}),')
        else:
            key_list.append(f'"{a}" varchar(65535),')
    key_sql = '\n'.join(key_list)
    create_sql = f'''
            CREATE TABLE "public"."{table_name}" (
            "{table_name}_id" INT IDENTITY(1,1),
            {key_sql}
            "create_time" int8 NOT NULL,
            "create_account_id" int8 NOT NULL,
            "modify_time" int8,
            "modify_account_id" int8,
            "state" int2 NOT NULL DEFAULT 1,
            "deleted" int2 NOT NULL,
            CONSTRAINT "{table_name}_pkey" PRIMARY KEY ("{table_name}_id")
        )
        '''
    return create_sql


def make_insert_sql(table_name, insert_item):
    columns = insert_item.keys()
    values = []
    for value in insert_item.values():
        if value is None:
            values.append('NULL')
        elif isinstance(value, str):
            escaped_value = value.replace("'", "''")
            values.append(f"'{escaped_value}'")
        elif isinstance(value, (int, float)):
            values.append(str(value))
        else:
            values.append(f"'{str(value)}'")

    columns_str = ', '.join(columns)
    values_str = ', '.join(values)
    insert_sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});"
    return insert_sql


def make_batch_insert_sql(table_name, insert_items):
    """
    构造批量插入的 SQL 语句。

    参数：
    - table_name: 表名。
    - insert_items: 包含字典的列表，每个字典表示一行数据。

    返回：
    - 批量插入的 SQL 语句。
    """
    if not insert_items:
        raise ValueError("insert_items 不能为空")

    # 获取列名（假设所有字典的键相同）
    columns = insert_items[0].keys()
    columns_str = ', '.join(columns)

    # 构造 VALUES 部分
    values_list = []
    for insert_item in insert_items:
        values = []
        for value in insert_item.values():
            if value is None:
                values.append('NULL')
            elif isinstance(value, str):
                escaped_value = value.replace("'", "''")  # 转义单引号
                values.append(f"'{escaped_value}'")
            elif isinstance(value, (int, float)):
                values.append(str(value))
            else:
                values.append(f"'{str(value)}'")
        values_str = ', '.join(values)
        values_list.append(f"({values_str})")

    # 拼接完整的 SQL 语句
    values_all = ',\n'.join(values_list)
    batch_insert_sql = f"INSERT INTO {table_name} ({columns_str}) VALUES\n{values_all};"
    return batch_insert_sql


def make_update_sql(table_name, up_item, condition):
    up_list = []
    for k, v in up_item.items():
        up_list.append(f"{k} = '{v}'")
    up_str = ', '.join(up_list)
    insert_sql = f"UPDATE {table_name} SET {up_str} WHERE {condition}"
    return insert_sql