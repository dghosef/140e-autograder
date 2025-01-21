import csv
import os
# cwd to the directory of this file
os.chdir(os.path.dirname(os.path.realpath(__file__)))
def check_lab1(autograder_output):
    if 'diff' not in autograder_output:
        return False
    if 'login failed' in autograder_output:
        return False
    if 'successful login' in autograder_output:
        return True

def check_lab3(autograder_output):
    cksums = [525118589, 2831894783, 3159539606, 3179942673, 610433833, 3754849163, 2100720877, 4083157797, 3731391281, 486978757, 3957154857]
    for cksum in cksums:
        if str(cksum) not in autograder_output:
            return False
    return True

checker_fns = {
    "lab1": check_lab1,
    "lab3": check_lab3
}

csv_headers = {
    "lab1": "Lab 1 Trust",
    "lab3": "Lab 3 Cross-checking"
}

for lab in checker_fns:
    assert lab in csv_headers, f"Missing header for {lab}"

def check_output(autograder_output, lab):
    return checker_fns[lab](autograder_output)

def check_lab_student(sunet, lab):
    # run `check_output` on every file in ./`lab`/`sunet`. Return true if any file passes
    files = os.listdir(f"./{lab}/{sunet}")
    for file in files:
        text = open(f"./{lab}/{sunet}/{file}").read()
        if check_output(text, lab):
            return True
    return False

def check_lab(lab):
    sunets = os.listdir(f"./{lab}")
    passes = set()
    for sunet in sunets:
        if check_lab_student(sunet, lab):
            passes.add(sunet)
    return passes

def check_labs():
    result = {}
    for lab in checker_fns:
        passes = check_lab(lab)
        result[csv_headers[lab]] = passes
    return result

def print_csv_updates():
    passes = check_labs()
    # Read the csv. If the student passed but 60Gthe csv says they failed, print to stdout
    with open("checkoffs.csv", "r") as f:
        reader = csv.DictReader(f)
        next(reader) # Skip the completed count
        for row in reader:
            for lab in csv_headers:
                if row[csv_headers[lab]] == "TBD" and row["SUNet ID"] in passes[csv_headers[lab]]:
                    print(f"{row['SUNet ID']} passed {csv_headers[lab]}")

print_csv_updates()