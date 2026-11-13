---
source_url: https://java.testcontainers.org/features/jib/
source_hash: sha256:18d096b44050d62d745b9f8d0a37203618feeee82ea95f0370db705082d2c578
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# 使用 Jib

[Jib](https://github.com/GoogleContainerTools/jib/tree/master/jib-core) 是一个用于构建 Docker 镜像的库。你可以把它作为 Testcontainers 默认 `DockerfileBuilder` 的替代方案。

**使用 JibImage 的 GenericContainer**

```java
GenericContainer<?> busybox = new GenericContainer<>(
    new JibImage(
        "busybox:1.35",
        jibContainerBuilder -> {
            return jibContainerBuilder.setEntrypoint("echo", "Hello World");
        }
    )
)
    .withStartupCheckStrategy(new OneShotStartupCheckStrategy().withTimeout(Duration.ofSeconds(3)))
```

> **Hint**
>
> Testcontainers 库的 JAR 不会自动为你的项目添加 `jib-core` JAR。所需的最低版本是 `com.google.cloud.tools:jib-core:0.22.0`。
