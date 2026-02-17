import logging
import math
import tkinter as tk
from collections.abc import Sequence
from logging import Logger
from typing import Literal

from ocr.output import TimedOutput
from ocr.output._base import Output
from ocr.output.timed import WordDurationPair


class TimedWordsViewer(Output):
    _logger: Logger = logging.getLogger(__name__)
    type: Literal["timed-viewer"] = "timed-viewer"
    timed_output: TimedOutput
    reload: bool = False

    async def _save_results(self, result: str) -> None:
        output_file = self.timed_output.path
        if self.reload or not output_file.exists():
            self._logger.info(f"Generating timed output to {output_file}")
            await self.timed_output.save_results(result)
        else:
            self._logger.info(
                f"Loading existing timed output from {output_file}"
            )
        timed_words = tuple(
            map(
                WordDurationPair.model_validate_json,
                output_file.read_text().splitlines(),
            )
        )
        self._logger.info(f"Loaded {len(timed_words)} words for RSVP display")
        self._logger.info(
            f"Total duration of text is {sum(w.duration for w in timed_words)}"
        )
        self._display_gui(timed_words)

    def _display_gui(self, timed_words: Sequence[WordDurationPair]) -> None:
        self._logger.info("Starting RSVP viewer GUI")
        root = tk.Tk()
        root.title("RSVP Reader")
        root.geometry("800x600")
        root.configure(bg="black")
        word_label = tk.Label(
            root,
            text="",
            font=("Arial", 72, "bold"),
            fg="white",
            bg="black",
        )
        word_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        progress_label = tk.Label(
            root,
            text="",
            font=("Arial", 14),
            fg="gray",
            bg="black",
        )
        progress_label.place(relx=0.5, rely=0.85, anchor=tk.CENTER)
        current_index = 0
        is_playing = False
        words_per_minute = 300.0
        min_wpm = 100.0
        max_wpm = 1000.0
        min_log = math.log(min_wpm)
        max_log = math.log(max_wpm)

        def wpm_to_slider(wpm: float) -> float:
            return (math.log(wpm) - min_log) / (max_log - min_log) * 100

        def slider_to_wpm(slider_value: float) -> float:
            log_wpm = min_log + (slider_value / 100) * (max_log - min_log)
            return math.exp(log_wpm)

        def get_word_duration(pair: WordDurationPair) -> float:
            return pair.duration * (60.0 / words_per_minute)

        def show_next_word() -> None:
            nonlocal current_index
            if current_index >= len(timed_words):
                word_label.config(text="Done")
                self._logger.info("Playback completed")
                return
            pair = timed_words[current_index]
            word_label.config(text=pair.word)
            progress_label.config(
                text=f"{current_index + 1} / {len(timed_words)}"
            )
            current_index += 1
            if is_playing:
                duration_ms = int(get_word_duration(pair) * 1000)
                root.after(duration_ms, show_next_word)

        def toggle_playback() -> None:
            nonlocal is_playing, current_index
            if is_playing:
                is_playing = False
                self._logger.debug("Playback paused")
            else:
                is_playing = True
                if current_index >= len(timed_words):
                    current_index = 0
                self._logger.debug("Playback started")
                show_next_word()
            toggle_button.config(text="Pause" if is_playing else "Start")

        def reset_playback() -> None:
            nonlocal is_playing, current_index
            is_playing = False
            current_index = 0
            word_label.config(text="")
            progress_label.config(text="")
            toggle_button.config(text="Start")
            self._logger.debug("Playback reset")

        def on_space(_: tk.Event) -> None:  # type: ignore[type-arg]
            toggle_playback()

        def on_speed_change(slider_value: str) -> None:
            nonlocal words_per_minute
            words_per_minute = slider_to_wpm(float(slider_value))
            speed_entry.delete(0, tk.END)
            speed_entry.insert(0, str(int(words_per_minute)))
            self._logger.debug(
                f"Speed changed to {int(words_per_minute)} WPM via slider"
            )

        root.bind("<space>", on_space)
        button_frame = tk.Frame(root, bg="black")
        button_frame.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
        toggle_button = tk.Button(
            button_frame, text="Start", command=toggle_playback, width=10
        )
        toggle_button.pack(side=tk.LEFT, padx=5)
        reset_button = tk.Button(
            button_frame, text="Reset", command=reset_playback, width=10
        )
        reset_button.pack(side=tk.LEFT, padx=5)
        speed_frame = tk.Frame(root, bg="black")
        speed_frame.place(relx=0.5, rely=0.95, anchor=tk.CENTER)
        speed_entry = tk.Entry(
            speed_frame,
            font=("Arial", 12),
            width=6,
            bg="black",
            fg="white",
            insertbackground="white",
        )
        speed_entry.insert(0, str(int(words_per_minute)))
        speed_entry.pack(side=tk.LEFT, padx=5)
        speed_label = tk.Label(
            speed_frame,
            text="WPM",
            font=("Arial", 12),
            fg="white",
            bg="black",
        )
        speed_label.pack(side=tk.LEFT, padx=5)
        speed_slider = tk.Scale(
            speed_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            command=on_speed_change,
            bg="black",
            fg="white",
            highlightthickness=0,
            length=300,
            showvalue=False,
        )
        speed_slider.set(wpm_to_slider(words_per_minute))
        speed_slider.pack(side=tk.LEFT, padx=5)

        def on_entry_change(_: tk.Event) -> None:  # type: ignore[type-arg]
            try:
                new_wpm = float(speed_entry.get())
                clamped_wpm = max(min_wpm, min(max_wpm, new_wpm))
                nonlocal words_per_minute
                words_per_minute = clamped_wpm
                speed_entry.delete(0, tk.END)
                speed_entry.insert(0, str(int(clamped_wpm)))
                speed_slider.set(wpm_to_slider(clamped_wpm))
                self._logger.debug(
                    f"Speed changed to {int(words_per_minute)} WPM via entry"
                )
            except ValueError:
                speed_entry.delete(0, tk.END)
                speed_entry.insert(0, str(int(words_per_minute)))

        speed_entry.bind("<Return>", on_entry_change)
        speed_entry.bind("<FocusOut>", on_entry_change)
        root.mainloop()
