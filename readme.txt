Hey everyone, check out this little project I put together! It's a GUI Python program that helps visualize how a simply supported beam behaves when you put a load on it. 
Basically, it draws the Shear Force Diagram (SFD) and Bending Moment Diagram (BMD) automatically.

Usage:

See diagrams instantly: Just punch in the beam's length, how much weight is on it, and where that weight is located, and BAM! The SFD and BMD pop up right away.

Looks pretty good: I used CustomTkinter to make the interface nice and modern. It feels smooth to use.
It's got your back with inputs: You can't just enter any crazy numbers. It makes sure the load position and size make sense.

Highlights the important stuff: It clearly shows where the load is and where the shear and moment change on the diagrams.

Save crisp images: You can save the diagrams as PNG files, and it even prints the beam details right on the image.

You choose where to save: There's a save button that lets you pick exactly where you want to save the image and what you want to name it.

What I used to build it:
Python 3.11 or newer
Matplotlib (for making the graphs)
NumPy (for some of the math stuff)
Tkinter (the base for the user interface, handling things like windows and button clicks)
