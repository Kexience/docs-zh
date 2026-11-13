---
source_url: https://java.testcontainers.org/features/reuse/
source_hash: sha256:9423efd573c807d43e1fc495d98d93635eb5fcb3601b013280fad518c9e78b0f
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# 可复用容器（实验性）

> **Warning**
>
> 可复用容器仍然是一个实验性功能，其行为可能会发生变化。这些容器在所有测试结束后不会停止。

*Reusable* 功能会保持容器继续运行，后续使用相同容器配置的执行将复用它。要使用该功能，请通过调用 `start()` 方法手动启动容器，不要直接或间接（例如通过 `try-with-resources` 或 `JUnit integration`）调用 `stop()` 方法，并在每个环境中通过显式启用机制手动开启。要复用容器，容器配置**必须完全相同**。

> **Note**
>
> 可复用容器不适用于 CI 场景；作为实验性功能，并非所有 Testcontainers 功能都能完全正常工作（例如资源清理或网络）。

## 如何使用

- 启用 `Reusable Containers`
  - 通过环境变量 `TESTCONTAINERS_REUSE_ENABLE=true`
  - 通过用户属性文件 `~/.testcontainers.properties`，添加 `testcontainers.reuse.enable=true`
  - **不要**通过 classpath 属性文件启用，[参见此评论](https://github.com/testcontainers/testcontainers-java/issues/5364#issuecomment-1125907734)
- 定义一个容器，并使用 `withReuse(true)` 声明复用该容器

```java
GenericContainer container = new GenericContainer("redis:6-alpine")
    .withExposedPorts(6379)
    .withReuse(true)
```

- 使用 `container.start()` 手动启动容器

### 在 Testcontainers JDBC URL 中使用可复用容器

如果使用 [Testcontainers JDBC URL 支持](../../modules/databases/jdbc/index.md#database-containers-launched-via-jdbc-url-scheme)，URL **必须**遵循 `jdbc:tc:mysql:8.0.36:///databasename?TC_REUSABLE=true` 的模式。`TC_REUSABLE=true` 作为 JDBC URL 的参数进行设置。
