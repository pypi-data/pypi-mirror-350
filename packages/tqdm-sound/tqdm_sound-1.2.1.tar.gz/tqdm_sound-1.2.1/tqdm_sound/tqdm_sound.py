import logging
import random
import time
import json

from typing import Optional, Iterator
from pathlib import Path
from importlib import resources
from concurrent.futures import ThreadPoolExecutor

from pynput import mouse, keyboard
from tqdm import tqdm
import simpleaudio as sa
import soundfile as sf
import sounddevice as sd

# Configure module logger
logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger(__name__)


def _adjust_volume(data: bytes, volume: float) -> bytes:
    """
    Scale raw PCM 16-bit little-endian audio data by a normalized volume factor.

    Args:
        data: Raw PCM byte buffer.
        volume: Normalized volume (0.0 = silent, 1.0 = original).

    Returns:
        Adjusted PCM byte buffer or silence if volume <= 0.
    """
    if volume <= 0:
        return b""
    vol = max(min(volume, 1.0), 0.0)
    import array
    pcm = array.array('h', data)
    for i in range(len(pcm)):
        pcm[i] = int(pcm[i] * vol)
    return pcm.tobytes()


class TqdmSound:
    """
    Manages sound playback for progress bars.

    Attributes:
        theme: Sound theme directory name.
        volume: Normalized foreground volume [0-1].
        background_volume: Normalized background volume [0-1].
        activity_mute_seconds: Seconds after activity to mute.
        dynamic_settings_file: Optional path to a JSON file controlling mute.
    """

    def __init__(
        self,
        theme: str = "ryoji_ikeda",
        volume: int = 100,
        background_volume: int = 50,
        activity_mute_seconds: Optional[int] = None,
        dynamic_settings_file: str = None
    ):
        """
        Initialize sound manager.

        Args:
            theme: Name of the theme folder under sounds/.
            volume: Foreground volume percentage (0-100).
            background_volume: Background volume percentage (0-100).
            activity_mute_seconds: Mute duration after user input.
            dynamic_settings_file: JSON file with {"is_muted": true/false}.

        Raises:
            ValueError: If volume parameters out of range.
            FileNotFoundError: If sound files or theme missing.
        """
        if not 0 <= volume <= 100:
            raise ValueError("Volume must be between 0 and 100")
        if not 0 <= background_volume <= 100:
            raise ValueError("Background volume must be between 0 and 100")

        # Normalize volumes
        self.volume = volume / 100.0
        self.background_volume = background_volume / 100.0
        self.theme = theme
        self.activity_mute_seconds = activity_mute_seconds
        self.dynamic_settings_file = Path(dynamic_settings_file)

        # Storage for effect and background data
        self.sounds: dict[str, sa.WaveObject] = {}
        self.click_sounds: list[sa.WaveObject] = []
        self.bg_data = None
        self.bg_samplerate = None
        self.bg_stream = None

        # Load all sound assets
        self._load_sounds()

        # Thread pool for playback
        self.executor = ThreadPoolExecutor(max_workers=4)
        self._bg_started = False

        # Track last user activity
        self.last_activity_time = time.time()
        self._setup_activity_monitors()

    def _setup_activity_monitors(self) -> None:
        """
        Launch listeners to reset activity timestamp on mouse/keyboard events.
        """
        self.mouse_listener = mouse.Listener(
            on_move=self._update_activity,
            on_click=self._update_activity,
            on_scroll=self._update_activity
        )
        self.keyboard_listener = keyboard.Listener(on_press=self._update_activity)
        self.mouse_listener.start()
        self.keyboard_listener.start()
        if self.activity_mute_seconds:
            # Allow immediate sound if mute configured
            self.last_activity_time = time.time() - self.activity_mute_seconds

    def _update_activity(self, *args, **kwargs) -> None:
        """
        Callback to record the time of latest user interaction.
        """
        self.last_activity_time = time.time()

    def _is_muted(self) -> bool:
        """
        Determine if sounds should be muted based on dynamic settings or recent activity.
        """
        # Dynamic file override
        if self.dynamic_settings_file:
            try:
                cfg = json.loads(Path(self.dynamic_settings_file).read_text())
                if cfg.get("is_muted", False):
                    return True
            except Exception:
                # On any read/parse error, ignore dynamic settings
                pass

        # Mute after activity if configured
        if (
            self.activity_mute_seconds is not None
            and (time.time() - self.last_activity_time) < self.activity_mute_seconds
        ):
            return True

        return False

    def _load_sounds(self) -> None:
        """
        Load click effects, start/mid/end tones, and background samples.

        Raises:
            FileNotFoundError: If expected files/directories are missing.
        """
        base = Path(resources.files('tqdm_sound')).joinpath('sounds', self.theme)
        if not base.exists():
            raise FileNotFoundError(f"Theme directory {base} not found")

        # Click effects
        for f in base.glob('click_*.wav'):
            self.click_sounds.append(sa.WaveObject.from_wave_file(str(f)))

        # Fixed tones
        files = {
            "start": "start_tone.wav",
            "semi_major": "semi_major.wav",
            "mid": "mid_tone.wav",
            "end": "end_tone.wav",
            "program_end": "program_end_tone.wav"
        }
        for name, fn in files.items():
            path = base / fn
            if not path.exists():
                raise FileNotFoundError(f"Missing sound file: {path}")
            self.sounds[name] = sa.WaveObject.from_wave_file(str(path))

        # Background loop loaded with soundfile
        bg_path = base / 'background_tone.wav'
        if not bg_path.exists():
            raise FileNotFoundError(f"Missing background file: {bg_path}")
        data, sr = sf.read(str(bg_path), dtype='float32')
        self.bg_data = data
        self.bg_samplerate = sr

    def set_volume(
        self,
        volume: float,
        mute: bool = False,
        background_volume: Optional[float] = None
    ) -> None:
        """
        Update normalized volumes or mute all sounds.

        Args:
            volume: Foreground volume (0-1).
            mute: If True, set volumes to zero.
            background_volume: Optional background volume override (0-1).
        """
        self.volume = 0.0 if mute else volume
        if background_volume is not None:
            self.background_volume = 0.0 if mute else background_volume

    def _start_background_loop(self) -> None:
        """
        Begin continuous background playback via sounddevice callback.
        Subsequent calls have no effect until stopped.
        """
        if self._bg_started or self.bg_data is None:
            return
        self._bg_started = True
        self._bg_pos = 0
        channels = self.bg_data.shape[1] if self.bg_data.ndim > 1 else 1

        def callback(outdata, frames, time_info, status):
            # Respect dynamic or activity-based mute
            if self._is_muted() or self.background_volume <= 0:
                outdata.fill(0)
                return
            for i in range(frames):
                idx = (self._bg_pos + i) % len(self.bg_data)
                sample = self.bg_data[idx] * self.background_volume
                outdata[i] = sample if channels > 1 else [sample]
            self._bg_pos = (self._bg_pos + frames) % len(self.bg_data)

        self.bg_stream = sd.OutputStream(
            samplerate=self.bg_samplerate,
            channels=channels,
            callback=callback
        )
        self.bg_stream.start()

    def _stop_background(self) -> None:
        """
        Cease background playback and reset state.
        """
        if self.bg_stream:
            self.bg_stream.stop()
            self.bg_stream.close()
        self._bg_started = False

    def play_random_click(self) -> None:
        """
        Play one randomly chosen click effect asynchronously.
        """
        if self._is_muted():
            return
        if self.click_sounds:
            wave = random.choice(self.click_sounds)
            self.executor.submit(wave.play)

    def play_sound(self, sound_name: str, loops: int = 0) -> None:
        """
        Play a named tone or start the background loop.

        Args:
            sound_name: One of 'start', 'semi_major', 'mid', 'end', 'program_end', 'background'.
            loops: Number of extra loops (unused).
        """
        if sound_name == 'background':
            return self._start_background_loop()
        if self._is_muted():
            return
        wave = self.sounds.get(sound_name)
        if wave:
            self.executor.submit(wave.play)

    def play_final_end_tone(self, volume: int = 100) -> None:
        """
        Play the program_end tone at specified level.

        Args:
            volume: Percentage volume (0-100).
        """
        if self._is_muted():
            return
        wave = self.sounds.get('program_end')
        if wave:
            self.executor.submit(wave.play)

    def play_sound_file(self, file_name: str, volume: Optional[int] = None) -> None:
        """
        Play any arbitrary wav file under current theme.

        Args:
            file_name: Filename in sounds/theme/.
            volume: Unused in this backend.
        """
        if self._is_muted():
            return
        path = Path(resources.files('tqdm_sound')).joinpath('sounds', self.theme, file_name)
        wave = sa.WaveObject.from_wave_file(str(path))
        self.executor.submit(wave.play)

    @staticmethod
    def sleep(duration: float) -> None:
        """
        Pause execution for given seconds (blocking).

        Args:
            duration: Seconds to sleep.
        """
        time.sleep(duration)

    def progress_bar(
        self,
        iterable,
        desc: str,
        volume: Optional[int] = None,
        background_volume: Optional[int] = None,
        end_wait: float = 0.04,
        ten_percent_ticks: bool = False,
        **kwargs
    ) -> 'SoundProgressBar':
        """
        Wrap an iterable in a sound-enabled tqdm.

        Args:
            iterable: Any iterable to track.
            desc: Progress description.
            volume: Foreground volume percent override.
            background_volume: Background volume percent override.
            end_wait: Delay after completion.
            ten_percent_ticks: Enable ticks every 10%.
            **kwargs: Additional tqdm args.

        Returns:
            SoundProgressBar instance.
        """
        vol = self.volume if volume is None else volume / 100.0
        bg = self.background_volume if background_volume is None else background_volume / 100.0
        self.set_volume(vol, False, bg)
        return SoundProgressBar(
            iterable,
            desc=desc,
            volume=vol,
            background_volume=bg,
            end_wait=end_wait,
            ten_percent_ticks=ten_percent_ticks,
            sound_manager=self,
            **kwargs
        )

    def close(self) -> None:
        """
        Stop listeners, background loop, and shut down executor.
        """
        if hasattr(self, 'mouse_listener') and self.mouse_listener.running:
            self.mouse_listener.stop()
        if hasattr(self, 'keyboard_listener') and self.keyboard_listener.running:
            self.keyboard_listener.stop()
        self._stop_background()
        self.executor.shutdown(wait=False)


class SoundProgressBar(tqdm):
    """
    tqdm subclass that triggers sounds at progress milestones.
    """

    def __init__(
        self,
        iterable,
        desc: str,
        volume: float,
        background_volume: float,
        end_wait: float,
        ten_percent_ticks: bool,
        sound_manager: TqdmSound,
        **kwargs
    ):
        """
        Initialize the sound progress bar.

        Args:
            iterable: Iterable to wrap.
            desc: Description text.
            volume: Foreground volume (0-1).
            background_volume: Background volume (0-1).
            end_wait: Delay after finish.
            ten_percent_ticks: Sound ticks every 10%.
            sound_manager: TqdmSound instance for playback.
            **kwargs: Other tqdm parameters.
        """
        self.sound_manager = sound_manager
        self.volume = volume
        self.background_volume = background_volume
        self.end_wait = end_wait
        self.ten_percent_ticks = ten_percent_ticks
        self.mid_played = False
        super().__init__(iterable, desc=desc, **kwargs)

    def _update_volume(self) -> None:
        """
        Respect mute-on-activity by adjusting volumes each tick.
        """
        mute = (
            self.sound_manager.activity_mute_seconds is not None
            and (time.time() - self.sound_manager.last_activity_time < self.sound_manager.activity_mute_seconds)
        )
        self.sound_manager.set_volume(self.volume, mute, self.background_volume)

    def __iter__(self) -> Iterator:
        """
        Iterate with sound callbacks:
        - start tone
        - background drone
        - click per iteration
        - mid-tone at 50%
        - optional ticks every 10%
        - end tone and stop drone

        Yields:
            Each item from the wrapped iterable.
        """
        # Kick off start + background
        self.sound_manager.play_sound('start')
        self.sound_manager.play_sound('background')
        played = {0, 50, 100}
        try:
            for i, item in enumerate(super().__iter__()):
                self._update_volume()
                self.sound_manager.play_random_click()
                if self.total:
                    pct = int((i + 1) / self.total * 100)
                    # Mid-progress tone once
                    if not self.mid_played and pct >= 50:
                        self.sound_manager.play_sound('mid')
                        self.mid_played = True
                    # Every 10% tick
                    if self.ten_percent_ticks:
                        t10 = (pct // 10) * 10
                        if t10 not in played and pct >= t10:
                            self.sound_manager.play_sound('semi_major')
                            played.add(t10)
                yield item
        finally:
            # Final sounds and cleanup
            self.sound_manager.play_sound('end')
            time.sleep(self.end_wait)
            self.sound_manager._stop_background()