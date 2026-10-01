from flask import Flask, render_template, request, send_file
from scrapper import search_incruit, search_jobkorea, search_saramin
from file import save_to_csv

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/search')
def search():
    keyword = request.args.get('keyword')
    page = int(request.args.get('page', 1))
    sites = request.args.getlist('sites')

    jobs = get_jobs(keyword, page, sites)

    return render_template('search.html', keyword=keyword, page=page, sites=sites, jobs=enumerate(jobs))

@app.route('/file')
def file():
    keyword = request.args.get('keyword')
    page = int(request.args.get('page', 1))
    sites = request.args.getlist('sites')
    print('sites:', sites)

    jobs = get_jobs(keyword, page, sites)

    save_to_csv(jobs)
    return send_file('downloads.csv', as_attachment=True)

def get_jobs(keyword, page, sites):
    jobs = []
    if 'incruit' in sites:
        jobs.extend(search_incruit(keyword, page))
    if 'jobkorea' in sites:
        jobs.extend(search_jobkorea(keyword, page))
    if 'saramin' in sites:
        jobs.extend(search_saramin(keyword, page))

    return jobs

# 다른 파일에서 import 했을 경우, main이 아니라 파일명(app)이 됨.
# debug=True : 개발모드
if __name__ == '__main__':
    app.run(debug=True)