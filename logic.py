# Move logic

import objects as battle_objects
import random

def make_move(board, you):
    best_move = None

    if you.health < 50:
        best_move = find_best_next_space(board, you, True)
    else:
        best_move = find_best_next_space(board, you)

    return best_move

def find_best_next_space(board, you, need_food=False):
    best_move = None
    best_move_score = 0

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
                move_score -= 50
        elif new_head in board.hazards:
            move_score -= 100
        elif new_head in new_body:
            move_score -= 100
        elif check_out_of_bounds(board, new_head):
            move_score -= 100
        else:
            move_score += 1
            if moved_away(you.head, new_head, you.body):
                move_score += 1

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

def moved_away(head, new_head, body):
    average_x = 0
    average_y = 0
    
    for b in body:
        average_x += b.x
        average_y += b.y
    
    average_x /= len(body)
    average_y /= len(body)

    if abs(new_head.x - average_x) > abs(head.x - average_x) or abs(new_head.y - average_y) > abs(head.y - average_y):
        return True

    return False
