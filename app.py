from flask import Flask, render_template, request
from SE import  Start_job
app = Flask(__name__,static_folder='static',static_url_path='/static')
start = Start_job.Start("https://cs.uic.edu/")
@app.route('/',methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        form_data = request.form # 'name' , 'choice'
        query_string = form_data['name']
        print(form_data['choice'])
        choice = form_data['choice']
        type=0
        if choice == "TF-IDF":
            type = 0
        elif choice == "Word2Vec":
            type=1
        elif choice=="PageRank":
            type=2
        print(query_string)
        res = start.query(query_string, type)
        i=0
        for k,v in res.items():
            print(k,":",v)
            i+=1
            if i>10:
                break
        list_of_urls = ["a1","a2","a3","a4"]
        return render_template("search.html",name=True,
                               list_data=list(res.keys()),res = res)
    elif request.method == 'GET':
        return render_template("search.html")

if __name__ == '__main__':
    start.called_from_flask()
    app.run()