---
source_url: https://java.testcontainers.org/modules/databases/presto/
source_hash: sha256:6881096f5bcfc5b51f0b2491d01eec3dc9b841733433ff108896b206b58b0e0c
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Presto 模块

> **Note**
>
> 该模块已弃用，请改用 Trino 模块。

有关所有数据库容器类型通用的文档和用法，请参阅[数据库容器](../index.md)。

## 使用示例

在测试中将 Presto 作为替代数据库运行：

```java
public class SomeTest {

    @Rule
    public PrestoContainer presto = new PrestoContainer();

    @Test
    public void someTestMethod() {
        String url = presto.getJdbcUrl();

        ... create a connection and run test as normal
```

Presto 预配置了多个 catalog。对测试最有用的是：

- `tpch` catalog，使用 [Presto TPCH Connector](https://prestosql.io/docs/current/connector/tpch.html)。这是一个只读 catalog，定义了标准 TPCH 模式，因此无需创建任何表即可直接查询。
- `memory` catalog，使用 [Presto Memory Connector](https://prestosql.io/docs/current/connector/memory.html)。该 catalog 可用于创建 schema 和表，不需要任何存储，因为所有内容都完全保存在内存中。

使用 `tpch` 和 `memory` catalog 的示例测试：

```java
public class SomeTest {
    @Rule
    public PrestoContainer prestoSql = new PrestoContainer();

    @Test
    public void queryMemoryAndTpchConnectors() throws SQLException {
        try (Connection connection = prestoSql.createConnection();
             Statement statement = connection.createStatement()) {
            // Prepare data
            statement.execute("CREATE TABLE memory.default.table_with_array AS SELECT 1 id, ARRAY[1, 42, 2, 42, 4, 42] my_array");

            // Query Presto using newly created table and a builtin connector
            try (ResultSet resultSet = statement.executeQuery("" +
                "SELECT nationkey, element " +
                "FROM tpch.tiny.nation " +
                "JOIN memory.default.table_with_array twa ON nationkey = twa.id " +
                "LEFT JOIN UNNEST(my_array) a(element) ON true " +
                "ORDER BY element OFFSET 1 FETCH NEXT 3 ROWS WITH TIES ")) {
                List<Integer> actualElements = new ArrayList<>();
                while (resultSet.next()) {
                    actualElements.add(resultSet.getInt("element"));
                }
                Assert.assertEquals(Arrays.asList(2, 4, 42, 42, 42), actualElements);
            }
        }
    }
}
```

## 将此模块添加到项目依赖中

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-presto:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-presto</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```

> **Hint**
>
> 添加这个 Testcontainers 库 JAR 不会自动为你的项目添加 Presto JDBC 驱动 JAR。如果你计划使用它，应确保项目中包含 Presto JDBC 驱动作为依赖。有关说明，请参阅 [Presto 项目下载页面](https://prestosql.io/download.html)。
