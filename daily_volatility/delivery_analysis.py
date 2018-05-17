import os
import pandas as pd

class DeliveryAnalysis:
    def __init__(self, stock_name='PNB'):
        self.resource_path = r'../resources/'
        self.stock_name = stock_name
        pass

    def get_deleverables_file_paths(self):
        file_list = os.listdir(self.resource_path)
        file_list = [file_name for file_name in file_list if '_deleverables.csv' in file_name]
        file_path = ['{}{}'.format(self.resource_path,file_path) for file_path in file_list]
        print file_path
        return file_path

    def build_stock_deleverables_df(self):
        file_path_list = self.get_deleverables_file_paths()
        master_df = None
        try:
            for file_path in file_path_list:
                temp_df = pd.read_csv(file_path)
                if not master_df:
                    cols = temp_df.columns

                    master_df = pd.DataFrame(columns=cols)
                row_df = temp_df[temp_df['SYMBOL'] == self.stock_name]
                print row_df, type(row_df)
                master_df.append(row_df.iloc[[0]])
            print"abc", master_df, row_df.iloc[[0]]
        except Exception as e:
            print e.message


DeliveryAnalysis().build_stock_deleverables_df()