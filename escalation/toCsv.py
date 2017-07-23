import sqlite3
import pandas.io.sql as sql

sqlite_file = '/Users/christie/Desktop/escalation/ProcessedData.db'
conn = sqlite3.connect(sqlite_file)
table = sql.read_sql('SELECT ID, Current_Status, Severity, Regression, Reproducible, Attachment_Counts, Duration_Days, Comment_Counts, Escalation_Level FROM Defects', conn)
table.to_csv('/Users/christie/Desktop/escalation/output.csv')

# c = conn.cursor()
# c.execute('SELECT ID, Current_Status, Severity, Regression, Reproducible, Attachment_Counts, Duration_Days, Comment_Counts, Escalation_Level FROM {tn} '. \
#           format(tn='Defects'))
# all_rows = c.fetchall()
# print('1):', all_rows)

conn.close()
