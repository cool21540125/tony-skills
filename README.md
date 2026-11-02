# tony-skills

Tony 的 agent skills 集合. 遵循 [Agent Skills](https://agentskills.io/specification) 開放格式, 不綁定特定 LLM 或 agent 工具.

所有 skill 都在 [`skills/`](skills/) 底下, 一個資料夾一個 skill.

## 安裝

任何支援 Agent Skills 的 agent (Claude Code, Cursor, Codex, OpenCode, Gemini CLI 等) 都可以用 [skills.sh](https://skills.sh) 安裝:

```bash
npx skills@latest add cool21540125/tony-skills
```

安裝時可以挑選要裝哪些 skill.

更新:

```bash
npx skills@latest update <skill-name>...
```

也可以手動複製 `skills/<name>/` 整個資料夾到你的 agent 的 skills 目錄.

## License

[MIT](LICENSE)
