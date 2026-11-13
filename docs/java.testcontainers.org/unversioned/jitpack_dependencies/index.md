---
source_url: https://java.testcontainers.org/jitpack_dependencies/
source_hash: sha256:ee08080e40d27680016bf9b3336f1eaabaf62da2b8874341f2a711440fa27c11
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# JitPack（未发布版本）

如果你喜欢尝鲜，可以使用 [jitpack.io](https://jitpack.io) 获取 SNAPSHOT 版本。此时请改用下面的依赖描述：

**Gradle**

```groovy
testImplementation "com.github.testcontainers.testcontainers-java:--artifact name--:main-SNAPSHOT"
```

**Maven**

```xml
<dependency>
    <groupId>com.github.testcontainers.testcontainers-java</groupId>
    <artifactId>--artifact name--</artifactId>
    <version>main-SNAPSHOT</version>
</dependency>
```

也可以改用特定的 git 修订版本（例如 `02782d9`）作为固定版本：

**Gradle**

```groovy
testImplementation "com.github.testcontainers.testcontainers-java:--artifact name--:02782d9"
```

**Maven**

```xml
<dependency>
    <groupId>com.github.testcontainers.testcontainers-java</groupId>
    <artifactId>--artifact name--</artifactId>
    <version>02782d9</version>
</dependency>
```

还必须声明 JitPack maven 仓库，例如：

**Gradle**

```groovy
repositories {
    maven {
        url "https://jitpack.io"
    }
}
```

**Maven**

```xml
<repositories>
    <repository>
        <id>jitpack.io</id>
        <url>https://jitpack.io</url>
    </repository>
</repositories>
```
