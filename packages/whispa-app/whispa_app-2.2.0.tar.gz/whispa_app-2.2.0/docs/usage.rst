Usage Guide
===========

This guide will help you get started with Whispa App and explain its main features.

Basic Usage
----------

1. Launch the Application
~~~~~~~~~~~~~~~~~~~~~~~

After installation, you can launch Whispa App in two ways:

- From the Start Menu (Windows installer)
- From the command line: ``whispa-app``

2. Select Audio File
~~~~~~~~~~~~~~~~~~

Click the "Browse" button to select an audio file. Supported formats:

- WAV
- MP3
- M4A
- FLAC
- OGG
- AAC

3. Choose Model Size
~~~~~~~~~~~~~~~~~~

Select a model size from the dropdown menu:

- tiny: Fastest, least accurate
- base: Fast, basic accuracy
- small: Good balance of speed and accuracy
- medium: High accuracy, slower
- large: Highest accuracy, slowest

4. Transcribe
~~~~~~~~~~~

Click the "▶ Transcribe" button to start processing. The progress bar will show the current status.

5. Translation (Optional)
~~~~~~~~~~~~~~~~~~~~~~

To translate the transcription:

1. Select the target language
2. Click "▶ Translate"

6. Save Results
~~~~~~~~~~~~~

Choose a format and click "Save":

- Text (.txt)
- SubRip (.srt)
- WebVTT (.vtt)
- JSON (.json)

Advanced Features
---------------

Batch Processing
~~~~~~~~~~~~~~

To process multiple files:

1. Click the "Batch" button
2. Select multiple audio files
3. Files will be processed in sequence

Advanced Settings
~~~~~~~~~~~~~~~

Configure advanced options:

- VRAM limit: Maximum GPU memory usage
- Beam size: Higher values = better accuracy but slower
- VAD filter: Remove non-speech segments
- Sample rate: Audio sampling frequency
- Audio channels: Mono/Stereo
- Temperature: Controls output randomness

System Monitoring
~~~~~~~~~~~~~~~

The status bar shows:

- CPU usage
- RAM usage
- GPU usage (if available)
- VRAM usage (if GPU available)

Keyboard Shortcuts
---------------

- Ctrl+O: Open file
- Ctrl+B: Open batch
- Ctrl+S: Save transcription
- Ctrl+T: Start transcription
- Ctrl+L: Start translation

Preferences
----------

Access preferences from View > Preferences:

- Font size (small/medium/large)
- Show/hide advanced settings
- Show/hide system stats
- Theme (light/dark)

Troubleshooting
-------------

Common Issues
~~~~~~~~~~~

1. **GPU Out of Memory**
   
   - Reduce VRAM limit in advanced settings
   - Use a smaller model size
   - Switch to CPU mode

2. **Slow Processing**
   
   - Use a smaller model size
   - Reduce beam size
   - Check system resource usage

3. **Poor Accuracy**
   
   - Use a larger model size
   - Increase beam size
   - Check audio quality
   - Ensure correct language selection

Getting Help
~~~~~~~~~~

If you encounter issues:

1. Check the documentation
2. Look for similar issues on GitHub
3. Open a new issue with:
   - Error message
   - System information
   - Steps to reproduce 