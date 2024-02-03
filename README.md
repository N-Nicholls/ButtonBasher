# ButtonBasher
Button Basher is a game written in python using pygame, serving as an introduction for
myself into pygame and a refresher for python. The premise being: you take control of
a character in a selection of levels and have to activate randomly placed buttons around 
the map before a timer gets to zero. As time goes on random events happen which make the 
game harder, such as by adjusting the game rules (gravity, input selection) or by creating
hazards (enemies, lava, etc). You can also upgrade your character to improve your chances
of survival.

## Todo
- Base Features
    - adaptable resolution, speed, framerate
    - transparency for rendered objects
    - Game class
    - Game scene class
    - level mask parser
        - level file format
- Objects (static)
    - liquid base class
        - lava
        - water
        - honey
    - ladders
- Objects (Scene)
- Objects (dynamic)
    - doors
    - buttons
    - elevator
- UI
    - timer
    - status effect counter
- Updates Existing
    - directional conveyor belts (sideways)
- Char features
    - wall jump, double jump, hold wall

Todo: (extra)
- Vector based movement (pos, vel, acc)
- streamlined physics system 
- modularized effects system (see vectors)
- update documentation:
    - remove/change useless code
    - standardize convention
    - adopt standardized documentation
    - customizeable controls, not hard coded
    - movement ability separate from player (multiplayer later)