---
source_url: https://java.testcontainers.org/modules/webdriver_containers/
source_hash: sha256:50be66621a8d140b8e349b9d99e5a2ffdd6a5e84fac9e784707ad1f095f18e03
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# WebDriver 容器模块

Testcontainers 可用于自动实例化和管理包含 Web 浏览器的容器，例如来自 SeleniumHQ 的 [docker-selenium](https://github.com/SeleniumHQ/docker-selenium) 项目的容器。

## 优势

- 与用于 Chrome 和 Firefox 的 Selenium 3 和 4 测试以及用于 Edge 的 Selenium 4 测试完全兼容，通过提供 `RemoteWebDriver` 实例
- 无需在测试服务器上安装特定的 Web 浏览器，甚至无需桌面环境。唯一的依赖是可用的 Docker 安装和你的 Java JUnit 测试套件。
- 浏览器始终从固定、干净的镜像启动。这意味着不会因用户更改或浏览器自动升级而产生配置漂移。
- 保证浏览器版本与 Selenium API 之间的兼容性：将根据类路径上 `selenium-api-*.jar` 的版本自动选择兼容版本的浏览器 Docker 镜像
- 此外，使用干净的浏览器可防止测试之间的 cookie、缓存数据或其他状态泄露。
- **VNC 屏幕录制**：Testcontainers 可以自动录制测试运行的视频（可选择仅捕获失败的测试）

浏览器容器的创建速度很快，因此为每个测试都使用全新的浏览器实例实际上是完全可行的。

## 示例

在你的 JUnit UI 测试类中，以下字段将准备一个运行 Chrome 的容器：

**Chrome**

```java
public BrowserWebDriverContainer chrome = new BrowserWebDriverContainer("selenium/standalone-chrome:4.13.0")
```

现在，不要直接实例化 WebDriver 实例，而是使用以下方式在测试方法中获取实例：

**RemoteWebDriver**

```java
RemoteWebDriver driver = new RemoteWebDriver(chrome.getSeleniumAddress(), new ChromeOptions());
```

然后，你可以像使用常规 WebDriver 一样使用此驱动实例。

请注意，如果你想测试**运行在主机上的 Web 应用程序**（即运行 JUnit 测试的机器——这很常见），你需要使用 Testcontainers 的[主机端口暴露](../../features/networking/index.md#exposing-host-ports-to-the-container)功能，例如：

**打开网页**

```java
Testcontainers.exposeHostPorts(localPort);
driver.get("http://host.testcontainers.internal:" + localPort);
```

## 选项

### 其他浏览器

目前支持 Chrome、Firefox 和 Edge。要切换浏览器，只需更改规则构造函数的第一个参数：

**Chrome**

```java
public BrowserWebDriverContainer chrome = new BrowserWebDriverContainer("selenium/standalone-chrome:4.13.0")
```

**Firefox**

```java
public BrowserWebDriverContainer firefox = new BrowserWebDriverContainer("selenium/standalone-firefox:4.13.0")
```

**Edge**

```java
public BrowserWebDriverContainer edge = new BrowserWebDriverContainer("selenium/standalone-edge:4.13.0")
```

### 录制视频

默认情况下，不会录制任何视频。但是，你可以指示 Testcontainers 为所有测试或仅为失败的测试捕获视频。

**录制所有测试**

```java
// To do this, simply add extra parameters to the rule constructor, so video will default to FLV format:
BrowserWebDriverContainer chrome = new BrowserWebDriverContainer("selenium/standalone-chrome:4.13.0")
    .withRecordingMode(VncRecordingMode.RECORD_ALL, target)
```

**录制失败的测试**

```java
// or if you only want videos for test failures:
BrowserWebDriverContainer chrome = new BrowserWebDriverContainer("selenium/standalone-chrome:4.13.0")
    .withRecordingMode(VncRecordingMode.RECORD_FAILING, target)
```

请注意，`withRecordingMode` 的第二个参数应为可保存录制文件的目录。

默认情况下，视频将以 [FLV](https://en.wikipedia.org/wiki/Flash_Video) 格式录制，但你可以显式指定格式，或使用带有 `VncRecordingFormat` 选项的 `withRecordingMode` 方法将其更改为 [MP4](https://en.wikipedia.org/wiki/MPEG-4_Part_14)：

**MP4 视频格式**

```java
// Set MP4 format for recorded video:
BrowserWebDriverContainer chrome = new BrowserWebDriverContainer("selenium/standalone-chrome:4.13.0")
    .withRecordingMode(VncRecordingMode.RECORD_ALL, target, VncRecordingFormat.MP4)
```

**FLV 视频格式**

```java
// Set (explicitly) FLV format for recorded video:
BrowserWebDriverContainer chrome = new BrowserWebDriverContainer("selenium/standalone-chrome:4.13.0")
    .withRecordingMode(VncRecordingMode.RECORD_ALL, target, VncRecordingFormat.FLV)
```

如果你想自定义录制文件的文件名，或根据测试描述和/或其成功或失败在运行时提供不同的目录，你可以按如下方式提供自定义录制文件工厂：

**CustomRecordingFileFactory**

```java
BrowserWebDriverContainer chrome = new BrowserWebDriverContainer("selenium/standalone-chrome:4.13.0")

⋯

    .withRecordingFileFactory(new CustomRecordingFileFactory())
```

请注意，该工厂必须实现 `org.testcontainers.containers.RecordingFileFactory`。

## 更多示例

[ChromeWebDriverContainerTest.java](https://github.com/testcontainers/testcontainers-java/blob/main/modules/selenium/src/test/java/org/testcontainers/selenium/ChromeWebDriverContainerTest.java) 中展示了一些不同的示例。

## 将此模块添加到项目依赖

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-selenium:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-selenium</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```

> **Hint**
>

> 添加此 Testcontainers 库 JAR 不会自动将 Selenium Webdriver JAR 添加到你的项目中。你应确保项目中也有合适的 Selenium 依赖，例如：
>
> **Gradle**
>
> **Maven**
>
> Testcontainers 将尝试将 Docker 化浏览器的版本与类路径上找到的 Selenium 版本进行匹配

```groovy
compile "org.seleniumhq.selenium:selenium-remote-driver:3.141.59"
```

```xml
<dependency>
    <groupId>org.seleniumhq.selenium</groupId>
    <artifactId>selenium-remote-driver</artifactId>
    <version>3.141.59</version>
</dependency>
```
