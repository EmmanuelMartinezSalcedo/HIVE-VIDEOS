import os
import cv2
import random
import json
from ultralytics import YOLO
from datetime import datetime

def parse_to_hive_date_format(date_str):
  try:
    return datetime.strptime(date_str, '%d-%m-%Y').strftime('%Y-%m-%d')
  except ValueError:
    return None


def parse_to_hive_timestamp_format(date_str, hour_int):
  try:
    dt_str = f"{date_str} {hour_int:02d}:00:00"
    return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
  except ValueError:
    return None


def detect_objects_yolo(frame, model):
  temp_filename = "temp_frame.jpg"
  cv2.imwrite(temp_filename, frame)
  results = model(temp_filename, imgsz=640, conf=0.25)
  detections = results[0].boxes.cls.tolist()
  object_count = {}
  names = model.names
  for cls_idx in detections:
    label = names[int(cls_idx)]
    object_count[label] = object_count.get(label, 0) + 1
  os.remove(temp_filename)
  return object_count

def generate_video_metadata(video_path, model_path='yolov8n.pt'):
  model = YOLO(model_path)

  parts = video_path.replace("\\", "/").split('/')
  location = parts[-3]
  camera_id = parts[-2]
  video_name = parts[-1]
  date_name = os.path.splitext(video_name)[0]

  date_name = parse_to_hive_date_format(date_name)

  priorities = ["very_low", "low", "medium", "high", "very_high"]
  priority = random.choice(priorities)

  cap = cv2.VideoCapture(video_path)
  if not cap.isOpened():
    raise Exception("No se pudo abrir el video")

  frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  fps = cap.get(cv2.CAP_PROP_FPS)
  duration = frame_count / fps
  duration_seconds = int(duration)

  if duration_seconds <= 60:
    seconds_selected = sorted(random.sample(range(0, duration_seconds), k=min(5, duration_seconds)))
  else:
    total_minutes = duration_seconds // 60
    num_timeslots = random.randint(1, min(10, total_minutes))
    minutes_selected = sorted(random.sample(range(0, total_minutes), num_timeslots))
    seconds_selected = [random.randint(0, 59) for _ in minutes_selected]

  base_hours = sorted(random.sample(range(0, 24), k=len(seconds_selected)))

  timeslots = []
  timestamps_for_alerts = []

  for idx, minute in enumerate(minutes_selected if duration_seconds > 60 else [0] * len(seconds_selected)):
    second = seconds_selected[idx]
    hour = base_hours[idx]
    minute_in_seconds = minute * 60 + second

    if minute_in_seconds >= duration_seconds:
      minute_in_seconds = duration_seconds - 1

    cap.set(cv2.CAP_PROP_POS_MSEC, minute_in_seconds * 1000)
    ret, frame = cap.read()
    if not ret:
      continue

    object_count = detect_objects_yolo(frame, model)

    hour_timestamp = parse_to_hive_timestamp_format(date_name, hour)

    timeslots.append({
      "hour": hour_timestamp,
      "video_minute": f"{minute:02d}:{second:02d}",
      "object_count": object_count
    })
    timestamps_for_alerts.append({
      "minute": minute,
      "hour": hour_timestamp,
      "object_count": object_count
    })

  cap.release()

  alerts = []
  for ts in timeslots:
    alert_type = None
    seed = random.random()

    if seed < 0.25:
      object_count = ts['object_count']

      if object_count.get("person", 0) > 2 and random.random() < 0.20:
        alert_type = "presence_out_of_hours"
      elif object_count.get("person", 0) > 0 and random.random() < 0.30:
        alert_type = "suspicious_movement"
      elif sum(count for obj, count in object_count.items() if obj not in ["car", "train", "motorcycle", "person", "bicycle", "truck", "bus", "stop sign"]) == 1 and random.random() < 0.40:
        alert_type = "abandoned_object"
      elif object_count.get("person", 0) == 1 and random.random() < 0.15:
        alert_type = "intrusion"
      elif random.random() < 0.15:
        alert_type = "camera_failure"
      elif object_count.get("car", 0) > 0 and random.random() < 0.20:
        alert_type = "unrecognized_vehicle"
      elif object_count.get("car", 0) > 10:
        alert_type = "high_traffic_volume"
      elif object_count.get("person", 0) > 0 and random.random() < 0.30:
        alert_type = "unauthorized_access"
      else:
        alert_type = "not_found_alert"

    if alert_type is not None:
      alerts.append({
        "type": alert_type,
        "timestamp": ts['hour']
      })

  final_json = {
    f"{location}_{camera_id}_{date_name}": {
      "camera_id": camera_id,
      "location": location,
      "priority": priority,
      "video_file": f"{location}/{camera_id}/{video_name}",
      "date": date_name,
      "timeslots": timeslots,
      "alerts": alerts
    }
  }

  return final_json

def process_videos_in_directory(videos_directory):
  locations = os.listdir(videos_directory)

  counter = 1

  for location in locations:
    cameras = os.listdir(f"{videos_directory}/{location}")
    
    for camera in cameras:
      video_files = os.listdir(f"{videos_directory}/{location}/{camera}")

      for video_path in video_files:
        if video_path.endswith('.mp4'):
          print(f"Procesando video: {video_path}")
          local_video_path = os.path.join(videos_directory, location, camera, video_path)

          metadata = generate_video_metadata(local_video_path)

          video_name = f"{counter:04d}.json"
          counter += 1

          output_dir = "Videos_json"
          os.makedirs(output_dir, exist_ok=True)

          output_filename = os.path.join(output_dir, video_name)

          with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=4)

          print(f"Archivo JSON generado: {output_filename}")

if __name__ == "__main__":
  videos_directory = "Videos"
  process_videos_in_directory(videos_directory)
