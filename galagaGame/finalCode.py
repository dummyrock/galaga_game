from dataclasses import dataclass
from random import randint
from designer import *

SHIP_SPEED = 10
ALIEN_SPEED = 5
HIGHEST_SHIP_HEIGHT = 300
LASER_DROP_SPEED = 15

@dataclass
class ShipData:
    ship_speedx: int
    ship_speedy: int
    ship_moving_x: bool
    ship_moving_y: bool
    far_left: bool
    far_right: bool
    too_high: bool
    too_low: bool

@dataclass
class Inputs:
    up_key: bool
    down_key: bool
    left_key: bool
    right_key: bool
    
@dataclass
class GameDifficulty:
    easy: list[int]
    medium: list[int]
    hard: list[int]

@dataclass
class LevelInfo:
    level_row: int
    level_main: int
    
@dataclass
class World:
    ship: DesignerObject
    ship_data: ShipData
    inputs: Inputs
    levels: list[list[list[str]]]
    lasers: list[DesignerObject]
    aliens: list[DesignerObject]
    level_info: LevelInfo
    difficulty: GameDifficulty
    lives: int
    counter: DesignerObject
    lives_counter: list[DesignerObject]
    
def edge_of_screen(world: World):
    """
    Initializes flags based on ship's position concerning the screen edges.

    Args:
    world (World): The current state of the game world.
    """
    if world.ship.x <= 0:
        world.ship_data.far_left = True
    elif world.ship.x >= get_width():
        world.ship_data.far_right = True
    else:
        world.ship_data.far_left = False
        world.ship_data.far_right = False
    if world.ship.y <= HIGHEST_SHIP_HEIGHT:
        world.ship_data.too_high = True
    elif world.ship.y >= get_height():
        world.ship_data.too_low = True
    else:
        world.ship_data.too_high = False
        world.ship_data.too_low = False
    
def create_ship() -> DesignerObject:
    """
    Creates the ship object with specific image and initial positioning.

    Returns:
    DesignerObject: The ship object with image, scaled properties, and initial y-position.
    """
    ship = image("galagaShip.png")
    ship.y = get_height() * (1 / 1.5)
    ship.scale_x = .1
    ship.scale_y = .1
    return ship

def create_laser() -> DesignerObject:
    """
    Creates a laser object with a specific image and initial positioning.

    Returns:
    DesignerObject: The laser object with scaled properties and initial y-position.
    """
    laser = image("lazer.png")
    laser.y = get_height() * (1/8)
    return laser

def create_alien() -> DesignerObject:
    """
    Creates an alien object with specific image and initial positioning.

    Returns:
    DesignerObject: The alien object with scaled properties and initial position at the top of the screen.
    """
    alien = image('alien.png')
    alien.scale_x = .1
    alien.scale_y = .1
    alien.x = get_width()/2
    alien.y = 0
    return alien

def create_live_counter_ship() -> DesignerObject:
    """
    Creates a live counter ship object.

    Returns:
    DesignerObject: The live counter ship object with scaled properties and initial position at the bottom of the screen.
    """
    ship = image('galagaShip.png')
    ship.scale_x = .05
    ship.scale_y = .05
    ship.x = 0
    ship.y = get_height() - 25
    return ship

def head_left(world: World):
    """
    Initiates the ship's leftward movement by updating its speed and orientation.

    Args:
    world (World): The current state of the game world.
    """
    world.ship_data.ship_speedx = -SHIP_SPEED
    world.ship.flip_x = False
    
def head_right(world: World):
    """
    Initiates the ship's rightward movement by updating its speed and orientation.

    Args:
    world (World): The current state of the game world.
    """
    world.ship_data.ship_speedx = SHIP_SPEED
    world.ship.flip_x = True
    
def head_up(world: World):
    """
    Initiates the ship's upward movement by updating its vertical speed.

    Args:
    world (World): The current state of the game world.
    """
    world.ship_data.ship_speedy = -SHIP_SPEED
    
def head_down(world: World):
    """
    Initiates the ship's downward movement by updating its vertical speed.

    Args:
    world (World): The current state of the game world.
    """
    world.ship_data.ship_speedy = SHIP_SPEED

def move_ship(world: World):
    """
    Moves the ship horizontally and vertically within screen boundaries.

    Args:
    world (World): The current state of the game world.
    """
    if world.ship_data.ship_moving_x and (world.ship.x >= 0 and world.ship.x <= get_width()):
        world.ship.x += world.ship_data.ship_speedx
    if world.ship_data.ship_moving_y and (world.ship.y >= HIGHEST_SHIP_HEIGHT and world.ship.y <= get_height()):
        world.ship.y += world.ship_data.ship_speedy
        
def move_ship_x_left(world: World, key: str):
    """
    Handles the ship's movement to the left based on key inputs.

    Args:
    world (World): The current state of the game world.
    key (str): The key pressed by the user.
    """
    if world.ship_data.far_right and (key == "a" or key == "left"):
        world.ship.x -= SHIP_SPEED
        head_left(world)
    if (key == "a" or key == "left"):
        head_left(world)
        world.ship_data.ship_moving_x = True
        world.inputs.left_key = False
        
def move_ship_x_right(world: World, key: str):
    """
    Handles the ship's movement to the right based on key inputs.

    Args:
    world (World): The current state of the game world.
    key (str): The key pressed by the user.
    """
    if world.ship_data.far_left and (key == "d" or key == "right"):
        world.ship.x += SHIP_SPEED
        head_right(world)
    if (key == "d" or key == "right"):
        head_right(world)
        world.ship_data.ship_moving_x = True
        world.inputs.right_key = False
        
def move_ship_y_up(world: World, key: str):
    """
    Handles the ship's movement upwards based on key inputs.

    Args:
    world (World): The current state of the game world.
    key (str): The key pressed by the user.
    """
    if world.ship_data.too_low and (key == "w" or key == "up"):
        world.ship.y -= SHIP_SPEED
        head_up(world)
    if (key == "w" or key == "up"):
        head_up(world)
        world.ship_data.ship_moving_y = True
        world.inputs.up_key = False
        
def move_ship_y_down(world: World, key: str):
    """
    Handles the ship's movement downwards based on key inputs.

    Args:
    world (World): The current state of the game world.
    key (str): The key pressed by the user.
    """
    if world.ship_data.too_high and (key == "s" or key == "down"):
        world.ship.y += SHIP_SPEED
        head_down(world)
    if (key == "s" or key == "down"):
        head_down(world)
        world.ship_data.ship_moving_y = True
        world.inputs.down_key = False
        
def stop_left(world: World, key: str):
    """
    Stops the ship's leftward movement based on key release.

    Args:
    world (World): The current state of the game world.
    key (str): The key released by the user.
    """
    if (key == "a" or key == "left"):
        world.inputs.left_key = True
        head_right(world)
        
def stop_right(world: World, key: str):
    """
    Stops the ship's rightward movement based on key release.

    Args:
    world (World): The current state of the game world.
    key (str): The key released by the user.
    """
    if (key == "d" or key == "right"):
        world.inputs.right_key = True
        head_left(world)
        
def stop_up(world: World, key: str):
    """
    Stops the ship's upward movement based on key release.

    Args:
    world (World): The current state of the game world.
    key (str): The key released by the user.
    """
    if (key == "w" or key == "up"):
        world.inputs.up_key = True
        head_down(world)
        
def stop_down(world: World, key: str):
    """
    Stops the ship's downward movement based on key release.

    Args:
    world (World): The current state of the game world.
    key (str): The key released by the user.
    """
    if (key == "s" or key == "down"):
        world.inputs.down_key = True
        head_up(world)

def stop_moving(world: World, key: str):
    """
    Stops the ship's movement when no directional keys are being pressed.

    Args:
    world (World): The current state of the game world.
    key (str): The key that is released.
    """
    if (world.inputs.left_key and world.inputs.right_key):
        world.ship_data.ship_moving_x = False
    if (world.inputs.up_key and world.inputs.down_key):
        world.ship_data.ship_moving_y = False
        
def shoot_laser(world: World, key: str):
    """
    Creates a laser when the space bar is pressed.

    Args:
    world (World): The current state of the game world.
    key (str): The key pressed by the user.
    """
    if key == 'space':
        new_laser = create_laser()
        move_below(new_laser, world.ship)
        world.lasers.append(new_laser)
def move_below(top: DesignerObject, bottom: DesignerObject):
    """
    Move the bottom object to be below the top object.

    Args:
    top (DesignerObject): The top object.
    bottom (DesignerObject): The bottom object.
    """
    top.y = bottom.y - bottom.height / 2
    top.x = bottom.x

def make_laser_move(world: World):
    """
    Move all the laser objects downwards.

    Args:
    world (World): The current state of the game world.
    """
    for laser in world.lasers:
        laser.y -= LASER_DROP_SPEED

def destroy_lasers_uptop(world: World):
    """
    Destroy any laser objects that have landed on the top of the screen.

    Args:
    world (World): The current state of the game world.
    """
    kept = []
    for laser in world.lasers:
        if laser.y > 0:
            kept.append(laser)
        else:
            destroy(laser)
    world.lasers = kept

def sort_aliens(world: World, row: list[str]):
    """
    Arrange alien objects in a row based on the provided list of strings.

    Args:
    world (World): The current state of the game world.
    row (list[str]): The configuration for arranging aliens in a row.
    """
    in_between_alien_length = get_width() / 11
    alien_location = in_between_alien_length
    for x in row:
        if x == "x":
            alien = create_alien()
            alien.x = alien_location
            world.aliens.append(alien)
        alien_location += in_between_alien_length

def check_aliens(world: World):
    """
    Checks the status of aliens and spawns new aliens if needed.

    Args:
    world (World): The current state of the game world.
    """
    can_spawn = True
    for alien in world.aliens:
        if alien.y <= 100:
            can_spawn = False
    if world.level_info.level_row == 4 and (len(world.aliens) == 0):
        world.level_info.level_row = 0
        world.level_info.level_main += 1
        create_level(world)
    if len(world.aliens) == 0 and can_spawn:
        sort_aliens(world, world.levels[world.level_info.level_main][world.level_info.level_row])
        world.level_info.level_row += 1
    elif not (len(world.aliens) == 0) and can_spawn and world.level_info.level_row < 4:
        sort_aliens(world, world.levels[world.level_info.level_main][world.level_info.level_row])
        world.level_info.level_row += 1

def make_aliens_move(world: World):
    """
    Moves all the alien objects.

    Args:
    world (World): The current state of the game world.
    """
    for alien in world.aliens:
        alien.y += ALIEN_SPEED / 2
        if world.level_info.level_main >= world.difficulty.easy[0]:
            alien.x += randint(-5, 5)
        if world.level_info.level_main >= world.difficulty.easy[1]:
            alien.y += randint(-5, 5)

def aliens_too_low(world: World):
    """
    Removes alien objects that have reached the bottom of the screen.

    Args:
    world (World): The current state of the game world.
    """
    kept = []
    for alien in world.aliens:
        if alien.y <= get_height() - 50:
            kept.append(alien)
        else:
            destroy(alien)
            world.lives -= 1
            try:
                world.lives_counter = filter_from(world.lives_counter, [world.lives_counter[len(world.lives_counter) - 1]])
            except:
                pass
    world.aliens = kept

def bounce_aliens(world: World):
    """
    Handles the bouncing effect for aliens off the screen edges.

    Args:
    world (World): The current state of the game world.
    """
    for alien in world.aliens:
        if alien.x > get_width():
            alien.x = 0
        elif alien.x < 0:
            alien.x = get_width()

def alien_hit_ship(world: World):
    """
    Handles collisions between the ship and aliens.

    Args:
    world (World): The current state of the game world.
    """
    destroyed_lives = []
    destroyed_aliens = []
    for alien in world.aliens:
        if colliding(alien, world.ship):
            world.lives -= 1
            destroyed_lives.append(world.lives_counter[len(world.lives_counter) - 1])
            destroyed_aliens.append(alien)
    world.lives_counter = filter_from(world.lives_counter, destroyed_lives)
    world.aliens = filter_from(world.aliens, destroyed_aliens)

def collide_lasers_aliens(world: World):
    """
    Handles collisions between laser objects and alien objects.

    Removes collided lasers and aliens from their respective lists.

    Args:
    world (World): The current state of the game world.
    """
    destroyed_lasers = []
    destroyed_aliens = []
    for alien in world.aliens:
        for laser in world.lasers:
            if colliding(laser, alien):
                destroyed_lasers.append(laser)
                destroyed_aliens.append(alien)
    world.aliens = filter_from(world.aliens, destroyed_aliens)
    world.lasers = filter_from(world.lasers, destroyed_lasers)

def lives_counter(world: World):
    """
    Manages and updates the visual representation of remaining lives.

    Args:
    world (World): The current state of the game world.
    """
    live_space = get_width() / 15
    live_count_space = live_space
    for live in world.lives_counter:
        live.x = live_count_space
        live_count_space += live_space

def filter_from(old_list: list[DesignerObject], elements_to_not_keep: list[DesignerObject]) -> list[DesignerObject]:
    """
    Filters out specified elements from the list.

    Args:
    old_list (list[DesignerObject]): The original list of objects.
    elements_to_not_keep (list[DesignerObject]): The objects to be removed from the list.

    Returns:
    list[DesignerObject]: A new list without the specified elements.
    """
    new_values = []
    for item in old_list:
        if item in elements_to_not_keep:
            destroy(item)
        else:
            new_values.append(item)
    return new_values

def create_level(world: World):
    """
    Generates a new level configuration.

    Args:
    world (World): The current state of the game world.
    """
    level = []
    row = []
    for rows in range(4):
        for letter in range(5):
            ship_or_not = randint(0, world.difficulty.easy[2])
            if ship_or_not == 1 or ship_or_not == 2 or ship_or_not == 3 or ship_or_not == 4:
                row.append("x")
            else:
                row.append("")
        level.append(row)
    world.levels.append(level)

def update_score(world: World):
    """
    Updates and displays the game score.

    Args:
    world (World): The current state of the game world.
    """
    world.counter.text = "Score: " + str(world.level_info.level_main) + " Lives: " + str(world.lives)

def game_over(world: World):
    """
    Checks for the game over condition based on remaining lives.

    Args:
    world (World): The current state of the game world.

    Returns:
    bool: True if the game is over, False otherwise.
    """
    if world.lives <= 0:
        for alien in world.aliens:
            destroy(alien)
        for laser in world.lasers:
            destroy(laser)
        destroy(world.ship)
        world.counter.y += 200
        world.counter.text = f"GAME OVER! You got up to level: {world.level_info.level_main}"
        return True

def create_world() -> World:
    """
    Initializes the game world with default values.

    Returns:
    World: The initial state of the game world.
    """
    ship_data = ShipData(SHIP_SPEED, SHIP_SPEED, False, False, False, False, False, False)
    inputs = Inputs(True, True, True, True)
    level_info = LevelInfo(0, 0)
    difficulty = GameDifficulty([10, 15, 2], [8, 12, 4], [6, 9, 6])
    levels = [
        [['', '', 'x', 'x', 'x', 'x', 'x', 'x', '', ''],
         ['', '', '', 'x', 'x', 'x', 'x', '', '', ''],
         ['', '', '', '', 'x', 'x', '', '', '', ''],
         ['', '', '', '', '', 'x', '', '', '', '']],
        [['x', '', '', 'x', 'x', 'x', 'x', '', '', 'x'],
         ['', 'x', '', '', 'x', 'x', '', '', 'x', ''],
         ['', '', '', 'x', '', '', '', 'x', '', ''],
         ['', '', '', '', 'x', 'x', '', '', '', '']],
        [['', '', '', '', 'x', '', '', '', '', ''],
         ['', '', '', 'x', 'x', '', '', '', '', ''],
         ['', '', '', 'x', 'x', '', '', '', '', ''],
         ['', '', '', '', 'x', 'x', '', '', '', '']],
        [['', '', '', '', 'x', '', '', '', '', ''],
         ['', '', '', 'x', 'x', '', '', '', '', ''],
         ['', '', '', 'x', 'x', '', '', '', '', ''],
         ['', '', '', '', 'x', 'x', '', '', '', '']]]
    return World(create_ship(), ship_data, inputs, levels, [], [], level_info, difficulty, 3,
                 text("white", "Score", 25, get_width() / 2, 100),
                 [create_live_counter_ship(), create_live_counter_ship(), create_live_counter_ship()])

background_image("nightSky.jpg")
when('starting', create_world)
when('updating', edge_of_screen)
when('updating', move_ship)
when('updating', stop_moving)
when("updating", make_laser_move)
when('updating', destroy_lasers_uptop)
when('updating', check_aliens)
when('updating', make_aliens_move)
when('updating', aliens_too_low)
when('updating', bounce_aliens)
when('updating', update_score)
when('updating', lives_counter)
when('updating', alien_hit_ship)
when('updating', collide_lasers_aliens)
when("typing", move_ship_x_left)
when("typing", move_ship_x_right)
when("typing", move_ship_y_up)
when("typing", move_ship_y_down)
when("typing", shoot_laser)
when('done typing', stop_left)
when('done typing', stop_right)
when('done typing', stop_up)
when('done typing', stop_down)
when(game_over, pause)
start()