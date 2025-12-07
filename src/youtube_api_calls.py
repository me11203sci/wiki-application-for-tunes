"""
YouTube audio extraction utilities using yt-dlp and FFmpeg.

This module provides a simple high-level wrapper around `yt-dlp` for
downloading audio from a single YouTube video and converting it into
an MP3 file via FFmpeg. Options are preconfigured for safe defaults,
including disabling playlist downloads and ensuring high-quality audio
extraction.

Functions
---------
download_youtube_mp3
    Download the audio from a single YouTube video URL and save it as an MP3.

Notes
-----
This module requires both `yt-dlp` and `ffmpeg` to be installed on the system.
The user is responsible for ensuring FFmpeg is available in the system PATH.

Examples
--------
Download a single track to the default downloads folder:

>>> download_youtube_mp3("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

Download to a custom directory:

>>> download_youtube_mp3(
...     "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
...     download_path="music/%(title)s.%(ext)s"
... )
"""

import yt_dlp


def download_youtube_mp3(
    yt_link: str, download_path: str = "downloads/%(title)s.%(ext)s"
) -> None:
    """
    Download a YouTube video's audio as an MP3 file using yt-dlp and FFmpeg.

    This function wraps `yt_dlp.YoutubeDL` with predefined options that ensure
    high-quality audio extraction and automatic conversion to MP3 format.
    Playlist URLs are explicitly disabled to guarantee that only a single video
    is downloaded, even if the provided link points to a YouTube Mix or
    auto-generated playlist.

    Parameters
    ----------
    yt_link : str
        The full URL of the YouTube video whose audio should be downloaded.
    download_path : str, optional
        A yt-dlp output template specifying where the resulting MP3 file should
        be saved. Defaults to ``'downloads/%(title)s.%(ext)s'``. May include
        yt-dlp template fields such as ``%(title)s`` and ``%(ext)s``.

    Returns
    -------
    None
        This function performs the download and does not return anything.

    Raises
    ------
    yt_dlp.utils.DownloadError
        If the download fails or the YouTube link is invalid.
    OSError
        If the output directory cannot be created or written to.

    Notes
    -----
    FFmpeg must be installed and available in the system PATH for MP3
    conversion to succeed. If FFmpeg is missing, yt-dlp will raise an error
    during post-processing.

    Examples
    --------
    Download an MP3 into the default folder:

    >>> download_youtube_mp3("https://youtu.be/dQw4w9WgXcQ")

    Save to a custom path:

    >>> download_youtube_mp3(
    ...     "https://youtu.be/dQw4w9WgXcQ",
    ...     download_path="music/%(title)s.%(ext)s"
    ... )
    """
    ydl_opts = {
        # Download the best quality *audio* only
        "format": "bestaudio/best",
        # Ensure there is just one song, no playlist
        "noplaylist": True,
        # FFmpeg post-processing: convert to MP3
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",  # kbps
            }
        ],
        # Output file naming
        "outtmpl": download_path,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([yt_link])
