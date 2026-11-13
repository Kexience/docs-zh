---
source_url: https://java.testcontainers.org/features/image_name_substitution/
source_hash: sha256:56283691b1cc32103a6b260d9ff59cc9769cf0a9c9fa2673307a9c7cb2a9258c
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# 镜像名替换

Testcontainers 支持自动替换 Docker 镜像名。

这使你可以把测试代码中指定的镜像名替换为替代名称——例如，把依赖的 Docker Hub 镜像名替换为托管在私有镜像仓库中的镜像名。

这样做有助于避免 [Docker Hub 速率限制](../../supported_docker_environment/image_registry_rate_limiting/index.md)，一些公司出于策略原因也会更倾向于这种做法。

本页介绍四种镜像名替换方式：

- [手动替换](#manual-substitution) —— 不依赖自动化机制
- 使用 Image Name Substitutor：
  - [开发一个自定义函数，在运行时动态转换镜像名](#developing-a-custom-function-for-transforming-image-names-on-the-fly)
  - [在配置中逐个覆盖镜像名](#overriding-image-names-individually-in-configuration)

这里假定你已经搭建好了私有镜像仓库，并托管了[构建所需的全部 Docker 镜像](../../supported_docker_environment/image_registry_rate_limiting/index.md#which-images-are-used-by-testcontainers)。

## 手动替换

在以下情况下可以考虑这种方式：

- 你只使用少量镜像，修改代码并不费力
- 你所在组织的所有开发者和 CI 机器都能访问同一个镜像仓库服务器
- 你还会使用某种自动化机制来替换 [Testcontainers 自身所需的镜像](../../supported_docker_environment/image_registry_rate_limiting/index.md#which-images-are-used-by-testcontainers)

这种方式只需要手动修改测试代码。例如，把：

例如，你的测试可能使用来自 Docker Hub 的 `mysql` 容器镜像：

**直接使用 Docker Hub 镜像名**

```java
// Referring directly to an image on Docker Hub (mysql:8.0.36)
final MySQLContainer<?> mysql = new MySQLContainer<>(
    DockerImageName.parse("mysql:8.0.36")
)
// start the container and use it for testing
```

改为：

**使用私有仓库镜像名**

```java
// Referring directly to an image on a private registry - image name will vary
final MySQLContainer<?> mysql = new MySQLContainer<>(
    DockerImageName.parse("registry.mycompany.com/mirror/mysql:8.0.36")
        .asCompatibleSubstituteFor("mysql")
)
// start the container and use it for testing
```

## 自动修改 Docker Hub 镜像名

Testcontainers 可以配置为在运行时动态修改 Docker Hub 镜像名，为其添加前缀字符串。

在以下情况下可以考虑这种方式：

- 开发者和 CI 机器需要使用不同的镜像名。例如，开发者可以从 Docker Hub 拉取镜像，但 CI 机器需要从私有仓库拉取
- 你的私有仓库中保存了来自 Docker Hub 的镜像副本，且命名可预测，只需添加前缀即可。例如，`registry.mycompany.com/mirror/mysql:8.0.36` 可以通过在原始 Docker Hub 镜像名（`mysql:8.0.36`）前添加一致的前缀字符串 `registry.mycompany.com/mirror/` 得到

在这种情况下，代码中的镜像名引用**保持不变**。也就是说，你仍然保留原样：

**保持不变的直接 Docker Hub 镜像名**

```java
// Referring directly to an image on Docker Hub (mysql:8.0.36)
final MySQLContainer<?> mysql = new MySQLContainer<>(
    DockerImageName.parse("mysql:8.0.36")
)
// start the container and use it for testing
```

然后，你可以配置 Testcontainers 对它尝试从 Docker Hub 拉取的每个镜像应用前缀 `registry.mycompany.com/mirror/`。这可以通过以下两种方式之一完成：

- 设置环境变量 `TESTCONTAINERS_HUB_IMAGE_NAME_PREFIX=registry.mycompany.com/mirror/`
- 通过配置文件，在以下任一位置设置 `hub.image.name.prefix`：
  - 用户主目录下的 `~/.testcontainers.properties` 文件，或
  - classpath 上名为 `testcontainers.properties` 的文件

Testcontainers 会自动对它从 Docker Hub 拉取的每个镜像应用该前缀——请确认你的仓库中存在所有[所需镜像](../../supported_docker_environment/image_registry_rate_limiting/index.md#which-images-are-used-by-testcontainers)。

Testcontainers 不会对以下情况应用前缀：

- 非 Hub 镜像名（例如指定了其他仓库）
- 名称中明确包含 Hub 仓库地址的 Docker Hub 镜像名（即主机部分为 `docker.io` 或 `registry.hub.docker.com` 的任何名称）

## 开发一个自定义函数，在运行时动态转换镜像名

在以下情况下可以考虑这种方式：

- 你对“应使用哪些私有仓库镜像作为替代品”有复杂的规则，例如：
  - 名称映射不确定，无法使用[名称前缀](#automatically-modifying-docker-hub-image-names)
  - 规则取决于开发者身份或所在位置
- 或者你希望对构建中使用的镜像进行审计记录
- 或者你希望防止意外使用未在批准列表中的镜像

在这种情况下，代码中的镜像名引用**保持不变**。也就是说，你仍然保留原样：

**保持不变的直接 Docker Hub 镜像名**

```java
// Referring directly to an image on Docker Hub (mysql:8.0.36)
final MySQLContainer<?> mysql = new MySQLContainer<>(
    DockerImageName.parse("mysql:8.0.36")
)
// start the container and use it for testing
```

你可以通过以下方式实现自定义镜像名替换器：

- 继承 `org.testcontainers.utility.ImageNameSubstitutor`
- 配置 Testcontainers 使用你的自定义实现

下面是一个镜像替换器实现示例：

**镜像替换器示例**

```java
public class ExampleImageNameSubstitutor extends ImageNameSubstitutor {

    @Override
    public DockerImageName apply(DockerImageName original) {
        // convert the original name to something appropriate for
        // our build environment
        return DockerImageName.parse(
            // your code goes here - silly example of capitalising
            // the original name is shown
            original.asCanonicalNameString().toUpperCase()
        );
    }

    @Override
    protected String getDescription() {
        // used in logs
        return "example image name substitutor";
    }
}
```

可以通过配置让 Testcontainers 在运行时找到它。为此，在 classpath 上创建或修改名为 `testcontainers.properties` 的文件。

例如：

**src/test/resources/testcontainers.properties**

```text
image.substitutor=com.mycompany.testcontainers.ExampleImageNameSubstitutor
```

请注意，同样的配置属性也可以通过以下方式提供：

- 放在库 JAR 文件根目录下的 `testcontainers.properties` 文件中（如果你希望在组织内部发布一个即插即用的镜像替换器 JAR，这种方式很有用）
- 放在用户主目录下的属性文件中（`~/.testcontainers.properties`；注意前导 `.`）
- 或作为环境变量（例如 `TESTCONTAINERS_IMAGE_SUBSTITUTOR=com.mycompany.testcontainers.ExampleImageNameSubstitutor`）。

更多信息请参阅[配置机制文档](../configuration/index.md)。

此外，你还可以使用 `ServiceLoader` 机制来提供 `ImageNameSubstitutor` 实现的全限定类名：

**src/test/resources/META-INF/services/org.testcontainers.utility.ImageNameSubstitutor**

```text
com.mycompany.testcontainers.ExampleImageNameSubstitutor
```

## 在配置中逐个覆盖镜像名

> **Note**
>
> 不推荐并且已弃用这种方式，但为了完整性仍在此记录。请优先考虑本页介绍的其他方式之一。未来可能会移除通过配置逐个覆盖镜像名的功能。

在以下情况下可以考虑这种方式：

- 代码中有大量镜像名引用，修改它们不切实际，并且
- 其他选项对你都不适用

在这种情况下，代码中的镜像名引用**保持不变**。也就是说，你仍然保留原样：

**保持不变的直接 Docker Hub 镜像名**

```java
// Referring directly to an image on Docker Hub (mysql:8.0.36)
final MySQLContainer<?> mysql = new MySQLContainer<>(
    DockerImageName.parse("mysql:8.0.36")
)
// start the container and use it for testing
```

你可以[使用配置文件](../configuration/index.md)强制 Testcontainers 替换为不同的镜像，这允许替换部分（但不是全部）容器名称。
