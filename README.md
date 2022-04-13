![](https://github.com/Ahmad791/Virtual-whiteboard/blob/master/media/20220412_140352.gif)


How to run:
1. Make sure you pc is connected to an external display (projector).
2. run main.py
3. point your PC camera at the projected screen, when the camera detects the displayed white screenwith black 
borders (green triangle around it) press q.
note: if camera not detecting screen try turning off the lights.
4. place your hand on the board for 5 seconds, (when a blue dot appears on your index you can start writing).
note: if your camera is not close to the center then place your hand at the farthest point from the camera
(on the board)
5. place your index on where you want to write and twist your hand to start writing.
6. hold your hand like a fist and twist it to erase.
note: try to make the camera as close to the center as possible for best performance and accuracy.

What's in the code:
First the code detects the board by displaying white screen with black borders (in detectBoard.py), then make
the picture black and white (white is white and black for everything else), find shapes and then pick the 
largest one make a green border around it, then let the user pick the board. When he does make a transformation
matrix (perspective transformation matrix).

Next we need the board distance to know when the user is writing, since we can't do that with one camera we make 
the user put his hand on the board to measure the width of his hand in pixels, then we can measure distance 
in relation to that, more pixels means closer to the camera (When the user twists his hand the code thinks
the distance of the hand is larger than the board so we used that for interacting with the board). 

Now the code keep checking the hand distance and if he's writing or erasing and sending it to the board.

The board gets the hand position and if user is writing or erasing. The code saves a mask (matrix) in 
black and blue which is the one the user actually writes on. It acts just like a blackboard, when the user 
writes it puts a blue line on it but when the user erases it puts a black one, then put the board on top of 
the screenshot, if blue display the board, if black display screen.
note: The code uses the transformation matrix to get the exact index location on the board.
note: color white not blue for now.

note 1: The current version does not work on mac, we are working on it.
note 2: We recommend using at least 1080p camera because it's hard to detect hands using lower resolution cameras
