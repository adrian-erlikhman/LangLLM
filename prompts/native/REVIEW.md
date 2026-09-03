# Native prompt review

Automated reviewer: `qwen/qwen3.7-plus` (not a subject, not the writer). It extracts topic / stance / sub-claims from each prompt blind, then matches them to the schema. Flags: `content` (topic, stance or sub-claim mismatch, or an extra claim), `no_prose_only_instruction`, `no_length`, `non_native` (quality < 4/5), `mentions_language`.

Fix flagged prompts by editing `{lang}.json` and re-running `python -m langllm.review --lang {lang}`. A fluent human reader may additionally set `human_checked: true` per prompt; that column is optional.

| lang | auto pass | flagged | human checked | notes |
|---|---|---|---|---|
| en | 12/12 | — | no | |
| es | 12/12 | — | no | |
| zh | 12/12 | — | no | |
| ru | 12/12 | — | no | |
| ja | 12/12 | — | no | |
| tr | 12/12 | — | no | |
| hi | 12/12 | — | no | |
