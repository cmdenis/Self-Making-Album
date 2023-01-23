# Parameter correlation

I'd like to implement some correlations between some parameters in the future. Ideally this would be doable accross many different scripts if all the scipts all take their randomness from a central randomness script. Maybe JSON format, idk yet...

An example of a cool application of correlation would be: If we have a bass drum sound, we could correlate the speed of pitch decay to the amplitude of the pitch modulation. This way if there is a lot of modulation it will take less time to decay. I can imagine other kinds of correlations being useful. Although I guess I don't necessarily want everything to be predictable.

To generate correlated gaussian random variables: https://stackoverflow.com/questions/18683821/generating-random-correlated-x-and-y-points-using-numpy