class Party:
    """ The Party class will contain a list
        of party members, and handle which party member
        is currently active in gameplay."""
    def __init__(self, mem1, mem2, mem3, mem4):
        # CONSTRUCTOR PARAMETERS:
        # mem1, mem2, mem3, mem4: Each one of these is an
        # individual party member

        self.party_members = [mem1, mem2, mem3, mem4]
        self.active_member = self.party_members[0]
        self.wealth = None
        self.avg_level = None
        self.cur_dungeon = None

    def switch_active(self):
        """ Method for changing active
            party member."""
        # W and S keys for switching active member
        pass

    def calc_avg_level(self):
        """ Method for calculating average
            level of the party."""
        pass
