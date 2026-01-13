import os
import subprocess
from text_to_audio import text_to_speech_file


def process_folder(folder):
    base = os.path.join("user_uploads", folder)
    flag = os.path.join(base, ".processed")

    try:
        # Prevent reprocessing
        if os.path.exists(flag):
            print(f"[SKIP] {folder} already processed")
            return

        desc_path = os.path.join(base, "desc.txt")
        input_path = os.path.join(base, "input.txt")
        audio_path = os.path.join(base, "audio.mp3")
        output_video = os.path.join("static", "reels", f"{folder}.mp4")

        # Validate inputs
        if not os.path.exists(desc_path):
            print(f"[ERROR] {folder}: desc.txt missing")
            return

        if not os.path.exists(input_path) or os.path.getsize(input_path) == 0:
            print(f"[ERROR] {folder}: input.txt missing or empty")
            return

        os.makedirs(os.path.dirname(output_video), exist_ok=True)

        # Generate audio
        if not os.path.exists(audio_path):
            print(f"[INFO] Generating audio for {folder}")
            with open(desc_path, "r", encoding="utf-8") as f:
                text = f.read().strip()

            if not text:
                print(f"[ERROR] {folder}: desc.txt empty")
                return

            text_to_speech_file(text, folder)

            if not os.path.exists(audio_path):
                print(f"[ERROR] {folder}: audio generation failed")
                return

        # FFmpeg command (CORRECT)
        command = [
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", input_path,
            "-i", audio_path,
            "-vf",
            "scale=1080:1920:force_original_aspect_ratio=decrease,"
            "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-shortest",
            "-r", "30",
            "-pix_fmt", "yuv420p",
            output_video
        ]

        print(f"[INFO] Running FFmpeg for {folder}")
        subprocess.run(command, check=True)

        open(flag, "w").close()
        print(f"[SUCCESS] {folder} processed successfully")

    except subprocess.CalledProcessError as e:
        print(f"[FFMPEG ERROR] {folder}", e)

    except Exception as e:
        print(f"[UNEXPECTED ERROR] {folder}", e)
