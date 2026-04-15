#---Kerakli kutubxonalar---------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

from  python_questions import appointments, billing, doctors, medications, patients, services
#------------------------------------------------------------------------------------------
connection=sqlite3.connect("test.db")
cursor=connection.cursor()
#-----------------------------------------------------------------------------------------
billing.to_sql("billing", connection, if_exists='replace', index=False)
services.to_sql("services", connection, if_exists='replace', index=False)
appointments.to_sql('appointments', connection, if_exists='replace', index=False)
medications.to_sql("medications", connection, if_exists='replace', index=False)
#----------------------------------------------------------------------------------------------

# 40.	[SQL] Eng ko'p talab qilinadigan tibbiy xizmatlar qaysilar?
query="""
    SELECT services.service_name, 
    COUNT(billing.billing_id) AS Umumiy_tolovlar_soni,
    SUM(billing.amount) AS Umumiy_summa,
    SUM(CASE WHEN payment_status = "To\'langan" THEN 1 ELSE 0 END) AS Tolangan,
    SUM(CASE WHEN payment_status = 'Bekor qilingan' THEN 1 ELSE 0 END) AS Bekor_qilingan,
    SUM(CASE WHEN payment_status = 'Qisman' THEN 1 ELSE 0 END) AS Qisman,
    SUM(CASE WHEN payment_status = 'Kutilmoqda' THEN 1 ELSE 0 END) AS Kutilmoqda,
    SUM(services.duration_minutes) AS Umumiy_davomiylik_minutes
    FROM billing INNER JOIN services ON billing.service_id=services.service_id
    GROUP BY services.service_name
    ORDER BY Umumiy_tolovlar_soni DESC LIMIT 10  ;
"""
top_tibbiy_xizmatlar=pd.read_sql_query(query, connection)
##top_tibbiy_xizmatlar.to_excel("top_tibbiy_xizmatlar.xlsx", index=False)
print(top_tibbiy_xizmatlar)

# 45.	[SQL] Qaysi kasalliklar eng ko'p uchraydi va mavsumiy tendentsiyasi?

query1="""
SELECT a.diagnosis, COUNT(a.appointment_id) AS Soni
FROM appointments AS a
WHERE diagnosis <> 'Unknown'
GROUP BY a.diagnosis
ORDER BY Soni DESC LIMIT 10;
"""
top_kasalliklar=pd.read_sql_query(query1, connection )
###top_kasalliklar.to_excel("top_kasalliklar_tendensiyasi.xlsx", index=False)

print(top_kasalliklar)

query2="""
SELECT diagnosis,
strftime("%Y", appointment_date) AS Yil,
strftime("%m", appointment_date) AS Oy,
COUNT(*) AS Soni
FROM appointments WHERE diagnosis <> 'Unknown'
GROUP BY diagnosis, Yil, Oy 
ORDER BY diagnosis, Yil, Oy ;
"""

mavsumiy_tendensiya=pd.read_sql_query(query2, connection)
print(mavsumiy_tendensiya)

query3="""
SELECT 
    diagnosis,
    CASE 
        WHEN STRFTIME('%m', appointment_date) IN ('12','01','02') THEN 'Qish'
        WHEN STRFTIME('%m', appointment_date) IN ('03','04','05') THEN 'Bahor'
        WHEN STRFTIME('%m', appointment_date) IN ('06','07','08') THEN 'Yoz'
        WHEN STRFTIME('%m', appointment_date) IN ('09','10','11') THEN 'Kuz'
    END AS mavsum,
    COUNT(*) AS soni
FROM appointments WHERE diagnosis <> 'Unknown'
GROUP BY  diagnosis ,mavsum
ORDER BY  diagnosis, mavsum ;
"""
fasliy_tendensiya=pd.read_sql_query(query3, connection)
print(fasliy_tendensiya)
#----------------------------------------------------------------------------------------------------

# 48.	[SQL] Dorilar va tibbiy materiallar xarajatlari qanday?

query4="""
SELECT medication_name ,
    COUNT(*) AS buyurtmalar_soni,
    ROUND(SUM(cost), 2) AS umumiy_xarajatlar
FROM medications 
GROUP BY medication_name
ORDER BY umumiy_xarajatlar DESC 
"""

dorilar_xarajatlari=pd.read_sql_query(query4, connection)
print(dorilar_xarajatlari)
##dorilar_xarajatlari.to_excel("dorilar_xarajatlari_48.xlsx", index=False)

##-----------------------------------------------------------------------------------------------------
# 51.	[SQL] Qaysi demografik guruhlar (yosh, jins) eng ko'p tashrif buyuradi?
print(patients['gender'].value_counts())

query5="""
SELECT p.gender,
(CAST(strftime('%Y', a.appointment_date) AS INTEGER)-
CAST(strftime('%Y', p.birth_date) AS INTEGER)) AS Yosh,
COUNT(a.appointment_id) as Soni
FROM appointments as a 
INNER JOIN patients as p ON a.patient_id=p.patient_id
WHERE gender <> 'UNKNOWN'
GROUP BY p.gender, Yosh ORDER BY Soni  DESC ;
"""
gender_difference =pd.read_sql_query(query5, connection)
##gender_difference.to_excel("jins_yosh_tashriflar.xlsx", index=False)
print(gender_difference)

