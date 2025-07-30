import json
import random

from pathlib import Path
from collections import deque

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from torch_geometric.data import Data

from bdo_empire.generate_graph_data import GraphData
from bdo_empire.generate_graph_data import generate_graph_data
from bdo_empire.generate_reference_data import generate_reference_data

# Initialize the PPO algorithm's settings
gamma = 0.99  # Discount factor for rewards
epsilon = 0.2  # Clipping parameter for PPO
ppo_epochs = 4  # Number of epochs to update policy after each batch
batch_size = 64  # Size of the batch for each PPO update


# Define a simple experience buffer for storing experiences
class ExperienceBuffer:
    def __init__(self, max_size=10000):
        self.buffer = deque(maxlen=max_size)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)

    def size(self):
        return len(self.buffer)


# Initialize experience buffer
buffer = ExperienceBuffer()


# Function to calculate discounted rewards
def compute_discounted_rewards(rewards, gamma):
    discounted_rewards = []
    running_sum = 0
    for r in reversed(rewards):
        running_sum = r + gamma * running_sum
        discounted_rewards.insert(0, running_sum)
    return discounted_rewards


# Function for PPO Update
def ppo_update(policy_net, value_net, optimizer_policy, optimizer_value, batch, epsilon=0.2, gamma=0.99):
    states, actions, rewards, next_states, dones = zip(*batch)

    states = torch.stack(states)
    actions = torch.tensor(actions, dtype=torch.long)
    rewards = torch.tensor(rewards, dtype=torch.float)
    next_states = torch.stack(next_states)
    dones = torch.tensor(dones, dtype=torch.float)

    # Calculate the current value estimates (V(s))
    value_estimates = value_net(states).squeeze()

    # Calculate discounted rewards
    discounted_rewards = compute_discounted_rewards(rewards, gamma)
    discounted_rewards = torch.tensor(discounted_rewards, dtype=torch.float)

    # Calculate the advantages (A(s, a) = R - V(s))
    advantages = discounted_rewards - value_estimates

    # Old log probabilities for the actions (for PPO clipping)
    old_log_probs = torch.log(policy_net(states).gather(1, actions.unsqueeze(1))).squeeze()

    # Compute the new log probabilities after action sampling
    log_probs = torch.log(policy_net(states).gather(1, actions.unsqueeze(1))).squeeze()

    # Compute the ratio between new and old probabilities
    ratios = torch.exp(log_probs - old_log_probs)

    # Compute the surrogate loss (clipped)
    surrogate_loss = torch.min(
        ratios * advantages, torch.clamp(ratios, 1 - epsilon, 1 + epsilon) * advantages
    )

    # Policy loss
    policy_loss = -surrogate_loss.mean()

    # Value function loss (MSE between value estimates and discounted rewards)
    value_loss = F.mse_loss(value_estimates, discounted_rewards)

    # Total loss
    total_loss = policy_loss + 0.5 * value_loss

    # Optimize the networks
    optimizer_policy.zero_grad()
    optimizer_value.zero_grad()
    total_loss.backward()
    optimizer_policy.step()
    optimizer_value.step()

    return total_loss.item()


def activate_node(G, node_id):
    """Activate a node in the graph (set its 'isForceActive' flag to True)."""
    node = G["V"].get(node_id)
    if node:
        node.isForceActive = True
        return node.cost  # Return the cost for activating this node
    return 0


def deactivate_node(G, node_id):
    """Deactivate a node in the graph (set its 'isForceActive' flag to False)."""
    node = G["V"].get(node_id)
    if node:
        node.isForceActive = False
        return -node.cost  # Return the negative cost for deactivating the node
    return 0


def set_flow(G, arc_key, flow_amount):
    """Set the flow on an arc and return its effect (reward/punishment)."""
    arc = G["E"].get(arc_key)
    if arc:
        arc_flow_change = flow_amount
        arc.cost = arc.cost + arc_flow_change  # Update arc's cost
        return arc.cost  # Return the change in cost due to flow
    return 0


def simulate_episode(G, policy_net, value_net, optimizer_policy, optimizer_value, budget=100):
    """Simulate an episode and update the policy network based on actions taken."""
    actions = {
        "node_activations": {},  # Maps node_id to activation state (True/False)
        "arc_flows": {},  # Maps arc_key to flow amount (e.g., 0 or 1)
    }

    # Example: random action selection for nodes (for now, just random actions)
    for node_id in G["V"]:
        actions["node_activations"][node_id] = torch.randint(0, 2, (1,)).item()

    # Example: random action selection for arcs (for now, just random flows)
    for arc_key in G["E"]:
        actions["arc_flows"][arc_key] = torch.randint(0, 2, (1,)).item()

    # Compute reward based on the actions taken
    reward = compute_reward(G, actions, budget)

    # Update the policy and value networks based on the reward (using PPO)
    optimizer_policy.zero_grad()
    optimizer_value.zero_grad()

    # Compute the policy loss and value loss (you'll need to implement these)
    policy_loss = compute_policy_loss(policy_net, actions, reward)
    value_loss = compute_value_loss(value_net, actions, reward)

    # Backpropagate the losses
    policy_loss.backward()
    value_loss.backward()

    # Update the networks
    optimizer_policy.step()
    optimizer_value.step()

    return reward


# PPO training loop
def train_ppo(policy_net, value_net, optimizer_policy, optimizer_value, num_epochs=1000):
    for epoch in range(num_epochs):
        # Interact with the environment (this part is usually done with actual interaction, here we simulate it)
        state = torch.randn(1, 64)  # Simulate state (this would be from the graph/environment)
        done = False
        total_reward = 0
        actions = []
        rewards = []
        next_states = []

        while not done:
            # Select action using the policy network (sample from action distribution)
            action_probabilities = policy_net(state)
            action = torch.multinomial(action_probabilities, 1).item()

            # Simulate the environment's response (reward and next state)
            reward = random.uniform(-1, 1)  # Random reward, simulate environment
            next_state = torch.randn(1, 64)  # Random next state

            buffer.push(state, action, reward, next_state, done)

            # Update variables
            state = next_state
            total_reward += reward

            # In a real case, we check if the state is terminal (done=True) here

        # After episode, update the policy and value networks
        if buffer.size() > batch_size:
            batch = buffer.sample(batch_size)
            loss = ppo_update(policy_net, value_net, optimizer_policy, optimizer_value, batch)
            print(f"Epoch {epoch}: Loss {loss}, Total Reward {total_reward}")


class PolicyNetwork(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(PolicyNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, output_dim)  # Output: action probabilities

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return torch.softmax(self.fc3(x), dim=-1)


class ValueNetwork(nn.Module):
    def __init__(self, input_dim):
        super(ValueNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 1)  # Output: value estimation

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)


def extract_node_features(G: GraphData):
    node_features = []
    for node in G["V"].values():
        # Extract features: ub, lb, cost, and binary type indicators
        features = [
            node.ub,  # Upper bound
            node.lb,  # Lower bound
            node.cost,  # Cost
            int(node.isPlant),
            int(node.isLodging),
            int(node.isTown),
            int(node.isWaypoint),
            int(node.isRegion),
        ]
        node_features.append(features)
    return torch.tensor(node_features, dtype=torch.float)


def extract_edge_features(G: GraphData):
    edge_index = []
    edge_features = []
    for arc in G["E"].values():
        edge_index.append([arc.source.id, arc.destination.id])  # Node IDs representing the arc
        edge_features.append([arc.ub, arc.cost])  # Arc features
    edge_index = torch.tensor(edge_index).t().contiguous()
    edge_features = torch.tensor(edge_features, dtype=torch.float)
    return edge_index, edge_features


def build_graph_for_gnn(G: GraphData):
    node_features = extract_node_features(G)
    edge_index, edge_features = extract_edge_features(G)

    # Construct the graph data object for GNN
    data = Data(x=node_features, edge_index=edge_index, edge_attr=edge_features)

    return data


def compute_reward(G, actions, budget=100):
    """Calculate the reward based on actions taken in the environment."""
    prize_values = 0
    cost = 0

    # Iterate over arcs to calculate the prize and cost of flow
    for arc_key, flow in actions["arc_flows"].items():
        arc = G["E"].get(arc_key)
        if arc:
            prize_values += set_flow(G, arc_key, flow)  # Update arc flow cost

    # Iterate over nodes to calculate the prize and cost of activation
    for node_id, activated in actions["node_activations"].items():
        if activated:
            prize_values += activate_node(G, node_id)  # Activate node and get cost
        else:
            prize_values += deactivate_node(G, node_id)  # Deactivate node and reduce cost

    # Penalize if the cost exceeds the budget
    cost = sum([node.cost for node in G["V"].values() if node.isForceActive])
    penalty = 0 if cost <= budget else (cost - budget) * 10  # Example penalty for exceeding budget

    return prize_values - penalty  # Maximize prize, minimize cost over budget


purchased_lodging = {
    "Velia": 0,
    "Heidel": 0,
    "Glish": 0,
    "Calpheon City": 0,
    "Olvia": 0,
    "Keplan": 0,
    "Port Epheria": 0,
    "Trent": 0,
    "Iliya Island": 0,
    "Altinova": 0,
    "Tarif": 0,
    "Valencia City": 0,
    "Shakatu": 0,
    "Sand Grain Bazaar": 0,
    "Ancado Inner Harbor": 0,
    "Arehaza": 0,
    "Old Wisdom Tree": 0,
    "Grána": 0,
    "Duvencrune": 0,
    "O'draxxia": 0,
    "Eilton": 0,
    "Dalbeol Village": 0,
    "Nampo's Moodle Village": 0,
    "Nopsae's Byeot County": 0,
    "Muzgar": 0,
    "Yukjo Street": 0,
    "Godu Village": 0,
    "Bukpo": 0,
}

grindTakenList = []


def main():
    config = {}
    config["name"] = "Empire"
    config["budget"] = 30
    config["top_n"] = 4
    config["nearest_n"] = 5
    config["waypoint_ub"] = 25
    config["prices_path"] = "src/bdo_empire/custom_prices.json"
    config["region_modifiers_path"] = "src/bdo_empire/modifiers.json"

    lodging = purchased_lodging
    prices = json.loads(Path(config["prices_path"]).read_text())["effectivePrices"]
    modifiers = {}

    data = generate_reference_data(config, prices, modifiers, lodging, grindTakenList)
    graph_data = generate_graph_data(data)
    G = graph_data

    # Assuming G is your GraphData object
    node_features = extract_node_features(G)  # Node feature matrix
    edge_index, edge_features = extract_edge_features(G)  # Arc features and edge connectivity

    # PyTorch Geometric data object
    data = Data(x=node_features, edge_index=edge_index, edge_attr=edge_features)

    # Example: Action space for node activation
    node_activation_actions = torch.tensor([1, 0, 1, 0, 1])  # Example activation for 5 nodes
    arc_flow_actions = torch.tensor([1, 0, 1, 1])  # Example flow decisions for 4 arcs

    # Initialize the policy and value networks
    policy_net = PolicyNetwork(
        input_dim=node_features.shape[1], output_dim=len(G["E"])
    )  # Example action space size
    value_net = ValueNetwork(input_dim=node_features.shape[1])

    # Optimizers for PPO
    optimizer_policy = optim.Adam(policy_net.parameters(), lr=1e-3)
    optimizer_value = optim.Adam(value_net.parameters(), lr=1e-3)

    # Start PPO training loop
    train_ppo(policy_net, value_net, optimizer_policy, optimizer_value, num_epochs=1000)


if __name__ == "__main__":
    main()
