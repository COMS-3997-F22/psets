# COMS BC 3997 - F22
# Project Thoughts and Coding Examples

## Timeline
Today is Wednesday December 1st -- we only have this class -- next week M/W the 5th, 7th -- and then our last class is on M the 12th! There is NOT a lot of time left. My suggestion would be to divide and conquer on car building / controlling / understanding and the core computer vision. You can work on both of those independently for now and then we can integrate those together next week.

## The Signs
We will consider one way signs and stop signs (see pages 1-3 of https://github.com/duckietown/signs-and-tags/blob/master/Signs_and_tags_V3.pdf).

## Grading -- your favorite thing!

### Basic Task (18 points)
6 points: Can your car recognize a stop sign (with AR tags) in benign conditions and stop near it more than 50% of the time (3 out of 5 trials)?

6 points: Can your car recognize a stop sign (with no AR tags) in benign conditions and stop near it more than 50% of the time (3 out of 5 trials)?

6 points: Can your car also recognize a one way sign in benign conditions and turn the correct way more than 50% of the time (3 out of 5 trials)?

### Advanced Tasks (2 points)
1 point: Can your car do the basic tasks under some moderately harder conditions? 

1 point: During the basic tasks, does your car stay in its lane and stop very close to the stop sign? Aka is your control good?

### Bonus Points (1 point)
1 point: Is your code and high level approach documented in a README somewhere?

## Controlling the Car
Once we get the hardware going there are stock examples that stay in lanes and can be controlled by your computer. So I think the software pipelines there may basically fully exisist for you (or at least in ways you can copy-paste and adapt). If the folks who are working on the hardware want to collaborate across groups to get the basic examples going and things built that is fine with me.

## Computer Vision
### Non-Learning
**Upload this notebook to Google Colab:** `OpenCVContours.ipynb`. It explores how to use contours to find discrete obejcts in images. This is probably the simplest and most straightforward way to recognize some simple signs (e.g., stopsigns) as you can use a combination of size and shape and color to find things. Note that video is just a stream of images and so if you can solve the problem on images -- then you can solve the problem on video! Also as an aside `opencv` is THE computer vision library so this is useful stuff! :)

### Beyond Contours to Learning
This is where the creativity and real open-ended project-ness comes in! Google is your friend! I've found a lot of possibly useful links by googling things like "stop sign detection neural network python"! Both some super way too advanced things -- and some more simple ones!
