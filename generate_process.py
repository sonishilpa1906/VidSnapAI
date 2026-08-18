import os
import shutil
from text_to_audio import text_to_speech_file
import time
import subprocess

def text_to_audio(folder):
   with open (f"user_uploads/{folder}/desc.txt") as f:
        text = f.read()    
   text_to_speech_file(text, folder)

def create_reel(folder):
    try:
        command = f'''ffmpeg -f concat -safe 0 -i user_uploads/{folder}/input.txt -i user_uploads/{folder}/audio.mp3 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p static/reels/{folder}.mp4'''
        result = subprocess.run(command, shell=True, check= True)
        return True
    except Exception as e:
        print("Some error occurred while generating reel!")
        return False

if __name__ == "__main__":
    while(True):
        print("Processing Queue...")
        done_folders = os.listdir("done_uploads")
        pending_folders = os.listdir("user_uploads")

        for folder in pending_folders:
            if(folder not in done_folders):  
                print(f"processing folder: {folder}")
                text_to_audio(folder)
                output = create_reel(folder)
                if output == True:
                    source_path = os.path.join("user_uploads",folder)
                    destination_path = os.path.join("done_uploads", folder)
                    shutil.move(source_path, destination_path) 
        time.sleep(4)