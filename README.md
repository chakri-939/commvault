<h1 align="center">
  Image management application
</h1>
<!-- <div align="center">
  <img alt="Demo" src="./assets/project-1-a7dcf9f6.png" />
</div> -->

<br/>


## Objective

Your task is to create a web application that allows users to upload, list, download, and optionally encrypt images. The application should be hosted on an AWS EC2 instance and interact with an AWS S3 bucket. You're free to use any Python web framework you're comfortable with, such as Flask, Django, or FastAPI.


Code snippets used

- for installing Flask boto3

```pip install Flask boto3```



- for checking AWS end to end connection

``` curl https://ec2.eu-north-1.amazonaws.com```



- for running python code for creating EC2 instance and s3 bucket

``` python code1.py```



- for transferring app.py file from local directory to EC2 user

```scp -i "C:/Users/Chakradhar/Downloads/test.pem" D:/Python/commvault/app.py ec2-user@16.170.201.188:/home/ec2-user```



- for connecting EC2 user

``` ssh -i test.pem ec2-user@16.170.201.188``` 


- for downloading cryptography for encryption and decryption

```pip install cryptography```




## How to Run?
 - Create a free AWS account
 - install Python, Boto3, and your chosen web framework on your development machine
 - Download the uploaded files
 - Run code1.py for creating a EC2 instance and s3 bucket
 - transfer the app.py code to EC2 user
 - Now, connect the EC2 user
 - Run the app.py on EC2 instance





## Milestone Achived
### Milestone 1: Basic Image Upload and Listing
 - Page 1 - Upload Images: Created a user interface that allows users to select and upload images to the S3 bucket. 
 - Page 2 - List and Download Images: Displays a list of images stored in the S3 bucket and provides an option to download each image. 

### Milestone 2: Implementing Encryption 
 -  Page 1 - Upload Images: Encrypts images while uploading
 -  Page 2 - Show only encrypted images

### Milestone 3: Decryption and Advanced Download Options
 - Provided a "Download Encrypted File" option that downloads the file in its encrypted form. 
 - Provided an option to "Decrypt and Download" the image, prompting the user for any necessary keys or passwords.
