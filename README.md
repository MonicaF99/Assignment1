First Assignment Research Track
================================

This is a controller for a robot in a simulator environment developed by [Student Robotics](https://studentrobotics.org).

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.

You can run the program with:

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
If the wall is on the left it has to turn right, if the wall is on the right it has to turn left.
How does the robot distinguish a wall on the left and a wall on the right?
The first idea is to consider the angle of the nearest golden block, but the robot often takes the wrong direction!
In the figure the robot will turn left, then it will find another wall, it will continue to turn left until it will come back.

![wrongAngle](https://user-images.githubusercontent.com/62377263/141100170-80fe52f6-465b-4df2-8575-d4078afd2e83.JPG)

So, to improve the algorithm, the robot doesn't control the angle of the wall in front of it, but checks the distances of the wall on the left and on the right.
It turns in the direction of the furthest wall. So it makes the curve in the right way.

![Curve](https://user-images.githubusercontent.com/62377263/141103173-22e62bbe-69a4-48b6-acb1-ce8646243552.JPG)

The other problem is to find the silver tokens and move them behind.
The robot has to check if there are silver blocks in front of it.
If it doesn't find a block, it goes on.
If it finds a block, it checks if there are walls between them.
If there is a wall, it ignore the silver token, otherwise it go to catch it.
In the last case the robot doesn't control if there are walls near itself until it releases the block.
When the robot grabs a silver token, it decides in which direction rotate to move the block behind: it checks the distances of the nearest walls on the left or on the right and then decides.

Pseudocode
--------------
```pseudocode
while(True):
 drive for a short time
 if(see a silver token):
  if(there is a wall between the robot and the block):
   ignore the block
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
   turn left until the wall isn't in front of the robot
  else:
   turn right until the wall isn't in front of the robot
```

Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/
