import matplotlib.pyplot as plt

from figure import Figure
from color_provider import ColorProvider

class MoneyWelfareFigure(Figure):

    def __init__(self):
        pass

    def set_challenge_number(self, challenge_number):
        self.challenge_number = challenge_number

    def draw(self, sessions, global_stat):

        for session in sessions:
            money = []
            welfare = []

            color_provider = ColorProvider()
            for i in self.challenge_number:
                if len(session.challenge) <= i:
                    continue
                challenge = session.challenge[i]

                money_avg, welfare_avg = global_stat.get_mean(i,
                        challenge.get_oil_cleaning_solution())

                money.append(challenge.money)
                welfare.append(challenge.welfare)

                # color_list = color_provider.get_color_list(i)
                # cluster_tag_name = '_money_welfare_' + str(i)
                # cluster_tag = session.cluster_tags[cluster_tag_name]
                # color = color_list[(cluster_tag - 1) * 2]
                color = self.get_win_lose_color(session.is_win(i))
                solution = challenge.get_oil_cleaning_solution()
                marker = self.get_cleaning_symbol(solution)
                hatch = ""
                if not session.give_recommendation():
                    hatch = "//////"

                plt.scatter(welfare[-1], money[-1], 48,
                        marker = marker,
                        color = color,
                        edgecolors = "black",
                        hatch = hatch)

                plt.annotate(str(session.id),
                    xy=(welfare[-1] + 0.02, money[-1]))

            line_style = 'k-'
            if not session.give_recommendation():
                line_style = 'k--'
            plt.plot(welfare, money, line_style, linewidth = 0.2)

        self.plot_target();



        self.set_x_label("Welfare")
        self.set_y_label("Earnings (Million Dollars)")
        self.ax.set_yticks([-4e6, -2e6, 0, 2e6, 4e6, 6e6]);
        self.ax.set_yticklabels(['-4', '-2', '0', '2', '4', '6'])
        plt.xlim((-0.1, 4))
        plt.ylim((-0.4e7, 0.7e7))

    def get_marker_shape(self, index):
        if index == 0:
            return 'D'
        elif index == 1:
            return 'o'
        else:
            return '^'

    def plot_target(self):
        if len(self.challenge_number) != 1:
            return

        money = 0
        welfare = 0
        if 0 in self.challenge_number:
            money = -640000
            welfare = 0.5
        elif 1 in self.challenge_number:
            money = 2600000
            welfare = 0.5
        elif 2 in self.challenge_number:
            money = 2500000
            welfare = 1.5

        plt.axvline(welfare)
        plt.axhline(money)

    def get_cleaning_symbol(self, solution):
        if solution == "None":
            return 's'
        elif solution == "Burn":
            return 'D'
        elif solution == "Dispersant":
            return 'o'
        elif solution == "Skimmers":
            return '^'
        else:
            print(solution)

    def get_win_lose_color(self, is_win):
        if is_win:
            return 'g'
        else:
            return 'r'
