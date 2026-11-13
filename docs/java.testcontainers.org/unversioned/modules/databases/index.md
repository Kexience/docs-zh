---
source_url: https://java.testcontainers.org/modules/databases/
source_hash: sha256:be204b63a8951a1c87aae18afbb29497c691c2466fb29dde68d72783b7aa0cec
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# 数据库容器

## 概览

在以下情况下，你可能希望使用 Testcontainers 的数据库支持：

- **替代 H2 数据库，用于依赖 H2 无法模拟的数据库特性的 DAO 单元测试。** Testcontainers 的性能不如 H2，但由于它在容器中运行真实的数据库，因此能够带来 100% 的数据库兼容性。
- **替代在本地机器或虚拟机中运行的数据库**，用于需要数据库存在的 DAO 单元测试或端到端集成测试。在这种场景下，Testcontainers 的优势在于数据库每次都能以已知状态启动，不会在不同测试运行之间或开发者本地机器上留下污染。

> **Note**
>
> 当然，尽可能减少访问数据库的测试数量仍然很重要，并且应在调用栈更上层的组件中善用 mock。

有关如何在类 SQL 数据库中使用 Testcontainers 的信息，请参阅 [JDBC](./jdbc/index.md) 和 [R2DBC](./r2dbc/index.md)。
