About Simple Poster
Effortless Poster Generation

Poster generation using Python's Pillow library and ConvertAPI
(This project initially used Pillow library but switched to ConvertAPI for the sake of project timeline. Pillow required manual elements positioning that needed time for more templates to be created)

This project allows users to generate custom posters by providing specific details such as event title, short description, date, time, and venue through a form view. Users can later add more information like photos. The process involves collecting user inputs, displaying sample templates, and generating downloadable posters using ConvertAPI.

Designed for:
i. users who are not comfortable or in a position to using Canva and other advanced design tools available
ii. users who are in need of a quick watermarking tool
iii. most importantly, platform specific use where users communicate with graphics/posters and may want to quickly generate a communication 
Users provide specific details like Event title, Short description, Date, Time, Venue, etc.
Automates the creation of professional-looking posters.

Prerequisites
Python 3.x
Django 3.x or later
Virtualenv
ConvertAPI account and API key

Clone the Repository
git clone https://github.com/Naftali-B/simple_poster.git
cd simple_poster

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

Set up your ConvertAPI secrete key

python manage.py migrate

python manage.py runserver

Open your web browser and navigate to http://127.0.0.1:8000/ or the IP you ran the server at, to access the application.

For questions or issues, please contact nbudamba@gmail.com.