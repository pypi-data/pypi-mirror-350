```python
from edgeml import edgeml
import time
import math
```

# Globals


```python
READ_KEY = "YOUR_READ_KEY"  # Replace with your actual read key
WRITE_KEY = "YOUR_WRITE_KEY"  # Replace with your actual write key
BACKEND_URL = "YOUR_BACKEND_URL"  # Replace with your actual backend URL
```

# Upload randomly generated data to the server using the edge-ml python library

### To upload data to edge-ml, we can use the DatasetCollector

For this, we need to provide the following information:
| **Parameter**         | **Description**                                                                 |
|-----------------------|---------------------------------------------------------------------------------|
| `url`                 | The URL to the edge-ml instance.                                                |
| `write_key`           | The API key for writing into the system.                                       |
| `use_own_timestamps`  | If `true`, users can pass timestamps to the collection function. Otherwise, timestamps are set by the `DatasetCollector`. |
| `timeSeries`          | An array containing the names of the time series to be used.                   |
| `metaData`            | A dictionary with metadata. Must contain only key-value pairs where both keys and values are strings. |


```python
datasetName = "Example Dataset"
useOwnTimeStamps = False
timeSeries = ["Acc", "Mag"]
metaData = {}

collector = edgeml.DatasetCollector(BACKEND_URL,
                                    WRITE_KEY,
                                    datasetName,
                                    useOwnTimeStamps,
                                    timeSeries,
                                    metaData)
```

### Now we can add data to this dataset

For this we can call the addDataPoint-function.
Don't forget to call onComplete after inserting all the data.


```python
timestamp = round(time.time() * 1000)
for i in range(100):
    timestamp += 40
    x = i / 10000        # Adjust the divisor to control the frequency of the wave
    y_acc = math.sin(x)  # Generate the y-coordinate for "Acc"
    y_mag = math.cos(x)  # Generate the y-coordinate for "Mag"
    await collector.addDataPoint(timestamp, "Acc", y_acc) 
    await collector.addDataPoint(timestamp, "Mag", y_mag) 

# signal data collection is complete. This uploads the remaining data to the server
collector.onComplete()
```




    True



# Retrieve data from edge-ml

It is also possible to obtain the datasets in a project. To do so use the DatasetReceiver


```python
project = edgeml.DatasetReceiver(BACKEND_URL, READ_KEY)

# See a single dataset
print(project.datasets[0])
# Or get some attribute from the dataset
print(project.datasets[0].metaData)

# Until now, we have only the metdata of the datasets.
# We can also download the actual time-series data.

# Only for one timeSeries:
project.datasets[0].timeSeries[0].loadData()
# Or for one dataset:
project.datasets[0].loadData()
# Or for all datasets:
project.loadData()
```

    Dataset - Name: Example Dataset, ID: 682ee7d8a3130d2327595758, Metadata: {}
    {}


### Get the data in the dataset
The datasets are provided as pandas dataframes


```python
# Access the data of a dataset
print("Dataset")
print(project.datasets[0].data.head())

print("\nTimeseries")
# Or just one time series
print(project.datasets[0].timeSeries[0].data.head())

# Or get all dataset in a project as list
project_data = project.data
print("\n#datasts: ", len(project_data))
```

    Dataset
                         time     Acc  Mag
    0 2025-05-22 09:01:12.595  0.0000  1.0
    1 2025-05-22 09:01:12.635  0.0001  1.0
    2 2025-05-22 09:01:12.675  0.0002  1.0
    3 2025-05-22 09:01:12.715  0.0003  1.0
    4 2025-05-22 09:01:12.755  0.0004  1.0
    
    Timeseries
                         time     Acc
    0 2025-05-22 09:01:12.595  0.0000
    1 2025-05-22 09:01:12.635  0.0001
    2 2025-05-22 09:01:12.675  0.0002
    3 2025-05-22 09:01:12.715  0.0003
    4 2025-05-22 09:01:12.755  0.0004
    
    #datasts:  11


### Get the labels in the dataset


```python
project.datasets[0].labelings
```




    []



### Labeling in the project
To labelings in a project define the labels


```python
project.labelings
```




    [{'_id': '682f07918245a094a595cdf5',
      'name': 'test',
      'labels': [{'name': 't1',
        'color': '#0081DD',
        '_id': '682f07918245a094a595cdf3'},
       {'name': 't2', 'color': '#C24A5F', '_id': '682f07918245a094a595cdf4'}],
      'projectId': '682ec257f42749f02e3a325f'}]




```python

```
