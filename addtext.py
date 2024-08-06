import subprocess
import os
import random

# Direktori input (dan output)
directory = 'in'

# Daftar teks yang akan dipilih secara acak
text_options = ["Hai semua", "Hai dunia", "Selamat datang"]

# Mendapatkan daftar semua file video di direktori
video_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# Iterasi melalui setiap file video
for video_file in video_files:
    input_path = os.path.join(directory, video_file)
    temp_output_path = os.path.join(directory, f'temp_{video_file}')
    
    # Pilih teks secara acak dari daftar
    selected_text = random.choice(text_options)
    
    # Perintah ffmpeg untuk menambahkan teks
    ffmpeg_command = [
        'ffmpeg',
        '-i', input_path,
    '-vf', f"drawtext=text='{selected_text}':fontfile=font.ttf:fontcolor=white:fontsize=74:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=h-th-140",
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
