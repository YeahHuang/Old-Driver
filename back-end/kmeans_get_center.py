import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np 
import pandas as pd
import time
import json
import pandas as pd
from io import BytesIO
import seaborn as sns

ROWS_SAMPLE = 80000

df = pd.read_csv("train.csv")

# Delete locations far away from the others
longitude_limit = [-74.027, -73.85]
latitude_limit = [40.67, 40.85]
df = df[(df.pickup_longitude.between(longitude_limit[0], longitude_limit[1], inclusive=False))]
df = df[(df.dropoff_longitude.between(longitude_limit[0], longitude_limit[1], inclusive=False))]
df = df[(df.pickup_latitude.between(latitude_limit[0], latitude_limit[1], inclusive=False))]
df = df[(df.dropoff_latitude.between(latitude_limit[0], latitude_limit[1], inclusive=False))]

df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])
df["dropoff_datetime"] = pd.to_datetime(df["dropoff_datetime"])

df_trimmed = df.sample(ROWS_SAMPLE)
#df_trimmed.head()

longitude = list(df_trimmed.pickup_longitude)  #+ list(df_trimmed.dropoff_longitude)
latitude = list(df_trimmed.pickup_latitude)  #+ list(df_trimmed.dropoff_latitude)

total_data = pd.DataFrame({'latitude': latitude, 'longitude': longitude})
start = time.clock()
n_clusters = 1000
debug = False
for i in range(9,15):
    start = time.clock()
    sub_df = df[(df.pickup_datetime.dt.hour.between(i,i+1,inclusive = True))]
    longitude = list(sub_df.pickup_longitude)
    latitude = list(sub_df.pickup_latitude)
    duration = list(sub_df.trip_duration)
    data = pd.DataFrame({'latitude': latitude, 'longitude': longitude})
    data.describe()
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(data)
    data['kmean_label'] = kmeans.labels_
    data["duration"] = duration
    center_duration = [0 for i in range(n_clusters)]
    number = [0 for i in range(n_clusters)]
    for i in range(len(data)):
        center_duration[int(data.values[i][2])] += data.values[i][3]
        number[int(data.values[i][2])] += 1

    for label in range(n_clusters):
        #sub_duration = pd.DataFrame(data.duration[data.kmean_label == label])
        #temp_sum = sub_duration.apply(lambda x: x.sum())
        #print(label," ",temp_sum)
        center_duration[label] = center_duration[label] / number[label]
        if debug:
            print(label," ",center_duration[label])

    n = len(kmeans.cluster_centers_)
    elapsed = (time.clock() - start)
    print(i, " ", elapsed)
    if debug:
        for j in range(n):
            print(kmeans.cluster_centers_[j])
   
print("Time used ", elapsed)
