# Venue hunt, domain G3: journals whose own statistics make a first decision by 31 Oct 2026 plausible

Compiled 20 Sept 2026. Question: if the paper goes in between 22 and 30 Sept 2026, which peer-reviewed journals in NLP, computational linguistics, ML, data science or digital humanities would plausibly return a FIRST EDITORIAL DECISION by 31 Oct 2026, judged only by the journal's own published turnaround figure?

Method: every fact below comes from the journal's or publisher's own pages (homepage, "about", "journal metrics" / "journal insights" / "journal statistics", instructions for authors, APC pages). Pages were read directly (WebFetch) or, where the publisher blocks automated fetches (Springer Nature, Elsevier/ScienceDirect, MDPI, PeerJ), in the browser pane. Words in quotation marks are verbatim. "Not stated" means the page was read and the item is not on it. Taylor & Francis (tandfonline.com) could not be opened at all: its Cloudflare bot check never cleared, so the Journal of Quantitative Linguistics entry is incomplete and says so.

One distinction matters throughout. Elsevier's "Submission to first decision" and Nature's "Submission to first editorial decision" are **desk-triage** numbers (Nature's definition: "the median time in days from when the journal receives a manuscript submission to when the submission is either sent out for peer review or rejected"). Elsevier separately publishes "Submission to decision after review", which is the number that matters for a substantive decision. Springer's "Submission to first decision (median)", PeerJ's "Time to first decision (median)", PLOS's "Time to First Decision", MDPI's "first decision is provided to authors approximately N days after submission" and IEEE Access's "4 weeks from submission to an accept/reject decision" all include reviewed manuscripts. Verdicts below are for a **reviewed** first decision; the desk figure is given separately where it exists.

Date arithmetic used: 22 Sept + N days and 30 Sept + N days, against 31 Oct (39 and 31 days away respectively).

---

## 0. Ranked summary (credibility first, speed second)

| # | Journal | Official turnaround (quoted) | Reviewed decision by 31 Oct? | Fee | Admissions-reader respect |
|---|---|---|---|---|---|
| 1 | **IEEE Access** (IEEE) | "On average, the IEEE Access peer review process takes 4 weeks from submission to an accept/reject decision notification" | **Yes** (late-window submissions land 26–28 Oct on the average) | $2,160 APC, no fee-free route | Recognised name (IEEE, SCIE, IF 4.2); insiders know it is a mega-journal |
| 2 | **Language Resources and Evaluation** (Springer / ELRA) | "Submission to first decision (median) 36 days" | **Borderline**: 28 Oct from 22 Sept, 5 Nov from 30 Sept | Free via subscription route; OA optional at $3,590 | High: established field journal, SCIE, DBLP, society-affiliated |
| 3 | **PeerJ Computer Science** | "Time to first decision (median): 35" | **Borderline-to-Yes**: 27 Oct from 22 Sept, 4 Nov from 30 Sept | $2,155 APC | Medium: SCIE, dblp, IF 2.9; less known outside CS |
| 4 | **Machine Learning with Applications** (Elsevier) | "1 day Submission to first decision", "38 days Submission to decision after review" | **Borderline**: 30 Oct from 22 Sept, 7 Nov from 30 Sept | $3,030 APC | Medium: Elsevier, Scopus + ESCI, IF 6.1 |
| 5 | **Data in Brief** (Elsevier), dataset paper only | "7 days Submission to first decision", "48 days Submission to decision after review" | Desk **Yes**; reviewed **Borderline-No** (9–16 Nov) | $1,600 APC | Medium: recognised data-article venue, Scopus + ESCI |
| 6 | **Scientific Data** (Nature), dataset paper only | "Submission to first editorial decision (median days): 11", "Submission to acceptance (median days): 162" | Desk **Yes**; reviewed **No** | $2,690 APC | High: Nature Portfolio, IF 7.2 |
| 7 | **Computational Linguistics** (ACL / MIT Press) | "Average time to first decision (46 days)" | **Borderline-to-No**: 7 Nov from 22 Sept | Free | Highest on this list for NLP |
| 8 | **PLOS ONE** | "Time to First Decision: 45 days (median, Jan-Jun 2023)"; "Time to First Editorial Decision: 17 days" | Desk yes; reviewed **No** (6–14 Nov) | $2,477 APC, fee-assistance programme | Recognised name; mega-journal |
| 9 | **Scientific Reports** (Nature) | "We aim to make our first decisions on your manuscript within 45 days of submission" (a target, no measured figure) | **No** on the stated target (6–14 Nov) | $2,850 APC | Recognised name; mega-journal |
| 10 | **Information** (MDPI) | "a first decision is provided to authors approximately 18.7 days after submission" | **Yes** (by 19 Oct even from 30 Sept) | CHF 1,800 | Low with anyone who knows publishing (see §16) |
| 11 | **Data** (MDPI), dataset paper | "approximately 19.2 days" | **Yes** | CHF 1,600 | Low, as above |
| 12 | **Applied Sciences** (MDPI) | "approximately 15 days" | **Yes**, weak scope fit | CHF 2,400 | Low, as above |
| 13 | **Electronics** (MDPI) | "approximately 14.8 days" | **Yes**, poor scope fit | CHF 2,400 | Low, as above |
| — | Natural Language Processing (Cambridge) | Not stated anywhere official | Cannot judge | $3,655 APC, waiver on request | High (CUP, SCIE, DBLP) |
| — | Journal of Quantitative Linguistics (T&F / IQLA) | Page unreachable (Cloudflare) | Cannot judge | Hybrid; free subscription route | High in quantitative linguistics |
| — | Natural Language Processing Journal (Elsevier) | "10 days" desk, "63 days Submission to decision after review" | **No** (24 Nov–2 Dec) | $915 APC (discounted to 30 Dec 2026) | Medium-low: young, Scopus + dblp, no IF yet |
| — | Intelligent Systems with Applications (Elsevier) | "2 days" desk, "50 days" after review | **No** | $2,830 | Medium |
| — | Array (Elsevier) | "9 days" desk, "64 days" after review | **No** | $2,770 | Medium |
| — | Heliyon (Cell Press) | Only "207 days Submission to acceptance"; no first-decision figure | **No** | $2,270 | Low-medium |
| — | Frontiers in Artificial Intelligence | No per-journal figure; publisher-wide "average review time is under 90 days" | **No** | CHF 2,195 | Contested (see §8) |
| — | Frontiers in Computer Science | Same; no NLP section | **No** | CHF 1,495 | Contested |
| — | Journal of Open Source Software | No figure; reviewers asked to finish "in 4-6 weeks"; repo must have "at least six months of public history" | **No** | Free | Respected among research-software people; unknown to most admissions readers |

**Which ones a strong university admissions reader would respect.** Computational Linguistics, Scientific Data, Language Resources and Evaluation, Natural Language Processing (Cambridge) and the Journal of Quantitative Linguistics are the venues whose names carry weight with anyone who checks. IEEE Access, Scientific Reports and PLOS ONE are recognised names that read well to a generalist and are discounted by insiders as mega-journals, but none is embarrassing. PeerJ CS, the Elsevier OA titles and Data in Brief are respectable and neutral. Frontiers and Heliyon are neutral-to-negative depending on the reader. MDPI titles are the fastest on this list and the only ones that clear 31 Oct with room to spare, but a reader who knows publishing will discount them; that trade is the whole decision.

**Practical reading.** Only IEEE Access states a substantive-decision average inside the window. LRE, PeerJ CS and MLWA are coin-flips that improve if the paper goes in on 22–23 Sept rather than 30 Sept. CL is the best home for the paper but its own average (46 days) misses by a week. For the 840-essay corpus as a separate dataset paper, Data in Brief is the realistic fast option and Scientific Data the prestigious slow one.

---

## 1. Language Resources and Evaluation (Springer, with ELRA)

- **URL:** https://link.springer.com/journal/10579
- **Turnaround (quoted, where):** Homepage, "Journal metrics" block: "Submission to first decision (median) 36 days". Also there: "Journal Impact Factor 2.0 (2025)", "5-year Journal Impact Factor 2.4 (2025)", "Downloads 389.7k (2025)".
- **Fees:** Hybrid. "How to publish with us" page: "The current APC for Language Resources and Evaluation is £2590.00 GBP / $3590.00 USD / €2890.00 EUR." and "Authors can also choose to publish under the subscription publishing model (no APC charges apply); both options will be offered after the paper has been accepted." No waiver text on the journal pages.
- **Author eligibility (quoted):** Submission guidelines, "Cover letter": "The cover letter should include at least one of the following items for each contributing author, to show their experience and commitment to the field: a verified ORCID profile that is up-to-date with publications and linked to the author's institution; a link to the author's university homepage with completed research profile and recent publications; a link to an up-to-date online Curriculum Vitae. If none of these are available, add a paragraph detailing each author's relevant experience." Also: "For authors that are (temporarily) unaffiliated we will only capture their city and country of residence". No degree or institutional-email rule; an unaffiliated or high-school author can submit, with a CV link or an experience paragraph.
- **Review type:** "This journal follows a single-blind reviewing procedure." "at least two referees per manuscript".
- **Preprint policy:** Not on the journal page; Springer's journal-policies page: "Posting of preprints is not considered prior publication and will not jeopardize consideration at Springer Nature journals."
- **Indexing claimed on the page:** "ACM Digital Library ... DBLP ... SCOPUS, Science Citation Index Expanded (SCIE) ... INSPEC ... MLA International Bibliography" and others.
- **Fit:** Scope: "the acquisition, creation, annotation, and use of language resources, together with methods for evaluation of resources, technologies, and applications." Paper types: full-length "typically 18-25 pages", project notes "typically 8-10 pages". Fit is good if the paper is framed around the multilingual corpus and the evaluation methodology; the homepage's newest item on 20 Sept was "Trends and challenges in authorship analysis: a review of ML, DL, and LLM approaches", so the topic is on the editors' radar. Note: "LRE asks that resources described in our publications be made publicly available".
- **Credibility:** Springer; "Societies and partnerships: ELRA Language Resources Association"; SCIE and Scopus; no concerns.
- **Verdict:** **Borderline.** 36-day median: 28 Oct from a 22 Sept submission, 5 Nov from 30 Sept. Half of manuscripts take longer than the median, and the figure includes desk rejections.

## 2. Journal of Quantitative Linguistics (Taylor & Francis, for the International Quantitative Linguistics Association)

- **URL:** https://www.tandfonline.com/journals/njql20 (metrics at .../about-this-journal#journal-metrics)
- **Turnaround:** **Not retrievable.** Every tandfonline.com URL returned HTTP 403 to fetches and a Cloudflare "Performing security verification" page in the browser that never cleared. Search snippets of the official page show only T&F's definition of the metric ("the average (median) number of days for a manuscript submitted to the journal to receive a first decision ... includes manuscripts which are not sent for peer review"), not the number. Someone must open the page by hand.
- **Fees:** Hybrid ("Open Select"); subscription route free; APC amount not retrieved.
- **Author eligibility:** Not retrieved. **Review type:** About-page snippet: "anonymized refereeing by at least two anonymous referees". **Preprint policy:** not retrieved. **Indexing:** not retrieved from the official page.
- **Fit:** Scope snippet: "Work published in JQL is expected to advance theoretical understanding of any given language domain in mathematical and/or statistical terms." Good for a stylometry paper that makes a quantitative-linguistic claim; weaker for a pure attribution-accuracy paper.
- **Credibility:** T&F, IQLA society journal; no concerns.
- **Verdict:** **Cannot judge** without the number.

## 3. Computational Linguistics (ACL / MIT Press)

- **URL:** https://cljournal.org/ (MIT Press: https://direct.mit.edu/coli, which returns 403 to fetches)
- **Turnaround (quoted, where):** cljournal.org front page: "Average time to first decision (46 days)". Submission guidelines: short papers "may be reviewed more quickly" (no figure).
- **Fees:** "Computational Linguistics does not charge processing or publication charges." "has been Open Access since the beginning of 2009."
- **Author eligibility (quoted):** None stated. Submission guidelines contain no restriction based on affiliation or student status.
- **Review type:** "Computational Linguistics does not do double-blind review: authorship of submissions is known to the editorial board and the reviewers."
- **Preprint policy:** Not stated. The bar is "has not been published in or submitted for publication to another refereed archival publication, and has not appeared in any conference or workshop proceedings"; a preprint is neither, but that is inference.
- **Indexing claimed:** Not on cljournal.org; MIT Press page unreachable. The front page cites "CL impact factor (9.3)".
- **Fit:** "the primary archival forum for research on computational linguistics and natural language processing." Direct fit. Lengths: long "typically between 30 and 40 journal pages", short "at least 15 and up to 25 journal pages", squibs "must not exceed eight pages of content".
- **Credibility:** ACL society journal, MIT Press; the top venue on this list for NLP.
- **Verdict:** **Borderline-to-No.** 46 days from 22 Sept is 7 Nov. Only a fast desk decision beats 31 Oct.

## 4. Natural Language Processing (Cambridge University Press; formerly Natural Language Engineering)

- **URL:** https://www.cambridge.org/core/journals/natural-language-processing
- **Turnaround:** **Not stated** on the homepage, About, review-process or author-instruction pages.
- **Fees:** Gold OA, mandatory: "This journal is a fully open access journal, which means all articles are published as Gold Open Access". Fees page: "GBP (£) 2610" / "USD ($) 3655". Waivers: "Any corresponding author of a research article who is not covered by one of the above funding routes can request a discount or full waiver of their APC"; no fee for "Book Reviews, Emerging Trends, Industry Watch, NLP for Social Good, Responsible NLP".
- **Author eligibility (quoted):** "We require all corresponding authors to identify themselves using ORCID when submitting a manuscript to this journal." Affiliations "at which the research presented was conducted and/or supported and/or approved." No degree rule. "All authors of papers submitted to Natural Language Processing agree to be invited to peer review other journal submissions."
- **Review type:** "This journal uses a single-anonymized model of peer review", "at least 2 external reviewers".
- **Preprint policy:** "Deposition of a preprint on the author's personal website, in an institutional repository, or in a preprint archive shall not be viewed as prior or duplicate publication."
- **Indexing claimed:** "Impact Factor (2025): 1.6", "163 out of 210 in Computer Science, Artificial Intelligence (2025 Journal Citation Reports)"; Scopus, SCIE, DBLP, INSPEC on the indexing page.
- **Fit:** Strong: "novel NLP methods and models (including the latest deep learning methods and large language models), particularly those reporting finding from multilingual and low-resource language projects".
- **Credibility:** CUP, since 1995, SCIE; no concerns.
- **Verdict:** **Cannot judge** from official data; the APC is a separate obstacle unless the waiver is granted.

## 5. PeerJ Computer Science

- **URL:** https://peerj.com/computer-science/ (FAQ: https://peerj.com/computer-science/faq-cs/)
- **Turnaround (quoted, where):** FAQ, "Where are the key metrics": "Time to first decision (median): 35", "Time to publication (median): 30". Homepage "Key Journal Statistics": "33% Acceptance rate", "32 days Acceptance to publication", "2.9 (2025) Journal impact factor", "6.1 (2025) CiteScore".
- **Fees:** "The Article Processing charge is $2,155 (plus local taxes)"; lifetime memberships as an alternative; institutional memberships may cover it. Waivers only for World Bank low-income countries, "one waiver per person, per year".
- **Author eligibility:** None stated beyond authorship criteria; no affiliation or degree rule.
- **Review type:** Single-blind pre-publication review; reviewers may sign; optional published review history.
- **Preprint policy:** Accepts submissions "which have previously appeared on preprint servers (including PeerJ Preprints and arXiv)".
- **Indexing claimed:** "Pubmed Central (PMC), Scopus, Web of Science SCIE, Journal Citation Reports, Google Scholar, Europe PMC, DOAJ, dblp, CiteSeerX ... Inspec".
- **Fit:** Discipline list includes "AI, Computer Vision & Natural Language Processing" and "Data Handling & Mining"; soundness-based criteria. Good fit.
- **Credibility:** Footer now reads "PeerJ is part of Taylor & Francis Group"; SCIE, dblp; no concerns.
- **Verdict:** **Borderline-to-Yes.** 35-day median: 27 Oct from 22 Sept, 4 Nov from 30 Sept. Submit in the first days of the window.

## 6. PLOS ONE

- **URL:** https://journals.plos.org/plosone/s/journal-information (fees: https://www.plos.org/publication-fees)
- **Turnaround (quoted, where):** Journal Information, "Journal Timings": "Time to First Editorial Decision: 17 days", "Time to First Decision: 45 days", "Time to Final Decision: 87 days", "Time to Acceptance: 188 days", "Time to Publication: 204 days", "Acceptance Rate: 30.74%", all "(median, Jan-Jun 2023)". Nothing newer is posted.
- **Fees:** Research articles "$2,477". Research4Life Group A free, Group B "$940". "Publication Fee Assistance (PFA)" for "authors unable to pay all or part of their publication fees and who can demonstrate financial need", decided "within 10 business days", applied for at submission; "requests made during the review process or after acceptance will not be considered."
- **Author eligibility (quoted):** "The corresponding author must provide an ORCID iD upon submission". No degree or affiliation rule.
- **Review type:** "single-anonymized peer review", optional published peer-review history.
- **Preprint policy:** Preprints allowed and facilitated.
- **Indexing claimed:** "Crossref, Dimensions, DOAJ, Google Scholar, PubMed, PubMed Central, Scopus, and Web of Science" and others. No IF shown by policy.
- **Fit:** "over two hundred subject areas across science, engineering, medicine, and the related social sciences and humanities"; evaluates "scientific validity, strong methodology, and high ethical standards—not perceived significance." No NLP audience.
- **Credibility:** PLOS (non-profit), Scopus + WoS. Caveat: the posted timings are three years old.
- **Verdict:** Desk (17 days) yes; **reviewed decision No** (45-day median lands 6–14 Nov).

## 7. Scientific Reports (Nature Portfolio)

- **URL:** https://www.nature.com/srep/ (About: /srep/about; editorial process: /srep/about/editorial-process; fees: /srep/open-access). The URL /srep/journal-metrics is "Page not found".
- **Turnaround (quoted, where):** Editorial process, Stage 4: "We aim to make our first decisions on your manuscript within 45 days of submission." No measured median is published. About page: "Journal Impact Factor: 4.9 (2025)", "Downloads: 536,857,704".
- **Fees:** "The current APC, subject to VAT or local taxes where applicable, is: £2290.00/$2850.00/€2490.00". Waivers for "the world's lowest income countries"; "Requests for APC waivers and discounts from other authors will be considered on a case-by-case basis, and may be granted in cases of financial need ... should be made at the point of manuscript submission".
- **Author eligibility:** No degree, email or ORCID requirement stated; affiliation "where the majority of their work was done".
- **Review type:** "By policy, reviewers are not identified to the authors, except at the request of the reviewer." Two or three reviewers.
- **Preprint policy:** "allows and encourages prior publication on recognized community preprint servers".
- **Indexing claimed:** "Web of Science, PubMed, PubMed Central, Scopus, Dimensions, Google Scholar, DOAJ and SAO/NASA ADS".
- **Fit:** "original research from across all areas of the natural sciences, psychology, medicine and engineering"; computer science sits under engineering; no NLP section.
- **Credibility:** Springer Nature, SCIE; mega-journal.
- **Verdict:** **No** on the stated target (45 days is 6–14 Nov); no measured figure supports anything faster.

## 8. Frontiers in Artificial Intelligence

- **URL:** https://www.frontiersin.org/journals/artificial-intelligence (About: .../about; fees: .../for-authors/publishing-fees)
- **Turnaround:** **Not stated** on any journal page. Publisher-wide only: "our average review time is under 90 days, with many journals and sections completing reviews in significantly less time."
- **Fees:** "A-Type Articles: CHF 2,195", "B-Type Articles: CHF 1,750", C-type 0. "Authors in countries classified by the World Bank as low or lower-middle income countries may be eligible for discounts"; publisher-wide, "Authors and institutions with insufficient funding are eligible for discounts ... as long as their article passes our independent and rigorous peer review."
- **Author eligibility (quoted):** "Where possible, we advise authors without institutional email addresses to link a verified ORCID profile to their Loop account." ORCID not mandatory; unaffiliated authors are contemplated.
- **Review type:** "The journal uses single anonymized peer review"; interactive review; reviewer names published on accepted articles.
- **Preprint policy:** Sharing on preprint servers allowed "provided that the server imposes no restrictions upon the author's full copyright and re-use rights".
- **Indexing claimed:** "PubMed Central (PMC), Scopus, DOAJ, Crossref, Digital Biography & Library Project (dblp), Web of Science Emerging Sources Citation Index (ESCI)"; "6.7 Impact Factor", "8 CiteScore".
- **Fit:** Strong via the specialty section "Computational Linguistics and Natural Language Processing", whose scope lists multilingual and cross-lingual processing, text classification, deception detection and language resources.
- **Credibility:** Frontiers Media; ESCI not SCIE; the publisher's reputation is contested in the community (mass special issues, past listing debates); nothing about that is on its own pages.
- **Verdict:** **No.** No per-journal first-decision figure; the publisher average is to final decision and exceeds the window.

## 9. Frontiers in Computer Science

- **URL:** https://www.frontiersin.org/journals/computer-science
- **Turnaround:** Not stated; same publisher-wide line as §8.
- **Fees:** "A-Type Articles: CHF 1,495", "B-Type: CHF 990", C 0; same fee support text.
- **Eligibility / review / preprints:** identical publisher policies to §8.
- **Indexing claimed:** "Scopus, Web of Science (ESCI), and the DOAJ", dblp, Inspec; "Impact Factor: 3.4", "CiteScore: 6.2".
- **Fit:** Weak. Sections are Computer Graphics and Visualization, Computer Security, Computer Vision, Digital Education, Human-Media Interaction, Mobile and Ubiquitous Computing, Networks and Communications, Software, Theoretical Computer Science; no NLP or ML section.
- **Verdict:** **No** (timing and scope).

## 10. Heliyon (Cell Press / Elsevier)

- **URL:** https://www.sciencedirect.com/journal/heliyon (Insights: .../about/insights). cell.com/heliyon pages return 403.
- **Turnaround (quoted, where):** Insights, "Publishing timeline": "207 days Submission to acceptance", "3 days Acceptance to online publication". **No time-to-first-decision or review-time figure is shown.**
- **Fees:** "Article Publishing Charge (APC): USD 2,270 (excluding taxes)". Elsevier-wide Research4Life waivers (Group A free, Group B 50%); other requests "case-by-case".
- **Author eligibility / review type:** Not retrievable (author guide behind bot check). **Preprint policy:** Elsevier-wide "Authors can share their preprint anywhere at any time".
- **Indexing claimed:** "Scopus, Science Citation Index Expanded (SCIE), Directory of Open Access Journals (DOAJ)"; "7.8 CiteScore", "3.6 Impact Factor".
- **Fit:** All-science mega-journal; "Computer Science (General)" among subject areas.
- **Credibility:** Elsevier/Cell Press; SCIE claimed on its page; a mega-journal with a mixed reputation.
- **Verdict:** **No.** The only timeline it publishes is 207 days to acceptance.

## 11. IEEE Access

- **URL:** https://ieeeaccess.ieee.org/ (Rapid Peer Review: /about/rapid-peer-review/; APC: /about/article-processing-charges/; bibliometrics: /about/bibliometrics/)
- **Turnaround (quoted, where):** Rapid Peer Review page: "On average, the IEEE Access peer review process takes 4 weeks from submission to an accept/reject decision notification." and "Submission-to-publication time typically takes 4 to 6 weeks, depending on how long it takes the authors to submit final files after they receive the acceptance notification." About page: "Average Acceptance Rate: 20%".
- **Fees:** "The APC is $2,160 per article (plus applicable local taxes)"; "no page limit". IEEE members 5%, society members 20%; low-income-country discount only "if all authors are located in a country eligible"; student membership does not qualify. No hardship waiver for US authors.
- **Author eligibility (quoted):** "The submitting author is required to have an ORCID ID associated with their account. The ORCID profile must be publicly visible and populated." No degree or affiliation rule.
- **Review type:** "a minimum of 2 independent reviewers using a single-anonymized peer review process"; "binary decision process ... accept or reject decision with constructive feedback"; rejected-for-updates papers may be resubmitted once.
- **Preprint policy:** IEEE Author Center: preprints may go on "arXiv.org, TechRxiv.org, or any not-for-profit preprint server approved by the Publication Services and Products Board"; "IEEE does not consider this to be a form of prior publication."
- **Indexing claimed:** "Science Citation Index Expanded (Clarivate Analytics)", "Web of Science", "Journal Citation Reports/Science Edition", Scopus, Ei Compendex, Inspec, DOAJ; "Impact factor of 4.2", "CiteScore of 9.3".
- **Fit:** "Multidisciplinary topics, or applications-oriented articles that do not fit within the scope of IEEE's traditional journals." Fine but generic.
- **Credibility:** IEEE; SCIE; a very high-volume mega-journal whose prestige sits below IEEE Transactions.
- **Verdict:** **Yes, late-window borderline.** 4-week average: 20 Oct from 22 Sept, 28 Oct from 30 Sept. Any reviewer delay pushes past 31 Oct.

## 12. Machine Learning with Applications (Elsevier)

- **URL:** https://www.sciencedirect.com/journal/machine-learning-with-applications (Insights: .../about/insights)
- **Turnaround (quoted, where):** Insights, "Publishing timeline": "1 day Submission to first decision", "38 days Submission to decision after review", "89 days Submission to acceptance", "7 days Acceptance to online publication".
- **Fees:** "Article Publishing Charge (APC): USD 3,030 (excluding taxes)" (live page on 20 Sept; an earlier search snapshot said USD 2,460, so the price has risen). OA mandatory. Research4Life waivers; GPOA geographical pricing.
- **Author eligibility:** None stated; ORCID encouraged.
- **Review type:** Guide for authors: "single anonymized review process ... minimum of two reviewers".
- **Preprint policy:** Elsevier-wide: "Authors can share their preprint anywhere at any time".
- **Indexing claimed:** "Directory of Open Access Journals (DOAJ), Ei Compendex, Scopus, Emerging Sources Citation Index (ESCI)"; "12.6 CiteScore", "6.1 Impact Factor".
- **Fit:** "encompasses all aspects of research and development in ML, including but not limited to data mining, computer vision, natural language processing (NLP)". Good.
- **Credibility:** Elsevier gold OA, Scopus + ESCI, IF 6.1; young (2020), applications-oriented.
- **Verdict:** **Borderline.** The 1-day "first decision" is desk triage; the reviewed decision averages 38 days: 30 Oct from 22 Sept, 7 Nov from 30 Sept.

## 13. Array (Elsevier)

- **URL:** https://www.sciencedirect.com/journal/array (Insights: .../about/insights)
- **Turnaround (quoted):** "9 days Submission to first decision", "64 days Submission to decision after review", "130 days Submission to acceptance", "6 days Acceptance to online publication".
- **Fees:** "USD 2,770 (excluding taxes)"; OA mandatory; Research4Life/GPOA.
- **Eligibility / review / preprints:** none stated; "single anonymized review process"; "sharing preprints on a preprint server will not count as prior publication".
- **Indexing claimed:** "Scopus, Directory of Open Access Journals (DOAJ), Emerging Sources Citation Index (ESCI)"; "10.1 CiteScore", "5.3 Impact Factor".
- **Fit:** "multidisciplinary journal encompassing a broad spectrum of topics in computer science, including Artificial Intelligence, Machine Learning and Robotics"; technical notes up to 10 pages. Acceptable, not NLP-specific.
- **Verdict:** **No.** Reviewed decision averages 64 days (late Nov–early Dec).

## 14. Intelligent Systems with Applications (Elsevier)

- **URL:** https://www.sciencedirect.com/journal/intelligent-systems-with-applications (Insights: .../about/insights)
- **Turnaround (quoted):** "2 days Submission to first decision", "50 days Submission to decision after review", "133 days Submission to acceptance", "8 days Acceptance to online publication".
- **Fees:** "USD 2,830 (excluding taxes)"; OA mandatory.
- **Eligibility / review / preprints:** none stated; "single-blind review process, utilizing a minimum of two (2) external referees"; Elsevier preprint policy.
- **Indexing claimed:** "Scopus, Directory of Open Access Journals (DOAJ)", SJR, SNIP; "13.1 CiteScore", "5.5 Impact Factor".
- **Fit:** Intelligent systems "applied to all aspects of human enterprize"; language is not named. Moderate.
- **Verdict:** **No.** Reviewed decision averages 50 days (11–19 Nov).

## 15. Natural Language Processing Journal (Elsevier, ISSN 2949-7191)

- **URL:** https://www.sciencedirect.com/journal/natural-language-processing-journal (Insights: .../about/insights)
- **Turnaround (quoted):** "10 days Submission to first decision", "63 days Submission to decision after review", "177 days Submission to acceptance", "5 days Acceptance to online publication".
- **Fees:** "Discounted Article Publishing Charge (APC): USD 915 (excluding taxes). This discount is valid for articles submitted by 30 December 2026. Full APC without discount: USD 1,830 (excluding taxes)." OA mandatory.
- **Eligibility / review / preprints:** none stated; "single anonymized review process ... minimum of two reviewers"; "sharing preprints, such as on a preprint server, will not count as prior publication".
- **Indexing claimed:** "Directory of Open Access Journals (DOAJ), dblp - Computer Science Bibliography, Scopus"; "9.1 CiteScore"; no Impact Factor shown.
- **Fit:** Best topical fit among the Elsevier titles: "trustworthy, interpretable, explainable human-centered and hybrid Artificial Intelligence as it relates to all aspects of human language".
- **Credibility:** Elsevier, launched 2022, Scopus + dblp, no WoS metric yet; cheapest APC on the list.
- **Verdict:** **No.** Reviewed decision averages 63 days (24 Nov–2 Dec); only the 10-day desk decision precedes 31 Oct.

## 16. MDPI: Applied Sciences, Information, Electronics, Data

Common facts (from each journal's instructions page and https://www.mdpi.com/apc):
- **Eligibility (quoted):** "If one or all the authors are not currently affiliated with a university, institution or company, or have not been during the development of the manuscript, they should list themselves as an 'Independent Researcher'." ORCID optional ("If a manuscript is accepted for publication, we will add an icon linking to your online ORCID profile"). No institutional-email or degree rule stated. A high-school author can submit.
- **Review type:** "The journal operates under a single-anonymized peer review system (also known as 'single-blind') ... At least two review reports are collected."
- **Preprint policy:** "accepts submissions that have previously been made available as preprints provided that they have not undergone peer review." (The MDPI template itself "cannot be used for posting online on preprint servers".)
- **Waivers (quoted):** "Support levels vary by journal, discipline, and eligibility pathway, and may range from partial discounts to full waivers ... Discounts and waivers may be available through institutional agreements, reviewer vouchers, and selected invitations issued to individual authors." No general low-income, student or hardship waiver is stated.
- **Turnaround source:** each homepage's "Journal Description" paragraph, "(median values for papers published in this journal in the first half of 2026)". The per-journal "Journal Statistics" page charts "Submission to First Decision" by month but prints no number in text.
- **Credibility note, stated plainly:** MDPI is a Basel OA publisher whose journals are Scopus- and often SCIE-indexed and COPE members, but whose reputation is contested: it appeared on Beall's list in 2014 (removed 2015), several national registers (Norway, China's CAS early-warning list) have downgraded MDPI titles, and the volume of special issues is very high (Applied Sciences: "92,752 Papers published"). A strong admissions reader who knows publishing will discount an MDPI paper; one who does not will see a Scopus/SCIE journal. These are the only journals on the list that clear 31 Oct with weeks to spare.

### 16a. Applied Sciences — https://www.mdpi.com/journal/applsci
- **Turnaround:** "manuscripts are peer-reviewed and a first decision is provided to authors approximately 15 days after submission; acceptance to publication is undertaken in 2.9 days". Stats page: rejection rate "58%" (2025), "56%" (2026, "data as of 30 June 2026").
- **Fees:** "CHF 2400". **Indexing claimed:** "Scopus, SCIE (Web of Science), Ei Compendex, Inspec"; stats page "2.9 Current Impact Factor", "6.1 CiteScore", "Q2: Engineering, Multidisciplinary".
- **Fit:** applied physics/chemistry/engineering with a "Computing and Artificial Intelligence" section; loose.
- **Verdict:** **Yes** on speed; weak scope.

### 16b. Information — https://www.mdpi.com/journal/information
- **Turnaround:** "a first decision is provided to authors approximately 18.7 days after submission; acceptance to publication is undertaken in 3.8 days". Rejection "63%" (2025), "62%" (2026).
- **Fees:** "CHF 1800". **Indexing claimed:** "Scopus, ESCI (Web of Science), Ei Compendex, dblp"; "4.3 Current Impact Factor", "8.2 CiteScore", "Q2: Computer Science, Information Systems".
- **Fit:** "information science and technology, data, knowledge and communication", with AI, data mining and information extraction; the best MDPI fit.
- **Verdict:** **Yes** (about 19 Oct even from 30 Sept).

### 16c. Electronics — https://www.mdpi.com/journal/electronics
- **Turnaround:** "approximately 14.8 days after submission; acceptance to publication is undertaken in 2.9 days". Rejection "52%" (2025), "50%" (2026).
- **Fees:** "CHF 2400". **Indexing claimed:** "Scopus, SCIE (Web of Science), CAPlus / SciFinder, Inspec, Ei Compendex"; "2.9 Current Impact Factor", "7.0 CiteScore".
- **Fit:** "the science of electronics and its applications" with "Computer Science & Engineering" and "Artificial Intelligence" subject areas; poor for a text-analysis paper.
- **Verdict:** **Yes** on speed; poor scope.

### 16d. Data — https://www.mdpi.com/journal/data (dataset paper)
- **Turnaround:** "approximately 19.2 days after submission; acceptance to publication is undertaken in 3.8 days". Rejection "68%" (2025), "59%" (2026).
- **Fees:** "CHF 1600". **Indexing claimed:** "dblp, Inspec, RePEc"; stats page "2.4 Current Impact Factor", "5.4 CiteScore", "Q2: Multidisciplinary Sciences".
- **Fit:** "the Data Descriptors section publishes descriptions of scientific and scholarly datasets (one dataset per paper). Described datasets need to be publicly deposited prior to publication, preferably under an open license"; required fields "Dataset: DOI number or link to the deposited dataset", "Dataset License"; sections "Summary, Data Description, Methods, User notes". No minimum size. Good fit for the 840-essay corpus.
- **Verdict:** **Yes.**

## 17. Journal of Open Source Software (JOSS)

- **URL:** https://joss.theoj.org/about (docs: https://joss.readthedocs.io/)
- **Turnaround:** **Not stated.** Reviewer guidelines: "We ask reviewers to complete their reviews in 4-6 weeks" and "We aim for the first pass of reviews to be completed within about 2-4 weeks." Authors "respond to reviewer comments and questions within 2 weeks" and "complete requested changes within 4-6 weeks".
- **Fees:** "JOSS is a diamond open access journal (free to read, free to publish)".
- **Author eligibility (quoted):** "You must be a major contributor to the software you are submitting, and have a GitHub account to participate in the review process." Login via ORCID. No degree or affiliation rule.
- **Review type:** "Reviews take place openly via public GitHub issues".
- **Preprint policy:** "Authors are welcome to submit their papers to a preprint server (arXiv, bioRxiv, SocArXiv, PsyArXiv etc.) at any point before, during, or after the submission and review process."
- **Indexing claimed:** Crossref DOI, Portico archiving; no Scopus/WoS statement; no impact factor.
- **Fit / gates:** "At least six months of public history prior to submission, with evidence of releases, public issues and pull requests"; "'Minor utility' packages, including 'thin' API clients, and single-function packages are not acceptable"; "Pre-trained machine learning models and notebooks are not in-scope."
- **Credibility:** Community-run under NumFOCUS; respected by research-software people; unfamiliar to most admissions readers, though the public review record is verifiable.
- **Verdict:** **No.** No official turnaround figure, the reviewer window alone is 4–6 weeks, and a package created this autumn fails the six-month public-history gate.

## 18. Data in Brief (Elsevier), dataset paper

- **URL:** https://www.sciencedirect.com/journal/data-in-brief (Insights: .../about/insights)
- **Turnaround (quoted, where):** Insights, "Publishing timeline": "7 days Submission to first decision", "48 days Submission to decision after review", "84 days Submission to acceptance", "7 days Acceptance to online publication"; "Acceptance rate 51%".
- **Fees:** "Article Publishing Charge (APC): USD 1,600 (excluding taxes)"; OA mandatory; GPOA geographical pricing; no individual waiver stated.
- **Author eligibility:** None stated. **Review type:** "single anonymized review process ... minimum of two reviewers". **Preprint policy:** "The work described has not been published previously except in the form of a preprint."
- **Indexing claimed:** "Scopus, Directory of Open Access Journals (DOAJ), PubMed Central (PMC), Emerging Sources Citation Index (ESCI)"; "3.4 CiteScore", "1.9 Impact Factor".
- **Fit:** "short, digestible data articles that describe and provide access to research data"; "All data articles must link to a repository that stores data produced and owned by either the author or the author's institution"; templated; "will not accept any submissions that contain datasets with insufficient variables or samples" (no numeric floor). Good fit for the corpus.
- **Credibility:** Elsevier; mainstream data-article venue; low IF, no reputation baggage.
- **Verdict:** Desk **Yes** (7 days); reviewed **Borderline-to-No** (48 days: 9 Nov from 22 Sept, 17 Nov from 30 Sept).

## 19. Scientific Data (Nature Portfolio), dataset paper

- **URL:** https://www.nature.com/sdata/ (metrics: https://www.nature.com/sdata/journal-impact; fees: /sdata/open-access)
- **Turnaround (quoted, where):** Journal Metrics, "Speed": "Submission to first editorial decision (median days): 11", "Submission to acceptance (median days): 162". Also "Journal Impact Factor: 7.2 (2025)", "5-year Journal Impact Factor: 9.3 (2025)". Definition on the same page: first editorial decision is "when the submission is either sent out for peer review or rejected".
- **Fees:** "The current APC, subject to VAT or local taxes where applicable, is: £2150.00/$2690.00/€2390.00". Waivers for "the world's lowest income countries"; other requests "case-by-case ... may be granted in cases of financial need ... should be made at the point of manuscript submission".
- **Author eligibility:** None stated. **Review type:** Nature Portfolio default single-anonymised. **Preprint policy:** "Nature Portfolio journals encourage posting of preprints of primary research manuscripts on preprint servers of the authors' choice".
- **Indexing claimed:** Metrics page lists JIF, SJR, SNIP (Scopus/WoS implied); no database list on the page.
- **Fit:** "Data Descriptors: describe new, open research datasets in a manner that promotes reuse, without reporting whether datasets support hypotheses or conclusions"; "For first round review we require that data are available for download and review by reviewers via any URL that allows anonymous download"; from round two, "data are public and available in a formal data repository". No minimum size. Strong fit for the corpus; the research paper itself is out of scope.
- **Credibility:** Springer Nature, IF 7.2; the most credible venue on this list and one an admissions reader will recognise.
- **Verdict:** Desk **Yes** (11 days); reviewed **No** (162-day median to acceptance).

---

## Pages that could not be opened
- tandfonline.com (Journal of Quantitative Linguistics): HTTP 403 to fetches; Cloudflare "Performing security verification" in the browser did not clear after two attempts.
- direct.mit.edu/coli (MIT Press pages for Computational Linguistics): HTTP 403; cljournal.org used instead.
- cell.com/heliyon (Heliyon author guide): HTTP 403; ScienceDirect Insights used instead.
- nature.com/srep/journal-metrics: "Page not found"; the About and Editorial-process pages used instead.
