import pandas as pd
import csv

out = csv.writer(open("report.csv", "w"))
out.writerow(["School", "Amount"])

targets = ["Salary Amount for Total Personnel (instructional support services and school administration)", "Salary Amount for Teachers"]

report = pd.ExcelFile("report.xls").parse("report")
result = report.loc[report["Category"].isin(targets)]
for a in range(0, len(result), 2):
    r1, r2 = result.iloc[[a]], result.iloc[[a + 1]]
    school = r1['School'].values[0]

    try:
        amt = r2['Amount'].values[0] / r1['Amount'].values[0]
        out.writerow([school, amt])
    except ZeroDivisionError:
        print(f"Zero result for {school}")
