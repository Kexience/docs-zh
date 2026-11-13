---
source_url: https://java.testcontainers.org/supported_docker_environment/continuous_integration/circle_ci/
source_hash: sha256:f7548b01658d211afddbe60c92f63cb6f4d359f85aae935c0a3e501bb165767e
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# CircleCI

你的 CircleCI 配置应使用专用 VM 才能让 Testcontainers 正常工作。你可以通过在 `.circleci/config.yml` 中将执行器类型指定为 `machine`（而不是默认的 `docker` 执行器）来实现这一点（更多信息请参见[选择执行器类型](https://circleci.com/docs/executor-intro)）。

以下是一个 CircleCI 配置示例，它会检出项目并运行 Maven：

```yml
jobs:
  build:
    # Check https://circleci.com/docs/executor-intro#linux-vm for more details
    machine: true
    steps:
      - checkout
      - run: mvn -B clean install
```

你可以在[这篇文章](https://www.atomicjar.com/2022/12/testcontainers-with-circleci/)中了解有关将 Testcontainers 与 CircleCI 结合使用的最佳实践的更多信息。
