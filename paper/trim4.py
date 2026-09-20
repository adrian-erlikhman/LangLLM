from pathlib import Path
p = Path(__file__).with_name("main.tex"); s = p.read_text(encoding="utf-8")
R = [
(r"\label{tab:main}" + "\n" + r"\centering" + "\n" + r"\small", r"\label{tab:main}" + "\n" + r"\centering" + "\n" + r"\footnotesize"),
(r"\label{tab:trans}" + "\n" + r"\centering" + "\n" + r"\small", r"\label{tab:trans}" + "\n" + r"\centering" + "\n" + r"\footnotesize"),
(r"\textbf{RQ4.} After z-scoring within each language, the mean pairwise distance between the five model centroids, the silhouette of model labels and the between/within scatter ratio, with stratified bootstrap intervals and Spearman's $\rho$ against rank.", r"\textbf{RQ4.} After z-scoring within each language, the mean pairwise distance between model centroids, the silhouette of model labels and the between/within scatter ratio, with stratified bootstrap intervals and Spearman's $\rho$ against rank."),
(r"The nested selection curve (Fig.~\ref{fig:curve}) shows five features already reach macro-F1 \CurveKfiveMin{}--\CurveKfiveMax{} and ten come within \CurveKtenWithin{} points of all \NFeatures{} in every language; the pooled ranking is \PooledTopFive{}. No feature group is necessary:", r"The nested selection curve (Fig.~\ref{fig:curve}) shows five features already reach macro-F1 \CurveKfiveMin{}--\CurveKfiveMax{} and ten come within \CurveKtenWithin{} points of all \NFeatures{} in every language. No feature group is necessary:"),
(r"The point estimate is under one accuracy point per step, and the ordering is not monotone: Japanese (rank 5) matches English, and Hindi (rank 7) is more identifiable than Spanish and Turkish.", r"The point estimate is under one accuracy point per step, and the ordering is not monotone: Japanese (rank 5) matches English and Hindi (rank 7) beats Spanish and Turkish."),
(r"Attribution on translated text alone runs \TrAllMin{}--\TrAllMax{} (Table~\ref{tab:trans}), every interval excluding chance; translating costs about nine points relative to the English originals (\LRen{}), roughly what moving from English to a native lower-resource language costs.", r"Attribution on translated text alone runs \TrAllMin{}--\TrAllMax{} (Table~\ref{tab:trans}), every interval excluding chance; translating costs about nine points relative to the English originals (\LRen{}), about what moving to a native lower-resource language costs."),
]
for a, b in R:
    assert a in s, "NOT FOUND: " + a[:70]
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8"); print("trim4 applied")
