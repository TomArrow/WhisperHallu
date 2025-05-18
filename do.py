import sys
from transcribeHallu import loadModel
from transcribeHallu import transcribePrompt

##### The audio language may be different from the one for the output transcription.
path=sys.argv[1]
lngInput="en"

print("debugPath")
print(path)

##### Activate this for music file to get a minimal processing
isMusic=False

##### Need to be adapted for each language.
##### For prompt examples, see transcribeHallu.py getPrompt(lng:str)
lng="en"
prompt= "Whisper, Ok. "\
	+"A pertinent sentence for your purpose in your language. "\
	+"Ok, Whisper. Whisper, Ok. "\
	+"Ok, Whisper. Whisper, Ok. "\
	+"Please find here, an unlikely ordinary sentence. "\
	+"This is to avoid a repetition to be deleted. "\
	+"Ok, Whisper. "

##### Model size to use
modelSize="tiny"
loadModel("0",modelSize=modelSize)


result = transcribePrompt(path=path, lng=lng, prompt=prompt, lngInput=lngInput,isMusic=isMusic)

