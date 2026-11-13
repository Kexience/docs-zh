---
source_url: https://java.testcontainers.org/modules/ollama/
source_hash: sha256:0d547e077cdf2bf41821c1ff6654c77d938d6ed18531ac247a37a52d5f91aacd
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Ollama

用于 [Ollama](https://hub.docker.com/r/ollama/ollama) 的 Testcontainers 模块。

## Ollama 使用示例

你可以在任何 Java 应用程序中通过以下方式启动 Ollama 容器实例：

**Ollama 容器**

```java
OllamaContainer ollama = new OllamaContainer("ollama/ollama:0.1.26")
```

### 拉取模型

Testcontainers 允许[在容器中执行命令](../../features/commands/index.md)。因此，拉取模型非常简单：

**拉取模型**

```java
ollama.execInContainer("ollama", "pull", "all-minilm");
```

### 创建新镜像

为了创建包含该模型的新镜像，你可以使用以下代码：

**提交镜像**

```java
ollama.commitToImage(newImageName);
```

然后将新镜像与[镜像名称替换](../../features/image_name_substitution/index.md#manual-substitution)一起使用：

**使用新镜像**

```java
OllamaContainer ollama = new OllamaContainer(
    DockerImageName.parse(newImageName)
        .asCompatibleSubstituteFor("ollama/ollama")
)
```

## 将此模块添加到项目依赖中

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-ollama:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-ollama</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
