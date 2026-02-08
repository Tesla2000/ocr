import tkinter as tk
from collections.abc import Sequence
from tkinter import ttk
from typing import Literal

from ocr.output import TimedOutput
from ocr.output._base import Output
from ocr.output.timed import WordDurationPair


class TimedWordsViewer(Output):
    type: Literal["timed-viewer"] = "timed-viewer"
    timed_output: TimedOutput
    reload: bool = False

    async def save_results(self, result: str) -> None:
        output_file = self.timed_output.path
        if not self.reload or not output_file.exists():
            await self.timed_output.save_results(result)
        self._display_gui(
            tuple(
                map(
                    WordDurationPair.model_validate_json,
                    output_file.read_text().splitlines(),
                )
            )
        )

    def _display_gui(self, timed_words: Sequence[WordDurationPair]) -> None:
        root = tk.Tk()
        root.title("Timed Words Viewer")
        root.geometry("800x600")
        stats_frame = tk.Frame(root)
        stats_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        total_duration = sum(item.duration for item in timed_words)
        stats_label = tk.Label(
            stats_frame,
            text=f"Words: {len(timed_words)} | Total Duration: {total_duration:.2f}",
            font=("Arial", 12, "bold"),
        )
        stats_label.pack()
        tree_frame = tk.Frame(root)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree = ttk.Treeview(
            tree_frame,
            columns=("index", "word", "duration"),
            show="headings",
            yscrollcommand=scrollbar.set,
        )
        scrollbar.config(command=tree.yview)
        tree.heading("index", text="Index")
        tree.heading("word", text="Word")
        tree.heading("duration", text="Duration")
        tree.column("index", width=80, anchor=tk.CENTER)
        tree.column("word", width=500, anchor=tk.W)
        tree.column("duration", width=120, anchor=tk.CENTER)
        tree.pack(fill=tk.BOTH, expand=True)
        for index, pair in enumerate(timed_words, 1):
            tree.insert(
                "", tk.END, values=(index, pair.word, f"{pair.duration:.2f}")
            )
        button_frame = tk.Frame(root)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        close_button = tk.Button(
            button_frame, text="Close", command=root.destroy, width=20
        )
        close_button.pack()
        root.mainloop()
