import pandas as pd
import numpy as np
import sqlite3 as sql


# Baza yaratish
connection = sql.connect("banking.db")
cursor = connection.cursor()
#---------------------------------------------------------------------------------
customers_df=pd.read_csv("customers.csv")
loans_df=pd.read_csv("loans.csv")
payments_df=pd.read_csv("payments.csv")
#----------------------------------------------------------------------------------
customers_df.to_sql("customers", connection, if_exists='replace', index=False)
loans_df.to_sql("loans", connection, if_exists="replace", index=False)
payments_df.to_sql("payments", connection, if_exists="replace", index=False)
#-----------------------------------------------------------------------------------

# 1-Savol:	Kredit portfeli tarkibi: qancha jismoniy va yuridik shaxslar krediti?

query="""
SELECT 
    CASE
        WHEN c.employment_type='Business' THEN 'Yuridik_shaxslar'
        ELSE 'Jismoniy_shaxslar'
    END AS mijoz_turi,
    COUNT(l.loan_id) AS kredit_soni FROM loans l
JOIN customers c ON c.customer_id=l.customer_id
GROUP BY mijoz_turi
"""
#Natijani DF korinishida o'qiymiz.
result=pd.read_sql_query(query, connection)
print(result)
#result.to_excel("Sql_1.xlsx")   # Jadvalni excel formatda saqlab olamiz.

#-------------------------------------------------------------------------------------

#  2-Savol:  Qaysi mijoz segmentlari (yosh, daromad) eng past risk ko‘rsatkichiga ega?

query1="""
SELECT 
    c.customer_id, c.name,
    CAST(strftime('%Y', 'now') AS INTEGER) - CAST(substr(c.birth_date, -4) AS INTEGER) AS Yosh,
    c.income,
    l.status,
    AVG(CASE WHEN p.on_time=0 THEN 1 ELSE 0 END) AS Risk_koeff
FROM customers c
JOIN loans l ON l.customer_id=c.customer_id
JOIN payments p ON p.loan_id=l.loan_id
GROUP BY c.customer_id, c.name, Yosh, c.income, l.status
ORDER BY Risk_koeff
"""

# Natijani DF ko'rinishida chiqaramiz.
result1=pd.read_sql_query(query1,connection)
print(result1)

# result1.to_excel("Sql_2.xlsx", index=False)  # Excel formatida saqlaymiz

#-----------------------------------------------------------------------------------------------

# 3-Savol:	Qaysi hududlar yoki filiallar eng yuqori kredit hajmiga ega?

query3="""
SELECT c.city AS Hudud,
    sum(l.amount) AS Kredit_hajmi,
    COUNT(l.loan_id) AS Kredit_soni
FROM customers c
JOIN loans l ON l.customer_id=c.customer_id
GROUP BY  c.city
ORDER BY Kredit_hajmi DESC
"""

result3 =pd.read_sql_query(query3, connection)
print(result3)
# result3.to_excel("Sql_3.xlsx", index=False)

#-----------------------------------------------------------------------------------------------

# 4-Savol: 	Mobil banking va online xizmatlar ishlatilish darajasi?

query4 ="""
SELECT p.payment_method AS Tolov_turi,
    COUNT(p.payment_id) AS Xizmatlar_soni
FROM payments p
GROUP BY p.payment_method
ORDER BY Xizmatlar_soni
"""

result4=pd.read_sql_query(query4, connection)
print(result4)
result4.to_excel("Sql_4.xlsx", index=False)  # Excel formatida saqlab oldik.