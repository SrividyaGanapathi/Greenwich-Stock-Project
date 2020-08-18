import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#master = pd.read_csv("Actual Data/greenwich_master_backtestsamplepublic.csv")
roles = pd.read_csv("Actual Data/greenwich_role_backtestsamplepublic.csv")
#tags = pd.read_csv("Actual Data/greenwich_tags_backtestsamplepublic.csv")
time_log = pd.read_csv("Actual Data/greenwich_timelog_backtestsamplepublic.csv")
#titles = pd.read_csv("Actual Data/greenwich_titles_backtestsamplepublic.csv")

#decoding errors in master, tags, titles so will use sample tags
tags_sample = pd.read_csv("Sample Data/greenwich_tags_backtestsamplepublic.csv")
#master_sample = pd.read_csv("Sample Data/greenwich_master_backtestsamplepublic.csv")
#titles_sample = pd.read_csv("Sample Data/greenwich_titles_backtestsamplepublic.csv")




#ROLES EDA:
#there are is corruption in the 'role' column. There are datetime values in role column.
def count_unique(ser):
    return len(ser)
roles_count = roles.groupby('role').apply(count_unique)
#top 10 roles
roles_count.sort_values(ascending = False)[0:10,]


#plot top 25 roles
plt.bar(roles_count.sort_values(ascending = False)[0:25,].index, roles_count.sort_values(ascending = False)[0:25,])
plt.xticks(rotation = 'vertical')
plt.title("Distribution of Roles")
plt.ylabel("Count")
plt.show()


#TIME LOG EDA
status_count = time_log.groupby('status').apply(count_unique)
plt.bar(status_count.index, status_count)
plt.ylabel("Count")
plt.title("Distribution of Job Statuses")
plt.show()
#MOST JOBS ARE CLOSED, with a FRACTION OPEN



#TAGS EDA
#some weird data about # years being stored in tag column
#what are the top 10 tags
tags_sample.groupby('tag').apply(count_unique).sort_values(ascending = False)[1:10,]


