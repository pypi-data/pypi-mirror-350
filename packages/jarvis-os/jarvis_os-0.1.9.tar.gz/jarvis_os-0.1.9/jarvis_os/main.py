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
    import pygame
    import re
    import textwrap
    import pygetwindow as gw
    import psutil
    import shutil 
    from rich.console import Console
    from rich.live import Live
    from rich.panel import Panel
    from rich.text import Text
    import time
    from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
    from rich.progress import SpinnerColumn
    import itertools
    import contextlib

    state = {
        "awaiting_shutdown" : False,
        "is_speaking" : False,
        "is_stopped" : False

    }
    app_processes = {}

    chat_history = [{"role": "system", "content": "You are Jarvis, a helpful and concise AI assistant."}]
    screen_queue = queue.Queue()
    llm_stop_event = threading.Event()
    system_commands = {
            "settings": "start ms-settings:",
            "file explorer": "explorer",
            "copilot": "start ms-copilot:"
            # Add more here as needed
        }



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

        width = shutil.get_terminal_size((80, 20)).columns

        with Live(refresh_per_second=5) as live:
            for i in range(1, len(ascii_jarvis) + 1):
                styled_text = Text(justify="center", no_wrap=True)
                for line in ascii_jarvis[:i]:
                    styled_text.append(line + "\n", style="bold bright_magenta")
                panel = Panel(styled_text, border_style="bold magenta", padding=(1, 4), width=width)
                live.update(panel)
                time.sleep(0.4)

            # Final glow
            time.sleep(0.3)
            final_text = Text(justify="center", no_wrap=True)
            for line in ascii_jarvis:
                final_text.append(line + "\n", style="bold cyan")
            panel = Panel(final_text, border_style="bold blue", padding=(1, 4), width=width)
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
            task = progress.add_task("[bold bright_magenta]Loading Speech Recognition Model...", total=100)
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
        loading_text = "Loading Speech Recognition Model:  "

        with Live(refresh_per_second=10) as live:
            start_time = time.time()
            done = threading.Event()

            def animate_spinner():
                while not done.is_set():
                    spinner = next(spinner_cycle)
                    text = Text(f"{loading_text} {spinner}", style="bold bright_magenta")
                    live.update(Panel(text, border_style="bright_magenta"))
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
                continue  # Skip speaking entirely if stop triggered
            if sentence:
                state["is_speaking"] = True
                yapr.yap(sentence.strip())  # Will be interrupted if speaker supports it
                state["is_speaking"] = False

    threading.Thread(target=yap_thread, daemon=True).start()
    


    def screen_thread():
        while True:
            msg = screen_queue.get()
            if msg is None:
                break

            console.print(Text(msg, style="bold yellow"), end="", soft_wrap=True)



    threading.Thread(target=screen_thread, daemon=True).start()

    # Initialize microphone input
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, 
                    input=True, frames_per_buffer=4000)
    stream.start_stream()

    recognizer = vosk.KaldiRecognizer(model, 16000)


    def shutdown(command):
        if "shutdown" in command.lower() or "shut down" in command.lower() :
            console.print("[bold green_yellow]Are you sure you want to shutdown now?[/bold green_yellow]")
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

    def extract_app_name(command):
        command = command.lower()
        for verb in ["open", "start", "launch", "run"]:
            if verb in command:
                command = command.replace(verb, "")
        command = command.strip()

        # Clean up trailing polite phrases or noise
        command = re.sub(r"\b(for me|please|now|up)\b", "", command).strip()

        # Optional: map verbose names to executable names
        app_aliases = {
            "google chrome": "chrome",
            "chrome browser": "chrome",
            "file explorer": "explorer",
            "ms word": "winword",
            "copilot": "copilot",
            "vs code": "code",
        }

        return app_aliases.get(command, command)

    def open_software(command):
        if not any(trigger in command.lower() for trigger in ["open", "start", "launch"]):
            return False

        app_name = extract_app_name(command)

        # Special system-level commands (not actual executables)


        if app_name in system_commands:
            try:
                subprocess.Popen(system_commands[app_name], shell=True)
                sentence_queue.put(f"Got it. Opening {app_name}.")
                return True
            except Exception as e:
                print(f"Error opening {app_name}: {e}")
                return False

        # Normal executable search and launch
        executable_path = find_executable(app_name)
        if executable_path:
            try:
                process = subprocess.Popen([executable_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False)
                app_processes[app_name] = process
                sentence_queue.put(f"Got it. Opening {app_name}.")
                return True
            except Exception as e:
                print(f"Error opening {app_name}: {e}")
                return True

        print(f"Could not find the application: {app_name}")
        sentence_queue.put(f"Sorry, I couldn't find {app_name}.")
        return True

    def where_search(app_name):
        """Try to locate the executable using Windows 'where' command."""
        try:
            output = subprocess.check_output(["where", app_name], stderr=subprocess.DEVNULL, shell=True)
            return output.decode().splitlines()[0]  # return first match
        except subprocess.CalledProcessError:
            return None

    def bfs_search_executable(start_dirs, app_name, max_depth=10):
        """Breadth-first search for an .exe in known app folders."""
        target = app_name.lower().strip().replace(" ", "")
        queue = deque([(path, 0) for path in start_dirs])
        visited = set()

        while queue:
            current_dir, depth = queue.popleft()
            if depth > max_depth or current_dir in visited:
                continue
            visited.add(current_dir)

            try:
                with os.scandir(current_dir) as entries:
                    for entry in entries:
                        if entry.is_file():
                            name = entry.name.lower().replace(" ", "")
                            if name.startswith(target) and name.endswith(".exe"):
                                return entry.path
                        elif entry.is_dir():
                            queue.append((entry.path, depth + 1))
            except (PermissionError, FileNotFoundError):
                continue

        return None

    def find_executable(app_name):
        """Find the path to an app either via system path or fallback BFS."""
        app_name = app_name.lower().strip().replace(".exe", "")

        # Try exact match in system PATH using 'where'
        exe_path = where_search(app_name)
        if exe_path:
            return exe_path

        # Try app_name.exe
        exe_path = where_search(app_name + ".exe")
        if exe_path:
            return exe_path

        # Fallback: limited-depth search in common locations
        common_paths = [
            os.environ.get("ProgramFiles", r"C:\Program Files"),
            os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
            os.path.expanduser("~\\AppData\\Local\\Programs"),
            os.path.expanduser("~\\AppData\\Local"),
            os.path.expanduser("~\\AppData\\Roaming"),
            os.path.expanduser("~\\Desktop")
        ]


        return bfs_search_executable(common_paths, app_name)

    def clean_command(command):
        command = command.lower()
        command = re.sub(r"\b(closedown|closed|close|kill|exit|quit)\b", "", command)
        return command.strip()

    def is_process_running(process_name):
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] and process_name.lower() in proc.info['name'].lower():
                return True
        return False


    def close_window_by_title(partial_title):
        for window in gw.getWindowsWithTitle(partial_title):
            try:
                window.restore()
                window.close()
                return True
            except Exception:
                continue
        return False

    def close_software(command):
        if not any(trigger in command.lower() for trigger in ["close", "closed", "closedown", "kill", "exit", "quit"]):
            return False

        command = clean_command(command)
        app_name = extract_app_name(command)

        process_aliases = {
            "code": "Code",
            "vs code": "Code",
            "discord": "Discord",
            "copilot": "WindowsCopilot",  # fallback name, not used here directly
            "settings": "SystemSettings",
            "chrome": "chrome",
        }

        window_titles = {
            "copilot": "Copilot",
            "settings": "Settings",
            "code": "Visual Studio Code",
            "discord": "Discord",
            "chrome": "Google Chrome",
        }

        # Step 1: Try closing by window title
        window_title = window_titles.get(app_name, app_name)
        if close_window_by_title(window_title):
            sentence_queue.put(f"Closed {app_name}.")
            if app_name in app_processes:
                del app_processes[app_name]
            return True

        # Step 2: Fallback to taskkill
        process_name = process_aliases.get(app_name, app_name)
        try:
            subprocess.run(
                ["taskkill", "/F", "/IM", f"{process_name}.exe"],
                check=True,
                shell=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            sentence_queue.put(f"Force-closing {app_name}.")
            if app_name in app_processes:
                del app_processes[app_name]
            return True
        except subprocess.CalledProcessError:
            sentence_queue.put(f"Could not close {app_name}.")
            return True



    def should_web_search(question):
        keywords = [
            # General info
            "today", "now", "currently", "latest", "breaking", "recent", "live", "current", "happening", "ongoing",
            "news", "update", "headline", "report", "event", "incident", "story", "alerts",

            # Dates and time-sensitive
            "this week", "this month", "this year", "tomorrow", "yesterday", "tonight", "morning", "afternoon", "evening",
            "calendar", "date", "schedule", "time", "deadline",

            # Questions
            "who is", "who's", "what's", "whose", "what is", "when is", "when did", "when's", "where's", "where is", "how to", "how do", "how does", "how many", "how long", "how much",
            "is it", "are there", "does", "did", "will", "should", "can", "could", "would", "why", "why's",

            # People / Places
            "person", "celebrity", "politician", "president", "prime minister", "celebs", "location", "country", "city", "state",
            "leader", "CEO", "actor", "singer", "athlete", "influencer", "artist", "born", "die", "death",

            # Dynamic facts
            "weather", "temperature", "forecast", "humidity", "sunrise", "sunset", "rain", "snow",
            "stock", "price", "crypto", "market", "bitcoin", "ethereum", "shares", "value", "worth",
            "score", "game", "match", "tournament", "series", "season", "league", "team", "win", "loss", "tie",

            # Web/pop culture
            "trending", "viral", "reddit", "x", "twitter", "threads", "instagram", "youtube", "tiktok", "views", "subscribers",
            "released", "launch", "dropped", "stream", "episode", "clip", "video", "trailer",

            # Misc data queries
            "conversion", "exchange rate", "convert", "calculator", "population", "height", "age", "distance", "location", "map",
            "definition", "meaning", "synonym", "translate", "translation", "language", "speed", "weight", "rank", "ranking",

            # Indicators of vague/informational intent
            "interesting", "facts", "random", "did you know", "explain", "summary", "top", "list", "stats", "statistics"
        ]

        non_web_search_phrases = [
        # Casual, contains "what", "how", "who", etc.
        "what's up", "what are you doing", "what are you doing right now", "what are you up to",
        "what's going on", "what's happening with you", "what’s new",
        "what is your name", "what's your name", "what are you", "what can you do",
        "what day is it", "what's today's date", "what day of the week is it", "what month is it",
        "what year is it", "what time is it", "what is the time", "what's the time",

        "how are you", "how's it going", "how do you feel", "how can you help", "how does this work",
        "how's your day", "how is your day going", "how do i use you", "how hot is it", "how cold is it",

        "who are you", "who's your creator",

        "when is your birthday", "when do you sleep", "when are you active",

        "where is your code", "where do you live", "where are you from",

        "is it morning", "is it afternoon", "is it evening", "is it raining", "is it snowing", "is it sunny",
        "is it hot", "is it cold", "is it windy", "is it cloudy", "is it dark outside",

        "are you real", "are you sentient", "are you a robot", "are you busy", "are you there", "are you online",

        "can you help me", "can you do something", "can you assist me", "can you tell me a story",
        "can you repeat that", "can you say it again", "can you sing", "can you feel", "can you play music",

        "do you have a name", "do you have feelings", "do you sleep", "do you eat", "do you feel pain",
        "do you play games", "do you have emotions", "do you dream", "do you like music", "do you love me",

        "should i bring an umbrella", "should i wear a jacket",

        "could you explain yourself", "could you repeat that",

        "would you tell me something cool", "would you like to talk", "would you mind helping me"
        ]

        lowered = question.lower()
        if any(p in lowered for p in non_web_search_phrases):
            return False
        return any(kw in lowered for kw in keywords)


    import requests
    from bs4 import BeautifulSoup

    def web_search(query, max_results=3):
        url = f"https://html.duckduckgo.com/html/?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []

        for a in soup.select('.result__a')[:max_results]:
            title = a.get_text()
            href = a['href']
            snippet_tag = a.find_parent(class_='result').select_one('.result__snippet')
            snippet = snippet_tag.get_text() if snippet_tag else ''
            results.append({'title': title, 'url': href, 'snippet': snippet})

        return results


    def ask_lm_studio_streaming(question):
        prompt = question

        if should_web_search(question):
            with console.status("[bold green]Searching the web...[/bold green]", spinner="dots"):
                web_context = web_search(question)
            prompt = f"Here is some recent web information that may help:\n{web_context}\n\nAnswer the question: {question}"

        chat_history.append({"role": "user", "content": prompt})

        url = "https://59b5-2600-4040-2c2c-2700-b4ca-17ee-134f-b0e1.ngrok-free.app/v1/chat/completions"
        headers = {
            "Authorization": "Bearer llama-3.1-8b-lexi-uncensored-v2",
            "Content-Type": "application/json"
        }
        data = {
            "messages": chat_history,
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

                    if llm_stop_event.is_set():
                        break

                    try:
                        json_data = json.loads(decoded_line)
                        result = (
                            json_data.get("choices", [{}])[0].get("delta", {}).get("content", "") or
                            json_data.get("choices", [{}])[0].get("text", "") or
                            json_data.get("choices", [{}])[0].get("message", {}).get("content", "")
                        )

                        if result:
                            # Preserve paragraph breaks but flatten awkward line breaks
                            normalized = result.replace("\n", "[[PARA]]")
                            normalized = re.sub(r"(?<![.!?\n])\[\[PARA\]\]", " ", normalized)  # flatten mid-sentence \n
                            normalized = normalized.replace("[[PARA]]", "\n\n")  # restore true paragraph breaks

                            screen_queue.put(normalized)
                            sentence += normalized

                            if any(result.endswith(p) for p in [".", "?", "!", ";"]):
                                cleaned = re.sub(r"\s+", " ", sentence.strip())
                                sentence_queue.put(cleaned)
                                chat_history.append({"role": "assistant", "content": cleaned})
                                sentence = ""

                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            console.print(f"[red]Error: {e}\nThe LLM may currently be offline. You can set up LM Studio on your local device (and change the url in main.py accordingly), or you can check again another time!\n [/red]")

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
        #print("[Jarvis stopped speaking]")
        pygame.mixer.stop()
        llm_stop_event.set()
        with sentence_queue.mutex:
            sentence_queue.queue.clear()
        state["is_stopped"] = False

        return True

    partial_buffer = deque(maxlen=3)  # holds last few partial phrases

    while True:
        data = stream.read(4000, exception_on_overflow=False)

        if state["is_speaking"]:
            partial = json.loads(recognizer.PartialResult()).get("partial", "").lower()

            if partial:
                partial_buffer.append(partial)
                combined = ' '.join(partial_buffer).strip()
                if "jarvis stop" in combined:
                    print("\n[Detected 'Jarvis stop']\n")
                    data = b""
                    handle_stop_command()
                    stream.read(4000, exception_on_overflow=False)  # flush buffer
                    recognizer.Reset()  # reset Vosk recognizer buffer
                    partial_buffer.clear()  # Prevent leftover speech from triggering commands

                    continue  # skip processing


        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "").lower()

            if state["awaiting_shutdown"]:
                console.print("[bold green]You said:[/bold green]", text)
                if text == "no":
                    console.print("[bold cyan]Shutdown cancelled.[/bold cyan]")
                    stream.stop_stream()
                    yapr.yap("Shutdown cancelled.")
                    stream.start_stream()
                    state["awaiting_shutdown"] = False
                elif text == "yes":
                    console.print("[bold dark_red]JarvisOS is shutting down...[/bold dark_red]")
                    stream.stop_stream()
                    yapr.yap("Shutting down. Goodbye.")
                    stream.start_stream()
                    sys.exit()
                else:
                    console.print("[bold yellow]Sorry, I didn't understand. Would you like to shutdown?[/bold yellow]")
                    print()
                    stream.stop_stream()
                    yapr.yap("Sorry, I didn't understand. Would you like to shutdown?")
                    stream.start_stream()
                continue
            
            elif state["is_stopped"]:
                while state["is_speaking"]:
                    time.sleep(0.5)
                state["is_stopped"] = False

                
            
            elif "jarvis" in text:

                command = text.split("jarvis", 1)[-1].strip()


                console.print("\n[bold green]You said:[/bold green]", command)

                if "clear memory" in command.lower():
                    chat_history[:] = [chat_history[0]]  # reset but preserve system prompt
                    sentence_queue.put("Memory cleared.")
                    continue

                ret1 = google(command)
                ret2 = youtube(command)
                ret3 = open_software(command)
                ret4 = docs(command)
                ret5 = close_software(command)
                ret6 = shutdown(command)

                if not (ret1 or ret2 or ret3 or ret4 or ret5 or ret6) and command != "":
                    llm_stop_event.clear()
                    threading.Thread(target=ask_lm_studio_streaming, args=(command,), daemon=True).start()


            
            
            
if __name__ == "__main__":
    main()
        

