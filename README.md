# stockdipperfunction-using-aws-2024-



STEP ONE- download the files to your local machine (download datautil.zip and lambda_function.py)

STEP TWO- -open lambda_function and update your alpha vantage api and your senders and receivers email addresses 
          -it is easy to get the alpha vantage API just go to https://www.alphavantage.co/support/#api-key and follow through for your api key
          -to setup SES, go to aws ses and verify your senders email, this is very easy and follow any youtube video for this

STEP THREE- drag and drop the updated lambda_function.py to datautil.zip and replace the existing default file

STEP FOUR- create a lambda function configs- any python 3 version should work, and dont forget to change the name to 'lambda_function.handler' (basically                              "lambda_func_name.handler")

STEP FIVE- upload the zip file to your lambda function and then test it, you should get a mail to your receivers mail

STEP SIX (optional)- Setup Eventbridge trigger to send a mail at your custom time
