---
name: untangle
disable-model-invocation: true
description: "第三者介入釐清: user 覺得與 main agent 的對話陷入混亂時呼叫, 由兩個不同 model 的 subagent 以旁觀者角度找出混亂源頭, 一語點破, 再由 main agent 彙整回覆."
---

# 第三者介入釐清

 user 呼叫這個 skill, 代表對話已經讓 user 混亂. main agent 身在局中, 很可能就是混亂的一部分, 所以診斷交給局外的兩個 subagents, main agent 只負責「忠實轉達」與「彙整」.

## 流程

### 1. 整理案卷 (不加詮釋)

把目前對話整理成一份案卷, 寫進暫存檔:

- ** user 的每則訊息: 逐字**.
- **main agent 的每則回覆: 逐字**; 過長時可節錄, 但保留原句, 不改寫成摘要.
- 對話中做過的動作 (改了哪些檔、跑了什麼指令、結果如何) 依時間序列出事實.

禁止寫入案卷:

- main agent 對混亂成因的猜測、自我辯護、或「我認為 user 其實想要...」.
- 會引導結論的形容詞或排序 (例: 「關鍵是第 3 則」).

案卷的目的是讓 subagent 看到原始現場, 不是看到 main agent 眼中的現場.

### 2. 啟動兩個 subagent, 然後等待

用可用的 subagent 機制, **平行**啟動兩個全新的 subagent (不繼承 main agent 的推理脈絡), 依 main agent 所在的環境指定 model, 兩者收到**完全相同**的 prompt (見下方「subagent prompt」).

| 環境 | model A | model B |
|---|---|---|
| Claude | `sonnet` | `opus` |
| Codex | `GPT-6.1-Sol` | `GPT-6.1 Terra` |

- 上表的 model 名稱是寫死的. 若查無該 model 或指定後無法啟動, 則自行替換成其他 model, 繼續任務, 並通知 user: 列出無法使用的 model 名稱, 說明 untangle skill 需要更新 model 對照表.

啟動之後到兩個 subagent 都回覆以前, main agent **不輸出任何文字給 user **, 不預告、不先給自己的看法.

### 3. 彙整回覆

兩個 subagent 都回覆後, 依下列格式回覆 user , 不加其他段落:

```
# main 摘要
(綜合兩份說明的摘要, 200 字以內. 先講混亂的源頭是什麼, 再講接下來怎麼走)

# {model A} 的說明
(model A subagent 的回覆, 原文照登)

# {model B} 的說明
(model B subagent 的回覆, 原文照登)

# main 的說明
(說明額外能夠讓 user 回歸到核心問題的補充細節)
```

- model A 的說明 / model B 的說明
  - 照登, 不潤飾、不刪減
- main agent 的說明
  - 不得為自己辯護而淡化 subagent 指出的問題
  - 不需要做任何當時搞混的因果進行描述
  - 不需要針對 2 subagents 意見不同之處進行比較及陳述
- 回覆完, 本 skill 結束. 下一則 user 訊息恢復正常對話

## subagent prompt

把 `{...}` 換成實際內容, 其餘照抄:

```
你是旁觀者. 一位 user 和一個 AI agent (下稱 main agent) 的對話讓 user 感到混亂.
你沒有參與這段對話, 你的任務是從第三者角度找出: user 為什麼被搞混.

案卷 (完整對話與動作紀錄): {案卷檔案的絕對路徑}
 user 自己描述的卡點: {逐字引用}

先讀 {principle-materiality 的 SKILL.md}, 你的回覆必須遵守它.

要求:
- 第一句話就點出混亂的源頭, 一句講完. 要讓 main agent 讀完立刻意識到問題在哪.
- 接著用最少的句子佐證: 引用案卷中造成混亂的具體語句或轉折點.
- 最後給一個能讓對話回到正軌的下一步 (例: 先確認某個詞的定義、先回答被跳過的問題).
- 只做診斷, 不替 user 解決原本的技術問題.
- 不要把案卷重述一遍, 不要列出沒有佐證的可能原因.
- 全文不超過 300 字.
```
