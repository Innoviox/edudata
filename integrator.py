import csv

dest_file = "edudata.csv"
_data = map(lambda i: str(i)[2:-1].split(","), open("edudata.csv", "rb").read().split(b"\n"))
data = []
for i in _data:
    data.append(i[:-1])
    data[-1].append(i[-1][:-2])
headers, *dest_data = data
headers[0] = headers[0][12:]
dest_data = list(map(lambda i: dict(zip(headers, i)), dest_data))

def integrate(in_file, in_col, dest_col, in_write):
    with open(in_file) as f:
        headers.extend(in_write)
        reader = csv.DictReader(f)
        print(dir(reader))
        import pdb;pdb.set_trace()
        with open(dest_file, "w") as out:
            writer = csv.DictWriter(out, fieldnames=headers)
            writer.writeheader()
            for in_line in reader:
                data = [i for i in dest_data if i[dest_col] == in_line[in_col]]
                if data:
                    data = data[0]
                    for col in in_write:
                        data[col] = in_line[col]
                    writer.writerow(data)
                else:
                    print(f"No data found for {in_line[in_col]}")

# integrate("Farms.csv", "School Name", "School", ["Rate with Multiplier If Applicable"])
# integrate("stanford.csv", "school_name", "School", ["students_chronically_absent", "students_susp_in_sch", "students_susp_out_sch_single", "students_susp_out_sch_multiple", "expulsions_no_ed_serv", "expulsions_with_ed_serv", "expulsions_zero_tolerance", "students_corporal_punish", "students_arrested", "students_referred_law_enforce"])
integrate("report.csv", "School", "School", ["Amount"])
