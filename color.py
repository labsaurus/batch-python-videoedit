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
    
    # Perintah ffmpeg untuk mengubah warna video dengan filter hue
    ffmpeg_command = [
        'ffmpeg',
        '-i', input_path,
        '-vf', 'hue=h=0.2:s=1.5',  # Mengubah hue dan saturasi
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
        print(f'Processed and replaced: {input_path}')
    else:
        print(f'Error processing: {input_path}, temporary file not found.')
