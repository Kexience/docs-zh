---
source_url: https://java.testcontainers.org/modules/k6/
source_hash: sha256:eeea15a1338cbe1cba203ad9353d4494d793a3e51197434de3bd2fa935686913
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# k6

> **注意**
>

> 此模块处于孵化阶段。虽然它已准备就绪并可在当前版本的 Testcontainers 中正常使用，但未来可能会引入破坏性变更。有关孵化模块策略的更多信息，请参阅[我们的贡献指南](../../contributing/index.md#incubating-modules)。

用于 [k6](https://registry.hub.docker.com/r/grafana/k6) 的 Testcontainers 模块。

[k6](https://k6.io/) 是一款为提升开发者体验而构建的可扩展可靠性测试工具。

## 基本脚本执行

你可以在任何 Java 应用程序中通过以下方式启动 K6 容器实例：

**设置容器**

```java
K6Container container = new K6Container("grafana/k6:0.49.0")
    .withTestScript(MountableFile.forClasspathResource("scripts/test.js"))
    .withScriptVar("MY_SCRIPT_VAR", "are cool!")
    .withScriptVar("AN_UNUSED_VAR", "unused")
    .withCmdOptions("--quiet", "--no-usage-report")
```

上面的测试使用了一个简单的 k6 脚本 `test.js`，其中包含命令行选项和注入的脚本变量。

容器启动后，你可以等待收集测试结果：

**等待测试结果**

```java
WaitingConsumer consumer = new WaitingConsumer();
container.followOutput(consumer);

// Wait for test script results to be collected
consumer.waitUntil(
    frame -> {
        return frame.getUtf8String().contains("iteration_duration");
    },
    3,
    TimeUnit.SECONDS
);
```

创建一个简单的 k6 测试脚本，作为测试的一部分执行：

**scripts/test.js 的内容**

```javascript
// The most basic of k6 scripts.
export default function(){
    console.log(`k6 tests ${__ENV.MY_SCRIPT_VAR}`)
}
```

## 将此模块添加到项目依赖中

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-k6:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-k6</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
