---
source_url: https://java.testcontainers.org/supported_docker_environment/continuous_integration/concourse_ci/
source_hash: sha256:b69b096bb399991fc183505e09ec75154f800780279ab1b5ccaabc4613d93dda
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Concourse CI

这是一个在 [Concourse CI](https://concourse-ci.org/) 上运行 Testcontainers 测试的示例。

一个可能的 `pipeline.yml` 配置如下所示：

```yaml
resources:
- name: repo
  type: git
  source:
    uri: https://github.com/testcontainers/testcontainers-java-repro.git

jobs:
- name: testcontainers-job
  plan:
  # Add a get step referencing the resource
  - get: repo
  - task: testcontainers-task
    privileged: true
    config:
      platform: linux
      image_resource:
        type: docker-image
        source:
          repository: amidos/dcind
          tag: 2.1.0
      inputs:
      - name: repo
      run:
        path: /bin/sh
        args: 
          - -c
          - |
            source /docker-lib.sh
            start_docker

            cd repo
            docker run -it --rm -v "$PWD:$PWD" -w "$PWD" -v /var/run/docker.sock:/var/run/docker.sock eclipse-temurin:17.0.5_8-jdk-alpine ./mvnw clean package
```

```bash
fly -t tutorial set-pipeline -p testcontainers-pipeline -c pipeline.yml
fly -t tutorial unpause-pipeline -p testcontainers-pipeline
fly -t tutorial trigger-job --job testcontainers-pipeline/testcontainers-job --watch
```
