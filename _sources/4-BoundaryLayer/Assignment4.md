# Assignment 4. Growth of Turbulent Boundary Layer

In the Notebook we have found a function that computes, for every $c_f$ the corresponding value of $\text{Re}_\delta$ (and, consequently, $\delta$). 

1. Use this function to find a power fit of the type 

$$
c_f = K \text{Re}_\delta^n
$$

2.  Use this to define a function for the friction velocity as a function of $\delta$ and $U$, `u_tau(delta, U)`

3. Introduce this function into the log-law to find a cloud of points $(y,u)$ and fit again witha power law

$$ 
\left(\frac{u}{U}\right) = K'\left(\frac{y}{\delta}\right)^m
$$

This is know as the power-law for the turbulent boundary layer. It is, as the log-law, valid only for $y^+ \gtrapprox 30$

4. Finally use the von Kármán equation for steady uniform flow, equation (27), to find how a turbulent boundary layer grows, $\delta(x)$.