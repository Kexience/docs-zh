---
source_url: https://java.testcontainers.org/features/files/
source_hash: sha256:571559ad936c300ca1664a2ba3e4a05dd2a3f0c2cd39b211aa604ab9095c5543
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# 文件与卷

## 复制文件

文件可以在启动前复制到容器中，也可以在容器启动后从容器中复制出来。

> **注意**
>
> 这是跨 Docker 环境实现可移植性的推荐做法。

### 启动前复制文件到容器

**使用 MountableFile 复制文件**

```java
GenericContainer<?> container = new GenericContainer<>(TestImages.TINY_IMAGE)
    .withCommand("sleep", "3000")
    .withCopyFileToContainer(
        MountableFile.forClasspathResource("/mappable-resource/"),
        directoryInContainer
    )
```

使用 `Transferable` 时，文件内容会被放置到指定位置。

**使用 Transferable 复制文件**

```java
GenericContainer<?> container = new GenericContainer<>(TestImages.TINY_IMAGE)
    .withStartupCheckStrategy(new NoopStartupCheckStrategy())
    .withCopyToContainer(Transferable.of("test"), "/tmp/test")
    .waitingFor(new WaitForExitedState(state -> state.getExitCodeLong() > 0))
    .withCommand("sh", "-c", "grep -q test /tmp/test && exit 100")
```

也可以设置文件权限模式。

**使用带文件权限模式的 Transferable 复制文件**

```java
GenericContainer<?> container = new GenericContainer<>(TestImages.TINY_IMAGE)
    .withStartupCheckStrategy(new NoopStartupCheckStrategy())
    .withCopyToContainer(Transferable.of("test", 0777), "/tmp/test")
    .waitingFor(new WaitForExitedState(state -> state.getExitCodeLong() > 0))
    .withCommand("sh", "-c", "ls -ll /tmp | grep '\\-rwxrwxrwx\\|test' && exit 100")
```

### 从运行中的容器复制文件

**从容器复制文件**

```java
container.copyFileFromContainer(directoryInContainer + fileName, destinationOnHost);
```
