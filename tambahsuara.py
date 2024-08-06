import subprocess
import os
import random

# Direktori input video dan suara
video_directory = 'in'
audio_directory = 'suara/fun'

# Mendapatkan daftar semua file video di direktori input
video_files = [f for f in os.listdir(video_directory) if os.path.isfile(os.path.join(video_directory, f))]

# Mendapatkan daftar semua file suara di direktori audio
audio_files = [f for f in os.listdir(audio_directory) if os.path.isfile(os.path.join(audio_directory, f))]

# Fungsi untuk mendapatkan durasi file media
def get_duration(file_path):
    result = subprocess.run([
        'ffprobe',
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        file_path
    ], capture_output=True, text=True)
    return float(result.stdout.strip())

# Iterasi melalui setiap file video
for video_file in video_files:
    input_path = os.path.join(video_directory, video_file)
    temp_output_path = os.path.join(video_directory, f'temp_{video_file}')
    
    # Pilih suara secara acak dari daftar suara
    audio_file = random.choice(audio_files)
    audio_path = os.path.join(audio_directory, audio_file)
    
    # Mendapatkan durasi video dan audio
    video_duration = get_duration(input_path)
    audio_duration = get_duration(audio_path)
    
    # Membuat suara baru yang sesuai dengan durasi video
    adjusted_audio_path = os.path.join(video_directory, f'adjusted_{audio_file}')
    
    if audio_duration >= video_duration:
        # Potong audio jika durasi lebih panjang dari video
        ffmpeg_audio_command = [
            'ffmpeg',
            '-i', audio_path,
            '-t', str(video_duration),
            '-y', adjusted_audio_path
        ]
    else:
        # Loop audio jika durasi lebih pendek dari video
        loop_count = int(video_duration // audio_duration) + 1
        ffmpeg_audio_command = [
            'ffmpeg',
            '-stream_loop', str(loop_count),
            '-i', audio_path,
            '-t', str(video_duration),
            '-y', adjusted_audio_path
        ]
    
    subprocess.run(ffmpeg_audio_command)
    
    # Perintah ffmpeg untuk menambahkan suara baru dengan volume 30%
    ffmpeg_command = [
        'ffmpeg',
        '-i', input_path,
        '-i', adjusted_audio_path,
        '-filter_complex', '[1:a]volume=0.1[a1];[0:a][a1]amix=inputs=2:duration=first',
        '-c:v', 'copy',
        '-shortest',
        '-y', temp_output_path
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
        os.remove(adjusted_audio_path)  # Menghapus file audio sementara
        print(f'Processed and replaced: {input_path} with additional audio: {audio_file}')
    else:
        print(f'Error processing: {input_path}, temporary file not found.')
