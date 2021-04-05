"""Getting Started Example for Python 2.7+/3.3+"""
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import wave
import sys


def generateAudioFile(text, filename):
    # Create a client using the credentials and region defined in the [adminuser]
    # section of the AWS credentials file (~/.aws/credentials).
    # session = Session(profile_name="default")
    polly = boto3.client("polly")

    try:
        # Request speech synthesis
        response = polly.synthesize_speech(Engine='neural', Text=text, OutputFormat="pcm",
                                            VoiceId="Amy")
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        return None

    # Access the audio stream from the response
    if "AudioStream" in response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
        data = None

        with closing(response["AudioStream"]) as stream:
            data = stream.read()

        wav_path = "audio/" + filename + ".wav"
        wav_file = wave.open(wav_path, 'w')
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(16000)
        # write the frames
        wav_file.writeframes(data)
        wav_file.close()

    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        return None

    return wav_path

def main():

    adviceFile = open('advice.txt', 'r')
    adviceNum = 1

    for advice in adviceFile:
        generateAudioFile(advice, str(adviceNum))
        adviceNum += 1

    # print(generateAudioFile("Hello, my name is Misty. I'll be here to help you during your puzzles.", "introduction"))


if __name__ == "__main__":
   main()