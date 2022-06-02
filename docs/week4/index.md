# Teamprojekt RoboArena
## Week 4

| Team 2 |
| ----------------- |
| Lukas Reutemann   | 
| An Trieu          | 
| Lasse Niederkrome |
| Leonard Zieger    |


what we did this week:

Created a MapCreator for creating map files
- You can switch between different tiles with the number keys 1-6 (for now)
- You can increase and decrease the size (number of Tiles) you are placing with the up-/ down-arrow.
- By pressing "S" you can save the map and choose a name for it
- The map is stored in a .json file

- For now the MapCreator is a different programm than our main-programm (RoboArena.py) but we want implement it
  in the main menu.


Created 2 Maps with the MapCreator:
- ![image](https://user-images.githubusercontent.com/72664329/171627386-373bccd1-26c9-4f97-a0e6-97b5cec75098.png)
- ![image](https://user-images.githubusercontent.com/72664329/171627493-6eb94e27-cbac-4dd0-8c61-bd12d077b0e2.png)


Created a Player-Movement-Function
- You can now controll a BasicRobot
- There are 8 possible directions right now


Created a Ai-Robot-Class
- spawns 3 robots in each corner of the map
- no movement right now (in progress)


Add simple colission Detection
- Still very buggy
- Idea to increase Tile size minimize complexity of colission



