# Race Visualiser

Visualise cars racing around a track using lap times and coloured dots.

## Overview

Race Visualiser is a Python/Pygame application that animates a dot (representing a car) traveling around a custom track defined by coordinates. You can specify the path and a sequence of lap times, and the program shows the car moving at the correct speed for each lap. It displays the current lap time, lap counter, and a start/finish line.

The intention is to be able to run this alongside old footage of motorsport races so you can get a better picture of what's going on.

Currently it is mostly a proof-of-concept. Only one vehicle is supported. However it is pretty cool and flexible for a very simple piece of code, and could even be expanded into a motorsport manager game.

## Features

* **Custom track** via coordinates file (supports any shape)
* **Lap times** from a file, with variable lap durations
* **Animated dot** shows the car’s movement
* **Lap timer** (hours\:minutes\:seconds.milliseconds)
* **Lap counter**
* **Start/Finish line** visually marked on the track

## Requirements

* Python 3.7+
* [pygame](https://www.pygame.org/) (`pip install pygame`)

## How to Use

1. **Prepare your track:**

* Create a file named `coordinates.txt`.
* Each line should be a pair of numbers between 0 and 1000 (e.g. `200,400`), representing the path of the car, in order.
* The first node is the start/finish line.
* You can use the path tool in GIMP. Trace a race track with the path tool and then export it and open the resulting file. Ask GPT to fix it up for you: `Can you please convert this list of coordinates into a simple list of unique coordinates. Remove all decimal value. Each unique coordinate should get a new line`
* I have included a tool which will normalize any set of coordinates to (10,10) - (990,990) so it looks nice in the window.

2. **Prepare your lap times:**

   * Create a file named `times.txt`.
   * Each line is a lap time in seconds (decimals allowed).

   Example:

   ```
   70.25
   72.10
   68.95
   ```

3. **Run the visualiser:**

   ```bash
   python race_visualiser.py
   ```

   * The window is resizable. The logical track coordinates always go from (0,0) to (1000,1000).
   * The red dot shows the car position; the blue line is the start/finish line.

4. **Controls:**

   * Close the window to quit.

## AI

This project was created with GPT.
