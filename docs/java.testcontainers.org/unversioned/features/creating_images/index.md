---
source_url: https://java.testcontainers.org/features/creating_images/
source_hash: sha256:46ce3a543bba293485c090e09fc165960d00771bc63554a1456e638064c8a559
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# 即时创建镜像

## 概览

在没有现成 Docker 镜像的情况下，Testcontainers 可以根据 Dockerfile 即时创建一个新的临时镜像。例如，当被测组件本身就是 Docker 镜像，或者需要针对特定测试定制已有的基础镜像时。

只需将配置好的 `ImageFromDockerfile` 实例作为构造参数传给 `GenericContainer`。Testcontainers 会执行 `docker build` 构建一个临时的容器镜像，并在创建容器时使用它。

## 来自字符串、文件或 classpath 资源的 Dockerfile

`ImageFromDockerfile` 接受任意文件、字符串或 classpath 资源，将它们作为构建上下文中的文件使用。其中至少有一个必须是 `Dockerfile`。

```java
GenericContainer container = new GenericContainer(
    new ImageFromDockerfile()
            .withFileFromString("folder/someFile.txt", "hello")
            .withFileFromClasspath("test.txt", "mappable-resource/test-resource.txt")
            .withFileFromClasspath("Dockerfile", "mappable-dockerfile/Dockerfile"))
```

以下方法可用于提供 `Dockerfile` 以及构建上下文中所需的其它文件：

- `withFileFromString(buildContextPath, content)`
- `withFileFromClasspath(buildContextPath, classpathPath)`
- `withFileFromPath(buildContextPath, filesystemPath)`
- `withFileFromFile(buildContextPath, filesystemFile)`

> **说明**
>
> 在较老版本的 Testcontainers（1.3.0 之前）中，必须显式声明 Docker 构建上下文里需要存在的每一个文件。现在可以用下面的写法替代：
>
> **将整个文件目录传入 Dockerfile 构建上下文**
>
> 其中 `RESOURCE_PATH` 是包含 `Dockerfile` 及其所引用文件的目录路径。这样做等价于在命令行执行 `docker build RESOURCE_PATH`。
>
> 若要模拟 `docker build .`，只需将 `RESOURCE_PATH` 同样设为 `.` 即可。

```java
new ImageFromDockerfile()
    .withFileFromPath(".", RESOURCE_PATH)),
```

## Dockerfile DSL

如果静态的 Dockerfile 不够用（例如你的测试需要覆盖大量变体，而这些变体最好通过编程方式生成），可以借助一套 DSL 在代码中定义 Dockerfile。例如：

```java
new GenericContainer(
        new ImageFromDockerfile()
                .withDockerfileFromBuilder(builder ->
                        builder
                                .from("alpine:3.17")
                                .run("apk add --update nginx")
                                .cmd("nginx", "-g", "daemon off;")
                                .build()))
                .withExposedPorts(80);
```

参见 `ParameterizedDockerfileContainerTest`，这是一个将其与 JUnit 参数化测试结合使用的最基本示例。

## 自动删除

测试 JVM 关闭时，临时容器镜像会被自动删除。如果不希望删除、需要镜像在多次测试之间保留，请向 `ImageFromDockerfile` 构造函数传入一个稳定的镜像名和 `false` 标志。

在测试之间保留镜像会利用 Docker 的镜像缓存来加速后续的测试运行。

默认情况下，无参构造函数会使用形如 `testcontainers/` + 随机字符串的镜像名：

- `public ImageFromDockerfile()`
- `public ImageFromDockerfile(String dockerImageName)`
- `public ImageFromDockerfile(String dockerImageName, boolean deleteOnExit)`

## 备选的 Dockerfile

通常 Docker 会自动从构建上下文根目录中找到的任意 `/Dockerfile` 构建镜像。若要覆盖这一行为，请使用 `.withDockerfilePath("./Name-Of-Other-Dockerfile")`。

## 构建参数

[构建参数](https://docs.docker.com/engine/reference/builder/#arg)可用于实现轻量的参数化。

要指定构建参数，请使用 `.withBuildArg("varname", "value")`，或使用 `.withBuildArgs(map)` 提供一个参数 `Map`。
