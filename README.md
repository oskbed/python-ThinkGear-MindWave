# python-ThinkGear-MindWave

This is my first python project. It's a module for EEG device, Mind Wave Mobile (ThinkGear technology).
I based on other modules found in github and documentation:
http://developer.neurosky.com/docs/doku.php?id=thinkgear_communications_protocol

This is early WIP version and has many issues.
Things to fix/do:
- correct class issues (args are not passed correctly)
- MultiProccessing instead of Threads module.
- define rest of code packets
- "write to file" function
- delete artifacts from packets
- poor signal detection

At this point, you can make live plots and read raw signal, attention or meditation levels.
