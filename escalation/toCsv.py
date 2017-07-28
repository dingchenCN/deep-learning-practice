import sqlite3
import pandas.io.sql as sql
import pandas as pd
import numpy as np

# sqlite_file = '/Users/christie/Desktop/escalation/ProcessedData.db'
sqlite_file = 'C:/Users/dingc/Downloads/ProcessedData/ProcessedData.db'
csv_file = 'output.csv'
oneHot_csv_file = 'oneHot.csv'

conn = sqlite3.connect(sqlite_file)
table = sql.read_sql('SELECT ID, Current_Status, Severity, Regression, Reproducible, Attachment_Counts, Comment_Counts, Escalation_Level FROM Defects', conn)
table.to_csv(csv_file)
conn.close()

df = pd.read_csv(csv_file)
df_1hot = pd.read_csv(oneHot_csv_file)
current_status = df['Current_Status']

a = np.array(current_status).astype(int)
b = np.zeros((a.size, a.max()+1))
b[np.arange(a.size), a] = 1
