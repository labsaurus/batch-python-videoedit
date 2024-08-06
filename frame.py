import subprocess
import os
import random

# Direktori input (dan output)
video_directory = 'in'
frame_directory = 'frames'

# Mendapatkan daftar semua file video di direktori input
video_files = [f for f in os.listdir(video_directory) if os.path.isfile(os.path.join(video_directory, f))]

# Mendapatkan daftar semua file bingkai di direktori frames
frame_files = [f for f in os.listdir(frame_directory) if os.path.isfile(os.path.join(frame_directory, f))]

# Iterasi melalui setiap file video
for video_file in video_files:
    input_path = os.path.join(video_directory, video_file)
    temp_output_path = os.path.join(video_directory, f'temp_{video_file}')
    
    # Pilih bingkai secara acak dari daftar bingkai
    frame_file = random.choice(frame_files)
    frame_path = os.path.join(frame_directory, frame_file)
    
    # Perintah ffmpeg untuk menambahkan bingkai ke video
    ffmpeg_command = [
        'ffmpeg',
        '-i', input_path,
        '-i', frame_path,
        '-filter_complex', (
            '[0:v][1:v]overlay=0:0'
        ),
        '-codec:a', 'copy',
        temp_output_path
    ]
    
    # Menjalankan perintah ffmpeg dan menangkap output
    process = subprocess.run(ffmpeg_command, capture_output=True, text=True)
    
    # Cetak output dan error untuk debugging
    print(process.stdout)
    print(process.stderr)
    
    # Pastikan file sementara telah dibuat sebelum mengganti file asli
    if os.path.exists(temp_output_path):
        os.remove(input_path)  # Menghapus file asli
        os.rename(temp_output_path, input_path)  # Mengganti nama file sementara menjadi file asli
        print(f'Processed and replaced: {input_path} with frame: {frame_file}')
    else:
        print(f'Error processing: {input_path}, temporary file not found.')
