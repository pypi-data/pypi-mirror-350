"""
Imagine a video with fps = 30 and that lasts 1
second. That means that the video has 30 frames
and that each frame duration is 1 / 30 = 0.03333.

The frame times are the next:
frame 0: [0, 0.0333333) -> First frame
frame 1: [0.033333, 0.0666667)
...
frame 28: [0.933333, 0.966667)
frame 29: [0.966667, 1.0) -> Last frame

So, considering the previous details and a 't'
variable that is a specific time moment within
a video, when t=0.01, as you can see, the
interval hits the frame 0 because 0.01 / 0.03333
= 0, but when t=0.04, the interval hits the frame
1 because 0.04 / 0.03333 = 1.

When working with python, floating points and 
periodic numbers, we have to consider that we can
obtain results like 0.3333333333333326, which is
actually lower than 0.3333333333333333 due to
a bad precision, so when we do the division the
result will be wrong. We will use a small amount
we add in any situation to make sure we avoid
those errors when calculating something related
to a 't' time moment.
"""