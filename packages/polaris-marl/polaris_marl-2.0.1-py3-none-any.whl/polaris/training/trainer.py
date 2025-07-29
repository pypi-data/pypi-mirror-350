"""
Core simulation logic for POLARIS experiments.
"""

import time

import numpy as np
import torch
from tqdm import tqdm

from ..agents.memory.replay_buffer import ReplayBuffer
from ..agents.polaris_agent import POLARISAgent
from ..networks.gnn import TemporalGNN
from ..utils.encoding import calculate_observation_dimension, encode_observation
from ..utils.io import (
    create_output_directory,
    flatten_episodic_metrics,
    get_metrics,
    load_agent_models,
    reset_agent_internal_states,
    save_final_models,
    select_agent_actions,
    set_metrics,
    setup_random_seeds,
    store_transition_in_buffer,
    update_progress_display,
    update_total_rewards,
    write_config_file,
)
from ..utils.metrics import (
    calculate_agent_learning_rates_from_metrics,
    calculate_theoretical_bounds,
    initialize_metrics,
    prepare_serializable_metrics,
    save_metrics_to_file,
    update_metrics,
)
from ..visualization import generate_plots
from .evaluator import Evaluator


class Trainer:
    """
    POLARIS training and evaluation class.

    This class encapsulates all the logic for running POLARIS agents in social learning
    environments, including training, evaluation, and model management.
    """

    def __init__(self, env, args):
        """
        Initialize the trainer.

        Args:
            env: The social learning environment
            args: Command-line arguments/configuration
        """
        self.env = env
        self.args = args
        self.agents = None
        self.replay_buffers = None
        self.metrics = None
        self.output_dir = None
        self.evaluator = None

    def run_agents(self, training=True, model_path=None):
        """
        Run POLARIS agents in the social learning environment.

        Args:
            training: Whether to train the agents (True) or just evaluate (False)
            model_path: Path to load models from (optional)

        Returns:
            learning_rates: Dictionary of learning rates for each agent
            serializable_metrics: Dictionary of metrics for JSON serialization
        """
        # Setup directory
        self.output_dir = create_output_directory(self.args, self.env, training)

        # Initialize agents and components
        obs_dim = calculate_observation_dimension(self.env)
        self.agents = self._initialize_agents(obs_dim)
        load_agent_models(
            self.agents, model_path, self.env.num_agents, training=training
        )

        # Initialize evaluator
        self.evaluator = Evaluator(self.env, self.agents, self.args)

        # Store agents for potential SI visualization
        if hasattr(self.args, "visualize_si") and self.args.visualize_si and training:
            from ..visualization.si_analysis import create_si_visualizations

            create_si_visualizations(self.agents, self.output_dir)

        # Calculate and display theoretical bounds
        theoretical_bounds = calculate_theoretical_bounds(self.env)

        # Handle training vs evaluation
        if training:
            return self._run_training(theoretical_bounds)
        else:
            return self._run_evaluation(theoretical_bounds)

    def _run_training(self, theoretical_bounds):
        """Run the training process."""
        self.replay_buffers = self._initialize_replay_buffers(
            calculate_observation_dimension(self.env)
        )

        # Write configuration
        write_config_file(self.args, self.env, theoretical_bounds, self.output_dir)

        print(
            f"Running {self.args.num_episodes} training episode(s) with {self.args.horizon} steps per episode"
        )

        # Initialize episodic metrics to store each episode separately
        episodic_metrics = {"episodes": []}

        # Training episode loop
        for episode in range(self.args.num_episodes):
            # Set a different seed for each episode based on the base seed
            episode_seed = self.args.seed + episode
            setup_random_seeds(episode_seed, self.env)
            print(
                f"\nStarting training episode {episode+1}/{self.args.num_episodes} with seed {episode_seed}"
            )

            # Initialize fresh metrics for this episode
            self.metrics = initialize_metrics(self.env, self.args, training=True)

            # Run simulation for this episode
            observations, episode_metrics = self._run_training_simulation()

            # Store this episode's metrics separately
            episodic_metrics["episodes"].append(episode_metrics)

        # Process training results
        return self._process_training_results(episodic_metrics, theoretical_bounds)

    def _run_evaluation(self, theoretical_bounds):
        """Run the evaluation process."""
        print(
            f"Running evaluation for {self.args.num_episodes} episode(s) with {self.args.horizon} steps per episode"
        )

        # Use the evaluator for comprehensive evaluation
        evaluation_results = self.evaluator.evaluate(
            num_episodes=self.args.num_episodes,
            num_steps=self.args.horizon,
            output_dir=self.output_dir,
        )

        # Process evaluation results for compatibility
        episodic_metrics = evaluation_results["episodic_metrics"]
        combined_metrics = evaluation_results["aggregated_metrics"]
        learning_rates = evaluation_results["learning_rates"]

        # Save evaluation results
        serializable_metrics = prepare_serializable_metrics(
            combined_metrics,
            learning_rates,
            theoretical_bounds,
            self.args.horizon,
            training=False,
        )

        # Save detailed evaluation results
        evaluation_serializable_metrics = {
            "evaluation_summary": evaluation_results["evaluation_summary"],
            "episodic_data": episodic_metrics,
            "aggregated_metrics": combined_metrics,
            "learning_rates": learning_rates,
            "theoretical_bounds": theoretical_bounds,
            "episode_length": self.args.horizon,
            "num_episodes": self.args.num_episodes,
        }

        save_metrics_to_file(serializable_metrics, self.output_dir, training=False)
        save_metrics_to_file(
            evaluation_serializable_metrics,
            self.output_dir,
            training=False,
            filename="detailed_evaluation_results.json",
        )

        # Generate plots with LaTeX style if requested
        generate_plots(
            combined_metrics,
            self.env,
            self.args,
            self.output_dir,
            training=False,
            episodic_metrics=episodic_metrics,
            use_latex=self.args.use_tex if hasattr(self.args, "use_tex") else False,
        )

        return episodic_metrics, serializable_metrics

    def _process_training_results(self, episodic_metrics, theoretical_bounds):
        """Process and save training results."""
        # Create a flattened version of metrics
        combined_metrics = flatten_episodic_metrics(
            episodic_metrics, self.env.num_agents
        )

        # Process results
        learning_rates = calculate_agent_learning_rates_from_metrics(combined_metrics)

        # Create SI visualizations after training is complete
        if hasattr(self.args, "visualize_si") and self.args.visualize_si:
            from ..visualization.si_analysis import create_si_visualizations

            print("\n===== FINAL SI STATE (AFTER TRAINING) =====")
            create_si_visualizations(self.agents, self.output_dir)

        # Save metrics and models
        serializable_metrics = prepare_serializable_metrics(
            combined_metrics,
            learning_rates,
            theoretical_bounds,
            self.args.horizon,
            training=True,
        )

        # Also save the episodic metrics for more detailed analysis
        episodic_serializable_metrics = {
            "episodic_data": episodic_metrics,
            "learning_rates": learning_rates,
            "theoretical_bounds": theoretical_bounds,
            "episode_length": self.args.horizon,
            "num_episodes": self.args.num_episodes,
        }

        save_metrics_to_file(serializable_metrics, self.output_dir, training=True)
        save_metrics_to_file(
            episodic_serializable_metrics,
            self.output_dir,
            training=True,
            filename="episodic_metrics.json",
        )

        if self.args.save_model:
            save_final_models(self.agents, self.output_dir)

        # Generate plots with LaTeX style if requested
        generate_plots(
            combined_metrics,
            self.env,
            self.args,
            self.output_dir,
            training=True,
            episodic_metrics=episodic_metrics,
            use_latex=self.args.use_tex if hasattr(self.args, "use_tex") else False,
        )

        return episodic_metrics, serializable_metrics

    def _run_training_simulation(self):
        """Run the main training simulation loop."""
        print(f"Starting training for {self.args.horizon} steps...")
        start_time = time.time()

        # Initialize environment and agents
        observations = self.env.initialize()
        total_rewards = np.zeros(self.env.num_agents)

        # Print environment state information
        self._print_environment_info()

        # If using SI, set the current true state for all agents
        self._setup_si_for_training()

        # Set global metrics for access in other functions
        set_metrics(self.metrics)

        # Reset and initialize agent internal states
        reset_agent_internal_states(self.agents)

        # Set agents to training mode
        for agent_id, agent in self.agents.items():
            agent.set_train_mode()

        # Extract environment parameters for MPE calculation
        env_params = self._extract_environment_params()

        # Main simulation loop
        steps_iterator = tqdm(range(self.args.horizon), desc="Training")
        for step in steps_iterator:
            # Get agent actions
            actions, action_probs = select_agent_actions(self.agents, self.metrics)

            # Collect policy information for continuous actions
            policy_info = self._collect_policy_information_training()

            # Take environment step
            next_observations, rewards, done, info = self.env.step(
                actions, action_probs
            )

            # Add policy distribution parameters to info
            if policy_info:
                info.update(policy_info)
                info["env_params"] = env_params

            # Update rewards
            if rewards:
                update_total_rewards(total_rewards, rewards)

            # Update agent states and store transitions
            self._update_agent_states_training(
                observations, next_observations, actions, rewards, step
            )

            # Update observations for next step
            observations = next_observations

            # For continuous actions in Strategic Experimentation env, add allocations to info
            if (
                hasattr(self.args, "continuous_actions")
                and self.args.continuous_actions
                and hasattr(self.env, "safe_payoff")
            ):
                if "allocations" not in info:
                    info["allocations"] = actions

            # Store and process metrics
            update_metrics(self.metrics, info, actions, action_probs)

            # Update progress display
            update_progress_display(
                steps_iterator, info, total_rewards, step, training=True
            )

            if done:
                self._handle_si_state_changes()
                break

        # Display completion time
        total_time = time.time() - start_time
        print(f"Training completed in {total_time:.2f} seconds")

        return observations, self.metrics

    def _print_environment_info(self):
        """Print information about the current environment state."""
        if hasattr(self.env, "safe_payoff"):
            # Strategic Experimentation Environment
            if self.env.true_state == 0:
                print(
                    f"True state is bad. Drift rate: {self.env.drift_rates[self.env.true_state]} "
                    f"Jump rate: {self.env.jump_rates[self.env.true_state]} "
                    f"Jump size: {self.env.jump_sizes[self.env.true_state]}"
                )
            else:
                print(
                    f"True state is good. Drift rate: {self.env.drift_rates[self.env.true_state]} "
                    f"Jump rate: {self.env.jump_rates[self.env.true_state]} "
                    f"Jump size: {self.env.jump_sizes[self.env.true_state]}"
                )
        else:
            # Social Learning Environment
            print(f"True state is {self.env.true_state}")

    def _setup_si_for_training(self):
        """Setup Synaptic Intelligence for training if enabled."""
        if hasattr(self.args, "use_si") and self.args.use_si:
            current_true_state = self.env.true_state
            for agent_id, agent in self.agents.items():
                if hasattr(agent, "use_si") and agent.use_si:
                    agent.current_true_state = current_true_state
                    # Set the current task in the SI trackers
                    if hasattr(agent, "belief_si") and hasattr(agent, "policy_si"):
                        agent.belief_si.set_task(current_true_state)
                        agent.policy_si.set_task(current_true_state)
                        # Mark that this agent has path integrals calculated so the SI loss will be applied
                        agent.path_integrals_calculated = True
                    print(
                        f"Set current true state {current_true_state} for agent {agent_id}"
                    )

    def _extract_environment_params(self):
        """Extract environment parameters for metric calculation."""
        env_params = {}
        if hasattr(self.env, "safe_payoff"):
            env_params = {
                "safe_payoff": self.env.safe_payoff,
                "drift_rates": self.env.drift_rates,
                "jump_rates": self.env.jump_rates,
                "jump_sizes": self.env.jump_sizes,
                "background_informativeness": self.env.background_informativeness,
                "num_agents": self.env.num_agents,
                "true_state": self.env.true_state,
            }
        return env_params

    def _collect_policy_information_training(self):
        """Collect policy information during training."""
        policy_info = {}

        if hasattr(self.args, "continuous_actions") and self.args.continuous_actions:
            policy_means = []
            policy_stds = []
            agent_beliefs = {}

            for agent_id, agent in self.agents.items():
                if hasattr(agent, "action_mean") and hasattr(agent.policy, "forward"):
                    # Get policy parameters directly
                    with torch.no_grad():
                        mean, log_std = agent.policy(
                            agent.current_belief, agent.current_latent
                        )
                        std = torch.exp(log_std)

                    policy_means.append(mean.item())
                    policy_stds.append(std.item())

                    # Extract agent's belief about the state
                    if (
                        hasattr(agent, "current_belief_distribution")
                        and agent.current_belief_distribution is not None
                    ):
                        # Check if belief distribution is valid (not NaN)
                        if torch.isnan(agent.current_belief_distribution).any():
                            # For NaN case, use a default value (0.5)
                            agent_beliefs[agent_id] = 0.5
                        else:
                            # For continuous signals, the belief is directly used
                            if agent.current_belief_distribution.size(1) == 1:
                                # Continuous case - map the value to [0,1] range
                                raw_value = agent.current_belief_distribution[
                                    0, 0
                                ].item()
                                # Clip to ensure it's in [0,1] range
                                agent_beliefs[agent_id] = max(0.0, min(1.0, raw_value))
                            # For binary state (common case), the belief about good state is the probability assigned to state 1
                            elif agent.current_belief_distribution.shape[-1] == 2:
                                agent_beliefs[agent_id] = (
                                    agent.current_belief_distribution[0, 1].item()
                                )
                            else:
                                # For multi-state cases, use a weighted average
                                belief_weights = torch.arange(
                                    agent.current_belief_distribution.shape[-1],
                                    device=agent.current_belief_distribution.device,
                                ).float()
                                belief_weights = belief_weights / (
                                    agent.current_belief_distribution.shape[-1] - 1
                                )  # Normalize to [0,1]
                                agent_beliefs[agent_id] = torch.sum(
                                    agent.current_belief_distribution * belief_weights,
                                    dim=-1,
                                ).item()

            policy_info = {
                "policy_means": policy_means,
                "policy_stds": policy_stds,
                "agent_beliefs": agent_beliefs,
            }

        return policy_info

    def _handle_si_state_changes(self):
        """Handle Synaptic Intelligence state changes when episodes end."""
        if hasattr(self.args, "use_si") and self.args.use_si:
            current_true_state = self.env.true_state
            print(f"Current true state: {current_true_state}")
            # Check if this is a new true state for any agent
            for agent_id, agent in self.agents.items():
                if (
                    hasattr(agent, "use_si")
                    and agent.use_si
                    and hasattr(agent, "seen_true_states")
                ):
                    if current_true_state not in agent.seen_true_states:
                        # We have a new true state, register the previous task and set the new one
                        if hasattr(agent, "belief_si") and hasattr(agent, "policy_si"):
                            # Register completed task for both networks
                            agent.belief_si.register_task()
                            agent.policy_si.register_task()

                            # Set new task
                            agent.belief_si.set_task(current_true_state)
                            agent.policy_si.set_task(current_true_state)

                            # Store task-specific trackers for visualization
                            if hasattr(agent, "state_belief_si_trackers"):
                                # Create clones of the trackers for visualization
                                agent.state_belief_si_trackers[current_true_state] = (
                                    agent._clone_si_tracker(agent.belief_si)
                                )
                                agent.state_policy_si_trackers[current_true_state] = (
                                    agent._clone_si_tracker(agent.policy_si)
                                )

                            print(
                                f"Registered completed task and set new true state {current_true_state} for agent {agent_id}"
                            )

                    # Add current true state to the set of seen states
                    agent.seen_true_states.add(current_true_state)
                    # Update the current true state
                    agent.current_true_state = current_true_state

    def _update_agent_states_training(
        self, observations, next_observations, actions, rewards, step
    ):
        """Update agent states and store transitions in replay buffer during training."""

        # Check if we're using continuous actions
        continuous_actions = (
            hasattr(self.args, "continuous_actions") and self.args.continuous_actions
        )

        for agent_id, agent in self.agents.items():
            # Get current and next observations
            obs_data = observations[agent_id]
            next_obs_data = next_observations[agent_id]

            # Extract signals and neighbor actions based on environment type
            if "signal" in obs_data:
                # Social Learning Environment format
                signal = obs_data["signal"]
                next_signal = next_obs_data["signal"]
                neighbor_actions = obs_data["neighbor_actions"]
                next_neighbor_actions = next_obs_data["neighbor_actions"]
            elif "background_signal" in obs_data:
                # Strategic Experimentation Environment format
                # Use the background signal increment directly without any transformation

                # Get the background signal increment if available, otherwise use the background signal
                if (
                    "background_increment" in obs_data
                    and "background_increment" in next_obs_data
                ):
                    # Use the raw increment values directly
                    signal = obs_data["background_increment"]
                    next_signal = next_obs_data["background_increment"]
                else:
                    # Fallback to using the background signal if increment isn't available
                    signal = obs_data["background_signal"]
                    next_signal = next_obs_data["background_signal"]

                # Get allocations instead of discrete actions
                neighbor_allocations = obs_data.get("neighbor_allocations", {})
                next_neighbor_allocations = next_obs_data.get(
                    "neighbor_allocations", {}
                )
                # Handle None values by using empty dictionaries instead
                # Always use raw allocation values for continuous actions, never convert to binary
                neighbor_actions = (
                    {} if neighbor_allocations is None else neighbor_allocations
                )
                next_neighbor_actions = (
                    {}
                    if next_neighbor_allocations is None
                    else next_neighbor_allocations
                )

            # Encode observations
            # Determine if we're using continuous signals based on the environment type
            continuous_signal = "background_increment" in obs_data

            signal_encoded, actions_encoded = encode_observation(
                signal=signal,
                neighbor_actions=neighbor_actions,
                num_agents=self.env.num_agents,
                num_states=self.env.num_states,
                continuous_actions=continuous_actions,
                continuous_signal=continuous_signal,
            )
            next_signal_encoded, _ = encode_observation(
                signal=next_signal,
                neighbor_actions=next_neighbor_actions,
                num_agents=self.env.num_agents,
                num_states=self.env.num_states,
                continuous_actions=continuous_actions,
                continuous_signal=continuous_signal,
            )

            # Get current belief and latent states (before observation update)
            belief = (
                agent.current_belief.detach().clone()
            )  # Make a copy to ensure we have the pre-update state
            latent = agent.current_latent.detach().clone()

            # Update agent belief state
            next_belief, next_dstr = agent.observe(signal_encoded, actions_encoded)
            # Infer latent state for next observation
            # This ensures we're using the correct latent state for the next observation
            next_latent = agent.infer_latent(
                signal_encoded,
                actions_encoded,
                (
                    rewards[agent_id]
                    if isinstance(rewards[agent_id], float)
                    else rewards[agent_id]["total"]
                ),
                next_signal_encoded,
            )

            # Store internal states for visualization if requested (for both training and evaluation)

            # Store belief distribution if available
            belief_distribution = agent.get_belief_distribution()
            self.metrics["belief_distributions"][agent_id].append(
                belief_distribution.detach().cpu().numpy()
            )

            # Store transition in replay buffer and update networks
            if agent_id in self.replay_buffers:

                # Get mean and logvar from inference
                mean, logvar = agent.get_latent_distribution_params()

                # Get reward value (handle both scalar and dictionary cases)
                reward_value = (
                    rewards[agent_id]["total"]
                    if isinstance(rewards[agent_id], dict)
                    else rewards[agent_id]
                )

                # Store transition
                store_transition_in_buffer(
                    self.replay_buffers[agent_id],
                    signal_encoded,
                    actions_encoded,
                    belief,
                    latent,
                    actions[agent_id],
                    reward_value,
                    next_signal_encoded,
                    next_belief,
                    next_latent,
                    mean,
                    logvar,
                )

                # Update networks if enough samples
                if (
                    len(self.replay_buffers[agent_id]) > self.args.batch_size
                    and step % self.args.update_interval == 0
                ):
                    # Sample a batch from the replay buffer
                    batch = self.replay_buffers[agent_id].sample(self.args.batch_size)
                    # Update network parameters
                    agent.update(batch)

    def _initialize_agents(self, obs_dim):
        """Initialize POLARIS agents."""
        print(
            f"Initializing {self.env.num_agents} agents{' for evaluation' if self.args.eval_only else ''}..."
        )

        # Log if using GNN
        if self.args.use_gnn:
            print(
                f"Using Graph Neural Network with {self.args.gnn_layers} layers, {self.args.attn_heads} attention heads, and temporal window of {self.args.temporal_window}"
            )
        else:
            print("Using traditional encoder-decoder inference module")

        # Log if excluding final layers from SI
        if (
            hasattr(self.args, "si_exclude_final_layers")
            and self.args.si_exclude_final_layers
            and hasattr(self.args, "use_si")
            and self.args.use_si
        ):
            print("Excluding final layers from Synaptic Intelligence protection")

        # Log if using continuous actions
        if hasattr(self.args, "continuous_actions") and self.args.continuous_actions:
            print("Using continuous action space for strategic experimentation")

        agents = {}

        for agent_id in range(self.env.num_agents):
            # Determine action dimension based on environment and action space type
            if (
                hasattr(self.args, "continuous_actions")
                and self.args.continuous_actions
            ):
                # For continuous actions, we use 1 dimension (allocation between 0 and 1)
                action_dim = 1
            else:
                # For discrete actions, we use num_states dimensions
                action_dim = self.env.num_states

            agent = POLARISAgent(
                agent_id=agent_id,
                num_agents=self.env.num_agents,
                num_states=self.env.num_states,
                observation_dim=obs_dim,
                action_dim=action_dim,
                hidden_dim=self.args.hidden_dim,
                belief_dim=self.args.belief_dim,
                latent_dim=self.args.latent_dim,
                learning_rate=self.args.learning_rate,
                discount_factor=self.args.discount_factor,
                entropy_weight=self.args.entropy_weight,
                kl_weight=self.args.kl_weight,
                device=self.args.device,
                buffer_capacity=self.args.buffer_capacity,
                max_trajectory_length=self.args.horizon,
                use_gnn=self.args.use_gnn,
                use_si=self.args.use_si if hasattr(self.args, "use_si") else False,
                si_importance=(
                    self.args.si_importance
                    if hasattr(self.args, "si_importance")
                    else 100.0
                ),
                si_damping=(
                    self.args.si_damping if hasattr(self.args, "si_damping") else 0.1
                ),
                si_exclude_final_layers=(
                    self.args.si_exclude_final_layers
                    if hasattr(self.args, "si_exclude_final_layers")
                    else False
                ),
                continuous_actions=(
                    self.args.continuous_actions
                    if hasattr(self.args, "continuous_actions")
                    else False
                ),
            )

            agents[agent_id] = agent

        return agents

    def _initialize_replay_buffers(self, obs_dim):
        """Initialize replay buffers for training."""
        replay_buffers = {}

        for agent_id in self.agents:
            replay_buffers[agent_id] = ReplayBuffer(
                capacity=self.args.buffer_capacity,
                observation_dim=obs_dim,
                belief_dim=self.args.belief_dim,
                latent_dim=self.args.latent_dim,
                device=self.args.device,
                sequence_length=8,  # Default sequence length for sampling
            )
        return replay_buffers

    # Public evaluation methods for external use
    def evaluate(self, num_episodes=None, num_steps=None):
        """
        Evaluate the trained agents.

        Args:
            num_episodes: Number of episodes to evaluate (optional)
            num_steps: Number of steps per episode (optional)

        Returns:
            Evaluation results dictionary
        """
        if self.evaluator is None:
            self.evaluator = Evaluator(self.env, self.agents, self.args)

        return self.evaluator.evaluate(num_episodes, num_steps, self.output_dir)

    def quick_evaluate(self, num_steps=100):
        """
        Perform a quick evaluation.

        Args:
            num_steps: Number of steps for quick evaluation

        Returns:
            Basic performance metrics
        """
        if self.evaluator is None:
            self.evaluator = Evaluator(self.env, self.agents, self.args)

        return self.evaluator.quick_evaluate(num_steps)


# Backward compatibility function
def run_agents(env, args, training=True, model_path=None):
    """
    Backward compatibility wrapper for the original function interface.

    Args:
        env: The social learning environment
        args: Command-line arguments
        training: Whether to train the agents (True) or just evaluate (False)
        model_path: Path to load models from (optional)

    Returns:
        learning_rates: Dictionary of learning rates for each agent
        serializable_metrics: Dictionary of metrics for JSON serialization
    """
    trainer = Trainer(env, args)
    return trainer.run_agents(training=training, model_path=model_path)
