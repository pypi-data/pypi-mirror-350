from .read_file import send_message_user,send_card_message_user,read_config_file
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime
import datarecipe as dc
class QualityCheck():
    def __init__(self,database,table_name,file_id='',sql='',date_col='',start_date='',end_date=''):
        self.database = database
        self.table_name = table_name
        self.standard_name_ods= 'ods_业务/渠道_业务过程_国家_更新频率'.split('_')
        self.standard_name_tb_bi= 'tb/bi/map_业务/渠道_业务过程_stat/detail/log_国家_更新频率'.split('_')
        self.date_df=dc.fetch_table_data('cfg.yaml','s4mp','map_date_month_year')
        if sql != '':
            self.sql = sql
        else:
            self.sql = f"select * from {self.table_name}"
        try:
            self.df = dc.sql_query('cfg.yaml',self.database,self.sql)
        except:
            if file_id != '':
                read_config_file(file_id)
                self.df = dc.sql_query('cfg.yaml',self.database,self.sql)
            else:
                pass
        if date_col !='':
            self.date_col = date_col
        if start_date !='':
            self.start_date = start_date
        if end_date != '':
            self.end_date = end_date

    def check_name_database(self):
        tb = self.table_name
        seperate_table = tb.split('_')
        wrong_col = []
        right_sugg = []
        for i in range(1,len(seperate_table)):
            if seperate_table[0] == 'ods':
                
                if i == 1:
                    if seperate_table[i] in ('amz','wb','app','sc','vc'):
                        continue
                    else:
                        suggestion = f"{i} position of the table's name is {seperate_table[i]}. The {i} position for this table should be {self.standard_name_ods[i]}. Please double check it!"
                        wrong_col.append(seperate_table[i])
                        right_sugg.append(suggestion)
                elif i >1:
                    suggestion = f"{i} position of the table's name is {seperate_table[i]}. The {i} position for this table should be{self.standard_name_ods[i]}. Please carefully check it!"
                    wrong_col.append(seperate_table[i])
                    right_sugg.append(suggestion)
            elif seperate_table[0] in ('tb','bi','map'):
                if i == 1:
                    if seperate_table[i] in ('amz','wb','app','sc','vc'):
                        continue
                    else:
                        suggestion = f"{i} position of the table's name is {seperate_table[i]}. The {i} position for this table should be {self.standard_name_ods[i]}. Please double check it!"
                        wrong_col.append(seperate_table[i])
                        right_sugg.append(suggestion)
                elif i >1:
                    try:
                        suggestion = f"{i} position of the table's name is {seperate_table[i]}. The {i} position for this table should be {self.standard_name_ods[i]}. Please carefully check it!"
                        wrong_col.append(seperate_table[i])
                        right_sugg.append(suggestion)
                    except:
                        pass
            else:
                suggestion = f"{i} position of the table's name is incorrect! Please find the suitable name for this position! The enums for {i} position are ('tb','bi','map')."
                wrong_col.append(seperate_table[i])
                right_sugg.append(suggestion)
        data_frame = {'Wrong Part of Table Name':wrong_col,"Optimized Suggestion of Table Name":right_sugg}
        data = pd.DataFrame(data_frame)
        return data
                    
    def check_column_name(self):
        tb = self.table_name
        sql = f"select COLUMN_NAME,COLUMN_TYPE,COLUMN_COMMENT from information_schema.columns where table_name= '{tb}';"
        execution_query= dc.sql_query('cfg.yaml',self.database,sql)
        wrong_col = []
        right_sugg = []
        for i in range(len(execution_query)):
            col_name = execution_query['COLUMN_NAME'][i]
            if ' ' in col_name :
                suggestion = f"The column name {col_name} contains space. Please remove the space and double check it!"
                wrong_col.append(col_name)
                right_sugg.append(suggestion)
            elif col_name.lower() != col_name:
                suggestion = f"The column name {col_name} is not in lower case. Please double check it!"
                wrong_col.append(col_name)
                right_sugg.append(suggestion)
            elif col_name.startswith(' '):
                suggestion = f"The column name {col_name} starts with a space. Please remove the space and double check it!"
                wrong_col.append(col_name)
                right_sugg.append(suggestion)
            elif col_name.endswith(' '):
                suggestion = f"The column name {col_name} ends with a space. Please remove the space and double check it!"
                wrong_col.append(col_name)
                right_sugg.append(suggestion)
            elif col_name.startswith('_'):
                suggestion = f"The column name {col_name} starts with an underscore. Please remove the underscore and double check it!"
                wrong_col.append(col_name)
                right_sugg.append(suggestion)
            elif col_name.endswith('_'):
                suggestion = f"The column name {col_name} ends with an underscore. Please remove the underscore and double check it!"
                wrong_col.append(col_name)
                right_sugg.append(suggestion)
        data_frame = {'Table Name':tb,'Wrong Column Name':wrong_col,"Optimized Suggestion of Column Name":right_sugg}
        data = pd.DataFrame(data_frame)
        if len(data['Table Name'])<1:
            return 'There is no wrong column name in the table!'
        else:
            return data

    def basic_info_tb(self):
        tb = self.table_name
        sql = f"describe {tb}"
        execution_query= dc.sql_query('cfg.yaml',self.database,sql)
        col_len = execution_query['Field'].apply('nunique')
        sql_2 = f"select count(*) as cnt from {tb}"
        execution_query_2= dc.sql_query('cfg.yaml',self.database,sql_2)
        count_len = execution_query_2['cnt'][0]
        tot_len = 'The table '+str(tb)+' has '+str(col_len)+' columns'+' and '+str(count_len)+' records'
        return tot_len
    
    def check_missing_value(self):
        tb = self.df
        miss = []
        index = []
        for col in tb.columns:
            for i in range(len(tb[col])):
                if tb[col][i] is None or tb[col][i] == '':
                    miss.append(col)
                    index.append(i)
        if len(index)< 1:
            dat = f'The table {self.table_name} has no missing value!'
        else:
            data = {'miss_column':miss,'index':index}
        
            dat = pd.DataFrame(data)
        return dat
                    
    def check_primary_key(self,primary_key):
        tb = self.table_name
        database = self.database
        primary_key = str(primary_key).replace('(','').replace(')','').replace("'",'')
        primary_sql = f"""select count(*) as total_cnt,count(distinct {primary_key}) as primary_key_cnt from {tb}"""
        df_primary = dc.sql_query('cfg.yaml',database,primary_sql)
        if df_primary['total_cnt'][0] == df_primary['primary_key_cnt'][0]:
            result = '主键唯一，无重复记录。'
        else:
            result = f'主键不唯一，有重复记录。主键记录数：{df_primary["primary_key_cnt"][0]}, 全表记录数：{df_primary["total_cnt"][0]}'
        return result
    
    def check_qc(self,notification='disabled',user_id = ''):
        result_1 = self.check_name_database()
        result_2 = self.check_column_name()
        result_3 = self.check_missing_value()
        # result_4 = self.basic_info_tb()
        if notification !='disabled':
            content_1 = result_1
            send_a = send_card_message_user(user_id,content =content_1,title='Table Name of {self.table_name} QC')  
            content_2 = result_2
            send_b = send_card_message_user(user_id,content = content_2,title=f'Column Name of {self.table_name} QC')  
            content_3 = result_3
            send_c = send_card_message_user(user_id,content = content_3,title=f'Missing Value of {self.table_name}')  
            # content_4= result_4
            # send_d = send_card_message_user(user_id,content = content_4,title=f'Basic Info of {self.table_name}') 
        send = 'True'
        if send_a['msg'] != 'ok' or send_b['msg'] !='ok' or send_c['msg'] !='ok' : #or send_d['msg'] !='ok'
            send = 'False'
        return send
        
    def check_strange_data(self,checked_col,date_col,x1='',cur_start_date='',cur_end_date='',prev_start_date='',prev_end_date='',notification='disabled',user_id = ''):
        df = self.df
        df[date_col] = df[date_col].apply(lambda x:(pd.to_datetime(x)).strftime('%Y-%m-%d'))
        today = (datetime.now()).strftime('%Y-%m-%d')
        if cur_start_date=='' and cur_end_date=='':
            
            cur_start_date = today
            cur_end_date = today
        else:
            cur_start_date = (pd.to_datetime(cur_start_date)).strftime('%Y-%m-%d')
            cur_end_date = (pd.to_datetime(cur_end_date)).strftime('%Y-%m-%d')
        if prev_start_date == '' and prev_end_date == '':
            prev_start_date = (pd.to_datetime(cur_start_date)- relativedelta(days=31)).strftime('%Y-%m-%d')
            prev_end_date = (pd.to_datetime(prev_start_date)+relativedelta(days = 30)).strftime('%Y-%m-%d')
                    
        if x1 == '':
            x1 = 1.4
        
        df_cur = df.copy()
        df_cur = df_cur.loc[(df_cur[date_col]>= cur_start_date)&(df_cur[date_col]<= cur_end_date)]
        df_cur[checked_col] = df_cur[checked_col].astype('float')
        df_prev = df.copy()
        df_prev = df_prev.loc[(df_prev[date_col]>= prev_start_date)&(df_prev[date_col]<= prev_end_date)]
        df_prev[checked_col] = df_prev[checked_col].astype('float')
        count = 0
        warning = pd.DataFrame(columns=['Warning'])
        if df_prev[checked_col].max() < df_cur[checked_col].min():
            result_1 = f"Current date range {cur_start_date}-{cur_end_date}, comparing with the {prev_start_date}-{prev_end_date}, checking with the max of prev < min of current, the current date range of data is much higher than the previous date range, {df_prev[checked_col].max()}<{df_cur[checked_col].min()}, {checked_col} is out of range!"
            warning_1 = pd.DataFrame({'Warning':[result_1]})
            warning = pd.concat([warning,warning_1],axis=0)
        else:
            count += 1
        if df_cur[checked_col].max()/df_prev[checked_col].max() >= x1:
            result_2 = f"Current date range {cur_start_date}-{cur_end_date}, comparing with the {prev_start_date}-{prev_end_date}, checking with the max of current / max of prev >= {x1}, the current date range of data is {x1} higher than the previous date range, {df_cur[checked_col].max()}/{df_prev[checked_col].max()}>={x1}, {checked_col} is out of range!"
            warning_2 = pd.DataFrame({'Warning':[result_2]})
            warning = pd.concat([warning,warning_2],axis=0)
        else:
            count += 1
        if df_prev[checked_col].min()/df_cur[checked_col].min() >= x1:
            result_3 = f"Current date range {cur_start_date}-{cur_end_date}, comparing with the {prev_start_date}-{prev_end_date}, checking with the min of prev / min of current >= {x1}, the current date range of data is {x1} lower than the previous date range, {df_prev[checked_col].min()}/{df_cur[checked_col].min()}>={x1}, {checked_col} is out of range!"
            warning_3 = pd.DataFrame({'Warning':[result_3]})
            warning = pd.concat([warning,warning_3],axis=0)
        else:
            count += 1
        if  df_prev[checked_col].min() >df_cur[checked_col].max():
            result_4 = f"Current date range {cur_start_date}-{cur_end_date}, comparing with the {prev_start_date}-{prev_end_date}, checking with the min of prev > max of current, the current date range of data is much lower than the previous date range, {df_prev[checked_col].min()}>{df_cur[checked_col].max()}, {checked_col} is out of range!"
            warning_4 = pd.DataFrame({'Warning':[result_4]})
            warning = pd.concat([warning,warning_4],axis=0)
        else:
            count += 1
        if  abs(df_cur[checked_col].median()) / abs(df_prev[checked_col].median()) >= x1:
            result_5 = f"Current date range {cur_start_date}-{cur_end_date}, comparing with the {prev_start_date}-{prev_end_date}, checking with the median of current / median of prev >= {x1}, the current date range of median of data is {x1} higher than the previous date range, {df_cur[checked_col].median()}/{df_prev[checked_col].median()}>={x1}, {checked_col} is out of range!"
            warning_5 = pd.DataFrame({'Warning':[result_5]})
            warning = pd.concat([warning,warning_5],axis=0)
        else:
            count += 1
        if count == 5:
            warning = f"Current date range {cur_start_date}-{cur_end_date}, comparing with the {prev_start_date}-{prev_end_date}, {checked_col} is in the range."
        if notification != 'disabled':
            content = warning
            send_message_user(user_id,content)  
        return warning
    def check_enum(self,enum_col):
        tb = self.df
        col_enum = tb.groupby(enum_col)[enum_col].count()
        result = f"The {enum_col} has following enums:{col_enum.index}. \n Please check carefully if the enums are complete!"
        return result
    
    
    def check_missing_date(self,date_col='',start_date='',end_date='',notification='disabled',user_id=''):
        tb = self.df
        date_tb = self.date_df
        date_tb = date_tb.rename(columns = {'date':'date_map'})
        if date_col =='':
            date_col = self.date_col
        tb[date_col] = pd.to_datetime(tb[date_col]).apply(lambda x:x.strftime('%Y-%m-%d'))
        date_tb['date_map'] = pd.to_datetime(date_tb['date_map']).apply(lambda x:x.strftime('%Y-%m-%d'))
        if start_date =='':
            date_tb = date_tb[date_tb['date_map']>=tb[date_col].min()].reset_index(drop=True)
        elif start_date !='':
            date_tb = date_tb[date_tb['date_map']>=start_date].reset_index(drop=True)
        if end_date !='':
            date_tb = date_tb[date_tb['date_map']<=end_date].reset_index(drop=True)
        data_list = tb[[date_col]].drop_duplicates()
        date_tb['date_map'] = pd.to_datetime(date_tb['date_map']).apply(lambda x:x.strftime('%Y-%m-%d'))
        date_check = date_tb.merge(data_list,left_on = 'date_map',right_on = date_col,how='left')
        date_check_miss = date_check[date_check[date_col].isna()].reset_index(drop=True)
        miss_date = pd.unique(date_check_miss['date_map'])
        length = len(miss_date)
        result  = f"In {self.table_name} : The {date_col} has {length} missing dates.\n The missing dates are \n {miss_date}"
        if notification !='disabled':
            if length > 0:
                send_card = send_card_message_user(user_id,content =result,title='Missing Date QC')

        return result


