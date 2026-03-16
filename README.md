# JLPTPrep Web 🇯🇵

> *The web version of JLPTPrep — study for the JLPT from any browser.*

A Flask web app for JLPT N5 and N4 study. Same quiz content as the iOS app, accessible from any device without needing to install anything. Built to be hosted on GoDaddy shared hosting via Passenger WSGI.

---

## 📱 Features

- **Multiple choice quizzes** — vocabulary, kanji, and grammar
- **Unit & chapter filtering** — drill exactly what you need
- **Score tracking** — every result saved to CSV
- **Wrong answer log** — review what you got wrong
- **Mobile-friendly UI** — works on phone browsers
- **CSV-driven** — add new quiz content by dropping a CSV file in `data/`

---

## 🛠️ Built With

- Python 3
- Flask
- Jinja2 templates
- CSV data files (no database needed)

---

## 🚀 Run Locally

```bash
git clone https://github.com/oo0speed0oo/quizmarkeronline.git
cd quizmarkeronline
pip install flask
python app.py
```

Then open `http://localhost:8081` in your browser.

---

## 📁 Project Structure

```
jlptprep-web/
├── app.py                  # Flask routes and app logic
├── passenger_wsgi.py       # GoDaddy WSGI entry point
├── quiz_logic.py           # Question filtering and scoring
├── question_loader.py      # CSV loader
├── score_manager.py        # Score persistence
├── wrong_answer_manager.py # Wrong answer tracker
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── index.html          # Quiz file selector
│   ├── units.html          # Unit selection
│   ├── chapters.html       # Chapter selection
│   ├── setup.html          # Question count picker
│   ├── quiz.html           # Active question
│   ├── answer.html         # Answer feedback
│   └── results.html        # Final score screen
└── data/
    └── *.csv               # Quiz content files go here
```

---

## 📋 CSV Format

```csv
question_number,unit_number,chapter_number,question,choice_a,choice_b,choice_c,choice_d,answer
1,1,1,彼女は毎日___を勉強します。,日本語,英語,数学,音楽,A
```

---

## 🌐 Deploying to GoDaddy

1. Upload all files to your GoDaddy hosting via cPanel File Manager or FTP
2. Install Flask: `pip install flask --target=.`
3. Make sure `passenger_wsgi.py` is in your app root
4. GoDaddy's Passenger server will auto-detect it

---

## 🗺️ Roadmap

- [x] Quiz flow (unit → chapter → count → quiz → results)
- [x] Score tracking
- [x] Wrong answer log
- [x] Mobile-friendly UI
- [ ] User accounts / login
- [ ] Leaderboard
- [ ] Spaced repetition

---

## 👤 Author

**Michael Placido** — English teacher turned developer, Saitama, Japan 🇯🇵

- iOS version: [JLPTPrep](https://github.com/oo0speed0oo/Quiz_Marker_IOS)
- GitHub: [@oo0speed0oo](https://github.com/oo0speed0oo)
- Email: Mpfx01@gmail.com
