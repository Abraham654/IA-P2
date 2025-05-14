import numpy as np

# Import necessary libraries

# Define the forward algorithm function
def forward_algorithm(observations, states, start_prob, trans_prob, emit_prob):
    """
    Perform the forward pass of the Forward-Backward algorithm.
    """
    # Initialize the forward probabilities matrix
    forward_probs = np.zeros((len(states), len(observations)))

    # Initialize the first column with start probabilities and emission probabilities
    for s in range(len(states)):
        forward_probs[s, 0] = start_prob[s] * emit_prob[s, observations[0]]

    # Iterate over each time step
    for t in range(1, len(observations)):
        for s in range(len(states)):
            # Compute the forward probability for state s at time t
            forward_probs[s, t] = sum(forward_probs[prev_s, t - 1] * trans_prob[prev_s, s] for prev_s in range(len(states))) * emit_prob[s, observations[t]]

    return forward_probs

# Define the backward algorithm function
def backward_algorithm(observations, states, trans_prob, emit_prob):
    """
    Perform the backward pass of the Forward-Backward algorithm.
    """
    # Initialize the backward probabilities matrix
    backward_probs = np.zeros((len(states), len(observations)))

    # Set the last column to 1 (end probabilities)
    backward_probs[:, -1] = 1

    # Iterate backward over each time step
    for t in range(len(observations) - 2, -1, -1):
        for s in range(len(states)):
            # Compute the backward probability for state s at time t
            backward_probs[s, t] = sum(trans_prob[s, next_s] * emit_prob[next_s, observations[t + 1]] * backward_probs[next_s, t + 1] for next_s in range(len(states)))

    return backward_probs

# Define the forward-backward algorithm function
def forward_backward_algorithm(observations, states, start_prob, trans_prob, emit_prob):
    """
    Combine forward and backward passes to compute the posterior probabilities.
    """
    # Perform the forward pass
    forward_probs = forward_algorithm(observations, states, start_prob, trans_prob, emit_prob)

    # Perform the backward pass
    backward_probs = backward_algorithm(observations, states, trans_prob, emit_prob)

    # Compute the posterior probabilities
    posterior_probs = np.zeros((len(states), len(observations)))
    for t in range(len(observations)):
        for s in range(len(states)):
            # Multiply forward and backward probabilities for each state and normalize
            posterior_probs[s, t] = forward_probs[s, t] * backward_probs[s, t]
        posterior_probs[:, t] /= np.sum(posterior_probs[:, t])  # Normalize to sum to 1

    return posterior_probs

# Example usage
if __name__ == "__main__":
    # Define the states
    states = [0, 1]  # Example: 0 = Rainy, 1 = Sunny

    # Define the observations (encoded as integers)
    observations = [0, 1, 0]  # Example: 0 = Walk, 1 = Shop

    # Define the start probabilities
    start_prob = np.array([0.6, 0.4])  # Example: P(Rainy) = 0.6, P(Sunny) = 0.4

    # Define the transition probabilities
    trans_prob = np.array([[0.7, 0.3],  # P(Rainy -> Rainy), P(Rainy -> Sunny)
                           [0.4, 0.6]])  # P(Sunny -> Rainy), P(Sunny -> Sunny)

    # Define the emission probabilities
    emit_prob = np.array([[0.1, 0.9],  # P(Walk | Rainy), P(Shop | Rainy)
                          [0.8, 0.2]])  # P(Walk | Sunny), P(Shop | Sunny)

    # Run the forward-backward algorithm
    posterior_probs = forward_backward_algorithm(observations, states, start_prob, trans_prob, emit_prob)

    # Print the posterior probabilities
    print("Posterior probabilities:")
    print(posterior_probs)