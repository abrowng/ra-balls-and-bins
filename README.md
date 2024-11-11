# Balls and Bins Simulation
Repository for the Randomized Algorithms Assignment 2.

## Description

This project is a simulation of different schemes for allocating n balls in m bins.
This probabilistic problem is used commonly in computer science, for example to model the distribution 
of hash values in hash tables.

## Installation

To run the simulation, first you need to have Python 3 installed on your machine.
It is recommended to create a virtual environment to install the required packages.
You can do this by running the following command:

```bash
python -m venv venv
```

Then, you can clone the repository and run the following command to install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

To run the simulation, you can use the following command:

```bash
python main.py
```

Trials are configured in the `main.py` file, by adding or removing them from the `TRIALS` global variable.
You can change the number of trials and the number of balls and bins to simulate different scenarios.
The results are shown as plots, and the statistical measurements for the gap are printed in the console. 
An example of setting up trials for each type of experiment is shown below:

```python
TRIALS = [
    Trial(allocation_strat=AllocationStrategy.STANDARD, balls=1000, bins=100, repetitions=100),
    Trial(allocation_strat=AllocationStrategy.D_CHOICE, balls=5000, bins=100, choices=2, repetitions=100),
    Trial(allocation_strat=AllocationStrategy.BETA_CHOICE, balls=1000, bins=100, choices=2, repetitions=100, beta=0.5),
    Trial(allocation_strat=AllocationStrategy.B_BATCHED, balls=1000, bins=100, choices=2, repetitions=100, batch_size=2000, beta=0.5),
    Trial(allocation_strat=AllocationStrategy.K_MEDIAN, balls=3000, bins=100, choices=4, repetitions=100, k_median=2),
]
```

Alternatively, by changing the `STD_TRIALS` to false, you can configure in the entrypoint a set of trials with
varying `b`, `d`, `beta` and `k` to run for different values of `n` going from a light-loaded scenario of `n=m`
to a heavy-loaded scenario of `n=m^2`. In this case, the output is a plot showing the behavior of the mean gap as `n` grows.
