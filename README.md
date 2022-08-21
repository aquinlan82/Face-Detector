 # # Facial Recognition Implementation

**What does it do?**
For my final project in CS 445- Computer Photography, I implemented a facial detection method in a published paper called Face detection using template matching and skin-color information by Zhong Jin, Zhen Lou, Jingyu Yang, and Quansen Sun. 

**How does it work**


* File Descriptions:
    cifar: compressed files holding the cifar-10 image set, which are used to test the facial detection on non-face images.
    crop-part1: images corresponding to the annotations in landmark_list_part1. Used to test accuracy of facial detection.
    part1: uncropped images used for testing facial detection on more difficult cases
    face_images_kaggle.npz: compressed folder of black and white images used to create average face template
    face_template.jpg: average face, used in template matching.
    facial_keypoints_kaggle.csv: annotations for images in face_images_kaggle.npz
    Final.ipynb: Jupyter notebook with facial detection code. This is the code to run facial detection.
    landmark_list_part1.txt: annotations for the images in crop-part1, used to measure accuracy of facial detection.
    paper.pdf: the paper this code is implementing, for reference
    utils.py: file of utility functions used by the jupyter notebook


* How To Run:
    * The jupyter notebook doesn't require much setup or non standard libraries, and so should be able to run all the way through without any special help. All but the last two cells are functions which are then called in the last cells.
    * Running the penultimate cell (labeled "single check") will randomly choose and image from the test set, run it through the detection algorithm, and put out an annotated face. 
    * Running the last cell runs a full set of images through the algorithm, checks their accuracy, and puts out the false positive and false negative rates. This last cell will take around 15 minutes to run.


* Method:
    The paper uses two features for facial detection: skin detection and eye detection. I approached this problem by separately implementing both of these in the same way as the paper and then combining when they were both fairly accurate. Since both of these features-finding methods are intricate but self-contained, keeping them independent made debugging much easier. However, it did have the drawback that I needed to use multiple test sets. The eye detector works on the assumption that the input image is a cropped face, while the goal of the skin detector is to take any image and find the general face area, so I needed different inputs to debug each.
    The skin detector’s main purpose is to  decide where skin is and which skin is the face. The former is the trickier problem, since there are a variety of skin colors in the world and a variety of luminance conditions affecting the perceived color. The paper approaches this problem in the YCrCb color space. They look at each pixel’s luminance and using that to determine likely bounds for the other two channels. If a pixel’s Cr and Cb values are within the bounds for its luminance, it is marked as skin. Once the skin is marked, we eliminate the skin pixels that are either noise or not from the face. The paper is vague on how they implemented this, but I was able to accomplish the same goal by finding the contours of the skin mask and building a bounding box around the one that met certain criteria.
    The eye detector does three basic tasks: find likely eyes using blob detection, normalize each candidate, and template match to choose the most likely location of the eyes. The blob detection works because a properly thresholded image of a face will have a dark spot at each eye surrounded by a light face area. With the paper’s guidance, I immediately eliminated some blobs pairs as eye candidates due to relative location. Normalizing each candidate is simply applying a rotation so that the eyes (and thus the face) are aligned with the camera. Once normalized, basic template matching calculates the difference between each rotated image and an average face template. As per the paper, I used SSD to get this difference and chose the highest score to be the correct location of the eyes.
    At the end of this process, the location of the eyes are known for an image that has gone through much cropping, resizing, and rotating. Working backwards, the corresponding points are located on the original image and labeled.
    Following the lead of the paper, I evaluated my implementation using the false positive and false negative rates. I had an average false negative rate of 35.4% and average false positive rate of  2.76%, which is in the same realm as the original publishers' results.

* Example:
![Original Image](img/original.png)
![Skin Mask](img/skin_mask.png)
![Cropped Face](img/cropped_face.png)
![Blob Detections](img/blobs.png)
![Template Matching](img/template.png)
![Result Image](img/result.png)


**Project Goals, Skills, and Tools**
* The goal of the final project was to apply what I learned in class to a new problem of sufficient difficulty. Though I was following the steps provided by the original authors, this was definetly a tricky project because 
sometimes instructions were too vague, leading me to do outside research or brainstorming on how to implement them myself. 

* The most prominent skill I picked up was an understanding of color analysis. Specifically, I had to find a way to transform the color in the images into likelihoods that they are a skin pixel. Since skin comes in many shades which are further influenced by the light levels in the picture, this was particularly hard. I did learn about a lot of ways to tackle the problem and eventually chose one to use in this project

**Reflection**
I had a lot of fun working on this project. Object detection has always felt like magic to me, so it was cool to see that it is something I'm capable of creating, even if it took a lot of work and a ton of guidance. I also found that I enjoyed doing research for this more than I do for most projects. Rather than merely looking something up so that the code stops giving errors, I had to read research papers and understand them at a deeper level.


