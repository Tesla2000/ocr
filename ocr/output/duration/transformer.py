import logging
import math
from typing import Any
from typing import Literal

import torch
from ocr.output.duration._base import DurationCalculator
from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer
from transformers import PreTrainedModel
from transformers import PreTrainedTokenizerBase

_LOG_PROB_FLOOR = -10.0


class TransformerDurationCalculator(DurationCalculator):
    type: Literal["transformer"] = "transformer"
    model_name: str = "eryk-mazus/polka-1.1b"
    min_duration: float = 0.5
    max_duration: float = 2.0
    context_window: int = 64
    device: str = "cpu"
    _tokenizer: PreTrainedTokenizerBase
    _model: PreTrainedModel
    _context_words: list[str]
    _logger: logging.Logger

    def model_post_init(self, context: Any, /) -> None:
        self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self._model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self._model.to(self.device)
        self._model.eval()
        self._context_words = []
        self._logger = logging.getLogger(__name__)

    def reset(self) -> None:
        self._context_words = []

    def calculate_duration(self, word: str) -> float:
        probability = self._get_word_probability(word)
        self._context_words.append(word)
        if len(self._context_words) > self.context_window:
            self._context_words = self._context_words[-self.context_window :]
        return self._probability_to_duration(probability)

    def _get_word_probability(self, word: str) -> float:
        context_text = " ".join(self._context_words)
        full_text = f"{context_text} {word}" if context_text else word
        context_ids = (
            self._tokenizer.encode(context_text, return_tensors="pt").to(
                self.device
            )
            if context_text
            else torch.tensor([[]], dtype=torch.long, device=self.device)
        )
        full_ids = self._tokenizer.encode(full_text, return_tensors="pt").to(
            self.device
        )
        context_len = context_ids.shape[1]
        target_ids = full_ids[:, context_len:]
        if target_ids.shape[1] == 0:
            self._logger.debug(
                f"No target tokens for word '{word}', returning floor probability"
            )
            return math.exp(_LOG_PROB_FLOOR)
        with torch.no_grad():
            outputs = self._model(full_ids)
        logits = outputs.logits
        log_probs = torch.log_softmax(logits, dim=-1)
        total_log_prob = 0.0
        for i in range(target_ids.shape[1]):
            token_idx = context_len + i
            token_id = target_ids[0, i].item()
            total_log_prob += log_probs[0, token_idx - 1, token_id].item()
        mean_log_prob = total_log_prob / target_ids.shape[1]
        return math.exp(mean_log_prob)

    def _probability_to_duration(self, probability: float) -> float:
        log_prob = max(
            math.log(probability) if probability > 0 else _LOG_PROB_FLOOR,
            _LOG_PROB_FLOOR,
        )
        normalized = log_prob / _LOG_PROB_FLOOR
        duration = self.min_duration + normalized * (
            self.max_duration - self.min_duration
        )
        return max(self.min_duration, min(self.max_duration, duration))
