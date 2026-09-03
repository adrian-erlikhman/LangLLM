# Native prompt review

Automated reviewer: `qwen/qwen3.7-plus` (not a subject, not the writer). It extracts topic / stance / sub-claims from each prompt blind, then matches them to the schema. Flags: `content` (topic, stance or sub-claim mismatch, or an extra claim), `no_prose_only_instruction`, `no_length`, `non_native` (quality < 4/5), `mentions_language`.

Fix flagged prompts by editing `{lang}.json` and re-running `python -m langllm.review --lang {lang}`. A fluent human reader may additionally set `human_checked: true` per prompt; that column is optional.

| lang | auto pass | flagged | human checked | notes |
|---|---|---|---|---|
| en | 4/12 | P02(content,no_length) P03(no_length) P06(content) P08(no_length) P09(no_length) P10(no_length) P11(no_length) P12(no_length) | no | |
| es | 9/12 | P06(content) P09(content) P12(content) | no | |
| zh | 6/12 | P01(content) P02(content) P04(content) P07(content) P08(content) P12(content) | no | |
| ru | 12/12 | — | no | |
| ja | 8/12 | P03(content) P05(content) P08(content) P11(content) | no | |
| tr | 12/12 | — | no | |
| hi | 10/12 | P07(no_prose_only_instruction) P12(content) | no | |
