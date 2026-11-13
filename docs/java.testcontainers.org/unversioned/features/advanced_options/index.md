---
source_url: https://java.testcontainers.org/features/advanced_options/
source_hash: sha256:a38f96d03e6e7790e6ee194d17b8aca19193ba914601972ea9e0d37e9f31876c
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# 高级选项

## 容器标签

要向容器添加自定义标签，请使用 `withLabel`：

**添加单个标签**

```java
public GenericContainer containerWithLabel = new GenericContainer(DockerImageName.parse("alpine:3.17"))
    .withLabel("key", "value");
```

此外，还可以从 map 中一次性应用多个标签：

**添加多个标签**

```java
private Map<String, String> mapOfLabels = new HashMap<>();
// populate map, e.g. mapOfLabels.put("key1", "value1");

public GenericContainer containerWithMultipleLabels = new GenericContainer(DockerImageName.parse("alpine:3.17"))
    .withLabels(mapOfLabels);
```

## 镜像拉取策略

默认情况下，容器镜像从本地 Docker 镜像缓存中获取。这在针对特定版本运行时效果良好，但对于使用静态标签（即 'latest'）的镜像，可能会导致未能拉取到更新的版本。

可以指定镜像拉取策略，以在运行时决定镜像是否需要拉取：

**设置镜像拉取策略**

```java
GenericContainer<?> container = new GenericContainer<>(imageName)
    .withImagePullPolicy(PullPolicy.alwaysPull())
```

……或者提供一个函数：

**自定义镜像拉取策略**

```java
GenericContainer<?> container = new GenericContainer<>(imageName)
    .withImagePullPolicy(
        new AbstractImagePullPolicy() {
            @Override
            protected boolean shouldPullCached(DockerImageName imageName, ImageData localImageData) {
                return System.getenv("ALWAYS_PULL_IMAGE") != null;
            }
        }
    )
```

你也可以通过 `pull.policy` 配置 Testcontainers 使用你的自定义实现

**src/test/resources/testcontainers.properties**

```text
pull.policy=com.mycompany.testcontainers.ExampleImagePullPolicy
```

你也可以使用内置实现来总是拉取镜像

**src/test/resources/testcontainers.properties**

```text
pull.policy=org.testcontainers.images.AlwaysPullPolicy
```

更多信息请参见[配置机制文档](../configuration/index.md)。

## 自定义容器

### 使用 docker-java

可以直接使用 [`docker-java`](https://github.com/docker-java/docker-java) API 在创建之前自定义容器。当需要使用 Testcontainers API 未暴露的高级 Docker 特性时，这非常有用。你通过 `withCreateContainerCmdModifier` 所做的任何自定义，都会在 Testcontainers 创建的容器定义*之上*生效，但仍在容器真正创建之前。

例如，可以用它来更改容器主机名：

**使用修改器更改主机名**

```java
@Rule
public GenericContainer theCache = new GenericContainer<>(DockerImageName.parse("redis:6-alpine"))
    .withCreateContainerCmdModifier(cmd -> cmd.withHostName("the-cache"));
```

……或者修改容器内存（如果看起来没有生效，请参见[这篇文章](https://fabiokung.com/2014/03/13/memory-inside-linux-containers/)）：

**使用修改器更改内存限制**

```java
private long memoryInBytes = 32l * 1024l * 1024l;

private long memorySwapInBytes = 64l * 1024l * 1024l;

@Rule
public GenericContainer memoryLimitedRedis = new GenericContainer<>(DockerImageName.parse("redis:6-alpine"))
    .withCreateContainerCmdModifier(cmd -> {
        cmd.getHostConfig()
            .withMemory(memoryInBytes)
            .withMemorySwap(memorySwapInBytes);
    });
```

> **注意**
>
> 建议谨慎使用该功能；如果选择使用，请留意 `docker-java` API 的变化。它通常相当稳定。

关于可以实现哪些功能，请查阅 [`docker-java CreateContainerCmd` 源代码](https://github.com/docker-java/docker-java/blob/3.2.1/docker-java-api/src/main/java/com/github/dockerjava/api/command/CreateContainerCmd.java)。

### 使用 CreateContainerCmdModifier

Testcontainers 提供了 `CreateContainerCmdModifier`，可以通过服务提供者接口（SPI）机制来自定义 [`docker-java CreateContainerCmd`](https://github.com/docker-java/docker-java/blob/3.2.1/docker-java-api/src/main/java/com/github/dockerjava/api/command/CreateContainerCmd.java)。

**CreateContainerCmd 示例实现**

```java
package org.testcontainers.custom;

import com.github.dockerjava.api.command.CreateContainerCmd;
import org.testcontainers.core.CreateContainerCmdModifier;

import java.util.HashMap;
import java.util.Map;

public class TestCreateContainerCmdModifier implements CreateContainerCmdModifier {

    @Override
    public CreateContainerCmd modify(CreateContainerCmd createContainerCmd) {
        Map<String, String> labels = new HashMap<>();
        labels.put("project", "testcontainers-java");
        labels.put("scope", "global");
        createContainerCmd.getLabels().putAll(labels);
        return createContainerCmd;
    }
}
```

上述实现应注册到 `META-INF/services/org.testcontainers.core.CreateContainerCmdModifier` 文件中。

> **警告**
>
> `CreateContainerCmdModifier` 的实现会作用于 Testcontainers 创建的所有容器。

## 并行启动容器

通常在使用多个容器时，容器是按顺序启动的。使用 `Startables.deepStart(container1, container2, ...).join()` 可以并行启动所有容器。这有助于减少容器启动开销带来的影响。
