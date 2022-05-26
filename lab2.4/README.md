# Lambda and image clean-up lab

Today all pictures come with metadata like GPS info, camera, etc. Here is a useful function to clean-up it and keep some of our privacy.

1. Download the lab files from this repository:

[https://github.com/Resistor52/hitc-dev/blob/main/lab2.4/lambda\_function.zip](https://github.com/Resistor52/hitc-dev/blob/main/lab2.4/lambda_function.zip)

![](images/Img_01_Lab_2.4.png?raw=true)

1. From AWS Management Console, time to create the buckets that will be used for our function. Create one called &quot;input-image-\&lt;myPhoneNumber\&gt;&quot; and another called &quot;output-image-\&lt;myPhoneNumber\&gt;&quot; using the procedure below.

Important - The buckets should start with the requested names, otherwise the clean up script will not work.

![](images/Img_02_Lab_2.4.png?raw=true)

![](images/Img_03_Lab_2.4.png?raw=true)

![](images/Img_04_Lab_2.4.png?raw=true)

Enable encryption by default and click in Create Bucket.

![](images/Img_05_Lab_2.4.png?raw=true)

Repeat this step for output bucket.

![](images/Img_06_Lab_2.4.png?raw=true)

Info - As S3 uses the global unique bucket, two students can&#39;t use the same bucket name.

1. Create a custom policy available in https://github.com/Resistor52/hitc-dev/blob/main/lab2.4/s3\_policy.json to add necessary permissions for the file transformation lambda function..

![](images/Img_07_Lab_2.4.png?raw=true)

Select Policies

![](images/Img_08_Lab_2.4.png?raw=true)

Select Create policy

![](images/Img_01_Lab_2.4.png?raw=true)

Click in JSON file and paste the file content available in the json file previously downloaded.

![](images/Img_10_Lab_2.4.png?raw=true)

Click in Next review

![](images/Img_11_Lab_2.4.png?raw=true)

Type the policy name and click in Create policy

![](images/Img_12_Lab_2.4.png?raw=true)

1. Create the lambda function that will be used to clean up the image when it is uploaded:

![](images/Img_13_Lab_2.4.png?raw=true)

![](images/Img_14_Lab_2.4.png?raw=true)

Select Use a blueprint and type s3-get-object-python.

![](images/Img_15_Lab_2.4.png?raw=true)

Select the available blueprint and click in configure.

![](images/Img_16_Lab_2.4.png?raw=true)

Add a function name and select Create a new role with basic Lambda permissions

![](images/Img_17_Lab_2.4.png?raw=true)

Scroll down and select Create function

![](images/Img_18_Lab_2.4.png?raw=true)

Now click in the function to configure it.

![](images/Img_19_Lab_2.4.png?raw=true)

Select Add trigger

![](images/Img_20_Lab_2.4.png?raw=true)

Select S3 as trigger, choosing the input bucket as source and keep All object create event.

![](images/Img_21_Lab_2.4.png?raw=true)

Acknowledge the potential recursive S3 action and click in Add

![](images/Img_22_Lab_2.4.png?raw=true)

Time to upload the code. Click in Code tab, Upload from and .zip file.

![](images/Img_23_Lab_2.4.png?raw=true)

Click in Upload button.

![](images/Img_24_Lab_2.4.png?raw=true)

Select the lambda\_function.zip file downloaded previously and hit OK

![](images/Img_25_Lab_2.4.png?raw=true)

![](images/Img_26_Lab_2.4.png?raw=true)

Now it&#39;s time to edit the IAM role, adding the missing permissions

![](images/Img_27_Lab_2.4.png?raw=true)

Select Add permissions and Add policies.

![](images/Img_28_Lab_2.4.png?raw=true)

Attach the previous policy created before and click in Attach policy

![](images/Img_29_Lab_2.4.png?raw=true)

1. Now it&#39;s time to test the function. You can use a sample file available here: . Open the S3 console and add the file to the input bucket.

![](images/Img_30_Lab_2.4.png?raw=true)

Open the input bucket

![](images/Img_31_Lab_2.4.png?raw=true)

Click in the Upload button

![](images/Img_32_Lab_2.4.png?raw=true)

Click in Add file and select a camera image

![](images/Img_33_Lab_2.4.png?raw=true)

![](images/Img_34_Lab_2.4.png?raw=true)

Click in Upload

![](images/Img_35_Lab_2.4.png?raw=true)

After a minute, you can check the output bucket that a file started with &quot;clean…&quot; will be in there.

![](images/Img_36_Lab_2.4.png?raw=true)

You can download this file and compare the results with the initial image with the previous one using [https://jimpl.com/](https://jimpl.com/)

1. The function logs can be checked here

![](images/Img_37_Lab_2.4.png?raw=true)

![](images/Img_38_Lab_2.4.png?raw=true)

![](images/Img_39_Lab_2.4.png?raw=true)

![](images/Img_40_Lab_2.4.png?raw=true)
