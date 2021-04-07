class Tile:
    def _emoji(self) -> str:
        raise NotImplementedError()

    def __str__(self) -> str:
        return self._emoji()

class Bee(Tile):
    def _emoji(self) -> str:
        return "🐝"

class Ant(Tile):
    def _emoji(self) -> str:
        return "🐜"

class Spider(Tile):
    def _emoji(self) -> str:
        return "🕷️"
