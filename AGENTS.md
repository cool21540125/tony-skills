# AGENTS.md

給修改這個 repo 的 agent 與貢獻者的規則.

## 結構

- 每個 skill 是 `skills/<name>/`, 至少包含 `SKILL.md`; 輔助檔放 `references/`, `scripts/`, `assets/`.
- 格式遵循 [Agent Skills spec](https://agentskills.io/specification):
  - `name`: 小寫英數與 `-`, ≤ 64 字元, 必須與資料夾同名.
  - `description`: ≤ 1024 字元, 寫清楚「做什麼」與「何時觸發 / 何時不觸發」. 一律用雙引號包住, 否則內文的 `: ` 會讓嚴格的 YAML parser 解析失敗 (skills.sh 會直接略過該 skill).
- 驗證: `npx skills@latest add . --list` 要能列出所有 skill.
- 每個 skill 附 `agents/openai.yaml` (Codex 的 UI 顯示設定, 其他 agent 會忽略). 欄位規則見 [openai/skills 的 openai_yaml.md](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/references/openai_yaml.md):
  - 字串值一律加雙引號.
  - `short_description` 25-64 字元.
  - `default_prompt` 必須以 `$skill-name` 提到該 skill.

## 寫作規則

- **不綁定 LLM**: SKILL.md 正文不寫特定 agent 的工具名 (例: `WebSearch`, `Bash`), 改寫成能力描述 (例: 「用可用的網路搜尋工具」).
- 語言: 中文為主, 專有名詞保留原文.
- 標點: 用半形 `, ` `. ` `: `, 不用全形 `，` `。` `：`.
- `README.md` 不列出個別 skill, 新增 skill 不需要改 README.
