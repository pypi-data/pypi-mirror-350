# Wilson_Beta_wrapper

Wilson-Beta-wrapper is a simple Python tool that lets you tweak the beta function behavior from the wilson library, which is used in SMEFT (Standard Model Effective Field Theory) work.

With this wrapper, you can:

Catch the output of wilson.run.smeft.beta.beta

Change specific values (like Wilson coefficients) in the beta dictionary

Do it on the fly by calling configure_patch(key, value)

It’s handy if you want to experiment, test changes quickly, or try out custom beta behaviors—without having to mess with wilson’s core code.
