"""
Weather prediction example using DiscreteHMM.

This example demonstrates using HMMs to model weather patterns,
where hidden states represent weather conditions and observations
are temperature/humidity categories.
"""

import numpy as np

from markov import DiscreteHMM
from markov.utils.io import export_model_parameters, save_model_json


def generate_weather_data(n_days=365, random_state=42):
    """
    Generate synthetic weather data.

    Hidden states: 0=Sunny, 1=Cloudy, 2=Rainy
    Observations: 0=Cold, 1=Mild, 2=Warm, 3=Hot
    """
    np.random.seed(random_state)

    # Weather transition probabilities
    # Sunny tends to stay sunny, but can become cloudy
    # Cloudy can go to any state
    # Rainy tends to stay rainy or become cloudy
    transition_probs = np.array(
        [
            [0.7, 0.25, 0.05],  # From Sunny
            [0.3, 0.4, 0.3],  # From Cloudy
            [0.15, 0.35, 0.5],  # From Rainy
        ]
    )

    # Start more often with sunny weather
    start_probs = np.array([0.6, 0.3, 0.1])

    # Temperature observations based on weather
    # Sunny: more warm/hot days
    # Cloudy: more mild days
    # Rainy: more cold/mild days
    emission_probs = np.array(
        [
            [0.1, 0.2, 0.4, 0.3],  # Sunny: Cold, Mild, Warm, Hot
            [0.2, 0.5, 0.25, 0.05],  # Cloudy: Cold, Mild, Warm, Hot
            [0.4, 0.45, 0.1, 0.05],  # Rainy: Cold, Mild, Warm, Hot
        ]
    )

    # Generate sequence
    states = np.zeros(n_days, dtype=int)
    observations = np.zeros(n_days, dtype=int)

    # Initial state
    states[0] = np.random.choice(3, p=start_probs)

    # Generate sequence
    for t in range(n_days):
        if t > 0:
            states[t] = np.random.choice(3, p=transition_probs[states[t - 1]])

        # Generate observation
        observations[t] = np.random.choice(4, p=emission_probs[states[t]])

    return observations, states, start_probs, transition_probs, emission_probs


def analyze_weather_patterns():
    """Analyze weather patterns using HMM."""
    print("=== Weather Pattern Analysis ===\n")

    # Generate synthetic weather data
    print("1. Generating weather data...")
    observations, true_states, true_start, true_trans, true_emiss = (
        generate_weather_data()
    )

    print(f"Generated {len(observations)} days of weather data")
    print(f"Temperature distribution: {np.bincount(observations)}")
    print(f"True weather distribution: {np.bincount(true_states)}")

    # Labels for interpretation
    weather_labels = ["Sunny", "Cloudy", "Rainy"]
    temp_labels = ["Cold", "Mild", "Warm", "Hot"]

    # Split data into training and testing
    split_point = 300
    train_obs = observations[:split_point]
    test_obs = observations[split_point:]
    train_states = true_states[:split_point]
    test_states = true_states[split_point:]

    print(f"\n2. Training HMM on weather data...")
    print(f"Training period: {len(train_obs)} days")
    print(f"Test period: {len(test_obs)} days")

    # Train HMM
    hmm = DiscreteHMM(n_states=3, n_observations=4, random_state=42)
    hmm.fit([train_obs], n_iter=100, verbose=True)

    # Analyze learned parameters
    print(f"\n3. Learned weather model:")
    print(f"\nStart probabilities (weather likelihood):")
    for i, prob in enumerate(hmm.start_probs):
        print(f"  {weather_labels[i]}: {prob:.3f}")

    print(f"\nTransition probabilities:")
    for i in range(3):
        print(f"  From {weather_labels[i]}:")
        for j in range(3):
            print(f"    To {weather_labels[j]}: {hmm.transition_probs[i,j]:.3f}")

    print(f"\nEmission probabilities (temperature | weather):")
    for i in range(3):
        print(f"  {weather_labels[i]} weather:")
        for j in range(4):
            print(f"    {temp_labels[j]}: {hmm.emission_probs[i,j]:.3f}")

    return hmm, train_obs, test_obs, train_states, test_states


def weather_prediction_demo(hmm, test_obs, test_states):
    """Demonstrate weather prediction capabilities."""
    print(f"\n4. Weather prediction demonstration:")

    # Take a week of test data
    week_obs = test_obs[:7]
    week_states = test_states[:7]

    weather_labels = ["Sunny", "Cloudy", "Rainy"]
    temp_labels = ["Cold", "Mild", "Warm", "Hot"]

    print(f"\nAnalyzing a week of weather:")
    print(f"Day  | Temp     | True Weather | Predicted | Confidence")
    print(f"-" * 55)

    # Predict weather states
    predicted_states = hmm.predict(week_obs)
    posterior_probs = hmm.predict_proba(week_obs)

    for day in range(7):
        temp = temp_labels[week_obs[day]]
        true_weather = weather_labels[week_states[day]]
        pred_weather = weather_labels[predicted_states[day]]
        confidence = np.max(posterior_probs[day])

        print(
            f"{day+1:3d}  | {temp:8} | {true_weather:12} | {pred_weather:9} | {confidence:.3f}"
        )

    # Accuracy
    accuracy = np.mean(predicted_states == week_states)
    print(f"\nWeather prediction accuracy: {accuracy:.3f}")

    # Sequence likelihood
    log_likelihood = hmm.score(week_obs)
    print(f"Week sequence log-likelihood: {log_likelihood:.3f}")

    return predicted_states, posterior_probs


def seasonal_analysis(hmm):
    """Analyze seasonal weather patterns."""
    print(f"\n5. Seasonal weather simulation:")

    weather_labels = ["Sunny", "Cloudy", "Rainy"]
    temp_labels = ["Cold", "Mild", "Warm", "Hot"]

    # Simulate different seasons
    seasons = ["Spring", "Summer", "Fall", "Winter"]
    season_days = 30

    for season in seasons:
        print(f"\n{season} simulation ({season_days} days):")

        # Generate weather for season
        season_obs, season_states = hmm.sample(season_days)

        # Analyze patterns
        weather_counts = np.bincount(season_states, minlength=3)
        temp_counts = np.bincount(season_obs, minlength=4)

        print(f"  Weather distribution:")
        for i, count in enumerate(weather_counts):
            pct = count / season_days * 100
            print(f"    {weather_labels[i]}: {count:2d} days ({pct:4.1f}%)")

        print(f"  Temperature distribution:")
        for i, count in enumerate(temp_counts):
            pct = count / season_days * 100
            print(f"    {temp_labels[i]}: {count:2d} days ({pct:4.1f}%)")


def weather_forecasting_demo(hmm, test_obs):
    """Demonstrate multi-step weather forecasting."""
    print(f"\n6. Weather forecasting demonstration:")

    weather_labels = ["Sunny", "Cloudy", "Rainy"]
    temp_labels = ["Cold", "Mild", "Warm", "Hot"]

    # Take recent observations
    recent_obs = test_obs[:5]
    print(f"\nGiven recent weather observations:")
    for i, obs in enumerate(recent_obs):
        print(f"  Day {i+1}: {temp_labels[obs]}")

    # Get current state probabilities
    posterior_probs = hmm.predict_proba(recent_obs)
    current_state_probs = posterior_probs[-1]

    print(f"\nCurrent weather state probabilities:")
    for i, prob in enumerate(current_state_probs):
        print(f"  {weather_labels[i]}: {prob:.3f}")

    # Forecast next few days by simulating forward
    print(f"\nForecast for next 3 days:")

    forecast_probs = current_state_probs.copy()

    for day in range(1, 4):
        # Apply transition matrix
        forecast_probs = forecast_probs @ hmm.transition_probs

        # Most likely state
        most_likely_state = np.argmax(forecast_probs)
        confidence = forecast_probs[most_likely_state]

        print(
            f"  Day +{day}: {weather_labels[most_likely_state]} (confidence: {confidence:.3f})"
        )

        # Show all probabilities
        print(f"    State probabilities: ", end="")
        for i, prob in enumerate(forecast_probs):
            print(f"{weather_labels[i]}={prob:.2f} ", end="")
        print()


def save_weather_model(hmm, filepath_base="weather_model"):
    """Save the trained weather model."""
    print(f"\n7. Saving weather model...")

    # Save in JSON format
    json_path = f"{filepath_base}.json"
    save_model_json(hmm, json_path)
    print(f"Model saved to {json_path}")

    # Export human-readable parameters
    txt_path = f"{filepath_base}_parameters.txt"
    export_model_parameters(hmm, txt_path)
    print(f"Parameters exported to {txt_path}")


def main():
    """Run weather prediction example."""
    print("HMM Weather Prediction Example")
    print("=" * 50)

    try:
        # Analyze weather patterns
        hmm, train_obs, test_obs, train_states, test_states = analyze_weather_patterns()

        # Weather prediction demo
        pred_states, post_probs = weather_prediction_demo(hmm, test_obs, test_states)

        # Seasonal analysis
        seasonal_analysis(hmm)

        # Forecasting demo
        weather_forecasting_demo(hmm, test_obs)

        # Save model
        save_weather_model(hmm)

        print("\n" + "=" * 50)
        print("Weather prediction example completed!")

        return hmm

    except Exception as e:
        print(f"Error in weather example: {e}")
        raise


if __name__ == "__main__":
    weather_hmm = main()
