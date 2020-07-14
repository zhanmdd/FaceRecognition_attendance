import pandas as pd
import os

#creating directories which will store photos of known and unknown students

#known
try:
    os.mkdir('/Users/AZM/Desktop/Projectss/Face Recognition Attendance/known')
    print('Directory "known" Created')
except FileExistsError:
    print('Directory "known" already exists')

try:
    os.mkdir('/Users/AZM/Desktop/Projectss/Face Recognition Attendance/unknown')
    print('Directory "unknown" Created')
except FileExistsError:
    print('Directory "unknown" already exists')

#Creating a dataset which will store students info
lst = []
df = pd.DataFrame(lst, columns=['id', 'Name', 'Last Name', 'Time Checked'])
df.to_csv(r'/Users/AZM/Desktop/Projectss/Face Recognition Attendance/students_dataset.csv')