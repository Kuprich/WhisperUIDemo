## Whisper UI

The main goal of the project is to create a graphical user interface for the [Whisper](https://github.com/openai/whisper) speech recognition library. 
GUI created using the [Flet](https://flet.dev/) library



The project supports two recognition modes:
- single file process - recognition of only one file
- batch process - processing multiple files at once

You can select a mode by clicking on the popup menu button on the main tab:
![change_mode](https://github.com/Kuprich/WhisperUIDemo/assets/23151696/2746f95e-cc79-41a8-8936-26176d3a3a54)

#### Single file mode
You need to select an audio file, select a recognition model and click the *Recognize* button. 
The recognition process is displayed in real time and you can copy part of the result. look at the example below:
![single_tab](https://github.com/Kuprich/WhisperUIDemo/assets/23151696/baf0e904-4e76-4720-986c-d453f02183d1)

#### Batch process
You need select an output folder, audio files (one or more), select recognition model. 
You can remove concrete selected  file from audio list or clear all files
![select_files](https://github.com/Kuprich/WhisperUIDemo/assets/23151696/74eb9648-3eb0-4bd6-ae04-30e8ee19ae41)

Take a look at the process of recognizing multiple files:

![recognition_batch](https://github.com/Kuprich/WhisperUIDemo/assets/23151696/02d3395c-0a40-4426-8a93-38bd27449eb8)



### Requirements
Whisper requires [FFMpeg](https://ffmpeg.org/) to be installed


### Remarks
- By default the model is downloaded to the following directory "~/.cache/whisper". You can't change this value via ui
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
- [Flet](https://flet.dev/) - the fastest way to build Flutter apps in Python