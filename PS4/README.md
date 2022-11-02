# COMS BC 3997 - F22
# PS4: Perception, Mapping, and Localization
* Due: 11:59pm, Monday November 14th

In this assignment, you will implement a particle filter, explore computer vision and work through written questions on perception, mapping, localization, and some leftover concepts from planning and control that didn't make it onto the last assignment.

# Written Assignment (28 points + 2 Bonus Points)

Please go to the PDF in the written folder for the written instructions.

Problem 1: (Optimal) Control and Planning Concepts (5 points)

Problem 2: Optimal Control (3 points)

Problem 3: Filtering (7 Points + 2 Bonus)

Problem 4: Computer Vision (10 points)

Problem 5: Computer Vision Experiment (3 points)

# Coding Assignment (6 points)
**You must submit to gradescope to get credit for the assignment --- make sure you submit the required files before the deadline!**

**NOTE: You need to install pygame for the visuals to run: `pip3 install pygame`**

## Particle Filter (6 points)

In this section, you'll be finishing an implementation of a particle filer. All code can be found in the `particle_filter` folder. Your goal will be to implement several functions in `util.py`.

**Files you'll want to read:**
`particleFilter.py` The main loop and graphics
`pointMass.py` 		Defines a series of (very useful) helper functions related to the robot we are working with. (a point mass that moves in 2D)

**Files you'll edit (and thus submit to Gradescope for Autograding):**

`util.py` 	Where all of your helper functions will go.

### Part 1 - Adding Noise
Throughout the particle filter noise is often added to ensure that the distribution doesn't collapse (aka that you don't resample to one simple point which is likely not exactly correct) and to take into account that the real world measurements and motions are noisy.

We will do this by adding Gaussian noise (aka mean 0 and standard deviation of TBD) to the output of the motion and sensor models and to the resulting particle locations after resampling.

Note that all inputs (and ouputs) are arrays of floats and that `random.gauss(mean,stdDev)` will return a single random sample from a guassian distribution.

Functions that should be filled in for full credit in the `util.py` file are:
* `addProccessNoise` - 1 point
* `addSensorNoise` 	 - 1 point
* `addResampleNoise` - 1 point

### Part 2 - The Motion and Sensor Models
Now that we can correctly add noise to our measurements and motion we need to actually implement those measurements and motion. The good news is like with the last problem set, these functions are usually unique per robot. As such the `robot_object` again defines helper functions that will do most (if not all) of the heavy lifting for you!

Hint: a sensor reading score might be a good value to use for a weight!

Functions that should be filled in for full credit in the `util.py` file are:
* `applyMotionModel` - 1 point
* `computeWeight`  	 - 1 point

### Part 3 - Resampling
Finally, you'll need to finish off the resampling step. You'll take in an array of particles and an array of their associated weights and you'll need to return an array of new resampled particles. We'll use weighted sampling on the current particles to compute the new particle array.

Hint: You'll want to return the same amount of particles as you are passed in!

Hint 2: Python random may have a function that does weighted sampling for you!

Functions that should be filled in for full credit in the `util.py` file are:
* `getNewParticles` - 1 points

### Part 4 - Explore
Now that you have a working particle filter, change the amount of particles and landmarks in the `runParticleFilter.py` file. What happens? Run it a few times. Can you see why we may want a lot of particles to get an accurate estimate. Can you see how the better samples are weighed more during re-sampling and how the distribution converges on the real value? Can you imagine better ways to do the resampling to converge fully to the true state?