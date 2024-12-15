import sounddevice as sd
from scipy.io import wavfile
import os
import pyloudnorm as pyln
import numpy as np
import queue
import csv
import platform
import datetime
import pandas as pd
import time
from run_FFT_analyzer import FFTAnalyzer

def Safe_sound_main_menu():
    Function = SoundAnalyzeGUI()
    analyzer = FFTAnalyzer()

    while True:
        print("_"*50)
        print("\n Safe Sound - Real time audio analaysis")
        print("_"*50)
        print("\n 1. Record New Data - Measure Loudness in real time ")
        print("\n 2. Analyze Existing Data - here you can analyize data youve recorded")
        print("\n 3. Visualize Audio - visualize the audio enviorment around you. \n Credit: https://github.com/aiXander")
        print("\n 4. Exit")
        
        userinput = input("\nEnter your choice (1-4): ")
        
        if userinput == "1":
            Function.record_audio()
        elif userinput == "2":
            Function.analyze_existing_data()
        elif userinput == "3":
            analyzer()
        elif userinput == "4":
            print("\nThank you for using Sound Analysis System!")
            break
        else:
            print("\nInvalid choice. Please try again.")
        if userinput in ["1", "2"]:
            input("\nPress Enter to return to main menu...")

class SoundAnalyzeGUI:
    def __init__(self):
        # Audio settings
        self.freq = 44100
        self.duration = 5
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.block_size = int(self.freq * 0.5)
        self.audio_data = []
        
        # Create necessary directories
        self.csv_dir = "csv_recordings"
        self.recordings_dir = "recordings"
        for directory in [self.csv_dir, self.recordings_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
        
        # Initialize pyloudnorm meter
        self.meter = pyln.Meter(self.freq)
        
        # Get system audio info
        self.get_system_audio_info()

    def get_system_audio_info(self):
        """Get system audio device information"""
        try:
            default_input = sd.query_devices(kind='input')
            self.source_name = default_input['name']
            self.source_version = f"{platform.system()} {platform.release()}"
        except Exception as e:
            print(f"Error getting audio device info: {e}")
            self.source_name = "x"
            self.source_version = "x"

    def record_audio(self):
        print("\n recording has started ...")        
        self.is_recording = True
        self.audio_data = []
        final_loudness = None

        try:
            with sd.InputStream(
                channels=1,
                samplerate=self.freq,
                callback=self.audio_callback,
                blocksize=self.block_size
            ) as stream:
                total_frames = int(self.duration * self.freq)
                recorded_frames = 0
                
                while recorded_frames < total_frames:
                    if not self.audio_queue.empty():
                        data = self.audio_queue.get()
                        audio_data = data.flatten().astype(np.float32)
                        try:
                            loudness = self.meter.integrated_loudness(audio_data)
                            final_loudness = loudness
                            print(f"\rCurrent Loudness: {loudness:.1f} DB", end="")
                        except ValueError:
                            pass
                    recorded_frames += self.block_size
                    time.sleep(0.1)

            if self.audio_data:
                # Save WAV file
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                wav_filename = os.path.join(self.recordings_dir, f"recording_{timestamp}.wav")
                full_recording = np.concatenate(self.audio_data)
                wavfile.write(wav_filename, self.freq, full_recording)
                
                # Save CSV file
                if final_loudness is not None:
                    self.write_to_csv(final_loudness, timestamp)
                
                print(f"\n\nRecording completed!")
                print(f"WAV file saved as: {wav_filename}")
                print(f"CSV file saved in: {self.csv_dir}")
            
        except Exception as e:
            print(f"\nRecording error: {e}")
        finally:
            self.is_recording = False

    def audio_callback(self, indata, frames, time, status):
        """Callback for audio stream"""
        if status:
            print(f"Status: {status}")
        self.audio_data.append(indata.copy())
        self.audio_queue.put(indata.copy())

    def write_to_csv(self, loudness, timestamp):
        """Write recording metadata to CSV"""
        current_time = datetime.datetime.now()
        end_time = current_time + datetime.timedelta(seconds=self.duration)
        
        data = {
            'Predic Environment': 'Indoor',
            'startDate': current_time.strftime('%Y-%m-%d %H:%M:%S'),
            'endDate': end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'sourceName': self.source_name,
            'sourceVersion': self.source_version,
            'decibel_level': round(loudness, 2)
        }
        
        csv_filename = os.path.join(self.csv_dir, f"audio_record_{timestamp}.csv") # data/audio_records.csv
        with open(csv_filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            writer.writeheader()
            writer.writerow(data)

    def analyze_existing_data(self):
        try:
            df = pd.read_csv("/Loudness-measuring-main-2/data/audio_records.csv")
            while True:
                print("\nSafe Sound Analysis:")
                print("1. Basic Statistics")
                print("2. Analyze audio by source")
                print("3. Duration Analysis")
                print("4. Return back home")
                
                userinput = input("\nEnter your choice (1-4): ")
                
                if userinput == "1":
                    print("\nBasic Statistical Analysis:")
                    print("\nDecibel Level Statistics:")
                    print(df['decibel_level'].describe())
                    print("\nEnvironment Counts:")
                    print(df['Predic Environment'].value_counts())
                
                elif userinput == "2":
                    print("\nAnalysis by Source:")
                    source_stats = df.groupby('sourceName')['decibel_level'].agg(['mean', 'min', 'max', 'count'])
                    print(source_stats)
                
                elif userinput == "3":
                    print("\nTime-Duration Analysis:")
                    df['startDate'] = pd.to_datetime(df['startDate'])
                    time_stats = df.groupby(df['startDate'].dt.date)['decibel_level'].agg(['mean', 'min', 'max', 'count'])
                    print(time_stats)
                
                elif userinput == "4":
                    break

                else:
                    print("\nInvalid choice. Please try again.")
                
                input("\nPress Enter to continue...")

        except FileNotFoundError as e:
            print(f"\nError: audio_records.csv not found! {e}")
        except Exception as e:
            print(f"\nError analyzing data: {e}")

if __name__ == "__main__":
   Safe_sound_main_menu()

