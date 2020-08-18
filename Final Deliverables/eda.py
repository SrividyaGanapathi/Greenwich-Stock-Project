from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


test_df = df.iloc[:25]

job_counts = df[['post_date', 'njobs_on_date']].groupby(['post_date']).agg(['count'])
job_counts.head(10)


x = job_counts.index
y = job_counts["njobs_on_date"]


#line plot
fig = plt.figure(figsize=(18, 10))
plt.plot(x, y)
plt.xticks(rotation = 45, ha='right', size = 7)
plt.title("Number of New Job Postings Over Time", fontsize = 25)
plt.xlabel("Date of Job Postings", fontsize = 20)
plt.ylabel("Number of New Postings", fontsize = 20)
plt.show()


#boxplot
x = df['salary']
fig = plt.figure(figsize=(18, 10))
plt.boxplot(x, vert=False)
plt.title("Distribution of Salaries", fontsize=25)
plt.show()


#boxplot
x = df['salary']
fig = plt.figure(figsize=(18, 10))
plt.boxplot(x, vert=False)
plt.title("Distribution of Salaries", fontsize=25)
plt.show()