# ButtonBasher
Button Basher is a game written in python using pygame, serving as an introduction for
myself into pygame and a refresher for python. The premise being: you take control of
a character in a selection of levels and have to activate randomly placed buttons around 
the map before a timer gets to zero. As time goes on random events happen which make the 
game harder, such as by adjusting the game rules (gravity, input selection) or by creating
hazards (enemies, lava, etc). You can also upgrade your character to improve your chances
of survival.

## Todo
- Objects (static)
    - lava
- Objects (Scene)
    - textures 
- Objects (dynamic)
    - doors
    - buttons, textures, direction, framerate
    - elevator nodes
    - enemies (toad)
    - enemies (mimic)
    - enemies (shooting)
    - enemies (roblox zombie)
    - enemies (slimes)
        - effects, block layers
- UI
    - timer
    - status effect counter
- Extra
    - sound effects
    - music track
        -dynamism
- Char features
    - wall jump, double jump, hold wall
- scenes
    - main menu
    - pause menu
    - settings

Todo: (extra)
- update documentation:
    - adopt standardized documentation (doxygen?)


Pros/Cons to having gibs as composition function of levelState:
- Pros:
    - Allows it to be a physChar, meaning we can reuse physics functions
    - Separate from object its being called by, meaning we can reuse the effect for anything. 
        - set precedent for effects later on. 
- Cons:
    - Will need to rewrite gibbed function (not gibbed class) for each state, but this gives us more control
    - Not tied to object, exists on its own
