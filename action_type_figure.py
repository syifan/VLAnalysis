from figure import Figure
from priority_action import PriorityAction
from color_provider import ColorProvider

import numpy as np
import matplotlib.pyplot as plt
from operator import add

class ActionTypeFigure(Figure):

    def __init__(self):
        super(ActionTypeFigure, self).__init__()

        self.goals = [
            (-640000, 0.5), 
            (2600000, 0.5),
            (2500000, 1.5)
        ]

    def set_challenge_number(self, challenge_number):
        self.challenge_number = challenge_number

    def draw(self, sessions):
        win_sessions, lose_sessions = self.collect_data(sessions)
        ranked_sessions = self.rank_data(win_sessions, lose_sessions)
        action_count = self.get_action_count(ranked_sessions)
    
        self.plot_figure(ranked_sessions, action_count, len(win_sessions))


    def collect_data(self, sessions):
        win_sessions = []
        lose_sessions = []

        for session in sessions:
            if len(session.challenge) <= self.challenge_number:
                continue
            
            challenge = session.challenge[self.challenge_number]
            if challenge.money >= self.goals[self.challenge_number][0] and \
                challenge.welfare >= self.goals[self.challenge_number][1]:
                    win_sessions.append(session)
            else:
               lose_sessions.append(session)

        return win_sessions, lose_sessions

    def rank_data(self, win_sessions, lose_sessions):
        win_sessions.sort(key = lambda x: x.challenge[
                self.challenge_number].money, reverse=True)
        lose_sessions.sort(key = lambda x: x.challenge[
                self.challenge_number].money, reverse=True)
        return win_sessions + lose_sessions
        '''
        sessions = win_sessions + lose_sessions
        sessions.sort(key = lambda x: x.challenge[self.challenge_number].money,
                reverse = True)
        return sessions
        '''

    def get_action_count(self, sessions):
        action_count = []
        for session in sessions:
            challenge = session.challenge[self.challenge_number]
            action_count.append(self.get_action_count_for_challenge(challenge))

        return action_count

    def get_action_count_for_challenge(self, challenge):
        action_count = [0, 0, 0]
        for action in challenge.actions:
            if isinstance(action, PriorityAction):
                if action.priority <= 3:
                    action_count[0] += 1
                elif action.priority <= 8:
                    action_count[1] += 1
                else:
                    action_count[2] += 1
        return action_count

    def plot_figure(self, sessions, action_count, win_count):
        position = range(len(sessions))
        
        color_provider = ColorProvider()  
        bottom = [0] * len(position)
        for i in range(len(action_count[0])):
            data = [x[i] for x in action_count]
            plt.bar(position, data,
                    bottom = bottom,
                    color = color_provider[i])
            bottom = map(add, bottom, data)

        
        plt.plot((win_count, win_count), 
                (0, 200),
                'k-')
        plt.xticks(position, [s.name for s in sessions], rotation = 90)

