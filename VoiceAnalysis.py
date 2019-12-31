#!/usr/bin/env python

import sox
import os
import time

project_id = "YOUR_PROJECT_ID"  # found in the DialogFlow conosle settings
session_id = "YOUR_SESSION_ID"  # This ID can be a random number
language_code = "en"  # the language the AGENT is expected to interpret


# This function detects if some new WAV file is added to the folder, if that is true then proceeds to send that
# audio file to an Dialogflow AGENT to identify the possible INTENT of the user.
def detectAndCall():
    path_to_watch = "."
    before = dict([(f, None) for f in os.listdir(path_to_watch)])
    # print("Original: ", ", ".join(before))
    print("Waiting for changes in the directory.")
    print("===============================================")
    while 1:
        time.sleep(10)
        after = dict([(f, None) for f in os.listdir(path_to_watch)])
        added = [f for f in after if not f in before]
        before = after

        for file in added:
            ext = file.rpartition('.')[-1]
            identificador = int(file.rpartition('.')[0].split('_')[1])
            if identificador is not 1:
                FinalID = str(identificador-1)
            else:
                FinalID = "1"
            if(ext == "wav"):
                finalPath = os.getcwd() + '\\record_00' + FinalID + ".wav"
                print(finalPath)
                detect_intent_stream(finalPath)


# Takes audio file pointed by the file path and reads it in blocks of 4096 bits piece by piece sending it to the
# DialogFlow agent and getting responses in the process.
def detect_intent_stream(audio_file_path):
    """Returns the result of detect intent with streaming audio as input.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient()

    # Note: hard coding audio_encoding and sample_rate_hertz for simplicity.
    audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_UNSPECIFIED
    sample_rate_hertz = 48000

    session_path = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session_path))

    def request_generator(audio_config, audio_file_path):
        query_input = dialogflow.types.QueryInput(audio_config=audio_config)

        # The first request contains the configuration.
        yield dialogflow.types.StreamingDetectIntentRequest(
            session=session_path, query_input=query_input)

        # Here we are reading small chunks of audio data from a local
        # audio file.  In practice these chunks should come from
        # an audio input device.
        # add delay to wait until file is fully saved in the folder
        print("Wait a second....")
        time.sleep(2)
        with open(audio_file_path, 'rb') as audio_file:
            while True:
                chunk = audio_file.read(4096)
                if not chunk:
                    print("Maybe File not found in directory: " + audio_file_path)
                    break
                # The later requests contains audio data.
                yield dialogflow.types.StreamingDetectIntentRequest(
                    input_audio=chunk)

    audio_config = dialogflow.types.InputAudioConfig(
        audio_encoding=audio_encoding, language_code=language_code,
        sample_rate_hertz=sample_rate_hertz)

    requests = request_generator(audio_config, audio_file_path)
    responses = session_client.streaming_detect_intent(requests)

    print('=' * 20)
    for response in responses:
        print('Intermediate transcript: "{}".'.format(
            response.recognition_result.transcript))

    # Note: The result from the last response is the final transcript along
    # with the detected content.
    query_result = response.query_result

    print('=' * 20)
    print('Query text: {}'.format(query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        query_result.intent.display_name,
        query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        query_result.fulfillment_text))


# runing main function
if __name__ == "__main__":
    detectAndCall()
