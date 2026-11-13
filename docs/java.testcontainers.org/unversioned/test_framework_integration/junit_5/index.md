---
source_url: https://java.testcontainers.org/test_framework_integration/junit_5/
source_hash: sha256:f70da5dad53b0f69efbc8b66359c992581a84f259f3e507020593ceec6ca43c6
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Jupiter / JUnit 5

该模块提供了一个基于 [JUnit Jupiter](https://junit.org/junit5/) 扩展模型的 API。

该扩展支持两种模式：

- 为每个测试方法重新启动的容器
- 在测试类的所有方法之间共享的容器

请注意，Jupiter/JUnit 5 集成被打包为一个单独的库 JAR；详情见[下文](#adding-testcontainers-junit-5-support-to-your-project-dependencies)。

## 扩展

Jupiter 集成通过 `@Testcontainers` 注解提供。

该扩展会查找所有带有 `@Container` 注解的字段，并调用它们的容器生命周期方法（`Startable` 接口上的方法）。声明为 static 字段的容器将在测试方法之间共享。它们只会在任何测试方法执行之前启动一次，并在最后一个测试方法执行之后停止。声明为实例字段的容器会为每个测试方法启动和停止。

**注意：** 该扩展仅在顺序执行测试的情况下经过测试。不支持在并行测试执行中使用它，可能会产生意外的副作用。

*示例：*

**混合生命周期**

```java
@Testcontainers
class MixedLifecycleTests {

    // will be shared between test methods
    @Container
    private static final MySQLContainer MY_SQL_CONTAINER = new MySQLContainer("mysql:8.0.36");

    // will be started before and stopped after each test method
    @Container
    private PostgreSQLContainer postgresqlContainer = new PostgreSQLContainer("postgres:9.6.12")
        .withDatabaseName("foo")
        .withUsername("foo")
        .withPassword("secret");

    @Test
    void test() {
        assertThat(MY_SQL_CONTAINER.isRunning()).isTrue();
        assertThat(postgresqlContainer.isRunning()).isTrue();
    }
}
```

## 示例

要使用 Testcontainers 扩展，请在测试类上添加 `@Testcontainers` 注解。

### 重新启动的容器

要定义一个重新启动的容器，请在测试类中定义一个实例字段，并使用 `@Container` 注解标记它。

**重新启动的容器**

```java
@Testcontainers
class TestcontainersNestedRestartedContainerTests {

    @Container
    private final GenericContainer<?> topLevelContainer = new GenericContainer<>(JUnitJupiterTestImages.HTTPD_IMAGE)
        .withExposedPorts(80);


⋯

    @Test
    void top_level_container_should_be_running() {
        assertThat(topLevelContainer.isRunning()).isTrue();

        ⋯

    }

    @Nested
    class NestedTestCase {

        @Container
        private final GenericContainer<?> nestedContainer = new GenericContainer<>(JUnitJupiterTestImages.HTTPD_IMAGE)
            .withExposedPorts(80);

        @Test
        void both_containers_should_be_running() {
            // top level container is restarted for nested methods
            assertThat(topLevelContainer.isRunning()).isTrue();
            // nested containers are only available inside their nested class
            assertThat(nestedContainer.isRunning()).isTrue();

            ⋯

        }


⋯

    }
}
```

### 共享容器

共享容器在顶层测试类中定义为 static 字段，并且必须使用 `@Container` 注解。请注意，共享容器不能在嵌套测试类中声明。这是因为嵌套测试类必须定义为非 static，因此不能拥有 static 字段。

## 单例容器

请注意，在使用 JUnit 5 时，[单例容器模式](../manual_lifecycle_control/index.md#singleton-containers)同样是一种可选方案。

## 限制

该扩展仅在顺序执行测试的情况下经过测试。不支持在并行测试执行中使用它，可能会产生意外的副作用。

## 将 Testcontainers JUnit 5 支持添加到项目依赖中

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-junit-jupiter:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-junit-jupiter</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
