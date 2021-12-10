# CS 494 : Information Retrieval course project

Initial steps:
Run ```pip install -r requirements.txt``` to install the necessary dependencies.

Download ```data```  and ```models``` folder from https://drive.google.com/drive/folders/1QkFppZxlZB59ypB2VjHLQUgRmcOccNmb?usp=sharing and place it within ```SE``` folder.

To setup the project run ```setup.py``` only once. This will crawl and calculate document vectors for all embeddings. It will also calculate page rank of all the pages.

# To run the project 
Run the flask app using ```python app.py```. This will start a flask web server where the UI is displayed and query terms can be searched.