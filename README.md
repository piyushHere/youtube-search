Hey! Welcome, I usually ask the reader to grab a cup of coffee when the setup is a little hard but the setup here is pretty straightforward.

If you are familiar with flask environment and are feeling a little adventourous and you want to set up locally make sure you create a virtual environment but I will only be discussing about
the docker setup here.

Steps:

1. Make sure docker daemon is running on your system otherwise you won't be able to build the image in the next step.
2. Build the docker image on your system using the command ```docker build --tag youtube-fetch . ```
3. This will take a minute or so for the first time, go drink some water, stay hydrated!
4. Confirm you have built the image using ```docker images```
5. To run this image as a container use the command ```docker run -p 5000:5000 youtube-fetch```, here make sure you give the -p flag to enable port forwarding so that you can use your system's port to access docker's port.
6. Since I have deployed this DB remotely using heroku, you should be able to send GET requests right away.

DATABASE MODELS->
I have kept it really simple and made a model called ```Youtube``` inside models.py with the required fields.

APIs:
1. I have followed layered architecture to design the APIs in this app, where first layer is the application layer which listens to the requests, 2nd is the service layer where all meaty logic resides which subsequently talks to the DAO layer (data application object) layer where DB operations are performed. (1st layer cannot talk directly to the 3rd layer). This ensures abstraction and comes really handly when we decide to add more functionality to our project (scalablity my friends)
2. I have used an inbuilt scheduler library provided in flask which I have used for my cronjob which fetches youtube data and dumps into my table, which allocates a different thread to perform background tasks so incoming requests won't be blocked by this process.

3. To get paginated youtube data, visit [localhost:5000/youtube_data?page=1] (localhost:5000/youtube_data?page=1), this will fetch the first five rows from our table, change page query param to get subsequent pages.
4. To search data on the basis of title and description visit [localhost:5000/search?query=hi] (localhost:5000/search?query=hi), this will fetch all videos which matches the query string we have provided here. 

Let me know if you face any issues with the setup.

Thanks! May the fork be with you. 