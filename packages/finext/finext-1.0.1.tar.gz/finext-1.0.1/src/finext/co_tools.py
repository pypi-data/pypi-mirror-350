#co_tools_beta.py
from finlab import data
import finlab
import pickle
import os
import plotly.express as px
import plotly.graph_objects as go
from finlab.backtest import sim
from finlab.tools.event_study import create_factor_data
import tqdm
import numpy as np 
import pandas as pd
from finlab.dataframe import FinlabDataFrame
import cufflinks as cf
from sklearn.linear_model import LinearRegression
from datetime import datetime
from IPython.display import display, HTML
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from typing import List, Tuple, Dict
import fitz  # PyMuPDF
# import df_type

db_path = "/home/sb0487/trade/finlab/finlab_db" #資料儲存路徑



"""
程式碼傷眼滲入


"""
#若未來相關函式增多再開發
class cofindf(FinlabDataFrame):
    @property
    def pr(self):
        # 計算每行的有效值數量
        valid_counts = self.count(axis=1)
        valid_counts = valid_counts.replace(0, np.nan)
        rank_df = self.rank(axis=1, ascending=True, na_option='keep')
        pr_df = rank_df.div(valid_counts, axis=0) * 100
        return pr_df


#載入區----------------------------------------------------------------------------------------------------------------

class Codata():
    def __init__(self, df_type="findf", db_path="", force_download=False, 
                 html_file="tmp_finlab_report.html",
                 image_file_1="tmp_finlab_report_img1.png", 
                 image_file_2="tmp_finlab_report_img2.png"):
        # super().__init__()
        self.df_type = df_type
        self.db_path = db_path
        data.set_storage(data.FileStorage(db_path))
        data.use_local_data_only = False
        data.force_cloud_download = force_download

        #HTML與圖片暫存
        self.html_file = html_file
        self.image_file_1 = image_file_1
        self.image_file_2 = image_file_2
    
    def get_file_path(self,file_name): 
        return os.path.join(self.db_path, file_name.replace(":", "#") + ".pickle")

    
    def get_update_time(self,filename):
        if os.path.exists(self.get_file_path(filename)):
            modification_time = os.path.getmtime(self.get_file_path(filename))
            last_modified = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modification_time))
            print(f"最後更新時間: {last_modified}, {[filename]}")
        else:
            print("檔案不存在,請柬查路徑")

    
    def ouput_type_df(self,file_df):
        if self.df_type == "findf":
            type_df = file_df
        elif self.df_type == "cudf":
            import cudf
            type_df = cudf.DataFrame(file_df)
        elif self.df_type == "sparkdf":
            from pyspark.sql import SparkSession
            spark = SparkSession.builder.appName("Pandas to Spark DataFrame").getOrCreate()
            type_df = spark.createDataFrame(file_df)
        return type_df


    def get(self, file_name, force_download = False ):
        if not os.path.isdir(self.db_path):
            raise OSError("資料夾路徑錯誤")

        if force_download == True:
            data.force_cloud_download = True 
            type_df = data.get(file_name)
            data.force_cloud_download = False
        else:
            type_df = data.get(file_name)
            
        #選擇df輸出型態
        type_df = self.ouput_type_df(type_df)
        self.get_update_time(file_name)
        return type_df

    # @staticmethod
    # def get_update_time(filename):
    #     data.get_update_time(filename)  # 调用 data 类的 get_update_time 方法

    

#產業區----------------------------------------------------------------------------------------------------------------
    
    #把category拆成主分類與細分類
    def get_industry_pro(self):
        industry = self.get('security_industry_themes').dropna()
        def extract_majcategory(category_list):
            matching_categories = set([category.split(':')[0] for category in eval(category_list) if ':' in category])
            return str(list(matching_categories))
        
        def extract_subcategory(category_list):
            matching_categories = [category.split(':')[-1] for category in eval(category_list) if ':' in category]
            return str(matching_categories)
        
        # 应用自定义函数到 DataFrame 的每一行
        industry['maj_category'] = industry['category'].apply(extract_majcategory)
        industry['sub_category'] = industry['category'].apply(extract_subcategory)
        
        return industry

    
    def show_industry(self):
        industry = self.get_industry_pro()
        sub_category_counts_df = pd.DataFrame(industry['sub_category'].apply(eval).explode('sub_category').value_counts()).reset_index()
        maj_category_counts_df = pd.DataFrame(industry['maj_category'].apply(eval).explode('maj_category').value_counts()).reset_index()
        
        industry["maj_category"] = industry["maj_category"].apply(eval)
        industry["sub_category"] = industry["sub_category"].apply(eval)
        industry_explode = industry.explode('maj_category').explode('sub_category')
        industry_explode["count"] = 1
        
        fig = px.treemap(industry_explode, path=[px.Constant("台股產業總總覽"), "maj_category", "sub_category","name"], values='count')
        fig.update_layout(
            margin=dict(t=1, l=1, r=1, b=1)
        )
        
        fig.show()
        return maj_category_counts_df,sub_category_counts_df
    
    def filter_industry(self,file_df, keyword_list, category_type = "maj_category", remove_or_add="remove", exact_or_fuzzy="fuzzy"):
        industry_pro = self.get_industry_pro()
        
        if exact_or_fuzzy == "fuzzy":
            if remove_or_add == "remove":
                
                file_filtered_df = (file_df
                    .loc[:, ~file_df.columns.isin(
                        industry_pro[industry_pro[category_type]
                        .apply(lambda x: bool(set(eval(x)) & set(keyword_list)))]['stock_id']
                        .tolist())]
                )
           
            elif remove_or_add == "add":
                file_filtered_df = (file_df
                    .loc[:, file_df.columns.isin(
                        industry_pro[industry_pro[category_type]
                        .apply(lambda x: bool(set(eval(x)) & set(keyword_list)))]['stock_id']
                        .tolist())]
                )
    
        
        if exact_or_fuzzy == "exact":
            if remove_or_add == "remove": # 完全一樣才移除
                
                file_filtered_df = (file_df
                    .loc[:, ~file_df.columns.isin(
                        industry_pro[industry_pro[category_type]
                        .apply(lambda x: bool(set(eval(x)) == set(keyword_list)))]['stock_id']
                        .tolist())]
                )
    
            elif remove_or_add == "add": # 完全一樣才加入
                file_filtered_df = (file_df
                    .loc[:, file_df.columns.isin(
                        industry_pro[industry_pro[category_type]
                        .apply(lambda x: bool(set(eval(x)) == set(keyword_list)))]['stock_id']
                        .tolist())]
                )
        
        return file_filtered_df



    
    
    #把category拆成主分類與細分類
    def get_industry_pro(self):
        industry = self.get('security_industry_themes').dropna()
        def extract_majcategory(category_list):
            matching_categories = set([category.split(':')[0] for category in eval(category_list) if ':' in category])
            return str(list(matching_categories))
        
        def extract_subcategory(category_list):
            matching_categories = [category.split(':')[-1] for category in eval(category_list) if ':' in category]
            return str(matching_categories)
        
        # 应用自定义函数到 DataFrame 的每一行
        industry['maj_category'] = industry['category'].apply(extract_majcategory)
        industry['sub_category'] = industry['category'].apply(extract_subcategory)
        
        return industry

#便利工具區----------------------------------------------------------------------------------------------------------------

        # def month_forward_sell(self,forward_days = 1):
        #     exits_df = self.get('price:收盤價')<0
        #     def update_row(row):
        #         if row.name in self.monthly_revenue.index:
        #             return True
        #         else:
        #             return row
        
        #     rev_date = exits_df.apply(update_row, axis=1)
        #     rev_date_shifted = rev_date.shift(-1)
        #     for i in range(1,forward_days+1):
        #         rev_date_shifted_n = rev_date.shift(-i)
        #         rev_date_shifted = rev_date_shifted  | rev_date_shifted_n
                
        return rev_date_shifted
    
    #把日資料轉成月資料(營收發布截止日),他們有說之後會改成電子檔上傳日
    def day_to_month(self,file_df):
        monthly_index_df = FinlabDataFrame(index=self.get("monthly_revenue:當月營收").index)
        file_df  = monthly_index_df.join(file_df, how='left')
        return file_df

    def to_day(self,file_df):
        monthly_index_df = FinlabDataFrame(index=self.get('price:收盤價').index)
        file_df  = monthly_index_df.join(file_df, how='left')
        return file_df
    
    #轉為日資料並藉由資料異動時間點保留財報發布日資訊(index_str_to_date會向下填滿)    
    def q_to_day(self,file_df):
        file_df =file_df.index_str_to_date()
        file_df =file_df.where(file_df.ne(file_df.shift()), np.nan)
        day_index_df = FinlabDataFrame(index=self.get('price:收盤價').index)
        c = pd.concat([file_df,day_index_df])
        file_df = FinlabDataFrame(c[~c.index.duplicated()].sort_index())
        return file_df
        
    def get_pr(self, file_df):
        # 計算每行的有效值數量
        valid_counts = file_df.count(axis=1)
        valid_counts[valid_counts == 0] = np.nan
        rank_df = file_df.rank(axis=1, ascending=True, na_option='keep')
        pr_df = rank_df.div(valid_counts, axis=0) * 100
        
        return pr_df
   
    def display_report_statis(self, file_df):
        mean_return = file_df["return"].mean()
        return_std = file_df["return"].std()
        mean_period = file_df["period"].mean()
        
        # 複利報酬率計算
        log_return_mean = mean_return - 0.5 * (return_std ** 2)
        periods_per_year = 240 / mean_period
        annual_compound_return = (1 + log_return_mean) ** periods_per_year - 1
        
        # 計算勝率
        win_rate = (file_df["return"] > 0).mean()
        
        # 組成 JSON 資料 (小數位數比照 HTML)
        stats_json = {
            "交易筆數": len(file_df),
            "平均報酬率": f"{mean_return * 100:.2f}%",  # 3位小數轉百分比 = 1位小數
            "平均MDD": f"{file_df['mdd'].mean():.3f}",
            "報酬率標準差": f"{return_std:.3f}",
            "平均持有期間(交易日)": f"{mean_period:.3f}",
            "勝率": f"{win_rate * 100:.2f}%",  # 3位小數轉百分比 = 1位小數
            "最大年化報酬率(波動調整_泰勒展開)": f"{annual_compound_return * 100:.2f}%"  # 3位小數轉百分比 = 1位小數
        }
        
        html_content = """
        <sorry style="font-size: larger;">交易統計</sorry>
        <ul>
          <li>交易筆數: {}</li>
          <li>平均報酬率: {}</li>
          <li>平均MDD: {}</li>
          <li>報酬率標準差: {}</li>
          <li>平均持有期間(交易日): {}</li>
          <li>勝率: {}</li>
          <li>最大年化報酬率(波動調整_泰勒展開): {}</li>
        </ul>
        """.format(len(file_df),
                   stats_json["平均報酬率"],
                   stats_json["平均MDD"],
                   stats_json["報酬率標準差"],
                   stats_json["平均持有期間(交易日)"],
                   stats_json["勝率"],
                   stats_json["最大年化報酬率(波動調整_泰勒展開)"])
        
        display(HTML(html_content))
        return stats_json
#爬蟲區----------------------------------------------------------------------------------------------------------------------
    
    #爬年報
    def crawl_annual_report_(self,year,symbol,save_dir,sleep = 2):
        #init
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 無頭模式
        year = str(year)
        symbol = str(symbol)
        
    
        d = webdriver.Chrome(options=chrome_options)
        d.maximize_window()
    
        try:
            while True:
                d.get(f'https://doc.twse.com.tw/server-java/t57sb01?step=1&colorchg=1&co_id={symbol}&year={year}&mtype=F&dtype=F04&') 
                time.sleep(sleep)
                
                page_content = d.page_source
                if "查詢過量" in page_content:
                    print(f"當前股票為{symbol},查詢過量，被證交所檔下，休息10秒")
                    time.sleep(10)
                    continue  
                else:
                    break  # 如果没有查詢過量，退出循环
    
            pdf_link = d.find_element(By.XPATH, "//a[contains(@href, 'javascript:readfile2') and contains(@href, 'F04')]")
            pdf_link.click()
            time.sleep(sleep)
        
            # 切換分頁
            all_tabs = d.window_handles
            d.switch_to.window(all_tabs[1])
            time.sleep(sleep)
    
            
            # 找到pdf連結,注意此連結為不定時浮動
            pdf_link2 = d.find_element(By.XPATH, "//a[contains(@href, '.pdf')]")
            pdf_url = pdf_link2.get_attribute('href')
        
            
            # 建構dir(若無),保存pdf
            os.makedirs(save_dir, exist_ok=True)
            file_name = f"{year}_{symbol}.pdf" 
            file_path = os.path.join(save_dir, file_name)
            
            # 下载 PDF 文件并保存
            response = requests.get(pdf_url)
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"PDF 文件已保存到: {file_path}")
            failed_symbol =None
            
        except ModuleNotFoundError as e:
            print(f"Module not found error: {e}")
            
        except NameError as e:
            print(f"Name not defined error: {e}") 
            
        except Exception as e:
            print(f"{symbol}_{year}年年報未找到")
            failed_symbol = symbol
            
        finally:
            d.quit()
            
        return failed_symbol
    #爬年報,多個
    def crawl_annual_reports(self,year,stock_list,save_dir,sleep = 2):
        failed_list = list(filter(None, (self.crawl_annual_report_(year, x, save_dir, sleep) for x in stock_list)))
        return failed_list
        
    #爬季報
    def crawl_quarterly_report_(self,year,quarter,symbol,save_dir,sleep = 2):
        
        #init
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 無頭模式
        year = str(year)
        symbol = str(symbol)
        format_quarter = "0"+str(quarter)
        ad = str(int(year)+1911)
        # 初始化Chrome瀏覽器
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
    
        d = webdriver.Chrome(options=chrome_options)
        d.maximize_window()
    
        try:
            while True:
                d.get(f'https://doc.twse.com.tw/server-java/t57sb01?step=1&colorchg=1&co_id={symbol}&year={year}&seamon=&mtype=A&dtype=AI1&') 
                time.sleep(sleep)
                
                page_content = d.page_source
                if "查詢過量" in page_content:
                    print(f"當前股票為{symbol},查詢過量，被證交所檔下，休息10秒")
                    time.sleep(10)
                    continue  
                else:
                    break  # 如果没有查詢過量，退出循环
           
            pdf_name = f"{ad}{format_quarter}_{symbol}_AI1.pdf"
            pdf_link = d.find_element(By.XPATH, f"//a[contains(@href, 'javascript:readfile2') and contains(@href,'{pdf_name}')]")
            pdf_link.click()
            time.sleep(sleep)
        
            # 切換分頁
            all_tabs = d.window_handles
            d.switch_to.window(all_tabs[1])
            time.sleep(sleep)
    
            # 找到pdf連結,注意此連結為不定時浮動
            pdf_link2 = d.find_element(By.XPATH, "//a[contains(@href, '.pdf')]")
            pdf_url = pdf_link2.get_attribute('href')
        
            
            # 建構dir(若無),保存pdf
            os.makedirs(save_dir, exist_ok=True)
            file_name = f"{year}_Q{quarter}_{symbol}.pdf" 
            file_path = os.path.join(save_dir, file_name)
            
            # 下载 PDF 文件并保存
            response = requests.get(pdf_url)
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"PDF 文件已保存到: {file_path}")
            failed_symbol =None
            
        except ModuleNotFoundError as e:
            print(f"Module not found error: {e}")
            
        except NameError as e:
            print(f"Name not defined error: {e}") 
        
        except:
            print(f"{symbol}_{year}_Q{quarter}季報未找到")
            failed_symbol = symbol
            
        finally:
            d.quit()
        return failed_symbol
    #爬季報,多個
    def crawl_quarterly_reports(self,year,quarter,stock_list,save_dir,sleep = 2):
        failed_list = list(filter(None, (self.crawl_quarterly_report_(year,quarter, x, save_dir, sleep) for x in stock_list)))
        return failed_list


    #用save_dir抓下來的檔案與全部的股票代號清單all_stock_list比較,找出尚未下載的pdf
    def get_undownloaded_stocks(self,save_dir,all_stock_list):
        download_stock_list = [f.split('.')[0][-4:] for f in os.listdir(save_dir) if os.path.isfile(os.path.join(save_dir, f))]
        result = [elem for elem in all_stock_list if elem not in download_stock_list]
        return result

#讀檔pdf區----------------------------------------------------------------------------------------------------------------------
    
    #用spark分散式讀取
    def load_pdf_spark(self,stock_list,pdf_path,memory = "5g"):
        from pyspark.sql import SparkSession
        
        # 起 Spark
        spark = SparkSession.builder.appName("Read PDFs with Spark")\
        .config("spark.driver.memory", memory)\
        .config("spark.driver.maxResultSize", memory)\
        .getOrCreate() # 內存大小
    
        def process_pdf(filename):
            if filename.endswith('.pdf'):
                #stock_symbol = filename.split('_')[1].split('.')[0] # 分割,取出股票代耗
                stock_symbol = filename.split('.')[0][-4:]
                if stock_symbol in stock_list: 
                    file_path = os.path.join(pdf_path, filename)
                    content = "".join(page.get_text() for page in fitz.open(file_path)) #打開pdf, 逐行讀取並合併
                    return stock_symbol, content
    
        # 使用 Spark 讀取每個 PDF 文件
        pdf_contents = spark.sparkContext.parallelize(os.listdir(pdf_path)).map(process_pdf).filter(lambda x: x).collect()
        
        # 將結果轉換為 Pandas DataFrame
        pdf_df = pd.DataFrame(pdf_contents, columns=["Stock Symbol", "PDF Content"]).set_index("Stock Symbol")
        return pdf_df

    #單線程讀取
    def load_pdf(self,stock_list, pdf_path):
        def process_pdf(filename):
            if filename.endswith('.pdf'):
                stock_symbol = filename.split('.')[0][-4:]
                if stock_symbol in stock_list:
                    file_path = os.path.join(pdf_path, filename)
                    content = "".join(page.get_text() for page in fitz.open(file_path))  
                    return stock_symbol, content
        
        pdf_contents = [process_pdf(filename) for filename in os.listdir(pdf_path) if filename.endswith('.pdf')]
        pdf_contents = [item for item in pdf_contents if item is not None]
        
        # 将结果转换为 Pandas DataFrame
        pdf_df = pd.DataFrame(pdf_contents, columns=["Stock Symbol", "PDF Content"]).set_index("Stock Symbol")
        return pdf_df

#相關係數區----------------------------------------------------------------------------------------------------------------------

    # 相關數排名
    def get_corr_ranked(self,stock_symbol: str, close: pd.DataFrame) -> None:
        stock_symbol = str(stock_symbol)
        correlation_with_target = close.corr()[stock_symbol].drop(stock_symbol)
        most_related = correlation_with_target.nlargest(30)
        least_related = correlation_with_target.nsmallest(30)
        
        for title, data in [("Most", most_related), ("Least", least_related)]:
            fig = px.bar(data, title=f'Top 30 Stocks {title} Related to {stock_symbol}', labels={'value': 'Correlation', 'index': 'Stocks'})
            fig.show()

    # 時間序列比較圖
    def get_tm_series_chart(self,stock_symbols: list, close: pd.DataFrame, lag: int = 0) -> None:
        stock1, stock2 = map(str, stock_symbols)
        
        if lag > 0:
            shifted_stock2 = close[stock2].shift(lag)
            valid_idx = ~shifted_stock2.isna()
            stock2_values = shifted_stock2[valid_idx]
            stock1_values = close[stock1][valid_idx]
        else:
            stock1_values = close[stock1]
            stock2_values = close[stock2]
        
        correlation = stock1_values.corr(stock2_values)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(x=close.index, y=close[stock1], mode='lines', name=stock1, yaxis='y1'))
        fig.add_trace(go.Scatter(x=close.index, y=shifted_stock2 if lag > 0 else close[stock2], mode='lines', name=f'{stock2} (lag={lag})', yaxis='y2'))
        
        fig.update_layout(
            title=f'時間序列比較圖 (lag={lag}, correlation={correlation:.2f})',
            xaxis=dict(title='日期'),
            yaxis=dict(title=f'{stock1} 收盤價', side='left'),
            yaxis2=dict(title=f'{stock2} 收盤價', side='right', overlaying='y')
        )
        
        fig.show()

#因子測試區----------------------------------------------------------------------------------------------------------------------



    def get_quartertly_factor_analysis(self,factor_list: List[str], pr: Tuple[int, int], n_high_or_low: int)-> pd.DataFrame:
        close = self.get('price:收盤價')
        market_value = self.get('etl:market_value')
        
        # Initialize DataFrame to store results
        factor_report_df_all = pd.DataFrame(columns=[
            "因子名稱", "策略條件", "PR_Range", "限制因子數值正負", "創n期高or低", "總交易筆數", 
            "策略年化報酬率", "策略MDD", "策略sortino(日)", "個股平均報酬率", "個股平均MDD", 
            "個股報酬率標準差", "個股平均持有期間(交易日)", "個股平均處於獲利天數", 
            "個股最大年化複利報酬"
        ])
    
        def calculate_factor_report(conditions: pd.DataFrame, factor_name: str, strategy_type: str, pr: Tuple[int, int], pn: str, n_high_or_low: int):
            pr_range = np.nan
            if strategy_type in ["qoq", "yoy", "factor_market_value_ratio","origin_value"]:
                n_high_or_low = np.nan
                pr_range = f"{pr[0]}-{pr[1]}"
            
            try:
                # Simulate strategy and generate report
                report = sim(position=conditions, position_limit=1, fee_ratio=1.425/1000*0.2, trade_at_price="open",upload=False)
                trades = report.get_trades()
                
                report_data = {
                    '因子名稱': factor_name,
                    '策略條件': strategy_type,
                    'PR_Range': pr_range,
                    '限制因子數值正負': pn,
                    '創n期高or低': n_high_or_low,
                    '總交易筆數': len(trades),
                    '策略年化報酬率': report.get_stats()["cagr"],
                    '策略MDD': report.get_stats()["max_drawdown"],
                    '策略sortino(日)': report.get_stats()["daily_sortino"],
                    '個股平均報酬率': trades["return"].mean(),
                    '個股平均MDD': trades["mdd"].mean(),
                    '個股報酬率標準差': trades["return"].std(),
                    '個股平均持有期間(交易日)': trades["period"].mean(),
                    '個股平均處於獲利天數': trades["pdays"].mean(),
                    '個股最大年化複利報酬': (1 + trades["return"].mean()) ** (240 / trades["period"].mean()) - 1,
                }
                return pd.DataFrame([report_data])
            except Exception:
                return None
    
        def generate_conditions(factor_df : pd.DataFrame, strategy_type: str, pr: Tuple[int, int], pn: str, n_high_or_low: int):
            pr_down, pr_up = pr
            conditions = None
            
            if pn == "pos":
                if strategy_type == "qoq":
                    conditions = (
                        (self.get_pr(factor_df / factor_df.shift(1)) > pr_down) & 
                        (self.get_pr(factor_df / factor_df.shift(1)) < pr_up) &
                        (factor_df > 0) & (close > 0)
                    )
                elif strategy_type == "yoy":
                    conditions = (
                        (self.get_pr(factor_df / factor_df.shift(4)) > pr_down) & 
                        (self.get_pr(factor_df / factor_df.shift(4)) < pr_up) &
                        (factor_df > 0) & (close > 0)
                    )
                elif strategy_type == "higest":
                    conditions = (factor_df == factor_df.rolling(n_high_or_low).max()) & (factor_df > 0) & (close > 0)
                elif strategy_type == "factor_market_value_ratio":
                    factor_market_value_ratio = factor_df / market_value
                    conditions = (
                        (self.get_pr(factor_market_value_ratio / factor_market_value_ratio.shift(4)) > pr_down) & 
                        (self.get_pr(factor_market_value_ratio / factor_market_value_ratio.shift(4)) < pr_up) &
                        (factor_df > 0) & (close > 0)
                    )
                elif strategy_type == "lowest":
                    conditions = (factor_df == factor_df.rolling(n_high_or_low).min()) & (factor_df > 0) & (close > 0)
                elif strategy_type == "origin_value":
                    conditions = (self.get_pr(factor_df)>pr_down) & (self.get_pr(factor_df)<pr_up)& (factor_df > 0) & (close > 0)
                    
            elif pn == "neg":
                if strategy_type == "qoq":
                    conditions = (
                        (self.get_pr(factor_df / factor_df.shift(1)) > pr_down) & 
                        (self.get_pr(factor_df / factor_df.shift(1)) < pr_up) &
                        (factor_df < 0) & (close > 0)
                    )
                elif strategy_type == "yoy":
                    conditions = (
                        (self.get_pr(factor_df / factor_df.shift(4)) > pr_down) & 
                        (self.get_pr(factor_df / factor_df.shift(4)) < pr_up) &
                        (factor_df < 0) & (close > 0)
                    )
                elif strategy_type == "higest":
                    conditions = (factor_df == factor_df.rolling(n_high_or_low).max()) & (factor_df < 0) & (close > 0)
                elif strategy_type == "factor_market_value_ratio":
                    factor_market_value_ratio = factor_df / market_value
                    conditions = (
                        (self.get_pr(factor_market_value_ratio / factor_market_value_ratio.shift(4)) > pr_down) & 
                        (self.get_pr(factor_market_value_ratio / factor_market_value_ratio.shift(4)) < pr_up) &
                        (factor_df < 0) & (close > 0)
                    )
                elif strategy_type == "lowest":
                    conditions = (factor_df == factor_df.rolling(n_high_or_low).min()) & (factor_df < 0) & (close > 0)
                elif strategy_type == "origin_value":
                    conditions = (self.get_pr(factor_df)>pr_down) & (self.get_pr(factor_df)<pr_up)& (factor_df < 0) & (close > 0)
                    
            return conditions
    
        def run_factor_analysis(factor_list, strategy_types, pos_neg_options, pr, n_high_or_low):
            factor_report_df_all = pd.DataFrame()
            for factor in factor_list:
                factor_df = self.get(factor)
                factor_name = factor.split(":")[1]
                
                for strategy_type in strategy_types:
                    for pn in pos_neg_options:
                        conditions = generate_conditions(factor_df, strategy_type, pr, pn, n_high_or_low)
                        report_df = calculate_factor_report(conditions, factor_name, strategy_type, pr, pn, n_high_or_low)
                        
                        if report_df is not None:
                            factor_report_df_all = pd.concat([factor_report_df_all, report_df])
            
            return factor_report_df_all
    
        # Run the analysis loop
        strategy_types = ["qoq", "yoy", "higest", "factor_market_value_ratio", "lowest","origin_value"]
        pos_neg_options = ["pos", "neg"]
        factor_report_df_all = run_factor_analysis(factor_list, strategy_types, pos_neg_options, pr, n_high_or_low)
        
        return factor_report_df_all.reset_index(drop=True)



#tg----------------------------------------------------------------------------------------------------------------------


# 在 co_tools_beta.py 的 Codata 類中添加以下方法

    def tg_extract_position_info(self, report):
        """提取持倉資訊
        
        Args:
            report: finlab 回測報告物件
            
        Returns:
            tuple: (進場股票列表, 持有股票列表, 出場股票列表, 最後日期)
        """
        trades = report.get_trades()
        last_date = report.daily_benchmark.index[-1]
        position_info = report.position_info2()
        
        if isinstance(position_info, dict) and 'positions' in position_info:
            positions = position_info['positions']
        else:
            positions = []
        
        enter_stocks = []
        hold_stocks = []
        exit_stocks = []
        
        for position in positions:
            if not isinstance(position, dict):
                continue
                
            asset_id = position.get('assetId', '')
            asset_name = position.get('assetName', '')
            stock_display = f"{asset_id} {asset_name}" if asset_id and asset_name else (asset_id or asset_name)
            
            action_type = position.get('action', {}).get('type', '')
            current_weight = position.get('currentWeight', 0)
            
            # 忽略過去的交易記錄
            if action_type == 'exit_p':
                continue
                
            # 根據動作類型分類
            if action_type == 'entry':
                enter_stocks.append(stock_display)
            elif current_weight != 0:
                hold_stocks.append(stock_display)
                if action_type == 'exit':
                    exit_stocks.append(stock_display)
        
        return enter_stocks, hold_stocks, exit_stocks, last_date
    
    def tg_generate_strategy_message(self, report, strategy_config):
        """生成策略 Telegram 訊息
        
        Args:
            report: finlab 回測報告物件
            strategy_config: 策略配置字典，包含以下鍵值：
                - name: 策略名稱
                - description: 策略說明
                - author: 策略作者
                - direction: 策略多空方向 (多/空)
                - notes: 策略備註 (可選)
                - enter_label: 進場標籤 (可選)
                - hold_label: 持倉標籤 (可選)
                - exit_label: 出場標籤 (可選)
                
        Returns:
            str: 格式化的 Telegram 訊息
        """
        # 提取持倉資訊
        trades = report.get_trades()
        enter_stocks, hold_stocks, exit_stocks, last_date = self.tg_extract_position_info(report)
        
        # 獲取統計數據
        stats_dict = self.display_report_statis(trades)
        
        # 處理策略配置預設值
        direction = strategy_config.get('direction', '多')
        notes = strategy_config.get('notes', '')
        
        # 根據多空方向設定標籤
        if direction == '空':
            enter_label = strategy_config.get('enter_label', '放空股票')
            exit_label = strategy_config.get('exit_label', '回補股票')
        else:
            enter_label = strategy_config.get('enter_label', '買入股票')
            exit_label = strategy_config.get('exit_label', '賣出股票')
        
        hold_label = strategy_config.get('hold_label', '當前持倉')
        
        # 生成訊息
        msg = f"""🔔🔔🔔<b>策略通知</b>
<pre>策略名稱: {strategy_config['name']}
策略說明: {strategy_config['description']}
策略作者: {strategy_config['author']}
策略多空: {direction}
策略備註: {notes}

預定換股日: {last_date}

📈
{enter_label}: {enter_stocks}
{hold_label}: {hold_stocks}
{exit_label}: {exit_stocks}

🔢
總交易筆數: {stats_dict["交易筆數"]}
平均報酬率: {stats_dict["平均報酬率"]}
平均持有天數: {stats_dict["平均持有期間(交易日)"]}
勝率: {stats_dict["勝率"]}
最大年化報酬率(波動調整_泰勒展開): {stats_dict["最大年化報酬率(波動調整_泰勒展開)"]}</pre>"""
 
        
        return msg.strip()
    
    def tg_create_strategy_message_quick(self, report, strategy_name, strategy_description, 
                                    strategy_author, strategy_direction="多", 
                                    strategy_notes="", **kwargs):
        """快速創建策略訊息的便利方法
        
        Args:
            report: finlab 回測報告
            strategy_name: 策略名稱
            strategy_description: 策略說明
            strategy_author: 策略作者
            strategy_direction: 策略方向 (多/空)
            strategy_notes: 策略備註
            **kwargs: 其他自定義標籤
            
        Returns:
            str: 格式化的 Telegram 訊息
        """
        strategy_config = {
            'name': strategy_name,
            'description': strategy_description,
            'author': strategy_author,
            'direction': strategy_direction,
            'notes': strategy_notes,
            **kwargs
        }
        
        return self.tg_generate_strategy_message(report, strategy_config)

    def tg_capture_report_images(self, html_filename=None, 
                                 output_image1=None,
                                 output_image2=None):
        """
        同步版本的 HTML 轉圖片方法
        
        Args:
            html_filename: HTML 檔案名稱 (None 則使用預設)
            output_image1: 第一張截圖檔名 (None 則使用預設)
            output_image2: 第二張截圖檔名 (None 則使用預設)
        """
        import asyncio
        
        # 使用預設值或傳入值
        html_filename = html_filename or self.html_file
        output_image1 = output_image1 or self.image_file_1
        output_image2 = output_image2 or self.image_file_2
        
        if not os.path.exists(html_filename):
            print(f"錯誤: HTML 檔案 '{html_filename}' 不存在")
            return False
        
        try:
            asyncio.run(self.tg_capture_html_to_image(html_filename, output_image1, output_image2))
            return True
        except Exception as e:
            print(f"截圖失敗: {e}")
            return False

    
    async def tg_capture_html_to_image(self, html_file_path, output_image_path1, output_image_path2, 
                                       browser_type='chromium', full_page=True, 
                                       viewport_width=1920, viewport_height=1080):
        """
        將本地 HTML 檔案轉換為圖片
        
        Args:
            html_file_path: HTML 檔案路徑
            output_image_path1: 第一張截圖路徑（原始頁面）
            output_image_path2: 第二張截圖路徑（點選後頁面）
            browser_type: 瀏覽器類型 ('chromium', 'firefox', 'webkit')
            full_page: 是否截取完整頁面
            viewport_width: 視窗寬度
            viewport_height: 視窗高度
        """
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            # 啟動瀏覽器
            if browser_type == 'chromium':
                browser = await p.chromium.launch()
            elif browser_type == 'firefox':
                browser = await p.firefox.launch()
            elif browser_type == 'webkit':
                browser = await p.webkit.launch()
            else:
                raise ValueError("不支援的瀏覽器類型")
            
            # 轉換為絕對路徑
            abs_html_file_path = os.path.abspath(html_file_path)
            file_url = f"file:///{abs_html_file_path.replace(os.sep, '/')}"
            print(f"正在開啟: {file_url}")
            
            page = await browser.new_page()
            await page.set_viewport_size({"width": viewport_width, "height": viewport_height})
            
            try:
                # 載入頁面
                await page.goto(file_url, wait_until="networkidle")
                await page.wait_for_timeout(2000)
                
                # 第一次截圖：原始頁面
                print(f"正在擷取原始頁面到: {output_image_path1}")
                await page.screenshot(path=output_image_path1, full_page=full_page)
                
                # 尋找選股按鈕 - 使用多種選擇器嘗試
                selectors = [
                    'a:has-text("選股")',  # 簡單文字選擇器
                    'a[role="tab"]:has-text("選股")',  # 帶role屬性
                    '.tab:has-text("選股")',  # class選擇器
                    'a.tab-active:has-text("選股")',  # 原始選擇器
                ]
                
                element_found = False
                for selector in selectors:
                    try:
                        print(f"嘗試選擇器: {selector}")
                        await page.wait_for_selector(selector, timeout=5000)
                        print(f"找到選股按鈕，正在點選...")
                        await page.click(selector)
                        element_found = True
                        break
                    except Exception as e:
                        print(f"選擇器 {selector} 失敗: {e}")
                        continue
                
                if not element_found:
                    print("無法找到選股按鈕，列出所有可能的選項...")
                    # 列出所有包含"選股"的元素
                    elements = await page.query_selector_all('*')
                    for element in elements[:20]:  # 只檢查前20個元素避免太多輸出
                        text = await element.text_content()
                        if text and "選股" in text:
                            tag_name = await element.evaluate('el => el.tagName')
                            class_name = await element.get_attribute('class')
                            print(f"找到包含'選股'的元素: {tag_name}, class: {class_name}, text: {text}")
                    
                    # 嘗試直接點擊任何包含"選股"文字的元素
                    try:
                        await page.click('text=選股')
                        element_found = True
                        print("使用 text=選股 成功點擊")
                    except:
                        print("所有方法都失敗")
                
                if element_found:
                    await page.wait_for_timeout(2000)  # 等待頁面更新
                    
                    # 第二次截圖：點選後
                    print(f"正在擷取選股後頁面到: {output_image_path2}")
                    await page.screenshot(path=output_image_path2, full_page=full_page)
                    print("擷取成功！")
                else:
                    print("無法點擊選股按鈕，只保存原始截圖")
                    
            except Exception as e:
                print(f"發生錯誤: {e}")
                # 除錯：印出頁面內容
                try:
                    html_content = await page.content()
                    print("頁面 HTML 內容片段：", html_content[:500])
                except:
                    print("無法取得頁面內容")
                    
            finally:
                await browser.close()

    def tg_send_photo(self, bot_token, channel_ids, photo_path, caption=""):
        """
        發送圖片到 Telegram
        
        Args:
            bot_token: Bot token
            channel_ids: 頻道ID列表
            photo_path: 圖片路徑
            caption: 圖片說明
            
        Returns:
            dict: 發送結果
        """
        if not os.path.exists(photo_path):
            print(f"圖片檔案不存在: {photo_path}")
            return {}
            
        url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
        results = {}
        
        for cid in channel_ids:
            try:
                with open(photo_path, 'rb') as photo:
                    files = {'photo': photo}
                    data = {'chat_id': cid, 'caption': caption}
                    resp = requests.post(url, files=files, data=data)
                    results[cid] = resp.status_code
                    
                    if resp.status_code != 200:
                        print(f"發送圖片至 {cid} 失敗: {resp.text}")
                    else:
                        print(f"圖片成功發送至 {cid}")
                        
            except Exception as e:
                print(f"發送圖片至 {cid} 發生錯誤: {e}")
                results[cid] = 0
                
        return results

    def tg_clean_files(self, clean_html=True, clean_images=True):
        """
        清理產生的檔案
        
        Args:
            clean_html: 是否刪除 HTML 檔案
            clean_images: 是否刪除圖片檔案
        """
        files_to_clean = []
        
        if clean_html and os.path.exists(self.html_file):
            files_to_clean.append(self.html_file)
            
        if clean_images:
            if os.path.exists(self.image_file_1):
                files_to_clean.append(self.image_file_1)
            if os.path.exists(self.image_file_2):
                files_to_clean.append(self.image_file_2)
        
        cleaned_files = []
        for file_path in files_to_clean:
            try:
                os.remove(file_path)
                cleaned_files.append(file_path)
                print(f"已刪除檔案: {file_path}")
            except Exception as e:
                print(f"刪除檔案 {file_path} 失敗: {e}")
                
        return cleaned_files

    def tg_generate_and_send_complete(self, report, strategy_config, bot_token, channel_ids, 
                                      send_images=True, clean_files=True, 
                                      clean_html=True, clean_images=True):
        """
        完整的策略推送流程：生成訊息 -> 截圖 -> 發送 -> 清理
        
        Args:
            report: finlab 回測報告
            strategy_config: 策略配置
            bot_token: Bot token
            channel_ids: 頻道ID列表
            send_images: 是否發送圖片
            clean_files: 是否清理檔案
            clean_html: 是否刪除 HTML 檔案
            clean_images: 是否刪除圖片檔案
            
        Returns:
            dict: 執行結果
        """
        results = {'message_sent': False, 'images_sent': [], 'files_cleaned': []}
        
        try:
            # 1. 生成文字訊息並發送
            msg = self.tg_generate_strategy_message(report, strategy_config)
            
            # 發送文字訊息
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            for cid in channel_ids:
                payload = {"chat_id": cid, "text": msg, "parse_mode": "HTML"}
                resp = requests.post(url, json=payload)
                if resp.status_code == 200:
                    results['message_sent'] = True
                    print(f"文字訊息成功發送至 {cid}")
                else:
                    print(f"文字訊息發送至 {cid} 失敗: {resp.text}")
            
            # 2. 如果需要發送圖片
            if send_images:
                # 生成截圖
                if self.tg_capture_report_images():
                    # 發送第一張圖片
                    if os.path.exists(self.image_file_1):
                        result1 = self.tg_send_photo(bot_token, channel_ids, self.image_file_1, "策略報告 - 原始頁面")
                        if any(status == 200 for status in result1.values()):
                            results['images_sent'].append(self.image_file_1)
                    
                    # 發送第二張圖片
                    if os.path.exists(self.image_file_2):
                        result2 = self.tg_send_photo(bot_token, channel_ids, self.image_file_2, "策略報告 - 選股頁面")
                        if any(status == 200 for status in result2.values()):
                            results['images_sent'].append(self.image_file_2)
                else:
                    print("截圖失敗，跳過圖片發送")
            
            # 3. 清理檔案
            if clean_files:
                cleaned = self.tg_clean_files(clean_html, clean_images)
                results['files_cleaned'] = cleaned
                
        except Exception as e:
            print(f"完整推送流程發生錯誤: {e}")
            
        return results



