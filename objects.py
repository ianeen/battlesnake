# Classes for BattleSnake objects held here


class Game:
    class Ruleset:
        def __init__(self, name, version):
            self.name = name
            self.version = version

    def __init__(self, id, ruleset, map, timeout, source):
        self.id = id
        self.ruleset = self.Ruleset(ruleset["name"], ruleset["version"])
        self.map = map
        self.timeout = timeout
        self.source = source


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Coordinate):
            return self.x == other.x and self.y == other.y
        return False

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


class Board:
    def __init__(self, height, width, food, hazards, snakes):
        self.height = height
        self.width = width
        self.food = [Coordinate(f["x"], f["y"]) for f in food]
        self.hazards = [Coordinate(h["x"], h["y"]) for h in hazards]
        self.snakes = [
            Snake(
                s["id"],
                s["name"],
                s["health"],
                s["body"],
                s["latency"],
                s["head"],
                s["length"],
                s["shout"],
                s["squad"],
                s["customizations"],
            )
            for s in snakes
        ]

    def __str__(self):
        board_str = ""
        for y in range(self.height):
            row_str = ""
            for x in range(self.width):
                if Coordinate(x, y) in self.food:
                    row_str += "F"
                elif Coordinate(x, y) in self.hazards:
                    row_str += "H"
                elif any(snake.is_head_at(Coordinate(x, y)) for snake in self.snakes):
                    # find the snake whose head is at this position
                    snake = next(
                        snake
                        for snake in self.snakes
                        if snake.is_head_at(Coordinate(x, y))
                    )
                    if snake.id == "you":
                        row_str += "Y"
                    else:
                        row_str += "S"
                else:
                    row_str += "."
            board_str += row_str + "\n"
        return board_str


class Snake:
    class Customizations:
        def __init__(self, color, head, tail):
            self.color = color
            self.head = head
            self.tail = tail

    def __init__(
        self,
        id,
        name,
        health,
        body,
        latency,
        head,
        length,
        shout,
        squad,
        customizations,
    ):
        self.id = id
        self.name = name
        self.health = health
        self.body = [Coordinate(c["x"], c["y"]) for c in body]
        self.latency = latency
        self.head = Coordinate(head["x"], head["y"])
        self.length = length
        self.shout = shout
        self.squad = squad
        self.customizations = self.Customizations(
            customizations["color"], customizations["head"], customizations["tail"]
        )

    def is_head_at(self, coordinate):
        return self.head.x == coordinate.x and self.head.y == coordinate.y
