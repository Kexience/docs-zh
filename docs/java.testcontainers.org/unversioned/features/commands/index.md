---
source_url: https://java.testcontainers.org/features/commands/
source_hash: sha256:0d48fbeb29d5ce9b63f6519d19eb23f3eec838a3600b348c742bf8e06a7863bb
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# 执行命令

## 容器启动命令

默认情况下，容器会执行镜像的 Dockerfile 中所指定的命令。如需覆盖该行为并指定其他命令，请使用 `withCommand`。例如：

**指定启动命令**

```java
public GenericContainer redisWithCustomPort = new GenericContainer(DockerImageName.parse("redis:6-alpine"))
    .withCommand("redis-server --port 7777")
```

## 执行命令

你的测试可以在运行中的容器内执行命令，类似于 `docker exec` 调用：

**在运行中的容器内执行命令**

```java
container.execInContainer("touch", "/somefile.txt");
```

这对于带有命令行管理工具的软件会很有用。你还可以获取命令的输出（stdout/stderr）和退出码——例如：

**在运行中的容器内执行命令并读取结果**

```java
Container.ExecResult lsResult = container.execInContainer("ls", "-al", "/");
String stdout = lsResult.getStdout();
int exitCode = lsResult.getExitCode();
assertThat(stdout).contains("somefile.txt");
assertThat(exitCode).isZero();
```

## 环境变量

要向容器添加环境变量，请使用 `withEnv`：

```
new GenericContainer(...)
        .withEnv("API_TOKEN", "foo")
```
