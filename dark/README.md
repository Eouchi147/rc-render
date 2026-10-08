# darkengine

This folder makes the Bamberg film on your Mac: it paints the pictures, adds the narration, sound and music, and saves a video. It needs an Apple Silicon Mac with macOS 13 or newer and about 5 GB of free disk space.

Put the `darkengine` folder on your Desktop, open Terminal (Applications > Utilities > Terminal) and run two commands:

1. Once, to set up: `bash ~/Desktop/darkengine/setup.sh`
   It installs Python and downloads about 2.5 GB of sounds, textures and instrument samples: allow 10-30 minutes, depending on your internet. If it stops, run it again; it carries on where it left off.
2. To make the video: `bash ~/Desktop/darkengine/render.sh test`
   Allow roughly 5-15 minutes the first time (it paints the scene once and keeps it); later renders are a few minutes quicker.

Folder somewhere else? Type `bash ` (with a space), drag `setup.sh` (or `render.sh`, then type ` test`) from the folder into the Terminal window, and press Return.
macOS may ask whether Terminal may access your Desktop folder: click Allow.
The finished video, "Bamberg test clip (Mac render).mp4", appears next to the darkengine folder (on your Desktop), and a Finder window opens to show it.
