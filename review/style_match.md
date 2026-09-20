# Style match: an accepted IEEE BigData High School Symposium paper vs. our draft

Prepared 20 Sept 2026 for the LangLLM submission to the IEEE BigData 2026 High School
Symposium (5 pages, IEEE CS two-column, single-blind). Companion to `review/venue_rules.md`.

## How the paper was found (so the search can be reproduced)

- The 2024 edition (1st, "Undergraduate and High School Symposium", Washington DC, 15 Dec
  2024) published its papers in the main BigData 2024 proceedings with no session label.
  The symposium site (`studentpapers-bigdata2024.netlify.app`) gives the agenda (18 oral
  papers at 12 minutes, 12 poster papers, one Best Paper award) but no paper list; the
  conference program PDF lists the session (Regency C, 9:00-17:00, chairs Xuan Wang and
  Yanjie Fu) but not its papers.
- What worked: Crossref's `query.affiliation=High School` restricted to the container
  "2024 IEEE International Conference on Big Data (BigData)". IEEE deposits affiliations,
  so this returns the 30 papers with a high-school-affiliated author. The symposium's
  block sits at pages 7292-7496 (all 5-page papers); a few HS-coauthored papers elsewhere
  in the volume are main-track or workshop papers.
- The same query for the 2025 edition (2nd, Macau) returns only two papers, both with a
  high-school student as a minor co-author on a university paper (pp. 3295 and 7107), so
  either the 2025 symposium's papers were not affiliation-tagged or very few were
  published. No 2025 symposium page survives online. Treat the 2024 volume as the
  reference set.
- The symposium's 2026 co-chair, Kunpeng Liu (Clemson, then Portland State), is the
  senior author of the paper chosen below. That makes it the best available signal of
  what the 2026 chairs consider a model paper.

## 1. Citation

Henry J. Xie (Westview High School, Portland, OR), Jinghan Zhang, Xinhao Zhang and
Kunpeng Liu (Portland State University), "Scoring with Large Language Models: A Study on
Measuring Empathy of Responses in Dialogues," in *Proc. 2024 IEEE International
Conference on Big Data (BigData)*, Washington, DC, 15-18 Dec 2024, pp. 7433-7437.
DOI 10.1109/BigData62323.2024.10825836. arXiv:2412.20264 (28 Dec 2024, comment
"Accepted by IEEE BigData 2024"). Code: github.com/henryjxie/Scoring-with-Large-Language-Models.
First-author footnote on page 1: "Currently a high school junior; work done as a research
intern at PSU." Full text used: arXiv PDF, 5 pages, 16 references.

Topic fit: an LLM-evaluation study (can GPT-class models score empathy like human raters,
and can explicit features approximate their scores). Same genre as ours: closed-API LLMs,
classifiers on interpretable features, feature selection, comparison against a stronger
black-box baseline.

Nearest alternates from the same 2024 block, if a second exemplar is wanted:
- N. He, V. Tang (Ocean Lakes HS), H. Wu (Temple), "How Effective is AI-Powered Social
  Media Analysis: Mining Reddit Conversations on Emergency Rooms," pp. 7318-7322,
  DOI 10.1109/BigData62323.2024.10825568 (text mining).
- J. Xu, J. Wang, J. Leung, J. Gu (Lexington HS), "GRASP: Municipal Budget AI Chatbots for
  Enhancing Civic Engagement," pp. 7438-7442, DOI 10.1109/BigData62323.2024.10825975.
- A. Pang (Horace Greeley HS), H. Jang, S. Fang (IU Indianapolis), "Generating Descriptive
  Explanations of Machine Learning Models Using LLM," pp. 5369-5374,
  DOI 10.1109/BigData62323.2024.10825667 (6 pages, outside the block; likely a workshop
  paper, not the symposium).

## 2. Section structure and word counts

Counts are from the arXiv text layer; sections IV and V include table text and figure
axis labels, so their prose is roughly 10 percent smaller than shown.

| Section | Words | Notes |
|---|---|---|
| Abstract | 239 | one paragraph, no numbers |
| Index Terms | 9 | "Scoring, Empathy, Large Language Models, Fine-tuning, Feature Selection" |
| I. Introduction | ~550 | four paragraphs; Fig. 1 (overview: pipeline above, headline accuracies below) sits in column 2 of page 1 |
| II. Related Work | ~145 | one paragraph, 9 citations |
| III. Problem Description and Dataset | ~280 | III-A task definition with notation; III-B dataset |
| IV. Benchmarking LLM Empathy Scoring | ~800 | IV-A data split; IV-B model choice (Table I); IV-C baseline prompt (shown in a box); IV-D fine-tuning (Table II) |
| V. Understanding LLM Empathy Scoring | ~1,300 | V-A embeddings (Fig. 2); V-B MITI code (Fig. 3); V-C explicit subfactors (Figs. 4-6); V-D combination and RFE (Figs. 7-8) |
| VI. Conclusions and Future Work | ~180 | two paragraphs: summary, then future work with one limitation |
| References | 16 entries | ~360 words |
| Body total (I-VI) | ~3,400 | plus 2 tables, 8 figures |

Shape: 15 percent introduction, 4 percent related work, 8 percent setup, 62 percent
method-and-results interleaved (each subsection = one method, one figure, one takeaway
sentence), 5 percent conclusion. There is no separate Results, Discussion or
Limitations section.

## 3. Openings

Abstract, first sentence: "In recent years, Large Language Models (LLMs) have become
increasingly more powerful in their ability to complete complex tasks."

Introduction, first sentence: "In recent years, Large Language Models (LLMs) such as
Gemini [2], GPT-4 [3], and LLaMA [10] have revolutionized Natural Language Processing
with their impressive capabilities beyond basic text generation and translation."

Both open wide (state of the field), narrow to the task in sentence two ("One such task
... is scoring"), and pose the research questions as literal questions by the end of
paragraph one: "We pose two key research questions: How accurate are LLMs at measuring
and scoring empathy as compared to human evaluators and how do we comprehend the
specifics involved in LLM scoring?" Paragraph two is the why-it-matters paragraph
("In many areas where LLMs are integrated, empathy is crucial for effective
communication ... it is important that LLMs have the ability to empathize at a proficient
level as they are further integrated into our society."). Paragraph three restates the
task in one plain sentence. Paragraph four is the method walk-through.

## 4. How contributions are stated

Prose, not bullets. The last introduction paragraph names the deliverable as "a novel and
comprehensive framework as shown in Figure 1" and then walks the pipeline as an inline
numbered list: "We (1) adopt an empathetic dialogue dataset ..., (2) balance this
dataset ..., (3) measure the performances of state-of-the-art LLMs, and (4) select the
best performing LLM ... training classifiers (5) with the embeddings ... and (6) using the
... MITI Code ... We further (7) create a set of explicit subfactors". It ends with the
headline result in words, not numbers ("the classifiers achieve parity with the accuracy
of fine-tuned LLMs") and one sentence on what the result lets you do ("can serve as a
vehicle to understand how LLMs apprehend empathy"). There is no "Our contributions are
(i)...(iii)" sentence and no numbers in the introduction at all.

## 5. How results are presented

- Two small tables (Table I: four LLMs, one accuracy column; Table II: five
  hyperparameter settings) and six result figures, all bar charts of classifier accuracy
  by model, plus a subfactor tree and a feature-importance chart.
- Numbers are single-split accuracies reported to two decimals as percentages
  (46.61%, 54.69%, 42.71%); the test set is one 80/20 split of 1,920 balanced items
  (384 test items). No confidence intervals, no standard deviations, no repeated splits,
  no significance tests, no p-values, no corrections. The only anchor is chance:
  "significantly more accurate than random guessing (33.33%) but have considerable room
  for improvement" and "roughly 20% higher than arbitrarily guessing (33.33%) and 8%
  higher than the default accuracy (46.61%)".
- Every number is followed by a plain-language reading: "This illustrates that the MITI
  Code assigned to the responses do contain information strongly relevant to empathy
  scoring." "This result shows that the state-of-the-art LLMs such as GPT-4o-mini, have a
  strong understanding of how to measure empathy after fine-tuning."
- The narrative arc is baseline (naive prompt) -> peak (fine-tuned) -> how close can
  explainable features get, so each figure is read against the same two reference lines.
- One negative result is kept and explained: concatenating both feature sets was "worse
  than expected. The potential reason could be that there exists redundancy in the
  concatenated vector. Consequently, we try feature selection".

## 6. Limitations and real-world application

Limitation, in full (the only one, in the last paragraph): "A limitation of this study
is that the dialogues are from a single dataset. In future work, we will use dialogues
from a variety of data sources to achieve a more representative understanding of empathy
scoring that factors in a wide range of backgrounds and contexts."

Sentences connecting the method to use:
- Related work: "Human ratings are the gold standard of scoring empathy [13], however
  not scalable. Therefore, automatic empathy measures through interpretable LLM scoring
  are a highly desirable alternative."
- End of V-D: "Instead of GPT-4o-mini being a black box for empathy scoring, we can now
  employ the trained classifiers as semi-transparent boxes that lay out what and how
  features are utilized in scoring."
- Conclusion: "our more explicit empathy scoring approach can be utilized in place of
  direct scoring by LLMs to make empathy scoring more explicit and transparent."
- Abstract: "helps the LLM community explore the potential of LLM scoring in social
  science studies."
- Introduction: "In many areas where LLMs are integrated, empathy is crucial for
  effective communication ... it is important that LLMs have the ability to empathize at
  a proficient level as they are further integrated into our society."

The pattern: name the human practice the method replaces or assists (human raters,
black-box LLM scoring), say why the replacement is wanted (scale, transparency), and
name the community that benefits (social science, "the LLM community").

## 7. Tone markers

- First person plural throughout: "we" 47 times and "our" 16 times in ~3,400 words
  (one "we" every 70 words). Passive voice is rare and used for procedure ("The
  experiment was done on the unified test dataset").
- Hedging is light. Confident readings ("It was evident that", "This result shows that",
  "have a strong understanding") outnumber hedges ("may result in", "The potential
  reason could be", "it is reasonable that").
- Introduction sentences: 23 sentences, mean 26 words, range 10-55. Results sentences
  are shorter (15-25 words). Heavy signposting: "In this section, we", "We first", "We
  then", "As shown in Figure 2", "Naturally, it is promising to investigate".
- Vocabulary is plain and slightly promotional: "novel and comprehensive framework",
  "promising", "highly desirable", "great starting point", "a new perspective".
- Every subsection ends with a one-sentence takeaway.
- Reader is assumed to be an ML generalist: MITI code, empathy dimensions and RFE are
  each explained in one or two sentences; nothing is assumed from stylometry or
  statistics.

## 8. What it does that our draft does not (and that the symposium evidently valued)

Caveat: reviews are not public. "Valued" is inferred from acceptance plus the fact that
the paper's senior author now co-chairs the 2026 symposium.

1. A one-paragraph, number-free abstract that ends on who benefits. Ours is a
   number-dense abstract (nine macros, a CI, a Holm count) that a non-specialist
   reviewer cannot skim.
2. A why-it-matters paragraph in the introduction, written for a person rather than a
   field. Our only motivation is one clause: "tracing influence campaigns and enforcing
   provider-specific rules".
3. Research questions stated as literal questions in the first paragraph. Ours are
   correct but arrive in paragraph three as a six-item bracketed list.
4. An overview figure on page 1 that shows the pipeline and the headline accuracies
   together. We have no overview figure; Table 1 is the first thing a reader sees and
   it has six columns of macros.
5. One method, one figure, one takeaway per subsection, with the same two reference
   lines (baseline, peak) in every plot. Our Results subsections carry several analyses
   each and reference the n-gram baseline, chance and the judges in different places.
6. A plain-language sentence after every number. We report "Holm-significant in N of
   seven" and "\Beta log-odds per rank step" without saying, in words, what a reader
   should conclude.
7. A short related work (145 words) that ends in the sentence that motivates the
   method. Ours is ~380 words with a three-way taxonomy; fine for a journal, long for
   five pages.
8. Explicit chance anchoring in prose ("random guessing (33.33%)"). We put "chance
   \Chance{}" in a parenthesis once.
9. A named, reusable deliverable ("a framework", "the trained classifiers as
   semi-transparent boxes"). Our deliverables (corpus, feature set, two baselines) are
   listed but never named as a thing someone could pick up and run.
10. A code link on page 1 and a first-author footnote flagging the high-school status
    and the mentoring arrangement. The venue is single-blind and asks for the HS flag
    in the affiliation; the footnote form is what the accepted paper used.
11. Limitations framed as future work, in two sentences, at the very end. Ours is an
    eight-item enumerated paragraph, which is more honest but reads as a reviewer's
    checklist rather than an author's plan. Keep the content; consider moving (i)-(iv)
    into the relevant Results paragraphs and leaving two or three items at the end.
12. Nothing we should copy: the exemplar has no intervals, no repeated splits and no
    correction for its many comparisons. Our pre-registration, prompt-clustered CIs and
    Holm family are strengths; the point is to keep them and add the plain readings,
    not to remove them.

## 9. Five rewrite suggestions for our abstract and introduction (one sentence each)

1. Open the abstract with the field-level sentence the exemplar uses, then the gap:
   "Large language models now write fluently in many languages, but almost everything
   known about telling their outputs apart comes from English."
2. Move the numbers out of the abstract's middle and end it on the use: "... so
   non-English machine text can be attributed with a classifier whose decisions can be
   read, which matters for provenance checks that cannot rely on a fine-tuned black box."
3. Put the two headline questions in the introduction's first paragraph as questions:
   "We ask two questions: can five frontier models be told apart from a small set of
   readable features in seven languages, and what does that readability cost against
   character n-grams?"
4. Add a why-it-matters paragraph after the opening, in the exemplar's register, that
   names a person and a task: a platform moderator or a teacher who needs to say which
   model wrote a Hindi or Turkish text, and who cannot act on a probability from a model
   they cannot inspect.
5. Replace the "(i)...(iii)" contribution sentence with a walk through the pipeline and
   one word-only result: "We collect content-matched essays, describe every text with 21
   features defined the same way in every language, and find that the features attribute
   the author in all seven languages at a modest, measured cost against n-grams; most of
   the signal sits in a handful of nameable features that survive machine translation."

Also worth doing: a Fig. 1 overview (corpus -> UD features -> LOPO classifier -> five
analyses, with the per-language accuracy bar under it), and a one-line
"This means ..." after each Holm or CI statement in Results.

---

# Reference checks

(a) **Gorman 2022** — found. Robert Gorman, "Universal Dependencies and Author
Attribution of Short Texts with Syntax Alone," *Digital Humanities Quarterly*, vol. 16,
no. 2, 2022, article 000606 (online journal, no page numbers).
DOI 10.63744/jwmhb58drxrg (DHQ-registered, resolves to
dhq.digitalhumanities.org/vol/16/2/000606/000606.html). Scope: udpipe UD parses, syntax
and morphology only, human authors in English, Finnish, German, Spanish and Polish;
>90% accuracy on 300-token segments, above chance at 50 tokens. Note the wording: it is
attribution *within each of several languages* with one UD-derived feature set, not
cross-lingual transfer. Our Related Work already says "in several languages"; keep that
and avoid "cross-lingual" for this citation.

(b) **Stamatatos 2017** — found. Efstathios Stamatatos, "Authorship Attribution Using
Text Distortion," in *Proc. 15th Conference of the European Chapter of the Association
for Computational Linguistics (EACL 2017), Volume 1: Long Papers*, Valencia, Spain,
April 2017, pp. 1138-1149. ACL Anthology ID E17-1107,
https://aclanthology.org/E17-1107/. The Anthology BibTeX carries no DOI field for this
volume, so cite by Anthology URL; do not add a 10.18653 DOI.

(c) **Rivera-Soto et al. 2026** — found. Rafael Rivera Soto, Barry Chen, Nicholas
Andrews, "Attacks on Machine-Text Detectors Retain Stylistic Fingerprints," *ICML 2026*
(poster, icml.cc/virtual/2026/poster/66801); arXiv:2505.14608 (v1 20 May 2025, v3 8 June
2026; v1 carried the title "Language Models Optimized to Fool Detectors Still Have a
Distinct Style (And How to Change It)"). Surname is "Rivera Soto" (two words) on arXiv
and ICML; PMLR volume and pages not yet verifiable. Claim to cite: prompt-engineering and
detector-guided evasion attacks degrade standard detectors but leave a stylistic
fingerprint that few-shot style-space detectors still catch; a purpose-built style-aware
paraphraser evades single-document detection, and aggregating several documents restores
it. (The same authors' arXiv:2606.10099, "Unsupervised Style Representation Learning for
AI-Text Detection via Paraphrase Inversion," 8 June 2026, is a different paper.)

(d) **Zaitsu et al. 2026** — found. Wataru Zaitsu, Mingzhe Jin, Shunichi Ishihara,
Satoru Tsuge, Mitsuyuki Inaba, "Detecting 'large language models fingerprint' for
Japanese texts generated by six LLMs," *Frontiers in Artificial Intelligence*, vol. 9,
art. 1771115, 2026 (published 22 June 2026). DOI 10.3389/frai.2026.1771115. A correction
was published 15 July 2026 (DOI 10.3389/frai.2026.1916608). Features: function-word
unigrams (with punctuation treated as function words), POS bigrams, phrase patterns, and
their combination; random forest, macro-F1 above 0.95 across six LLMs (the article lists
ChatGPT, Claude 3.5, Gemini, Microsoft Copilot, Llama 3.1, Perplexity). Our draft's
"part-of-speech and function-word features" is accurate.

(e) **Kumarage and Liu 2023** — confirmed. Tharindu Kumarage and Huan Liu, "Neural
Authorship Attribution: Stylometric Analysis on Large Language Models," in *Proc. 2023
International Conference on Cyber-Enabled Distributed Computing and Knowledge Discovery
(CyberC)*, 2-4 Nov 2023, pp. 51-54, IEEE. DOI 10.1109/CyberC58899.2023.00019 (resolves
to IEEE Xplore document 10438784). arXiv:2308.07305 confirmed (same title and authors).

Sources consulted: studentpapers-bigdata2024.netlify.app; www3.cs.stonybrook.edu/~ieeebigdata2024/
(SpecialSymposium.html, BD2024-Program-Schedule.pdf); bigdataieee.org/BigData2026/high-school-symposium/;
api.crossref.org (affiliation query and DOI record); export.arxiv.org API; arxiv.org/abs/2412.20264;
dhq.digitalhumanities.org; aclanthology.org/E17-1107; arxiv.org/abs/2505.14608; icml.cc/virtual/2026/poster/66801;
frontiersin.org (10.3389/frai.2026.1771115); asu.elsevierpure.com record for Kumarage and Liu; doi.org resolutions.
