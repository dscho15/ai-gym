import torch
import torch.nn as nn
from torch.distributions import normal


class Actor(nn.Module):

    def __init__(self, n_states, n_actions):

        super(Actor, self).__init__()
        self.n_states = n_states

        self.n_actions = n_actions

        self.fc1 = nn.Linear(in_features=self.n_states, out_features=64)
        self.fc2 = nn.Linear(in_features=64, out_features=64)
        self.mu = nn.Linear(in_features=64, out_features=self.n_actions)

        self.log_std = nn.Parameter(torch.zeros(1, self.n_actions))

    def forward(self, inputs):
        x = inputs / torch.tensor([2.5, 2.5, 10, 10, 6.2831855, 10, 0.5, 0.5])
        x = torch.tanh(self.fc1(x))
        x = torch.tanh(self.fc2(x))
        mu = self.mu(x)

        std = self.log_std.exp()
        dist = normal.Normal(mu, std)

        return dist


class Critic(nn.Module):

    def __init__(self, n_states):

        super(Critic, self).__init__()
        self.n_states = n_states

        self.fc1 = nn.Linear(in_features=self.n_states, out_features=64)
        self.fc2 = nn.Linear(in_features=64, out_features=64)
        self.value = nn.Linear(in_features=64, out_features=1)

    def forward(self, inputs):
        x = inputs / torch.tensor([2.5, 2.5, 10, 10, 6.2831855, 10, 0.5, 0.5])
        x = torch.tanh(self.fc1(x))
        x = torch.tanh(self.fc2(x))
        value = self.value(x)

        return value
