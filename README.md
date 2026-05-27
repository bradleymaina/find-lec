# find-lec
find-lec is a hobby project that I wrote to  to obtain lecturer's contact details . The names of lecturers were obtained in a large school timetable and the contact details were obtained from various soures that are publicly available.
It has a backend and a front end , but i mostly wrote the backend logic and vibe coded the front end well because nobody cares about front end anymore

# Installation
This installation guide is focused on linux and more specifically arch linux but can work on any linux distro.
First you need to have python3 installed on your system if it is not 

```bash
sudo pacman -Syu python3

```
Create a virtual environment 

```bash
python3 -m venv venv

```
Activate the virtual environment

```bash
source venv/bin/activate

```

Install dependancies

```bash
pip install pdfplumber
pip install pandas
pip install flask

```
Clone the repo 

Navigate to src

Run search.py to do a custom search

```bash
python3 search.py

```

# Contribution
If you have any suggestions, critique you can create a PR and/or create an Issue and i will work on it 

# Licence 
MIT Licence 

# NOTE
This project was build on entirely open source data but still sensitive data. It may be in violation of the Data Protection Act but well , i bet the government has bigger things to worry about .

