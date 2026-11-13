---
source_url: https://java.testcontainers.org/modules/databases/mongodb/
source_hash: sha256:f2f0b1d059f9aebec937e3a862b776203ff2d0a466fa0784fa036a0ff206ffdd
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# MongoDB 模块

MongoDB 模块提供了两个用于 MongoDB 单元测试的 Testcontainers：

- [MongoDBContainer](#mongodbcontainer) - 核心 MongoDB 数据库
- [MongoDBAtlasLocalContainer](#mongodbatlaslocalcontainer) - 核心 MongoDB 数据库，并结合 MongoDB Atlas Search + Atlas Vector Search

## MongoDBContainer

### 使用示例

以下示例展示如何创建 MongoDBContainer：

**创建 MongoDB 容器**

```java
MongoDBContainer mongoDBContainer = new MongoDBContainer("mongo:4.0.10").withReplicaSet()
```

以及如何启动它：

**启动 MongoDB 容器**

```java
mongoDBContainer.start();
```

> **注意**
>

> 若要构建多节点 MongoDB 集群，可以考虑使用 [mongodb-replica-set 项目](https://github.com/silaev/mongodb-replica-set/)

#### 动机

实现一个可复用、跨平台、安装简单且不依赖固定端口的方案，用于测试 MongoDB 事务。

#### 概述

从 4 版本开始，MongoDB 仅在副本集（replica set）中支持多文档事务。例如，若要通过 Docker 在固定端口上初始化一个单节点副本集，需要执行以下操作：

- 运行 4 及以上版本的 MongoDB 容器，并指定 --replSet 命令
- 通过执行相应的命令初始化一个单节点副本集
- 等待初始化完成
- 提供一个专用的 url，供用户在 MongoDB 驱动中使用，无需指定 replicaSet

可以看到，需要执行的操作非常多，而我们甚至还没有涉及非固定端口的方案。MongoDBContainer 正是在这种情况下能派上用场。

## MongoDBAtlasLocalContainer

### 使用示例

以下示例展示如何创建 MongoDBAtlasLocalContainer：

**创建 MongoDB Atlas Local 容器**

```java
MongoDBAtlasLocalContainer atlasLocalContainer = new MongoDBAtlasLocalContainer(
    "mongodb/mongodb-atlas-local:7.0.9"
);
```

以及如何启动它：

**启动容器**

```java
atlasLocalContainer.start();
```

MongoDBAtlasLocalContainer 的 getConnectionString() 方法返回的连接字符串中包含动态分配的端口：

**获取连接字符串**

```java
String connectionString = atlasLocalContainer.getConnectionString();
```

例如 `mongodb://localhost:12345/?directConnection=true`

### 参考资料

MongoDB Atlas Local 将 MongoDB 数据库引擎与 MongoT 结合在一起。MongoT 是由 MongoDB 构建的边车进程，为高级搜索能力提供支持，其底层由 [Apache Lucene](https://lucene.apache.org/) 驱动。

该容器（mongodb/mongodb-atlas-local）的文档可[在此查看](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-deploy-docker/)。

有关 Atlas Search 的更多信息可[在此查看](https://www.mongodb.com/docs/atlas/atlas-search/)。

## 将本模块添加到项目依赖中

在你的 `pom.xml`/`build.gradle` 文件中添加以下依赖：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-mongodb:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-mongodb</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```

> **提示**
>

> 添加此 Testcontainers 库 JAR 并不会自动为你的项目添加数据库驱动 JAR。你需要确保项目中还包含合适的数据库驱动作为依赖

#### 版权

版权所有 (c) 2019 Konstantin Silaev [silaev256@gmail.com](mailto:silaev256@gmail.com)
