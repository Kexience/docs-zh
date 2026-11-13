---
source_url: https://java.testcontainers.org/test_framework_integration/junit_4/
source_hash: sha256:bec0b7fc5733c57e916d96a87473c990756db94b36c41368795498799903872f
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# JUnit 4

## `@Rule`/`@ClassRule` 集成

**JUnit4 `@Rule`/`@ClassRule`**：该模式会在测试之前启动容器，并在测试之后将其销毁。

在测试类中添加一个带 `@Rule` 或 `@ClassRule` 注解的字段，例如：

```java
public class SimpleMySQLTest {
    @Rule
    public MySQLContainer mysql = new MySQLContainer();

    // [...]
}
```

## 手动控制容器生命周期

作为替代方案，你可以在测试中带有 `@BeforeClass`/`@Before` 注解的方法里手动启动容器。容器会在 JVM 退出时自动销毁，但你当然也可以使用带有 `@AfterClass`/`@After` 注解的方法手动调用容器的 `stop()` 方法。

*在带有 `@Before` 注解的方法中启动容器的示例：*

```java
class SimpleMySQLTest {
    private MySQLContainer mysql = new MySQLContainer();

    @Before
    void before() {
        mysql.start();
    }

    @After
    void after() {
        mysql.stop();
    }

    // [...]
}
```

## 单例容器

请注意，在使用 JUnit 4 时，[单例容器模式](../manual_lifecycle_control/index.md#singleton-containers)同样是一种可选方案。
