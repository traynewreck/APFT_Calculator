import json
import bisect

# Defining user input variables with some input validation
age = int(input('Enter Age: '))
if age < 17:
    print('[*] ERROR: Must be older than 17.')
sex = input('Enter [M] for Male or [F] for Female: ').lower()
if sex not in ('m', 'f'):
    print('[*] ERROR: Please enter [m] for Male and [f] for Female')
pushups = str(input('Enter Push-up Repetitions: '))
situps = input('Enter Sit-up Repetitions: ')
run = input('Enter Two-Mile Run Time [MM:SS]: ').split(':')
run = ''.join(run)
run = int(run)
if run == 0:
    print('[*] ERROR: Run timc cannot be 0!')

# Importing JSON values for APFT scores
with open('apft_standards.json') as f:
    apft_standards_dict = json.load(f)

# Creating dictionaries out of the JSON
male_pu_dict = apft_standards_dict['male']['push-ups']
male_su_dict = apft_standards_dict['male']['sit-ups']
male_run_dict = apft_standards_dict['male']['run']
female_pu_dict = apft_standards_dict['female']['push-ups']
female_su_dict = apft_standards_dict['female']['sit-ups']
female_run_dict = apft_standards_dict['female']['run']
# Creating a run time list for the round-up run function
run_time_int_list = []
for runtime in male_run_dict:
    run_time_int_list.append(int(runtime))

# Determines what age range the candidate should be graded by
def ageRange(age):
    range17_21 = "17-21"
    range22_26 = "22-26"
    range27_31 = "27-31"
    range32_36 = "32-36"
    range37_41 = "37-41"
    range42_46 = "42-46"
    range47_51 = "47-51"
    range52_56 = "52-56"
    range57_61 = "57-61"
    range62plus = "62+"
    if age in range(17,21):
       age = range17_21
    elif age in range(22,26):
        age = range22_26
    elif age in range(27,31):
        age = range27_31
    elif age in range(32,36):
        age = range32_36
    elif age in range(37,41):
        age = range37_41
    elif age in range(41,46):
        age = range42_46
    elif age in range(47,51):
        age = range47_51
    elif age in range(52,56):
        age = range52_56
    elif age in range(57,61):
        age = range57_61
    elif age >= 62:
        age = range62plus
    return age
# Chooses the appropriate run time for someone who comes in between standard run intervals
def roundUpRun(run):
    if run in run_time_int_list:
        run = run
    else:
        round_up = bisect.bisect_right(run_time_int_list,run)
        run = run_time_int_list[round_up]
    return run
# Determines pushup score
def puScore(sex, age, pushups):
    age_range = ageRange(age)
    if sex == 'm':
        if int(pushups) < 5:
            score = 0
        elif int(pushups) > 77:
            score = 100
        else:
            score = male_pu_dict[pushups][0].get(age_range)
    elif sex == 'f':
        if int(pushups) < 5:
            score = 0
        elif int(pushups) > 50:
            score = 100
        else:
            score = female_pu_dict[pushups][0].get(age_range)
    return score
# Determines situp score
def suScore(sex, age, situps):
    age_range = ageRange(age)
    if sex == 'm':
        if int(situps) < 21:
            score = 0
        elif int(situps) > 82:
            score = 100
        else:
            score = male_su_dict[situps][0].get(age_range)
    elif sex == 'f':
        if int(situps) < 21:
            score = 0
        elif int(situps) > 82:
            score = 100
        else:
            score = female_su_dict[situps][0].get(age_range)
    return score
# Determines run score
def runScore(sex, age, run):
    age_range = ageRange(age)
    run = roundUpRun(run)
    print(f'runtime is: {run}')
    if sex == 'm':
        if int(run) > 2630:
            score = 0
        elif int(run) < 1254:
            score = 100
        else:
            score = male_run_dict[str(run)][0].get(age_range)
    elif sex == 'f':
        if int(run) > 2630:
            score = 0
        elif int(run) < 1254:
            score = 100
        else:
            score = female_run_dict[str(run)][0].get(age_range)
    return score

# Defining final scores for ease of use
pu_score = puScore(sex,age,pushups)
su_score = suScore(sex,age,situps)
run_score = runScore(sex,age,run)
total_score = pu_score + su_score + run_score

# Printing results
print(f'Your Pushup score is: {pu_score}')
print(f'Your Sit-up score is: {su_score}')
print(f'Your Run score is: {run_score}')
print(f'Your TOTAL score is: {total_score}')
