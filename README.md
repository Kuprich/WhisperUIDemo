## Whisper UI

The main goal of the project is to create a graphical user interface for the [Whisper](https://github.com/openai/whisper) speech recognition library
GUI created using the [Flet](https://flet.dev/) library



The project supports two recognition modes:
- single file process - recognition of only one file
- batch process - processing multiple files at once

You can select a mode by clicking on the popup menu button on the main tab

#### Single file mode
You need to select an audio file, select a recognition model and click the *Recognize* button. 
The recognition process is displayed in real time and you can copy part of the result
(screen)

#### Batch process
You need select an output folder, audio files (one or more), select recognition model. 
You can remove concrete selected  file from audio list or clear all files


![whisperUI](https://github.com/Kuprich/WhisperUIDemo/assets/23151696/c5cdc27b-791e-41bb-869d-f2dc32f40c36)




### Requirements
Whisper requires [FFMpeg](https://ffmpeg.org/) to be installed


### Remarks
- By default the model is downloaded to the following directory "~/.cache/whisper". 
- The output tab does not display information about the model download process.The beginning and end of the model download process is indicated as follows:
    ```
    Model download directory: ~./cache/whisper      #download model started
    Model {model_name} downloaded                   #download model finished
    ```
- In Linux, the FilePicker control depends on Zenity when running Flet as an app. This is not a requirement when running Flet in a browser.
To install Zenity on Ubuntu/Debian run the following commands:
    ```
    sudo apt-get install zenity
    ```


### Links
- [Whisper](https://github.com/openai/whisper) - is a general-purpose speech recognition model
- [Flet](https://flet.dev/) as the fastest way to build Flutter apps in Python