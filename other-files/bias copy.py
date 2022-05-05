import string

# male_names = open("data/male.txt")
# female_names = open("data/female.txt")

# males = male_names.read()
# females = female_names.read()

male_set = []
female_set = []


with open("other-files/male.txt","r") as males:
    male_names = males.readlines() # returns only the first line as string and iterates over this string

for name in range(len(male_names)):
    male_names[name] = male_names[name][:-1]

with open("other-files/female.txt","r") as females:
    female_names = females.readlines() # returns only the first line as string and iterates over this string

for name in range(len(female_names)):
    female_names[name] = female_names[name][:-1]


def get_gender(user):
    pass

