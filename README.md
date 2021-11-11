First Assignment Research Track
================================

This is a controller for a robot in a simulator environment developed by [Student Robotics](https://studentrobotics.org).

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Once the dependencies are installed, simply run the new_assignment1.py script with the following bash command:

```bash
$ python run.py new_assignment1.py
```

Problem to solve
-----------------------------
The robot environment for this assignment is the following arena:

![robotArena](https://user-images.githubusercontent.com/62377263/141092719-f8607cb9-e30c-4e28-b33e-d73d3bc285a8.JPG)

The robot should:
* move in the circuit in the counter-clockwise direction 
* avoid touching the walls (golden blocks)
* when it finds a silver block on its road, it grabs it and moves it behind itself

Reasoning to solve the problem
-----------------------------------
First, the robot has to avoid collisions with the walls.
So the robot has to drive until it's too close to a wall.
If this wall is on the left it has to turn right, if this is on the right it has to turn left.
How can the robot distinguish a wall on the right from a wall on the left?
The first idea is to consider the angle of the nearest golden block, but the robot often takes the wrong direction!
In the figure the robot will turn left, then it will find another wall, it will continue to turn left until it will come back.
So the first requisite wouldn't be satisfied.

![wrongAngle](https://user-images.githubusercontent.com/62377263/141100170-80fe52f6-465b-4df2-8575-d4078afd2e83.JPG)

So, to improve the algorithm, the robot doesn't control the angle of the wall in front of it, but checks the distances of the wall on the left and the wall on the right.
It turns in the direction of the furthest wall. So it makes the curve in the right way.

![Curve](https://user-images.githubusercontent.com/62377263/141103173-22e62bbe-69a4-48b6-acb1-ce8646243552.JPG)

The other problem is to find the silver tokens and move them behind.
The robot has to check if there are silver tokens in front of it.
If it doesn't find a block, it goes on.
If it finds a block, it checks if there are walls between them.
If there is a wall, it ignores the silver token, otherwise it goes to catch it.
In the last case the robot doesn't control if there are walls near itself until it releases the block.
When the robot grabs a silver token, it decides in which direction rotate to move the block behind: it checks the distances of the nearest walls on the left and on the right and then decides.

Pseudocode
--------------
The reasoning just made can be formalized with the following pseudocode:

```pseudocode
while(True):
 drive for a short time
 
 if(see a silver token):
  if(there is a wall between the robot and the token):
   ignore the token
  else:
   reach it
   grab it
   if(the nearest wall is on the left):
    move the block behind turning right
    release the block
    turn behind
   else:
    move the block behind turning left
    release the block
    turn behind
    
 if(there is a wall in front of the robot too close):
  if(wall on the right is nearest than the wall on the left):
   turn left until the wall is no longer in front of the robot
  else:
   turn right until the wall is no longer in front of the robot
```
Implementation
----------------
The main function of my solution repeats three steps in a loop:
* drive(speed = 50, seconds = 0.1) -> drive for a short time
* go_and_catch_silver_token() -> check if there is a catchable silver token, if the answer is yes the robot goes to grab it and moves it behind itself
* avoid_wall() -> check if there are wall in front of the robot and if there is a wall the robot turns in the right direction

The functions are commented in the new_assignment1.py code, but there are some aspects to emphasize.
The functions find_silver_token() and find_golden_token() have been modified from the original version, so that you can specify as input in which direction and with what width of view to look for tokens.
In this way the two functions are more versatile and can be used for different purposes. In particular, the find_golden_token(direction, amplitude) function can be used to check if there is any wall in front of the robot, on the left (-90°), on the right (+90°) or in the silver token's direction.
The visual amplitude in which the robot search a token is different in the different situations.

The values of the thresholds regarding distances and angular amplitudes have been chosen empirically trying to improve the performance of the robot.


[sr-api]: https://studentrobotics.org/docs/programming/sr/
