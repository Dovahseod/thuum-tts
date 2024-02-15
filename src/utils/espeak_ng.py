import asyncio
from typing import Optional
import re


class ESpeakError(Exception):
    pass


class TTSParameterError(Exception):
    def __init__(self, parameter, value, limits) -> None:
        super().__init__(
            f"TTS Parameter {parameter} out of bounds: {value} given, expected within [{limits[0]}, {'inf' if limits[1] is None else limits[1]}]"
        )


class Speaker():
    def __init__(self, program: str = 'espeak-ng', voice: str = 'en', enable_mbrola: bool = False, **kwargs) -> None:
        self.verify_parameters(kwargs)

        self.amplitude = kwargs.get('amplitude', 100) # 0-200
        self.pitch = kwargs.get('pitch', 50) # 0-99
        self.wpm = kwargs.get('wpm', 175) # words per min, 20-500 recommended
        self.gap = kwargs.get('gap', 0) # additional word gap, positive int, 10ms intervals
        self.voice = voice
        self.program = program
        self.enable_mbrola = enable_mbrola

    def verify_parameters(self, parameters):
        limits = {
            'amplitude' : (0, 200),
            'pitch': (0, 99),
            'wpm': (20, 500), # Technically not limited; 20-500 recommended
            'gap': (0, None)
        }

        for key in parameters.keys():
            if key in limits.keys():
                if (parameters[key] < limits[key][0]
                    or (limits[key][1] is not None
                        and parameters[key] > limits[key][1])
                ):
                    raise TTSParameterError(key, parameters[key], limits[key])

    async def list_voices(self, lang: str = "") -> list[list[str]]:
        process = await asyncio.subprocess.create_subprocess_exec(
            self.program, f'--voices={lang}',
            stdout=asyncio.subprocess.PIPE,
            text=False, # text = True not supported by asyncio
            )
        results = await process.communicate()
        languages_str = results[0].decode() # stdout
        languages_info = languages_str.split('\n')[1:] # discard title row
        available_voices = []
        for language_info in languages_info:
            # discard empty rows
            if language_info:
                info_fields = language_info.split()
                info_fields = info_fields[0:2] \
                    + info_fields[2].split('/') \
                    + [info_fields[3]] \
                    + re.split(r'[\\\/]', info_fields[4])
                # Pty, Language, Age, Gender, Voice Name, File folder, File name
                
                if self.enable_mbrola:
                    available_voices.append(info_fields)
                elif not re.match(r"mb-\S+", info_fields[-1]):
                    available_voices.append(info_fields)
                else:
                    pass
            
        return available_voices

    async def read(self, words: str, voice: Optional[str] = None, wpm: Optional[int] = None,
                   gap: Optional[int] = None, pitch: Optional[int] = None,
                   amplitude: Optional[int] = None) -> bytes:
        """Reads the words with the given parameters or default parameters, and returns a `bytes` object of the TTS audio."""
        if voice is None:
            voice = self.voice
        if wpm is None:
            wpm = self.wpm
        if gap is None:
            gap = self.gap
        if pitch is None:
            pitch = self.pitch
        if amplitude is None:
            amplitude = self.amplitude

        self.verify_parameters({
            'wpm': wpm,
            'gap': gap,
            'pitch': pitch,
            'amplitude': amplitude,
        })

        process = await asyncio.subprocess.create_subprocess_exec(
            self.program, '-v', voice, '-s', str(wpm), '-g', str(gap),
            '-p', str(pitch), '-a', str(amplitude), '--stdout', f'"{words}"',
            stdout=asyncio.subprocess.PIPE, text=False
            )
        results = await process.communicate()
        if results[1]:
            raise ESpeakError(results[1].decode())
        return results[0]
