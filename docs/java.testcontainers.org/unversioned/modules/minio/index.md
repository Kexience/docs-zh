---
source_url: https://java.testcontainers.org/modules/minio/
source_hash: sha256:6b035daabed761a211bce38f34ebe0078c34a2af678eb71e3336bf1231787bd4
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# MinIO

Testcontainers 可用于自动实例化和管理 [MinIO](https://min.io) 容器。

> **注意**
>

> 上游 MinIO 在 2025 年末停止发布免费的社区构建版本，并于 2026 年归档了 [minio/minio](https://github.com/minio/minio) 仓库；`minio/minio` 镜像已不再在 Docker Hub 上提供。因此，该模块现在也支持 [Silo](https://github.com/pgsty/silo)（`pgsty/silo`），这是由 [Pigsty](https://pigsty.io) 项目维护的、采用 AGPL 许可证的 MinIO 社区分支，下文示例中使用的即为该镜像。有关该分支的背景信息，请参阅 [Silo 宣言](https://silo.pigsty.io/about/manifesto/)。

## 使用示例

创建一个 `MinIOContainer` 以在测试中使用：

**启动 MinIO 容器**

```java
MinIOContainer container = new MinIOContainer("pgsty/silo:RELEASE.2026-09-16T00-00-00Z");
```

可以按如下方式使用该容器配置 [MinIO Java 客户端](https://min.io/docs/minio/linux/developers/java/API.html)：

**配置 MinIO 客户端**

```java
MinioClient minioClient = MinioClient
    .builder()
    .endpoint(container.getS3URL())
    .credentials(container.getUserName(), container.getPassword())
    .build();
```

如有需要，可以按如下方式覆盖用户名和密码：

**覆盖 MinIO 容器配置**

```java
MinIOContainer container = new MinIOContainer("pgsty/silo:RELEASE.2026-09-16T00-00-00Z")
    .withUserName("testuser")
    .withPassword("testpassword");
```

## 将此模块添加到项目依赖中

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
 testImplementation "org.testcontainers:testcontainers-minio:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-minio</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
