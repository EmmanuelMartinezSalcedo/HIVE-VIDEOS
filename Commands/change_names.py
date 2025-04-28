import os
import random
import argparse
from datetime import datetime, timedelta

def generate_random_date():
  start_date = datetime(2024, 1, 1)
  end_date = datetime(2024, 12, 31)
  delta = end_date - start_date
  random_days = random.randint(0, delta.days)
  random_date = start_date + timedelta(days=random_days)
  return random_date.strftime("%d-%m-2024")

def rename_videos_in_folder(folder_path):
  for filename in os.listdir(folder_path):
    if filename.endswith(".mp4"):
      random_date = generate_random_date()
      new_name = f"{random_date}.mp4"
      
      old_file = os.path.join(folder_path, filename)
      new_file = os.path.join(folder_path, new_name)
      
      os.rename(old_file, new_file)
      print(f"Renombrado: {filename} -> {new_name}")

if __name__ == "__main__":

  parser = argparse.ArgumentParser(description="Renombrar videos a fechas aleatorias del 2024.")
  parser.add_argument("folder_path", help="Ruta a la carpeta que contiene los videos.")
  args = parser.parse_args()
  
  rename_videos_in_folder(args.folder_path)