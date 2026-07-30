# LakbaySearch — Search Evaluation

This document evaluates the actual, currently-running LakbaySearch search
engine. Every result below was captured by sending real HTTP requests to
the live Flask application (`GET /search?q=...`) against the real
47-document corpus in `data/documents.json` — nothing here is invented or
predicted in advance. Relevance scores are the `relevance_percent` values
(cosine similarity × 100) actually returned by `search_engine.py`.

This is a small, educational, keyword/vector-based search engine over a
47-page Wikipedia-derived corpus. It is evaluated here as exactly that —
not as a benchmark against a commercial search engine.

---

## Query 1: "best beaches near Manila"

**Search intent:** Find beach destinations located close to Manila.

**Expected relevant result(s):** A beach/island destination such as
Boracay, Puerto Galera, or another beach municipality reasonably near
Metro Manila.

**Top 3 actual results:**
| Rank | Title | Category | Score |
|---|---|---|---|
| 1 | Manila | Cities | 17.4% |
| 2 | Intramuros | Historical Sites | 9.8% |
| 3 | San Agustin Church (Manila) | Historical Sites | 9.2% |

**Evaluation:** No dedicated beach page appears in the top 3 (Boracay
appears further down the list with a much lower score). The engine
correctly recognized "Manila" as the dominant shared term between the
query and the corpus — "Manila" is repeated in the title/heading of the
Manila document and appears throughout Intramuros and San Agustin Church,
both of which are physically located in Manila. TF-IDF has no concept of
geographic distance and no concept of "beach" as a category distinct from
"city" — it only measures shared vocabulary. The word "beaches" alone
isn't enough to outweigh three separate strong matches on "Manila."

**Verdict: Partial Pass.** The results are not irrelevant (Manila,
Intramuros, and San Agustin Church are all legitimate Philippine tourism
pages, and the query did literally name "Manila"), but they do not answer
the actual intent of the query — finding a beach. This is a textbook
illustration of a known TF-IDF limitation, discussed further below.

---

## Query 2: "historical places in Cebu"

**Search intent:** Find historical sites in or around Cebu.

**Expected relevant result(s):** Cebu City (contains historical content
about Spanish colonial history) and/or Cebu-related cultural/historical
pages.

**Top 3 actual results:**
| Rank | Title | Category | Score |
|---|---|---|---|
| 1 | Cebu City | Cities | 21.7% |
| 2 | Sinulog | Cultural Attractions | 15.7% |
| 3 | Moalboal | Beaches | 8.2% |

**Evaluation:** Cebu City is a strong, correct match — its article
discusses Cebu's history directly. Sinulog (a Cebu-based cultural/
religious festival) is a reasonable secondary match since "historical"
and "Cebu" both overlap with its content. Moalboal, a beach town in Cebu
province, ranks third mainly because it shares the word "Cebu," not
because it is historically significant.

**Verdict: Pass.** The top result is genuinely relevant and the second
result is a defensible interpretation of "historical/cultural." The
third result is weaker but has a clearly visible low score (8.2%),
correctly signaling lower confidence rather than being presented as
equally relevant.

---

## Query 3: "mountains in the Philippines"

**Search intent:** Find mountain destinations anywhere in the country.

**Expected relevant result(s):** Any of the corpus's six Mountains-category
pages (Mount Apo, Mount Pulag, Mayon, Mount Pinatubo, Mount Banahaw, Taal
Volcano).

**Top 3 actual results:**
| Rank | Title | Category | Score |
|---|---|---|---|
| 1 | Mount Banahaw | Mountains | 8.2% |
| 2 | Mount Pinatubo | Mountains | 8.1% |
| 3 | Pagudpud | Beaches | 3.8% |

**Evaluation:** The top two results are both genuine mountain pages,
correctly ranked above everything else in the corpus. The third result,
Pagudpud (a beach municipality), scores much lower (3.8%, less than half
of #2) and only surfaces because "Philippines" appears in its text — the
low score correctly signals it is a weak match.

**Verdict: Pass.** The most relevant document category dominates the top
results, and score separation clearly distinguishes strong from weak
matches.

---

## Query 4: "nature attractions Palawan"

**Search intent:** Find nature/scenery destinations in Palawan province.

**Expected relevant result(s):** Palawan province page, and/or Palawan
municipalities known for nature (El Nido, Coron).

**Top 3 actual results:**
| Rank | Title | Category | Score |
|---|---|---|---|
| 1 | Palawan | Other | 28.3% |
| 2 | El Nido, Palawan | Beaches | 11.6% |
| 3 | Coron, Palawan | Nature | 6.8% |

**Evaluation:** All three results are genuinely Palawan destinations
known for nature tourism. This is the strongest result set of the five
required queries — likely because "Palawan" is a distinctive, low-frequency
term across the rest of the corpus (high IDF), so it strongly narrows the
match to the right documents.

**Verdict: Pass.** Highly relevant top 3, with a large, meaningful score
gap between the #1 result and the rest.

---

## Query 5: "cultural attractions in Manila"

**Search intent:** Find cultural/historical attractions within Manila.

**Expected relevant result(s):** Intramuros, San Agustin Church, Fort
Santiago, or the Manila city page itself.

**Top 3 actual results:**
| Rank | Title | Category | Score |
|---|---|---|---|
| 1 | Manila | Cities | 19.1% |
| 2 | Intramuros | Historical Sites | 14.7% |
| 3 | San Agustin Church (Manila) | Historical Sites | 10.1% |

**Evaluation:** Unlike Query 1, this query's intent (cultural attractions
in Manila) is actually well served by these exact results — Intramuros
and San Agustin Church are genuine cultural/historical landmarks in
Manila, and the Manila city page itself reasonably ranks first since it
directly matches "Manila" and discusses the city broadly, including its
cultural landmarks.

**Verdict: Pass.**

---

## Query 6: "Boracay" (exact destination name)

**Search intent:** Find the page about Boracay specifically.

**Expected relevant result(s):** The Boracay document.

**Top result:**
| Rank | Title | Category | Score |
|---|---|---|---|
| 1 | Boracay | Beaches | 63.7% |

Only one result was returned (all other documents scored 0% similarity,
so the ranking function correctly excluded them rather than padding the
list with unrelated pages).

**Evaluation:** An exact-name query performs very well, as expected —
"Boracay" appears in the title (repeated, per the indexing weighting
scheme) and throughout the content, producing by far the highest score
observed in this entire evaluation.

**Verdict: Pass.**

---

## Query 7: "xyzqwerty987654" (nonsense / zero-result query)

**Search intent:** N/A — intentionally meaningless input, used to test
zero-result handling.

**Expected relevant result(s):** None.

**Actual result:** "No relevant results were found. Try using different
or broader keywords." Zero documents returned.

**Evaluation:** The random string shares no vocabulary with any indexed
document, so every cosine similarity score is exactly 0, and
`search_engine.py` correctly excludes all zero-score matches rather than
returning arbitrary low-quality results. The Flask UI shows the friendly
no-results message rather than an empty page or an error.

**Verdict: Pass.**

---

## Query 8: "diving spots in Cebu" (wording does not match any page title)

**Search intent:** Find a place to go diving in Cebu province.

**Expected relevant result(s):** Moalboal — no document is titled
anything like "diving," but Moalboal's actual article text describes it
as "one of the best-known diving sites in the Philippines."

**Top 3 actual results:**
| Rank | Title | Category | Score |
|---|---|---|---|
| 1 | Cebu City | Cities | 17.6% |
| 2 | Sinulog | Cultural Attractions | 8.9% |
| 3 | Moalboal | Beaches | 8.4% |

**Evaluation:** This is the clearest demonstration in this evaluation of
retrieval beyond simple title matching: the word "diving" does not appear
in any document title, yet Moalboal — the one document whose body text
actually discusses diving — is successfully retrieved and ranked in the
top 3, purely from TF-IDF matching against its *content*, not its title.
A simple `WHERE title LIKE '%diving%'` search would have returned nothing
at all. At the same time, this query also shows the same "place name
dominance" limitation as Query 1: "Cebu City" outranks Moalboal simply
because it repeats "Cebu" more prominently (in its title, which is
weighted), even though it is not a diving destination.

**Verdict: Partial Pass.** Successfully demonstrates content-based
retrieval (the main point of using TF-IDF instead of exact string
matching), but the most topically relevant document (Moalboal) is not
ranked #1.

---

## Evaluation Summary

- **Queries tested:** 8
- **Pass:** 6 (historical places in Cebu; mountains in the Philippines;
  nature attractions Palawan; cultural attractions in Manila; Boracay;
  xyzqwerty987654)
- **Partial Pass:** 2 (best beaches near Manila; diving spots in Cebu)
- **Fail:** 0

### General observations

- The engine performs strongly when the query's key terms are distinctive
  within the corpus (e.g. "Palawan," "Boracay," "Banahaw") — these
  queries produced clean, correctly-ordered, highly relevant results.
- The engine performs weakest when a query combines a common, high-frequency
  place name (like "Manila" or "Cebu," which appear throughout many
  documents because they are referenced as nearby landmarks) with a
  *category concept* the corpus doesn't label explicitly (like "beach" or
  "diving"). TF-IDF has no notion that "Manila" is a city and the user
  wants something that is *not* Manila but merely *near* it.
- Zero-result handling works correctly and produces no false-positive
  matches.
- Score values (e.g. "17.4% match") were consistently useful as a
  *relative* confidence signal — weak matches were visibly and
  substantially lower-scored than strong matches in every query tested,
  even in the "Partial Pass" cases. A user scanning the percentages would
  reasonably suspect the top result wasn't a great fit for "best beaches
  near Manila," since 17.4% is a modest score compared to the 63.7% seen
  for the exact "Boracay" query.

### Strengths

- Correctly retrieves documents based on shared vocabulary in the full
  article body, not just the title (Query 8).
- Ranks distinctive, low-frequency terms very effectively (Query 4).
- Handles exact-name lookups very well (Query 6).
- Gracefully handles zero-result and nonsense queries without errors or
  irrelevant fallback content (Query 7).
- Relevance scores meaningfully separate strong and weak matches rather
  than presenting everything with equal confidence.

### Weaknesses

- Cannot interpret geographic relationships like "near" (Query 1).
- Cannot interpret implicit categories like "beach" or "diving spot" that
  aren't stated as such in the matching documents (Query 1, Query 8).
- Ranking can be dominated by a single frequently-repeated place name
  even when that document isn't the best answer to the query's actual
  intent.

### Conclusion

LakbaySearch successfully demonstrates the complete classical information
retrieval pipeline — crawling, text preprocessing, TF-IDF vectorization,
and cosine-similarity ranking — and, on 6 of 8 test queries, returns
results a human would judge genuinely relevant. The 2 "Partial Pass"
cases are not implementation bugs; they are honest, expected
demonstrations of what keyword/vector-based retrieval can and cannot do
without semantic understanding. As an educational project, this is a
successful and appropriately scoped outcome: it shows both the real
value of TF-IDF over naive substring matching (Query 8) and its
well-documented limitations compared to modern semantic search (Query 1),
which is exactly the kind of comparison a student should be able to
explain in a defense.
