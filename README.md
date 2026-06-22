# CSFN Skills

蔡氏福宁 WorkBuddy Skill 仓库，供团队成员安装和同步更新。

## 已有 Skill

| Skill | 说明 |
|| 循环工程 | 2026年全新AI工程范式——设计闭环让AI自主迭代达标 |
-------|------|
| 蔡氏福宁文案审核 | 文案合规审核，支持广告法检查、企标标签对照 |

---

## 安装（首次）

**方式一：让 AI 帮你装（推荐）**

把这段话发给你的 WorkBuddy：

```
请帮我把蔡氏福宁文案审核 skill 安装到 ~/.workbuddy/skills/ 目录。
GitHub 仓库：https://github.com/Zankusama/CSFN-skills
```

**方式二：手动安装**

```bash
cd ~/.workbuddy/skills/
git clone https://github.com/Zankusama/CSFN-skills.git temp
cp -r temp/蔡氏福宁文案审核 ./
rm -rf temp
```

安装完成后重启 WorkBuddy，输入「审文案」测试是否生效。

---

## 更新（以后每次锴哥改了 skill）

**方式一：让 AI 帮你更新（推荐）**

```
请帮我同步蔡氏福宁文案审核 skill 的最新版本。
进入 ~/.workbuddy/skills/蔡氏福宁文案审核，
执行 git pull 同步（如果之前是用 git clone 装的）。
如果不是，请从 https://github.com/Zankusama/CSFN-skills 重新安装。
```

**方式二：手动更新**

```bash
cd ~/.workbuddy/skills/蔡氏福宁文案审核
git pull
```

---

## 注意事项

- 仓库为公开状态，无需 GitHub 账号即可 clone（方式二）
- 让 AI 帮忙装（方式一）需要你的 WorkBuddy 能访问 GitHub
- 安装或更新后记得重启 WorkBuddy
