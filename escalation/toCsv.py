import sqlite3
import pandas.io.sql as sql
import pandas as pd
import numpy as np

sqlite_file = '/Users/christie/Desktop/escalation/ProcessedData.db'
csv_file = '/Users/christie/Desktop/escalation/output.csv'

conn = sqlite3.connect(sqlite_file)
table = sql.read_sql('SELECT ID, Current_Status, Severity, Regression, Reproducible, Attachment_Counts, Duration_Days, Comment_Counts, Escalation_Level FROM Defects', conn)
table.to_csv(csv_file)

# c = conn.cursor()
# c.execute('SELECT ID, Current_Status, Severity, Regression, Reproducible, Attachment_Counts, Duration_Days, Comment_Counts, Escalation_Level FROM {tn} '. \
#           format(tn='Defects'))
# all_rows = c.fetchall()
# print('1):', all_rows)

conn.close()

df = pd.read_csv(csv_file)
current_status = df['Current_Status']

a = np.array(current_status).astype(int)
print(a.size)
print(a.max())
b = np.zeros((a.size, a.max()+1))
b[np.arange(a.size),a] = 1
print(b)