echo 'publishing changes to Heroku'
cd  "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source venv/bin/activate
git add .
git commit -m 'testing'
git push heroku master
heroku open
heroku logs