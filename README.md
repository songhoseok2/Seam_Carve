# Seam_Carve
https://ancient-chamber-87494.herokuapp.com/

This project was inspired from one of the University of Michigan's EECS 280 project. I wanted to give a better user interface to this interesting carving algorithm, and thus developed this web application using Flask. The application accepts an user uploaded image, then proceeds to the resizing page. There, the user resizes the displayed image, and whenever any change is made, the python program proceeds with the seam carving and returns the result to be uploaded to the server. The page then makes a GET request to the appropriate carved image to display the result in real time.

### What is Seam Carving?
Seam Carving is an algorithm for content-aware image resizing. It functions by establishing a number of seams (paths of least importance) in an image and removing them in the resizing process. The purpose of the algorithm is image retargeting, which allows the users to resize images without distorting or losing significant portions of the image.

![Seam Carve example images](https://github.com/songhoseok2/Seam_Carve/blob/master/static/sample_images/sample.jpg)
