---
source_url: https://java.testcontainers.org/supported_docker_environment/continuous_integration/travis/
source_hash: sha256:e9d19990ae2b4a9543648c7dd364b475daeb67ace8dcdcda81343a08ddf65f0b
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# TravisCI

要在 TravisCI 上运行 Testcontainers，需要安装 docker。以下配置是所需的最小配置。

```yaml
language: java
jdk:
- openjdk8

services:
- docker

script: ./mvnw verify
```
