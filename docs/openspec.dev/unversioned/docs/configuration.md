---
source_url: https://openspec.dev/docs/configuration
source_hash: sha256:e0b003d631b0f4a351a99064154a676387049c76ca45665a90c188f4cfe86342
translated_at: 2026-11-13T09:48:42+08:00
translation_version: 1
---

# 配置总览

| 文件 | 位置 | 控制什么 |
| --- | --- | --- |
| [项目配置（config.yaml）](./configuration/config-yaml.md) | `openspec/config.yaml` | 该项目用于规划的模式、上下文和规则 |
| [变更元数据（.openspec.yaml）](./configuration/change-metadata.md) | `openspec/changes/<name>/.openspec.yaml` | 单个变更的工作流模式、目标、范围和规格例外 |
| [CLI 设置（config.json）](./configuration/config-json.md) | `~/.config/openspec/config.json`（Windows 不同） | openspec CLI 在你机器上的行为方式 |
| 环境变量 | 你的 shell 或 CI 环境 | 遥测退出（opt-out），以及配置目录和数据目录的位置 |
| 存储库 | `~/.local/share/openspec/stores/`（Windows 不同） | 支撑多仓库存储库的注册表和元数据 |
