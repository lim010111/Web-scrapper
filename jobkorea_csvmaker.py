from extractors.jobk import extract_jobkorea_jobs

what = input("what do you want to search for? :")

jobs = extract_jobkorea_jobs(what)

file = open(f"{what}.csv", "w")
file.write("Company, Title, Exp, Edu, Location, URL\n")

for job in jobs:
    file.write(f"{job['company']}, {job['title']}, {job['exp']}, {job['edu']}, {job['location']}, {job['link']}\n")

file.close()