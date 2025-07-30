import pytest
import pygame
from tqdm_sound.tqdm_sound import TqdmSound, SoundProgressBar

@pytest.fixture(scope="module")
def sound_manager():
    return TqdmSound(theme="ryoji_ikeda")

@pytest.fixture(scope="function")
def reset_pygame():
    pygame.mixer.quit()
    pygame.mixer.init()


def test_volume_initialization():
    ts = TqdmSound(volume=80, background_volume=40)
    assert ts.volume == 0.8
    assert ts.background_volume == 0.4


def test_invalid_volume():
    with pytest.raises(ValueError):
        TqdmSound(volume=150)
    with pytest.raises(ValueError):
        TqdmSound(background_volume=-10)


def test_sound_loading(sound_manager):
    assert "start" in sound_manager.sounds
    assert "mid" in sound_manager.sounds
    assert "end" in sound_manager.sounds
    assert "background" in sound_manager.sounds
    assert "program_end" in sound_manager.sounds
    assert len(sound_manager.click_sounds) > 0


def test_set_volume(sound_manager):
    sound_manager.set_volume(50)
    assert sound_manager.volume == 50
    sound_manager.set_volume(100, mute=True)
    assert sound_manager.volume == 0


def test_play_random_click(sound_manager):
    if sound_manager.click_sounds:
        sound_manager.play_random_click()  # No exception should be raised


def test_play_sound(sound_manager):
    sound_manager.play_sound("start")  # Should not raise errors


def test_progress_bar(sound_manager):
    iterable = range(10)
    pb = SoundProgressBar(iterable, desc="Test", volume=50, background_volume=30, end_wait=0.01,
                          ten_percent_ticks= True, sound_manager=sound_manager)
    list(pb)  # Ensure iteration completes without errors
    assert pb.mid_sound_played
