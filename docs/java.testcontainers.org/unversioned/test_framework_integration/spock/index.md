---
source_url: https://java.testcontainers.org/test_framework_integration/spock/
source_hash: sha256:1ac13d90a1808eb0ed6d650fae16a710d060ef43b84ab9153c9b725dda9c6a04
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Spock

用于 [Testcontainers](https://github.com/testcontainers/testcontainers-java) 库的 [Spock](https://github.com/spockframework/spock) 扩展，它允许在 Spock 测试中使用 Docker 容器。

## 用法

### `@Testcontainers` 类注解

指定 `@Testcontainers` 注解将指示 Spock 相应地启动和停止所有 testcontainers。该注解可以与 Spock 的 `@Shared` 注解混合使用，以表示容器不应在测试之间重启。

**PostgresContainerIT**

```groovy
@Testcontainers
class PostgresContainerIT extends Specification {

    @Shared
    PostgreSQLContainer postgreSQLContainer = new PostgreSQLContainer(SpockTestImages.POSTGRES_TEST_IMAGE)
    .withDatabaseName("foo")
    .withUsername("foo")
    .withPassword("secret")

    def "waits until postgres accepts jdbc connections"() {

        given: "a jdbc connection"
        HikariConfig hikariConfig = new HikariConfig()
        hikariConfig.setJdbcUrl(postgreSQLContainer.jdbcUrl)
        hikariConfig.setUsername("foo")
        hikariConfig.setPassword("secret")
        HikariDataSource ds = new HikariDataSource(hikariConfig)

        when: "querying the database"
        Statement statement = ds.getConnection().createStatement()
        statement.execute("SELECT 1")
        ResultSet resultSet = statement.getResultSet()
        resultSet.next()

        then: "result is returned"
        int resultSetInt = resultSet.getInt(1)
        resultSetInt == 1

        cleanup:
        ds.close()
    }
}
```

## 将 Testcontainers Spock 支持添加到项目依赖中

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-spock:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-spock</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```

## 致谢

该项目的初始版本深受 [FaustXVI](https://github.com/FaustXVI) 编写的优秀 [JUnit5 docker extension](https://github.com/FaustXVI/junit5-docker) 的启发。
