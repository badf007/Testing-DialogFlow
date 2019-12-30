# Testing DialogFlow

Code example to test the capabilities of DialogFlow.
The code creates an .WAV audio file each time the audio is above noise base level, then another python process detects new .WAV files created inside the folder then sends it to a detection *AGENT* from DialogFlow that analyses the audio file and sends back possible text interpretations of the user sentence and if the audio match one of the pre-defined *Intents* created by the user the *Agent* send back a pre-defined response for that *Intent*.

## Requirements

+ SoX
+ IMA Credentials JSON file

## Code Modifications

First change the text constants value inside VoiceAnalysis.py:

```python
project_id = "YOUR_PROJECT_ID"  # found in the DialogFlow conosle settings
session_id = "YOUR_SESSION_ID"  # This ID can be a random number
language_code = "en"  # the language the AGENT is expected to interpret
```

## Executing the example code

1. Run the VoiceAnalysis.py with `python VoiceAnalysis.py`
2. Run infiniteRecord.py with `python infiniteRecord.py`
