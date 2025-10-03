# [H19_project3_jrevense_siljejka](https://github.uio.no/IN1910/H19_project3_jrevense_siljejka)

Assignment for IN1910 Fall 2019. In this assignment we created two classes forming fractals from sets of mathematical rules, and one class for performing non-linear transformation on the resulting figure.

## Triangle

Chaos Game variation restricted to an equilateral triangle.

## Chaos Game

A class which initialises with an equilateral n-gon and a factor r. Once the n-gon is initialised you can generate a random starting point, and then use this to iterate through randomly chosen points. These random points are chosen by picking a random corner in the n-gon, then moving towards it by a factor r of the distance to the corner from the current point.

### Test

The first two tests finds the function of the lines through the corners of an n-gon, then for each line determines from the y-intercept whether a point within the n-gon should go above or below the line. The tests then checks whether the starting points or iterated points of the final figure are on the right side of the lines, and therefore within the n-gon.

The third test checks that the n-gon is equilateral and centered around the origin.

The fourth test checks that errors are raised when values are out of range.

### Iterate fast

Iteration function compiled using numba greatly improving speed.

### Animate Chaos Game

Class which animates the transition between a chaos game performed on an n-gon for different values of r.

## Fern

Contains two classes. First, AffineTransform which initialises with a transformation matrix, then when called performs this transformation on a 2D-vector. Secondly, Fern which calls AffineTransform for a set of functions and assigns a probability to them, letting us create a shape based on multiple AffineTransformations on a point.

### Fern Fast

Jitted version of the Fern class which improves speed.

## Variations

Takes in a data set, then allows you to perform multiple transformations on it, using either the method itself or the call. When called with a dictionary containing methods and a factor for each, the sum of the factors being 1, it'll apply a linear combinations of the transformations.

### Animation

Allows you to animate a figure using either an Ax -> Bx or Ax -> BAx transformation, going from one variation to another combination. This method allows you to go through a series of multiple variations.

### Issues

We don't think the spiral variation looks correct, but we can't find what's incorrect in our implementation.
