import argparse
from src.stream_analyzer import Stream_Analyzer
import time
import sys

class FFTAnalyzer:
    def __init__(self):
        self.args = self.parse_args()
        self.window_ratio = self.convert_window_ratio(self.args.window_ratio)
        
    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--device', type=int, default=None, dest='device',
                           help='pyaudio (portaudio) device index')
        parser.add_argument('--height', type=int, default=450, dest='height',
                           help='height, in pixels, of the visualizer window')
        parser.add_argument('--n_frequency_bins', type=int, default=200, dest='frequency_bins',
                           help='The FFT features are grouped in bins')
        parser.add_argument('--verbose', action='store_true')
        parser.add_argument('--window_ratio', default='24/9', dest='window_ratio',
                           help='float ratio of the visualizer window. e.g. 24/9')
        parser.add_argument('--sleep_between_frames', dest='sleep_between_frames', action='store_true',
                           help='when true process sleeps between frames to reduce CPU usage')
        return parser.parse_args()

    def convert_window_ratio(self, window_ratio):
        if '/' in window_ratio:
            dividend, divisor = window_ratio.split('/')
            try:
                return float(dividend) / float(divisor)
            except:
                raise ValueError('window_ratio should be in the format: float/float')
        raise ValueError('window_ratio should be in the format: float/float')

    def __call__(self):
        # Initialize Stream Analyzer with parameters
        ear = Stream_Analyzer(
            device=self.args.device,
            rate=None,
            FFT_window_size_ms=100,
            updates_per_second=60,
            smoothing_length_ms=50,
            n_frequency_bins=self.args.frequency_bins,
            visualize=1,
            verbose=self.args.verbose,
            height=self.args.height,
            window_ratio=self.window_ratio
        )

        fps = 60  # Target frame rate
        frame_time = 1.0 / fps
        last_update = time.time()
        print("Starting audio measurements...")
        
        try:
            while True:
                current_time = time.time()
                elapsed = current_time - last_update
                
                if elapsed >= frame_time:
                    raw_fftx, raw_fft, binned_fftx, binned_fft = ear.get_audio_features()
                    last_update = current_time
                elif self.args.sleep_between_frames:
                    sleep_time = frame_time - elapsed
                    if sleep_time > 0:
                        time.sleep(sleep_time * 0.99)
        except KeyboardInterrupt:
            print("\nStopping audio analysis...")
            ear.clean_up()

if __name__ == '__main__':
    analyzer = FFTAnalyzer()
    analyzer()