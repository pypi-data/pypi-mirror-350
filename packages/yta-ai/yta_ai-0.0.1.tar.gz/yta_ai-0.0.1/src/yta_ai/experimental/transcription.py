"""
This module has interesting functionality but is outdated.
"""
from moviepy.editor import ImageSequenceClip, AudioFileClip, VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
from tqdm import tqdm
from yta_general_utils.text_processor import remove_accents
from yta_voice_module.stt.whisper import get_transcription_with_timestamps

import whisper_timestamped as whisper
import os
import cv2

def subtitle(video_filename):
    """
    Receives a video and creates a new one with subtitles at the bottom.
    """
    video = VideoFileClip(video_filename)
    video.audio.write_audiofile('tmp_transcription.mp3')
    transcription = get_transcription_with_timestamps('tmp_transcription.mp3')

    generator = lambda txt: TextClip(txt,
        font = 'Ubuntu-bold',
        fontsize = 72,
        color = 'white',
        stroke_color = 'black',
        stroke_width = 1,
    )

    subtitles = []
    for element in transcription['segments'][0]['words']:
        subtitles.append(((element['start'], element['end']), element['text']))

    subtitles = SubtitlesClip(subtitles, generator)
    result = CompositeVideoClip([video, subtitles.set_pos(('bottom'))])
    result.write_videofile("video_subtitled.mp4",
        fps = video.fps,
        temp_audiofile = "temp-audio.m4a",
        remove_temp = True,
        codec = "libx264",
        audio_codec = "aac"
    )

def transcribe(audio_filename):
    """
    TODO: This is being tested
    TEST: Obtains the subtitles based on video audio and sets it. Working on
    test files, not actual files.
    """
    # Testing video
    video = VideoFileClip('test_transcription.mp4') # 2.
    audio = video.audio # 3.
    audio.write_audiofile('test_transcription.mp3') # 4.

    transcription = get_transcription_with_timestamps('test_transcription.mp3')

    generator = lambda txt: TextClip(txt,
        font = 'Ubuntu-bold',
        fontsize = 72,
        color = 'white',
        stroke_color = 'black',
        stroke_width = 1,
    )

    subtitles = []
    for element in transcription['segments'][0]['words']:
        subtitles.append(((element['start'], element['end']), element['text']))

    subtitles = SubtitlesClip(subtitles, generator)
    video = VideoFileClip("test_transcription.mp4")
    # TODO: Here we have the audio error again
    result = CompositeVideoClip([video, subtitles.set_pos(('center'))])
    result.write_videofile("output.mp4",
        fps = video.fps,
        temp_audiofile = "temp-audio.m4a",
        remove_temp = True,
        codec = "libx264",
        audio_codec = "aac"
    )
    
def detect_word(audio_filename, word):
    """
    This method makes a transcription of the provided 'audio_filename',
    iterates over all words found and detects if the provided 'word' is
    in that audio. It returns an array with each time that 'word' exist
    in the audio, telling the 'start' and 'end' of that word in the 
    audio.
    """
    found = []

    transcription = get_transcription_with_timestamps(audio_filename)
    for element in transcription['segments'][0]['words']:
        if word in remove_accents(element['text'].lower()):
            found.append({
                'word': word,
                'start': element['start'],
                'end': element['end']
            })

    return found

# TODO: Remove this below as above is working
class VideoTranscriber:
    def __init__(self, model_path, video_path):
        self.model = whisper.load_model(model_path)
        self.video_path = video_path
        self.audio_path = ''
        self.text_array = []
        self.fps = 0
        self.char_width = 0

    def transcribe_video(self):
        print('Transcribing video')
        result = self.model.transcribe(self.audio_path)
        text = result["segments"][0]["text"]
        textsize = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
        cap = cv2.VideoCapture(self.video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        asp = 16/9
        ret, frame = cap.read()
        width = frame[:, int(int(width - 1 / asp * height) / 2):width - int((width - 1 / asp * height) / 2)].shape[1]
        width = width - (width * 0.1)
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        self.char_width = int(textsize[0] / len(text))
        
        for j in tqdm(result["segments"]):
            lines = []
            text = j["text"]
            end = j["end"]
            start = j["start"]
            total_frames = int((end - start) * self.fps)
            start = start * self.fps
            total_chars = len(text)
            words = text.split(" ")
            i = 0
            
            while i < len(words):
                words[i] = words[i].strip()
                if words[i] == "":
                    i += 1
                    continue
                length_in_pixels = len(words[i]) * self.char_width
                remaining_pixels = width - length_in_pixels
                line = words[i] 
                
                while remaining_pixels > 0:
                    i += 1 
                    if i >= len(words):
                        break
                    length_in_pixels = len(words[i]) * self.char_width
                    remaining_pixels -= length_in_pixels
                    if remaining_pixels < 0:
                        continue
                    else:
                        line += " " + words[i]
                
                line_array = [line, int(start) + 15, int(len(line) / total_chars * total_frames) + int(start) + 15]
                start = int(len(line) / total_chars * total_frames) + int(start)
                lines.append(line_array)
                self.text_array.append(line_array)
        
        cap.release()
        print('Transcription complete')
    
    def extract_audio(self, output_audio_path='audio.mp3'):
        print('Extracting audio')
        video = VideoFileClip(self.video_path)
        audio = video.audio 
        audio.write_audiofile(output_audio_path)
        self.audio_path = output_audio_path
        print('Audio extracted')
    
    def extract_frames(self, output_folder):
        print('Extracting frames')
        cap = cv2.VideoCapture(self.video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        asp = width / height
        N_frames = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = frame[:, int(int(width - 1 / asp * height) / 2):width - int((width - 1 / asp * height) / 2)]
            
            for i in self.text_array:
                if N_frames >= i[1] and N_frames <= i[2]:
                    text = i[0]
                    text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
                    text_x = int((frame.shape[1] - text_size[0]) / 2)
                    text_y = int(height/2)
                    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                    break
            
            cv2.imwrite(os.path.join(output_folder, str(N_frames) + ".jpg"), frame)
            N_frames += 1
        
        cap.release()
        print('Frames extracted')

    def create_video(self, output_video_path):
        print('Creating video')
        image_folder = os.path.join(os.path.dirname(self.video_path), "frames")
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
        
        self.extract_frames(image_folder)
        
        print("Video saved at:", output_video_path)
        images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
        images.sort(key=lambda x: int(x.split(".")[0]))
        
        frame = cv2.imread(os.path.join(image_folder, images[0]))
        height, width, layers = frame.shape
        
        clip = ImageSequenceClip([os.path.join(image_folder, image) for image in images], fps=self.fps)
        audio = AudioFileClip(self.audio_path)
        clip = clip.set_audio(audio)
        clip.write_videofile(output_video_path)

"""
# Example usage
model_path = "base"
video_path = PROJECT_ABSOLUTE_PATH + "output/2024-01-18_16-34-50.mp4"
output_video_path = PROJECT_ABSOLUTE_PATH + "output/transcription.mp4"

transcriber = VideoTranscriber(model_path, video_path)
transcriber.extract_audio()
transcriber.transcribe_video()
transcriber.create_video(output_video_path)
"""