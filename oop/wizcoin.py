class Wizcoin:
    def __init__(self, galleons, sickles, knuts):
        """Create a new WizCoin object with galleons, sickles and knuts."""
        self.galleons = galleons
        self.sickles = sickles
        self.knuts = knuts

    def value(self):
        """The value in knuts of all coins in the WizCoin object."""
        return (self.galleons*17*29) + (self.sickles * 29) + self.knuts

    def weight_in_grams(self):
        """Return thr weight of coins in grams."""
        return (self.galleons * 31.03) + (self.sickles * 11.34) + (self.knuts * 5.0)
