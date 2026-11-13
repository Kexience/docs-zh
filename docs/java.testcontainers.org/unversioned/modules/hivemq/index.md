---
source_url: https://java.testcontainers.org/modules/hivemq/
source_hash: sha256:dfc0cc6ccadcb05a9cd0500f64c01b0c063b548c1dab4407cf58622470657a0c
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# HiveMQ

![HiveMQ logo](https://java.testcontainers.org/modules_logos/hivemq-module.png)

用于在 JUnit5 测试中自动启动 HiveMQ Docker 容器。这使得测试 MQTT 客户端应用程序以及对自定义 HiveMQ 扩展进行集成测试成为可能。

- 社区论坛：https://community.hivemq.com/
- HiveMQ 网站：https://www.hivemq.com/
- MQTT 资源：
  - [MQTT Essentials](https://www.hivemq.com/mqtt-essentials/)
  - [MQTT 5 Essentials](https://www.hivemq.com/mqtt-5/)

请务必查阅 hivemq-docs 中关于 [Community Edition](https://github.com/hivemq/hivemq-community-edition/wiki/) 和 [Enterprise Edition](https://www.hivemq.com/docs/hivemq/4.7/user-guide/) 的文档。

## 使用 HiveMQ CE/EE

HiveMQ 在 [Docker Hub](https://hub.docker.com/u/hivemq) 上提供了不同的版本：

- 开源的 [Community Edition](https://github.com/hivemq/hivemq-community-edition)，发布为 *hivemq/hivemq-ce*。
- [Enterprise Edition](https://www.hivemq.com/docs/hivemq/4.7/user-guide/)，发布为 *hivemq/hivemq4*。

两种版本都可以直接使用：

使用 Community Edition：

**Community Edition HiveMQ 镜像**

```java
@Container
final HiveMQContainer hivemqCe = new HiveMQContainer(DockerImageName.parse("hivemq/hivemq-ce").withTag("2024.3"))
    .withLogLevel(Level.DEBUG);
```

使用 Enterprise Edition：

**Enterprise Edition HiveMQ 镜像**

```java
@Container
final HiveMQContainer hivemqEe = new HiveMQContainer(DockerImageName.parse("hivemq/hivemq4").withTag("4.7.4"))
    .withLogLevel(Level.DEBUG);
```

可以通过使用标签来指定特定版本：

**指定 HiveMQ 版本**

```java
@Container
final HiveMQContainer hivemqSpecificVersion = new HiveMQContainer(DockerImageName.parse("hivemq/hivemq-ce:2024.3"));
```

## 测试你的 MQTT 3 和 MQTT 5 客户端应用程序

使用 Mqtt 客户端（例如 [HiveMQ-Mqtt-Client](https://github.com/hivemq/hivemq-mqtt-client)），你可以直接开始测试。

**MQTT5 客户端**

```java
final Mqtt5BlockingClient client = Mqtt5Client
    .builder()
    .serverPort(hivemqCe.getMqttPort())
    .serverHost(hivemqCe.getHost())
    .buildBlocking();

client.connect();
client.disconnect();
```

## 设置

在容器设置之前可以进行多项调整。以下示例展示了如何启用 Control Center（这是一项企业版功能）、将日志级别设置为 DEBUG，并从 classpath 加载 HiveMQ 配置文件。

**配置示例**

```java
@Container
final HiveMQContainer hivemqEeWithControlCenter = new HiveMQContainer(
    DockerImageName.parse("hivemq/hivemq4").withTag("4.7.4")
)
    .withLogLevel(Level.DEBUG)
    .withHiveMQConfig(MountableFile.forClasspathResource("/inMemoryConfig.xml"))
    .withControlCenter();
```

---

**注意：** HiveMQ 的 Control Center 可以通过启动容器输出中显示的 URL 访问：

```
2021-09-10 10:35:53,511 INFO  - The HiveMQ Control Center is reachable under: http://localhost:55032
```

请注意，Control Center 是 HiveMQ 企业版的功能，因此仅在企业版镜像中可用。

---

## 测试 HiveMQ 扩展

使用 [Extension SDK](https://github.com/hivemq/hivemq-extension-sdk)，可以扩展所有版本 HiveMQ 的功能。HiveMQ 模块也支持测试你自己的自定义扩展。

### 等待策略

原始的 HiveMQ 模块通过等待特定的启动日志消息来判断是否就绪。由于扩展是动态加载的，它们可能会在主容器启动后短暂延迟才可用。因此，我们为 HiveMQ 扩展提供了自定义等待条件：

以下示例将指定从 **src/test/resources/modifier-extension** 加载扩展到容器中，并等待名为 **'My Extension Name'** 的扩展启动：

**自定义等待策略**

```java
@Container
final HiveMQContainer hivemqWithWaitStrategy = new HiveMQContainer(
    DockerImageName.parse("hivemq/hivemq4").withTag("4.7.4")
)
    .withExtension(MountableFile.forClasspathResource("/modifier-extension"))
    .waitForExtension("Modifier Extension");
```

接下来是一个直接从 classpath 使用扩展并直接等待该扩展的示例：

**来自 Classpath 的扩展**

```java
final HiveMQExtension hiveMQEClasspathxtension = HiveMQExtension
    .builder()
    .id("extension-1")
    .name("my-extension")
    .version("1.0")
    .mainClass(MyExtensionWithSubclasses.class)
    .build();

@Container
final HiveMQContainer hivemqWithClasspathExtension = new HiveMQContainer(
    DockerImageName.parse("hivemq/hivemq-ce").withTag("2024.3")
)
    .waitForExtension(hiveMQEClasspathxtension)
    .withExtension(hiveMQEClasspathxtension)
    .withHiveMQConfig(MountableFile.forClasspathResource("/inMemoryConfig.xml"));
```

---

**注意** 调试扩展

两个示例都包含 `.withDebugging()`，它可以在容器上启用远程调试。启用调试后，你可以直接在扩展中设置断点。

---

### 使用 Gradle 测试扩展

在基于 Gradle 的 HiveMQ 扩展项目中，可以使用专用的 [HiveMQ Extension Gradle Plugin](https://github.com/hivemq/hivemq-extension-gradle-plugin/README.md) 来支持测试。

该插件添加了一个 `integrationTest` 任务，用于执行 `integrationTest` 源集中的测试。- 集成测试源文件定义在 `src/integrationTest` 中。- 集成测试依赖通过 `integrationTestImplementation`、`integrationTestRuntimeOnly` 等配置进行定义。

`integrationTest` 任务会构建扩展并将其解压到 `build/hivemq-extension-test` 目录。然后测试可以将构建好的扩展加载到 HiveMQ Testcontainer 中。

**来自文件系统的扩展**

```java
@Container
final HiveMQContainer hivemqExtensionFromFilesystem = new HiveMQContainer(
    DockerImageName.parse("hivemq/hivemq4").withTag("4.7.4")
)
    .withExtension(MountableFile.forHostPath("src/test/resources/modifier-extension"));
```

### 启用/禁用扩展

可以在运行时启用和禁用 HiveMQ 扩展。扩展也可以在启动时被禁用。

---

**注意**：在运行时禁用或启用扩展仅在 HiveMQ 4 Enterprise Edition 容器中受支持。

---

以下示例展示了如何在启动 HiveMQ 容器时禁用名为 **my-extension** 的扩展。

**在启动时禁用扩展**

```java
private final HiveMQExtension hiveMQExtension = HiveMQExtension
    .builder()
    .id("extension-1")
    .name("my-extension")
    .version("1.0")
    .disabledOnStartup(true)
    .mainClass(MyExtension.class)
    .build();

@Container
final HiveMQContainer hivemq = new HiveMQContainer(DockerImageName.parse("hivemq/hivemq4").withTag("4.7.4"))
    .withExtension(hiveMQExtension);
```

然后，以下测试会继续启用并再次禁用该扩展：

**在运行时启用/禁用扩展**

```java
@Test
void test_disable_enable_extension() throws Exception {
    hivemq.enableExtension(hiveMQExtension);
    hivemq.disableExtension(hiveMQExtension);
}
```

## 启用/禁用从文件夹加载的扩展

在运行时从扩展文件夹加载的扩展也可以即时启用/禁用。如果扩展文件夹中包含 DISABLED 文件，则该扩展将在启动时被禁用。

---

**注意**：在运行时禁用或启用扩展仅在 HiveMQ 4 Enterprise Edition 容器中受支持。

---

我们首先从文件系统加载扩展：

**来自文件系统的扩展**

```java
@Container
final HiveMQContainer hivemqExtensionFromFilesystem = new HiveMQContainer(
    DockerImageName.parse("hivemq/hivemq4").withTag("4.7.4")
)
    .withExtension(MountableFile.forHostPath("src/test/resources/modifier-extension"));
```

现在我们可以使用扩展名称来启用/禁用它：

**在运行时启用/禁用扩展**

```java
@Test
void test_disable_enable_extension_from_filesystem() throws Exception {
    hivemqExtensionFromFilesystem.disableExtension("Modifier Extension", "modifier-extension");
    hivemqExtensionFromFilesystem.enableExtension("Modifier Extension", "modifier-extension");
}
```

### 移除预装的 HiveMQ 扩展

自 HiveMQ 4.4 版本发布以来，HiveMQ Docker 镜像附带了 HiveMQ Extension for Kafka、HiveMQ Enterprise Bridge Extension 和 HiveMQ Enterprise Security Extension。这些扩展默认处于禁用状态，但有时你可能需要在容器启动前将它们移除。

移除所有扩展非常简单：

**移除所有扩展**

```java
@Container
final HiveMQContainer hivemqNoExtensions = new HiveMQContainer(
    DockerImageName.parse("hivemq/hivemq4").withTag("4.7.4")
)
    .withoutPrepackagedExtensions();
```

移除单个扩展（例如 Kafka）同样简单：

**移除特定扩展**

```java
@Container
final HiveMQContainer hivemqNoKafkaExtension = new HiveMQContainer(
    DockerImageName.parse("hivemq/hivemq4").withTag("4.7.4")
)
    .withoutPrepackagedExtensions("hivemq-kafka-extension");
```

## 将文件放入容器

### 将文件放入 HiveMQ 主目录

**将文件放入 HiveMQ 主目录**

```java
final HiveMQContainer hivemqFileInHome = new HiveMQContainer(
    DockerImageName.parse("hivemq/hivemq-ce").withTag("2024.3")
)
    .withFileInHomeFolder(
        MountableFile.forHostPath("src/test/resources/additionalFile.txt"),
        "/path/in/home/folder"
    );
```

### 将文件放入扩展主目录

**将文件放入 HiveMQ 扩展主目录**

```java
@Container
final HiveMQContainer hivemqFileInExtensionHome = new HiveMQContainer(
    DockerImageName.parse("hivemq/hivemq-ce").withTag("2024.3")
)
    .withExtension(
        HiveMQExtension
            .builder()
            .id("extension-1")
            .name("my-extension")
            .version("1.0")
            .mainClass(MyExtension.class)
            .build()
    )
    .withFileInExtensionHomeFolder(
        MountableFile.forHostPath("src/test/resources/additionalFile.txt"),
        "extension-1",
        "/path/in/extension/home"
    );
```

### 将许可证文件放入容器

**将许可证文件放入 HiveMQ 容器**

```java
@Container
final HiveMQContainer hivemq = new HiveMQContainer(DockerImageName.parse("hivemq/hivemq-ce").withTag("2024.3"))
    .withLicense(MountableFile.forHostPath("src/test/resources/myLicense.lic"))
    .withLicense(MountableFile.forHostPath("src/test/resources/myExtensionLicense.elic"));
```

### 进一步自定义容器

由于 `HiveMQContainer` 继承自 [Testcontainers](https://github.com/testcontainers) 的 `GenericContainer`，因此可以根据需要对容器进行自定义。

## 添加到你的项目

### Gradle

添加到 `build.gradle`：

```
testImplementation 'org.testcontainers:testcontainers-hivemq:2.0.5'
```

添加到 `build.gradle.kts`：

```
testImplementation("org.testcontainers:testcontainers-hivemq:2.0.5")
```

### Maven

添加到 `pom.xml`：

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-hivemq</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
