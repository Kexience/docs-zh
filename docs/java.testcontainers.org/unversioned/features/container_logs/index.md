---
source_url: https://java.testcontainers.org/features/container_logs/
source_hash: sha256:60e1c70ef73ce34ae565bf8e9dfe481b630d66d71e5e809d141db03188e6e619
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# 访问容器日志

可以通过以下方式捕获容器输出：

- `getLogs()` 方法，它直接返回容器完整日志输出的 `String` 快照
- `followOutput()` 方法。该方法接受一个 Consumer，并（可选）接受一个可变参数列表，指明要跟随 STDOUT、STDERR 还是两者。如果未指定，则两者都会被跟随。

目前，容器输出总是从容器创建的时刻开始。

## 读取全部日志（从启动到当前）

`getLogs()` 是访问容器日志最简单的机制，用法如下：

**访问全部输出（stdout 和 stderr）**

```java
final String logs = container.getLogs();
```

**只访问 stdout**

```java
final String logs = container.getLogs(OutputFrame.OutputType.STDOUT);
```

**只访问 stderr**

```java
final String logs = container.getLogs(OutputFrame.OutputType.STDERR);
```

## 流式读取日志

Testcontainers 内置了一些开箱即用的 Consumer 实现，可与流式的 `followOutput()` 模型配合使用；示例如下。

### 将容器输出流式写入 SLF4J logger

给定一个已存在的、名为 LOGGER 的 SLF4J logger 实例：

```java
Slf4jLogConsumer logConsumer = new Slf4jLogConsumer(LOGGER);
container.followOutput(logConsumer);
```

默认情况下，standard out 和 standard error 都会以 INFO 级别输出。如果需要，standard error 也可以以 ERROR 级别输出：

```java
Slf4jLogConsumer logConsumer = new Slf4jLogConsumer(LOGGER).withSeparateOutputStreams();
```

输出消息的 [Mapped Diagnostic Context (MDC)](http://logback.qos.ch/manual/mdc.html) 可以通过 `withMdc(...)` 选项进行配置：

```java
Slf4jLogConsumer logConsumer = new Slf4jLogConsumer(LOGGER).withMdc("key", "value");
```

或者使用一个已有的键值对 map：

```java
Slf4jLogConsumer logConsumer = new Slf4jLogConsumer(LOGGER).withMdc(map);
```

### 将容器输出捕获为 String

要实时流式读取日志或自定义解码方式，可以使用 `ToStringConsumer`：

```java
ToStringConsumer toStringConsumer = new ToStringConsumer();
container.followOutput(toStringConsumer, OutputType.STDOUT);

String utf8String = toStringConsumer.toUtf8String();

// Or if the container output is not UTF-8
String otherString = toStringConsumer.toString(CharSet.forName("ISO-8859-1"));
```

### 等待容器输出包含预期内容

`WaitingConsumer` 会一直阻塞，直到某一帧容器输出（通常是一行）匹配给定的谓词。

可以指定超时时间，如下例所示。

```java
WaitingConsumer consumer = new WaitingConsumer();

container.followOutput(consumer, STDOUT);

consumer.waitUntil(frame -> 
    frame.getUtf8String().contains("STARTED"), 30, TimeUnit.SECONDS);
```

此外，由于使用的是 Java 8 的 Consumer 函数式接口，多个 Consumer 可以组合在一起使用。例如，这可以让你捕获全部容器输出，但只在找到匹配的字符串之后才输出。例如：

```java
WaitingConsumer waitingConsumer = new WaitingConsumer();
ToStringConsumer toStringConsumer = new ToStringConsumer();

Consumer<OutputFrame> composedConsumer = toStringConsumer.andThen(waitingConsumer);
container.followOutput(composedConsumer);

waitingConsumer.waitUntil(frame -> 
    frame.getUtf8String().contains("STARTED"), 30, TimeUnit.SECONDS);

String utf8String = toStringConsumer.toUtf8String();
```
