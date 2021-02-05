<h1 align="center"> Image Labelling App </h1>
<h5 align="center">An image labelling application to use in neural network training.</h5>

</p>
<p align="center">
<img src ="./doc/log.png" alt="drawing" width="1200"/>
</p>

Considering the impact on the world of artificial intelligence and process automation in recent years, semi-autonomous systems have been developed that act responding to signals from their environment. An example is food delivery robots that establish their trajectory from images of their surroundings. To develop a system like this it is necessary to make use of segmentation algorithms trained to recognize obstacles, and to train these algorithms, databases of segmented images corresponding to the environment in which the robot will operate are required.

To facilitate the image segmentation process, the application based on [GrabCut](https://docs.opencv.org/master/d8/d83/tutorial_py_grabcut.html) available in this repository was developed.
</p>
<p align="center">
<img src ="./doc/INTRO.png" alt="drawing" width="500"/>
</p>

**Status**: In development (code updates may be submitted after publication) x

---
### ***Install Image Labelling App***

For the installation it is necessary to clone the current repository in a local repository. If you don't have GitHub installed yet, you should.
If you are on Linux you can run the following command:

	sudo apt-get install git

Now you need to configure GitHub. For this run the following commands:

	git config --global user.name "user_name"
	git config --global user.email "email_id"

Otherwise, if you are not working on Linux, you can install GitHub from the [official website](https://desktop.github.com/). 

After installing and configuring GitHub on your computer, you must clone the repository. If you are on Linux, from the terminal you must access the path where you want the repository to be cloned and execute the following command:

	git clone https://github.com/Kiwi-PUJ/DataLabelling.git

*If you are not working on Linux you must clone the repository from the GitHub application.*

**Now the application files will be on your device.**

---
### ***Build and Run Docker Image***

The Image Labelling App dependencies, compilation, and configuration are packaged in a Docker Image. Before continuing, make sure you have Docker installed on your device. If it is not installed you can do it by visiting the [official website](https://docs.docker.com/get-docker/).

To run the Image Labelling App Docker image, verify that you are on the **DataLabelling** path and run the following command:

	bash start.sh

If it's the first time probably is going to take a while.

If all goes well, you should be seeing what is shown in the following image on your screen:

</p>
<p align="center">
<img src ="./doc/dark.png" alt="drawing" width="700"/>
</p>
