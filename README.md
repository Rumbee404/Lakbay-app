# LakbaySearch: A Philippine Tourism Web Search and Information Retrieval System

## Quick Start: Clone and Run LakbaySearch

This guide is for students who are new to GitHub, Git, Python virtual environments, and Flask.

### Step 1 — Check the Required Software

Make sure you have **Python 3**, **Git**, and **Visual Studio Code** installed.

Open PowerShell or the Visual Studio Code terminal and check:

```powershell
py --version
git --version
```

If both commands display version numbers, you can continue.

### Step 2 — Clone the GitHub Repository

**Cloning** means downloading a copy of the project from GitHub to your computer.

1. Open **Visual Studio Code**.
2. Select **Terminal > New Terminal**.
3. Navigate to the folder where you want to save the project.
4. Run:

```powershell
git clone https://github.com/profrbazur/lakbaysearch
```

5. Enter the downloaded project folder:

```powershell
cd lakbaysearch
```

If your repository uses a different folder name, use:

```powershell
cd <repository-folder-name>
```

### Step 3 — Open the Project in Visual Studio Code

If needed, run:

```powershell
code .
```

If the project is already open in Visual Studio Code, skip this step.

### Step 4 — Create a Python Virtual Environment

A **virtual environment** keeps the Python packages used by LakbaySearch separate from your other Python projects.

Run:

```powershell
py -3 -m venv venv
```

This creates a local `venv` folder.

> The `venv` folder is intentionally not stored in GitHub. Each student creates their own local virtual environment after cloning the repository.

### Step 5 — Activate the Virtual Environment

In Windows PowerShell, run:

```powershell
.\venv\Scripts\Activate.ps1
```

If activation succeeds, the terminal should look similar to:

```text
(venv) PS C:\...\lakbaysearch>
```

### Step 6 — If PowerShell Blocks Activation

If you see an error similar to:

```text
running scripts is disabled on this system
```

run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again:

```powershell
.\venv\Scripts\Activate.ps1
```

`-Scope Process` means the temporary policy change applies only to the current PowerShell session.

### Step 7 — Install the Required Python Packages

Once `(venv)` appears in the terminal, run:

```powershell
pip install -r requirements.txt
```

`requirements.txt` contains the packages required by LakbaySearch, including Flask, Requests, BeautifulSoup4, scikit-learn, and MarkupSafe.

### Step 8 — Optional: Regenerate the Search Dataset

The project already includes `data/documents.json`, so **you do not need to run the crawler to use LakbaySearch**.

To regenerate the tourism corpus:

```powershell
python crawler.py
```

This requires internet access and rebuilds `data/documents.json`. You do not need to run the crawler every time you start the application.

### Step 9 — Run LakbaySearch

Start the Flask application:

```powershell
python app.py
```

You should see something similar to:

```text
Running on http://127.0.0.1:5000
```

Open:

```text
http://127.0.0.1:5000/
```

### Step 10 — Test the Search Engine

Try:

- `Boracay`
- `historical places in Cebu`
- `mountains in the Philippines`
- `nature attractions Palawan`
- `Chocolate Hills`

Results should display ranked documents with relevance scores, snippets, categories, sources, and highlighted query terms.

### Step 11 — Open Search Analytics

After performing some searches, open:

```text
http://127.0.0.1:5000/analytics
```

The dashboard shows **Total Searches**, **Zero-Result Searches**, **Average Search Time**, **Most Searched Queries**, **Most Frequent Top Result**, and **Recent Searches**.

A fresh copy may initially have little or no analytics data. It will populate as searches are performed.

### Step 12 — Stop the Application

Return to the terminal running Flask and press:

```text
Ctrl + C
```

### Step 13 — Running LakbaySearch Again Later

You do **not** need to clone the repository, recreate `venv`, or reinstall the dependencies every time.

Normally, you only need to:

```powershell
.\venv\Scripts\Activate.ps1
python app.py
```

Then open:

```text
http://127.0.0.1:5000/
```

If PowerShell blocks activation in a new terminal session, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

and activate `venv` again.

### Quick Command Summary

For the first setup:

```powershell
git clone YOUR_GITHUB_REPOSITORY_URL
cd lakbaysearch
py -3 -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Then open:

```text
http://127.0.0.1:5000/
```

> **Remember:** Replace `YOUR_GITHUB_REPOSITORY_URL` with the actual repository URL before giving this README to students.

### Troubleshooting

| Problem                                      | Solution                                                                                                                                |
| -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `py is not recognized`                       | Python may be missing or not correctly installed. Install Python 3, reopen the terminal, and try `py --version`.                        |
| `git is not recognized`                      | Git may be missing or unavailable in PATH. Install Git, reopen the terminal, and try `git --version`.                                   |
| `running scripts is disabled on this system` | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate `venv` again.                                           |
| `ModuleNotFoundError`                        | Make sure `(venv)` appears in the terminal, then run `pip install -r requirements.txt`.                                                 |
| Port 5000 is already in use                  | Stop the other Flask/Python process or close the other LakbaySearch terminal before starting another instance.                          |
| No results appear                            | Try another or broader query. LakbaySearch searches a small 47-document corpus, so not every tourism query will have a relevant result. |

---

## 1. Project Overview

LakbaySearch is a small, domain-specific search engine focused on
Philippine tourism. You type a query like "beaches in Palawan" and it
returns ranked pages about Philippine destinations, complete with a
relevance score, a highlighted text snippet, and a link to the source
page.

It is a student/educational project built to demonstrate — end to end —
how a classical (non-AI, non-semantic) search engine works: collecting
web pages, cleaning their text, building a searchable index, and ranking
results by relevance to a query.

## 2. Project Objectives

LakbaySearch demonstrates the complete basic information-retrieval
pipeline:

```
Web Pages
   -> Crawl / Collect
   -> Extract
   -> Clean
   -> Index
   -> Search
   -> Rank
   -> Display Results
   -> Record Analytics
```

Every stage of that pipeline is implemented, testable, and small enough
for a student to read, run, and explain during a project defense.

## 3. Features

- Controlled web crawling of a fixed, hand-curated list of Philippine
  tourism pages (not a general-purpose internet crawler)
- A 47-document Philippine tourism corpus, stored as JSON
- Text preprocessing (lowercasing, punctuation stripping, stop-word
  removal)
- TF-IDF indexing using scikit-learn
- Cosine-similarity ranking between the query and every indexed document
- Dynamic search results rendered by Flask (no hardcoded/placeholder
  data)
- Relevance scores shown as a percentage
- Text snippets generated from each matching page
- Query terms highlighted in the snippets
- Category filtering (Beaches, Mountains, Historical Sites, Cities,
  Nature, Cultural Attractions, Other)
- Source filtering (by originating domain)
- SQLite-backed search analytics (total searches, zero-result searches,
  average search time, most searched queries, most frequent top result,
  recent searches)
- Zero-result handling with a friendly message
- Empty-query handling (redirects back to the homepage instead of
  crashing)

## 4. Technology Stack

Confirmed against `requirements.txt` and the actual imports in the code:

- **Python 3**
- **Flask** — web framework and routing
- **Requests** — HTTP fetching in `crawler.py`
- **BeautifulSoup4** — HTML parsing
- **scikit-learn** — `TfidfVectorizer` and `cosine_similarity`
- **SQLite** (Python's built-in `sqlite3` module) — search analytics
- **JSON** (Python's built-in `json` module) — document corpus storage
- **HTML5 / CSS3**
- **Bootstrap 5** (via CDN) — page layout and styling

No ORM, no charting library, no JavaScript framework, and no external
search/AI service is used anywhere in the project.

## 5. Project Structure

```text
lakbaysearch/
|
├── app.py                 # Flask app: routes, index build at startup, analytics logging
├── crawler.py              # Fetches the Wikipedia seed pages and builds data/documents.json
├── preprocessing.py        # Shared text cleaning: lowercase, punctuation, stop words
├── indexer.py               # Loads documents.json and builds the TF-IDF index
├── search_engine.py        # Query transform, cosine similarity, ranking, snippets
├── database.py              # SQLite analytics: schema, logging, and reporting queries
├── requirements.txt
├── README.md                 # This file
├── SEARCH_EVALUATION.md      # Evaluation of real search results
├── DEFENSE_GUIDE.md          # Q&A prep for a project defense
│
├── data/
│   ├── documents.json        # The 47-document crawled corpus
│   ├── analytics.db           # SQLite database of search analytics (auto-created)
│
├── templates/
│   ├── base.html              # Shared layout (navbar, Bootstrap head/scripts)
│   ├── index.html             # Homepage: search box + example searches
│   ├── results.html           # Ranked results, filters, snippets, highlighting
│   └── analytics.html         # Analytics dashboard
│
└── static/
    ├── css/style.css
    └── js/script.js
```

## 6. System Architecture

```text
Web Sources (Wikipedia)
    |
    v
crawler.py  (Requests + BeautifulSoup4)
    |
    v
data/documents.json
    |
    v
preprocessing.py  (clean + tokenize)
    |
    v
indexer.py  (TF-IDF Index, built at Flask startup)
    |
    v
User Query  (Flask /search route)
    |
    v
Query Vector  (same fitted vectorizer, .transform())
    |
    v
Cosine Similarity  (search_engine.py)
    |
    v
Ranked Results  (rank, score, snippet, category, source)
    |
    v
Flask Web Interface  (results.html)
    |
    +----> SQLite Search Analytics (database.py -> data/analytics.db)
```

## 7. Search Pipeline (Explained)

1. **Crawling** — `crawler.py` fetches a fixed list of ~47 Wikipedia
   pages about Philippine tourist destinations. It does not follow
   links; it only visits URLs from a hand-written list.
2. **HTML parsing / extraction** — BeautifulSoup4 parses each page,
   removes `<script>`/`<style>` tags, and pulls out the title and body
   paragraphs.
3. **Cleaning** — whitespace is normalized and the text is saved to
   `data/documents.json`.
4. **Preprocessing** — before indexing (and later, before searching),
   `preprocessing.py` lowercases text, strips punctuation, and removes
   common English stop words (like "the," "and," "of").
5. **TF-IDF indexing** — `indexer.py` combines each document's title
   (repeated), heading, and content into one string, cleans it, and
   fits a `TfidfVectorizer` over all 47 documents.
6. **Query transformation** — when a user searches, the same cleaning
   function is applied to the query, and the _already-fitted_
   vectorizer's `.transform()` turns it into a vector in the same space
   as the documents.
7. **Cosine similarity** — `search_engine.py` compares the query vector
   to every document vector and produces a similarity score from 0 to 1
   for each.
8. **Ranking** — documents with a score of 0 are dropped, the rest are
   sorted highest-to-lowest, and the top results are returned.
9. **Snippets** — a short excerpt of each matching document is built
   around the first place a query word appears in its text.
10. **Filtering** — results can optionally be narrowed to one category
    or one source before being returned.
11. **Analytics** — after a search completes, `database.py` logs the
    query, timestamp, result count, top result, and execution time to
    SQLite, so `/analytics` can report on real usage.

## 8. Installation Instructions (Windows PowerShell)

From the project root:

```powershell
py -3 -m venv venv
```

If PowerShell blocks activation with an execution-policy error:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## 9. Running the Crawler

The corpus (`data/documents.json`) is already included in this project,
so you do **not** need to run the crawler to use LakbaySearch. To
re-crawl and regenerate it from scratch:

```powershell
python crawler.py
```

This fetches the fixed list of Philippine tourism pages from Wikipedia,
extracts and cleans each page's text, and overwrites
`data/documents.json`. The crawler targets roughly 30–50 useful
documents; the currently validated corpus contains **47 documents**
across 7 categories (Beaches, Mountains, Historical Sites, Cities,
Nature, Cultural Attractions, Other).

## 10. Dataset

`data/documents.json` is a JSON array of document objects. Each object
contains exactly these fields, as actually produced by `crawler.py`:

| Field      | Meaning                                                           |
| ---------- | ----------------------------------------------------------------- |
| `id`       | Sequential integer ID                                             |
| `title`    | Page title                                                        |
| `url`      | Source URL                                                        |
| `heading`  | Page heading (matches `title` for these Wikipedia pages)          |
| `content`  | Cleaned article text used for indexing and snippets               |
| `source`   | Originating domain (`en.wikipedia.org` for all current documents) |
| `category` | One of the 7 tourism categories listed above                      |

## 11. Running LakbaySearch

Start the Flask app:

```powershell
python app.py
```

Then open:

```
http://127.0.0.1:5000/
```

The TF-IDF index is built once, in memory, when the app starts (this is
fast because the corpus is small). The SQLite analytics database and
table are also created automatically at startup if they don't already
exist.

## 12. Using Search

Example queries you can try:

- `best beaches near Manila`
- `historical places in Cebu`
- `mountains in the Philippines`
- `nature attractions Palawan`
- `cultural attractions in Manila`

You can also search for an exact place name (e.g. `Boracay`) or a topic
that isn't a page title at all (e.g. `diving spots in Cebu`, which
matches Moalboal's article text even though "diving" is not in its
title).

## 13. Search Filters

On the results page, two optional filters are available:

- **Category** — narrows results to one of the 7 tourism categories
  (e.g. only "Beaches").
- **Source** — narrows results to one originating domain.

Both filters resubmit the same query as a normal GET request to
`/search` with an added `category` or `source` parameter, so results
stay bookmarkable/shareable.

## 14. Search Analytics

Visit:

```
http://127.0.0.1:5000/analytics
```

This page reads real data from `data/analytics.db` (SQLite) and shows:

- **Total Searches** — count of all valid (non-empty) searches performed
- **Zero-Result Searches** — how many of those returned no matches
- **Average Search Time** — mean `execution_time_ms` across all recorded
  searches, in milliseconds
- **Most Searched Queries** — most frequent queries, grouped
  case-insensitively (so "Palawan," "palawan," and "PALAWAN" count as
  one query)
- **Most Frequent Top Result** — which documents appear as the #1 result
  most often
- **Recent Searches** — the most recent searches (query, date/time,
  result count, top result, execution time), newest first

Analytics are recorded automatically after every real search — empty
queries are never logged, and refreshing the `/analytics` page itself
does not create new records.

## 15. TF-IDF Explanation

**Term Frequency (TF)** measures how often a word appears within one
document. If a page about Boracay says "beach" many times, "beach" gets
a high TF score for that page.

**Inverse Document Frequency (IDF)** measures how _rare_ a word is
across the whole corpus. A word that shows up in almost every document
(like "Philippines") gets a low IDF, because it doesn't help tell
documents apart. A word that only shows up in a few documents (like
"Chocolate Hills") gets a high IDF.

**TF-IDF** multiplies these together. Common words that appear
everywhere get pulled down in importance, even if they're frequent in
one document, because they aren't useful for distinguishing that
document from the rest. Rare, specific words that show up a lot in one
document but rarely elsewhere get boosted, because they're a strong
signal of what that document is actually about.

## 16. Cosine Similarity Explanation

Every document (and every query) is turned into a vector — a list of
numbers, one per word in the vocabulary, based on that word's TF-IDF
weight. Cosine similarity measures the _angle_ between the query's
vector and each document's vector, producing a score from 0 (no shared
meaningful words) to 1 (identical word-weight pattern). A higher score
generally means more textual overlap with the query, not proof that the
result is correct.

**Important:** values like "17.4% match" shown in the UI are a
user-friendly percentage form of the cosine similarity score. They are
**not** a probability that the result is the right answer — they only
describe how much vocabulary the query and that document share.

## 17. Difference from Simple Keyword Matching

A simple approach like `SELECT * FROM pages WHERE title LIKE '%keyword%'`
can only find pages whose _title_ literally contains the search word,
and it can't tell a strong match from a weak one — a page either matches
or it doesn't.

LakbaySearch instead represents every document (title, heading, and full
body text) as a TF-IDF vector and ranks all documents by similarity to
the query vector. This is why, for example, searching `diving spots in
Cebu` can find the Moalboal page — the word "diving" appears nowhere in
any page title, but it does appear in Moalboal's article text, and
TF-IDF/cosine similarity is able to use that. A `LIKE '%diving%'` search
against titles alone would have returned nothing.

## 18. Known Limitations

Documented honestly, based on the actual evaluation in
`SEARCH_EVALUATION.md`:

- The corpus is small — 47 documents, all sourced from Wikipedia. Search
  quality is limited by what's actually in that corpus.
- TF-IDF does not understand meaning the way a modern semantic/AI search
  system would — it only measures shared vocabulary.
- Queries like `best beaches near Manila` can rank Manila-related pages
  (the city itself, Intramuros, San Agustin Church) above actual beach
  destinations, because TF-IDF does not understand geographic distance
  or the meaning of "near," and has no concept of "beach" as a category
  distinct from "city."
- No spelling correction is implemented — a misspelled query simply
  won't match the correctly-spelled term.
- No semantic embeddings or machine learning ranking model is used.
- No personalization or user accounts.
- The crawler is intentionally small-scale and controlled (a fixed seed
  list, not a general-purpose internet crawler), so it cannot expand the
  corpus on its own.
- Rankings are based purely on textual similarity, not popularity,
  quality, or authority of the source page.

These are presented as reasonable, expected tradeoffs for a small
educational information-retrieval project — not as defects to be
ashamed of. Part of the point of the project is being able to explain
_why_ these limitations exist.

## 19. Future Improvements

Realistic next steps, none of which are currently implemented:

- A larger corpus, and additional Philippine tourism sources beyond
  Wikipedia
- Stemming or lemmatization (so "beach" and "beaches" are treated as the
  same term)
- Spelling suggestions for queries with no matches
- Geographic metadata (e.g. actual coordinates) to support real
  "near me" style queries
- More precise, possibly automated category classification
- Semantic/embedding-based search to complement TF-IDF
- Query expansion (e.g. automatically treating "beach" and "shoreline"
  as related)
- Result pagination for larger corpora
- Further ranking improvements informed by ongoing evaluation

## 20. Evaluation Approach

See `SEARCH_EVALUATION.md` for the full evaluation: 8 real queries were
run against the live application, each documented with its actual top
results, relevance scores, and an honest Pass / Partial Pass / Fail
judgment — including cases where the ranking does not fully match user
intent, and an explanation of why.
