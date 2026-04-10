# Adversarial Pong (Minimax AI)

A real-time Pong implementation in Python featuring an AI opponent powered by minimax search with alpha-beta pruning, designed under strict performance constraints.

## Summary

This project applies adversarial search to an interactive game environment. The AI performs forward simulation of game states and selects actions based on predicted outcomes rather than simple reactive heuristics.

This was my first implementation of search-based game AI, inspired by concepts from *The New Turing Omnibus* (A.K. Dewdney), where I explored how theoretical decision algorithms can be adapted into practical, real-time systems.

## Key Features

- Minimax-based AI opponent with alpha-beta pruning  
- Discretised state space for real-time performance  
- Adjustable difficulty via search depth (1–3)  
- Dynamic ball speed scaling  
- Collision simulation inside the search tree  
- Real-time rendering using turtle  
- Audio feedback using pygame.mixer  

## System Design

### State Representation

The continuous game state is discretised to reduce computational complexity:

- Ball position (bx, by)  
- Ball velocity (dx, dy)  
- Paddle position (paddle_y)  

Values are rounded to fixed intervals:
- Position → nearest 10 pixels  
- Velocity → nearest 0.1  

This reduces the branching factor while preserving meaningful behaviour.

### Action Space

At each step, the AI evaluates three possible paddle movements:

- Move up (+20)  
- Stay (0)  
- Move down (-20)  

This keeps the search space small enough for real-time execution.

### Minimax with Alpha-Beta Pruning

The AI simulates future states up to a fixed depth:

- Easy → depth 1  
- Medium → depth 2  
- Hard → depth 3  

Alpha-beta pruning removes unnecessary branches, improving performance without reducing decision quality within the search horizon.

### Evaluation Function

Game states are scored based on:

- Distance between paddle and ball  
- Whether the ball is moving toward the AI  
- Risk of missing the ball near edges  

This produces stable positioning and consistent interception behaviour.

## Performance Trade-offs

The system balances:

- Search depth vs. frame rate  
- Accuracy vs. computational cost  

Discretisation and pruning are essential for maintaining responsiveness.

## Limitations

- Simplified physics (no spin or angular collisions)  
- Heuristic evaluation (not learned)  
- Limited planning depth  

## Running the Project

pip install pygame  
python pong.py  

Ensure the audio file "bounce-8111.mp3" is in the same directory.

## Why This Project

This project demonstrates:

- Application of adversarial search in a real-time system  
- Managing exponential complexity through pruning and discretisation  
- Translating theoretical algorithms into working software  

## Potential Extensions

- Reinforcement learning agent (Q-learning / DQN)  
- Full Pygame-based rendering instead of turtle  
- Improved evaluation heuristics  
- More accurate physics simulation  
