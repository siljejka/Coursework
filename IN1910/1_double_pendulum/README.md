# [H19_project1_jrevense_siljejka](https://github.uio.no/IN1910/H19_project1_jrevense_siljejka)

Assignment for IN1910 Fall 2019. In this this assignment we solved two systems, a single and a double pendulum system, and animated the double pendulum system.

# Exponential Decay

The first part of this project has us make a class to compute exponential decay, the class is found in `exp_decay.py` and a simple function to test it can be found in `test_exp_decay.py`.

We make a simple `__call__` method, and then make a `solve` method which uses SciPy's `solve_ivp` method, to solve an initial value problem.

After the `if __name__=="__main__"` block of the program we make an instance of the class, solve it for an initial value of 100, and then plot results with different decay rates, to check our work.

# Pendulum

The second part of this project has us make a class to represent a pendulum hanging from a fixed point, we make several simplifications in our model by ignoring air resistance and hinge friction, but we still take into account gravity. The class can be found in `pendulum.py`, the tests made for the class can be found in `test_pendulum.py`.

We make a `__call__(t, u)` method which takes in t<sup>[1](#footnote1)</sup>, and the pendulums current position &theta;<sub>i</sub> and velocity &omega;<sub>i</sub>, and returns d&theta;<sub>i</sub>/dt and d&omega;<sub>i</sub>/dt.

We then make a `solve(y0, T, dt, angles)` method which takes in our initial values y0 = [&theta;<sub>0</sub>, &omega;<sub>0</sub>], the total time to solve the problem for T, the time step to solve it for dt, and finally a string angles, which has to be either "rad" or "deg", to indicate whether y0 has been input in radians or degrees.

The `solve` method then utilises SciPy's `solve_ivp` method to solve our initial value problem with `self.__call__` as our function `fun`, (0,T) as our timespan `t_span`, y0 as `y0`, self.method as `method` and the time points to evaluate the ivp `t_eval` is a linspace from 0 to T, with (T/dt)+1 values.

The values `solve` calculates are not returned by the function call, but stored locally in the class instance. These values can be overwritten by later calls to the `solve` method.

After the `solve` method was finished, we made the calculated values for t, &theta; and &omega; into properties of the class using the `@property` tag. And made a new method `check_run`, which checks if a bool in the class instance called `self._Solver_Run` is `True`, if this is not the case it raises an `AttributeError` with the message "Solver not run".

Then we added new properties translating from the polar coordinates we had solved the problem for, into cartesian coordinates. This was done to make it easier to plot the pendulum path using PyPlot.

After this we also added properties which calculated the potential and kinetic energy of the pendulum.

After the `if __name__=="__main__"` block of the program we made an instance of the class, solved it for an initial values problem and made plots of the results to check our work.

We did notice that if we used the method `"RK45"` we had a slight drop in the total energy over time, this is due to the imperfect nature of the `"RK45"` integration method. We tested it with `"radau"` and it seemed to work better.

Lastly we made a new class `DampenedPendulum` which inherited everything from the `Pendulum` class, but added a dampening factor B. We modified the `__call__` method to account for this dampening factor.

# Double Pendulum

In the third part of the project we are adding a second pendulum to the mix, this pendulum is attached to the first and now we have to account for their interaction too. Gravity is accounted for naturally, air resistance and hinge friction is still ignored to make our lives easier.

Now we had to expand the `__call__` method to accept four values, [&theta;<sub>(1,i)</sub>, &omega;<sub>(1,i)</sub>, &theta;<sub>(2,i)</sub>, &omega;<sub>(2,i)</sub>]. The `__call__` method then solves four coupled ODE's and returns [d&theta;<sub>(1,i)</sub>, d&omega;<sub>(1,i)</sub>, d&theta;<sub>(2,i)</sub>, d&omega;<sub>(2,i)</sub>]. We were simply given these ODE's, because the focus of this project is the programming and not the mathematics.

To make our lives easier we poured over the equations and looked for ways to simplify it, we found some values that kept popping up in the equations and made them into "constants for this call of the method".

We then split the equations for &omega;<sub>1</sub> and &omega;<sub>2</sub> up into numerators and denominators, called `num1`, `den1`, `num2` and `den2`, this made it possible for us to write our equations out in an easy to read way, and use multiline by encapsulating it all in brackets.

The `solve` method in DoublePendulum is practically identical to the one in Pendulum, the only thing that is different is that we are saving more variables.

Again we made properties translating from the polar coordinates we had solved for, into cartesian coordinates. For the second pendulum we did the same translation as the first pendulum, but we also added the x and y coordinates of the first pendulum, to put it in the correct place.

Again we also added properties for the kinetic and potential energy. We chose to make 6 properties, one for the potential energy of the first pendulum, one for the potential energy of the second pendulum, and one for the total potential energy of the system, the same for kinetic energy.

Again after the `if __name__=="__main__"` check in our code, we made an instance of the class and made plots of pendulum paths, and energies to check our work.

# Animating the Double Pendulum

For the fourth and final part of this project, we were tasked with making an animation of our work. We chose to implement this by making a new file called `animate_double_pendulum.py`, importing the DoublePendulum class into it and making a new class.<sup>[2](#footnote2)</sup>

This new class inherited all of DoublePendulum's functionality and then added the methods to make the animations, we chose to do it this way to keep our code neat and organised. Since the DoublePendulum class was just shy of 200 lines of code, this seemed to be a better solution in our minds.

We then decided on some parameters to use for setting axis behaviour, size and limits. We made a method `init_frame` which initialises the figure the animation will be put in, with axis and limits defined by the aforementioned parameters. We had a parameter `axis_lim` where you could define your own x and y limits, but we found it more rewarding to use the `auto_lim` parameter. The `auto_lim` parameter is a boolean, and if it is set to `True`, the `init_frame` method tries to set the frame up with appropriate x,y limits, based on the highest/lowest x and y coordinates the second pendulum reached.

Then we made the `create_animation` method, which uses `init_frame` to initialise the figure, sets up "empty" `self.` variables using PyPlot's `.plot([], [], **kwargs)`, and then creates the animation with PyPlot's `FuncAnimation` method.

After this we made the function which draws the i'th frame, called `_next_frame(i)`, and set it up so it updated the positional data in our animation to the i'th datapoint.

Finally we made the `show_animation` method which used PyPlot's `.show()` to show it, and the `save_animation` method which saves the animations as an mp4 file.

## Additional challenge

We decided we wanted to give the additional challenge a try, so we added a boolean parameter to the constructor called `inc_trace`, which was by default set to false.

We then made an extra `_next_frame(i)` method called `_next_frame_trace(i)`, which was basically a copy of `_next_frame(i)`, but it also updated `self.trace_1` and `self.trace_2`. We implemented this by updating the data, with data from the 0th position to the i'th position. We simply plot all the data from 0 to i.

Next we looked at adding a timer, this was done by adding `self.txt = plt.txt(timer_x,timer_y,"t = 0")` to the `create_animation` method. The values of `timer_x` and `timer_y` are worked out in the `init_frame` method, the way they are worked out depends on whether `auto_lim` is `True` or `False`. We then added a line in both `_next_frame` and `_next_frame_trace` to update this text, using the `self.t` values.

We did discover that `show_animation` had some weird behaviour after adding the text, the dot for the first pendulum disappeared from time to time, but this did not show up in `save_animation`. We tried to figure out why this was the case, we could not figure out why this was happening, but we did find out that if we set `blit = False` in the `FuncAnimation` method, the problem went away. So we added a `blit` parameter to `create_animation`, and made it so that `show_animation` calls the `create_animation` method with `blit = False`.

## An actual animation

We then tackled making an actual animation which was rendered in real-time, we spent quite some time working out how to do it. We finally came up with a new method which we called `real_time_animation`, this method takes in parameters like the `solve` method, but it omits the dt parameter. The dt parameter is worked out based on the fps we wish the final animation to be rendered with. We also decided to include a scalar paremeter `vid_speed`, which is 1 by default, but you can change it to alter the speed at which the animation runs<sup>[3](#footnote3)</sup>.

When we finally had working code that we were satisfied with, we spent some time exploring how animations looked for different initial conditions, we found an animation we felt was interesting and chose it as our example.

### Footnotes
<a name="footnote1">1</a>: this variable is unused, but required in the `solve_ivp` method from SciPy, which we use in our `solve` method. This is the case for all `t` variables in every `__call__` method in this project.

<a name="footnote2">2</a>: We also made a test for `AnimateDoublePendulum` in `test_animate_double_pendulum.py`, this is basically a carbon copy of the test for `DoublePendulum`, but we wanted to implement it to check that `AnimateDoublePendulum` inherited everything from `DoublePendulum` correctly.

<a name="footnote3">3</a>: If you change the `vid_speed` parameter, the problem is still computed from 0 to T, but the playback speed of the animation is speed up/down, the length of the animation is then also shortened/lengthened. If you set `vid_speed` to 0.5, it will play at half speed, but be twice as long
