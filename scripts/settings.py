# Copyright (C) 2026 NYC School Zones · SPDX-License-Identifier: AGPL-3.0-or-later
"""Settings shared by the map (src/template.html, filled in by build.py), the school, district and neighborhood
pages (pages.py, neighborhoods.py) and fetch_data.py. Change a value here and rebuild; don't copy it elsewhere."""

# ---------- which year's data the site shows ----------

# School Quality Snapshot: ratings, programs, high school outcomes (and charter schools' test scores). "2025" is the 2024-25 school year
# (its address on tools.nycenet.edu/snapshot/2025/...).
SNAPSHOT_YEAR = "2025"
SNAPSHOT_LABEL = f"{int(SNAPSHOT_YEAR) - 1}–{SNAPSHOT_YEAR[2:]}"   # "2024–25"
# State ELA and math test scores (data/state_tests.json): the DOE's school results on InfoHub, a year ahead of the
# Snapshot. TESTS_YEAR is the spring the tests were taken. Charter schools aren't in that file, so theirs (and any
# school missing from it) still come from the Snapshot and say so.
TESTS_YEAR = "2026"
TESTS_LABEL = f"spring {TESTS_YEAR}"
# NYC-wide share meeting standards in grades 3-5 that spring (%), from the DOE's citywide results, quoted on the map
CITY_ELA_ES = 47
CITY_MATH_ES = 60
# A note on that year's scores, next to them on the map and the school pages; "" for none. Spring 2026: grades 3-5
# ELA jumped in 2025 (the state lowered the grade 3, 4 and 6 cut scores) and fell back in 2026 to about its 2023-24
# level (citywide grade 3: 2024 ~46%, 2025 58%, 2026 44%). TESTS_NOTE_SHORT goes on each elementary school's card.
TESTS_NOTE = ("ELA scores jumped across New York State in 2025 and fell back in 2026, mostly in grades 3–5. "
              "Compare schools with each other rather than with last year.")
TESTS_NOTE_SHORT = "ELA jumped statewide in 2025, then fell back"
# Pre-K and 3-K seats and applicants: the DOE's Local Law 72 admissions report (data/prek.json)
PREK_LABEL = "fall 2025"
# MySchools directories (data/ms_directory.json, hs_directory.json, k_priority.json): the admissions round their
# "last year" seats, applicants and priority groups describe. The 2026-27 directories report fall 2026 admissions;
# fetch_data.py warns when a download's school year doesn't match.
MYSCHOOLS_LABEL = "fall 2026"
# Building use: the SCA's Enrollment, Capacity & Utilization Report ("Blue Book", data/utilization.json)
BLUE_BOOK_LABEL = "2025–26"
# Race and ethnicity, family income and more: the DOE's Demographic Snapshot (data/demographics.json), the school year it counts
DEMOGRAPHICS_LABEL = "2025–26"

# NYC-wide high school averages from that Snapshot, quoted next to each school's numbers
CITY_GRAD = 81        # 4-year graduation rate, %
CITY_READINESS = 54   # college readiness score, of 100
# NYC-wide middle school average from that Snapshot: share of 8th graders who earned high school credit (passed an
# accelerated, Regents-level course), %
CITY_HS_CREDIT = 44

# ---------- color ramps ----------

# [value, color name] stops, low (red) to high (green). The map's Color by modes, legends and card bars use them,
# and so do the tables and bars on the generated pages. Each theme has its own colors for the names:
# light is bright and light, so dark map labels read well on top of the zone fills, and steps down in lightness
# red < teal < orange < yellow so neighboring levels stay apart for red-green color blindness (checked by simulation).
RAMP_COLORS = {"light": {"red": [228, 68, 73], "orange": [249, 140, 16], "yellow": [255, 226, 110], "green": [53, 182, 156]},
               "dark": {"red": [184, 32, 42], "orange": [232, 116, 42], "yellow": [247, 207, 69], "green": [31, 138, 132]}}
# DOE ratings: 1 -> 5, 2 -> 50, 3 -> 75, 4 -> 95 on this scale
RATE_STOPS = [[5, "red"], [50, "orange"], [75, "yellow"], [95, "green"]]
# % meeting state standards
TEST_STOPS = [[10, "red"], [50, "yellow"], [90, "green"]]
# high school outcomes
OUT_STOPS = {"grad": [[65, "red"], [80, "yellow"], [95, "green"]],     # 4-year graduation rate (%)
             "coll": [[40, "red"], [60, "yellow"], [80, "green"]],     # college or career program (%)
             "ccr": [[35, "red"], [55, "yellow"], [80, "green"]],      # college readiness score
             "sat": [[800, "red"], [950, "yellow"], [1200, "green"]]}  # average SAT

# Race and ethnicity bars on the cards and school pages: [label, color], in the order of a demographics.json row.
# Categorical (no group is "better"), so none of the ramp colors above; checked for color blindness side by side.
DEMO_GROUPS = [["Asian or Pacific Islander", "#2a78d6"], ["Black", "#eb6834"], ["Hispanic", "#1baf7a"], ["White", "#eda100"],
               ["Multiracial, Native American or not reported", "#9aa5a0"]]

# High school admissions methods, one line each: the map card shows it when you tap a program's method, the school
# pages under each program. Keys are the method codes in build.py MCODE.
HS_METHOD_HELP = {
    "E": "Takes students across a range of 7th-grade grades, not only top students.",
    "S": "Ranks applicants by their 7th-grade course grades.",
    "SA": "Ranks applicants by 7th-grade grades plus the school’s own assessment, like an essay, interview or test.",
    "SL": "Ranks applicants by 7th-grade grades and a language assessment, for bilingual or language-focused programs.",
    "O": "Random among applicants, after any priorities.",
    "A": "Admits by audition or portfolio, for arts programs.",
    "L": "For students who speak, or are learning, the program’s language, such as English learners or dual-language programs.",
    "T": "Admits only by SHSAT score. Students sign up for the test separately in the fall.",
    "ZG": "Students who live in the zone and list the program are guaranteed a seat.",
    "ZP": "Students who live in the zone get top priority.",
    "TR": "A transfer school, for older students who are behind on credits or have left school; not part of 8th-grade admissions.",
    "D75": "Seats for students whose IEP recommends a District 75 program.",
    "ASD": "Seats for students whose IEP recommends an autism (ASD Nest or Horizon) or ACES program.",
}

# Middle school admissions methods, the same way (keys: the method codes in src/template.html MNAME).
MS_METHOD_HELP = {
    "Z": "Students who live in the zone get priority, after siblings and, at K–8 schools, the school’s own 5th graders.",
    "O": "Random among applicants, after any priorities.",
    "S": "Ranks applicants by their course grades.",
    "SA": "Ranks applicants by the school’s own assessment, and in some cases their course grades.",
    "A": "Ranks applicants by audition, for arts programs.",
    "T": "Admits by District 21’s Mark Twain talent test score.",
    "L": "Ranks applicants by English proficiency or home language, for English learners and dual-language programs.",
    "D75": "Seats for students whose IEP recommends a District 75 program.",
    "ASD": "Seats for students whose IEP recommends an autism (ASD Nest or Horizon) or ACES program.",
}

# ---------- AP classes ----------

# Every College Board AP course, by the College Board's subject areas, as high school cards and pages list them: the
# areas A-Z, AP Capstone (a research and seminar program, not a subject) last, each area's courses A-Z
# (build.py ap_courses). The names are the College Board's, without "AP "; a school's list from MySchools
# (hs_directory.json, "x" "ap") is matched to these, so schools can be compared course by course. The build warns
# about a course it can't match: add it here, or to AP_ALIASES when MySchools spells it another way.
AP_COURSES = (
    ("Arts", ("2-D Art and Design", "3-D Art and Design", "Art History", "Drawing", "Music Theory")),
    ("English", ("English Language and Composition", "English Literature and Composition")),
    ("History and social sciences", ("African American Studies", "Comparative Government and Politics", "European History",
                                     "Human Geography", "Macroeconomics", "Microeconomics", "Psychology",
                                     "United States Government and Politics", "United States History", "World History: Modern")),
    ("Math and computer science", ("Calculus AB", "Calculus BC", "Computer Science A", "Computer Science Principles",
                                   "Precalculus", "Statistics")),
    ("Sciences", ("Biology", "Chemistry", "Environmental Science", "Physics 1", "Physics 2",
                  "Physics C: Electricity and Magnetism", "Physics C: Mechanics")),
    ("World languages", ("Chinese Language and Culture", "French Language and Culture", "German Language and Culture",
                         "Italian Language and Culture", "Japanese Language and Culture", "Latin",
                         "Spanish Language and Culture", "Spanish Literature and Culture")),
    ("AP Capstone (research and seminar)", ("Research", "Seminar")),
)
# MySchools spellings that differ from the College Board's (older course names), without "AP "
AP_ALIASES = {"Pre-Calculus": "Precalculus", "Studio Art - 2D": "2-D Art and Design", "Studio Art - 3D": "3-D Art and Design",
              "Studio Art - Drawing": "Drawing"}

# Middle school accelerated and honors classes (ms_directory.json "acc", as fetch_data.py _ms_extras names them:
# "Algebra (accelerated)", "Math (honors)"), by subject for the map's Color by "Accelerated classes" and the card's
# list (build.py ms_accelerated). A class goes in the area that names what comes before its " (": "Algebra II" in
# Math. The build warns about one it can't place, which lands in "Other": add it here.
MS_ACC_AREAS = (
    ("Math", ("Algebra", "Algebra II", "Geometry", "Math")),
    ("Science", ("Biology", "Chemistry", "Earth & Space Science", "Earth Science", "Physics", "Science")),
    ("English", ("ELA",)),
    ("Social studies", ("Global History & Geography II", "Social Studies", "US History")),
    ("World languages", ("World Languages",)),
    ("Arts and technology", ("Arts", "Comp Sci/Math Tech")),
)

# Middle school electives and clubs (ms_directory.json "el" and "ac", as schools pick them on MySchools), by kind, for
# the card's and school page's "Classes, sports & activities" (build.py ms_extras), shown A-Z with "Other" last. Both lists share these groups;
# names match ignoring case. The build warns about a name it can't place, which lands in "Other": add it here.
MS_EXTRA_GROUPS = (
    ("Languages", ("American Sign Language", "Foreign Language", "French", "French Club", "Italian", "Latin Language Club",
                   "Mandarin", "Spanish", "Spanish Language & Culture")),
    ("STEM and technology", ("Aquaponics", "Biotechnology", "Civil Engineering", "Coding", "Coding/robotics", "Computer Science",
                             "Daily Student Computer Use", "Engineering", "Family Science Night", "Forensics", "Game Design",
                             "Hydroponics", "LEGO Robotics", "Math Team", "Robotics", "S.T.E.A.M.", "Science Club",
                             "Science Olympiad", "Sports Medicine", "STEM", "Technology", "Urban Advantage",
                             "Urban Advantage program", "Web Design")),
    ("Visual arts and design", ("Art", "Ceramics", "Fashion", "Film", "Fine Arts", "Graphic Design", "Photography",
                                "Photography/yearbook club", "Sewing", "Studio Art", "Urban Arts", "Videography", "Visual Arts")),
    ("Music", ("Band", "Choir", "Chorus", "Concert Band", "Drumline", "Glee Club", "Guitar", "Jazz Band", "Marching Band",
               "Modern Band", "Music", "Music instruction - NYSSMA", "Orchestra", "Piano", "Rock Band", "Strings", "Vocal Music")),
    ("Dance and theater", ("African Dance", "Ballroom Dancing", "Dance", "Drama", "Hip-Hop", "Latin Dance", "Musical Theater",
                           "Performing Arts", "Step Team", "Talent Show", "Talent Showcase", "Theater", "Theatre")),
    ("Writing, debate and law", ("Book Club", "Comic Book Club", "Creative Writing", "Debate", "Journalism", "Law",
                                 "Library Squad", "Mock Trial", "Newspaper", "School Newspaper", "Spelling Bee", "Yearbook")),
    ("Business", ("Business and Finance", "Stock Market", "Virtual Enterprise")),
    ("Sports, fitness and wellness", ("Baseball", "Basketball", "Boys Basketball Team", "Brain Power Wellness", "Cheerleading",
                                      "Fitness", "Girls Volleyball Team", "In-line Skating", "Martial Arts", "Mindfulness",
                                      "Soccer", "Swimming", "Track", "Volleyball", "Wrestling", "Yoga")),
    ("Games and hobbies", ("Chess", "Cooking", "Gardening", "Video Game Club")),
    ("Leadership and service", ("Arista/Archon", "Community Service", "Environmental Club", "Green Team", "Leadership",
                                "Multicultural club", "National Junior Honor Society", "Peer Mediation", "Restorative Circles",
                                "Service Learning", "Student Council", "Student Government", "Student government and tutoring",
                                "Student Leadership Ambassadors")),
    ("Extra help and test prep", ("80 Challenge", "Accelerated Program", "College Immersion Programs (Seventh and Eighth Grades) from QC.",
                                  "Homework Help", "Saturday Academy", "Specialized High School Test Preparation", "Tutoring")),
    ("Other", ("Daily lunch clubs of all varieties.", "Many Student Designed Courses")),
)
# Classes every middle school teaches (or that the Accelerated classes section already covers), which some schools list
# as electives or clubs anyway: left out of both lists
MS_REQUIRED = ("Advisory", "Algebra I", "CC Algebra Regents", "Earth Science - NYS Regents", "English - NYS Regents",
               "Global History - NYS Regents", "Health", "Library", "Living Environment", "Math", "Physical Education",
               "Regents Living Environment", "Science", "US History", "US History - NYS Regents")

# Application dates for the next admissions round, one per level: the line under the panel title ("Apply by Fri, Dec 4
# · 24 days left") and "Key dates" in each "How … admissions work" window. Dates are YYYY-MM-DD. "offers_text", when
# set, is shown instead of the offer date (the DOE hadn't posted the high school one); "offers" still decides when the
# line goes away. "more": other deadlines listed in the window. Update these each fall from the pages in "source";
# once a round's offers are out, the line hides itself and the build reminds you.
APPLY_DATES = {
    "es": {"opens": "2026-12-09", "closes": "2027-01-22", "offers": "2027-03-30",
           "source": "https://www.schools.nyc.gov/enrollment/enroll-grade-by-grade/kindergarten"},
    "ms": {"opens": "2026-10-14", "closes": "2026-12-11", "offers": "2027-04-07",
           "source": "https://www.schools.nyc.gov/enrollment/enroll-grade-by-grade/middle-school"},
    "hs": {"opens": "2026-10-06", "closes": "2026-12-04", "offers": "2027-03-15", "offers_text": "early March",
           "more": [["SHSAT sign-up closed", "2026-10-30"], ["Audition and assessment materials due", "2026-12-04"],
                    ["LaGuardia application closes", "2026-12-04"]],
           "source": "https://www.schools.nyc.gov/enrollment/enroll-grade-by-grade/high-school"},
}
