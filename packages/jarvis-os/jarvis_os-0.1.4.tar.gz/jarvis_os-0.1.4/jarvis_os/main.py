# Copyright 2025 Arvin Adeli
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

def main():
    import os
    os.environ["VOSK_LOG_LEVEL"] = "0"

    import vosk
    import pyaudio
    import json
    import subprocess
    from collections import deque
    import requests
    from jarvis_os.yapper.core import Yapper, PiperSpeaker
    from jarvis_os.yapper.enhancer import GroqEnhancer
    from jarvis_os.yapper.speaker import BaseSpeaker
    from jarvis_os.yapper.speaker import PiperVoiceUS
    import threading
    import queue
    import urllib.request
    import zipfile
    import sys

    state = {
        "awaiting_shutdown" : False,
        "is_speaking" : False,
        "is_stopped" : False

    }

    from rich.console import Console
    from rich.live import Live
    from rich.panel import Panel
    from rich.text import Text
    import time
    from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
    from rich.progress import SpinnerColumn
    import itertools
    import contextlib


    def ensure_vosk_model():
        base_dir = os.path.expanduser("~/.jarvis-os/models")
        model_name = "vosk-model-en-us-0.42-gigaspeech"
        model_path = os.path.join(base_dir, model_name)

        if not os.path.exists(model_path):
            print("Vosk model not found. Downloading...")
            os.makedirs(base_dir, exist_ok=True)

            zip_path = os.path.join(base_dir, f"{model_name}.zip")
            url = f"https://alphacephei.com/vosk/models/{model_name}.zip"
            urllib.request.urlretrieve(url, zip_path)

            print("Extracting model...")
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(base_dir)
            os.remove(zip_path)
            print("Model setup complete.")

        return model_path
    
    def glowing_boot_animation():

        ascii_jarvis = [
                "    _   _    ______     _____ ____         ___  ____  ",
                "     | | / \  |  _ \ \   / /_ _/ ___|       / _ \/ ___| ",
                "  _  | |/ _ \ | |_) \ \ / / | |\___ \ _____| | | \___ \ ",
                " | |_| / ___ \|  _ < \ V /  | | ___) |_____| |_| |___) |",
                "  \___/_/   \_\_| \_\ \_/  |___|____/       \___/|____/ ",
            ]

        with Live(refresh_per_second=5) as live:
            for i in range(1, len(ascii_jarvis) + 1):
                lines = ascii_jarvis[:i]
                styled_text = Text.from_markup("\n".join(f"[bold bright_magenta]{line}" for line in lines), justify="center")
                panel = Panel(styled_text, border_style="bold magenta", padding=(1, 4))
                live.update(panel)
                time.sleep(0.4)

            # Final glow
            time.sleep(0.3)
            final_text = Text.from_markup("\n".join(f"[bold cyan]{line}" for line in ascii_jarvis), justify="center")
            panel = Panel(final_text, border_style="bold blue", padding=(1, 4))
            live.update(panel)
            time.sleep(1.2)

    @contextlib.contextmanager
    def suppress_stderr(log_path = "~/.jarvis-os/logs/jarvis.log"):
        log_path = os.path.expanduser(log_path)
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        with open(log_path, 'w') as log_file:
            stderr_fileno = sys.stderr.fileno()
            with os.fdopen(os.dup(stderr_fileno), 'w') as old_stderr:
                os.dup2(log_file.fileno(), stderr_fileno)
                try:
                    yield
                finally:
                    os.dup2(old_stderr.fileno(), stderr_fileno)

    def load_vosk_model_with_progress():
        model_path = ensure_vosk_model()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            transient=True,
        ) as progress:
            task = progress.add_task("[bold bright_magenta]Loading Vosk Speech Recognition Model...", total=100)
            for _ in range(20):
                time.sleep(0.05)
                progress.update(task, advance=5)
            with suppress_stderr("~/.jarvis-os/logs/jarvis.log"):
                model = vosk.Model(model_path)
        return model

    def load_vosk_model_with_spinner():

        model_path = ensure_vosk_model()
        #spinner_cycle = itertools.cycle(["|  |  |  |  |  |", "J  A  R  V  I  S", "|  |  |  |  |  |", "/  /  /  /  /  /", "-  -  -  -  -  -", "\\  \\  \\  \\  \\  \\"])
        spinner_cycle = itertools.cycle([
                                            "|  |  |  |  |  |",       # classic spinner
                                            "/  /  /  /  /  /",
                                            "-  -  -  -  -  -",
                                            "\\  \\  \\  \\  \\  \\",

                                            "J  |  |  |  |  |",       # morph begins
                                            "J  A  |  |  |  |",
                                            "J  A  R  |  |  |",
                                            "J  A  R  V  |  |",
                                            "J  A  R  V  I  |",
                                            "J  A  R  V  I  S",       # full reveal
                                            "J  A  R  V  I  S",
                                            "J  A  R  V  I  |",       # morph out
                                            "J  A  R  V  |  |",
                                            "J  A  R  |  |  |",
                                            "J  A  |  |  |  |",
                                            "J  |  |  |  |  |",
                                            "|  |  |  |  |  |",       # back to spinner
                                        ])
        loading_text = "Loading Vosk Speech Recognition Model:  "

        with Live(refresh_per_second=10) as live:
            start_time = time.time()
            done = threading.Event()

            def animate_spinner():
                while not done.is_set():
                    spinner = next(spinner_cycle)
                    text = Text(f"{loading_text} {spinner}", style="bold green")
                    live.update(Panel(text, border_style="green"))
                    time.sleep(0.1)

            spinner_thread = threading.Thread(target=animate_spinner, daemon=True)
            spinner_thread.start()

            # Load model (this part blocks the main thread)
            with suppress_stderr("~/.jarvis-os/logs/jarvis.log"):
                model = vosk.Model(model_path)

            done.set()  # stop spinner
            spinner_thread.join()

            # Show success panel
            elapsed = time.time() - start_time
            success = Text(f"✓ Model loaded in {elapsed:.1f} seconds", style="bold cyan")
            live.update(Panel(success, border_style="cyan"))
            time.sleep(1)

        return model



    glowing_boot_animation()

    # def glowing_boot_animation():
    #     console = Console()

    #     ascii_jarvis = [
    #         "    _   _    ______     _____ ____         ___  ____  ",
    #         "     | | / \  |  _ \ \   / /_ _/ ___|       / _ \/ ___| ",
    #         "  _  | |/ _ \ | |_) \ \ / / | |\___ \ _____| | | \___ \ ",
    #         " | |_| / ___ \|  _ < \ V /  | | ___) |_____| |_| |___) |",
    #         "  \___/_/   \_\_| \_\ \_/  |___|____/       \___/|____/ ",
    #     ]

    #     with Live(refresh_per_second=5) as live:
    #         for i in range(1, len(ascii_jarvis) + 1):
    #             lines = ascii_jarvis[:i]
    #             styled_text = Text.from_markup("\n".join(f"[bold cyan]{line}" for line in lines), justify="center")
    #             panel = Panel(styled_text, border_style="bold blue", padding=(1, 4))
    #             live.update(panel)
    #             time.sleep(0.4)

    #         # Final flash or glow
    #         time.sleep(0.3)
    #         final_text = Text.from_markup("\n".join(f"[bold bright_magenta]{line}" for line in ascii_jarvis), justify="center")
    #         panel = Panel(final_text, border_style="bold magenta", padding=(1, 4))
    #         live.update(panel)
    #         time.sleep(1.2)




    # @contextlib.contextmanager
    # def suppress_stderr():
    #     with open(os.devnull, 'w') as fnull:
    #         stderr_fileno = sys.stderr.fileno()
    #         with os.fdopen(os.dup(stderr_fileno), 'w') as old_stderr:
    #             os.dup2(fnull.fileno(), stderr_fileno)
    #             try:
    #                 yield
    #             finally:
    #                 os.dup2(old_stderr.fileno(), stderr_fileno)

    # def load_vosk_model_with_progress():
    #     model_path = ensure_vosk_model()

    #     with Progress(
    #         SpinnerColumn(),
    #         TextColumn("[progress.description]{task.description}"),
    #         BarColumn(),
    #         TimeElapsedColumn(),
    #         transient=True,
    #     ) as progress:
    #         task = progress.add_task("[green]Loading Vosk Speech Recognition Model...", total=100)

    #         for _ in range(20):
    #             time.sleep(0.05)
    #             progress.update(task, advance=5)

    #         # Suppress Vosk logs while loading the model
    #         with suppress_stderr():
    #             model = vosk.Model(model_path)

    #     return model

    model = load_vosk_model_with_spinner()

    #model = vosk.Model(r"C:\Users\arvin\Documents\Jarvis\vosk-model-en-us-0.42-gigaspeech")
    #engine = pyttsx3.init()
    lessac = PiperSpeaker(voice = PiperVoiceUS.JOE)
    yapr = Yapper(speaker = lessac)

    sentence_queue = queue.Queue()
    stop_event = threading.Event()


    def yap_thread():
        while True:
            sentence = sentence_queue.get()
            if stop_event.is_set():
                # Drain the rest of the queue without speaking
                with sentence_queue.mutex:
                    sentence_queue.queue.clear()
                continue
            if sentence:
                state["is_speaking"] = True
                yapr.yap(sentence.strip())
                state["is_speaking"] = False

    threading.Thread(target=yap_thread, daemon=True).start()
    
    # Initialize microphone input
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, 
                    input=True, frames_per_buffer=4000)
    stream.start_stream()

    recognizer = vosk.KaldiRecognizer(model, 16000)


    def shutdown(command):
        if "shutdown" in command.lower() or "shut down" in command.lower() :
            print("Are you sure you want to shutdown now?")
            yapr.yap("Are you sure you want to shutdown now?")
            state["awaiting_shutdown"] = True
            return True
        else:
            return False


    def google(command):
        if "google" in command.lower() or "look up" in command.lower():
            search = command.lower().replace("google", "").replace("look up", "").strip()
            words = search.split()
            url = "https://www.google.com/search?q="

            for item in words:
                if url != "https://www.google.com/search?q=":
                    url += "+"
                url += item

            try:
                subprocess.run(["start", url], shell=True, check=True)
                sentence_queue.put("Sure. Googling " + search + " now.")
            except Exception as e:
                print(f"Google Search Failed: {e}")
            return True
        else:
            return False

    def youtube(command):
        if "search youtube" in command.lower() or "youtube search" in command.lower() or "youtube search for" in command.lower():
            search = command.lower().replace("youtube search for", "").replace("youtube search", "").replace("search youtube", "").strip()
            words = search.split()
            url = "https://www.youtube.com/results?search_query="

            for item in words:
                if url != "https://www.youtube.com/results?search_query=":
                    url += "+"
                url += item

            try:
                subprocess.run(["start", url], shell=True, check=True)
                sentence_queue.put("Sure. Searching YouTube for " + search + " now.")
            except Exception as e:
                print(f"YouTube Search Failed: {e}")
            return True
        else:
            return False


    def open_software(command):
        if "open" in command.lower() or "start" in command.lower():
            app_name = command.lower().replace("open ", "").replace("start ", "").strip()
            
            # Check system PATH for executable
            def is_executable_in_path(executable):
                for path in os.environ["PATH"].split(os.pathsep):
                    full_path = os.path.join(path, executable)
                    if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                        return full_path
                return None

            # Define system-specific commands for non-executable tools
            system_commands = {
                "settings": "start ms-settings:",
                "file explorer": "explorer",
                "copilot": "start ms-copilot:"  # Assuming Copilot can be started via a custom URL scheme or command
                # Add more system-specific commands as needed
            }

            # Try to find the executable in PATH, common paths, or perform BFS search
            executable_path = is_executable_in_path(app_name) or is_executable_in_path(app_name + ".exe")
            if not executable_path:
                common_paths = [
                    os.path.expanduser("~/Desktop"),
                    os.environ.get('ProgramFiles', 'C:/Program Files'),
                    os.environ.get('ProgramFiles(x86)', 'C:/Program Files (x86)'),
                    r"C:\Users\arvin\AppData\Roaming\Microsoft\Windows\Start Menu\Programs"
                ]
                executable_path = bfs_search_executable(common_paths, app_name)
                if not executable_path:
                    # Fallback to search the entire OS starting from the root directory
                    executable_path = bfs_search_executable([os.path.abspath(os.sep)], app_name)
            
            # Execute system commands or open executables
            if executable_path:
                try:
                    subprocess.Popen([executable_path])
                    engineOutput = f"Opening {app_name}..."
                    sentence_queue.put("Got it. Opening " + app_name)
                    #print(f"Opening {app_name}...")
                    #engine.say(engineOutput)
                    #engine.runAndWait()

                except Exception as e:
                    print(f"Error opening {app_name}: {e}")
            elif app_name in system_commands:
                try:
                    subprocess.Popen([system_commands[app_name]], shell=True)
                    sentence_queue.put("Got it. Opening " + app_name)
                    print(f"Opening {app_name}...")
                except Exception as e:
                    print(f"Error opening {app_name}: {e}")
            else:
                print(f"Could not find the application: {app_name} in PATH or common search directories")
            
            return True
        else:
            return False

    def bfs_search_executable(start_dirs, app_name):
        queue = deque(start_dirs)
        visited = set()
        
        while queue:
            current_dir = queue.popleft()
            if current_dir in visited:
                continue
            visited.add(current_dir)

            try:
                with os.scandir(current_dir) as it:
                    for entry in it:
                        if entry.is_file() and entry.name.lower() == app_name.lower() + '.exe':
                            return entry.path
                        elif entry.is_dir():
                            queue.append(entry.path)
            except PermissionError:
                continue
        return None

    def ask_lm_studio_streaming(question):
        url = "https://59b5-2600-4040-2c2c-2700-b4ca-17ee-134f-b0e1.ngrok-free.app/v1/chat/completions"
        headers = {
            "Authorization": "Bearer llama-3.1-8b-lexi-uncensored-v2",
            "Content-Type": "application/json"
        }
        data = {
            "messages": [{"role": "user", "content": question}],
            "max_tokens": 5000,
            "stream": True
        }

        try:
            response = requests.post(url, headers=headers, json=data, stream=True)
            sentence = ""
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8').strip()
                    if decoded_line.startswith("data: "):
                        decoded_line = decoded_line[len("data: "):]

                    if not decoded_line or decoded_line == "[DONE]":
                        continue

                    try:
                        json_data = json.loads(decoded_line)
                        result = (
                            json_data.get("choices", [{}])[0].get("delta", {}).get("content", "") or
                            json_data.get("choices", [{}])[0].get("text", "") or
                            json_data.get("choices", [{}])[0].get("message", {}).get("content", "")
                        )
                        if result:
                            print(result, end="", flush=True)
                            sentence += result
                            if any(result.endswith(p) for p in [".", "?", "!", ";"]):
                                sentence_queue.put(sentence)
                                sentence = ""
                                print()
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            print(f"Error: {e}")


    def docs(command):
        if "create a new document" in command.lower() or "create a new doc" in command.lower() or "create a doc" in command.lower() or "create a google doc" in command.lower():
            url = "https://docs.new"

            try:
                subprocess.run(["start", url], shell=True, check=True)
                sentence_queue.put("Sure, here's a new document.")
            except Exception as e:
                print(f"Google Docs Failed: {e}")
            return True
        else:
            return False

    console = Console()
    
    instructions = Text()
    instructions.append("Say 'Jarvis' followed by a command:\n\n", style="bold underline")
    instructions.append("- ", style="bold green")
    instructions.append("Open [Application]\n", style="cyan")
    instructions.append("- ", style="bold green")
    instructions.append("Google [Search Query]\n", style="cyan")
    instructions.append("- ", style="bold green")
    instructions.append("Youtube Search [Search Query]\n", style="cyan")
    instructions.append("- ", style="bold green")
    instructions.append("Create a new document\n", style="cyan")
    instructions.append("- ", style="bold green")
    instructions.append("Shutdown\n", style="cyan")
    instructions.append("- ", style="bold green")
    instructions.append("Or ask anything your AI assistant can help with— Jarvis can answer questions, explain concepts, and more!\n", style="bold cyan")
    panel = Panel(instructions, title="Jarvis Commands", border_style="blue")

    console.print(panel)

    def handle_stop_command():
        print("[Jarvis stopped speaking]")
        stop_event.set()
        with sentence_queue.mutex:
            sentence_queue.queue.clear()
        while state["is_speaking"]:
            time.sleep(0.05)
        stop_event.clear()
        state["is_stopped"] = False
        return True

    while True:
        partial_buffer = deque(maxlen=3)  # holds last few partial phrases

        while state["is_speaking"]:
            data = stream.read(4000, exception_on_overflow=False)
            partial = json.loads(recognizer.PartialResult()).get("partial", "").lower()
            if partial:
                partial_buffer.append(partial)

            combined = ' '.join(partial_buffer).strip()
            if "jarvis stop" in combined and not state["is_stopped"]:
                partial_buffer.clear()
                state["is_stopped"] = True
                print("[Detected 'Jarvis stop'] (during speech)")
                handle_stop_command()
                break


        data = stream.read(4000, exception_on_overflow=False)
        
        # partial = json.loads(recognizer.PartialResult()).get("partial", "").lower()
        # if "jarvis stop" in partial and not state["is_stopped"]:
        #         state["is_stopped"] = True
        #         print("[Detected 'Jarvis stop'] (while speaking)")
        #         handle_stop_command()
        #         continue

        if not state["is_speaking"] and recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "").lower()

            if state["awaiting_shutdown"]:
                print("You said:", text)

                if text == "no":
                    print("Shutdown cancelled.")
                    stream.stop_stream()
                    yapr.yap("Shutdown cancelled.")
                    stream.start_stream()
                    state["awaiting_shutdown"] = False
                elif text == "yes":
                    print("JarvisOS is shutting down...")
                    stream.stop_stream()
                    yapr.yap("Shutting down. Goodbye.")
                    stream.start_stream()
                    sys.exit()
                else:
                    print("Sorry, I didn't understand. Would you like to shutdown?")
                    stream.stop_stream()
                    yapr.yap("Sorry, I didn't understand. Would you like to shutdown?")
                    stream.start_stream()
                continue

            # if "jarvis stop" in text:
            #     print("[Detected 'Jarvis stop']")
            #     handle_stop_command()
            
            elif "jarvis" in text:

                command = text.split("jarvis", 1)[-1].strip()

                # if "stop" in command:
                #     handle_stop_command()
                #     continue

                print("You said:", command)

                ret1 = google(command)
                ret2 = youtube(command)
                ret3 = open_software(command)
                ret4 = docs(command)
                ret5 = shutdown(command)

                if not (ret1 or ret2 or ret3 or ret4 or ret5) and command != "":
                    ask_lm_studio_streaming(command)

        # else:
        #     # ✅ Check partial results *here*, safely
        #     partial = json.loads(recognizer.PartialResult()).get("partial", "").lower()
        #     if "jarvis stop" in partial:
        #         print("[Detected 'Jarvis stop']")
        #         handle_stop_command()

            
            
            
if __name__ == "__main__":
    main()
        

