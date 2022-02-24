class ExamException(Exception):
  pass

class CSVFile():

  def __init__(self, name):
    self.name = name

  def get_data(self):
    try:
        my_file = open(self.name, 'r')
        my_file.readline()
        my_file.close()
    except Exception:
        raise ExamException("Invalid file")


    data = []

    my_file = open(self.name, 'r')
    for line in my_file:    
      elements = line.split(',')
      elements[-1] = elements[-1].strip()
      if (elements[0] != 'date'):
        data.append(elements)

    my_file.close()

    return data
        

class CSVTimeSeriesFile(CSVFile):

  def get_data(self):
    parsed_data = super().get_data()
    time_series = []

    cur_year = 0
    cur_month = 0

    prev_year = 0
    prev_month = 0

    cur_date = ''
    prev_date = ''

    
    for index in range(len(parsed_data)-1):
      parsed_date = parsed_data[index][0].split('-')
      if len(parsed_date) < 2:
        del parsed_data[index]

    for data in parsed_data:
      year, month = data[0].split('-')
      cur_year = int(year)
      cur_month = int(month)
      cur_date = data[0]

      if (prev_year > cur_year) and (prev_month > cur_month):
        raise ExamException("Time series isn't ordered")

      if cur_date == prev_date:
        raise ExamException("Duplicated time series")
      
      prev_year = cur_year
      prev_month = cur_month
      prev_date = cur_date


    for data in parsed_data:
      if len(data) > 1:
        try:
          if int(data[1]) >= 0:
            data[1] = int(data[1])
            time_series.append(data)
        except Exception:
          pass
        
    return time_series


def detect_similar_monthly_variations(time_series, years):
  if time_series == None:
    raise ExamException("Invalid time series")

  if len(time_series) == 0:
    raise ExamException("Time series can't be void")

  if (years[1] - years[0]) != 1:
    raise ExamException("Years are not consecutive")

  grouped_data = {
    years[0]: [0 for x in range(12)],
    years[1]: [0 for x in range(12)]
  }

  difference = {
    years[0]: [],
    years[1]: []
  }

  results = []

  for year in years:
    for month in range(12):
      for data in time_series:
        if data[0] == '{}-{:02d}'.format(year, month + 1):
          grouped_data[year][month] = data[1]
  
  
  for month in range(11):
    
    difference[years[0]].append(abs(grouped_data[years[0]][month] - grouped_data[years[0]][month+1]))
    difference[years[1]].append(abs(grouped_data[years[1]][month] - grouped_data[years[1]][month+1]))

  for month in range(11):
    print(difference[years[0]][month] - difference[years[1]][month])
    results.append(-2 <= difference[years[0]][month] - difference[years[1]][month] <= 2)

  return results

time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()