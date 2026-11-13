---
source_url: https://java.testcontainers.org/modules/localstack/
source_hash: sha256:902093b5f9c18c7f2285537808561598d52613c6610a0d69f38eda0bc62f5ce7
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# LocalStack

用于 [LocalStack](http://localstack.cloud/) 的 Testcontainers 模块。LocalStack 是“一个功能齐全的本地 AWS 云栈”，可让你在不实际使用云服务的情况下开发和测试云及无服务器应用。

## 使用示例

你可以在任何 Java 应用程序中通过以下方式启动 LocalStack 容器实例：

**容器创建**

```java
LocalStackContainer localstack = new LocalStackContainer(LocalstackTestImages.LOCALSTACK_IMAGE)
    .withServices("s3")
```

可以使用 [LocalStack 配置文档](https://docs.localstack.cloud/references/configuration/) 中列出的环境变量来自定义 LocalStack 的配置。在 `LocalStackContainer` 上使用 `.withEnv(key, value)` 方法来应用配置设置。

> **注意**
>

> 从 2026 年 3 月 23 日开始，`localstack/localstack` 需要通过 `LOCALSTACK_AUTH_TOKEN` 环境变量进行身份验证。如果没有该变量，容器将无法启动。
>
> 使用 `.withEnv("LOCALSTACK_AUTH_TOKEN", System.getenv("LOCALSTACK_AUTH_TOKEN"))` 来传递令牌。有关更多详细信息，请参阅 [LocalStack 博客文章](https://blog.localstack.cloud/localstack-single-image-next-steps/)。

## 使用 AWS SDK 创建客户端

**AWS SDK V2**

```java
S3Client s3 = S3Client
    .builder()
    .endpointOverride(localstack.getEndpoint())
    .credentialsProvider(
        StaticCredentialsProvider.create(
            AwsBasicCredentials.create(localstack.getAccessKey(), localstack.getSecretKey())
        )
    )
    .region(Region.of(localstack.getRegion()))
    .build();
```

## 将此模块添加到项目依赖中

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-localstack:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-localstack</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
