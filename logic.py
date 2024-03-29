# Move logic

import objects as battle_objects
import random


def make_move(board, you):
    best_move = None

    if you.health < 60:
        best_move = find_best_next_space(board, you, True)
    else:
        best_move = find_best_next_space(board, you)

    return best_move


def find_best_next_space(board, you, need_food=False):
    best_move = None
    best_move_score = -99999

    for move in ["up", "down", "left", "right"]:
        move_score = 0
        new_head = move_head(you.head, move)
        new_body = you.body.copy()[1:]

        # print(new_head)
        # for b in new_body:
        #     print(b)

        if new_head in board.food:
            if need_food:
                move_score += 100
            else:
                move_score -= 1
        elif will_die(board, new_head, new_body):
            move_score -= 100
        else:
            move_score += 1
            open_cells = get_possible_open_cells(board, you.head, you.body, move)

            if moved_away(you.head, new_head, you.body):
                move_score += 1
            if need_food and move_to_food(board, you.head, new_head):
                move_score += 2
            if move_from_close_bigger_snake(board, you.head, new_head, you.length):
                move_score += 1
            if move_from_close_head(board, you.head, new_head, you.length):
                move_score += 2
            if open_cells > 9:
                move_score += 1
            elif open_cells < 5:
                move_score -= 1

        print(move + ": " + str(move_score))

        if move_score >= best_move_score:
            # Randomly choose between two equally good moves (keep em guessing)
            if move_score == best_move_score and random.randint(0, 1) == 1:
                continue

            best_move = move
            best_move_score = move_score

    return best_move


def move_head(head, move):
    if move == "up":
        return battle_objects.Coordinate(head.x, head.y + 1)
    elif move == "down":
        return battle_objects.Coordinate(head.x, head.y - 1)
    elif move == "left":
        return battle_objects.Coordinate(head.x - 1, head.y)
    elif move == "right":
        return battle_objects.Coordinate(head.x + 1, head.y)


def check_out_of_bounds(board, head):
    if head.x < 0 or head.x >= board.width or head.y < 0 or head.y >= board.height:
        return True
    return False


def check_snake_collide(board, head):
    for snake in board.snakes:
        if head in snake.body:
            return True
    return False


def move_from_close_head(board, head, new_head, length):
    closest_snake = None
    for s in board.snakes:
        if s.head == head:
            continue

        if closest_snake == None:
            closest_snake = s
            continue

        if abs(s.head.x - head.x) + abs(s.head.y - head.y) < abs(
            closest_snake.head.x - head.x
        ) + abs(closest_snake.head.y - head.y):
            closest_snake = s

    if closest_snake.length < length:
        return False

    if abs(new_head.x - closest_snake.head.x) > abs(
        head.x - closest_snake.head.x
    ) or abs(new_head.y - closest_snake.head.y) > abs(head.y - closest_snake.head.y):
        return True

    return False


def move_to_food(board, head, new_head):
    closest_food = None
    for f in board.food:
        if closest_food == None:
            closest_food = f
            continue

        if abs(f.x - head.x) + abs(f.y - head.y) < abs(closest_food.x - head.x) + abs(
            closest_food.y - head.y
        ):
            closest_food = f

    if abs(new_head.x - closest_food.x) < abs(head.x - closest_food.x) or abs(
        new_head.y - closest_food.y
    ) < abs(head.y - closest_food.y):
        return True

    return False


def moved_away(head, new_head, body):
    average_x = 0
    average_y = 0

    for b in body:
        average_x += b.x
        average_y += b.y

    average_x /= len(body)
    average_y /= len(body)

    if abs(new_head.x - average_x) > abs(head.x - average_x) or abs(
        new_head.y - average_y
    ) > abs(head.y - average_y):
        return True

    return False


def move_from_close_bigger_snake(board, head, new_head, length):
    closest_snake = None
    for s in board.snakes:
        if s.head == head:
            continue

        if closest_snake == None:
            closest_snake = s
            continue

        if abs(s.head.x - head.x) + abs(s.head.y - head.y) < abs(
            closest_snake.head.x - head.x
        ) + abs(closest_snake.head.y - head.y):
            closest_snake = s

    if closest_snake.length < length:
        return False

    average_x = 0
    average_y = 0

    for b in closest_snake.body:
        average_x += b.x
        average_y += b.y

    average_x /= closest_snake.length
    average_y /= closest_snake.length

    if abs(new_head.x - average_x) > abs(head.x - average_x) or abs(
        new_head.y - average_y
    ) > abs(head.y - average_y):
        return True

    return False


visited = []
total = 0


def will_die(board, new_head, new_body):
    if new_head in new_body:
        return True
    elif check_out_of_bounds(board, new_head):
        return True
    elif check_snake_collide(board, new_head):
        return True

    return False


def open_cells_recursive(board, head, body, direction):
    global visited, total
    new_head = move_head(head, direction)
    new_body = body.copy()[1:]

    if will_die(board, new_head, new_body) or total > 9 or new_head in visited:
        return

    visited.append(new_head)
    total += 1

    open_cells_recursive(board, new_head, new_body, "up")
    open_cells_recursive(board, new_head, new_body, "down")
    open_cells_recursive(board, new_head, new_body, "left")
    open_cells_recursive(board, new_head, new_body, "right")

    return total


def get_possible_open_cells(board, head, body, direction):
    global visited, total
    visited = []
    total = 0
    return open_cells_recursive(board, head, body, direction)
