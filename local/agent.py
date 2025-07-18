import numpy as np
import random
import matplotlib.pyplot as plt

"""
This agent is designed for only this game. It cannot be used for other games.
This is because it is hardcoded for the paddle movement and ball movement of this specific game.
"""
class Agent:

    def __init__(self):
        self.actions = [0, 1]  # 0: left, 2: right
        self.Q = np.full((
            27, # X position of the ball divided into 8 parts
            2, # Number of possible x speed values
            40, # Number of possible Paddle positions (0 to 550 increments of 20)
            2 # number of actions (left or right)
        ), None, dtype=object)
        self.learn = True
        self.epsilon = 0.9  # Exploration rate
        self.expore_or_exploit = 1
        self.alpha = 0.03  # Learning rate
        self.gamma = 0.9  # Discount factor
        self.state = 0
        
        self.x_start = 0

        # Vars for plotting
        self.game_count = 1
        self.scores = [0]
        self.score_sources = [0]  # Track which games were exploited
        
    def random_action(self, actions):
        """Returns a random action from the list of actions."""
        return random.choice(actions) 
    
    def fix_speed(self, ballx_add):
        if ballx_add < 0:
            # print(f"{ballx_add} -> 0")
            return 0
        elif ballx_add > 0:
            # print(f"{ballx_add} -> 1")
            return 1
            
    def fix_paddle(self, paddle1_startx):
        # Convert paddle position to index (0-550 range to 0-27 index)
        paddle_state = paddle1_startx // 20
        if paddle_state < 0:
            paddle_state = 0
        elif paddle_state > 40:
            paddle_state = 40
        return paddle_state
    
    def fix_sizing(self, ballx, ballx_add, paddle1_startx):
        # Convert continuous values to discrete indices
        x_state = ballx // 30
        # 0 = going left, 1 = going right
        speed_state = self.fix_speed(ballx_add)
        # Convert paddle position to index (0-550 range to 0-27 index)
        paddle_state = self.fix_paddle(paddle1_startx)
        return x_state, speed_state, paddle_state

    def get_action(self, ballx, ballx_add, paddle1_startx):
        x_state, speed_state, paddle_state = self.fix_sizing(ballx, ballx_add, paddle1_startx)
        if self.expore_or_exploit == 1:
            r = self.random_action(self.actions)
            return r
        else:
            qentry = self.Q[x_state][speed_state][paddle_state]
            if all([x is None for x in qentry]):
                return self.random_action(self.actions)
            else:
                valid = [0 if x == None else x for x in qentry]
                a = np.argmax(valid)
                # print(f"For state x: {x_state}, speed: {speed_state}, paddle pos: {paddle_state} Q-values for table: {qentry}, Choosing best action {a}")
                return a

    def calculate_next_state(self, ballx, paddle1_startx, action, ballx_add):
        next_paddle = 0
        if action == 0:
            if paddle1_startx >= 20:
                next_paddle = paddle1_startx - 20
        elif action == 1:
            if paddle1_startx <= 780:
                next_paddle = paddle1_startx + 20
        return self.fix_sizing(
            ballx + ballx_add,
            ballx_add,
            next_paddle)


    def update_Q(self, ballx, bally, paddle1_startx, action, hit, ballx_add, score):
        x_state, speed_state, paddle_state = self.fix_sizing(
            ballx, ballx_add, paddle1_startx
        )
        next_x, next_speed, next_paddle = self.calculate_next_state(
        ballx, paddle1_startx, action, ballx_add
        )   
        # print(bally)
        if hit:
            reward = 1 + score
        elif bally >= 1100:
            reward = -1
            # print(f"Ball missed! Reward: {reward}")
        else:
            reward = 0
        current_q = self.Q[x_state][speed_state][paddle_state][action] or 0
        q_entries = [0 if x == None else x for x in self.Q[next_x][next_speed][next_paddle]]
        next_max_q = np.max(q_entries)
        assert next_paddle >= 0 and next_paddle <= 40, "paddle position out of bounds"
        assert paddle_state >= 0 and paddle_state <= 40, "paddle position out of bounds"
        # Update Q-value
        new_q = current_q + (self.alpha) * (reward + self.gamma * next_max_q - current_q)
        # print(f"Updating Q-value for state ({x_state}, {speed_state}, {paddle_state}), action {action} value {new_q}")
        self.Q[x_state][speed_state][paddle_state][action] = new_q

    def plot_scores(self, scores: list):
        mean_score = [0] * len(scores)  # Initialize with zeros
        # Get indices where score_sources is True (exploit games)
        exploit_indices = [i for i, source in enumerate(self.score_sources) if source]
        
        # Plot all scores in light gray
        plt.clf()
        plt.plot(range(len(scores)), scores, color='lightblue', alpha=0.5, label='All scores')
        
        # Plot only exploit scores in blue
        exploit_scores = [(i, scores[i]) for i in exploit_indices]
        if exploit_scores:  # Only plot if there are exploit scores
            x_vals, y_vals = zip(*exploit_scores)
            plt.scatter(x_vals, y_vals, color='blue', alpha=0.5, label='Exploit scores')
        
        # Calculate moving average of exploit scores only
        window_size = len(scores)
        last_mean = 0
        
        for i in range(len(scores)):  # Iterate over all indices
            if i in exploit_indices:
                if i < window_size:
                    # Get all exploit scores up to index i
                    window_scores = [scores[j] for j in exploit_indices if j <= i]
                else:
                    # Get exploit scores from window i-100:i
                    window_scores = [scores[j] for j in exploit_indices 
                                if i-window_size <= j <= i]
                
                if window_scores:
                    last_mean = np.mean(window_scores)
            
            mean_score[i] = last_mean  # Update mean_score for all indices
        
        # Plot moving average
        plt.plot(range(len(scores)), mean_score, color='red', 
                label=f'Mean Exploit Score (window={window_size})', linewidth=2)
        
        plt.title('Training...')
        plt.xlabel('Number of Games')
        plt.ylabel('Score')
        plt.ylim(ymin=0)
        plt.text(len(scores)-1, scores[-1], str(scores[-1]))
        plt.legend()
        plt.show(block=False)
        plt.pause(.1)
        
    def format_q_table(self):
        """Returns the Q-table as a single-line Python list for copy-pasting."""
        # Convert None to 0 or another placeholder if needed, or keep as None
        q_table_list = self.Q.tolist()
        return repr(q_table_list)
