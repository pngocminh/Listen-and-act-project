from gtts import gTTS
import io
from pydub import AudioSegment
from pydub.playback import play

def synthesize_speech(text, speed=1.3):
    """Chuyển đổi văn bản thành âm thanh và phát âm thanh đó."""
    tts = gTTS(text=text, lang='vi', slow=False)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    audio = AudioSegment.from_mp3(fp)
    
    if speed != 1.0:
        new_frame_rate = int(audio.frame_rate * speed)
        audio = audio._spawn(audio.raw_data, overrides={"frame_rate": new_frame_rate})
        audio = audio.set_frame_rate(audio.frame_rate)
    
    play(audio)
synthesize_speech("Xin chào, bạn khỏe không?")