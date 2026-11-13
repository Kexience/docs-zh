---
source_url: https://java.testcontainers.org/supported_docker_environment/continuous_integration/bitbucket_pipelines/
source_hash: sha256:54722e74daba171117812c27997c5c90610581eb7c44681f13564719f56cb025
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Bitbucket Pipelines

要在 Bitbucket Pipelines 中启用对 Docker 的访问，你需要在步骤中将 `docker` 添加为服务。

此外，需要关闭 Ryuk，因为 Bitbucket Pipelines 不允许启动特权容器（参见[禁用 Ryuk](../../../features/configuration/index.md#disabling-ryuk)）。这可以通过在 Bitbucket 的项目设置中设置仓库变量，或在步骤中显式导出该变量来完成。

在某些情况下，需要增加 Docker 可用的内存。

以下是一个 Bitbucket Pipeline 配置示例，它会检出项目并运行 maven：

```yml
image: maven:3.6.1

pipelines:
  default:
    - step:
        script:
          - export TESTCONTAINERS_RYUK_DISABLED=true
          - mvn clean install
        services:
          - docker
definitions:
  services:
    docker:
      memory: 2048
```
