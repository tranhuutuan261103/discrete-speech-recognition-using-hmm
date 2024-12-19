import os
import wave
import pyaudio

class AudioRecorder:
    def __init__(self, output_dir='../datasets_testing', categories=None, sample_rate=16000, record_seconds=2):
        self.output_dir = output_dir
        self.categories = categories or ["a", "ba", "bai", "bay", "bon", "cham", "chay", "chin", "chu", "co", 
    "cuoi", "dau", "ddung", "doc", "dung", "e", "giam", "gio", "giup", 
    "hai", "huy", "i", "ke", "khong", "lai", "lap", "lui", "luu", "mot", 
    "muc", "nam", "ngay", "ngung", "nhanh", "nho", "o", "sai", "sau", "tai", 
    "tam", "tang", "thodia", "tiep", "to", "toi", "truoc", "tuoi", "u", 
    "vao", "ve", "xoa", "xong"]
        self.sample_rate = sample_rate
        self.record_seconds = record_seconds
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1

        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(self.output_dir, exist_ok=True)
        for category in self.categories:
            os.makedirs(os.path.join(self.output_dir, category), exist_ok=True)

    def record_audio(self, category, file_name):
        p = pyaudio.PyAudio()

        stream = p.open(format=self.format,
                        channels=self.channels,
                        rate=self.sample_rate,
                        input=True,
                        frames_per_buffer=self.chunk)

        print(f"Recording for '{category}'...")
        frames = []

        for _ in range(0, int(self.sample_rate / self.chunk * self.record_seconds)):
            data = stream.read(self.chunk)
            frames.append(data)

        print("Recording finished.")

        stream.stop_stream()
        stream.close()
        p.terminate()

        # Lưu file vào thư mục tương ứng
        file_path = os.path.join(self.output_dir, category, file_name)
        with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(p.get_sample_size(self.format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(frames))
        print(f"File saved: {file_path}")

    def start_recording(self):
        for category in self.categories:
            print(f"\nStart recording for category: '{category}'")
            num_files = len(os.listdir(os.path.join(self.output_dir, category)))
            while True:
                file_name = f"{category}_{num_files + 1}.wav"
                self.record_audio(category, file_name)
                num_files += 1

                cont = input("Press Enter to record another file for this category, or type 'q' to quit: ").strip().lower()
                if cont == 'q':
                    break

if __name__ == '__main__':
    recorder = AudioRecorder(output_dir='../datasets_testing', categories=["a", "ba", "bai", "bay", "bon", "cham", "chay", "chin", "chu", "co", 
    "cuoi", "dau", "ddung", "doc", "dung", "e", "giam", "gio", "giup", 
    "hai", "huy", "i", "ke", "khong", "lai", "lap", "lui", "luu", "mot", 
    "muc", "nam", "ngay", "ngung", "nhanh", "nho", "o", "sai", "sau", "tai", 
    "tam", "tang", "thodia", "tiep", "to", "toi", "truoc", "tuoi", "u", 
    "vao", "ve", "xoa", "xong"])
    recorder.start_recording()
