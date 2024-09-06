import pandas as pd

# URL del dataset en el repositorio UCI
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data'

# Definir los nombres de las columnas según la documentación del dataset
column_names = [
    'age', 'workclass', 'fnlwgt', 'education', 'education-num',
    'marital-status', 'occupation', 'relationship', 'race', 'sex',
    'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'salary'
]

# Cargar el dataset usando pandas
df = pd.read_csv(url, names=column_names, index_col=False, skipinitialspace=True)

race_counts = df['race'].value_counts()
#What is the average age of men?
men = df[df['sex'] == 'Male']
age_avg = men['age'].mean()
#What percentage of people with advanced education (Bachelors, Masters, or Doctorate) make more than 50K?
advanced_education = ['Bachelors', 'Masters', 'Doctorate']
higher_education = df[df['education'].isin(advanced_education)] # or df['education'].str.contains('Bachelors|Masters|Doctorate') gets a df with the same rows
higher_education_rich = higher_education[higher_education['salary'] == '>50K']  # from the previous df, get the rows where salary is >50K
higher_education_rich_percentage = (len(higher_education_rich) / len(higher_education)) * 100 # divide the number of rows in the previous df by the number of rows in the previous df
#What percentage of people without advanced education make more than 50K?
people_without_advanced_education = df[~df['education'].isin(advanced_education)] #This does the opposite of the previous line
people_without_advanced_education_rich = people_without_advanced_education[people_without_advanced_education['salary'] == '>50K']
people_without_advanced_education_rich_percentage = (len(people_without_advanced_education_rich) / len(people_without_advanced_education)) * 100
#What is the minimum number of hours a person works per week?
min_work_hours = df['hours-per-week'].min()
#What percentage of the people who work the minimum number of hours per week have a salary of more than 50K?
num_min_workers = df[df['hours-per-week'] == min_work_hours] # get the rows where the number of hours per week is the minimum
rich_percentage = (len(num_min_workers[num_min_workers['salary'] == '>50K']) / len(num_min_workers)) * 100 # divide the number of rows where the salary is >50K by the number of rows where the number of hours per week is the minimum
print(rich_percentage)
#What country has the highest percentage of people that earn >50K?
highest_earning_country = (df[df['salary'] == '>50K']['native-country'].value_counts() / df['native-country'].value_counts()).idxmax() # divide the number of rows where the salary is >50K by the number of rows in the df and get the index of the maximum value
#Identify the most popular occupation for those who earn >50K in India.
top_IN_occupation = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]['occupation'].value_counts().idxmax() # get the rows where the native country is India and the salary is >50K and get the index of the maximum value
print(top_IN_occupation)
print(f"{people_without_advanced_education_rich_percentage:.2f}%")

