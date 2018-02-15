# python-ThinkGear-MindWave

This is my first python project. It's a module for EEG device, Mind Wave Mobile (ThinkGear technology).
I based on other modules found in github and documentation:
http://developer.neurosky.com/docs/doku.php?id=thinkgear_communications_protocol

This is early WIP version and has many issues.
Things to fix/do:
- MultiProccessing instead of Threads module.
- define rest of code packets
- "write to file" function
- poor signal detection

I also created simple GUI in PyQT to visualise the data.
It comes in two version:
- low signal resolution (to visualiste signal)
- high signal resolution (more demanding for cpu, less optimized)
