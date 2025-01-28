import csv
import os
# cwd to the directory of this file
os.chdir(os.path.dirname(os.path.realpath(__file__)))
def check_lab1(autograder_output, sunet):
    if 'diff' not in autograder_output:
        return False
    if 'login failed' in autograder_output:
        return False
    if 'successful login' in autograder_output:
        return True

def check_lab3(autograder_output, sunet):
    cksums = [525118589, 2831894783, 3159539606, 3179942673, 610433833, 3754849163, 2100720877, 4083157797, 3731391281, 486978757, 3957154857]
    for cksum in cksums:
        if str(cksum) not in autograder_output:
            return False
    return True

def check_lab4(autograder_output, sunet):
    return True

def check_lab5(autograder_output, sunet):
    expected = """-------------------------------------------------
checking <2-test-one-fork>: 
  about to emit new <2-test-one-fork.test>:
     pi-install  ./2-test-one-fork.bin  > 2-test-one-fork.test
  about to compare contents:
     diff 2-test-one-fork.out 2-test-one-fork.test
  SUCCESS!   Test output and reference match.
-------------------------------------------------
checking <3-test-exit>: 
  about to emit new <3-test-exit.test>:
     pi-install  ./3-test-exit.bin  > 3-test-exit.test
  about to compare contents:
     diff 3-test-exit.out 3-test-exit.test
  SUCCESS!   Test output and reference match.
-------------------------------------------------
checking <3-test-restart>: 
  about to emit new <3-test-restart.test>:
     pi-install  ./3-test-restart.bin  > 3-test-restart.test
  about to compare contents:
     diff 3-test-restart.out 3-test-restart.test
  SUCCESS!   Test output and reference match.
-------------------------------------------------
checking <3-test-thread>: 
  about to emit new <3-test-thread.test>:
     pi-install  ./3-test-thread.bin  > 3-test-thread.test
  about to compare contents:
     diff 3-test-thread.out 3-test-thread.test
  SUCCESS!   Test output and reference match.
-------------------------------------------------
checking <4-test-yield-fail>: 
  about to emit new <4-test-yield-fail.test>:
     pi-install  ./4-test-yield-fail.bin  > 4-test-yield-fail.test
  about to compare contents:
     diff 4-test-yield-fail.out 4-test-yield-fail.test
  SUCCESS!   Test output and reference match.
-------------------------------------------------
checking <4-test-yield>: 
  about to emit new <4-test-yield.test>:
     pi-install  ./4-test-yield.bin  > 4-test-yield.test
  about to compare contents:
     diff 4-test-yield.out 4-test-yield.test
  SUCCESS!   Test output and reference match.
-------------------------------------------------
checking <5-test-implicit-exit-run-N>: 
  about to emit new <5-test-implicit-exit-run-N.test>:
     pi-install  ./5-test-implicit-exit-run-N.bin  > 5-test-implicit-exit-run-N.test
  about to compare contents:
     diff 5-test-implicit-exit-run-N.out 5-test-implicit-exit-run-N.test
  SUCCESS!   Test output and reference match.
-------------------------------------------------
checking <5-test-implicit-exit-run-one>: 
  about to emit new <5-test-implicit-exit-run-one.test>:
     pi-install  ./5-test-implicit-exit-run-one.bin  > 5-test-implicit-exit-run-one.test
  about to compare contents:
     diff 5-test-implicit-exit-run-one.out 5-test-implicit-exit-run-one.test
  SUCCESS!   Test output and reference match.
-------------------------------------------------
checking <5-test-implicit-exit>: 
  about to emit new <5-test-implicit-exit.test>:
     pi-install  ./5-test-implicit-exit.bin  > 5-test-implicit-exit.test
  about to compare contents:
     diff 5-test-implicit-exit.out 5-test-implicit-exit.test
  SUCCESS!   Test output and reference match.
-------------------------------------------------
checking <7-test-ping-pong>: 
  about to emit new <7-test-ping-pong.test>:
     pi-install  ./7-test-ping-pong.bin  > 7-test-ping-pong.test
  about to compare contents:
     diff 7-test-ping-pong.out 7-test-ping-pong.test
  SUCCESS!   Test output and reference match.
-------------------------------------------------
checking <7-test-realtime-yield>: 
  about to emit new <7-test-realtime-yield.test>:
     pi-install  ./7-test-realtime-yield.bin  > 7-test-realtime-yield.test
  about to compare contents:
     diff 7-test-realtime-yield.out 7-test-realtime-yield.test
  SUCCESS!   Test output and reference match.
-------------------------------------------------
checking <7-test-thread>: 
  about to emit new <7-test-thread.test>:
     pi-install  ./7-test-thread.bin  > 7-test-thread.test
  about to compare contents:
     diff 7-test-thread.out 7-test-thread.test
  SUCCESS!   Test output and reference match.
--------------------------------------------------------
Environment:
   STAFF_OBJS [should just have staff-kmalloc.o] =<staff-kmalloc.o>
   COMMON_SRC [should have both .o] =<rpi-thread-asm.S  rpi-thread.c>
-n    total tests=
      12
-n    checksum of cksum: 
cksum ./2-test-one-fork.out ./3-test-exit.out ./3-test-restart.out ./3-test-thread.out ./4-test-yield-fail.out ./4-test-yield.out ./5-test-implicit-exit-run-N.out ./5-test-implicit-exit-run-one.out ./5-test-implicit-exit.out ./7-test-ping-pong.out ./7-test-realtime-yield.out ./7-test-thread.out | sort -n | cksum
721271717 477
======================"""
    return expected in autograder_output
checker_fns = {
    "lab1": check_lab1,
    "lab3": check_lab3,
    "lab4": check_lab4,
    "lab5": check_lab5
}

csv_headers = {
    "lab1": "Lab 1 Trust",
    "lab3": "Lab 3 Cross-checking",
    "lab4": "Lab 4 Interrupts",
    "lab5": "Lab 5 Threads"
}

for lab in checker_fns:
    assert lab in csv_headers, f"Missing header for {lab}"

def check_output(autograder_output, lab, sunet):
    return checker_fns[lab](autograder_output, sunet)

def check_lab_student(sunet, lab):
    # run `check_output` on every file in ./`lab`/`sunet`. Return true if any file passes
    files = os.listdir(f"./{lab}/{sunet}")
    for file in files:
        text = open(f"./{lab}/{sunet}/{file}").read()
        if check_output(text, lab, sunet):
            return True
    return False

def check_lab(lab):
    sunets = os.listdir(f"./{lab}")
    passes = set()
    for sunet in sunets:
        if check_lab_student(sunet, lab):
            passes.add(sunet)
            continue
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
                if (row[csv_headers[lab]] == "TBD" or row[csv_headers[lab]] == "WIP Checkoff") and row["SUNet ID"] in passes[csv_headers[lab]]:
                    print(f"{row['SUNet ID']} passed {csv_headers[lab]}")

print_csv_updates()