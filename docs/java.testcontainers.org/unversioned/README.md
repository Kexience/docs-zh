---
source_url: https://java.testcontainers.org/
source_hash: sha256:66e0191d946ed0ba73c1b847c6b3620016223f1963b05d4a40f76347e43159b7
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Testcontainers for Java

**不用 Java？还有其他受支持的语言！**

![](https://java.testcontainers.org/language-logos/java.svg)Java

[![](https://java.testcontainers.org/language-logos/go.svg)Go](https://golang.testcontainers.org/)

[![](https://java.testcontainers.org/language-logos/dotnet.svg).NET](https://dotnet.testcontainers.org/)

[![](https://java.testcontainers.org/language-logos/nodejs.svg)Node.js](https://node.testcontainers.org/)

[![](https://java.testcontainers.org/language-logos/python.svg)Python](https://testcontainers-python.readthedocs.io/en/latest/)

[![](https://java.testcontainers.org/language-logos/rust.svg)Rust](https://docs.rs/testcontainers/latest/testcontainers/)

[![](https://java.testcontainers.org/language-logos/haskell.svg)Haskell](https://github.com/testcontainers/testcontainers-hs/)

[![](https://java.testcontainers.org/language-logos/ruby.svg)Ruby](https://github.com/testcontainers/testcontainers-ruby/)

## 关于 Testcontainers for Java

*Testcontainers for Java* 是一个支持 JUnit 测试的 Java 库，为常见数据库、Selenium 浏览器或任何其他能在 Docker 容器中运行的软件提供轻量级、用完即弃的实例。

Testcontainers 让以下几类测试更容易编写：

- **数据访问层集成测试**：使用 MySQL、PostgreSQL 或 Oracle 数据库的容器化实例来充分验证数据访问层代码的兼容性，无需在开发者的机器上做复杂配置，并且可以确信测试总是从已知的数据库状态开始。任何能够容器化的数据库类型都可以使用。
- **应用集成测试**：以短生命周期的测试模式运行你的应用，并接入数据库、消息队列或 Web 服务器等依赖。
- **UI/验收测试**：使用与 Selenium 兼容的[容器化浏览器](./modules/webdriver_containers/index.md)来执行自动化 UI 测试。每个测试都能获得全新的浏览器实例，无需担心浏览器状态、插件差异或浏览器自动升级。你还会得到每个测试会话的视频录像，或者只录制测试失败的会话。
- **还有更多！** 看看各种社区贡献的模块，或者以 [`GenericContainer`](./features/creating_container/index.md) 为基础创建你自己的自定义容器类。

## 前置条件

- Docker - 参见[常规 Docker 环境要求](./supported_docker_environment/index.md)
- 一个受支持的 JVM 测试框架：
  - [JUnit 4](./test_framework_integration/junit_4/index.md) - 参见 [JUnit 4 快速入门指南](./quickstart/junit_4_quickstart/index.md)
  - [Jupiter/JUnit 5](./test_framework_integration/junit_5/index.md)
  - [Spock](./test_framework_integration/spock/index.md)
  - *或者*手动添加代码来控制容器/测试的生命周期（参见[这种方式的使用提示](./test_framework_integration/junit_4/index.md#manually-controlling-container-lifecycle)）

## Maven 依赖

Testcontainers 以多个独立的 JAR 包分发，共用一个版本号：

- 一个核心 JAR 包，包含核心功能、通用容器（generic containers）和 docker-compose 支持
- 每个专用模块各有一个独立的 JAR 包。每个模块的文档都说明了需要添加到项目构建中的 Maven/Gradle 依赖。

对于核心库，最新的 Maven/Gradle 依赖如下：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```

你也可以[查看 Maven Central 上可用的最新版本](https://search.maven.org/#search%7Cga%7C1%7Cg%3A%22org.testcontainers%22)。

### 管理多个 Testcontainers 依赖的版本

为了避免为每个依赖指定版本，你可以使用 `BOM`（Bill Of Materials，物料清单）。

使用 Maven 时，可以将以下内容添加到 `pom.xml` 的 `dependencyManagement` 部分：

**Maven**

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.testcontainers</groupId>
            <artifactId>testcontainers-bom</artifactId>
            <version>2.0.5</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

随后即可在不指定版本号的情况下使用依赖：

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-mysql</artifactId>
    <scope>test</scope>
</dependency>
```

使用 Gradle 5.0 或更高版本时，可以将以下内容添加到 `build.gradle` 的 `dependencies` 部分：

**Gradle**

```groovy
implementation platform('org.testcontainers:testcontainers-bom:2.0.5') //import bom
testImplementation('org.testcontainers:testcontainers-mysql') //no version specified
```

预发布版本可通过 [JitPack](./jitpack_dependencies/index.md) 构建获得。

> **Shaded 依赖**
>
> Testcontainers 依赖其他库（如 docker-java）才能工作。
>  其中一些（JUnit、docker-java-{api,transport} 及其传递依赖、JNA、visible-assertions 等）属于我们的公共 API 的一部分。
>  但也有一些"私有"的实现细节依赖（例如 docker-java-core、Guava、OkHttp 等），它们不对公共 API 暴露，却容易与测试代码/被测应用代码发生冲突。因此，**这些库会被 "shaded" 到核心 Testcontainers JAR 中**，并重定位到 `org.testcontainers.shaded` 之下，以避免类冲突。

## 赞助商

衷心感谢我们的赞助商：

### 青铜赞助商

[ ![](https://java.testcontainers.org/sponsor_logos/cirrus_labs.jpg) Cirrus CI  由 fkorotkov 赞助  ](https://cirrus-ci.org/)

[ ![](https://java.testcontainers.org/sponsor_logos/vivy.png) Vivy ](https://vivy.com)

[ ![](https://java.testcontainers.org/sponsor_logos/jooq.jpg) jOOQ ](https://www.jooq.org/)

[ ![](https://java.testcontainers.org/sponsor_logos/backbase.png) Backbase ](https://www.backbase.com/)

[ ![](https://java.testcontainers.org/sponsor_logos/elastic.png) Elastic ](https://www.elastic.co/)

### 捐赠者

[ ![](https://java.testcontainers.org/sponsor_logos/red_hat.png) Red Hat ](https://www.redhat.com)

[ ![](https://java.testcontainers.org/sponsor_logos/spotify.png) Spotify ](https://www.spotify.com)

### 支持者

- [Philip Riecks (@rieckpil)](https://github.com/rieckpil)
- [Karl Heinz Marbaise (@khmarbaise)](https://github.com/khmarbaise)
- [Sascha Frinken (@sascha-frinken)](https://github.com/sascha-frinken)
- [Christoph Dreis (@dreis2211)](https://github.com/dreis2211)
- [Nikita Zhevnitskiy (@zhenik)](https://github.com/zhenik)
- [Bas Stoker (@bastoker)](https://github.com/bastoker)
- [Oleg Nenashev (@oleg-nenashev)](https://github.com/oleg-nenashev)
- [Rik Glover (@rikglover)](https://github.com/rikglover)
- [Amitosh Swain Mahapatra (@recrsn)](https://github.com/recrsn)
- [Paris Apostolopoulos](https://opencollective.com/paris-apostolopoulos)

## 谁在使用 Testcontainers？

- [ZeroTurnaround](https://zeroturnaround.com) - 对 Java Agents、微服务、Selenium 浏览器自动化的测试
- [Zipkin](https://zipkin.io) - MySQL 与 Cassandra 测试
- [Apache Gora](https://gora.apache.org) - CouchDB 测试
- [Apache James](https://james.apache.org) - LDAP 与 Cassandra 集成测试
- [StreamSets](https://github.com/streamsets/datacollector) - LDAP、MySQL Vault、MongoDB、Redis 集成测试
- [Playtika](https://github.com/Playtika/testcontainers-spring-boot) - Kafka、Couchbase、MariaDB、Redis、Neo4j、Aerospike、MemSQL
- [JetBrains](https://www.jetbrains.com/) - 针对 HashiCorp Vault 的 TeamCity 插件测试
- [Plumbr](https://plumbr.io) - 数据处理流水线微服务的集成测试
- [Streamlio](https://streaml.io/) - 基于 Apache Pulsar、Apache BookKeeper 和 Apache Heron 的快速数据平台的集成测试与混沌测试。
- [Spring Session](https://projects.spring.io/spring-session/) - Redis、PostgreSQL、MySQL 与 MariaDB 集成测试
- [Apache Camel](https://camel.apache.org) - 使用 Consul、Etcd 等原生服务测试 Camel
- [Infinispan](https://infinispan.org) - 测试 Infinispan Server，以及与数据库、LDAP 和 KeyCloak 的集成测试
- [Instana](https://www.instana.com) - 测试 agent 与流处理后端
- [eBay Marketing](https://www.ebay.com) - 针对 MySQL、Cassandra、Redis、Couchbase、Kafka 等的测试。
- [Skyscanner](https://www.skyscanner.net/) - 基于 HTTP 服务 mock 和各类数据存储的集成测试
- [Neo4j-OGM](https://neo4j.com/developer/neo4j-ogm/) - 基于 Neo4j 的测试
- [Spring Data Neo4j](https://github.com/spring-projects/spring-data-neo4j/) - 使用 Neo4j 测试命令式与响应式实现
- [Lightbend](https://www.lightbend.com/) - 测试 [Alpakka Kafka](https://doc.akka.io/docs/alpakka-kafka/current/)，并在 [Alpakka Kafka Testkit](https://doc.akka.io/docs/alpakka-kafka/current/testing.html#testing-with-kafka-in-docker) 中提供支持
- [Zalando SE](https://corporate.zalando.com/en) - 核心业务服务的测试
- [Europace AG](https://tech.europace.de/) - 数据库与微服务的集成测试
- [Micronaut Data](https://github.com/micronaut-projects/micronaut-data/) - 测试数据库访问工具包 Micronaut Data JDBC
- [Vert.x SQL Client](https://github.com/eclipse-vertx/vertx-sql-client) - 使用 PostgreSQL、MySQL、MariaDB、SQL Server 等进行测试。
- [JHipster](https://www.jhipster.tech/) - Couchbase 与 Cassandra 集成测试
- [wescale](https://www.wescale.com) - 基于 HTTP 服务 mock 和各类数据存储的集成测试
- [Marquez](https://marquezproject.github.io/marquez) - PostgreSQL 集成测试
- [Wise（原 TransferWise）](https://wise.com) - 针对不同 RDBMS、Kafka 和微服务的集成测试
- [XWiki](https://xwiki.org) - 在所有[受支持的配置](https://dev.xwiki.org/xwiki/bin/view/Community/SupportStrategy/)下[测试 XWiki](https://dev.xwiki.org/xwiki/bin/view/Community/Testing/DockerTesting/)
- [Apache SkyWalking](https://github.com/apache/skywalking) - 对 Apache SkyWalking 进行端到端测试，并对其子项目 [Apache SkyWalking Python](https://github.com/apache/skywalking-python) 及其社区构建的生态系统（如 [SkyAPM NodeJS Agent](https://github.com/SkyAPM/nodejs)）进行插件测试
- [jOOQ](https://www.jooq.org) - 使用多种 RDBMS 对 jOOQ 进行集成测试
- [Trino（原 Presto SQL）](https://trino.io) - 对 Trino 核心及所有连接器进行集成测试，包括多节点部署和安全配置的测试。
- Google - 多个开源项目：[OpenTelemetry](https://github.com/GoogleCloudPlatform/opentelemetry-operations-java)、[Universal Application Tool](https://github.com/seattle-uat/universal-application-tool)、[CloudBowl](https://github.com/GoogleCloudPlatform/cloudbowl-microservice-game)
- [Backbase](https://www.backbase.com/) - 针对所支持的各种数据库（Oracle、SQL Server、MySQL）、各类消息系统（Kafka、Rabbit、AMQ）以及其他微服务和 HTTP mock 的单元测试、集成测试与验收测试。
- [CloudBees](https://www.cloudbees.com/) - 产品的集成测试，其中包括但不限于数据库以及 AWS/Localstack 的集成测试。
- [Jenkins](https://www.jenkins.io/) - 对多个插件以及由 Jenkins 社区维护的 Trilead SSH2 分支进行集成测试（[查询](https://github.com/search?l=Maven+POM&q=org%3Ajenkinsci+testcontainers&type=Code)）。
- [Elastic](https://www.elastic.co) - Java APM agent 的集成测试
- [Alkira](https://www.alkira.com/) - 使用 Kafka、PostgreSQL、Apache Zookeeper、Etcd 等测试多个微服务。
- [Togglz](https://www.togglz.org/) - 面向 Java 平台的功能开关
- [Byzer](https://www.byzer.org/home) - 基于 Byzer、Ray 和 Apache Spark 多个版本的数据与 AI 平台集成测试。
- [Apache SeaTunnel](https://github.com/apache/incubator-seatunnel) - 与不同数据源的集成测试。
- [Bucket4j](https://github.com/bucket4j/bucket4j) - 基于令牌桶算法的 Java 限流库。
- [Spark ClickHouse Connector](https://github.com/housepower/spark-clickhouse-connector) - Apache Spark 分别与单节点 ClickHouse 实例和多节点 ClickHouse 集群的集成测试。
- [Quarkus](https://github.com/quarkusio/quarkus) - Quarkus 的 [DevServices](https://quarkus.io/guides/dev-services) 功能广泛使用了 Testcontainers。
- [Apache Kyuubi](https://kyuubi.apache.org) - 与 Trino（作为数据源引擎）、Kafka 等的集成测试。
- [Dash0](https://www.dash0.com) - OpenTelemetry 可观测性产品的集成测试。

## 许可证

参见 [LICENSE](https://raw.githubusercontent.com/testcontainers/testcontainers-java/main/LICENSE)。

## 来源与致谢

本项目包含一个取自 Spring JDBC 项目的修改版类（ScriptUtils），依据 Apache 许可证条款进行了改编。该类的版权仍归原作者所有。

本项目最初的灵感来自 [Moshe Eshel](https://github.com/mosheeshel) 的这段 [gist](https://gist.github.com/mosheeshel/c427b43c36b256731a0b)。

## 版权

版权所有 (c) 2015-2021 Richard North 及其他作者。

贡献者名单见 [AUTHORS](https://raw.githubusercontent.com/testcontainers/testcontainers-java/main/AUTHORS)。

## 文档索引

- [Testcontainers for Java](./README.md)

### 快速入门

- [JUnit 4 快速入门](./quickstart/junit_4_quickstart/index.md)
- [JUnit 5 快速入门](./quickstart/junit_5_quickstart/index.md)
- [Spock 快速入门](./quickstart/spock_quickstart/index.md)

### 功能

- [高级选项](./features/advanced_options/index.md)
- [执行命令](./features/commands/index.md)
- [自定义配置](./features/configuration/index.md)
- [访问容器日志](./features/container_logs/index.md)
- [创建容器](./features/creating_container/index.md)
- [即时创建镜像](./features/creating_images/index.md)
- [文件与卷](./features/files/index.md)
- [镜像名替换](./features/image_name_substitution/index.md)
- [使用 Jib](./features/jib/index.md)
- [网络与容器通信](./features/networking/index.md)
- [可复用容器（实验性）](./features/reuse/index.md)
- [启动与等待](./features/startup_and_waits/index.md)

### 模块

- [ActiveMQ](./modules/activemq/index.md)
- [Azure](./modules/azure/index.md)
- [ChromaDB](./modules/chromadb/index.md)
- [Consul](./modules/consul/index.md)
- [Cassandra](./modules/databases/cassandra/index.md)
- [ClickHouse](./modules/databases/clickhouse/index.md)
- [CockroachDB](./modules/databases/cockroachdb/index.md)
- [Couchbase](./modules/databases/couchbase/index.md)
- [CrateDB](./modules/databases/cratedb/index.md)
- [[Databend](https://hub.docker.com/r/datafuselabs/databend) 的 Testcontainers 模块](./modules/databases/databend/index.md)
- [[DB2](https://www.ibm.com/docs/en/db2/11.5.x?topic=deployments-db2-community-edition-docker) 的 Testcontainers 模块](./modules/databases/db2/index.md)
- [数据库容器](./modules/databases/index.md)
- [InfluxData [InfluxDB](https://www.influxdata.com/products/influxdb/) 的 Testcontainers 模块](./modules/databases/influxdb/index.md)
- [JDBC 数据库容器](./modules/databases/jdbc/index.md)
- [[MariaDB](https://hub.docker.com/_/mariadb) 的 Testcontainers 模块](./modules/databases/mariadb/index.md)
- [MongoDB 模块](./modules/databases/mongodb/index.md)
- [MS SQL Server 模块](./modules/databases/mssqlserver/index.md)
- [MySQL 模块](./modules/databases/mysql/index.md)
- [Neo4j 模块](./modules/databases/neo4j/index.md)
- [OceanBase 模块](./modules/databases/oceanbase/index.md)
- [Oracle Free 模块](./modules/databases/oraclefree/index.md)
- [Oracle XE 模块](./modules/databases/oraclexe/index.md)
- [OrientDB 模块](./modules/databases/orientdb/index.md)
- [PostgreSQL 模块](./modules/databases/postgres/index.md)
- [Presto 模块](./modules/databases/presto/index.md)
- [QuestDB 模块](./modules/databases/questdb/index.md)
- [R2DBC 支持](./modules/databases/r2dbc/index.md)
- [ScyllaDB](./modules/databases/scylladb/index.md)
- [TiDB 模块](./modules/databases/tidb/index.md)
- [Timeplus 模块](./modules/databases/timeplus/index.md)
- [Trino 模块](./modules/databases/trino/index.md)
- [YugabyteDB 模块](./modules/databases/yugabytedb/index.md)
- [Docker Compose](./modules/docker_compose/index.md)
- [Docker MCP Gateway](./modules/docker_mcp_gateway/index.md)
- [Docker Model Runner](./modules/docker_model_runner/index.md)
- [Elasticsearch](./modules/elasticsearch/index.md)
- [Google Cloud](./modules/gcloud/index.md)
- [Grafana OTel LGTM](./modules/grafana/index.md)
- [HiveMQ](./modules/hivemq/index.md)
- [K3s](./modules/k3s/index.md)
- [k6](./modules/k6/index.md)
- [Kafka](./modules/kafka/index.md)
- [LLDAP](./modules/ldap/index.md)
- [LocalStack](./modules/localstack/index.md)
- [Milvus](./modules/milvus/index.md)
- [MinIO](./modules/minio/index.md)
- [MockServer](./modules/mockserver/index.md)
- [Nginx](./modules/nginx/index.md)
- [Ollama](./modules/ollama/index.md)
- [OpenFGA](./modules/openfga/index.md)
- [Pinecone 模块](./modules/pinecone/index.md)
- [Pulsar 模块](./modules/pulsar/index.md)
- [Qdrant 模块](./modules/qdrant/index.md)
- [RabbitMQ 模块](./modules/rabbitmq/index.md)
- [Redpanda 模块](./modules/redpanda/index.md)
- [Solace 模块](./modules/solace/index.md)
- [Solr 模块](./modules/solr/index.md)
- [Toxiproxy 模块](./modules/toxiproxy/index.md)
- [Typesense 模块](./modules/typesense/index.md)
- [Vault 模块](./modules/vault/index.md)
- [Weaviate 模块](./modules/weaviate/index.md)
- [WebDriver 容器模块](./modules/webdriver_containers/index.md)

### 测试框架集成

- [外部集成](./test_framework_integration/external/index.md)
- [JUnit 4](./test_framework_integration/junit_4/index.md)
- [Jupiter / JUnit 5](./test_framework_integration/junit_5/index.md)
- [手动控制容器生命周期](./test_framework_integration/manual_lifecycle_control/index.md)
- [Spock](./test_framework_integration/spock/index.md)

### 示例

- [示例](./examples/index.md)

### 系统要求与环境

- [AWS CodeBuild](./supported_docker_environment/continuous_integration/aws_codebuild/index.md)
- [Bitbucket Pipelines](./supported_docker_environment/continuous_integration/bitbucket_pipelines/index.md)
- [CircleCI](./supported_docker_environment/continuous_integration/circle_ci/index.md)
- [Concourse CI](./supported_docker_environment/continuous_integration/concourse_ci/index.md)
- [Docker-in-Docker 与 Docker wormhole 模式](./supported_docker_environment/continuous_integration/dind_patterns/index.md)
- [Drone CI](./supported_docker_environment/continuous_integration/drone/index.md)
- [GitLab CI](./supported_docker_environment/continuous_integration/gitlab_ci/index.md)
- [Tekton](./supported_docker_environment/continuous_integration/tekton/index.md)
- [TravisCI](./supported_docker_environment/continuous_integration/travis/index.md)
- [镜像仓库速率限制](./supported_docker_environment/image_registry_rate_limiting/index.md)
- [支持的 Docker 环境](./supported_docker_environment/index.md)
- [日志配置](./supported_docker_environment/logging_config/index.md)
- [Windows](./supported_docker_environment/windows/index.md)

### 其他

- [参与贡献](./contributing/index.md)
- [文档贡献指南](./contributing_docs/index.md)
- [解决无法发现受支持的容器运行时环境的问题](./error_missing_container_runtime_environment/index.md)
- [获取帮助](./getting_help/index.md)
- [JitPack（未发布版本）](./jitpack_dependencies/index.md)
