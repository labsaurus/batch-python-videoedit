import subprocess
import os

# Direktori input (dan output)
directory = 'in'

# Mendapatkan daftar semua file video di direktori
video_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# Iterasi melalui setiap file video
for video_file in video_files:
    input_path = os.path.join(directory, video_file)
    temp_output_path = os.path.join(directory, f'temp_{video_file}')
    
    # Perintah ffmpeg untuk membalik video secara horizontal
    ffmpeg_command = [
        'ffmpeg',
        '-i', input_path,
        '-vf', 'hflip',
        temp_output_path
    ]
    
    # Menjalankan perintah ffmpeg
    subprocess.run(ffmpeg_command)
    
    # Menghapus file asli dan menggantinya dengan file sementara
    os.remove(input_path)
    os.rename(temp_output_path, input_path)

    print(f'Processed and replaced: {input_path}')
