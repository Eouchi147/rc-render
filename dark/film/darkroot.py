"""Where the darkengine folder is, and which ffmpeg to run.

ROOT is $DARK_ROOT when that is set, otherwise the darkengine folder (the parent of film/).
Everything else is found from it: ROOT/film, ROOT/look, ROOT/voice, ROOT/fonts, ROOT/sfx, ROOT/tex,
ROOT/vsco, ROOT/samples, ROOT/models and ROOT/out."""
import os
import shutil

ROOT = os.path.abspath(os.path.expanduser(
    os.environ.get('DARK_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

_FF = []


def ffmpeg_exe():
    """$FFMPEG if set, else the ffmpeg that ships with imageio-ffmpeg, else ffmpeg on the PATH."""
    if not _FF:
        exe = os.environ.get('FFMPEG')
        if not exe:
            try:
                import imageio_ffmpeg
                exe = imageio_ffmpeg.get_ffmpeg_exe()
            except Exception:
                exe = shutil.which('ffmpeg') or 'ffmpeg'
        _FF.append(exe)
    return _FF[0]
