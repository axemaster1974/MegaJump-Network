# MegaJump-Network

MegaJump Network is a platform game written in python using pygame.

You control a ball and the simple goal is to jump on all the platforms in the quickest time possible, apart from "INSANE" mode, where the object is just to jump on as many platforms as you can (jump on all 100 platforms to become MegaJump Champion!).

You can select the platform size (EASY, MEDIUM, HARD) which changes the width of the platforms. You can also change the game size, which changes the number of platforms (SMALL = 10, MEDIUM = 15, LARGE = 20, MEGA = 50) and also the window size.

Each level is randomly generated, so no two levels will be the same. Some levels may appear to be impossible, but virtually all can be completed (there may be the odd "impossible level", but remember your Megajump!)

The controls are:-

Space to jump (+ down arrow for small jump, M for MegaJump) - Only 1 MegaJump per game!
Left & Right arrows to move (+ up arrow to move faster)
Q to quit, R to reset, Function keys to change background & sound (F1-F5 changes background, F6-F10 changes music)
P to toggle music on/off

(NOTE: There is a "feature", which was originally a bug, but which I kept as it actually allows you complete levels that may otherwise be impossible. If you jump on a platform and keep moving, when you fall off, you can let go of the left or right key and you will drop straight down. However if you stop on the platform, then fall off, you will fall off sideways)

The game allows you to save levels so you can replay them and try to beat your best time (save file is gameSaves.txt). You can share this file with friends and therefore play the same levels and try to beat each others time.

There is also the ability to play against an opponent on a LAN via "Network Play" and compete to see who can finish the level first. One player should select "Host Game", and he or she is in charge of game selection. The other player selects to "Connect to Game" and should enter the IP address of the host (you need to ensure firewall rules allow Megajump to connect to the host on port 50107)

The project uses the pygame library (it also uses pyglet but this was purely for the clock timer, as I found this resulted in smoother play the the pygame one).

Hope you enjoy playing MegaJump!

