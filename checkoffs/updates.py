import csv
import os
# cwd to the directory of this file
os.chdir(os.path.dirname(os.path.realpath(__file__)))
def check_lab9(autograder_output, sunet):
    check = """-------------------------------------------------
checking <1-watchpt-test>: 
  about to emit new <1-watchpt-test.test>:
     my-install  ./1-watchpt-test.bin  > 1-watchpt-test.test
  about to compare contents:
     diff 1-watchpt-test.out 1-watchpt-test.test
  SUCCESS!   Test output and reference match.
-------------------------------------------------
checking <2-brkpt-test>: 
  about to emit new <2-brkpt-test.test>:
     my-install  ./2-brkpt-test.bin  > 2-brkpt-test.test
  about to compare contents:
     diff 2-brkpt-test.out 2-brkpt-test.test
  SUCCESS!   Test output and reference match.
-------------------------------------------------
checking <3-mini-watch-byte-access>: 
  about to emit new <3-mini-watch-byte-access.test>:
     my-install  ./3-mini-watch-byte-access.bin  > 3-mini-watch-byte-access.test
  about to compare contents:
     diff 3-mini-watch-byte-access.out 3-mini-watch-byte-access.test
  SUCCESS!   Test output and reference match.
-------------------------------------------------
checking <3-mini-watch-test>: 
  about to emit new <3-mini-watch-test.test>:
     my-install  ./3-mini-watch-test.bin  > 3-mini-watch-test.test
  about to compare contents:
     diff 3-mini-watch-test.out 3-mini-watch-test.test
  SUCCESS!   Test output and reference match.
-------------------------------------------------
checking <4-mini-step-diff>: 
  about to emit new <4-mini-step-diff.test>:
     my-install  ./4-mini-step-diff.bin  > 4-mini-step-diff.test
  about to compare contents:
     diff 4-mini-step-diff.out 4-mini-step-diff.test
  SUCCESS!   Test output and reference match.
-------------------------------------------------
checking <4-mini-step-trace-only>: 
  about to emit new <4-mini-step-trace-only.test>:
     my-install  ./4-mini-step-trace-only.bin  > 4-mini-step-trace-only.test
  about to compare contents:
     diff 4-mini-step-trace-only.out 4-mini-step-trace-only.test
  SUCCESS!   Test output and reference match.

Return code: 0"""
    return check in autograder_output
def check_lab8(autograder_output, sunet):
   check1 = """-------------------------------------------------
checking <0-test-checks>: 
  about to emit new <0-test-checks.test>:
     my-install  ./0-test-checks.bin  > 0-test-checks.test
  about to compare contents:
     diff 0-test-checks.out 0-test-checks.test
  SUCCESS!   Test output and reference match.
-------------------------------------------------
checking <1-test-run>: 
  about to emit new <1-test-run.test>:
     my-install  ./1-test-run.bin  > 1-test-run.test
  about to compare contents:
     diff 1-test-run.out 1-test-run.test
  SUCCESS!   Test output and reference match.""" in autograder_output
   check2 = """------------------------------------------
-n checking 6-gpio-event-clear:

./6-gpio-event-clear.fake 2>&1 | grep  "TRACE:" > ./6-gpio-event-clear.test
diff ./6-gpio-event-clear.out ./6-gpio-event-clear.test
Success!
------------------------------------------
-n checking 6-gpio-event-detected-n:

./6-gpio-event-detected-n.fake 2>&1 | grep  "TRACE:" > ./6-gpio-event-detected-n.test
diff ./6-gpio-event-detected-n.out ./6-gpio-event-detected-n.test
Success!
------------------------------------------
-n checking 6-gpio-event-detected:

./6-gpio-event-detected.fake 2>&1 | grep  "TRACE:" > ./6-gpio-event-detected.test
diff ./6-gpio-event-detected.out ./6-gpio-event-detected.test
Success!
------------------------------------------
-n checking 6-gpio-has-interrupt:

./6-gpio-has-interrupt.fake 2>&1 | grep  "TRACE:" > ./6-gpio-has-interrupt.test
diff ./6-gpio-has-interrupt.out ./6-gpio-has-interrupt.test
Success!
------------------------------------------
-n checking 6-gpio-set-falling:

./6-gpio-set-falling.fake 2>&1 | grep  "TRACE:" > ./6-gpio-set-falling.test
diff ./6-gpio-set-falling.out ./6-gpio-set-falling.test
Success!
------------------------------------------
-n checking 6-gpio-set-rising:

./6-gpio-set-rising.fake 2>&1 | grep  "TRACE:" > ./6-gpio-set-rising.test
diff ./6-gpio-set-rising.out ./6-gpio-set-rising.test
Success!
------------------------------------------
-n checking 7-gpio-event-clear-n:

./7-gpio-event-clear-n.fake 2>&1 | grep  "TRACE:" > ./7-gpio-event-clear-n.test
diff ./7-gpio-event-clear-n.out ./7-gpio-event-clear-n.test
Success!
------------------------------------------
-n checking 7-gpio-event-detected-n:

./7-gpio-event-detected-n.fake 2>&1 | grep  "TRACE:" > ./7-gpio-event-detected-n.test
diff ./7-gpio-event-detected-n.out ./7-gpio-event-detected-n.test
Success!
------------------------------------------
-n checking 7-gpio-set-falling-n:

./7-gpio-set-falling-n.fake 2>&1 | grep  "TRACE:" > ./7-gpio-set-falling-n.test
diff ./7-gpio-set-falling-n.out ./7-gpio-set-falling-n.test
Success!
------------------------------------------
-n checking 7-gpio-set-rising-n:

./7-gpio-set-rising-n.fake 2>&1 | grep  "TRACE:" > ./7-gpio-set-rising-n.test
diff ./7-gpio-set-rising-n.out ./7-gpio-set-rising-n.test
Success!""" in autograder_output
   check3 = """
   -------------------------------------------------
checking <0-check-connect>: 
  about to emit new <0-check-connect.test>:
     pi-install  ./0-check-connect.bin  > 0-check-connect.test
  about to compare contents:
     diff 0-check-connect.out 0-check-connect.test
  SUCCESS!   Test output and reference match.
-------------------------------------------------
checking <1-falling-edge>: 
  about to emit new <1-falling-edge.test>:
     pi-install  ./1-falling-edge.bin  > 1-falling-edge.test
  about to compare contents:
     diff 1-falling-edge.out 1-falling-edge.test
  SUCCESS!   Test output and reference match.
-------------------------------------------------
checking <1-rising-edge>: 
  about to emit new <1-rising-edge.test>:
     pi-install  ./1-rising-edge.bin  > 1-rising-edge.test
  about to compare contents:
     diff 1-rising-edge.out 1-rising-edge.test
  SUCCESS!   Test output and reference match.
-------------------------------------------------
checking <1-timer>: 
  about to emit new <1-timer.test>:
     pi-install  ./1-timer.bin  > 1-timer.test
  about to compare contents:
     diff 1-timer.out 1-timer.test
  SUCCESS!   Test output and reference match.
-------------------------------------------------
checking <2-rise-fall-edge>: 
  about to emit new <2-rise-fall-edge.test>:
     pi-install  ./2-rise-fall-edge.bin  > 2-rise-fall-edge.test
  about to compare contents:
     diff 2-rise-fall-edge.out 2-rise-fall-edge.test
  SUCCESS!   Test output and reference match.
-------------------------------------------------
checking <2-timer-rise-fall-edge>: 
  about to emit new <2-timer-rise-fall-edge.test>:
     pi-install  ./2-timer-rise-fall-edge.bin  > 2-timer-rise-fall-edge.test
  about to compare contents:
     diff 2-timer-rise-fall-edge.out 2-timer-rise-fall-edge.test
  SUCCESS!   Test output and reference match.
-------------------------------------------------
checking <3-N-rise-fall-timer>: 
  about to emit new <3-N-rise-fall-timer.test>:
     pi-install  ./3-N-rise-fall-timer.bin  > 3-N-rise-fall-timer.test
  about to compare contents:
     diff 3-N-rise-fall-timer.out 3-N-rise-fall-timer.test
  SUCCESS!   Test output and reference match.
-------------------------------------------------
checking <3-N-rise-fall>: 
  about to emit new <3-N-rise-fall.test>:
     pi-install  ./3-N-rise-fall.bin  > 3-N-rise-fall.test
  about to compare contents:
     diff 3-N-rise-fall.out 3-N-rise-fall.test
  SUCCESS!   Test output and reference match.
-------------------------------------------------
checking <3-N-rising-edge>: 
  about to emit new <3-N-rising-edge.test>:
     pi-install  ./3-N-rising-edge.bin  > 3-N-rising-edge.test
  about to compare contents:
     diff 3-N-rising-edge.out 3-N-rising-edge.test
  SUCCESS!   Test output and reference match.
"""
   check4 = "cyc=60" in autograder_output
   result = check1 and check2 and check3 and check4
   if result:
      # Open the makefile in ../repos/sunet/labs/8-device-int/4-logic-analyzer/
      makefile4_text = open(f"../repos/{sunet}/labs/8-device-int/4-logic-analyzer/Makefile").read()
      # If there is an individual line that contains 'staff-sw-uart' but has no '#' in it, return False
      for lines in makefile4_text.split('\n'):
         if 'staff-sw-uart' in lines and '#' not in lines:
            return False
      return True

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
    "lab5": check_lab5,
    "lab8": check_lab8,
    "lab9": check_lab9
}

csv_headers = {
    "lab1": "Lab 1 Trust",
    "lab3": "Lab 3 Cross-checking",
    "lab4": "Lab 4 Interrupts",
    "lab5": "Lab 5 Threads",
    "lab8": "Lab 8 dev interrupt",
    "lab9": "Lab 9 debug hw"
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