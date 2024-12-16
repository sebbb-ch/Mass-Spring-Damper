# Spring-Mass-Damper Simulation

Models a spring-mass-damper by solving its governing second order differential equation, with a layer of Pygame on top to allow for real-time visualization different starting conditions. Matplotlib outputs the correspoding time-position and velocity-position graphs for any given displacement.

### Quickly

For a mass oscillating linearly and being dampened, we start with applications of Newton's Second Law and Hooke's Law to arrive at a second order differential equation. The key insight that might fall through the cracks is that when we guess that the solution is $x(t) = e^\lambda t$, it's a natural choice because of the necessary conditions of the system: that is, we need a function whose derivative is a scalar of itself. (Of note: in a system with no damper, we can choose $\cos{t}x_0$ as well, since this function also has a second derivative equal to itself, oscillates, and doesn't start at 0.) 

### Parameters

d (damping constant) affects the rate of decay of the oscillation
x_0, v_0 (initial displacement and velocity) determine the conditions of the system at t = 0

### TODO
- Add more detailed spring and damper animationsm
- Extend simulation to handle [coupled oscillators](https://scholar.harvard.edu/files/schwartz/files/lecture3-coupled-oscillators.pdf) 
- Implement Runge-Kutta for more accurate solutions (scipy actually does this for us but I'd like to take the time and understand the code in [this paper](https://www.researchgate.net/publication/344220586_A_simple_Runge-Kutta_4_th_order_python_algorithm) with the help of [this video](https://www.youtube.com/watch?v=hGCP6I2WisM).)