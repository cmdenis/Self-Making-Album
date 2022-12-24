# Bass Drum Math

The bass drum sound generator uses the following formula

$$f(x)=\sin\left(\left(1-A\right)\tau\ e^{-\frac{x}{\tau}}-\left(1-A\right)t+x\right)e^{-\frac{x}{k}}$$

Where $\tau$ is the decay rate for the pitch, $A$ is the amount of pitch modulation and $k$ is the decay rate of the amplitude of thte signal. We can think of this as an oscillator whose pitch is modulated by an exponential decay and whose amplitude is also modulated by an exponential decay.

To obtain this form, let's first look at how to make the inside of the sine. In a regular $\sin x$ function, the frequency does not change because the slope of the inside function remains constant. The slope of the function inside of the $\sin$ is what determines the pitch (and pitch over time). We would like to have a pitch that decays like an exponential. Mathematically this means:

$$\text{pitch}(x) = (A-1)e^{-\frac{x}{\tau}}+1$$

This decays from pitch $A$ to a pitch of 1 with a rate $\tau$. We want a function whose derivative is this function, by the fundamental theorem of calculus, this is simply its integral. Which gives us

$$\left(1-A\right)t\ e^{-\frac{x}{t}}-\left(1-A\right)t+x$$

Using initial conditions such that the above function starts at $0$. Putting this into a $\sin$ function and then multiplying by an exponential decay gives us the desired expression.