---
source_url: https://java.testcontainers.org/modules/databases/couchbase/
source_hash: sha256:a8e604321e1cba9de488096a1984752c5e2676e18c95ffbc57e6532ef2583514
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Couchbase

![](https://cdn.worldvectorlogo.com/logos/couchbase.svg)

用于 Couchbase 的 Testcontainers 模块。[Couchbase](https://www.couchbase.com/) 是一个面向文档的 NoSQL 数据库。

## 使用示例

在测试中以 Couchbase 作为替身运行：

1. 定义一个 bucket：

   **Bucket 定义**

   ```java
   BucketDefinition bucketDefinition = new BucketDefinition("mybucket");
   ```
2. 定义一个容器：

   **容器定义**

   ```java
   CouchbaseContainer container = new CouchbaseContainer(couchbaseImage).withBucket(bucketDefinition)
   ```
3. 创建一个集群：

   **集群创建**

   ```java
   Cluster cluster = Cluster.connect(
       container.getConnectionString(),
       container.getUsername(),
       container.getPassword()
   );
   ```

## 将本模块添加到项目依赖中

在你的 `pom.xml`/`build.gradle` 文件中添加以下依赖：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-couchbase:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-couchbase</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
