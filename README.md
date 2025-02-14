<h1 align="center"> VOILA: A Video or Image Labeling Applicationused for fast Semantic Segmentation </h1>
<h5 align="center">An image labelling application to use in neural network training.</h5>

</p>
<p align="center">
<img src ="./documentation/media/log.png" alt="Logo" width="1200"/>
</p>

Considering the impact on the world of artificial intelligence and process automation in recent years, semi-autonomous systems have been developed that act responding to signals from their environment. An example is food delivery robots that establish their trajectory from images of their surroundings. To develop a system like this it is necessary to make use of segmentation algorithms trained to recognize obstacles, and to train these algorithms, databases of segmented images corresponding to the environment in which the robot will operate are required.

To facilitate the image segmentation process, the application based on [GrabCut](https://docs.opencv.org/master/d8/d83/tutorial_py_grabcut.html) available in this repository was developed.
</p>
<p align="center">
<img src ="./documentation/media/INTRO.png" alt="Intro" width="300"/>
</p>

**Status**: Finished (Waiting for evaluation)

---
<h3 align="left"> Install Image Labelling App </h3>

For the installation is necessary to clone the current repository in a local repository. If you don't have GitHub installed yet, you should.
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
<h3 align="left"> Build and Run Docker Image </h3>

The Image Labelling App dependencies, compilation, and configuration are packaged in a Docker Image. Before continuing, make sure you have Docker installed on your device. If it is not installed and you are working on Linux, you can run the following commands in a terminal:

	sudo apt-get update
 	sudo apt-get install docker-ce docker-ce-cli containerd.io


This can take a while. When the installation is done you can test it by running the Docker image *hello-world*. 

	sudo docker run hello-world


If the installation was done correctly, you should see some informational text on the screen.

Besides this, there are other post-installation steps for Linux. To complete them, run the following commands:

	sudo groupadd docker
	sudo usermod -aG docker $USER
	newgrp docker


*If you are not working on Linux, you can install by visiting the* [official website](https://docs.docker.com/get-docker/).

To run the Image Labelling App Docker image, verify that you are on the **DataLabelling** path and run the following command:

	bash start.sh

If it's the first time probably is going to take a while.

If all goes well, you should be seeing what is shown in the following image on your screen:

</p>
<p align="center">
<img src ="./documentation/media/dark.png" alt="def" width="600"/>
</p>


---
<h2 align="center">How to use?</h2>

<h3 align="left"> Basic configuration of the App </h3>

After the application is launched and what is shown in the previous image appears on the screen, the application is ready to start using. But before continuing, let's save the images to tag in the recommended folder, which is located in the project folder *-> DataLabelling -> media -> inputs*. After this we are going to introduce the labels that we want to generate. For this we are going to find the file *labels.txt* and we are going to open it. After opening, we are going to write each of the labels, separating each one with a new line (enter). When the labels are ready, we proceed to save the changes and exit the text editor. 

</p>
<p align="center">
<img src ="./documentation/media/labels.gif" alt="gif_labels" width="700"/>
</p>

Then, we can open the application by following the steps that had already been mentioned.

</p>
<p align="center">
<img src ="./documentation/media/opening.gif" alt="gif_opening" width="700"/>
</p>

Once the application is open, we will have the main menu on the screen. Some of the buttons on the graphical interface have shortcuts that we can see in the following table: 

| **Button** | **Shortcut** |
|:-----------|:------------:|
|Open file   |Ctrl + O      |
|Rectangle   |Ctrl + R      |
|Background  |Ctrl + B      |
|Foreground  |Ctrl + F      |
|Iteration   |Ctrl + I      |
|New         |Ctrl + N      |
|Open file   |Ctrl + O      |
|Previous    |Ctrl + Left   |
|Next        |Ctrl + Right  |
|SAVE        |Ctrl + S      |


<h3 align="left"> Use of the App </h3>


After the application appears on the screen, the application is ready to use. As already mentioned, the images or videos to be segmented must be in the *inputs* folder. What follows is to click on the *Open file* button or use the shortcut, after that a file browser will appear on the screen and in this we will open the *media* folder and locate the files to segment.

After selecting the files we are ready to start segmenting images. To begin we are going to select the area of interest by clicking on the **Rectangle** button and drawing on the image. If we want to see the result of the segmentation only selecting the area with the rectangle, we press the **Iteration** button. Otherwise, if we want to improve the segmentation process from the first iteration, we can select the Background and Foreground regions by selecting the corresponding button.

After executing the first iteration, you can continue making corrections on the foreground and background areas until the user considers that the segmentation process is complete.

</p>
<p align="center">
<img src ="./documentation/media/use.gif" alt="gif_use" width="700"/>
</p>

Finally, the results of the segmentation process and the time stamps for each of the images are saved in the **media** folder.

</p>
<p align="center">
<img src ="./documentation/media/outs.png" alt="outputs" width="600"/>
</p>

---
<h2 align="left"> Code Documentation </h2>

The code documentation was done using PEP8 and Doxygen and is available [here](http://labellingkiwipuj.125mb.com/)

---
<h2 align="left"> This project is being developed by: </h2>

✈️ Andrea Juliana Ruiz Gómez, [GitHub](https://github.com/andrearuizg), Email: andrea_ruiz@javeriana.edu.co

🏎️ Pedro Elí Ruiz Zárate, [GitHub](https://github.com/PedroRuizCode), Email: pedro.ruiz@javeriana.edu.co


<h3 align="left"> With the support of: </h3>

👨🏻‍🏫 Francisco Carlos Calderón Bocanegra, [GitHub](https://github.com/calderonf)

👨🏻‍💻 John Alberto Betancourt Gonzalez, [GitHub](https://github.com/JohnBetaCode)
