# IEEE BigData 2026 High School Symposium — submission rules

Researched 19 Sept 2026 from the official pages (fetched raw HTML, quoted verbatim below).
Official name on the site: **"IEEE BigData 2026 High School Symposium"** (the "3rd High School Symposium"), part of the 2026 IEEE International Conference on Big Data, Sheraton Phoenix Downtown, 340 N 3rd St, Phoenix, AZ 85004, Dec 14–17, 2026.

Primary source: https://bigdataieee.org/BigData2026/high-school-symposium/

## 1. Submission deadline and time zone

Symposium page, verbatim:

> Paper Submission Deadline: September 20 2026
> Notification of Acceptance: October 9,2026
> Camera-Ready Paper Submission: October 24, 2026
> Symposium Date: December 17, 2026

- **Time zone: unspecified** on the symposium page. The raw HTML contains no "AoE", "PST", "11:59" or "midnight" string (grepped).
- The sister track, the Undergraduate and REU Consortium (same date, same chairs' template), prints: "Paper Submission Deadline: September 20, 2026, 11:59 PM AoE" (https://bigdataieee.org/BigData2026/undergraduate-reu-consortium/). That is a reasonable indication the symposium also means end-of-day AoE, but it is **not stated** for the symposium.
- The CyberChair SP19 submission page itself still says "Submission deadline: to be announced soon." (https://wi-lab.com/cyberchair/2026/bigdata26/scripts/submit.php?subarea=SP19&undisplay_detail=1&wh=/cyberchair/2026/bigdata26/scripts/ws_submit.php), so no server-side cutoff time is published.
- **Extension: none found.** Neither the symposium page, the two co-chairs' LinkedIn posts, nor a web search for "High School Symposium" + "extended" shows any extension as of 19 Sept 2026. Both LinkedIn posts (~3 months old) repeat "Paper Submission Deadline: September 20, 2026" with no time zone; the LinkedIn posts give "Symposium Date: TBD, during Dec. 14–17, 2026" whereas the site now says December 17.
- Main-conference deadline (Aug 21, 2026) is irrelevant to the symposium; the main Important Dates page also prints no time zone (https://bigdataieee.org/BigData2026/important-dates/).

## 2. Page limit and references

Symposium page, verbatim:

> High school student research papers should not exceed 5 pages, including all figures, tables, and references.

CyberChair SP19 page, verbatim:

> Papers should be up to 5 pages (references included), in the IEEE 2-column format.

So: **5 pages, references count.** (Main conference: 10 pages incl. references, "No appendix is allowed." Camera-ready page says extra pages can be bought at "US$100 per page", up to two, for main/workshop papers; not stated whether that applies to the symposium.)

## 3. Format / template

Symposium page, verbatim:

> Submissions must adhere to the IEEE Computer Society Proceedings Manuscript Formatting Guidelines (see link to "formatting instructions" below: https://www.ieee.org/conferences/publishing/templates.html).
> Please highlight whether the first author is a high school student in the author affiliation of your submitted paper.

CyberChair: "in the IEEE 2-column format". Camera-ready page (https://wi-lab.com/cyberchair/2026/bigdata26/scripts/BigData_2026_Camera_ready_instruction.php): "Your final papers MUST be formatted to IEEE Manuscript Templates for Conference Proceedings (https://www.ieee.org/conferences/publishing/templates.html)" and "8.5\" x 11\" x 2 (DOC, PDF)", page size "612.0 x 792.0 points (8.5\" x 11\")".

- The link is the generic IEEE "Manuscript Templates for Conference Proceedings" page, i.e. the standard IEEE conference template (US letter, two-column; LaTeX = IEEEtran in `conference` mode). There is **no BigData-specific template**.
- I could not fetch ieee.org/conferences/publishing/templates.html itself (bot-protected, HTTP 202 challenge); the identification of the template as IEEEtran conference mode is from the page's known content, not a fresh quote.

## 4. Submission system

CyberChair. Symposium page "How to Submit" → "Open Submission Portal":
https://wi-lab.com/cyberchair/2026/bigdata26/scripts/submit.php?subarea=SP19&undisplay_detail=1&wh=/cyberchair/2026/bigdata26/scripts/ws_submit.php
(subarea SP19 is labelled "High Scholol Symposium" [sic] in CyberChair; it lives under the "Special Sessions / Demo / Symposium" group at https://wi-lab.com/cyberchair/2026/bigdata26/index.php). Not EasyChair, not CMT.

## 5. Review type

Symposium page, verbatim:

> The review process is single-blind (reviewers anonymous; authors visible to reviewers).

So author names and affiliations **should appear**, and the affiliation should flag the first author as a high-school student (see item 3). Main CFP: "The conference adopts a single-blind review policy."

## 6. Eligibility

Symposium page, verbatim:

> The first author must be a high school student at the time of submission. Co-first authorship (equal contribution) is accepted; however, in the case of equal contribution, the first author must still be a high school student, while the equally-contributing co-author(s) may be either high school or middle school students.
> Each submission must have at least one student author, who should be the presenter if the paper is accepted.
> Co-authorship with faculty members or researchers is allowed, but the student must be the primary contributor to the work.

Kunpeng Liu's LinkedIn post: "High school students are eligible to submit as first authors. Faculty/researcher co-authorship is allowed, but the student must be the primary contributor and presenter if accepted."

So: not all authors need be high-school students; a university mentor may be a co-author (not first author).

## 7. Dual / concurrent submission rule

Symposium page, section "Publication Ethics and Dual Submission Policy", verbatim:

> We uphold the highest standards of academic integrity and ethical research conduct. All authors must ensure that their submissions fully comply with the following guidelines.
> Originality and Dual Submission: Submitted manuscripts must represent original work that has not been submitted or published elsewhere. Dual submission—submitting the same or substantially similar content to multiple venues concurrently—is strictly prohibited and constitutes a violation of publication ethics and integrity. Submissions that have been previously posted on arXiv (or other preprint servers) are allowed.
> Subsequent Journal Submission: If authors wish to submit an extended version of their published work to a journal after conference publication (e.g., IEEE journals), they must clearly disclose that a preliminary version has been published. Transparency with journal editors and reviewers is required. Any subsequent submission to another venue must include significant new contributions, such as expanded experiments, novel theoretical insights, or additional methodological developments. Minor revisions or incremental changes are not sufficient to qualify as a new work.
> Ethical Responsibility: Authors are responsible for maintaining ethical standards in all aspects of the publication process, including authorship, data integrity, and proper citation of prior work. Violations may lead to retraction, notification of the authors' institutions, and disqualification from future submissions.

- "Sister tracks": the rule says "multiple venues"; it does **not** mention workshops, special sessions or other tracks of the same conference explicitly, and no carve-out exists either. Read plainly, "the same or substantially similar content" to any other venue concurrently is prohibited, which would cover a BigData workshop or special session. The main CFP (https://bigdataieee.org/BigData2026/calls/papers/), workshop CFP and submission page contain **no** dual-submission wording at all; the symposium page is the only statement.
- arXiv posting is explicitly allowed.

## 8. Notification, camera-ready, registration, attendance

- Notification: October 9, 2026. Camera-ready: October 24, 2026. Symposium day: December 17, 2026 (site) / "TBD, during Dec. 14–17" (LinkedIn). "Camera-Ready Instructions: TBD" on the symposium page.
- Attendance, symposium page verbatim:

> In-Person Policy
> In-person attendance is required for all accepted papers. We strongly encourage the first author to present in person, as this is an important part of the symposium experience. If the first author is unable to attend due to exceptional circumstances, a parent/guardian or a co-author must be present to deliver the presentation on-site in Phoenix. Unfortunately, we are not able to accommodate fully virtual presentations at this time.
> Each accepted paper must have at least one author registered and present in person during the symposium day.

- Registration page (https://bigdataieee.org/BigData2026/attending/registration/), verbatim:

> At least one author per paper must register as an AUTHOR at the full Member/Non-Member registration rate (not the student member rate), regardless of whether they are a student.
> For the main conference, we allow remote participation to join the keynote speech session, but not for the main conference paper presentation session. ... But for workshop/special session, it is hybrid, the workshop/special session organizer allow remote presentation.

  (The symposium's own page overrides the hybrid allowance: no virtual presentations.)
- Camera-ready page STEP 7: "All authors have to register the conference first, and then, submit the copy of the registration receipt"; STEP 8 asks each paper to declare "In-person presentation" or not. PDF eXpress opens 2026-10-05.
- **Fee amounts: not found.** The cvent registration site (https://cvent.me/1ovnZb → https://web.cvent.com/event/ea01f8b2-6760-4c81-babc-4c44cc93aeb9/) renders the Fees page client-side; the only extractable text is "Registration Deadlines: Author: 25 November, 2026; Early Bird: 25 November, 2026". Dollar amounts are behind the registration flow. Expect the full (non-student) author rate.

## 9. Proceedings

Symposium page, verbatim:

> All papers accepted by this symposium will be included in the Workshop Proceedings published by the IEEE Computer Society Press, made available at the Conference

The words "IEEE Xplore" do not appear on the symposium page. The conference camera-ready instructions (which cover "main conference, workshops and posters") say the final PDF must be "IEEE Xplore-compatible" via PDF eXpress and require an IEEE electronic copyright form, which is the pipeline for Xplore indexing of the workshop proceedings. Whether the symposium papers are indexed in Xplore is **not stated explicitly**; the 2024 edition's workshop proceedings were.

## 10. Review criteria / "good submission" text

Symposium page, verbatim:

> Submitted papers should present novel ideas, methodologies, algorithms, or applications in the realm of data mining. Papers will be evaluated based on their technical quality, novelty, relevance, and clarity of presentation.

Scope, verbatim: "We invite submissions of original research papers from high school students on topics related to data mining, including but not limited to:" foundations/algorithms of data mining; ML/DL/statistical methods for big data; mining text, semi-structured, spatio-temporal, streaming, graph, web and multimedia data; systems, parallel/distributed/federated mining and privacy; modeling, visualization, personalization, recommendation; cyber-physical systems and time-evolving networks; "Data mining with large language models"; novel applications across sciences, finance, health, etc.

Awards: "Outstanding Paper Awards, Runner-Up Awards, and Rising Star Awards". Program agenda, parent panel and poster session are all "TBD".

## 11. Chairs and contacts

Symposium page "Program Co-Chairs":
- **Kunpeng Liu**, Assistant Professor, Clemson University — kunpenl@clemson.edu (from https://www.kunpengliu.com/, which lists "High School Symposium Co-Chair of IEEE BigData 2026", Feb 2026)
- **Huazheng Wang**, Assistant Professor, Oregon State University — huazheng.wang@oregonstate.edu (from https://engineering.oregonstate.edu/people/huazheng-wang)
- Symposium Q&A mailbox (the one the page asks you to use): **bigdatahss2026@clemson.edu**

Confirmed on the Organization Committee page (https://bigdataieee.org/BigData2026/organization/committee/): "High School Symposium Co-chairs: Kunpeng Liu, Clemson University; Huazheng Wang, Oregon State University".

## URLs checked

- https://bigdataieee.org/BigData2026/high-school-symposium/ (primary; all quotes above)
- https://bigdataieee.org/BigData2026/calls/papers/ (main CFP: 10 pp incl. refs, no appendix, single-blind, CyberChair, IEEE CS template; no dual-submission text)
- https://bigdataieee.org/BigData2026/important-dates/ (no time zones)
- https://bigdataieee.org/BigData2026/calls/submission/
- https://bigdataieee.org/BigData2026/calls/workshops/
- https://bigdataieee.org/BigData2026/attending/registration/
- https://bigdataieee.org/BigData2026/organization/committee/
- https://bigdataieee.org/BigData2026/undergraduate-reu-consortium/ (sister track, "11:59 PM AoE")
- https://bigdataieee.org/BigData2026/ (news: only Dec 2025 venue and Jan 2026 site-launch items)
- https://wi-lab.com/cyberchair/2026/bigdata26/index.php
- https://wi-lab.com/cyberchair/2026/bigdata26/scripts/submit.php?subarea=SP19&undisplay_detail=1&wh=/cyberchair/2026/bigdata26/scripts/ws_submit.php
- https://wi-lab.com/cyberchair/2026/bigdata26/scripts/BigData_2026_Camera_ready_instruction.php
- https://cvent.me/1ovnZb (fees not extractable)
- https://www.linkedin.com/posts/kunpeng-liu-aba1781a3_ieeebigdata2026-highschoolresearch-artificialintelligence-activity-7468472906755248128-ePgN
- https://www.linkedin.com/posts/huazheng-wang-28234599_ieee-bigdata-2026-high-school-symposium-activity-7468513033099784192-OfbB
- https://www.kunpengliu.com/ ; https://engineering.oregonstate.edu/people/huazheng-wang
- https://www.ieee.org/conferences/publishing/templates.html (could not be fetched: bot challenge)
- https://bigdataieee.org/BigData2025/high-school-symposium/ (404)
