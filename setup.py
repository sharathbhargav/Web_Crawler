from SE import  Start_job

start = Start_job.Start("https://cs.uic.edu/")
# change the below number to limit the number of pages to be crawled
start.start_all(pages=3500,cache=False)