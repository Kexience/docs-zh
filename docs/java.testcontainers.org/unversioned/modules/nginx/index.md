---
source_url: https://java.testcontainers.org/modules/nginx/
source_hash: sha256:96d6d6c08351a95b66f1c6b1f54332a65c2fa82b5b330286d26f768479df732e
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Nginx

Nginx 是一个 Web 服务器、反向代理、邮件代理和 HTTP 缓存。

## 使用示例

以下示例展示了如何启动 Nginx。

**创建 Nginx 容器**

```java
NginxContainer nginx = new NginxContainer(NGINX_IMAGE)
    .withCopyFileToContainer(MountableFile.forHostPath(tmpDirectory), "/usr/share/nginx/html")
    .waitingFor(new HttpWaitStrategy());
```

如何向 Nginx 服务器添加自定义内容。

**创建要提供的静态内容**

```java
// Create a temporary dir
File contentFolder = new File(tmpDirectory);
contentFolder.mkdir();
contentFolder.deleteOnExit();

// And "hello world" HTTP file
File indexFile = new File(contentFolder, "index.html");
indexFile.deleteOnExit();
@Cleanup
PrintStream printStream = new PrintStream(new FileOutputStream(indexFile));
printStream.println("<html><body>Hello World!</body></html>");
```

以及如何向 Nginx 服务器查询所添加的自定义内容。

**创建要提供的静态内容**

```java
URL baseUrl = nginx.getBaseUrl("http", 80);

assertThat(responseFromNginx(baseUrl))
    .as("An HTTP GET from the Nginx server returns the index.html from the custom content directory")
    .contains("Hello World!");
```

## 将此模块添加到项目依赖中

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-nginx:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-nginx</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
