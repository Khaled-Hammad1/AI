# Local Package Delivery Optimization

A Python-based optimization project for managing local package delivery operations using **Simulated Annealing** and **Genetic Algorithms**.

## Overview

This project solves a delivery optimization problem for a local package delivery shop.  
The system assigns packages to available vehicles and determines delivery routes while minimizing the total traveled distance.

Each package has:
- destination coordinates `(x, y)`
- weight in kilograms
- priority from `1` to `5`

Each vehicle has:
- a maximum capacity in kilograms

The objective is to minimize operational cost while respecting vehicle capacity constraints and considering package priorities when possible. :contentReference[oaicite:0]{index=0}

## Algorithms Implemented

- **Simulated Annealing**
- **Genetic Algorithm**

The user can choose either algorithm at runtime to generate a solution. :contentReference[oaicite:1]{index=1}

## Features

- Package-to-vehicle assignment
- Route generation and optimization
- Capacity constraint handling
- Priority-aware delivery planning
- Runtime algorithm selection
- Parameter tuning for both algorithms
- User interface for displaying results :contentReference[oaicite:2]{index=2}

## Assumptions

- Shop location is fixed at `(0, 0)`
- Package destinations lie within a 2D grid
- Distance is calculated using the **Euclidean distance formula** :contentReference[oaicite:3]{index=3}

## Recommended Parameters

### Simulated Annealing
- Initial Temperature: `1000`
- Cooling Rate: `0.90 – 0.99`
- Stopping Temperature: `1`
- Iterations per Temperature: `100`

### Genetic Algorithm
- Population Size: `50 – 100`
- Mutation Rate: `0.01 – 0.1`
- Number of Generations: `500` :contentReference[oaicite:4]{index=4}

## Tech Stack

- **Python**
- Search / Optimization Algorithms
- Heuristic Problem Solving

