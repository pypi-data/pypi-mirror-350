"""
Text-to-Speech (TTS) implementations for pdf2podcast.
"""

import os
import time
from typing import Dict, Any, Optional, List, Callable, Tuple
from contextlib import closing
import tempfile
import logging
from functools import wraps

# AWS Polly
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Azure
import azure.cognitiveservices.speech as speechsdk

# Google TTS
from gtts import gTTS
from gtts.tts import gTTSError

# Audio processing
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

from kokoro import KPipeline
import soundfile as sf

# import torch # Not directly used in this refactoring, can be removed if not needed by Kokoro or other parts

# Setup logging
logger = logging.getLogger(__name__)


def retry_on_exception(
    retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,),
) -> Callable:
    """
    Retry decorator with exponential backoff.

    Args:
        retries (int): Maximum number of retries
        delay (float): Initial delay between retries in seconds
        backoff (float): Backoff multiplier
        exceptions (tuple): Exceptions to catch
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retry_delay = delay
            last_exception = None

            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if i < retries - 1:
                        logger.warning(
                            f"Attempt {i + 1}/{retries} failed: {str(e)}. "
                            f"Retrying in {retry_delay:.1f}s..."
                        )
                        time.sleep(retry_delay)
                        retry_delay *= backoff
                    else:
                        logger.error(f"All {retries} attempts failed.")

            raise last_exception

        return wrapper

    return decorator


from .base import BaseTTS


def validate_mp3_file(file_path: str) -> bool:  # Renamed from validate_audio_file
    """
    Validate that an audio file is properly formatted MP3.

    Args:
        file_path (str): Path to the audio file

    Returns:
        bool: True if valid, False otherwise
    """
    try:
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            logger.warning(f"MP3 file does not exist or is empty: {file_path}")
            return False
        audio = AudioSegment.from_mp3(file_path)
        return len(audio) > 0
    except (CouldntDecodeError, OSError):
        logger.warning(f"Could not decode MP3 file or OS error: {file_path}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error validating MP3 audio {file_path}: {str(e)}")
        return False


def _validate_wav_file(file_path: str) -> bool:
    """
    Validate that an audio file is a properly formatted WAV.
    Relies on pydub's ability to load it and checks for non-zero length.
    """
    try:
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            logger.warning(f"WAV file does not exist or is empty: {file_path}")
            return False
        # Attempt to load the WAV file to check its integrity and get duration
        audio = AudioSegment.from_wav(file_path)
        return len(audio) > 0  # Ensure it has a positive duration
    except CouldntDecodeError:  # pydub raises this for bad WAVs
        logger.error(f"Could not decode WAV file: {file_path}")
        return False
    except FileNotFoundError:  # Should be caught by os.path.exists, but good to have
        logger.error(f"WAV file not found for validation: {file_path}")
        return False
    except Exception as e:  # Catch any other pydub or OS errors
        logger.error(f"Unexpected error validating WAV audio {file_path}: {str(e)}")
        return False


def split_text(text: str, max_length: int = 3000) -> List[str]:
    """
    Split text into chunks that are safe for TTS processing.

    Args:
        text (str): Text to split
        max_length (int): Maximum length per chunk

    Returns:
        List[str]: List of text chunks
    """
    chunks = []
    sentences = text.split(". ")
    current_chunk = ""

    for sentence in sentences:
        if not sentence.strip():
            continue

        # Add period back if it was removed by split
        sentence = sentence.strip() + ". "

        if len(current_chunk) + len(sentence) > max_length:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk += sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def _merge_audio_chunks_and_export_wav(  # Renamed from merge_audio_files
    chunk_files: List[str], output_path: str
) -> bool:
    """
    Merge multiple WAV audio chunks into a single WAV file.
    Handles cleanup of temporary chunk files.
    """
    combined = AudioSegment.empty()
    valid_input_files_for_cleanup = []

    logger.info(
        f"Starting merge of {len(chunk_files)} audio chunks into WAV: {output_path}"
    )

    for file_path in chunk_files:
        try:
            # Expecting WAV files primarily.
            # GoogleTTS might initially produce MP3, which should be converted to WAV before this stage.
            if file_path.lower().endswith(".wav"):
                if not _validate_wav_file(file_path):
                    logger.error(f"Skipping invalid or empty WAV chunk: {file_path}")
                    continue
                audio_chunk = AudioSegment.from_wav(file_path)
            elif file_path.lower().endswith(
                ".mp3"
            ):  # Fallback for non-converted GoogleTTS chunks
                logger.warning(
                    f"Processing MP3 chunk {file_path} for WAV output pipeline. Consider converting to WAV earlier."
                )
                if not validate_mp3_file(file_path):
                    logger.error(f"Skipping invalid or empty MP3 chunk: {file_path}")
                    continue
                audio_chunk = AudioSegment.from_mp3(
                    file_path
                )  # This implies a decode step
            else:
                logger.warning(f"Unsupported chunk file format: {file_path}. Skipping.")
                continue

            combined += audio_chunk
            valid_input_files_for_cleanup.append(file_path)
            logger.debug(
                f"Added chunk {file_path} to combined audio. Current combined length: {len(combined)} ms."
            )

        except Exception as e:
            logger.error(f"Error processing chunk {file_path} for WAV merge: {e}")
            continue

    if not combined or len(combined) == 0:
        logger.error(
            "No valid audio data to merge into WAV after processing all chunks."
        )
        for (
            f_path
        ) in (
            valid_input_files_for_cleanup
        ):  # Clean up successfully processed chunks even if merge fails
            try:
                if os.path.exists(f_path):
                    os.remove(f_path)
            except OSError:
                pass
        return False

    try:
        # Export the combined audio segment to a WAV file
        combined.export(output_path, format="wav")
        logger.info(f"Successfully exported merged WAV to {output_path}")

        # Clean up all processed temporary chunk files after successful export
        for f_path in valid_input_files_for_cleanup:
            try:
                if os.path.exists(f_path):
                    os.remove(f_path)
            except OSError as e_clean:
                logger.warning(
                    f"Failed to remove temporary chunk file {f_path}: {e_clean}"
                )
        return True
    except Exception as e_export:
        logger.error(f"Error exporting final WAV to {output_path}: {e_export}")
        # Consider not cleaning up chunks if export fails, for debugging.
        return False


class AWSPollyTTS(BaseTTS):
    """
    AWS Polly-based Text-to-Speech implementation.
    Outputs WAV chunks.
    """

    def __init__(
        self,
        voice_id: str = "Joanna",
        region_name: str = "eu-central-1",
        engine: str = "neural",
        temp_dir: str = "temp",
    ):
        self.polly = boto3.client("polly", region_name=region_name)
        self.voice_id = voice_id
        self.engine = engine
        self.temp_dir = temp_dir
        os.makedirs(temp_dir, exist_ok=True)

    @retry_on_exception(retries=3, delay=1.0, exceptions=(BotoCoreError, ClientError))
    def _generate_chunk(
        self, text: str, output_path: str, voice_id: Optional[str] = None
    ) -> bool:
        voice_id_to_use = voice_id or self.voice_id
        try:
            # Request PCM (WAV) output from Polly
            response = self.polly.synthesize_speech(
                Text=text,
                OutputFormat="pcm",
                VoiceId=voice_id_to_use,
                Engine=self.engine,
                SampleRate="24000",  # Example, adjust as needed
            )

            if "AudioStream" not in response:
                logger.error("No AudioStream in Polly PCM response")
                return False

            with closing(response["AudioStream"]) as stream:
                with open(output_path, "wb") as file:  # output_path should be .wav
                    file.write(stream.read())

            # Validate generated WAV file (using pydub to convert raw PCM to proper WAV if necessary, or ensure Polly sends WAV header)
            # For now, assuming Polly's PCM is directly usable or easily convertible.
            # If Polly's "pcm" is raw PCM, we need to wrap it into a WAV container.
            # A simpler approach for now: save as .wav and let _validate_wav_file (which uses pydub) check it.
            # If Polly's PCM is raw, pydub might need more info to load it.
            # Let's assume for now that saving it as .wav and validating works.
            # If not, we'd need to use soundfile or wave module to write a proper WAV header.

            # To ensure it's a proper WAV for pydub, let's re-save it with pydub if it's raw PCM
            try:
                audio = AudioSegment.from_file(
                    output_path, format="s16le", frame_rate=24000, channels=1
                )  # Example for raw PCM
                audio.export(output_path, format="wav")
            except Exception as e_raw:
                logger.warning(
                    f"Could not process raw PCM from Polly for {output_path}, assuming it's already WAV-compatible or relying on later validation. Error: {e_raw}"
                )
                # If this fails, _validate_wav_file will catch it.

            if not _validate_wav_file(output_path):
                logger.error(f"Generated WAV chunk {output_path} is invalid")
                return False
            return True
        except (BotoCoreError, ClientError) as e:
            logger.error(f"AWS Polly error generating WAV: {str(e)}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in WAV audio generation (AWS Polly): {str(e)}"
            )
            return False

    def generate_audio(
        self,
        text_segments: List[str],
        output_path: str,  # Expected to be a .wav path
        voice_id: Optional[str] = None,
        max_chunk_length: int = 3000,  # Polly's limit for PCM might differ
        **kwargs: Dict[str, Any],
    ) -> Dict[str, Any]:
        try:
            text = " ".join(filter(None, text_segments))
            if not text.strip():
                return {
                    "success": False,
                    "error": "No text provided",
                    "path": None,
                    "size": 0,
                }

            if not output_path.lower().endswith(".wav"):
                logger.warning(
                    f"Output path {output_path} for AWSPollyTTS is not .wav. Forcing .wav output."
                )
                # output_path = os.path.splitext(output_path)[0] + ".wav" # Or raise error

            chunks = split_text(text, max_chunk_length)
            chunk_wav_files = []

            for i, chunk_text in enumerate(chunks):
                # Ensure chunk paths are .wav
                chunk_wav_path = os.path.join(self.temp_dir, f"aws_chunk_{i}.wav")
                if self._generate_chunk(chunk_text, chunk_wav_path, voice_id):
                    chunk_wav_files.append(chunk_wav_path)

            if not chunk_wav_files:
                raise Exception("No WAV audio chunks were generated by AWSPollyTTS")

            if len(chunk_wav_files) == 1:
                os.rename(chunk_wav_files[0], output_path)
            else:
                if not _merge_audio_chunks_and_export_wav(chunk_wav_files, output_path):
                    raise Exception(
                        f"AWSPollyTTS: Failed to merge WAV chunks into {output_path}"
                    )

            if not _validate_wav_file(output_path):  # Validate final merged/renamed WAV
                return {
                    "success": False,
                    "error": "Final WAV file is invalid",
                    "path": output_path,
                    "size": 0,
                }

            size = os.path.getsize(output_path)
            return {"success": True, "path": output_path, "size": size}
        except Exception as e:
            logger.error(f"AWSPollyTTS: Overall audio generation failed: {str(e)}")
            return {"success": False, "error": str(e), "path": None, "size": 0}


class GoogleTTS(BaseTTS):
    """
    Google Text-to-Speech implementation using gTTS.
    Produces MP3 chunks, then converts them to WAV for the pipeline.
    Final output of the pipeline is WAV.
    """

    def __init__(
        self,
        language: str = "en",
        tld: str = "com",
        slow: bool = False,
        temp_dir: str = "temp",
    ):
        self.language = language
        self.tld = tld
        self.slow = slow
        self.temp_dir = temp_dir
        os.makedirs(temp_dir, exist_ok=True)

    @retry_on_exception(retries=3, delay=2.0, exceptions=(gTTSError,))
    def _generate_chunk_as_wav(
        self, text: str, output_wav_path: str, language: Optional[str] = None
    ) -> bool:
        """Generates MP3 via gTTS, then converts to WAV."""
        temp_mp3_path = os.path.splitext(output_wav_path)[0] + "_temp.mp3"
        try:
            lang_to_use = language or self.language
            tts = gTTS(text=text, lang=lang_to_use, slow=self.slow, tld=self.tld)
            tts.save(temp_mp3_path)

            if not validate_mp3_file(temp_mp3_path):
                logger.error(f"gTTS generated invalid MP3: {temp_mp3_path}")
                return False

            # Convert MP3 to WAV
            sound = AudioSegment.from_mp3(temp_mp3_path)
            sound.export(output_wav_path, format="wav")

            if not _validate_wav_file(output_wav_path):
                logger.error(
                    f"Failed to convert gTTS MP3 to valid WAV: {output_wav_path}"
                )
                return False
            return True
        except gTTSError as e_gtts:
            logger.error(f"Google TTS error: {str(e_gtts)}")
            raise
        except Exception as e_conv:
            logger.error(
                f"Error converting gTTS MP3 to WAV or validating: {str(e_conv)}"
            )
            return False
        finally:
            if os.path.exists(temp_mp3_path):
                try:
                    os.remove(temp_mp3_path)
                except OSError:
                    pass

    def generate_audio(
        self,
        text_segments: List[str],
        output_path: str,  # Expected to be a .wav path
        language: Optional[str] = None,
        max_chunk_length: int = 4500,  # gTTS limit is around 5000, play safe
        **kwargs: Dict[str, Any],
    ) -> Dict[str, Any]:
        try:
            text = " ".join(filter(None, text_segments))
            if not text.strip():
                return {
                    "success": False,
                    "error": "No text provided",
                    "path": None,
                    "size": 0,
                }

            if not output_path.lower().endswith(".wav"):
                logger.warning(
                    f"Output path {output_path} for GoogleTTS is not .wav. Forcing .wav output."
                )
                # output_path = os.path.splitext(output_path)[0] + ".wav"

            chunks = split_text(text, max_chunk_length)
            chunk_wav_files = []

            for i, chunk_text in enumerate(chunks):
                chunk_wav_path = os.path.join(self.temp_dir, f"gtts_chunk_{i}.wav")
                if self._generate_chunk_as_wav(chunk_text, chunk_wav_path, language):
                    chunk_wav_files.append(chunk_wav_path)

            if not chunk_wav_files:
                raise Exception(
                    "No WAV audio chunks were generated by GoogleTTS (after MP3 to WAV conversion)"
                )

            if len(chunk_wav_files) == 1:
                os.rename(chunk_wav_files[0], output_path)
            else:
                if not _merge_audio_chunks_and_export_wav(chunk_wav_files, output_path):
                    raise Exception(
                        f"GoogleTTS: Failed to merge WAV chunks into {output_path}"
                    )

            if not _validate_wav_file(output_path):
                return {
                    "success": False,
                    "error": "Final WAV file is invalid",
                    "path": output_path,
                    "size": 0,
                }

            size = os.path.getsize(output_path)
            return {"success": True, "path": output_path, "size": size}
        except Exception as e:
            logger.error(f"GoogleTTS: Overall audio generation failed: {str(e)}")
            return {"success": False, "error": str(e), "path": None, "size": 0}


class AzureTTS(BaseTTS):
    """
    Azure Text-to-Speech implementation.
    Outputs WAV chunks.
    """

    def __init__(
        self,
        subscription_key: str,
        region_name: str,
        voice_id: str = "en-US-AvaMultilingualNeural",  # Example, ensure this voice is available
        temp_dir: str = "temp",
    ):
        self.speech_config = speechsdk.SpeechConfig(
            subscription=subscription_key, region=region_name
        )
        # Set voice
        self.speech_config.speech_synthesis_voice_name = voice_id
        # Set output format to a WAV format, e.g., Riff24Khz16BitMonoPcm
        # Check Azure documentation for available WAV formats.
        # Using a common one:
        self.speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm
        )

        # Note: AudioOutputConfig(use_default_speaker=True) might not be what we want if saving to file.
        # To save to file directly from SDK, use AudioOutputConfig(filename="path.wav")
        # However, we want to get audio_data and write it ourselves to manage chunks.
        # So, we don't pass audio_config to SpeechSynthesizer to get data in memory.
        self.speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config, audio_config=None
        )
        self.temp_dir = temp_dir
        os.makedirs(temp_dir, exist_ok=True)

    @retry_on_exception(retries=3, delay=1.0, exceptions=(Exception,))
    def _generate_chunk(
        self,
        text: str,
        output_path: str,
        voice_id: Optional[str] = None,  # output_path should be .wav
    ) -> bool:
        try:
            if (
                voice_id
            ):  # Allow overriding voice per chunk if needed, though usually set in __init__
                self.speech_synthesizer.speech_config.speech_synthesis_voice_name = (
                    voice_id
                )

            result = self.speech_synthesizer.speak_text_async(text).get()

            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                with open(output_path, "wb") as file:
                    file.write(result.audio_data)  # This is the WAV data

                if not _validate_wav_file(output_path):
                    logger.error(f"Generated Azure WAV chunk {output_path} is invalid")
                    return False
                return True
            else:
                cancellation_details = result.cancellation_details
                logger.error(f"Azure speech synthesis failed: {result.reason}")
                if cancellation_details:
                    logger.error(f"Error details: {cancellation_details.error_details}")
                    logger.error(f"Reason details: {cancellation_details.reason}")
                return False
        except Exception as e:
            logger.error(f"Azure TTS error generating WAV: {str(e)}")
            raise

    def generate_audio(
        self,
        text_segments: List[str],
        output_path: str,  # Expected to be a .wav path
        voice_id: Optional[str] = None,
        max_chunk_length: int = 3000,  # Check Azure limits for SSML/text length
        **kwargs: Dict[str, Any],
    ) -> Dict[str, Any]:
        try:
            text = " ".join(filter(None, text_segments))
            if not text.strip():
                return {
                    "success": False,
                    "error": "No text provided",
                    "path": None,
                    "size": 0,
                }

            if not output_path.lower().endswith(".wav"):
                logger.warning(
                    f"Output path {output_path} for AzureTTS is not .wav. Forcing .wav output."
                )

            chunks = split_text(text, max_chunk_length)
            chunk_wav_files = []

            for i, chunk_text in enumerate(chunks):
                chunk_wav_path = os.path.join(self.temp_dir, f"azure_chunk_{i}.wav")
                if self._generate_chunk(chunk_text, chunk_wav_path, voice_id):
                    chunk_wav_files.append(chunk_wav_path)

            if not chunk_wav_files:
                raise Exception("No WAV audio chunks were generated by AzureTTS")

            if len(chunk_wav_files) == 1:
                os.rename(chunk_wav_files[0], output_path)
            else:
                if not _merge_audio_chunks_and_export_wav(chunk_wav_files, output_path):
                    raise Exception(
                        f"AzureTTS: Failed to merge WAV chunks into {output_path}"
                    )

            if not _validate_wav_file(output_path):
                return {
                    "success": False,
                    "error": "Final WAV file is invalid",
                    "path": output_path,
                    "size": 0,
                }

            size = os.path.getsize(output_path)
            return {"success": True, "path": output_path, "size": size}
        except Exception as e:
            logger.error(f"AzureTTS: Overall audio generation failed: {str(e)}")
            return {"success": False, "error": str(e), "path": None, "size": 0}


class KokoroTTS(BaseTTS):
    """
    Kokoro TTS implementation with timing information.
    """

    def _preprocess_text(self, text: str) -> str:
        """Basic text preprocessing."""
        # Basic cleanup
        processed_text = " ".join(text.split())
        # Basic punctuation handling and remove special formatting
        processed_text = (
            processed_text.replace(" ,", ",")
            .replace(" .", ".")
            .replace("*", "")
            .replace("_", "")
            .replace("[SOUND]", "<SOUND>")  # Convert any tags to English format with <>
            .replace("[PAUSE]", "<PAUSE>")
            .replace("[MUSIC]", "<MUSIC>")
            .replace("[EFFECT]", "<EFFECT>")
        )
        processed_text = (
            processed_text.replace(".", ". ").replace("!", "! ").replace("?", "? ")
        )
        return processed_text

    def __init__(
        self,
        voice_id: str = "af_heart",
        temp_dir: str = "temp",
        language: Optional[str] = None,  # Add but ignore language parameter
        **kwargs,  # Accept additional params but ignore them
    ):
        self.voice_id = voice_id
        # Map languages to Kokoro's lang_codes
        lang_map = {
            "it": "i",  # Italian
            "en": "a",  # American English (or "b" for British English)
            "fr": "f",  # French
            "es": "e",  # Spanish
            "hi": "h",  # Hindi
            "ja": "j",  # Japanese
            "zh": "z",  # Mandarin Chinese
            "pt": "p",  # Brazilian Portuguese
        }
        # Get the language code, default to "en" if not supported
        lang_code = (
            lang_map.get(language, "a") if language else "a"
        )  # Default to American English
        # Store language for text preprocessing
        self.language = language

        # Initialize pipeline with basic language support
        self.pipeline = KPipeline(repo_id="hexgrad/Kokoro-82M", lang_code=lang_code)
        self.temp_dir = temp_dir
        os.makedirs(temp_dir, exist_ok=True)

    def _generate_chapter_audio(
        self, text: str, chapter_index: int, current_time: float = 0.0
    ) -> Tuple[Optional[str], Dict[str, Any]]:
        """Generate audio for a chapter and collect timing information."""

        chapter_wav_path = os.path.join(self.temp_dir, f"chapter_{chapter_index}.wav")
        timing_data = {"start_time": current_time, "word_timings": [], "duration": 0.0}

        try:
            # Apply language-specific text preprocessing
            processed_text = self._preprocess_text(text)

            # Use pipeline with preprocessed text
            generator = self.pipeline(processed_text, voice=self.voice_id)
            audio_segments = []
            current_position = 0.0  # Track timing manually

            for result in generator:
                # Process timing information only for English
                if (
                    self.language == "en"
                    and result.tokens is not None
                    and len(result.tokens) > 0
                ):
                    for token in result.tokens:
                        if token.start_ts is not None and token.end_ts is not None:
                            timing_data["word_timings"].append(
                                {
                                    "word": token.text,
                                    "start": token.start_ts + current_time,
                                    "end": token.end_ts + current_time,
                                }
                            )
                            timing_data["duration"] = max(
                                timing_data["duration"], token.end_ts
                            )
                # For non-English or if tokens are not available, just estimate duration
                elif result.tokens is not None and len(result.tokens) > 0:
                    last_token = result.tokens[-1]
                    if last_token.end_ts is not None:
                        timing_data["duration"] = max(
                            timing_data["duration"], last_token.end_ts
                        )
                    else:
                        timing_data["duration"] += len(result.tokens) * 0.5

                # Save audio segment
                if result.audio is not None:
                    audio_data = result.audio.cpu().numpy()
                    temp_segment_path = os.path.join(
                        self.temp_dir,
                        f"chapter_{chapter_index}_segment_{len(audio_segments)}.wav",
                    )
                    sf.write(temp_segment_path, audio_data, 24000)
                    audio_segments.append(temp_segment_path)

            # Merge audio segments if needed
            if len(audio_segments) > 1:
                if not _merge_audio_chunks_and_export_wav(
                    audio_segments, chapter_wav_path
                ):
                    raise Exception(f"Failed to merge chapter {chapter_index} segments")
            elif len(audio_segments) == 1:
                os.rename(audio_segments[0], chapter_wav_path)
            else:
                raise Exception(
                    f"No audio segments generated for chapter {chapter_index}"
                )

            timing_data["end_time"] = current_time + timing_data["duration"]
            return chapter_wav_path, timing_data

        except Exception as e:
            logger.error(f"Error generating chapter {chapter_index}: {str(e)}")
            return None, timing_data

    @retry_on_exception(retries=3, delay=1.0, exceptions=(Exception,))
    def generate_audio(
        self,
        text_segments: List[str],
        output_path: str,
        voice_id: Optional[str] = None,
        **kwargs: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate audio for each chapter with timing information.
        """
        if voice_id:
            self.voice_id = voice_id

        chapter_wav_files = []
        timing_data = {"chapters": [], "total_duration": 0.0}

        try:
            current_time = 0.0

            # Process each chapter
            for i, chapter_text in enumerate(text_segments):
                if not chapter_text.strip():
                    continue

                wav_path, chapter_timing = self._generate_chapter_audio(
                    chapter_text, i, current_time
                )

                if wav_path:
                    chapter_wav_files.append(wav_path)
                    timing_data["chapters"].append(chapter_timing)
                    current_time = chapter_timing["end_time"]

            if not chapter_wav_files:
                raise Exception("No audio was generated for any chapter")

            # Merge all chapter audio files
            if not _merge_audio_chunks_and_export_wav(chapter_wav_files, output_path):
                raise Exception("Failed to merge chapter audio files")

            # Validate final output
            if not _validate_wav_file(output_path):
                raise Exception("Final audio file is invalid")

            timing_data["total_duration"] = current_time
            size = os.path.getsize(output_path)

            return {
                "success": True,
                "path": output_path,
                "size": size,
                "timing_data": timing_data,
            }

        except Exception as e:
            logger.error(f"Audio generation failed: {str(e)}")
            # Cleanup
            try:
                for f_name in os.listdir(self.temp_dir):
                    if f_name.startswith(("chapter_", "kokoro_chunk_")):
                        os.remove(os.path.join(self.temp_dir, f_name))
            except OSError:
                pass

            return {
                "success": False,
                "error": str(e),
                "path": None,
                "size": 0,
                "timing_data": None,
            }
