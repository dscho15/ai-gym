import torch
import numpy as np

from collections import namedtuple

from algorithms.utils import get_gae_advantages
from algorithms.utils import get_returns

Memory = namedtuple(
    "Memory", ["state", "action", "action_log_prob", "reward", "done", "value"]
)

MemoryAux = namedtuple(
    "MemoryAux", ["state", "actions", "value"]
)


class ExperienceDataset(torch.utils.data.Dataset):
    def __init__(self, episodes: list[list[Memory]]):
        self.advantages, self.episodes = [], []
        for e in episodes:
            self.advantages.extend(get_gae_advantages(e))
            self.episodes.extend(e)

        (
            self.states,
            self.actions,
            self.actions_log_prob,
            self.rewards,
            self.done,
            self.values,
        ) = zip(*self.episodes)

        self.returns = get_returns(self.values, self.advantages)

    def __len__(self):
        return len(self.states)

    def __getitem__(self, idx):
        return (
            self.states[idx].flatten(),
            self.actions[idx].flatten(),
            self.actions_log_prob[idx].flatten(),
            self.rewards[idx],
            self.done[idx],
            self.values[idx],
            self.advantages[idx],
            self.returns[idx],
        )


class ExperienceAuxDataset(torch.utils.data.Dataset):
    def __init__(
        self, episodes_aux: list[MemoryAux], action_log_probs: torch.FloatTensor = None
    ):
        self.episodes_aux = episodes_aux
        (self.states, self.returns, self.old_values) = zip(*self.episodes_aux)

        self.states = torch.stack(self.states)
        self.states = self.states.view((-1, self.states.shape[-1]))
        self.returns = torch.stack(self.returns).view((-1, 1))
        self.old_values = torch.stack(self.old_values).view((-1, 1))
        self.action_log_probs = action_log_probs

    def __len__(self):
        return len(self.states)

    def __getitem__(self, idx):
        return (
            self.states[idx].flatten(),
            self.returns[idx].flatten(),
            self.old_values[idx].flatten(),
            self.action_log_probs[idx].flatten(),
        )
