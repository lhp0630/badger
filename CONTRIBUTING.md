# 贡献代码规范

## 核心规则

1. 禁止直接向 `main`/`master` 提交，必须从 `main`/`master` 切功能分支
2. 未获用户许可，禁止 commit、push、创建 PR
3. 禁止 `git push --force` 到 `main`/`master`
4. 变更范围不明确时，先向用户确认

## 分支命名

```
feat/<简短描述>    # 新功能
fix/<简短描述>     # Bug 修复
docs/<简短描述>    # 文档变更
```

## Commit 规范

```
<type>(<scope>): <subject>

<body>

<footer>
```

- **type**
  - feat | fix | docs | style | refactor | tweak | perf | test | chore | ci | revert

- **subject 规则**
  - 祈使语气，不加句号，不超过 50 字符
  - 原子提交：每次仅解决一个逻辑变更

- **breaking change**
  - type 后加 `!`，如 `feat!:`

- **docs 类型约束**
  - 不得混入代码逻辑变更

## PR 流程

```bash
# 1. 推送分支
git push -u origin HEAD

# 2. 创建 PR
gh pr create --title "<标题>" --body "$(cat <<'EOF'
## Summary
- <变更要点>

## Test plan
- [ ] <验证项>
EOF
)"
```

## 违规处理

1. 暂停当前操作
2. 报告违规规则
3. 给出修正方案
4. 等待用户确认