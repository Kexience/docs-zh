---
source_url: https://java.testcontainers.org/supported_docker_environment/logging_config/
source_hash: sha256:0186903b50e1b1ce711c24185fcef38a6dcb996d0a6941c212b9c56cbd778972
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# 日志配置

Testcontainers 及其使用的许多库都使用 SLF4J 进行日志记录。为了查看来自 Testcontainers 的日志，你的项目应包含一个 SLF4J 实现（推荐使用 Logback）。应将以下 `logback-test.xml` 示例包含在你的 classpath 中，以显示合理级别的日志输出：

```xml
<configuration>
    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger - %msg%n</pattern>
        </encoder>
    </appender>

    <root level="info">
        <appender-ref ref="STDOUT"/>
    </root>

    <logger name="org.testcontainers" level="INFO"/>
    <!-- The following logger can be used for containers logs since 1.18.0 -->
    <logger name="tc" level="INFO"/>
    <logger name="com.github.dockerjava" level="WARN"/>
    <logger name="com.github.dockerjava.zerodep.shaded.org.apache.hc.client5.http.wire" level="OFF"/>
</configuration>
```

为了排查 Testcontainers 的问题，请将 `org.testcontainers` 的日志级别提高到 `DEBUG`：

```xml
<logger name="org.testcontainers" level="DEBUG"/>
```

避免将根 logger 的级别更改为 `DEBUG`，因为这会为此处未显式配置级别的每个包启用调试日志记录，从而产生大量日志数据。
