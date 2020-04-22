# Spyder ScreenCast plugin



# Description

For documentation-, training-, and bug-reporting purposes, we need to have a 'ScreenCast' plug-in in Spyder.

The idea is that at the bottom right of the Spyder window there is a little camera icon (mdi-video).
As soon as we left-click on this icon, the spyder screen (and only that) is grabbed at some frame-rate as
well as the audio until we left-click the icon again, then the captured video and audio is assembled in an .mp4 file.

The grabbing of audio and video should be done with Qt, whereas the assembling is handled by OpenCV

There is a very minimalistic 'settings' dialog (see: ATE.org/src/SpyderMockUp/ScreenCasting/ScreenCastSettings.ui)
Basically the only thing to 'set' is the video resolution ...

    - 240p (462x240)
    - 360p (640x360)
    - 480p (854x480)
    - 720p (1280x720)  ---> will be our default to start off with
    - 1080p (1920x1080 aka 1K)
    - 1440p (2560x1440 aka 2K)
    - 2160p (3840x2160 aka 4K)

if 'Cancel' is pressed, nothing is done.
if 'Apply' is pressed, the Spyder(MockUp) main window is resized to have the same aspect ratio as
the selected video resolution (maybe scalled ½x, 1x, 2x), so that if subsequently we start the recording,
we will *ONLY* capture the video *INSIDE* the main window, and we thus don't need to transform the image
(which would be ugly in any case!)

Note that if, when the screencast is started, and the aspect ratio of the main Spyder(MockUp) window
does not comply to the active video format, that then the main window will be resized first (same 
procedure as with the 'Apply' button above)

The resulting .mp4 is *ALWAYS* put on the desktop (of the user that is logged in).
The name of the .mp4 file conforms to 'Spyder_ScreenCast_#' where '#' is a number that starts with 1.
If 'Spyder_ScreenCast_4.mp4' is already existing, then the next name is 'Spyder_ScreenCast_5.mp4'
even if 'Spyder_ScreenCast_3.mp4' is not there! (so basically make a list of the numbers, and the new
number is max(list)+1 :-)

# Usage

The idea is that the screenCast plugin always works in Spyder regardless the OS:
    - Linux --> ref = Ubuntu desktop LTS 18.04 (soon 20.04)
    - OSX --> ref = Mojave
    - Windows --> ref = Win10

We thus can not use half-baked 'windows-only' packages in any case !
Try to stay with the 'Big standard packages' :-)

# Proposed Packages to use

    1. Qt5 (for sure always installed) --> https://doc.qt.io/qt-5/multimediaoverview.html

        - grabbing screen area's --> https://doc.qt.io/qt-5/videooverview.html
        - grabbing audio --> https://doc.qt.io/qt-5/audiooverview.html
    
    2. numpy (should always be installed :-) 
        - RGB transformation

    3. OpenCV (is heavy, normally not installed, so we need to detect if it is installed ... see SpyderMockUp.py line 65 onward)
        - assembling the 'MP4'

# Packages maybe to use ...

    - pillow --> Qt should covers this
    - sounddevice --> Qt5 should covers this

# Settings

quote : "The best video format for YouTube is MP4 with H. 264 video codec 
        and AAC audio codec, as it allows to get high-quality video while 
        file size remains small."

As we are capturing a screen, we don't have to have high frame rates, 
I propose to set the frame rate standard to 12 fps !

As for audio, I propose to set this fixed to 44.1kHz & 16Bit. This shoud
be plenty good to start with (maybe later even tune it a bit down ...)

# References
 Icons : https://cdn.materialdesignicons.com/4.9.95/
     Video : mdi-video
 
 Resolutions : https://learn.g2.com/youtube-video-size
 
 YouTube : https://elfsight.com/blog/2017/06/requirements-uploading-video-youtube/
 
 Audio sample rates & bit depth : https://resoundsound.com/sample-rate-bit-depth/
 
 Examples :
     - https://www.youtube.com/watch?v=1eHQIu4r0Bc
     - https://www.youtube.com/watch?v=wjfWa590EFQ
     - https://www.youtube.com/watch?v=GWdrL8dt1xQ&t=133s
     - https://www.youtube.com/watch?v=KTlgVCrO7IQ
     - https://www.youtube.com/watch?v=CK-8XB36q44
     
     
