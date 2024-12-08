Hi everyone, this is an ML Based Feedback Analysis Software, feel free to have a look, meanwhile, I'm writing up the docs.




I have changed a bunch of things for the docker-specific branch. [Other changes like changes to model or core logic are not mentioned here]

 For instance all of it's dependencies are localized; meaning, before we were supposed to download whisper independently and add the path to voice-2-text.sh. However under the ```whisper/models``` folder, I have added a script that automatically downloads the whisper model for you.

 Along with the model you also need the executable. I noticed the executable was ~1.5 megabytes so I pushed it to the repo as well under the ```whisper``` folder. So no headache of building it as such.

 Of course, I have modified all the paths to be relative instead, this way would prove much better and intuitive. I call this methodology **general relativity** because of the usage of relative paths.

### TODO

 - The file_watcher already runs, however I am not so sure if the models are being loaded. this is bizarre to me as of right now but I haven't looked into it much anyway.

 - Cowj needs to be taken care of, I didn't touch it.

 - I don't remember what was next. Oh well. I would love if you would try building the image though.




# If you would like to contact me, then feel free to drop a message here or on Linkedin. 
# Referals, Donations, Job Applications, Internships, Consultancy, anything at all, if you have anything in mind, I'm open to anything, anytime, anyday. THANK YOU FOR VISITING!
