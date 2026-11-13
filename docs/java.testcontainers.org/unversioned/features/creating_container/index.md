---
source_url: https://java.testcontainers.org/features/creating_container/
source_hash: sha256:c35116e895f41a3cec10ef3d3947847ec0db1e49261350f0256b6e04eac1f4af
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# 创建容器

## 基于镜像创建通用容器

Testcontainers 的通用容器支持提供了最大的灵活性，让你几乎可以把任意容器镜像当作临时测试依赖来使用。例如，你可能会用它来测试与以下组件的交互：

- NoSQL 数据库或其他数据存储（例如 redis、elasticsearch、mongo）
- Web 服务器/代理（例如 nginx、apache）
- 日志服务（例如 logstash、kibana）
- 由你的团队/组织开发并已完成容器化的其他服务

使用通用容器时，你通过规则构造函数的一个参数来设置容器镜像，例如：

```java
new GenericContainer(DockerImageName.parse("jboss/wildfly:9.0.1.Final"))
```

### 指定镜像

Testcontainers 中的许多 Container 类在历史上支持：

- 无参构造函数——例如 `new GenericContainer()` 和 `new ElasticsearchContainer()`。使用这些构造函数时，Testcontainers 传统上会使用默认的镜像名（包括固定的镜像标签/版本）。这导致了一方面需要保持默认值合理（即保持最新），另一方面又需要避免这些依赖随 Testcontainers 的新版本被静默升级，两者之间产生了冲突。
- 单个字符串参数的构造函数，它接受一个版本号或镜像名作为 String。这带来了一定的歧义与困惑。

自 v1.15.0 起，这两种构造函数均已被废弃，原因如上所述。

相反，我们强烈建议使用接受 `DockerImageName` 对象的构造函数来构造*所有容器*。`DockerImageName` 类是对 Docker 镜像的无歧义引用。

建议开发者像对待其他可能成为常量的值那样对待 `DockerImageName`——考虑在测试代码库中定义一个与生产环境所用依赖版本相一致的常量。

### 示例

通用容器规则可用于任意公共 Docker 镜像；例如：

**创建 Redis 容器**

```java
@Container
public GenericContainer redis = new GenericContainer(DockerImageName.parse("redis:6-alpine"))
    .withExposedPorts(6379);
```

该容器作为 `@Container`，会在该类中任何测试运行之前启动，并在所有测试运行完毕后销毁。
