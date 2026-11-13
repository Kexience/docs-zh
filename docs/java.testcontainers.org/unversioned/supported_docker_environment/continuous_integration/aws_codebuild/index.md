---
source_url: https://java.testcontainers.org/supported_docker_environment/continuous_integration/aws_codebuild/
source_hash: sha256:f1693c4181c764d3cb0c5ee3cd64b9498f2ace686ef0c89373e65956413a4ff3
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# AWS CodeBuild

要在 AWS CodeBuild 中启用对 Docker 的访问，请转到 `Privileged` 部分并勾选
 `Enable this flag if you want to build Docker images or want your builds to get elevated privileges`。

以下是一个 `buildspec.yml` 配置示例：

```yaml
version: 0.2

phases:
  install:
    runtime-versions:
      java: corretto17
  build:
    commands:
      - ./mvnw test
```
