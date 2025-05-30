# WhisperHallu
Experimental code: sound file preprocessing to optimize Whisper transcriptions without hallucinated texts

See this discussion: https://github.com/openai/whisper/discussions/679

# Main algo
- remove noise by voice extraction using  [Facebook Demucs](https://github.com/facebookresearch/demucs) or [Deezer Spleeter](https://github.com/deezer/spleeter).
- remove silences, and normalize loudness with ffmpeg.
- remove noise parts using [Silero VAD](https://github.com/snakers4/silero-vad).
- add voice markers.
- apply speech compressor (requires `ffmpeg` 4.4, while Google Colab is 4.2, it has to be upgraded, see below).
- try to transcribe. If markers are present in output, transcription is OK.
- if not, try to invert markers. If markers are present in output, transcription is OK.
- if not, try without markers.

# Processing options and parameters
- use Whisper V1, V2 or V3 (V2 by default, because V3 seems bad with music).
- beam_size (2 by default), patience, temperature.
- process only a subpart of the input file (needs a post-processing of timestamp values).
- various time stretching methods tested (see in-code comments. Needs a post-processing of timestamp values. It was an interesting suggested idea, but no real gain obtained on my side).
- vocals remix (with or without speech normalization).
- multiple final transcriptions (get multiple results, knowing Whisper is not stable from one run to an other, without doing pre-processing several times) 

# Complement

May be used to produce "accurate transcriptions" for WhisperTimeSync:<br/>
https://github.com/EtienneAb3d/WhisperTimeSync

May be tested using NeuroSpell Dictaphone:<br/>
https://neurospell.com/

WhisperHallu and WhisperTimeSync are used to extract vocals and lyrics in karaok-AI:<br/>
https://github.com/EtienneAb3d/karaok-AI

ChatMate is a complete versatile ChatGPT automation tool, including explanations to produce a SRT file translator to Chinese (as an example):<br/>
https://github.com/EtienneAb3d/ChatMate

# Google Colab

Standard Whisper:<br/>
https://colab.research.google.com/drive/1-GpXaNaGFXKX9VXl60JGVVrGO41t09KA?usp=sharing

Faster Whisper:<br/>
https://colab.research.google.com/drive/1RkvOtUTbUD5NVsRI4aKEqJO8BRo8BFIY?usp=sharing

# Install

**Check ffmpeg version >=4.4**
```sh
ffmpeg -version

Output should be:
=================
ffmpeg version 4.4.3-0ubuntu1~20.04.sav2 Copyright (c) 2000-2022 the FFmpeg developers
[...]

Install latest:
===============
sudo add-apt-repository -y ppa:savoury1/ffmpeg4
sudo apt-get -qq install -y ffmpeg

```

**Demucs (if used)**

```sh
pip install -U demucs
```

**Spleeter (if used)**

```sh
pip install spleeter
```

**Standard Whisper (if used)**

```sh
sudo apt update && sudo apt install ffmpeg

sudo apt install python3
sudo apt install python3-pip
sudo apt install virtualenv

virtualenv -p python3 ../venvWhisper
. ../venvWhisper/bin/activate

pip install -U openai-whisper

pip3 install torchaudio
```

**Faster Whisper (if used in place of Whisper)**

```sh
sudo apt update && sudo apt install ffmpeg

sudo apt install python3
sudo apt install python3-pip
sudo apt install virtualenv

virtualenv -p python3 ../venvFasterWhisper
. ../venvFasterWhisper/bin/activate

git clone https://github.com/guillaumekln/faster-whisper.git
cd faster-whisper/

pip install -e .[conversion]
pip install -e .

cd ..

ct2-transformers-converter --model openai/whisper-medium --output_dir whisper-medium-ct2 --quantization float16
ct2-transformers-converter --model openai/whisper-large --output_dir whisper-large-ct2 --quantization float16
ct2-transformers-converter --model deepdml/whisper-large-v3-turbo --output_dir whisper-turbo-ct2 --copy_files tokenizer.json preprocessor_config.json --quantization float16

pip3 install torchaudio
```

**SM4T (if used in place of Whisper)**

```sh
sudo apt update && sudo apt install ffmpeg

sudo apt install python3
sudo apt install python3-pip
sudo apt install virtualenv

virtualenv -p python3 ../venvSM4T
. ../venvSM4T/bin/activate

git clone https://github.com/facebookresearch/seamless_communication.git
cd seamless_communication/

pip install --upgrade pip
pip install .

m4t_predict "On ne fait pas d'omelette sans casser des oeufs." t2tt eng --src_lang fra

pip3 install torchaudio
```

# Code

```python
from transcribeHallu import loadModel
from transcribeHallu import transcribePrompt

##### The audio language may be different from the one for the output transcription.
path="/path/to/your/en/sound/file"
lngInput="en"

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
modelSize="medium"
loadModel("0",modelSize=modelSize)

result = transcribePrompt(path=path, lng=lng, prompt=prompt, lngInput=lngInput,isMusic=isMusic)
```

<hr>
This tool is a demonstration of our know-how.<br/>
If you are interested in a commercial/industrial AI linguistic project, contact us:<br/>
https://cubaix.com
