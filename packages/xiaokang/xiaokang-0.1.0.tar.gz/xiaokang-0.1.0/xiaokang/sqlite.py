
import sqlite3
import time
import xiaokang.ChangYong as ChangYong


def db_sql(sql, 数据库='主记录表'):
    '''db_sql(sql, 数据库='主记录表')\n
    sql：数据语句\n
    数据库：默认链接='主记录表'\n
    (返回执行情况[真/假]，返回执行后的数据表)
    '''
    try:
        conn = sqlite3.connect(f'数据存放/{数据库}.db')
        cursor = conn.cursor()
        a = time.strftime("%Y-%m-%d %H:%M:%S\n")+f'sql：{sql}{'\n'*2}'
        open('日志/数据库操作.txt', 'a', encoding='utf-8').write(a)
        open('日志/执行库数据.txt', 'a', encoding='utf-8').write(a)
        cursor.execute(sql)
        a = cursor.fetchall()
        conn.commit()
        conn.close()
    except:
        ChangYong.报错信息()
        return False, ''
    return True, a


def db_cj(表名, 字段: list, 字段类型: dict = {}, 默认值='TEXT', 数据库='主记录表'):
    '''
    db_cj(表名, 字段, 字段类型: dict = {}, 默认值='TEXT', 数据库='主记录表')\n
    表名：创建的表名\n
    字段[]：创建表中的字段\n
    字段类型{}：指定创建字段的类型\n
    默认值：在没有指定的情况下创建字段的默认值='TEXT'\n
    数据库：默认链接='主记录表'\n
    返回创建情况[真/假]\n
    '''
    try:
        sql = f'CREATE TABLE "{表名}" ('
        for f1 in 字段:
            sql += f'{f1} {字段类型.get(f1, 默认值)},'
        sql = sql[:-1]+');'
        conn = sqlite3.connect(f'数据存放/{数据库}.db')
        cursor = conn.cursor()
        a = time.strftime("%Y-%m-%d %H:%M:%S\n")+f'sql：{sql}{'\n'*2}'
        open('日志/数据库操作.txt', 'a', encoding='utf-8').write(a)
        open('日志/创建库数据.txt', 'a', encoding='utf-8').write(a)
        cursor.execute(sql)
        conn.commit()
        conn.close()
    except:
        ChangYong.报错信息()
        return False
    return True


def db_dq(sql, value: tuple = '', 数据库='主记录表'):
    '''
    db_dq(sql, value: tuple = '', 数据库='主记录表')
    sql: 查询数据的sql语句
    value(): sql语句中的'?'值
    数据库: 默认链接='主记录表'
    (返回执行情况[真/假]，返回执行后的数据表)
    '''
    try:
        conn = sqlite3.connect(f'数据存放/{数据库}.db')
        cursor = conn.cursor()
        a = time.strftime("%Y-%m-%d %H:%M:%S\n")+f'sql：{sql}\nvalue：{value}'+'\n'*2
        open('日志/数据库操作.txt', 'a', encoding='utf-8').write(a)
        open('日志/读取库数据.txt', 'a', encoding='utf-8').write(a)
        if value == "":
            cursor.execute(sql)
        else:
            cursor.execute(sql, value)
        a = cursor.fetchall()
        conn.close()
    except:
        ChangYong.报错信息()
        return False, ''
    return True, a


def db_xr(表: str, 段: list, 值: list, 数据库='主记录表'):
    '''
    db_xr(表: str, 段: list, 值: list, 数据库='主记录表')
    表: 写入数据的表名
    段: 写入的字段名
    值: 写入的字段值
    数据库: 写入的数据库名默认数据库='主记录表'
    (返回执行情况[真/假]，返回自增值序号)
    '''
    try:
        for f1 in range(len(值)):
            if not type(值[f1]) in [int, str] and not 值[f1] == None:
                值[f1] = str(值[f1])
        a = '"'+'","'.join(段)+'"'
        b = ','.join(['?']*len(段))
        conn = sqlite3.connect(f'数据存放/{数据库}.db')
        cursor = conn.cursor()
        sql = f'INSERT INTO "{表}" ({a}) VALUES ({b})'
        a = time.strftime("%Y-%m-%d %H:%M:%S\n")+f'sql：{sql}\nvalue：{值}'+'\n'*2
        open('日志/数据库操作.txt', 'a', encoding='utf-8').write(a)
        open('日志/写入数据库.txt', 'a', encoding='utf-8').write(a)
        cursor.execute(sql, 值)
        a = cursor.lastrowid
        conn.commit()
        conn.close()
    except:
        ChangYong.报错信息()
        return False, ''
    return True, a


def db_xg(表: str, 查段: list, 查值: tuple, 写段: list, 写值: tuple, 数据库='主记录表'):
    '''
    db_xg(表: str, 查段: list, 查值: tuple, 写段: list, 写值: tuple, 数据库='主记录表')
    表: 修改数据的表名
    查段: 判断修改数据的字段名
    查值: 字段名对应的值确保数据修改
    写段: 需要修改的字段名
    写值: 修改字段的值
    数据库: 需要修改的数据名：默认值='主记录表'
    (返回修改情况[真/假])
    '''
    try:
        a = '=?,'.join(写段)+'=?'
        b = '=? AND '.join(查段)+'=?'
        conn = sqlite3.connect(f'数据存放/{数据库}.db')
        cursor = conn.cursor()
        sql = f'UPDATE "{表}" SET {a} WHERE {b}'
        a = time.strftime("%Y-%m-%d %H:%M:%S\n") + f'sql：{sql}\nvalue：{写值+查值}'+'\n'*2
        open('日志/数据库操作.txt', 'a', encoding='utf-8').write(a)
        open('日志/修改数据库.txt', 'a', encoding='utf-8').write(a)
        cursor.execute(sql, 写值+查值)
        conn.commit()
        conn.close()
    except:
        ChangYong.报错信息()
        return False
    return True
