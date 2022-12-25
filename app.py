from flask import Flask, render_template,request
import pandas as pd
from flask_ngrok import run_with_ngrok

df = pd.read_csv(r'D:/PROJECT/job analytics/Job Analytics 2-20221224T143851Z-001/Job Analytics 2/final_job_data.csv')

def job(skills):
    try:
        data = df[df['technical_skills'].str.contains(skills)]
        Most_common_level = data.groupby(['level']).size()[:1].reset_index()['level'][0]
        Most_common_industry = data.groupby(['industry']).size()[:1].reset_index()['industry'][0]
        Most_common_comp_class = data.groupby(['job class']).size()[:1].reset_index()['job class'][0]
        Total_Number_jobs = len(data)
        return {'mcel': Most_common_level, 'mci': Most_common_industry, 'mccc': Most_common_comp_class, 'tn': Total_Number_jobs}
    except:
        return {'placeholder': 'No! Job opening for the given skill'}

def job_details(skills):
    data = df[df['technical_skills'].str.contains(skills)]
    jobs = data.T.to_dict().values()
    return jobs

skills = li = ['python', 'c','r', 'java','hadoop','scala','flask','pandas','spark',
    'numpy','php','sql','mysql','dbms','mongdb','nltk','keras', 'pytorch','tensorflow',
    'linux','ruby','django','react','excel','reactjs','ai','ui','tableau','cad','php']

# #################################app section ###########################################
app = Flask(__name__)
# run_with_ngrok(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        object = request.form.to_dict()
        if object["skill"].lower() not in skills:
            data = {'placeholder' : "Search Relevant Skill"}
        else:
            data = job(object['skill'].lower())
            if 'placeholder' not in data.keys():
                data['placeholder'] = object['skill']
        return render_template('index.html', data= data)
    else:
        data = {"placeholder" :"Search your skills here"}
        return render_template('index.html', data= data)

@app.route('/jobdetails', methods=['POST'])
def jobdetails():
    object = request.form.to_dict()
    data = job_details(object['skill'].lower())
    return render_template('new.html', data = data)
    

if __name__ == '__main__':
    app.run()

