# Venue hunt, domain D: security, privacy, trustworthy-AI and AI-safety venues

Compiled 20 September 2026 from official pages fetched that day (plus sec-deadlines.github.io and aiworkshoptracker.com as aggregators, marked where used). Target window: submission deadline between 25 September and 15 December 2026, notification within about 10 weeks. Authors: two high-school first authors plus an adjunct faculty co-author at UCLA. Topic: authorship attribution of LLM output, stylometry as a privacy risk, machine translation as an obfuscation attack, LLM self-recognition, provenance of AI text.

Every record follows the same order: name and URL; track; deadline and time zone; notification; page limit and template; review type and blindness; eligibility (with the verdict for a high-school first author with a faculty co-author); dual-submission / arXiv policy; registration fee and in-person requirement (and whether a student rate would cover a high-school student); proceedings; fit; risk. "Not found" always names the URL tried.

Blanket finding on eligibility: **no venue below has any rule on author status or affiliation.** Not one CFP mentions students, degrees, or institutions as a condition of submission; the only student-specific texts are best-student-paper awards and student registration rates. So the verdict everywhere is "not addressed, therefore allowed", unless a record says otherwise. Two practical wrinkles recur: (1) SaTML, USENIX Security and (via ACSAC's author surcharge) some others require one author to register at the **full non-student rate**, which the faculty co-author can cover; (2) student registration rates ask for proof of enrolment and EuroS&P's wording says "university ID card", so a high-school ID may need an email to the registration chair.

---

## Part 1. Deadlines inside the window (25 Sept - 15 Dec 2026), ranked by fit

### 1. IEEE SaTML 2027 (Conference on Secure and Trustworthy Machine Learning)
- **URL:** https://satml.org/ and https://satml.org/call-for-papers/ (HotCRP: https://satml27.hotcrp.com/)
- **Track:** Research papers; also SoK and position papers (position papers 5-12 pages).
- **Deadline:** Mandatory abstract registration **"Tue, Sep 22, 2026"**; paper **"Tue, Sep 29, 2026"**; anonymized artifacts "Fri, Oct 2, 2026". All deadlines "set to 11:59 PM AoE (Anywhere on Earth), which corresponds to UTC-12".
  - **Has the abstract deadline passed?** No. As of 20 Sept 2026 it is two days away. The abstract registration is "mandatory" and the site says "Authors and affiliations cannot be changed after the abstract registration deadline, not even in the camera-ready version" and "Adding or removing authors or affiliations is otherwise grounds for desk rejection." All authors "MUST provide their ORCIDs through the profile page on HotCRP by the abstract registration deadline" and "MUST confirm the submission terms within HotCRP via the Author Certification field by the abstract registration deadline."
  - **Late abstracts:** not addressed anywhere on satml.org (URLs tried: https://satml.org/, https://satml.org/call-for-papers/). No grace period or late-registration text exists; treat the 22 Sept AoE deadline as firm.
- **Notification:** early rejections "Wed, Nov 4, 2026"; interactive discussion "Wed, Nov 25 - Wed, Dec 9, 2026"; final decisions **"Wed, Dec 16, 2026"** (11 weeks after the paper deadline); revision notification "Mon, Feb 1, 2027".
- **Page limit / template:** Research and SoK "up to 12 pages of body text"; "Submissions must be a PDF file in two-column IEEE proceedings style" using `\documentclass[conference]{IEEEtran}` at the default 10pt. "Using a different template, or modifying font size, margins, or spacing to fit more content, is grounds for desk rejection."
- **Review:** double-blind. Papers "must be properly anonymized", omit "reference to the authors' names or their institutions", cite own work "in the third person"; "de-anonymization through additional material such as artifacts are grounds for rejection." Conflicts must be declared by the abstract deadline.
- **Eligibility:** "The Call for Papers contains no explicit language regarding student status, eligibility criteria, or restrictions for authors." Only requirements are ORCID for every author and a fixed affiliation at abstract registration. **Verdict: not addressed, so allowed.** Both students need ORCIDs (free) before 22 Sept AoE and the high school is entered as their affiliation.
- **Dual submission / arXiv:** "Submitted papers must not substantially overlap with papers that have been published or accepted for publication, or that are simultaneously under submission" elsewhere. Authors "may give talks about their work, post a preprint of the paper online" but "publicly advertising their work on social media" "may lead to desk rejection." Papers previously rejected elsewhere must "append those prior reviews" with a description of how they were addressed.
- **Registration / in-person:** "All presentations at SaTML 2027 to take place in person at the conference." A paper appears in the proceedings only if "at least one author registers (with the full non-student registration fee)" and it is "presented in person, on site." Fees for 2027 not posted: https://satml.org/attend/ says it "will be updated as the conference approaches"; the 2026 fee table is behind a Cvent registration app (https://web.cvent.com/event/679f866a-df96-4a57-a83e-25a5057d79a3/) that shows only deadlines, so amounts are **not found**. The student-rate question is moot because one full-rate registration is mandatory anyway (the UCLA co-author). Conference: Reykjavik, Iceland, 8-10 May 2027.
- **Proceedings:** "published in the IEEE Computer Society Digital Library, and authors are encouraged to also make them freely available via arXiv."
- **Fit:** Strong. Listed areas include "Privacy in machine learning", "Forensic analysis of machine learning", "Novel attacks on machine learning" and "Trustworthy machine learning in cybersecurity applications", which is exactly where attribution-as-privacy-risk, translation-as-obfuscation and provenance sit. SaTML is the most on-topic venue in this domain.
- **Risk:** The calendar. Abstract with locked author list and ORCIDs due in 2 days, a 12-page IEEE paper in 9 days, and an in-person trip to Iceland in May 2027 with a full-rate registration. Notification lands on 16 Dec, just past 10 weeks. Only worth it if the manuscript is already near complete.

### 2. PETS 2027 / PoPETs 2027 Issue 3 (Privacy Enhancing Technologies Symposium)
- **URL:** https://petsymposium.org/cfp27.php ; author guide https://petsymposium.org/authors-2027.php (mirror https://crysp.petsymposium.org/authors-2027.php); submission https://submit.petsymposium.org/
- **Track:** Regular PoPETs paper (journal-style, four issues a year).
- **Deadline:** Issue 3 **"Paper submission deadline: November 30, 2026 (firm)"**; all deadlines "23:59:59 Anywhere on Earth, UTC-12". (Issue 2 was 31 Aug 2026 - passed; Issue 4 is 28 Feb 2027.)
- **Notification:** Issue 3 rebuttal "January 12-18, 2027"; **author notification "February 1, 2027"** (9 weeks); revision deadline 1 March 2027; camera-ready 15 March 2027.
- **Page limit / template:** "Submissions and resubmissions to PoPETs must consist of at most 12 typeset pages for the main body of the paper." The mandatory PoPETs 2027 LaTeX template (https://petsymposium.org/files/submission-template.zip) adds three required sections that do not count: ethical considerations, open science, and AI use. One extra page (13) is allowed at revision/camera-ready.
- **Review:** "All submitted papers will be judged based on their quality and relevance through double-blind reviewing, where the identities of the authors are withheld from the reviewers." Remove names, affiliations and identifying funding; cite own work "in the third person, just as you would any other piece of related work."
- **Eligibility:** No rule on author status. The only student text is the award: "Papers written solely or primarily by a student who is presenting the work at PETS are eligible for the award" (https://petsymposium.org/student-paper-award.php); "student" is not defined. The AI policy adds "human authors must have made substantial intellectual contributions" and "Generative AI tools cannot be listed as authors." **Verdict: not addressed, so allowed**; two high-school first authors would plausibly qualify the paper for the Andreas Pfitzmann Best Student Paper Award if one of them presents.
- **Dual submission / arXiv:** "Submitted papers must not substantially overlap with papers that have been published or that are simultaneously submitted to a journal or a conference with proceedings. Simultaneous submission of the same work to multiple venues ... constitute[s] dishonesty or fraud." Preprints: "we discourage authors from publicly posting pre-prints of their submissions while under review (e.g., on arXiv or their personal website)"; sharing "directly with collaborators or sponsors, and/or posting it in a non-public archive" is fine. Rejected papers (Early Reject or Reject) "must skip one full issue before resubmitting" and resubmissions need a change summary.
- **Registration / in-person:** "Authors of accepted papers are strongly encouraged to attend and present at the physical event" but "in-person attendance is not strictly required for publication in the proceedings." (Note that the 2026 registration page said "Each paper must be presented in person, by a co-author of the paper"; the 2027 CFP wording above is the newer one. Confirm with the chairs before relying on remote publication.) Fees for 2027 not posted; PETS 2026 (https://petsymposium.org/2026/registration.php) charged in Canadian dollars: "Full PETS: $1000 early / $1200 late", "PETS only: $700 early / $850 late", "Virtual: $300", and **no student rate was listed** on that page, so the student-rate question does not arise. PETS 2027 venue: TU Delft, Netherlands (per the TU Delft event listing found in search; dates not on the CFP page fetched).
- **Proceedings:** Proceedings on Privacy Enhancing Technologies (PoPETs), open access.
- **Fit:** Strong. Topics of interest include "Machine learning and privacy", "Information leakage, data correlation, and abstract attacks on privacy" and "Traffic analysis". Stylometric deanonymization and obfuscation are a long-standing PETS thread (the authorship-obfuscation and Anonymouth literature published here), so translation-as-obfuscation and attribution-as-leakage will find expert reviewers.
- **Risk:** PoPETs reviewers expect a privacy framing (threat model, adversary, leakage measurement), not a pure ML-attribution paper; the 12-page journal format is heavier than a workshop. The preprint discouragement conflicts with arXiv-first plans. Skip-an-issue rule if rejected.

### 3. ACM FAccT 2027 (Conference on Fairness, Accountability, and Transparency)
- **URL:** https://facctconference.org/2027/cfp.html ; author guide https://facctconference.org/2027/authorguide.html
- **Track:** Archival paper (or non-archival option). Blog notes the timeline moved earlier from 2027 on (https://facct-blog.github.io/2026-06-24/submission-timeline).
- **Deadline:** **Abstract "October 27, 2026"; papers "November 3, 2026"**; "All at 11:59 PM Anywhere On Earth." Author list is locked at abstract time: authors "cannot modify the registered list of authors" afterwards.
- **Notification:** **"First round decisions: December 22, 2026"** (7 weeks); "Revisions due: January 28, 2027"; "Final decisions: March 23, 2027".
- **Page limit / template:** "Submitted papers must be up to 14 pages (including all figures and tables) in single-column format, plus unlimited pages for references"; revised/accepted papers up to 15 pages, plus one page for "ethics, adverse impacts, and other statements". ACM TAPS workflow; LaTeX `\documentclass[manuscript,screen,review,anonymous]{acmart}` (Word also accepted).
- **Review:** anonymized ("Submissions must be anonymized and may not contain any identifying information"; own work in third person; no Acknowledgements, Author Contributions, Competing Interests or Positionality sections at submission). The term "double-blind" is not used but the process is.
- **Eligibility:** "Author Eligibility: Not specified in CFP." **Verdict: not addressed, so allowed.**
- **Dual submission / arXiv:** "You may not submit papers that are identical, or substantially similar to papers that are currently under review at another peer-reviewed conference or journal, have been previously published, or have been accepted for publication." Preprints explicitly welcome: "FAccT welcomes work that is already available without peer review as a technical report (e.g., in SSRN, arXiv, or similar). In this case, the authors should not cite the report, to preserve anonymity."
- **Registration / in-person:** "At least one author of each accepted paper must register for, attend, and present the work at the conference." Conference "June 21-24 2027" (location not on the CFP). 2027 fees not posted; FAccT 2026 (https://facctconference.org/2026/registration.html) was in Canadian dollars with a category "Non-Profit/Student (including academic postdocs)": in-person early bird CAD 184 (ACM member) / 227 (non-member); virtual student CAD 114 / 140. Student is not defined beyond the label, so a high-school student is not excluded; the rate is very low in any case.
- **Proceedings:** archival papers in the ACM Digital Library; non-archival option (abstract only).
- **Fit:** Moderate. FAccT takes sociotechnical framings of accountability, provenance and privacy; a paper positioned as "attribution of AI text is a privacy and accountability problem, and translation breaks it" fits, whereas a pure benchmark of attribution accuracy does not. Interdisciplinary reviewers.
- **Risk:** First-round decision is fast but the final decision is late March; papers may get "revise" rather than accept. Framing must carry the societal argument, not just the numbers.

### 4. ACM CODASPY 2027 (Conference on Data and Application Security and Privacy)
- **URL:** https://www.codaspy.org/2027/ and https://www.codaspy.org/2027/cfp.html
- **Track:** Research paper (also Dataset/Tool, SoK, BlueSky tracks).
- **Deadline:** **Abstract "November 16, 2026"; paper "November 23, 2026"**, "Anywhere on Earth".
- **Notification:** **"January 25, 2027"** (9 weeks); camera-ready 26 March 2027.
- **Page limit / template:** Research papers "at most 12 pages in double-column ACM 'sigconf' format" (Dataset/Tool 6, SoK 15, BlueSky 10); ACM Proceedings Template.
- **Review:** Research and Dataset/Tool submissions "must be anonymized" (double-blind); BlueSky and SoK "not required to be anonymous".
- **Eligibility:** nothing on author status. **Verdict: not addressed, so allowed.**
- **Dual submission / arXiv:** "Submitted papers must not substantially overlap with papers that have been published or that are simultaneously submitted to a journal, conference or workshop." arXiv not mentioned on the CFP page.
- **Registration / in-person:** not stated on the CFP page fetched (https://www.codaspy.org/2027/cfp.html); conference "June 14 - 17, 2027", "Fort Collins, Colorado, USA". Fees not posted. Note on open access: authors from institutions not in ACM Open pay an APC, "$500 (ACM/SIG Members) or $750 (Non-Members)"; UCLA's ACM Open status would decide this.
- **Proceedings:** ACM (ACM Digital Library).
- **Fit:** Moderate. Topics include "Artificial intelligence / machine learning for security", "Privacy-preserving techniques" and "Trustworthy artificial intelligence / machine learning". A mid-tier ACM security venue that is friendlier than S&P/CCS and has a fall deadline that fits the window exactly.
- **Risk:** Less visible than SaTML or PETS; reviewer pool is data-security rather than NLP, so the stylometry background must be self-contained. Possible APC.

### 5. IEEE EuroS&P 2027 (European Symposium on Security and Privacy)
- **URL:** https://eurosp2027.ieee-security.org/cfp.html
- **Track:** Main research track.
- **Deadline:** **Abstract registration "25 November 2026 (Wednesday)"; paper "02 December 2026 (Wednesday)"**, "Anywhere on Earth - UTC-12h".
- **Notification:** early rejection "28 January 2027"; rebuttal "24 February - 01 March 2027"; **author notification "18 March 2027"** (15 weeks; outside the 10-week target).
- **Page limit / template:** "Papers shall not exceed 13 pages of body text, with unlimited additional pages for references and appendices." LaTeX only, supplied eurosp2027-template.zip, **A4** paper, PDF.
- **Review:** anonymous ("no author names or affiliations may appear on the title page"; own work in third person).
- **Eligibility:** only "Maximum seven papers per author." **Verdict: not addressed, so allowed.**
- **Dual submission / arXiv:** "Simultaneous submission of the same paper or substantially similar paper to another venue ... is not allowed." Preprints on arXiv are permitted during review.
- **Registration / in-person:** "One of the authors of the accepted paper is expected to present the paper at the conference," with possible remote allowances for legitimate reasons. Madrid, 5-9 July 2027. 2027 fees not posted; EuroS&P 2026 (https://eurosp2026.ieee-security.org/registration.html) charged in euros: regular early bird EUR 955 (IEEE member) / 1,150 (non-member); student EUR 670 / 805; "Students must provide proof of their status at registration time by submitting a copy of the university ID card or an official institutional webpage confirming their enrollment." A high-school ID is not what that sentence describes; ask the registration chair. "At least one author per accepted paper must register" by a fixed date.
- **Proceedings:** IEEE (Computer Society Digital Library; the CFP page did not state it explicitly, so marked as expected).
- **Fit:** Moderate-to-strong for a security audience (privacy, ML security are core topics).
- **Risk:** Notification in March 2027 misses the 10-week target by five weeks; competitive top-tier bar; A4 LaTeX template quirk.

### 6. IEEE S&P 2027 (Oakland), second deadline
- **URL:** https://sp2027.ieee-security.org/cfpapers.html
- **Track:** Main research track.
- **Deadline:** **Abstract "November 10, 2026"; paper "November 17, 2026"**, "AoE UTC-12". (First deadline 11 June 2026 passed.)
- **Notification:** early reject "January 18, 2027"; reviews "February 11, 2027"; rebuttal "February 16, 2027"; **acceptance "March 5, 2027"** (15.5 weeks; outside target).
- **Page limit / template:** "up to 13 pages of text and up to 5 pages for references and appendices, totaling no more than 18 pages"; `\documentclass[conference,compsoc]{IEEEtran}`.
- **Review:** anonymous submission; own work in third person. Any author "may submit no more than 6 papers per cycle." All authors must give ORCIDs at abstract registration.
- **Eligibility:** nothing on author status. **Verdict: not addressed, so allowed.**
- **Dual submission / arXiv:** "Simultaneous submission of the same paper to another venue with proceedings or a journal is not allowed and will be grounds for automatic rejection." Authors may "post a preprint of the paper to an archival repository such as arXiv" but should avoid widespread advertising.
- **Registration / in-person:** "One of the authors of the accepted paper is expected to register and present the paper at the conference." Montreal, 17-20 May 2027. Fees not found (https://sp2026.ieee-security.org/registration.html and /attend.html both 404).
- **Proceedings:** "published, open access, in the Computer Society's Digital Library".
- **Fit:** On-topic but the acceptance bar (top-4 security venue) is far above a first paper from high-school authors.
- **Risk:** Very low acceptance odds; notification well past 10 weeks. Recorded for completeness.

### 7. IEEE CSF 2027 (Computer Security Foundations Symposium), fall cycle
- **URL:** https://csf2027.ieee-security.org/ and https://csf2027.ieee-security.org/cfp.html
- **Track:** Main track (three cycles).
- **Deadline:** **fall cycle "October 15, 2026"**, "AoE (UTC-12h)". (Summer cycle 3 Aug passed; winter cycle 28 Jan 2027.)
- **Notification:** **"December 14, 2026"** (8.5 weeks).
- **Page limit / template:** "at most 12 pages long, not counting acknowledgments on the usage of AI if any, bibliography, and well-marked appendices"; "two-column IEEE Proceedings style".
- **Review:** "CSF 2027 will employ double-blind reviewing."
- **Eligibility:** only "At least one coauthor of each accepted paper is required to attend CSF to present the paper." **Verdict: not addressed, so allowed.**
- **Dual submission / arXiv:** "Submitted papers must not substantially overlap with papers that have been published or that are simultaneously submitted to a journal or a conference with published proceedings." arXiv not mentioned.
- **Registration / in-person:** one co-author must attend; Tokyo, 13-17 September 2027. Fees not posted.
- **Proceedings:** "published by the IEEE Computer Society Press".
- **Fit:** Weak. CSF is a foundations venue (formal methods, information flow, proofs); "security and privacy aspects of machine learning" is listed, but an empirical attribution study would be an outlier.
- **Risk:** Mismatch with the reviewer culture; September 2027 conference in Tokyo.

### 8. ACM ASIA CCS 2027, second round
- **URL:** official site **not found** (tried https://asiaccs2027.github.io/ - 404, https://asiaccs2027.org/ - no such host). Data below is from the aggregator https://sec-deadlines.github.io/ only.
- **Deadline:** "Deadline (2 / 2): 2026-12-11 23:59" (AoE per the aggregator's convention); conference "July 12-16 // Macau".
- Notification, page limit, review, eligibility, arXiv, fees, proceedings: **not found** (no official page reached).
- **Fit:** ASIA CCS is a general ACM security conference (ACM proceedings) that accepts ML-security and privacy papers; comparable tier to CODASPY.
- **Risk:** Unverified; find the official site before planning around it.

### 9. NeurIPS 2026 workshop with a deadline still open: InfPriv fast track
- **Workshop:** "Beyond Private Training: The New Landscape of AI Privacy" (InfPriv 2026), Sydney, 11-12 Dec 2026. URL https://beyond-private-training.ai.studio/ (the page is script-rendered and returned only its title; OpenReview group NeurIPS.cc/2026/Workshop/InfPriv gives "Submission Deadline: Sep 08 2026 12:00PM UTC-0" for the main track).
- **Deadline:** per https://aiworkshoptracker.com/conference/neurips/2026/ , "InfPriv (Fast Track) - Due Sep 26, 2026, 11:59 UTC". Not confirmed on an official page.
- Notification, page limit, review, eligibility, arXiv, proceedings: **not found** on an official page (URLs tried above). NeurIPS workshops are non-archival by default and the mandatory workshop author-notification date is 29 Sept 2026.
- **Fit:** Good in principle (privacy of/through foundation models; stylometric leakage is a privacy attack).
- **Risk:** Fast-track deadlines usually take papers already reviewed elsewhere (e.g. NeurIPS main-track rejects); in-person Sydney in December; unverified.

### Other in-window deadlines seen on sec-deadlines.github.io but off-topic
ACNS 2027 (24 Sept, cycle 1), FC 2027 (24 Sept, financial crypto), DFC Europe 2027 (9 Oct, forensics), CT-RSA 2027 (22 Oct, crypto), WWW 2027 (25 Oct, Dublin; abstract one week earlier - a Web-conference "trust and safety"/privacy track could fit but is a sibling domain), HOST 2027 (8 Nov, hardware), CASCADE 2027 (10 Nov), ACISP 2027 (30 Nov, Melbourne, cycle 1), DSN 2027 (2 Dec, dependability). Not researched further.

---

## Part 2. Requested venues whose deadlines are outside the window (passed or not yet announced)

### USENIX Security 2027
- **URL:** https://www.usenix.org/conference/usenixsecurity27/call-for-papers
- **Cycle 1:** registration 18 Aug 2026, submission 25 Aug 2026 (passed). **Cycle 2: registration "Tuesday, January 19, 2027", submissions "Tuesday, January 26, 2027"**, artifacts 29 Jan 2027, "All dates AoE"; early reject 9 Mar 2027; rebuttal 8-15 Apr; **notification "Thursday, May 6, 2027"** (14 weeks). Outside the window on both ends.
- Page limit "13 pages of body text" plus unlimited appendices (camera-ready max 20); USENIX template; "Papers must be submitted for anonymous review". Simultaneous submission to archived venues "constitute[s] dishonesty or fraud"; preprints allowed during review without identity-revealing publicity. Registration: "at least one of the authors will register to attend the Symposium at full price (i.e., not the student rate) and to present the paper." USENIX Security '26 fees (https://www.usenix.org/conference/usenixsecurity26/registration-information): general US$1,100 early / 1,400 standard; student US$625 / 775 (student not defined). Eligibility: **not addressed, so allowed.** Fit: strong topic-wise, top-tier bar.

### NDSS 2027 and its workshops
- **URL:** https://www.ndss-symposium.org/ndss2027/submissions/call-for-papers/ ; co-located events page https://www.ndss-symposium.org/ndss2027/co-located-events/ (still shows the 2023 list).
- Main track: fall cycle deadline "Wed, 19 August 2026" (passed); notification 24 Nov 2026. 13 pages, NDSS template, double-blind; "Publishing a technical report on a preprint repository, such as arXiv, while not encouraged, is not forbidden." Proceedings by the Internet Society, free.
- **Workshops for 2027: not yet listed.** https://www.ndss-symposium.org/ndss2027/submissions/ says only "The call for co-located workshops for the 2027 symposium is now open." Symposium is 22-26 March 2027 in Seoul, so workshop paper deadlines will most likely fall in December 2026 - January 2027 (USEC, AISCC, MADWeb, WOSOC etc. historically). Re-check in mid-October. Fit if a USEC/AISCC-type workshop appears: good.

### ACM CCS 2026 workshops (The Hague, 15 and 19 Nov 2026)
- **URL:** https://www.sigsac.org/ccs/CCS2026/workshops/workshops.html (lists 15 workshops with organizers and dates but no links or deadlines).
- **WPES 2026** (https://wpes2026.github.io/cfp.html): deadline "July 24, 2026 (11:59 PM AoE, UTC-12)", notification "September 4, 2026" - **passed**. 12 pages ACM double-column (or 4-page short); "Submissions should not be anonymized" (single-blind); workshop 15 Nov 2026. Eligibility not addressed. Fit would have been good.
- **AISec 2026** (https://aisec.cc/): "Paper submission deadline: July 24th, 2026 (firm)", "23:59 / 11:59pm AoE"; notification "September 9th, 2026" - **passed**. 10 pages + 2 for appendices, ACM CCS format, "properly anonymized"; ACM DL proceedings; 15 Nov 2026. Eligibility not addressed. Fit would have been strong.
- **TAKEDOWN 2026**: deadline 13 July 2026 (sec-deadlines) - passed.
- **3D-Sec (Deepfake, Deception, and Disinformation Security), LAMPS (Large AI Systems and Models with Privacy and Safety Analysis), TrustAICyberSec, SaTS, AGENT-SEC**: the CCS page gives organizers only (3D-Sec: "Abuadbba, Sharif (Data61, Marsfield)"; LAMPS: "Jason Xue"); no URLs or deadlines found (URL tried: the CCS workshops page above; web-search budget was exhausted before individual sites could be located). With workshop dates of 15/19 Nov 2026 and camera-ready needed by late Oct, their deadlines have almost certainly passed. 3D-Sec would have been the best topical match of the set.

### ACSAC 2026 and workshops (Los Angeles, 7-11 Dec 2026)
- **URL:** https://www.acsac.org/2026/submissions/papers/ - main deadline "May 26 (23:59 AoE) - firm deadline"; acceptance 8 Sept 2026 - **passed**. 11 pages IEEE compsoc, double-blind, in-person expected.
- **Workshops** (https://www.acsac.org/2026/workshops/): AIDC, ARTMAN (Trustworthy ML), BioAISS, CSET, HealthSec, ICSS, LASER, WAITI. The ACSAC pages list no deadlines. ARTMAN's site https://artman-workshop.gitlab.io/ could not be fetched (domain blocked by the fetch tool). LASER's CFP PDF (https://www.acsac.org/2026/workshops/laser/LASER2026-CFP.pdf) says "LASER does not solicit separate workshop papers"; it invites "authors of accepted IEEE ACSAC papers" only, so it is closed to outside submissions. ACSAC 2026 fees (https://www.acsac.org/2026/registration/): technical program regular $1,440 / student $1,010 (early); workshop day regular $480 / student $340; "author surcharge: $125 per paper"; student not defined.
- **Verdict:** no open ACSAC route this year, since the ARTMAN deadline could not be verified and it is a December workshop (assume passed).

### IEEE CNS 2026
- **URL:** https://cns2026.ieee-cns.org/authors/call-papers (returned HTTP 418 to the fetch tool; data from the ComSoc listing and IEEE ComSoc social posts found in search). Deadline 11 May 2026, extended to 18 May 2026; conference 14-17 Sept 2026, Delaware - **passed and already held**.

### IEEE TPS-ISA 2026 (now "IEEE TPS")
- **URL:** https://tps.ieee-cs.org/2026/call-for-papers/ - Round 2 submission "August 15, 2026 -> August 22, 2026", notification "September 22, 2026", "Anywhere on Earth"; conference 4-6 Nov 2026, San Jose. **Passed.** 10 pages IEEE two-column, anonymous submission, AI-disclosure statement required. Eligibility not addressed.

### ARES 2027
- **URL tried:** https://www.ares-conference.eu/ (shows only ARES 2026: 24-27 Aug 2026, Linköping); http://www.wikicfp.com/cfp/program?id=216 (connection reset twice). **ARES 2027 not announced.** ARES 2026 had abstract 2 Mar / paper 9 Mar 2026, so expect a late-Feb/March 2027 deadline: outside the window. ARES workshops (e.g. on AI security) historically share that spring deadline.

### IEEE S&P 2027 workshops (DLSP, ConPro, SafeThings, WOOT)
- **URL:** https://sp2027.ieee-security.org/workshops.html still lists the **2026** workshops (LangSec, CyberBio, ArtSec, SAGAI, ConPro, MetaCRiSP, Data4SoftSec, AVID; all URLs end in "26"). **No 2027 workshop CFPs are posted.** Reference points: ConPro '26 (https://conpro26.ieee-security.org/) had deadlines "January 14, 2026 (11:59:59PM ET)" / "January 22, 2026 (AoE)", notification 11/18 Feb 2026; DLSP and SafeThings 2026 sites did not resolve (https://dlsp2026.ieee-security.org/, https://safethings26.ieee-security.org/: no such host). **WOOT is no longer an S&P workshop**: WOOT '26 (https://www.usenix.org/conference/woot26/call-for-papers) was "co-located with the 35th USENIX Security Symposium", with cycle 1 due "Friday, December 12, 2025, 11:59 pm AoE" and cycle 2 "March 3, 2026". WOOT '27's page (https://www.usenix.org/conference/woot27/call-for-papers) is 404; if it follows the 2026 pattern its cycle 1 would fall in mid-December 2026 - inside the window - but WOOT is an offensive-technologies venue and a poor topical fit. Expect S&P 2027 workshop deadlines in January-February 2027, outside the window.

### EuroS&P 2027 workshops
- **URL:** https://eurosp2027.ieee-security.org/workshops.html - lists IWPE, WACCO, WoRMA, XAISEC, SCID ("has been cancelled by the organizers"), ACSW, DeMeSSAI, SeRIM, SPIQE; no deadlines on the page. With a July 2027 conference these will be spring 2027 deadlines: outside the window. Note the cancelled SCID (Security-Centric Strategies for Combating Information Disorder) would have been an on-topic misinformation workshop.

### SaTML workshops
- **Not found.** satml.org lists no workshop programme for 2027 (URLs tried: https://satml.org/, https://satml.org/call-for-papers/, https://satml.org/attend/); SaTML runs competitions rather than workshops.

### NeurIPS 2026 workshops on safety / privacy / provenance (recorded even if a sibling agent covers them)
Source: https://blog.neurips.cc/2026/08/10/announcing-the-neurips-2026-workshops/ (three sites: Sydney 11-12 Dec, Paris and Atlanta 12-13 Dec) and each workshop's page. All main-track deadlines have **passed** (NeurIPS suggested 29 Aug 2026; mandatory notification 29 Sept 2026):
- **FLMSec, Foundations of Language Model Security** (Paris) https://flmsec.github.io/ - deadline "August 27, 2026", "23:59 AoE"; up to 8 pages, NeurIPS workshop template; "Reviewing is double-blind"; non-archival; "Previously published work is not eligible"; notification 25-29 Sept. Passed.
- **PriLOM, Privacy in the Era of Large Opaque Models** (Paris) https://neurips-workshop2026.github.io/foundation_model_agentic_privacy/call_for_papers.html - deadline "Friday, 5th of September (12 AM AOE)"; notification "September 29, 2026, AoE"; short papers up to 4 pages; "work available on preprint servers such as arXiv is permitted"; "non-archival venue"; "All accepted papers must be presented in person". Passed.
- **ATTRIB, Attributing Model Behavior at Scale: Data Attribution and Provenance** (Sydney) https://attrib-workshop.cc/ - deadline "September 5 (AOE)"; notification "September 29"; main track 3-6 pages, idea track 2-4; double-blind; non-archival; reciprocal reviewing ("at least one author is expected to serve as a reviewer"). Passed.
- **InfPriv, Beyond Private Training** (Sydney) - main deadline 8 Sept 2026 12:00 UTC (OpenReview); fast track 26 Sept 11:59 UTC per aiworkshoptracker (see Part 1, item 9).
- **AI4GOOD, Trustworthy AI for Good** (Paris) https://trustworthy-ai-for-good.github.io/ - deadline "1 Sep 2026", "11:59 PM AoE"; notification "29 Sep 2026"; 2-9 pages; non-archival by default; submissions under review elsewhere allowed subject to the other venue's rules. Passed.
- **TAI-Eval, Trustworthy AI Evaluation** (Sydney) https://tai-eval.github.io/ - deadline "August 29, 2026 (AoE)"; notification "September 22, 2026 (AoE)". Passed.
- Also listed: Agents in the Wild (safety/security), Who Verifies the Agents?, Can We Trust the Judge?, Child Safety in AI (4 pages, deadline 30 Aug), Dynamic Alignment; all passed. No 2026 edition of SoLaR, Red Teaming GenAI, Safe Generative AI or Lock-LLM appears in the 2026 list.
- Eligibility: none of these pages mentions author status. NeurIPS registration is required to attend; workshop-only registration exists but 2026 rates were not fetched.

### FAccT 2027 - see Part 1, item 3 (in window).

### AIES 2027
- **URL tried:** https://www.aies-conference.com/ (shows AIES 2026 only: Malmo, 12-14 Oct 2026). **AIES 2027 not announced.** AIES 2026 (https://www.aies-conference.com/2026/call-for-papers/) had abstract "May 14, 2026 - 11:59 AoE", submission "May 21, 2026 - 11:59pm AoE", notification "July 16, 2026"; 10 pages AAAI kit; "doubly-anonymized"; arXiv/SSRN preprints welcome; archival in the AAAI Digital Library or non-archival option; one author must attend. Expect a May 2027 deadline: outside the window. Note AIES 2026's LLM rule: "Papers that include text generated from a large-scale language model (LLM) such as ChatGPT are prohibited unless the produced text is presented as a part of the paper's experimental analysis" - a paper about LLM outputs is fine, but AI-assisted prose is not.

### TrustNLP 2027
- **URL tried:** https://trustnlpworkshop.github.io/ (shows the 6th edition at ACL 2026: deadline "March 5, 2026", fast track "April 10, 2026", notification "April 28, 2026"; 8/4 pages; double-blind; archival with a non-archival cross-submission option; "At least one of the authors of each accepted paper must register for the workshop and present the paper"). **2027 edition not announced**; expect a Feb-Mar 2027 deadline tied to ACL/NAACL 2027: outside the window. Fit would be strong (privacy-preserving and robust NLP).

### Truth and Trust Online (TTO)
- **URL tried:** https://truthandtrustonline.com/ - the latest edition shown is TTO 2022 (13-14 Oct 2022, Boston). **Dormant; no 2025 or 2026 edition found.**

### CySoc (International Workshop on Cyber Social Threats)
- **URL tried:** https://cy-soc.github.io/2026/ - 7th edition at ICWSM 2026 had submission "March 22nd, 2026", notification "April 8th, 2026". **CySoc 2027 not announced**; expect ~March 2027. Outside the window.

### ICWSM 2027 (for the misinformation angle)
- **URL:** https://www.icwsm.org/2027/submit/ - cycles "15th Sep 2026" (notification 15 Nov 2026; **passed five days ago**) and "15th Jan 2027" (notification 15 Mar 2027), "23:59 AoE"; full papers up to 11 pages AAAI two-column, double-blind; Edinburgh 2027; "Papers receiving an R&R in January 2027 will not be presented at ICWSM 2027." Outside the window.

### MisinfoCon and other misinformation venues
- **MisinfoCon:** not found as a 2026 call (search returned no event of that name with a fall deadline).
- **MisD 2026, Misinformation Detection in the Era of LLMs** (https://sites.google.com/view/misd-2026): deadline 31 Mar / 5 Apr 2026, at ICWSM 2026 - passed.
- **Cambridge Disinformation Summit 2026** (https://www.mctd.ac.uk/call-for-papers-cambridge-disinformation-summit-2026/ and the SSRN announcement https://www.ssrn.com/index.cfm/en/janda/announcement/?id=15559): both returned HTTP 403 to the fetch tool; deadline **not found**.
- **2nd European Congress on Disinformation and Fact-Checking**: the NordMedia page fetched (https://nordmedianetwork.org/latest/call-for-papers/call-for-papers-2nd-european-congress-on-disinformation-and-fact-checking-hybrid/) describes the 2025 edition (Madrid, 29-30 Oct 2025, deadline 15 Sept 2025); the search snippet placing a congress at Copenhagen on 19-20 Nov 2026 could not be verified and its deadline is **not found**.
- **"From Prompt to Propaganda: Generative AI and the New Dis/Mis-Information Lifecycle"** (https://cybercni.fr/2026/04/30/ai-generative-disinformation-call-for-submissions-2026/): workshop 22 Sept 2026, deadline 7 May 2026 - passed. LNI open-access proceedings.

---

## Part 3. Summary table (in-window only)

| Venue | Deadline (AoE unless noted) | Notification | Weeks | Blind | Eligibility verdict | In-person | Fit |
|---|---|---|---|---|---|---|---|
| IEEE SaTML 2027 | abstract 22 Sept, paper 29 Sept 2026 | 16 Dec 2026 (early reject 4 Nov) | 11 | double | not addressed, allowed; ORCIDs by 22 Sept | yes, Reykjavik May 2027, one full-rate reg | strong |
| PETS 2027 Issue 3 | 30 Nov 2026 (firm) | 1 Feb 2027 | 9 | double | not addressed, allowed; student award possible | strongly encouraged, not required for publication | strong |
| ACM FAccT 2027 | abstract 27 Oct, paper 3 Nov 2026 | first round 22 Dec 2026; final 23 Mar 2027 | 7 / 20 | anonymized | not addressed, allowed | yes, June 2027 | moderate |
| ACM CODASPY 2027 | abstract 16 Nov, paper 23 Nov 2026 | 25 Jan 2027 | 9 | double (research track) | not addressed, allowed | not stated; Fort Collins June 2027 | moderate |
| IEEE EuroS&P 2027 | abstract 25 Nov, paper 2 Dec 2026 | 18 Mar 2027 | 15 | anonymous | not addressed, allowed | expected, Madrid July 2027 | moderate-strong |
| IEEE S&P 2027 (2nd) | abstract 10 Nov, paper 17 Nov 2026 | 5 Mar 2027 | 15.5 | anonymous | not addressed, allowed | expected, Montreal May 2027 | on-topic, very low odds |
| IEEE CSF 2027 fall | 15 Oct 2026 | 14 Dec 2026 | 8.5 | double | not addressed, allowed | yes, Tokyo Sept 2027 | weak |
| ACM ASIA CCS 2027 (2nd) | 11 Dec 2026 (aggregator only) | not found | - | not found | not found | Macau July 2027 | moderate, unverified |
| NeurIPS InfPriv fast track | 26 Sept 2026 11:59 UTC (aggregator only) | not found | - | not found | not found | Sydney 11-12 Dec 2026 | good, unverified |

## Part 4. Gaps and what could not be verified
- Web-search budget for this session ran out after the first pass; everything after that came from direct page fetches, so a few workshop sites (3D-Sec, LAMPS, TrustAICyberSec, ARTMAN, ASIA CCS 2027) were never located or were blocked.
- Registration fees for 2027 are unpublished everywhere; 2026 figures are given as reference where a page was reachable (USENIX Security, EuroS&P, ACSAC, FAccT, PETS). SaTML and S&P fee tables were not reachable.
- No venue defines "student" for its student rate except EuroS&P ("university ID card or an official institutional webpage confirming their enrollment"), which is the one place a high-school ID might be questioned.
- SaTML late-abstract policy: no text exists; the only safe reading is that a missed 22 Sept AoE abstract registration means no submission this year.
