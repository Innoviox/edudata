import time
import os
import requests
import csv
from functools import reduce

star_float = lambda i: 0 if i == "*" else float(i)
def avg_level(dist):
    return reduce(lambda x, y: x + y[0] * y[1], enumerate(dist, start=1), 0)

def math_dist(row):
    return [star_float(row[f'm{i}r']) for i in range(1, 6)]

def eng_dist(row):
    return [star_float(row[f'e{i}r']) for i in range(1, 6)]

GAINS = "https://edudata.fldoe.org/ReportCards/data/Gains/{}.csv"
ACHIEV = "https://edudata.fldoe.org/ReportCards/data/Achievement/{}.csv"

rc = csv.DictReader(open("rc_base.csv"))

fields = ['County', 'School', 'id', 'Zip Code', 'Size', 'Housing Prices', 'Test Performance', 'Math Test Performance', 'English Test Performance',
          'Learning Rate', 'Math Learning Gains', 'Math Low Learning Gains', 'ELA Learning Gains', 'ELA Low Learning Gains',
          'Graduation Rates']
out = csv.DictWriter(open("edudata.csv", "w"), fieldnames=fields)
out.writeheader()

zip_reader = open("Zip_Zhvi_Summary_AllHomes.csv", 'rb')
zips = {}
for line in zip_reader:
    _, _, zc, _, _, _, _, _, zhvi, *_ = str(line)[2:-1].split(',')
    zips[zc[1:-1]] = zhvi

cz_reader = open("County_Zhvi_Summary_AllHomes.csv", "rb")
county_zhvi = {}
for line in cz_reader:
    _, _, n, st, _, _, zhvi, *_ = str(line)[2:-1].split(",")
    if st == "FL":
        county_zhvi[n.lower()[1:-1]] = zhvi
# zips = {line[1]: line["Zhvi"] for line in zip_reader}
line = 0

for row in rc:
    if row["year"] != "1819" or row["school_type"] != "High School":
        continue
    line += 1
    if line % 100 == 0:
        print("Read line", line)
    
    data = {}
    data['County'] = c = row["district_name"]
    data['School'] = row["school_name_s"]
    data['id'] = sch_id = row["school_number"]
    data['Graduation Rates'] = row["grad_rate_pct"]
    data['Size'] = row["total_students"]
    data['Zip Code'] = zc = row["PHYSICAL_ZIP"]
    
    data['Housing Prices'] = star_float(zips.get(zc.split("-")[0], 0)) / \
                             star_float(county_zhvi.get(c.lower() + " county", 1))
    
    dn = row["district_number"]
    
    gains_file = f'Gains/{dn}.csv'
    if not os.path.exists(gains_file):
        gains = requests.get(GAINS.format(dn))
        open(gains_file, "w").write(gains.text)

    gains = csv.DictReader(open(gains_file))
    for row in gains:
        if row['y'] == '1819' and \
            row['c'] == 'Total Students' and row['g'] == 'Total':
            if row['d'] == '00' and row['s'] == '0000':
                state = row
            elif row['d'] == dn and row['s'] == str(sch_id):
                data['Math Learning Gains']     = (star_float(row['mgr']) - star_float(state['mgr'])) / star_float(state['mgr'])
                data['Math Low Learning Gains'] = (star_float(row['mlr']) - star_float(state['mlr'])) / star_float(state['elr'])
                data['ELA Learning Gains']      = (star_float(row['egr']) - star_float(state['egr'])) / star_float(state['mgr'])
                data['ELA Low Learning Gains']  = (star_float(row['elr']) - star_float(state['elr'])) / star_float(state['elr'])

    data['Learning Rate'] = (data['Math Learning Gains'] + data['ELA Learning Gains']) / 2

    achiev_file = f"Achievement/{dn}.csv"
    if not os.path.exists(achiev_file):
        achiev = requests.get(ACHIEV.format(dn))
        open(achiev_file, "w").write(achiev.text)

    achiev = csv.DictReader(open(achiev_file))
    for row in achiev:
        if row['y'] == '1819' and \
            row['c'] == 'Total Students' and row['g'] == 'Total':
            if row['d'] == '00' and row['s'] == '0000':
                state = row
                state_math = avg_level(math_dist(state))
                state_eng  = avg_level(eng_dist(state))
            elif row['d'] == dn and row['s'] == str(sch_id):
                sch_math = avg_level(math_dist(row))
                sch_eng  = avg_level(eng_dist(row))

                data['Math Test Performance'] = sch_math / state_math
                data['English Test Performance'] = sch_eng / state_eng

    data['Test Performance'] = (data['Math Test Performance'] + data['English Test Performance']) / 2
    out.writerow(data)
    # break
