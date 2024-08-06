import subprocess
import os

# Direktori input (dan output)
video_directory = 'in'
background_image = 'putih/putih.png'

# Mendapatkan daftar semua file video di direktori input
video_files = [f for f in os.listdir(video_directory) if os.path.isfile(os.path.join(video_directory, f))]

# Iterasi melalui setiap file video
for video_file in video_files:
    input_path = os.path.join(video_directory, video_file)
    temp_output_path = os.path.join(video_directory, f'temp_{video_file}')
    
    # Perintah ffmpeg untuk mengecilkan video dan menambahkan background putih
    ffmpeg_command = [
        'ffmpeg',
        '-i', input_path,
        '-i', background_image,
        '-filter_complex', (
            '[0:v]scale=iw*0.95:ih*0.95[scaled];'  # Mengecilkan video asli
            '[1:v][scaled]overlay=(W-w)/2:(H-h)/2'  # Menempatkan video di tengah background putih
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
        print(f'Processed and replaced: {input_path}')
    else:
        print(f'Error processing: {input_path}, temporary file not found.')
