# Venue hunt, domain E: journals and rolling venues

Compiled 20 Sept 2026 for a 6–12 page paper on LLM authorship attribution / multilingual LLM text analysis / LLM evaluation, by two high-school first authors plus an adjunct faculty co-author at UCLA, to be submitted in October 2026 with a decision wanted within roughly 8–12 weeks.

Method: official pages were fetched directly (WebFetch, or the browser pane where the publisher's bot protection blocked plain fetches). Every quotation below is from the page named next to it. "Not found" means the page was fetched (or blocked) and the item was not on it; the URL tried is given. Third-party figures (manusights, journalsearches, scienceaijournal) are marked as such and never used where an official number exists. DBLP could not be checked for any venue: dblp.org's Anubis bot protection returned "Access Denied" to every venue-search request (https://dblp.org/search/venue?q=...), and the sandbox's own network call to the dblp API was refused. Where a journal's own page lists DBLP that is recorded; otherwise DBLP is "not verified".

Scoring note used for the summary: credibility (community standing for an NLP/ML paper) × speed (stated or measured time to first decision) × zero fees (no APC on at least one publishing route).

---

## 1. TMLR — Transactions on Machine Learning Research
**URL:** https://jmlr.org/tmlr/ (author guide https://jmlr.org/tmlr/author-guide.html; editorial policies https://jmlr.org/tmlr/editorial-policies.html; FAQ https://jmlr.org/tmlr/faq.html; submissions on OpenReview)

- **Scope fit:** Strong for an ML-methods framing of LLM attribution/evaluation; the emphasis is on correctness and clear claims rather than novelty of impact.
- **Submission type / length:** Rolling; "Submissions may be any length, but a paper's length should be justified by its content." Reviewer deadline depends on length: "reviews must be submitted within 2 weeks of their assignment by the AE for submissions up to 12 pages (of main content, before references), and 4 weeks for submissions over 12 pages" (reviewer guide). Keep the main body at or under 12 pages to get the fast track. LaTeX and a newer HTML format are both accepted.
- **Time to first decision:** FAQ: "TMLR does not make any guarantees, and manuscripts whose main body exceeds 12 pages are subject to longer timescales, but in general the rolling review process aims to deliver a final decision approximately 9 weeks after submission." Editorial policies: "An action editor will be assigned to the submission within a week." AE guide: reviewers "within 2 weeks of their assignment"; reviewer recommendations "no sooner than 2 weeks and no later than 4 weeks" after discussion opens; AE decision "within 1 week" after that. An October submission at ≤12 pages fits the 8–12 week window on paper.
- **Fees:** None stated anywhere on the TMLR pages (JMLR family; JMLR's own author page says "There are no publication fees associated with this journal"). No submission fee mentioned.
- **Author eligibility (quoted):** "All authors must have complete and active OpenReview profiles, including information such as affiliations, conflicts of interest, and publication history." Editorial policies: "The exact set of authors must be listed on OpenReview, with active profiles, at the time of submission." There is also a per-author submission quota ("Generalized Harmonic Quota Rule"; "Authors who are reviewers or action editors enjoy doubled quotas"), irrelevant for a first submission. No degree, affiliation or ORCID requirement is stated. **OpenReview profile for a high-school student:** OpenReview's signup docs say "We recommend that you sign up with your institutional (university, company, or organization) email" and "It can take up to 2 weeks for profiles using public email services to be activated." The warning shown for a Gmail address reads "gmail.com does not appear in our list of publishing institutions." Activation requires a homepage: "A valid homepage is a website that shows your name, affiliation, and email that you used to register for OpenReview." (https://docs.openreview.net/getting-started/creating-an-openreview-profile/signing-up-for-openreview). The fast path is an institutional email (https://docs.openreview.net/getting-started/creating-an-openreview-profile/expediting-profile-activation: "The fastest way to activate an OpenReview Account is to ensure that you have an email associated with your school or company added and confirmed to your profile"). A school (.k12 / district) email may or may not be recognised as an institution; the personal site adrianerlikhman.is-a.dev, if it shows name, affiliation and the registration email, satisfies the homepage rule. **Verdict: no rule bars a high-school author; budget up to two weeks of moderation, and create the profiles before October.**
- **Open review or anonymous:** "TMLR uses a double blind review process and submissions must be anonymized." Reviews are visible to authors as they arrive; accepted papers and their reviews are public on OpenReview.
- **Preprint policy:** "Authors are also allowed to upload their submissions to arXiv or other preprint servers at any time, either anonymously or including their identity," but must not link the anonymous submission to a named version. Note the originality rule: "Original work only—no expanded conference papers accepted" and "TMLR does not accept submissions that have any overlap with previously published work." A non-archival workshop abstract/poster is usually fine in the ML community, but the URTC 2026 abstract should be disclosed to the AE.
- **Indexing:** Not found on TMLR pages (FAQ only discusses Google Scholar: "Google Scholar is unfortunately unreliable and a black box to us"). DBLP not verified (blocked). Scopus/WoS: not found.
- **Risk:** Medium. Reviewers expect a complete, well-controlled ML study and will push on claims; the 9-week figure is an aim, not a guarantee, and a "reject with encouragement to resubmit" is common. Profile activation for two Gmail-only authors is the one hard logistical step.

## 2. DMLR — Journal of Data-centric Machine Learning Research
**URL:** https://data.mlr.press/ (submissions https://data.mlr.press/submissions; OpenReview group https://openreview.net/group?id=DMLR)

- **Scope fit:** Moderate: DMLR wants "the data aspect of machine learning research" (datasets, benchmarks, evaluation methodology). A multilingual LLM-attribution benchmark framing would fit; a pure attribution-method paper would not.
- **Submission type / length:** "Submissions are not constrained by a page limit; however, authors should be mindful that the review process for lengthy papers may require an extended period." Extended conference/workshop papers allowed with "minimum of 30% additional content compared to their prior versions."
- **Time to first decision:** Submissions page: pre-screened within a "two-week timeframe"; "Reviewers are asked to submit their reviews in four weeks"; "three weeks (two for Rebuttal one for Discussion periods)"; "AE has one week to reach a decision"; and the headline: "expected turnaround time for the decision is usually between 4 and 6 months." **Too slow for the window.**
- **Fees:** "DMLR also does not require any fees or payments from authors, reviewers, action editors, or editors-in-chief."
- **Author eligibility (quoted):** "All authors are required to have an OpenReview profile and identify domain and personal conflicts." Same OpenReview activation caveat as TMLR. No degree/affiliation rule.
- **Open review or anonymous:** "DMLR employs a single-blind review process with open reviewing"; "authors' identities are not anonymized"; "Submissions will be public on OpenReview only when they are accepted."
- **Preprint policy:** "DMLR also allows authors to submit their work concurrently to other non-archival venues or preprint servers, such as arXiv and bioRxiv, but not to another archival venue."
- **Indexing:** Not found on data.mlr.press. DBLP not verified.
- **Risk:** Timeline (4–6 months) rules it out for October-to-December; keep as a fallback if the paper is reframed as a benchmark/dataset contribution.

## 3. JMLR — Journal of Machine Learning Research
**URL:** https://www.jmlr.org/author-info.html (submission system https://jmlr.csail.mit.edu/manudb/)

- **Scope fit:** Weak for an applied NLP paper; JMLR expects substantial methodological or theoretical ML contributions.
- **Submission type / length:** JMLR LaTeX style, PDF under 5 MB, cover letter with 3–5 suggested action editors and reviewers, abstract ≤200 words. "Papers longer than 35 pages will take a longer time to review"; "papers above 50 pages require a note of justification."
- **Time to first decision:** Not stated as a number. The page says only that "some papers may take a long time to review" and "a few papers may take less time (e.g., if rejected without review)." Community experience is many months. **Probably too slow**, as the brief anticipated.
- **Fees:** "There are no publication fees associated with this journal and all papers are freely available to readers."
- **Author eligibility (quoted):** None stated; "JMLR accepts submissions via its own electronic submission management system." No OpenReview, ORCID or affiliation requirement found on the page.
- **Open review or anonymous:** Not addressed on the author page (JMLR is single-blind in practice; not quoted).
- **Preprint policy:** "Authors may submit work to JMLR that is already available as a preprint, for example on arXiV or personal websites."
- **Indexing:** Not found on the author page. DBLP not verified.
- **Risk:** High on both fit and speed. Not recommended.

## 4. JAIR — Journal of Artificial Intelligence Research
**URL:** https://www.jair.org/index.php/jair/about/submissions (about page https://www.jair.org/index.php/jair/about)

- **Scope fit:** Good: JAIR publishes NLP and LLM-evaluation work under the broad AI umbrella; multilingual attribution of LLM output is in scope.
- **Submission type / length:** Regular article; "No explicit page limits stated" on the submissions page; authors should "be concise." Three mandatory survey questions at submission; extended conference papers allowed with substantial new content.
- **Time to first decision:** "Articles sent to JAIR will be reviewed and a decision returned to the authors in approximately 8-12 weeks." The about page says "JAIR reviews papers within approximately three months of submission." Caveat on the same page: longer papers or submissions during conference periods may take more time.
- **Fees:** "There is no charge to submit a paper, nor are there any publication fees once an article is accepted." JAIR is "funded solely by grants/donations to AI Access Foundation."
- **Author eligibility (quoted):** None. Only originality: "The work cannot have been published previously or be pending publication in another journal, nor can it be under review or be sent for review in any other forum." No degree, affiliation, ORCID or institutional-email rule found.
- **Open review or anonymous:** Reviewer identities hidden: "Maintaining the confidentiality of submissions and the anonymity of reviewers is crucial to JAIR's peer review process." Author anonymity not required (single-blind).
- **Preprint policy:** "Authors may submit their JAIR papers to arXiv and similar services, but should ensure that the archived version has the proper metadata for their JAIR publication."
- **Indexing:** About page: "indexed by INSPEC, Science Citation Index, and MathSciNet"; "JAIR Available in ACM Library." Scopus and DBLP not stated on the page (DBLP not verified).
- **Risk:** Low-medium. Diamond OA, credible, explicit 8–12 week promise, no author restrictions. JAIR articles tend to be long (20+ pages); a 10–12 page paper is acceptable but should read as a complete journal study, not a conference paper.

## 5. Computational Linguistics (ACL / MIT Press)
**URL:** https://cljournal.org/ (submission guidelines https://submissions.cljournal.org/index.php/cljournal/about/submissions; MIT Press pages https://direct.mit.edu/coli/pages/submission-guidelines returned HTTP 403 / Cloudflare challenge to both fetch and browser)

- **Scope fit:** Strong: the field's archival NLP journal; authorship attribution and multilingual LLM analysis are squarely in scope.
- **Submission type / length:** "Regular Research Papers (Long and Short), Survey Articles, Position Papers, Squibs and Discussions, and Last Words." Long: "Typically up to 40 pages of main text." Short: "Initial submissions are typically up to 20 pages. Final versions may be up to 25 pages." Squibs: "must not exceed 8 pages of content (with unlimited pages for references)." A 6–12 page paper would go in as a Short paper or a Squib.
- **Time to first decision:** cljournal.org front page: "Average time to first decision (46 days)". (A web-search snippet also reported "16.5 days (including desk rejections) and 55.0 days (excluding desk rejections)" for 2025, but I could not open the page it came from, so treat 46 days as the official number.)
- **Fees:** None. cljournal.org: "has been Open Access since the beginning of 2009" and "All issues published by MIT Press are freely available to all." No APC or submission fee is mentioned on the submissions page.
- **Author eligibility (quoted):** None stated on the submissions page. Manuscripts are screened: "submit manuscripts and associated materials to trusted third-party screening services, such as the similarity-detection service iThenticate."
- **Open review or anonymous:** Not found on the pages I could open (URLs tried: cljournal.org, submissions.cljournal.org/.../submissions, direct.mit.edu/coli/pages/submission-guidelines).
- **Preprint policy:** Not found (same URLs).
- **Indexing:** Not found on the journal pages; DBLP not verified.
- **Risk:** Medium-high on selectivity: CL expects mature, thorough work and revisions are common, so 46 days to a first decision does not mean 12 weeks to acceptance. Best free, high-credibility NLP-journal option if the paper is polished.

## 6. Natural Language Processing (Cambridge; formerly Natural Language Engineering)
**URL:** https://www.cambridge.org/core/journals/natural-language-processing (author instructions .../information/author-instructions/preparing-your-materials; fees .../author-instructions/fees-and-pricing)

- **Scope fit:** Good: "an open access journal which meets the needs of professionals and researchers working in all areas of natural language processing (NLP)"; "encourages papers reporting research with a clear potential for practical application."
- **Submission type / length:** Article "~8,000-12,000 words"; Squib "Max. 8,000 words"; Position Paper "Max. 8,000 words"; Survey "~10,000-16,000 words." Initial submission as PDF; LaTeX at acceptance.
- **Time to first decision:** Not found (URLs tried: about-this-journal, preparing-your-materials).
- **Fees:** Fully gold OA with a mandatory APC: "GBP (£): 2,610" / "USD ($): 3,655." "This journal is a wholly open access journal, which means all articles are published Gold Open Access under a Creative Commons licence." Waivers: "Cambridge provides multiple other routes to funding Gold Open Access, including equity initiatives and APC waivers and discounts, in order to ensure that every author can publish in this journal." UCLA has a Cambridge read-and-publish agreement in many years; whether it covers this title and whether an adjunct corresponding author qualifies must be checked with UCLA Library.
- **Author eligibility (quoted):** "All authors of papers submitted to Natural Language Processing agree to be invited to peer review other journal submissions." ORCID is listed as a section of the author instructions; no degree/affiliation rule.
- **Open review or anonymous:** Not found. The author-instructions page links a "Peer review information" section, but the URL I tried for it (.../author-instructions/peer-review-information) returned 404, and the about-this-journal page does not state single- or double-anonymous review.
- **Preprint policy:** "Deposition of a preprint on the author's personal website, in an institutional repository, or in a preprint archive shall not be viewed as prior or duplicate publication."
- **Indexing:** Page has an "Abstracting and indexing" section but the list was not in the fetched content. Natural Language Engineering was Scopus/SCIE indexed; not re-verified here. DBLP not verified.
- **Risk:** The $3,655 APC is the blocker unless a UCLA agreement or a waiver covers it; timeline unknown.

## 7. Harvard Data Science Review
**URL:** https://hdsr.mitpress.mit.edu/author-info (proposals https://hdsr.mitpress.mit.edu/pub/proposals; policies https://hdsr.mitpress.mit.edu/pub/publicationpolicies; FAQ https://hdsr.mitpress.mit.edu/pub/1lt3ciev)

- **Scope fit:** Weak-moderate: HDSR wants data-science pieces with broad societal or methodological interest, not standard NLP experiments.
- **Submission type / length:** Two-stage. "HDSR will only review manuscripts by invitation, but all interested authors are invited to submit proposals for full papers." "HDSR does not accept unsolicited submissions of full manuscripts. If authors submit full manuscripts without invitation, these manuscripts will be returned to their authors without review." Proposal = title, authors, up to 6 keywords, "1-2 page short description or executive summary." No maximum manuscript length.
- **Time to first decision:** Proposal stage only: "HDSR aims to respond to proposals within 4 to 6 weeks of submission." No timeline is given for the invited full-manuscript review, so a decision within 12 weeks of an October start is not realistic.
- **Fees:** "No article processing charges are required to submit to HDSR." Published CC-BY 4.0.
- **Author eligibility (quoted):** None stated. Submissions via Editorial Manager only.
- **Open review or anonymous:** "HDSR is a single-blind journal. Co-Editors, Associate Editors, and Reviewers will know the authors' identities, but authors will not know any of their editors' or reviewers' identities."
- **Preprint policy:** "HDSR considers exclusive submissions only. However, HDSR will consider content that has been deposited in institutional archives or repositories such as arXiv."
- **Indexing:** Not found on the pages opened. DBLP not verified.
- **Risk:** Proposal gate plus unknown review time; fit is weak. Not recommended for this paper.

## 8. Patterns (Cell Press)
**URL:** https://www.cell.com/patterns/faq (article types https://www.cell.com/patterns/information-for-authors/article-types; APC table https://www.cell.com/open-access, Cloudflare-blocked)

- **Scope fit:** Moderate: "data science in the broadest sense, including computational science, data-heavy research"; "both fully open access and highly selective."
- **Submission type / length:** Research article "approximately 5,000–7,000 words, but longer or shorter articles may be considered" (article-types page via search snippet; direct fetch blocked). PDF accepted for first submission.
- **Time to first decision:** FAQ: "The initial decision to review is usually made within about five days. The first decision after peer review is usually rendered within 45 days."
- **Fees:** Mandatory APC on acceptance: "Authors of accepted papers are required to pay an article processing charge... Our current APC is listed on the Cell Press open access page." The amount is **not found** (https://www.cell.com/open-access served a Cloudflare challenge on every attempt); third-party sites list about USD 8,900 for Patterns (journalsearches.com, manusights.com), unverified. Waivers: "Authors who cannot afford the journal's APC are invited to contact the journal prior to submission (patterns@cell.com). Waiver requests will be considered on a case-by-case basis." Also a "geographical pricing pilot" for low/middle-income countries and Elsevier institutional agreements.
- **Author eligibility (quoted):** None stated. Strong open-science expectation: "Authors are expected to share data, code, and models openly with their paper whenever possible."
- **Open review or anonymous:** "Patterns uses a single-anonymized peer-review process, meaning that reviewers are aware of the authors' names but that reviewers' names are not shared with authors."
- **Preprint policy:** "Patterns strongly encourages preprint sharing and is glad to consider papers that have already been posted on community preprint servers."
- **Indexing:** "indexed in the major scientific indices, including PubMed, Scopus, the DOAJ, and the Web of Science." 2025 metrics: "CiteScore (Scopus): 18.0; Journal Impact Factor (Clarivate): 10.8." DBLP not verified.
- **Risk:** High selectivity ("major methodological advances or ground-breaking insights") and a very large APC unless waived. Speed is good.

## 9. PLOS ONE
**URL:** https://journals.plos.org/plosone/s/journal-information (fees https://www.plos.org/publication-fees)

- **Scope fit:** Accepts any sound science across "over two hundred subject areas"; computer science/NLP papers appear, but the audience is not NLP.
- **Submission type / length:** Research article; no length limit stated on the pages fetched.
- **Time to first decision:** Journal information page: "Time to First Decision" median "44-62 days," most recent listed period "45 days."
- **Fees:** Research article APC "$2,477." Waivers: Research4Life Group A countries free, Group B "$940"; "Publication Fee Assistance (PFA)" for "authors unable to pay all or part of their publication fees and who can demonstrate financial need," decisions "within 10 business days." No submission fee.
- **Author eligibility (quoted):** None; "We evaluate research on the basis of scientific validity, strong methodology, and high ethical standards—not perceived significance."
- **Open review or anonymous:** Not found on the pages fetched (PLOS ONE is single-anonymous by default with optional published reviews; not quoted).
- **Preprint policy:** Not found on the pages fetched.
- **Indexing:** "indexed by major services such as Crossref, Dimensions, DOAJ, Google Scholar, PubMed, PubMed Central, Scopus, and Web of Science." DBLP not verified.
- **Risk:** APC; weak prestige signal for an NLP paper; ~45 days to first decision is fine.

## 10. PeerJ Computer Science
**URL:** https://peerj.com/journals/computer-science/ (pricing https://peerj.com/pricing/; waivers https://peerj.com/questions/faq/4784-are-there-fee-waivers/)

- **Scope fit:** Good: "artificial intelligence, data science, software engineering, cybersecurity, and human-computer interaction"; a listed discipline is "AI, Computer Vision & Natural Language Processing."
- **Submission type / length:** Research article; no page limit stated on the pages fetched ("Are there additional charges for longer articles?" is a pricing FAQ item; answer not expanded).
- **Time to first decision:** Pricing page: "30-35 Days to First Decision." Journal page: "32 days Acceptance to publication," "33% Acceptance rate."
- **Fees:** "PeerJ Computer Science $2,155" APC ("excluding applicable local taxes"), or Lifetime Membership per author (Basic "$755" for 1 publication a year; all authors must hold a membership on that route). Waivers: "a no questions asked membership fee waiver... to any author from countries that are classified by the World Bank as Low-income economies," and "any co-author who was an undergraduate at the time of the research may request a membership waiver (provided the paper has senior co-author(s) who have at least a Basic publishing plan...)". That undergraduate clause is the only student provision; high-school authors are not mentioned. Annual Institutional Memberships cover authors at member institutions (UCLA not confirmed; check https://peerj.com/pricing/ "Find my institution").
- **Author eligibility (quoted):** None on the pages fetched.
- **Open review or anonymous:** "Reviews published alongside article" (optional open reviews); reviewer anonymity policy page https://peerj.com/about/policies-and-procedures/cs returned 403 to fetch.
- **Preprint policy:** Not found (policies page blocked).
- **Indexing:** "indexed in all major Abstracting & Indexing databases including Pubmed Central (PMC), MEDLINE, Scopus, Web of Science SCIE"; impact factor "2.9 (2025)." DBLP not verified.
- **Risk:** APC ($2,155 or memberships); otherwise fast and reasonably credible.

## 11. Frontiers in Artificial Intelligence
**URL:** https://www.frontiersin.org/journals/artificial-intelligence (fees .../for-authors/publishing-fees; article types .../for-authors/article-types)

- **Scope fit:** Moderate: broad AI journal with an NLP/language section.
- **Submission type / length:** "Original Research articles are peer-reviewed and have a maximum word count of 12,000." "Brief Research Report articles are peer-reviewed, have a maximum word count of 4,000 and may contain no more than 4 Figures/Tables."
- **Time to first decision:** Not found (URLs tried: author-guidelines, publishing-fees, article-types).
- **Fees:** "Original Research (A-Type Article): CHF 2,195"; "Brief Research Report (B-Type Article): CHF 1,750." Support: "Authors in countries classified by the World Bank as low or lower-middle income countries may be eligible for discounts"; "A portion of our income is used to support authors unable to pay APCs"; institutional partnerships.
- **Author eligibility (quoted):** None found.
- **Open review or anonymous:** Frontiers' "interactive review" is referenced; reviewer names appear on published articles under Frontiers policy, but that sentence was not on the fetched pages, so: not found.
- **Preprint policy:** "Preprints can be cited as long as a DOI or archive URL is available."
- **Indexing:** Not found on the fetched pages. DBLP not verified.
- **Risk:** APC; mixed reputation for selectivity; timeline unverified.

## 12. IEEE Access
**URL:** https://ieeeaccess.ieee.org/ (APC https://ieeeaccess.ieee.org/about/article-processing-charges/; guidelines https://ieeeaccess.ieee.org/authors/submission-guidelines/; bibliometrics https://ieeeaccess.ieee.org/about/bibliometrics/)

- **Scope fit:** Any IEEE field; NLP/LLM papers are common.
- **Submission type / length:** "While IEEE Access does not have a page limit; we strongly recommend keeping the page count under 20 pages." Over 20 pages needs Editor-in-Chief approval.
- **Time to first decision:** Home page: "submission-to-publication time of 4 to 6 weeks"; "rapid peer review." Time to first decision itself: not found as a separate number.
- **Fees:** "$2,160 per article (plus applicable local taxes) without page limits." Discounts: "Corresponding authors who are IEEE members receive a 5% discount"; IEEE + Society members 20%; low-income-country waiver "if all authors are located in a country eligible for a discount."
- **Author eligibility (quoted):** "The submitting author is required to have an ORCID ID associated with their account. The ORCID profile must be publicly visible and populated." No degree/affiliation rule.
- **Open review or anonymous:** Not found on the pages fetched (peer-review page https://ieeeaccess.ieee.org/authors/peer-review-process/ returned 404).
- **Preprint policy:** Not found on the pages fetched (IEEE's general policy allows arXiv with a notice; see TCSS entry for the wording IEEE SMC uses).
- **Indexing:** "Scopus," "Science Citation Index Expanded (Clarivate Analytics)," "IET Inspec"; "Impact factor of 4.2" (2025 JCR). DBLP not verified.
- **Risk:** APC; fast; broad but low-signal venue for an NLP paper.

## 13. IEEE Transactions on Computational Social Systems
**URL:** https://www.ieeesmc.org/publications/transactions-on-computational-social-systems/ (information for authors .../information-for-authors/; submissions https://ieee.atyponrex.com/journal/tcss)

- **Scope fit:** Weak-moderate: "modeling, simulation, analysis and understanding of social systems from the quantitative and/or computational perspective"; an LLM-attribution paper would need a social-systems angle (e.g., provenance of machine text in online discourse).
- **Submission type / length:** "Regular papers are normally about 10 TRANSACTIONS pages in length, or shorter"; technical correspondences "no more than 5 TRANSACTIONS pages"; cap of "2 over length pages." IEEE two-column format.
- **Time to first decision:** "Our goal is to provide review results in approximately ten weeks."
- **Fees:** Hybrid: "allowing either Traditional manuscript submission or Open Access (author-pays OA) manuscript submission"; OA route "discounted $2,150 OA fee if your manuscript is accepted." Traditional route has no APC, but "A mandatory over length page charge of $175 is required for each page in excess of 10 pages for a regular paper, 5 pages for technical correspondences."
- **Author eligibility (quoted):** "All IEEE journals require an Open Researcher and Contributor ID (ORCID) for all authors." No degree/affiliation rule.
- **Open review or anonymous:** "reviewed by a minimum of two independent reviewers using a single-anonymous peer review process, where the identities of the reviewers are not known to the authors, but the reviewers know the identities of the authors."
- **Preprint policy:** Allowed with the notice "This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible." and "Authors should disclose postings on approved preprint services when submitting papers."
- **Indexing:** Not found on the SMC pages; IEEE Transactions are Scopus/SCIE indexed as a rule (not verified here). DBLP not verified.
- **Risk:** Fit is the main risk; otherwise free (traditional route, ≤10 pages), ~10-week goal, ORCID for all authors is free to obtain at any age.

## 14. ACM Transactions on Intelligent Systems and Technology (TIST)
**URL:** https://dl.acm.org/journal/tist/author-guidelines (open access https://dl.acm.org/journal/tist/open-access)

- **Scope fit:** Moderate-good: topics include "speech and language understanding and processing systems," "large-scale machine learning systems and technology," "machine learning applications."
- **Submission type / length:** Regular paper: "Submissions must have a maximum length of 25 pages including references"; "Authors are encouraged to submit non-lengthy regular papers (around 24 published journal pages or 10,000 words)." Research Note/Short Paper: "no more than about 10 pages in length." Use the acmsmall template.
- **Time to first decision:** "We strive to complete this process from submission to decision in 3-4 months, though some papers can require longer periods to review." Administrative rejects are immediate.
- **Fees:** ACM is fully OA from 1 Jan 2026. No charge "If the corresponding author is affiliated with an institution participating in ACM's transformative ACM Open model" or from a World Bank low-income country. Otherwise, 2026 subsidised journal APC: "$1450" (no ACM/SIG member among authors) / "$950" (at least one ACM or SIG member); lower-middle-income country "$725"/"$475." "no production work... will proceed until APC payment is received." Whether UCLA is in ACM Open must be checked on the participating-institutions list linked from that page; if it is, and the UCLA adjunct is corresponding author, the fee is zero.
- **Author eligibility (quoted):** None stated; submit via Manuscript Central.
- **Open review or anonymous:** Not stated on the author guidelines (ACM journals are typically single-anonymous; not quoted).
- **Preprint policy:** Not on the TIST page; ACM's general policy permits preprints (not quoted).
- **Indexing:** ACM Digital Library; Scopus/WoS not stated on the page. DBLP not verified.
- **Risk:** 3–4 months is past the window; fee depends on ACM Open membership.

## 15. Journal of Quantitative Linguistics (Taylor & Francis)
**URL:** https://www.tandfonline.com/journals/njql20 (instructions https://www.tandfonline.com/action/authorSubmission?show=instructions&journalCode=njql20, opened in the browser pane)

- **Scope fit:** Strong for stylometry/authorship attribution; the journal's community is quantitative linguistics rather than ML, so LLM-evaluation framing should be translated into linguistic terms.
- **Submission type / length:** "Original Articles, Book Review." "A typical paper for this journal should be between 2000 and 8000 words, inclusive of: Abstract, Tables, References, Figure or table captions, Footnotes, Endnotes." Format-free submission.
- **Time to first decision:** Not found (URLs tried: instructions page, about-this-journal page which returned 403).
- **Fees:** Hybrid. "You have the option to publish open access in this journal via our Open Select publishing program"; "You will be asked to pay an article publishing charge (APC) to make your article open access" (amount via T&F APC finder, not on the page). No APC on the subscription route; no submission fee mentioned.
- **Author eligibility (quoted):** None beyond originality: "the manuscript is your own original work"; "the manuscript has been submitted only to Journal of Quantitative Linguistics." English only.
- **Open review or anonymous:** "it will then be double anonymous peer reviewed by two independent, anonymous expert."
- **Preprint policy:** "If you have shared an earlier version of your Author's Original Manuscript on a preprint server, please be aware that anonymity cannot be guaranteed" (preprints allowed under the T&F preprints policy).
- **Indexing:** Not found on the pages opened (SCImago lists it; Scopus/SSCI not verified here). DBLP not verified.
- **Risk:** Unknown turnaround; small journal with slow issue cadence; 8,000-word cap including references is tight for a 12-page paper.

## 16. Digital Scholarship in the Humanities (Oxford / EADH-ADHO)
**URL:** https://academic.oup.com/dsh/pages/General_Instructions

- **Scope fit:** Good for computational stylometry and authorship attribution (the DH community's home for it); LLM-evaluation framing is secondary.
- **Submission type / length:** "Contributions should not normally exceed 9,000 words in length for full papers (exclusive of notes and references)"; "Short papers... should not exceed 5,000 words." Structured abstract ≤250 words with five mandatory headings; data availability statement; AI disclosure statement.
- **Time to first decision:** Not found (URL tried: General_Instructions).
- **Fees:** Optional OA: "You will need to pay an open access charge to publish under an open access licence" (amount not on the page). No page charges for the subscription route.
- **Author eligibility (quoted):** None stated.
- **Open review or anonymous:** Not found on the page.
- **Preprint policy:** Not found on the page.
- **Indexing:** Not found on the page. DBLP not verified.
- **Risk:** Timeline unknown and DH journals are typically slow (several months to a year to print); fit is good if the paper leans stylometric.

## 17. Language Resources and Evaluation (Springer)
**URL:** https://link.springer.com/journal/10579 (submission guidelines .../submission-guidelines; fees .../how-to-publish-with-us)

- **Scope fit:** Good if the contribution is framed as a multilingual evaluation resource/benchmark and its evaluation ("acquisition, creation, annotation, and use of language resources, together with methods for evaluation of resources, technologies, and applications"). A recent article is "Trends and challenges in authorship analysis: a review of ML, DL, and LLM approaches," so authorship analysis is on the editors' radar.
- **Submission type / length:** Original Paper; no page limit found on the guidelines page. Springer LaTeX template available.
- **Time to first decision:** Journal metrics on the home page: "Submission to first decision (median) 36 days."
- **Fees:** Hybrid: "Authors can also choose to publish under the subscription publishing model (no APC charges apply); both options will be offered after the paper has been accepted." OA APC: "£2590.00 GBP / $3590.00 USD / €2890.00 EUR."
- **Author eligibility (quoted):** None stated. When suggesting reviewers "the Corresponding Author must provide an institutional email address for each suggested reviewer" (a rule about reviewers, not authors).
- **Open review or anonymous:** "This journal follows a single-blind reviewing procedure."
- **Preprint policy:** Springer's standard policy applies (preprints allowed); the specific sentence was not on the filtered text, so: not quoted.
- **Indexing:** Home page lists "DBLP," "SCOPUS," "Science Citation Index Expanded (SCIE)," "ACM Digital Library," "INSPEC," among others. Impact factor "2.0 (2025)."
- **Risk:** Median 36 days is to first decision; acceptance typically needs a revision round, so a final decision by December is possible but not assured. Fit requires a resource/evaluation framing.

## 18. Machine Learning with Applications (Elsevier)
**URL:** https://www.sciencedirect.com/journal/machine-learning-with-applications (opened in the browser pane)

- **Scope fit:** Good: "all aspects of research and development in ML, including but not limited to data mining, computer vision, natural language processing (NLP)."
- **Submission type / length:** Research article; length limit not on the journal page (guide for authors not fetched).
- **Time to first decision:** Journal insights on the page: "1 day Submission to first decision"; "38 days Submission to decision after review"; "89 days Submission to acceptance"; "7 days Acceptance to online publication." (The 1-day figure is the median including desk rejects.)
- **Fees:** Fully OA: "Article Publishing Charge (APC): USD 3,030 (excluding taxes). This journal is taking part in the GPOA program" (geographical pricing). No waiver text on the page.
- **Author eligibility (quoted):** None on the page.
- **Open review or anonymous:** Not found on the page.
- **Preprint policy:** Not found on the page (Elsevier permits preprints generally; not quoted).
- **Indexing:** "CiteScore 12.6," "Impact Factor 6.1" shown; Scopus (Elsevier) implied; DBLP not verified.
- **Risk:** APC $3,030 with no fee-waiver language; fast.

## 19. Expert Systems with Applications (Elsevier)
**URL:** https://www.sciencedirect.com/journal/expert-systems-with-applications (opened in the browser pane)

- **Scope fit:** Moderate: applied intelligent systems; LLM-based text analysis papers are published there.
- **Submission type / length:** Research article; limits not on the journal page.
- **Time to first decision:** "5 days Submission to first decision"; "62 days Submission to decision after review"; "147 days Submission to acceptance"; "7 days Acceptance to online publication."
- **Fees:** Hybrid: "Subscription: No publication fee charged to authors"; OA option "Article Publishing Charge (APC): USD 3,630 (excluding taxes)."
- **Author eligibility (quoted):** None on the page.
- **Open review or anonymous:** Not found on the page.
- **Preprint policy:** Not found on the page.
- **Indexing:** "CiteScore 17.0," "Impact Factor 9.4"; Scopus implied; DBLP not verified.
- **Risk:** Free on the subscription route and a first decision after review in about 9 weeks on the median, but 147 days to acceptance; very high volume and heavy desk-rejection.

## 20. Scientific Reports (Springer Nature)
**URL:** https://www.nature.com/srep/ (fees https://www.nature.com/srep/open-access; about https://www.nature.com/srep/about)

- **Scope fit:** Multidisciplinary; accepts computer science but the readership is not NLP.
- **Submission type / length:** Article; no limit found on the pages opened.
- **Time to first decision:** Not found on the pages opened (the journal-metrics URL https://www.nature.com/srep/journal-metrics returned "Page not found"; the home page had no "first decision" text). Third-party (manusights) says median 21 days; unverified.
- **Fees:** "The current APC, subject to VAT or local taxes where applicable, is: £2290.00/$2850.00/€2490.00." Waivers: for "corresponding authors... based in the world's lowest income countries"; "Requests for APC waivers and discounts from other authors will be considered on a case-by-case basis, and may be granted in cases of financial need... All applications for discretionary APC waivers and discounts should be made at the point of manuscript submission."
- **Author eligibility (quoted):** None on the pages opened.
- **Open review or anonymous:** Not found on the pages opened.
- **Preprint policy:** Not found on the pages opened.
- **Indexing:** "indexed in Web of Science, PubMed, PubMed Central, Scopus, Dimensions, Google Scholar, DOAJ and SAO/NASA ADS." DBLP not verified.
- **Risk:** APC; low signal for NLP; timeline unverified.

## 21. Royal Society Open Science
**URL:** https://royalsocietypublishing.org/rsos/for-authors (charges .../rsos/pages/charges; waivers .../rsos/pages/waivers; overview https://royalsociety.org/journals/open-access/)

- **Scope fit:** Multidisciplinary with a computer science section; accepts sound-science papers regardless of impact.
- **Submission type / length:** "Royal Society Open Science does not have a word limit, but writing should be clear and concise." Article types: research article, review, perspective, Registered Report, replication, etc.
- **Time to first decision:** Not found on the pages opened.
- **Fees:** Gold OA: "Royal Society Open Science £1400 $1960 €1680" (royalsociety.org open-access page). RSOS is **not** in the 2026 Subscribe-to-Open scheme: "Our born open access journals Open Biology and Royal Society Open Science will remain gold open access." Waivers: "We will consider waiving the APC in cases where the authors lack funds, and these will be considered on a case-by-case basis"; "the request must be made at article submission"; applicants "must provide documentary evidence that you have explored alternative funding sources" (e.g. letters from a librarian or head of department). Full waiver for Open Access Equity countries; Read & Publish institutions publish free; certain article types free.
- **Author eligibility (quoted):** None stated.
- **Open review or anonymous:** "The journal operates a single-anonymized peer review policy"; and "Royal Society Open Science operates open peer review for all manuscripts... making the reviewer reports, decision letters and associated author responses accessible alongside published articles."
- **Preprint policy:** "we encourage authors to deposit early versions of articles in appropriate subject repositories or preprint servers"; arXiv submissions can be uploaded "using just the e-print number."
- **Indexing:** PubMed Central deposit stated; Scopus/WoS not on the pages opened. DBLP not verified.
- **Risk:** APC unless a discretionary waiver is granted (documentary evidence required); timeline unknown.

## 22. SoftwareX (Elsevier) — software paper for the pipeline
**URL:** https://www.sciencedirect.com/journal/softwarex (opened in the browser pane)

- **Scope fit:** Only for a paper about the pipeline as reusable software ("acknowledge the impact of software on today's research practice"), not for the attribution findings.
- **Submission type / length:** "Original Software Publication" (short, structured; limit not on the journal page).
- **Time to first decision:** "7 days Submission to first decision"; "43 days Submission to decision after review"; "98 days Submission to acceptance"; "12 days Acceptance to online publication."
- **Fees:** Fully OA: "Article Publishing Charge (APC): USD 1,920 (excluding taxes)."
- **Author eligibility (quoted):** None on the page.
- **Open review or anonymous:** Not found on the page.
- **Preprint policy:** Not found on the page.
- **Indexing:** "CiteScore 3.9," "Impact Factor 1.9"; Scopus implied; DBLP not verified.
- **Risk:** APC; a software paper does not carry the research result.

## 23. JOSS — Journal of Open Source Software — software paper for the pipeline
**URL:** https://joss.theoj.org/about (submitting https://joss.readthedocs.io/en/latest/submitting.html; paper https://joss.readthedocs.io/en/latest/paper.html)

- **Scope fit:** Only as a research-software paper about the LangLLM pipeline. Important scope exclusion: "pre-trained machine learning models and notebooks are not in-scope for JOSS." Software must be "feature-complete (no half-baked solutions)"; "Minor 'utility' packages, including 'thin' API clients, and single-function packages are not acceptable."
- **Submission type / length:** "The paper should be between 750-1750 words" with required sections Summary, Statement of need, State of the field, Software design, Research impact statement, AI usage disclosure.
- **Time to first decision:** Not stated anywhere on the JOSS docs fetched (about, submitting, paper, editing). Process is iterative; "respond to reviewer comments and questions within 2 weeks." Public review history shows months are typical, but that is observation, not a stated figure.
- **Fees:** "There are no fees for submitting or publishing in JOSS"; "diamond open access journal (free to read, free to publish)."
- **Author eligibility (quoted):** "You must be a major contributor to the software you are submitting, and have a GitHub account to participate in the review process." "Purely financial (such as being named on an award) and organizational (such as general supervision of a research group) contributions are not considered sufficient for co-authorship" (so the adjunct co-author must have contributed to the code or its design to be listed). No degree or affiliation requirement. Substantial-effort criteria include "sufficient public development history" of "more than six months prior to submission, with active development spanning that period," "comprehensive testing, clear documentation, and pathways for community contribution," and evidence of "Research impact."
- **Open review or anonymous:** "Submissions, reviews, and editorial decisions all take place as public GitHub issues." Fully open, non-anonymous.
- **Preprint policy:** Not applicable (software paper).
- **Indexing:** Crossref DOI ("a Crossref DOI is minted"); Google Scholar/DBLP not stated on the pages fetched.
- **Risk:** The LangLLM repo would need a public history of 6+ months, tests, docs and contributor guidelines; the pipeline wraps LLM calls and analysis, which reviewers may judge "thin" or ML-model-adjacent. Not a substitute for a research venue.

---

## arXiv endorsement (cs.CL / cs.LG)
**Source:** https://info.arxiv.org/help/endorsement.html (FAQ URL https://info.arxiv.org/help/faq/endorsement.html returned 404).

- Who needs it: "arXiv requires that users be endorsed before submitting their first paper to arXiv or a new category." Some accounts are auto-endorsed: "you have claimed ownership of a paper submitted by a co-author and your email address meets the institutional email criteria." A first-time submitter registering from Gmail will not be auto-endorsed and needs an endorser for the specific archive (cs).
- Who can endorse: "Endorsers must have authored a certain number of papers within the endorsement domain of a subject area." The threshold is per archive and the page does not print the number; it is calibrated so "any active scientist who has been working in their field for a few years should be able to endorse." Only recent papers count: "We only count papers that have been submitted between three months and five years ago." The endorser must also hold "an active positive endorsement to that area yourself." Practically: the UCLA adjunct can endorse for cs if they have several cs.* arXiv papers dated between Dec 2021 and July 2026; the arXiv account page shows whether one is an endorser.
- How the code is obtained: the student "Start[s] a new submission and select[s] the category you wish to submit to," then "Check[s] your email for an endorsement request email. This will include a link you can provide to prospective endorsers"; the request carries a "six-character alphanumeric endorsement code."
- How the endorser acts: they open the link (or the endorsement form) and "enter this code on the endorsement form," where "you can tell us that you do or do not wish to endorse a person."
- What the endorser attests: that "the paper is appropriate for the subject area," and that the author is not "unfamiliar with the basic facts of the field" nor is the work "entirely disconnected with current work in the area." Rules: "You should know the person that you endorse or you should see the paper that the person intends to submit," and "Only provide endorsement to authors seeking to submit their own work, not to third-parties or proxies." arXiv states it cannot find endorsers for authors.
- Practical route: the adjunct co-author registers or already holds an arXiv account with an institutional (ucla.edu) email; whichever student will be the submitting author creates an account, starts the submission in cs.CL, sends the code to the adjunct, who endorses; alternatively the adjunct submits the paper as the submitting author, which needs no endorsement for the students at all (they are just listed authors). Endorsement is per archive (cs), so one endorsement covers cs.CL and cs.LG.

---

## Addendum: pages that could not be opened
- https://www.cell.com/open-access (Patterns APC table): Cloudflare challenge on every attempt (WebFetch 403; browser pane stuck at "Just a moment").
- https://direct.mit.edu/coli/pages/submission-guidelines and .../submissions (Computational Linguistics review model, preprint policy): 403 / Cloudflare.
- https://peerj.com/about/policies-and-procedures/cs (PeerJ CS review model, preprint policy): 403.
- https://dblp.org/search/venue?q=... for every venue: Anubis "Access Denied."
- https://www.nature.com/srep/journal-metrics: "Page not found."
- https://ieeeaccess.ieee.org/authors/peer-review-process/: 404.
- https://info.arxiv.org/help/faq/endorsement.html: 404.
