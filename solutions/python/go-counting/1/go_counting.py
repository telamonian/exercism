WHITE = "W"
BLACK = "B"
NONE = ""

class Board:
    """Count territories of each player in a Go game

    Args:
        board (list[str]): A two-dimensional Go board
    """

    def __init__(self, board):
        self.board = board

    def get(self, x, y):
        return self.board[y][x]

    def X(self):
        return len(self.board[0])

    def Y(self):
        return len(self.board)

    def shape(self):
        return self.X(), self.Y()
    
    def crawlConnected(self, x, y):
        sym = self.get(x, y)
        coords = {(x, y)}
        surrounds = set()
        shape = self.shape()
        
        def _crawlConnected(x, y):
            for dim in (0, 1):
                for shift in (-1, 1):
                    newCoord = (x + shift, y) if dim == 0 else (x, y + shift)
                    if newCoord[dim] < 0 or newCoord[dim] >= shape[dim]:
                        # bounds check
                        continue
                    newSym = self.get(*newCoord)
                    if newSym == sym:
                        if newCoord not in coords:
                            coords.add(newCoord)
                            _crawlConnected(*newCoord)
                    else:
                        surrounds.add(newSym)

        _crawlConnected(x, y)
        return surrounds, coords
        
    def territory(self, x, y):
        """Find the owner and the territories given a coordinate on
           the board

        Args:
            x (int): Column on the board
            y (int): Row on the board

        Returns:
            (str, set): A tuple, the first element being the owner
                        of that area.  One of "W", "B", "".  The
                        second being a set of coordinates, representing
                        the owner's territories.
        """
        if x < 0 or y < 0 or x >= self.X() or y >= self.Y():
            raise ValueError("Invalid coordinate")
        sym = self.get(x, y)
        if sym != " ":
            return NONE, set()

        surrounds, coords = self.crawlConnected(x, y)
        if len(surrounds) != 1:
            return "", coords
        else:
            return surrounds.pop(), coords

    def territories(self):
        """Find the owners and the territories of the whole board

        Args:
            none

        Returns:
            dict(str, set): A dictionary whose key being the owner
                        , i.e. "W", "B", "".  The value being a set
                        of coordinates owned by the owner.
        """
        ret = {
            "W": set(),
            "B": set(),
            "": set(),
        }
        claimed = set()
        
        for x in range(self.X()):
            for y in range(self.Y()):
                if self.get(x, y) == " " and (x, y) not in claimed:
                    owner, coords = self.territory(x, y)
                    ret[owner] |= coords
                    claimed |= coords

        return ret