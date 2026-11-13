---
source_url: https://java.testcontainers.org/test_framework_integration/manual_lifecycle_control/
source_hash: sha256:216869773878b3bba44e75a5c273144de72d6ecd38a12f1b79667ae32fa773a7
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# 手动控制容器生命周期

Testcontainers 可以与任何测试框架配合使用，甚至完全不使用测试框架。

## 手动启动/停止容器

可以在代码中使用 `start()` 和 `stop()` 方法启动和停止容器。此外，容器类实现了 `AutoCloseable`。这能更好地确保容器在合适的时机被停止。

```java
try (GenericContainer container = new GenericContainer("imagename")) {
    container.start();
    // ... use the container
    // no need to call stop() afterwards
}
```

## 单例容器

有时，定义一个只为多个测试类启动一次的容器会很有用。Testcontainers 扩展并未为这种用例提供专门支持。不过，可以使用以下模式来实现：

```java
abstract class AbstractContainerBaseTest {

    static final MySQLContainer MY_SQL_CONTAINER;

    static {
        MY_SQL_CONTAINER = new MySQLContainer();
        MY_SQL_CONTAINER.start();
    }
}

class FirstTest extends AbstractContainerBaseTest {

    @Test
    void someTestMethod() {
        String url = MY_SQL_CONTAINER.getJdbcUrl();

        // create a connection and run test as normal
    }
}
```

单例容器只会在基类加载时启动一次。之后，所有继承的测试类都可以使用该容器。在测试套件结束时，由 Testcontainers core 启动的 [Ryuk 容器](https://github.com/testcontainers/moby-ryuk) 会负责停止该单例容器。
