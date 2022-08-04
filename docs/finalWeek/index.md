# Teamprojekt RoboArena
## Final Week

| Team 2 |
| ----------------- |
| Lukas Reutemann   | 
| An Trieu          | 
| Lasse Niederkrome |
| Leonard Zieger    |

**How it began:**
  - We started planning how we want our game to look and feel
  - We thought about how we can manage our workflow and work efficiently
  - We also needed to start with a solid base for everything we want to code:
  
  *These are our first sketches for the Menu and a level of the game:*
  ![image](https://user-images.githubusercontent.com/72664329/181482252-07d7fcf4-9f6c-44cc-a0e5-12ec4e9c491f.png)
  
  ![image](https://user-images.githubusercontent.com/70483582/168475373-8e8e9804-520c-4c74-84a8-61d34c1bd05b.png)
  
  
  
  *After that, we focused on our first experience drawing and moving a circle with PyQT:*
  ![1](https://user-images.githubusercontent.com/72664329/181482500-387cd313-58d2-48cb-85be-eeaaa1528ddf.gif)



**Workflow:**

We also thought about a general way of structuring our project. We used a scrum-like system, where we met once a week and discussed our project. We shared our custom-progress with each other and also distributed our tasks for the next meeting. For that, we used gitHub-"Project". 
![171641815-9ae9b427-112c-4adf-864a-72e2b1653eb2](https://user-images.githubusercontent.com/70483582/181487545-c49738f1-2224-4787-a8af-f70505ea54f8.png)

To create maps efficiently, we implemented a map-editor, which saves the maps as .JSON -files. This is a short exmaple of a .JSON-File and our first 2 maps that we created. Another big change was the implementation of a basic-Movement function, which allowed us to move across the map.

![171642081-3715ea69-aa58-4b82-a11b-bb214627906c](https://user-images.githubusercontent.com/70483582/181487539-e7d6a611-e801-4a2e-8461-9ee53598c06e.png)

![171627386-373bccd1-26c9-4f97-a0e6-97b5cec75098](https://user-images.githubusercontent.com/70483582/181487565-332681ee-62dc-4e02-80ea-1b1615b518cb.png)

![171643269-1b180567-3a04-4dda-850f-a341294e2f45](https://user-images.githubusercontent.com/70483582/181487572-4e7dcfae-0b0d-448d-94da-0af0c98c9ff1.gif)

After this, we designed a our Main-Menu. At this step, you could ony use "Start Game" and "Map Editor", but it felt way better having a decent Menu-Screen than just starting the game directly.
![175298864-811295f2-d46f-40ea-845c-69e33d713c99](https://user-images.githubusercontent.com/70483582/181487585-6b199ff2-e23f-45fd-baf8-520fc4baea37.png)


Adding Textures was also a big step, because it changed the whole feel of the game to another level. For this, we created different tiles with different textures, which you could then use in the Map-Editor to create your own maps and load them into the game.
  <video src="https://user-images.githubusercontent.com/70483582/175304746-e3736f6a-d2d2-4758-b867-1b6c8850c1bb.mp4" controls="controls" style="max-width: 500px;"> </video>
  
 We also wanted to add some flavour to the game, so we decided to implement Powerups and the shooting-mechanic. Until now, there where only Speedpowerups and the bullets had no collision, but it was a big step to the final game. 
![176688723-3f9803f2-8014-4535-bcd3-27f4aca5879e](https://user-images.githubusercontent.com/70483582/181487930-7abf8008-d1b5-407e-bab6-9e7ce4229916.gif)
![176689807-38c6d65a-e6bc-4173-95c7-010aa0bec3b1](https://user-images.githubusercontent.com/70483582/181487945-591474cf-cf8b-4304-9c7b-6d8196d124eb.gif)


We decided to change our Tile-Size from 10x10 to 25x25 pixels.
![178989409-e085ecc1-bdc8-4649-8e80-e1fdda294d34](https://user-images.githubusercontent.com/70483582/181487983-0a3018cc-8ca2-409b-b756-327af9fd049b.png)

At this stage, we needed to make the AI stronger, so we decided to implement a pathfinding-algorithm to move to the current player-location.
For this purpose, we used iGraph to create a graph of the map, which then can be used by the AI-Robots to know where they can go.
![178823922-b1893f55-a244-45b9-828a-575a6b1f659b](https://user-images.githubusercontent.com/70483582/181488003-94162d34-4267-40a1-beb2-59355070656b.png)
![178822579-9c9e48ef-3835-4a7d-8d85-82f624686958](https://user-images.githubusercontent.com/70483582/181488008-12259948-d097-4108-a46b-07663627437f.png)

Added a FPS-Counter:

![178991653-e35ac8c8-59a7-4237-b4e6-b8cc41ef8deb](https://user-images.githubusercontent.com/70483582/181488021-5fea3ee8-5ce2-449f-aee5-c807c7720661.gif)

**Final polishing:**
- We reworked the Map-Editor and added a small GUI which can be deactivated by pressing Spacebar. Also, there a new Tiles available. 
![Screenshot 2022-07-28 125538](https://user-images.githubusercontent.com/70483582/181489187-44fc7d18-90f9-4fc6-ab04-8118c9ae38c4.png)
- We added more Sounds using AbletonLive, e.g. explosion-sound, shooting-sound, ...
- We added a few new Powerups (heal, red), (rapidfire, green), (speed, yelllow): 

![healPowerup](https://user-images.githubusercontent.com/70483582/181506656-7fea4964-897e-48ac-8a46-74160ee829a2.png)
![rapidPowerup](https://user-images.githubusercontent.com/70483582/181506672-bf4c9347-5d8c-4bc1-9ae3-9759c2c82e8f.png)
![speedPowerup](https://user-images.githubusercontent.com/70483582/181506638-e0ce2b2d-ed04-4868-a1cc-d4a07183eb62.png)
- We added a new Pixel-Style font which suits the general aesthetic of our game better.
- We created a small gif for the MainMenu with AdobePremiere.
![ezgif com-gif-maker (10) (1) (1)](https://user-images.githubusercontent.com/70483582/181491411-40e81001-836f-4955-9291-6225603456f3.gif)

**UML Class Diagram:**

![Roboarena](https://user-images.githubusercontent.com/72664329/181833610-9d7cfb05-6f19-482c-b7ac-2cf542c57dcb.svg)

**UML Sequence Diagram:**

![Roboarena_Sequence_final](https://user-images.githubusercontent.com/70217976/181519519-54ecdcd0-7c68-46db-b0c5-ea48730c917f.jpg)

**General difficulties:**
- PyQT 
- github
- python
- Collision + Hitbox
- Thread-Implementation


**Conclusion:**

Overall, we all agree that this was a really fun and challenging Project.
We learned a lot about:
-  programming in general
-  gitHub and Git!
-  structuring a project and working as a team 
-  time-management 



**Finished Game**



Here are 2 impressiones of the finished game: 

- This is the normal game-loop. You can start a game with different settings and maps.
<video src="https://user-images.githubusercontent.com/70483582/182848471-44759665-44d1-4da9-bc67-da58b318579a.mp4" controls="controls" style="max-width: 500px;"> </video>

- This is our map creator. As you can see, you can create maps easily, which than can be imported to the game.
<video src="https://user-images.githubusercontent.com/70483582/182848746-64be77af-ffbd-4d63-86f5-2fe38f3778ca.mp4" controls="controls" style="max-width: 500px;"> </video>
