from phase_action import PhaseAction
from priority_action import PriorityAction

class ActionCsvGenerator(object):

    def __init__(self):
        self.session_id = 0
        self.run_id = 0
        self.action_id = 0
        self.decision_id = 0

    def generate(self, sessions):
        self.csv_file = open('actions.csv', 'w')
        self.write_header()

        for session in sessions:
            self.session_id = session.id
            for challenge in session.challenge:
                if challenge == None:
                    continue
                self.generate_run(challenge)
            self.run_id = 0


    def write_header(self):
        self.csv_file.write(
            'session_id, challenge, decision_id, decision_start_time, action_id, '
            'action_time, ship_id, priority\n')

            
    def generate_run(self, run):
        self.run_id += 1

        for action in run.actions:
            if isinstance(action, PhaseAction) and action.phase == "Decision":
                self.decision_id += 1
                self.decision_start_time = action.real_time
            elif isinstance(action, PhaseAction) and action.phase == "Simulation":
                self.action_id = 0
            elif isinstance(action, PriorityAction):
                self.generate_priority_action(action)

        self.decision_id = 0
        self.action_id = 0

    def generate_priority_action(self, action):
        self.action_id += 1
        self.csv_file.write(
            '' + str(self.session_id) + ', '
            '' + str(self.run_id) + ', '
            '' + str(self.decision_id) + ', '
            '' + str(self.decision_start_time) + ', '
            '' + str(self.action_id) + ', '
            '' + str(action.real_time) + ', '
            '' + str(action.ship_id) + ', '
            '' + str(action.priority) + '\n')

        
        
   
