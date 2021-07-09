import aflr
import os
aflr.api_key = os.getenv("API-KEY")

# Let's create a script!
text = "<<sectionName::question>> Do you know how big the universe is? <<sectionName::answer>> Silence. Don't bore the people at Strive School."
script = aflr.Script().create(scriptText=text, scriptName="multiple_speakers")
print(script)

# Create text to speech
r = aflr.Speech().create(
    scriptId=script["scriptId"],
    voice="en-GB-RyanNeural",
    speed=90,
    silence_padding=0,
     sections={
        "question": {
            "voice": "Hawking",
            "speed": 90,
            "silence_padding": 1000
        },
        "answer": {
            "voice": "Matthew",
            "speed": 100,
            "effect": "dark_father"
        }

     }
)
print(r)

# Mastering creation
r = aflr.Mastering().create(scriptId=script["scriptId"], backgroundTrackId="full__deepsea.wav")
print(r)

# retrieve the mastered audio files
r = aflr.Mastering().retrieve(scriptId=script["scriptId"])
print(r)

# download all speech audio files
# check your folder :) you should have the following audio_files
file = aflr.Mastering().download(scriptId=script.get("scriptId"), destination=".")
print(file)
