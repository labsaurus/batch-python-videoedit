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
    
    # Perintah ffmpeg untuk menghapus metadata
    ffmpeg_command = [
        'ffmpeg',
        '-i', input_path,
        '-map_metadata', '-1',  # Menghapus semua metadata
        '-map_chapters', '-1',  # Menghapus semua chapter
        '-codec', 'copy',       # Menyalin codec tanpa re-encoding
        temp_output_path
    ]
    
    # Menjalankan perintah ffmpeg
    subprocess.run(ffmpeg_command)
    
    # Pastikan file sementara telah dibuat sebelum mengganti file asli
    if os.path.exists(temp_output_path):
        os.remove(input_path)  # Menghapus file asli
        os.rename(temp_output_path, input_path)  # Mengganti nama file sementara menjadi file asli
        print(f'Processed and replaced: {input_path}')
    else:
        print(f'Error processing: {input_path}, temporary file not found.')
