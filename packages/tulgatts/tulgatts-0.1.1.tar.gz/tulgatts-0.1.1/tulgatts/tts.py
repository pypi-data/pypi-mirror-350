import requests
import asyncio
import os
# Use the correct library import based on user feedback
from PyCharacterAI import Client
# Import exceptions correctly
from PyCharacterAI.exceptions import AuthenticationError, SessionClosedError 
import logging
import io # For pygame audio playback from bytes

# Optional import for audio playback
try:
    import pygame
    _pygame_available = True
except ImportError:
    _pygame_available = False
    logging.warning("pygame library not found. Audio playback feature will be disabled. Install with 'pip install pygame' or 'pip install tulgatts[audio]'.")

class TulgaTTS:
    """
    Synthesizes speech using a **single, pre-configured Character ID** 
    but allows selecting from **multiple defined Voice IDs** for that character.
    Leverages the PyCharacterAI library.
    """

    # --- Hardcoded Character ID --- 
    _FIXED_CHAR_ID = '2WPyJRflV_4nTx6_-tuNrhkiiqhDyOsn9O25BR1sDO8' # User provided ID (TulgaTTS)
    # -----------------------------

    # --- Available Voices for the Fixed Character --- 
    # Users MUST manually fill this dictionary with Voice Name -> voice_id
    # Use find_voices.py or other methods to find valid voice_ids for the _FIXED_CHAR_ID.
    VOICES = {
        'Tokaev': '99192fcd-c975-401e-a037-330004680010',
        'Nursultan Nazarbaev': '3138d24f-2950-44b8-92ae-d81abacae72b',
        'Pavel Durov': '0e0a98cc-2161-44d8-a857-0dfbe167eccb',
        'Nurlan Saburov': '5177af01-5c0a-4ffe-9325-8f7817739eac',
        'Putin': 'b5fcf542-62be-4edf-bb4b-04ae43e58a3e',
        'Skriptonit': '3a2e1f94-4b10-4c2b-901d-bf6f64657ca9',
        'Elon Musk': '2af1234d-c24d-4bcc-a5d8-bb30cc548cc8',
        'Albert E': '4bb6ecb6-02a0-4458-a89e-11557969745e',
        'Yandex Alica': '5195e632-d3d1-49c0-afa8-5bddc8cd608a',
        'J.A.R.V.I.S': '32fb79f8-7ea1-4939-add2-547337717da5',
        'Tony Stark': '30d762b8-364b-42ae-8dcc-f80bdccd8e1b',
        'Mura':'5de48fb3-2279-45f8-8261-88db39d17847'
    }
  
    def __init__(self, 
                 api_token: str | None = None,
                 voice: str | None = None):
        """
        Initializes the TulgaTTS client for the fixed character, with selectable voices.

        Args:
            api_token (str | None): The Character AI API token. If None, tries env var.
            voice (str | None): The voice name (key from VOICES) to use. 
                                        If None, uses the first voice in VOICES.

        Raises:
            ValueError: If api_token is needed but not found, or if VOICES is empty.
            KeyError: If the specified voice is not found in VOICES.
        """
        if not self.VOICES:
            raise ValueError("The VOICES dictionary in tts.py is empty. Please populate it with voice names and IDs for the fixed character.")
        
        if api_token is None:
            raise ValueError("API token not provided and CHARACTER_AI_TOKEN environment variable not set.")

        self.api_token = api_token
        self.client = Client()
        self._authenticated = False
        self._is_authenticating = False
        self.auth_lock = asyncio.Lock()

        # Set voice
        if voice:
            if voice not in self.VOICES:
                raise KeyError(f"Changed voice '{voice}' not found in the defined VOICES dictionary.")
            self.voice = voice
        else:
            self.voice = list(self.VOICES.keys())[0]

        # Pygame initialization
        if _pygame_available:
            try:
                pygame.mixer.init()
                self._pygame_available = True
            except Exception as e:
                 logging.error(f"Failed to initialize pygame mixer: {e}. Audio playback disabled.")
                 self._pygame_available = False
        else:
            self._pygame_available = False

        self._current_chat = None  # Добавляем хранение текущего чата
        self._current_chat_id = None  # И его ID

    async def _ensure_authenticated(self):
        """Authenticates the PyCharacterAI client if not already done."""
        async with self.auth_lock:
            if self._authenticated or self._is_authenticating:
                return True
            self._is_authenticating = True
            try:
                logging.info("Authenticating PyCharacterAI client...")
                await self.client.authenticate(self.api_token)
                self._authenticated = True
                return True
            except AuthenticationError as e:
                logging.error(f"PyCharacterAI Authentication failed: {e}")
                self._authenticated = False
                raise ConnectionError("Authentication failed. Check your API token.") from e
            except Exception as e:
                logging.error(f"An unexpected error occurred during authentication: {e}")
                self._authenticated = False
                raise ConnectionError(f"Authentication failed unexpectedly: {e}") from e
            finally:
                self._is_authenticating = False

    async def list_voices(self) -> list[str]:
         """Returns a list of available voice names defined in the VOICES dictionary."""
         return list(self.VOICES.keys())

    async def _synthesize_internal(self, text: str, voice_name: str) -> bytes | None:
        """Internal method for TTS using the fixed character ID and the specified voice ID."""
        char_id = self._FIXED_CHAR_ID
        
        # Get voice_id from the VOICES dictionary
        if voice_name not in self.VOICES:
            logging.error(f"Voice '{voice_name}' not found in the defined VOICES dictionary.")
            raise KeyError(f"Voice '{voice_name}' not defined in VOICES.")
        voice_id = self.VOICES[voice_name]
        
        if not voice_id:
            logging.error(f"Voice ID is missing or invalid for voice '{voice_name}' in VOICES.")
            raise ValueError(f"Invalid configuration for voice '{voice_name}'.")

        try:
            if not await self._ensure_authenticated():
                return None

            # Check greeting text length (must not exceed 2048 characters)
            if len(text) > 2048:
                raise ValueError("Greeting text must not exceed 2048 characters!")

            # 1. Fetch all current character parameters
            character = await self.client.character.fetch_character_info(char_id)
            
            # 2. Update greeting to the text to be synthesized
            await self.client.character.edit_character(
                character_id=char_id,
                name=character.name,
                greeting=text,
                title=character.title,
                description=character.description,
                definition=character.definition,
                copyable=character.copyable,
                visibility=character.visibility,
                avatar_rel_path="",
                default_voice_id=character.default_voice_id
            )

            # 3. Create a new chat
            chat_obj, greeting_message = await self.client.chat.create_chat(char_id)

            # 4. Get the greeting message's voiceover
            turn_id = greeting_message.turn_id
            primary_candidate = greeting_message.get_primary_candidate()
            if not primary_candidate:
                logging.error(f"No primary candidate found for greeting message with char ID '{char_id}'.")
                return None
            candidate_id = primary_candidate.candidate_id

            speech_bytes = await self.client.utils.generate_speech(
                chat_id=chat_obj.chat_id,
                turn_id=turn_id,
                candidate_id=candidate_id,
                voice_id=voice_id
            )
            return speech_bytes

        except AuthenticationError as e:
            logging.error(f"Auth error during internal synth for fixed char: {e}")
            self._authenticated = False 
            raise ConnectionError("Authentication failed during synthesis.") from e
        except SessionClosedError as e:
            logging.error(f"Session closed during internal synth for fixed char: {e}")
            self._authenticated = False
            raise ConnectionError("Session closed during synthesis.") from e
        except KeyError as e: # Catch KeyError from VOICES lookup
            logging.error(f"Internal Error: {e}")
            raise
        except ValueError as e: # Catch ValueError for invalid voice config
            logging.error(f"Internal Error: {e}")
            raise
        except Exception as e:
            logging.exception(f"Unexpected error during internal synthesis for fixed char: {type(e).__name__} - {e}")
            raise RuntimeError(f"Unexpected error during synthesis for fixed char.") from e

    async def say_async(self,
                text: str,
                voice: str | None = None,
                output_file: str | None = None,
                play_audio: bool = True) -> str | None:
        """
        Generates speech using the fixed character ID and the specified (or default) voice.

        Args:
            text (str): The text to synthesize.
            voice (str | None): The voice name (key from VOICES) to use. 
                                Defaults to self.voice.
            output_file (str | None): Path to save the generated MP3 audio file.
            play_audio (bool): Whether to play the generated audio using pygame.

        Returns:
            str | None: Path to saved audio file if successful, else None.
        
        Raises:
            KeyError: If the specified voice is not found in VOICES.
            ValueError: If the configuration for the voice in VOICES is invalid.
            ConnectionError: If authentication fails or the session is closed.
            RuntimeError: For other unexpected errors during synthesis.
        """
        used_voice = voice or self.voice
        
        audio_bytes = None
        try:
            # Pass used_voice to internal synth
            audio_bytes = await self._synthesize_internal(text, used_voice)
        except (KeyError, ValueError, ConnectionError, RuntimeError) as e:
             logging.error(f"Synthesis failed for voice '{used_voice}': {e}")
             raise e 
        except Exception as e:
             logging.exception(f"Unexpected error during synthesis call for voice '{used_voice}': {e}")
             raise RuntimeError(f"An unexpected error occurred during synthesis for voice '{used_voice}'.") from e

        if not audio_bytes:
            # This case should ideally not be reached if exceptions are handled correctly above,
            # but kept as a fallback.
            logging.error("Synthesis returned no audio bytes without raising an exception. This indicates an issue.")
            return None

        # Save audio if requested
        saved_path = None
        if output_file:
            try:
                with open(output_file, "wb") as f:
                    f.write(audio_bytes)
                saved_path = output_file
            except IOError as e:
                logging.error(f"Failed to save audio to {output_file}: {e}")
                # Continue to playback if requested, even if saving failed

        # Play audio if requested and possible
        if play_audio:
            if self._pygame_available:
                if not pygame.mixer.get_init():
                    logging.warning("pygame mixer not initialized. Attempting reinit.")
                    try: pygame.mixer.init()
                    except Exception: self._pygame_available = False
                if pygame.mixer.get_init():
                    try:
                        sound = pygame.mixer.Sound(io.BytesIO(audio_bytes))
                        sound.play()
                        # Keep the script running until playback finishes
                        while pygame.mixer.get_busy():
                            await asyncio.sleep(0.1) # Use asyncio.sleep in async context
                    except Exception as e:
                        logging.error(f"Error during pygame audio playback: {e}")
            else:
                logging.warning("Audio playback requested but pygame is not available or failed to initialize.")

        return saved_path
    
    def say(self,
                 text: str,
                 voice: str | None = None, 
                 output_file: str | None = None,
                 play_audio: bool = True) -> str | None:
        """
        Synchronous version of say using the fixed character ID and specified voice.
        Blocks until synthesis and playback (if enabled) are complete.

        Args:
            text (str): Text to synthesize.
            voice (str | None): The voice name (key from VOICES) to use. 
                                Defaults to self.voice.
            output_file (str | None): Path to save the audio.
            play_audio (bool): Play audio using pygame.

        Returns:
            str | None: Path to saved audio file if successful, else None.
        
        Raises:
            KeyError, ValueError, ConnectionError, RuntimeError from say().
            TypeError: If called from a running asyncio event loop.
        """
        used_voice = voice or self.voice
        
        try:
            # Call the updated async say method (with voice param)
            result = asyncio.run(self.say_async(text, used_voice, output_file, play_audio))
            return result
        except RuntimeError as e:
            if "cannot be called from a running event loop" in str(e):
                 logging.error("say_sync cannot be called from a running event loop. Use `await self.say()` instead.")
                 raise TypeError("say_sync cannot be called from a running event loop.") from e
            else: raise
        except Exception as e:
            logging.error(f"Error during say_sync execution: {type(e).__name__} - {e}")
            raise e