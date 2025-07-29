#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os
import pymysql
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import pandas as pd
from typing import List, Dict, Any, Union, Optional, Callable, Tuple

class DataSyncUtils:
    """数据同步工具类，提供高效的数据库操作方法"""
    
    @staticmethod
    def default_batch_callback(batch_id: int, count: int, elapsed: float) -> None:
        """
        默认的批处理回调函数，输出批处理结果统计
        
        参数:
            batch_id: 批次ID
            count: 处理的记录数
            elapsed: 处理耗时(秒)
        """
        speed = count / elapsed if elapsed > 0 else 0
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 子批次 {batch_id} 完成: {count} 条记录, "
              f"耗时 {elapsed:.2f} 秒, 速率: {speed:.1f} 条/秒")
    
    @staticmethod
    def batch_insert_worker(
        batch_data: List[List[Any]], 
        insert_sql: str, 
        db_config: Dict[str, Any], 
        batch_id: int,
        callback: Optional[Callable] = None
    ) -> int:
        """
        并行批量插入工作线程
        
        参数:
            batch_data: 要插入的数据批次
            insert_sql: 预编译的插入SQL语句
            db_config: 数据库连接配置
            batch_id: 批次ID，用于日志
            callback: 可选的回调函数，处理每批次结果后调用
            
        返回:
            插入的记录数
        """
        conn = None
        cursor = None
        start_time = time.time()
        try:
            # 创建新连接而不是从连接池获取，避免并发问题
            conn = pymysql.connect(
                host=db_config["host"],
                port=db_config["port"],
                user=db_config["user"],
                password=db_config["password"],
                database=db_config["database"],
                charset=db_config["charset"],
                connect_timeout=db_config.get("connect_timeout", 10),
                read_timeout=db_config.get("read_timeout", 30),
                write_timeout=db_config.get("write_timeout", 30),
                local_infile=db_config.get("local_infile", 1),
                autocommit=False,  # 禁用自动提交
                max_allowed_packet=db_config.get("max_allowed_packet", 16*1024*1024)
            )
            cursor = conn.cursor()
            
            # 设置会话变量以优化批量插入
            cursor.execute("SET SESSION tidb_distsql_scan_concurrency=15")  # 调整扫描并发
            cursor.execute("SET SESSION tidb_dml_batch_size=128")  # 批处理大小
            
            # 执行批量插入
            cursor.executemany(insert_sql, batch_data)
            conn.commit()
            
            elapsed = time.time() - start_time
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 批次 {batch_id} 完成: 插入 {len(batch_data)} 条记录, 耗时 {elapsed:.2f} 秒")
            
            # 如果有回调函数，则调用
            if callback:
                callback(batch_id, len(batch_data), elapsed)
                
            return len(batch_data)
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 批次 {batch_id} 失败: {str(e)}")
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    @staticmethod
    def parallel_write_to_db(
        data: Union[pd.DataFrame, List[Dict[str, Any]]],
        db_config: Dict[str, Any],
        columns: List[str] = None,
        batch_size: int = 2000,
        max_workers: int = 20,
        insert_method: str = "update",
        primary_keys: List[str] = None,
        callback: Optional[Callable] = None
    ) -> Tuple[int, float, List[str]]:
        """
        并行写入数据到数据库
        
        参数:
            data: 要写入的数据，可以是Pandas DataFrame或字典列表
            db_config: 数据库连接配置，必须包含host, port, user, password, database, table等字段
            columns: 列名列表，如果为None则从data中推断
            batch_size: 每批次处理的记录数
            max_workers: 并行工作线程的最大数量
            insert_method: 插入方法，可选值为'update'(更新),'ignore'(忽略重复),'direct'(直接插入)
            primary_keys: 主键列表，用于构建ON DUPLICATE KEY UPDATE语句，仅在insert_method='update'时有效
            callback: 可选的回调函数，处理每批次结果后调用，如果未提供则使用默认回调函数
            
        返回:
            (插入记录数, 总耗时, 警告信息列表)
        """
        start_time = time.time()
        warnings = []
        
        # 如果未提供回调函数，使用默认回调
        if callback is None:
            callback = DataSyncUtils.default_batch_callback
        
        # 处理输入数据
        if isinstance(data, pd.DataFrame):
            # 如果是DataFrame，转换为字典列表
            if columns is None:
                columns = data.columns.tolist()
            
            # 处理NaN和None值
            for col in data.columns:
                data[col] = data[col].replace({pd.NA: None, float('nan'): None})
            
            # 转换为记录列表
            rows = []
            for _, row in data.iterrows():
                # 按列顺序提取值
                values = [row.get(col, None) for col in columns]
                rows.append(values)
        else:
            # 如果是字典列表
            if columns is None and data:
                # 从第一条记录推断列
                columns = list(data[0].keys())
            
            # 转换为记录列表
            rows = []
            for row in data:
                # 按列顺序提取值
                values = [row.get(col, None) for col in columns]
                rows.append(values)
        
        total_rows = len(rows)
        if total_rows == 0:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 没有数据需要写入")
            return 0, 0, warnings
        
        # 构建SQL语句
        table_name = db_config["table"]
        column_names = ', '.join(['`' + col + '`' for col in columns])
        placeholders = ', '.join(['%s'] * len(columns))
        
        if insert_method == 'update':
            # 更新模式: INSERT ... ON DUPLICATE KEY UPDATE
            if not primary_keys:
                # 如果没有提供主键，假设第一列是主键
                primary_keys = [columns[0]]
            
            # 构建更新部分，排除主键字段
            update_columns = [col for col in columns if col not in primary_keys]
            update_stmt = ', '.join([f"`{col}` = VALUES(`{col}`)" for col in update_columns])
            
            insert_sql = f"""
                INSERT /*+ SET_VAR(tidb_dml_type='bulk') */ INTO {table_name} ({column_names})
                VALUES ({placeholders})
                ON DUPLICATE KEY UPDATE {update_stmt};
            """
        elif insert_method == 'ignore':
            # 忽略模式: INSERT IGNORE INTO
            insert_sql = f"""
                INSERT /*+ SET_VAR(tidb_dml_type='bulk') */ IGNORE INTO {table_name} ({column_names})
                VALUES ({placeholders});
            """
        else:
            # 直接插入模式: INSERT INTO
            insert_sql = f"""
                INSERT /*+ SET_VAR(tidb_dml_type='bulk') */ INTO {table_name} ({column_names})
                VALUES ({placeholders});
            """
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] SQL: {insert_sql}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始并行写入数据到{db_config['table']}，总记录数: {total_rows}")
        
        # 分配数据到批次
        batches = []
        for i in range(0, total_rows, batch_size):
            end = min(i + batch_size, total_rows)
            batch_data = rows[i:end]
            batches.append(batch_data)
        
        # 限制工作线程数量
        actual_workers = min(max_workers, len(batches))
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 使用 {actual_workers} 个工作线程处理 {len(batches)} 个批次")
        
        # 使用ThreadPoolExecutor并行处理批次
        inserted_count = 0
        failed_batches = 0
        
        with ThreadPoolExecutor(max_workers=actual_workers) as executor:
            # 提交所有批次任务
            future_to_batch = {
                executor.submit(
                    DataSyncUtils.batch_insert_worker, 
                    batch, 
                    insert_sql, 
                    db_config, 
                    i,
                    callback
                ): i for i, batch in enumerate(batches)
            }
            
            # 处理完成的任务
            for future in as_completed(future_to_batch):
                batch_id = future_to_batch[future]
                try:
                    data_count = future.result()
                    inserted_count += data_count
                    completion_percentage = inserted_count / total_rows * 100
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 进度: {inserted_count}/{total_rows} 条记录 ({completion_percentage:.1f}%)")
                except Exception as e:
                    failed_batches += 1
                    error_msg = f"批次 {batch_id} 处理失败: {str(e)}"
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {error_msg}")
                    warnings.append(error_msg)
        
        total_time = time.time() - start_time
        rate = inserted_count / total_time if total_time > 0 else 0
        
        summary = (
            f"数据写入完成，共写入 {inserted_count}/{total_rows} 条记录，"
            f"失败批次: {failed_batches}，"
            f"总耗时: {total_time:.2f} 秒，"
            f"平均速度: {rate:.1f} 条/秒"
        )
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {summary}")
        
        return inserted_count, total_time, warnings 