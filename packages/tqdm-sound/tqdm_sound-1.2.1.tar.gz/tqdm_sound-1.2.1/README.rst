Sound TQDM
==========

``tqdm_sound`` adds sounds to the well-known progress bar library
`TQDM <https://github.com/tqdm/tqdm>`__.

It extends the TQDM base class, so anything you can do in TQDM you can
do in this library.

It can self-mute during mouse or keyboard activity.

Motivation
----------

I was renovating while running very long ML tasks, and I wanted a way of
tracking how everything was going while I had paint on my hands.

This was inspired by the work of Ryoji Ikeda and includes sounds similar
to
`data.matrix <https://www.youtube.com/watch?v=JZcMLjnm1ps&pp=ygUXZGF0YS5tYXRyaXggcnlvamkgaWtlZGE%3D>`__.
You can create any set of WAV files for your project, but I picked this
because it’s subtle and unobtrusive.

Use Cases
---------

1. Screen-free progress tracking
2. Accessibility for developers using screen readers
3. You hate your co-workers

Installation
------------

.. code:: bash

   pip install tqdm_sound

Examples
--------

Basic Example
~~~~~~~~~~~~~

.. code:: python

   from tqdm_sound import TqdmSound
   import random
   import time

   # Example usage:
   if __name__ == "__main__":
       sound_monitor = TqdmSound(theme="ryoji_ikeda", activity_mute_seconds=1)

       my_list = [0] * 50
       progress_one = sound_monitor.progress_bar(my_list, desc="Processing", volume=100, background_volume=30, end_wait=1, ten_percent_ticks=True)
       for _ in progress_one:
           time.sleep(random.uniform(.2, .5))

Silence When Active
~~~~~~~~~~~~~~~~~~~

If you’re actively using your mouse/keyboard, you can silence the
program via the ``activity_mute_seconds`` parameter. To mute for 5
seconds after mouse/keyboard activity:

.. code:: python

   sound_monitor = TqdmSound(theme="ryoji_ikeda", activity_mute_seconds=5)

   my_list = [0] * 10
   progress_one = sound_monitor.progress_bar(my_list, desc="Processing", volume=100, background_volume=30, end_wait=1, ten_percent_ticks=False)
   for _ in progress_one:
       time.sleep(random.uniform(.2, .5))

Play Final Sound
~~~~~~~~~~~~~~~~

This is just a shortcut to play ``program_end_tone.wav``:

.. code:: python

   sound_monitor.play_final_end_tone(50)

Play Any Sound in the Theme Directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Play any WAV file in the ``sounds/your_theme`` directory:

.. code:: python

   sound_monitor.play_sound_file('short_beep.wav', 50)

Sound Files
-----------

Add your own collection of sound files by adding a directory to the
``sounds`` folder, which will correspond to the “theme” argument.

Interval Sounds
~~~~~~~~~~~~~~~

``click_###.wav`` are played at every interval that is not the start,
middle, or end. You can have any number of these files in this format to
increase/decrease variation.

Major Sounds
~~~~~~~~~~~~

1. ``start_tone.wav`` plays at the start of each loop.
2. ``mid_tone.wav`` plays at the midpoint of each loop.
3. ``end_tone.wav`` plays at the end of each loop.
4. ``semi_major.wav`` plays at every 10% step when
   ``ten_percent_ticks=True``.
5. ``program_end_tone.wav`` is an optional sound that plays at the end
   of a given loop—this is just a convenience function you might use as
   the last loop in your program.
