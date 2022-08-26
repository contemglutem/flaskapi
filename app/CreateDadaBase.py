import pandas as pd
import numpy as np
import requests, zipfile
from sqlalchemy import create_engine


class DadaBase:
    # Credentials to database connection
    hostname = 'localhost'
    dbname = 'flaskapp'
    uname = "root"
    pwd = "123456"

    # Create SQLAlchemy engine to connect to MySQL Database
    def engine(self):
        return create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                             .format(host=self.hostname,
                                     db=self.dbname,
                                     user=self.uname,
                                     pw=self.pwd))

    link_csv = 'https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.KD.ZG?downloadformat=csv'
    saved_path = 'save_path.zip'

    @staticmethod
    def download_url(url, save_path, chunk_size=128):
        r = requests.get(url, stream=True)
        with open(save_path, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=chunk_size):
                fd.write(chunk)

    @staticmethod
    def open_zip_read_csv(path_reader):
        zf = zipfile.ZipFile(path_reader)
        files = np.array(zf.namelist())
        df1 = pd.read_csv(zf.open(files[0]))
        df2 = pd.read_csv(zf.open(files[1]), skiprows=3)
        df3 = pd.read_csv(zf.open(files[2]))
        return df1, df2, df3

    @staticmethod
    def transform_df1(data_frame):
        data_frame = data_frame.drop("Unnamed: 66", axis=1)
        data_frame = data_frame.melt(id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
                                     var_name="Date",
                                     value_name="Value")

        data_frame.columns = data_frame.columns.str.replace(' ', '_')
        return data_frame

    def process(self):
        self.download_url(self.link_csv, self.saved_path)
        df0 = self.open_zip_read_csv(self.saved_path)[0]
        df1 = self.open_zip_read_csv(self.saved_path)[1]
        df1 = self.transform_df1(df1)
        df2 = self.open_zip_read_csv(self.saved_path)[2].drop("Unnamed: 5", axis=1)
        df2.columns = df2.columns.str.replace(' ', '_')

        # Use SQLAlchemy engine to transfer df to MySQL Database
        df0.to_sql('metadata_indicator', self.engine(), index=True, if_exists='replace')
        df1.to_sql('api_ny', self.engine(), index=True, if_exists='replace')
        df2.to_sql('metadata_coutry', self.engine(), index=True, if_exists='replace')


if __name__ == '__main__':
    DadaBase.process(DadaBase())
