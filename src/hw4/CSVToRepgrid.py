import csv
import os

# This file converts the regrid results stored in a CSV file to the format he has in repgrid1.csv

data_dir = "../../etc/data/"


def convert(file):
    rows = []
    with open(data_dir + file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)

    rows[0].pop(0)
    cols = rows[0]
    rows.pop(0)
    for n, col in enumerate(cols):
        cols[n] = col.split("$")

    rowTitles = []
    for row in rows:
        rowTitles.append(row[0])
        row.pop(0)
    
    with open(data_dir + "Repgrid" + file, "w") as f:
        f.write("local _ = " "\nreturn {\n  domain=\"Bars in Raleigh\"\n  cols={")
        for n, col in enumerate(cols):
            line = "    {'%s', " % col[0]
            for row in rows:
                val = row[n]
                line += val + ", "
            line += "'%s'},\n" % col[1]
            f.write(line)

        f.write("  },\n  rows={")
        curr = len(rowTitles) - 1
        rowTitles.reverse()
        for rt in rowTitles:
            line = "    { "
            for i in range(curr):
                line += "_, "
            curr -= 1
            line += "'%s'},\n" % rt
            f.write(line)
        f.write("  }\n}")



for file in os.listdir(data_dir):
    # print(file)
    # print(type(file))
    if file.startswith("Greg"):
        convert(file)

print("done")