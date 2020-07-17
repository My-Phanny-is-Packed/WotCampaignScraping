from code.scrapper import Scrapper
import os


class Main:
    top_clans = {}

    def __init__(self) -> None:
        self.topClans = Scrapper.get_top_clans()
        self.get_tonk_data()

    def get_tonk_data(self) -> None:
        # Header
        lines = ["Clan, Tank Eligible, Tanks Received, Battles, Win Rate"]

        # For each clan, get clantools data and create a csv
        for clan in self.topClans:
            tank_data_string = Scrapper.get_clan_tools_data(self.topClans[clan])
            final_string = "{},{}".format(str(clan), tank_data_string)
            lines.append(final_string)
            print(final_string)

        # Write all csvs to a file
        path = os.path.join(os.getcwd(), "metalwarsresults.csv")
        with open(path, "w+") as fp:
            fp.write("\n".join(lines))

        print("Done!")


m = Main()
