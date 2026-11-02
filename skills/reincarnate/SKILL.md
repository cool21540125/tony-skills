---
name: reincarnate
description: "Produce a self-contained continuation prompt for a new session after a long or disrupted discussion, preserving decisions, environment changes, and outstanding work."
---

# Reincarnate

Use this skill when the current session should be replaced after a lengthy or
troubled discussion, especially when context is unwieldy or the environment,
memory, or session state has changed. Its only deliverable is a prompt the user
can paste into a new session. Do not make changes, run new investigations, or
continue the original task unless the user separately requests that work.

## Build the continuation prompt

Review the current conversation and only the already available evidence needed
to make the handoff accurate. Write the result as a direct instruction to the
next model, in the user's preferred language and style.

Make the prompt self-contained and concise. Include, when applicable:

1. The user's goal and scope, including explicit constraints and permissions.
2. Confirmed decisions, facts, and relevant file paths or commands already
   checked. Mark assumptions and unverified claims clearly.
3. Environment changes since the discussion began, such as refreshed variables,
   memory updates, changed files, or a required new session.
4. Work completed, work deliberately not performed, and the exact outstanding
   task or question.
5. The recommended first action for the next model, plus any verification that
   must happen before it acts.

Preserve critical error messages or command output only when they are needed to
diagnose or continue the task. Never include secrets, credentials, tokens,
private personal data, or large raw logs. Do not invent missing facts.

## Deliver

Start with a brief statement that the prompt is ready. Then put the complete
copy-ready prompt in one fenced code block. Do not add an additional summary
outside that block, so the user can copy it without reconstruction.
