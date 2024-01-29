# ButtonBasher
Button Basher is a game written in python using pygame, serving as an introduction for
myself into pygame and a refresher for python. The premise being: you take control of
a character in a selection of levels and have to activate randomly placed buttons around 
the map before a timer gets to zero. As time goes on random events happen which make the 
game harder, such as by adjusting the game rules (gravity, input selection) or by creating
hazards (enemies, lava, etc). You can also upgrade your character to improve your chances
of survival.

## Works Used

https://www.pygame.org/project-Rect+Collision+Response-1061-.html
- I used the rect collision response game to learn how to implement accurate and (hopefully) 
 performance efficient collision detection. I also borrowed the idea of formatting the level 
 in an array to speed up level design.
https://realpython.com/pygame-a-primer/
- I used this guide as an introduction to pygame. The first iteration of the game was
 functionally identical to what is in this guide, which defined movement, object + sprite
 placement, and the general gameplay loop.

## Disclaimer (Surely not real legal protection)
Note: This project serves only as a personal tutorial and offers no financial gain to myself
or anyone involved. All respective work used will be obviously documented if used.


## Current problems
Should sprite groups be defined globally or in the main?
Should objects be added to the sprite group on initialization?
- How to handle removal from sprite group

## Todo
level designer (dev only)
- choose a data type (array?)
- Gridlike placement (32x18), * 60 for full resolution
- parser
blocks
- Fall-through platforms
- ladders
- water
- doors
timer
- reads
- resets
- moves
buttons
- random placement
- hitbox
- directional input
objects
