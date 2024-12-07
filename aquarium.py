import curses
import random
import time

# constants 
width = 80
height = 20
num_fish = 5
num_bubbles = 6

def aquarium(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100) # refresh time

    ### build the aquriam elements
    # spawning locations for the fish essentially
    fish = [{"x": random.randint(1, width - 3),
             "y": random.randint(1, height - 2),
             "dir": random.choice(["left","right"])} for _ in range(num_fish)]
    
    # same sort of thing for bubbles, except we want the bubbles to only move upwards
    # this is why 'y' doesn't get a random position placement (they start from bottom)
    bubbles = [{"x": random.randint(1, width - 2),
                "y": height - 2} for _ in range(num_bubbles)]
    
    # this is the build the actual aqurium, like the background and stuff
    # we will also make the fish and bubbles move here
    while True:
        stdscr.clear()

        # plants (i might redesign these eventually)
        for x in range(0, width, 5):
            stdscr.addstr(height - 1, x, "||||")

        # making the actual fish and their movement
        for f in fish:
            if f["dir"] == "right":
                stdscr.addstr(f["y"],f["x"],"><>")
                f["x"] += 1
                # this checks to see how close to the wall the fish is and
                # changes direction if it is too close
                if f["x"] >= width - 3:
                    f["dir"] = "left"
            else:
                stdscr.addstr(f["y"], f["x"], "<><")
                f["x"] -= 1
                # this also checks to see how close to wall but from the
                # other direction for fish moving left
                if f["x"] <= 1:
                    f["dir"] = "right"
            
            # build the vertical movement as well
            f["y"] += random.choice([-1, 0, 1])
            f["y"] = max(1, min(height - 2, f["y"]))
        
        # making the bubbles and their movement
        for b in bubbles:
            if b["y"] > 0:
                # add em to the screen
                stdscr.addstr(b["y"],b["x"],"o")
            # starting spot
            b["y"] -= 1
            # and make em move up
            if b["y"] < 1:
                b["y"] = height - 2
                b["y"] = random.randint(1, width - 3)
        
        # user input (if yk you wanna drop food or some yk)
        key = stdscr.getch()
        # allows user to quit
        if key == ord("q"):
            break
        # allows user to drop food 
        elif key == ord("f"):
            stdscr.addstr(height // 2, width // 2, "*") 

        # keeps refreshing screen to show movements
        stdscr.refresh()
        time.sleep(0.1)
    
# run that bad boy
curses.wrapper(aquarium)
