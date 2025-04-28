import os
import json
import csv
from hdfs import InsecureClient

def generate_csv_from_json(input_folder_path, output_folder_path):
  video_rows = []
  timeslot_rows = []
  alert_rows = []
  object_count_rows = []  # Nueva lista para registrar el conteo de objetos por tipo

  client = InsecureClient('http://namenode:9870', user='hadoop')

  files = client.list(input_folder_path)

  for file_name in files:
    if file_name.endswith('.json'):
      file_path = os.path.join(input_folder_path, file_name)
      
      with client.read(file_path, encoding='utf-8') as f:
        data = json.load(f)

      for video_id, video_data in data.items():
        camera_id = video_data['camera_id']
        location = video_data['location']
        priority = video_data['priority']
        video_file = video_data['video_file']
        date = video_data['date']
        
        video_rows.append([video_id, camera_id, location, priority, video_file, date])
        
        for timeslot in video_data['timeslots']:
          hour = timeslot['hour']
          video_minute = timeslot['video_minute']
          object_count = sum(timeslot['object_count'].values())
          
          # Registrar el conteo total de objetos por timeslot
          timeslot_rows.append([hour, video_minute, object_count, video_id])
          
          # Registrar el conteo de cada tipo de objeto (train, person, car, etc.)
          for object_type, count in timeslot['object_count'].items():
            object_count_rows.append([hour, video_minute, object_type, count, video_id])
            
        for alert in video_data['alerts']:
          alert_type = alert['type']
          timestamp = alert['timestamp']
          alert_rows.append([alert_type, timestamp, video_id])

  output_video_path = os.path.join(output_folder_path, 'Video.csv')
  
  with client.write(output_video_path, overwrite=True, encoding='utf-8') as writer:
    csv_writer = csv.writer(writer)
    csv_writer.writerow(['video_id', 'camera_id', 'location', 'priority', 'video_file', 'date'])
    csv_writer.writerows(video_rows)

  output_timeslot_path = os.path.join(output_folder_path, 'Timeslot.csv')
  with client.write(output_timeslot_path, overwrite=True, encoding='utf-8') as writer:
    csv_writer = csv.writer(writer)
    csv_writer.writerow(['hour', 'video_minute', 'object_count', 'video_id'])
    csv_writer.writerows(timeslot_rows)

  output_object_count_path = os.path.join(output_folder_path, 'ObjectCount.csv')
  with client.write(output_object_count_path, overwrite=True, encoding='utf-8') as writer:
    csv_writer = csv.writer(writer)
    csv_writer.writerow(['hour', 'video_minute', 'object_type', 'object_count', 'video_id'])
    csv_writer.writerows(object_count_rows)

  output_alert_path = os.path.join(output_folder_path, 'Alert.csv')
  with client.write(output_alert_path, overwrite=True, encoding='utf-8') as writer:
    csv_writer = csv.writer(writer)
    csv_writer.writerow(['type', 'timestamp', 'video_id'])
    csv_writer.writerows(alert_rows)

  print("Los archivos CSV se han generado correctamente")

def main():
  input_folder_path = '/user/hadoop/Videos_json'
  output_folder_path = '/user/hadoop/Videos_csv'
  generate_csv_from_json(input_folder_path, output_folder_path)

if __name__ == '__main__':
  main()
