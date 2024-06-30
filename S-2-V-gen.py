import cv2
import pyttsx3
import os

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()

# Function to generate speech audio from text
def text_to_speech(text, filename):
    tts_engine.save_to_file(text, filename)
    tts_engine.runAndWait()

# Function to create a video from script
def generate_video_from_script(script, output_video_path):
    # Dummy data for background and character images
    background_img_path = 'background.jpg'
    character_img_path = 'character.png'
    
    # Load background and character images
    background_img = cv2.imread(background_img_path)
    character_img = cv2.imread(character_img_path, cv2.IMREAD_UNCHANGED)

    # Video writer setup
    height, width, _ = background_img.shape
    video_writer = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), 1, (width, height))

    for scene in script:
        # Create a blank frame
        frame = background_img.copy()

        # Position character image on the frame
        x_offset = width // 2 - character_img.shape[1] // 2
        y_offset = height - character_img.shape[0]
        for c in range(0, 3):
            frame[y_offset:y_offset + character_img.shape[0], x_offset:x_offset + character_img.shape[1], c] = \
                character_img[:, :, c] * (character_img[:, :, 3] / 255.0) + frame[y_offset:y_offset + character_img.shape[0], x_offset:x_offset + character_img.shape[1], c] * (1.0 - character_img[:, :, 3] / 255.0)
        
        # Generate speech audio
        audio_filename = 'speech.wav'
        text_to_speech(scene['dialogue'], audio_filename)

        # Play speech audio
        os.system(f'play {audio_filename}')
        
        # Write frame to video
        video_writer.write(frame)
    
    video_writer.release()
    print(f'Video saved to {output_video_path}')

# Example usage
script = [
    {"scene": "A beautiful garden.", "dialogue": "Hello, welcome to our garden!"},
    {"scene": "A sunny beach.", "dialogue": "The beach is sunny and bright today."},
]

output_video_path = 'output_video.mp4'
generate_video_from_script(script, output_video_path)
