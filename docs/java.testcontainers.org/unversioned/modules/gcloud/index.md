---
source_url: https://java.testcontainers.org/modules/gcloud/
source_hash: sha256:1f40e4f48d358a86b0bec99a764eefe2c956c94e21f6c79aebef3a608e6adc87
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Google Cloud

> **注意**
>
> 此模块处于孵化阶段（INCUBATING）。虽然它在当前版本的 Testcontainers 中已可用且可正常运行，但未来可能会引入破坏性变更。有关我们孵化模块策略的更多信息，请参阅[贡献指南](../../contributing/index.md#incubating-modules)。

Google Cloud Platform [Cloud SDK](https://cloud.google.com/sdk/) 的 Testcontainers 模块。

目前，该模块支持 `BigQuery`、`Bigtable`、`Datastore`、`Firestore`、`Spanner` 和 `Pub/Sub` 模拟器。要使用它，你应使用以下类：

| 类 | 容器镜像 |
| --- | --- |
| BigQueryEmulatorContainer | [ghcr.io/goccy/bigquery-emulator](https://ghcr.io/goccy/bigquery-emulator) |
| BigtableEmulatorContainer | [gcr.io/google.com/cloudsdktool/google-cloud-cli:emulators](https://gcr.io/google.com/cloudsdktool/google-cloud-cli) |
| DatastoreEmulatorContainer | [gcr.io/google.com/cloudsdktool/google-cloud-cli:emulators](https://gcr.io/google.com/cloudsdktool/google-cloud-cli) |
| FirestoreEmulatorContainer | [gcr.io/google.com/cloudsdktool/google-cloud-cli:emulators](https://gcr.io/google.com/cloudsdktool/google-cloud-cli) |
| SpannerEmulatorContainer | [gcr.io/cloud-spanner-emulator/emulator](https://gcr.io/cloud-spanner-emulator/emulator) |
| PubSubEmulatorContainer | [gcr.io/google.com/cloudsdktool/google-cloud-cli:emulators](https://gcr.io/google.com/cloudsdktool/google-cloud-cli) |

## 使用示例

### BigQuery

在测试期间启动 BigQuery Emulator：

**启动 BigQuery Emulator 容器**

```java
BigQueryEmulatorContainer container = new BigQueryEmulatorContainer("ghcr.io/goccy/bigquery-emulator:0.4.3")
```

**创建 BigQuery 客户端**

```java
String url = container.getEmulatorHttpEndpoint();
BigQueryOptions options = BigQueryOptions
    .newBuilder()
    .setProjectId(container.getProjectId())
    .setHost(url)
    .setLocation(url)
    .setCredentials(NoCredentials.getInstance())
    .build();
BigQuery bigQuery = options.getService();
```

### Bigtable

在测试期间启动 Bigtable Emulator：

**启动 Bigtable Emulator 容器**

```java
BigtableEmulatorContainer emulator = new BigtableEmulatorContainer(
    DockerImageName.parse("gcr.io/google.com/cloudsdktool/google-cloud-cli:583.0.0-emulators")
);
```

在 Emulator 中创建测试用 Bigtable 表：

**创建测试表**

```java
private void createTable(
    TransportChannelProvider channelProvider,
    CredentialsProvider credentialsProvider,
    String tableName
) throws IOException {
    TableAdminRequestContext requestContext = TableAdminRequestContext.create(PROJECT_ID, INSTANCE_ID);
    EnhancedBigtableTableAdminStub stub = EnhancedBigtableTableAdminStub.createEnhanced(
        BigtableTableAdminStubSettings
            .newBuilder()
            .setTransportChannelProvider(channelProvider)
            .setCredentialsProvider(credentialsProvider)
            .build(),
        requestContext
    );

    try (BigtableTableAdminClient client = BigtableTableAdminClient.create(PROJECT_ID, INSTANCE_ID, stub)) {
        Table table = client.createTable(CreateTableRequest.of(tableName).addFamily("name"));
    }
}
```

针对 Emulator 进行测试：

**使用 Bigtable Emulator 容器进行测试**

```java
void testSimple() throws IOException {
    try (
        // emulatorContainer {
        BigtableEmulatorContainer emulator = new BigtableEmulatorContainer(
            DockerImageName.parse("gcr.io/google.com/cloudsdktool/google-cloud-cli:583.0.0-emulators")
        );
        // }
    ) {
        emulator.start();
        ManagedChannel channel = ManagedChannelBuilder
            .forTarget(emulator.getEmulatorEndpoint())
            .usePlaintext()
            .build();

        TransportChannelProvider channelProvider = FixedTransportChannelProvider.create(
            GrpcTransportChannel.create(channel)
        );
        NoCredentialsProvider credentialsProvider = NoCredentialsProvider.create();
        createTable(channelProvider, credentialsProvider, "test-table");
        try (
            BigtableDataClient client = BigtableDataClient.create(
                BigtableDataSettings
                    .newBuilderForEmulator(emulator.getHost(), emulator.getEmulatorPort())
                    .setProjectId(PROJECT_ID)
                    .setInstanceId(INSTANCE_ID)
                    .build()
            )
        ) {
            client.mutateRow(RowMutation.create(TableId.of("test-table"), "1").setCell("name", "firstName", "Ray"));

            Row row = client.readRow(TableId.of("test-table"), "1");
            List<RowCell> cells = row.getCells("name", "firstName");

            assertThat(cells).isNotNull().hasSize(1);
            assertThat(cells.get(0).getValue().toStringUtf8()).isEqualTo("Ray");
        } finally {
            channel.shutdown();
        }
    }
}
```

查看更多示例：

- [完整示例代码](https://github.com/testcontainers/testcontainers-java/tree/main/modules/gcloud/src/test/java/org/testcontainers/gcloud/DatastoreEmulatorContainerTest.java)
- [与 Spring Boot 配合使用](https://github.com/saturnism/testcontainers-gcloud-examples/tree/main/springboot/datastore-example/src/test/java/com/example/springboot/datastore)

### Datastore

在测试期间启动 Datastore Emulator：

**启动 Datastore Emulator 容器**

```java
DatastoreEmulatorContainer emulator = new DatastoreEmulatorContainer(
    DockerImageName.parse("gcr.io/google.com/cloudsdktool/google-cloud-cli:583.0.0-emulators")
);
```

并针对 Emulator 进行测试：

**使用 Datastore Emulator 容器进行测试**

```java
@Test
public void testSimple() {
    try (
        // creatingDatastoreEmulatorContainer {
        DatastoreEmulatorContainer emulator = new DatastoreEmulatorContainer(
            DockerImageName.parse("gcr.io/google.com/cloudsdktool/google-cloud-cli:583.0.0-emulators")
        );
        // }
    ) {
        emulator.start();
        DatastoreOptions options = DatastoreOptions
            .newBuilder()
            .setHost(emulator.getEmulatorEndpoint())
            .setCredentials(NoCredentials.getInstance())
            .setRetrySettings(ServiceOptions.getNoRetrySettings())
            .setProjectId(emulator.getProjectId())
            .build();
        Datastore datastore = options.getService();

        Key key = datastore.newKeyFactory().setKind("Task").newKey("sample");
        Entity entity = Entity.newBuilder(key).set("description", "my description").build();
        datastore.put(entity);

        assertThat(datastore.get(key).getString("description")).isEqualTo("my description");
    }
}
```

查看更多示例：

- [完整示例代码](https://github.com/testcontainers/testcontainers-java/tree/main/modules/gcloud/src/test/java/org/testcontainers/gcloud/DatastoreEmulatorContainerTest.java)
- [与 Spring Boot 配合使用](https://github.com/saturnism/testcontainers-gcloud-examples/tree/main/springboot/datastore-example/src/test/java/com/example/springboot/datastore)

### Firestore

在测试期间启动 Firestore Emulator：

**启动 Firestore Emulator 容器**

```java
FirestoreEmulatorContainer emulator = new FirestoreEmulatorContainer(
    DockerImageName.parse("gcr.io/google.com/cloudsdktool/google-cloud-cli:583.0.0-emulators")
);
```

并针对 Emulator 进行测试：

**使用 Firestore Emulator 容器进行测试**

```java
@Test
void testSimple() throws ExecutionException, InterruptedException {
    try (
        // emulatorContainer {
        FirestoreEmulatorContainer emulator = new FirestoreEmulatorContainer(
            DockerImageName.parse("gcr.io/google.com/cloudsdktool/google-cloud-cli:583.0.0-emulators")
        );
        // }
    ) {
        emulator.start();
        FirestoreOptions options = FirestoreOptions
            .getDefaultInstance()
            .toBuilder()
            .setHost(emulator.getEmulatorEndpoint())
            .setCredentials(NoCredentials.getInstance())
            .setProjectId("test-project")
            .build();
        Firestore firestore = options.getService();

        CollectionReference users = firestore.collection("users");
        DocumentReference docRef = users.document("alovelace");
        Map<String, Object> data = new HashMap<>();
        data.put("first", "Ada");
        data.put("last", "Lovelace");
        ApiFuture<WriteResult> result = docRef.set(data);
        result.get();

        ApiFuture<QuerySnapshot> query = users.get();
        QuerySnapshot querySnapshot = query.get();

        assertThat(querySnapshot.getDocuments().get(0).getData()).containsEntry("first", "Ada");
    }
}
```

查看更多示例：

- [完整示例代码](https://github.com/testcontainers/testcontainers-java/tree/main/modules/gcloud/src/test/java/org/testcontainers/gcloud/FirestoreEmulatorContainerTest.java)
- [与 Spring Boot 配合使用](https://github.com/saturnism/testcontainers-gcloud-examples/tree/main/springboot/firestore-example/src/test/java/com/example/springboot/firestore/FirestoreIntegrationTests.java)

### Spanner

在测试期间启动 Spanner Emulator：

**启动 Spanner Emulator 容器**

```java
SpannerEmulatorContainer emulator = new SpannerEmulatorContainer(
    DockerImageName.parse("gcr.io/cloud-spanner-emulator/emulator:1.4.0")
);
```

在 Emulator 中创建测试用 Spanner 实例：

**创建测试 Spanner 实例**

```java
private InstanceId createInstance(Spanner spanner) throws InterruptedException, ExecutionException {
    InstanceConfigId instanceConfig = InstanceConfigId.of(PROJECT_NAME, "emulator-config");
    InstanceId instanceId = InstanceId.of(PROJECT_NAME, INSTANCE_NAME);
    InstanceAdminClient insAdminClient = spanner.getInstanceAdminClient();
    Instance instance = insAdminClient
        .createInstance(
            InstanceInfo
                .newBuilder(instanceId)
                .setNodeCount(1)
                .setDisplayName("Test instance")
                .setInstanceConfigId(instanceConfig)
                .build()
        )
        .get();
    return instanceId;
}
```

在 Emulator 中创建测试数据库：

**创建测试 Spanner 数据库**

```java
private void createDatabase(Spanner spanner) throws InterruptedException, ExecutionException {
    DatabaseAdminClient dbAdminClient = spanner.getDatabaseAdminClient();
    Database database = dbAdminClient
        .createDatabase(
            INSTANCE_NAME,
            DATABASE_NAME,
            Arrays.asList("CREATE TABLE TestTable (Key INT64, Value STRING(MAX)) PRIMARY KEY (Key)")
        )
        .get();
}
```

并针对 Emulator 进行测试：

**使用 Spanner Emulator 容器进行测试**

```java
@Test
void testSimple() throws ExecutionException, InterruptedException {
    try (
        // emulatorContainer {
        SpannerEmulatorContainer emulator = new SpannerEmulatorContainer(
            DockerImageName.parse("gcr.io/cloud-spanner-emulator/emulator:1.4.0")
        );
        // }
    ) {
        emulator.start();
        SpannerOptions options = SpannerOptions
            .newBuilder()
            .setEmulatorHost(emulator.getEmulatorGrpcEndpoint())
            .setCredentials(NoCredentials.getInstance())
            .setProjectId(PROJECT_NAME)
            .build();

        Spanner spanner = options.getService();

        InstanceId instanceId = createInstance(spanner);

        createDatabase(spanner);

        DatabaseId databaseId = DatabaseId.of(instanceId, DATABASE_NAME);
        DatabaseClient dbClient = spanner.getDatabaseClient(databaseId);
        dbClient
            .readWriteTransaction()
            .run(tx -> {
                String sql1 = "Delete from TestTable where 1=1";
                tx.executeUpdate(Statement.of(sql1));
                String sql = "INSERT INTO TestTable (Key, Value) VALUES (1, 'Java'), (2, 'Go')";
                tx.executeUpdate(Statement.of(sql));
                return null;
            });

        ResultSet resultSet = dbClient
            .readOnlyTransaction()
            .executeQuery(Statement.of("select * from TestTable order by Key"));
        resultSet.next();
        assertThat(resultSet.getLong(0)).isEqualTo(1);
        assertThat(resultSet.getString(1)).isEqualTo("Java");
    }
}
```

查看更多示例：

- [完整示例代码](https://github.com/testcontainers/testcontainers-java/tree/main/modules/gcloud/src/test/java/org/testcontainers/gcloud/SpannerEmulatorContainerTest.java)
- [与 Spring Boot 配合使用](https://github.com/saturnism/testcontainers-gcloud-examples/tree/main/springboot/spanner-example/src/test/java/com/example/springboot/spanner/SpannerIntegrationTests.java)

### Pub/Sub

在测试期间启动 Pub/Sub Emulator：

**启动 Pub/Sub Emulator 容器**

```java
PubSubEmulatorContainer emulator = new PubSubEmulatorContainer(
    DockerImageName.parse("gcr.io/google.com/cloudsdktool/google-cloud-cli:583.0.0-emulators")
);
```

在 Emulator 中创建测试用 Pub/Sub topic：

**创建测试 topic**

```java
private void createTopic(
    String topicId,
    TransportChannelProvider channelProvider,
    NoCredentialsProvider credentialsProvider
) throws IOException {
    TopicAdminSettings topicAdminSettings = TopicAdminSettings
        .newBuilder()
        .setTransportChannelProvider(channelProvider)
        .setCredentialsProvider(credentialsProvider)
        .build();
    try (TopicAdminClient topicAdminClient = TopicAdminClient.create(topicAdminSettings)) {
        TopicName topicName = TopicName.of(PROJECT_ID, topicId);
        topicAdminClient.createTopic(topicName);
    }
}
```

在 Emulator 中创建测试用 Pub/Sub subscription：

**创建测试 subscription**

```java
private void createSubscription(
    String subscriptionId,
    String topicId,
    TransportChannelProvider channelProvider,
    NoCredentialsProvider credentialsProvider
) throws IOException {
    SubscriptionAdminSettings subscriptionAdminSettings = SubscriptionAdminSettings
        .newBuilder()
        .setTransportChannelProvider(channelProvider)
        .setCredentialsProvider(credentialsProvider)
        .build();
    SubscriptionAdminClient subscriptionAdminClient = SubscriptionAdminClient.create(subscriptionAdminSettings);
    SubscriptionName subscriptionName = SubscriptionName.of(PROJECT_ID, subscriptionId);
    subscriptionAdminClient.createSubscription(
        subscriptionName,
        TopicName.of(PROJECT_ID, topicId),
        PushConfig.getDefaultInstance(),
        10
    );
}
```

并针对 Emulator 进行测试：

**使用 Pub/Sub Emulator 容器进行测试**

```java
void testSimple() throws IOException {
    try (
        // emulatorContainer {
        PubSubEmulatorContainer emulator = new PubSubEmulatorContainer(
            DockerImageName.parse("gcr.io/google.com/cloudsdktool/google-cloud-cli:583.0.0-emulators")
        );
        // }
    ) {
        emulator.start();
        String hostport = emulator.getEmulatorEndpoint();
        ManagedChannel channel = ManagedChannelBuilder.forTarget(hostport).usePlaintext().build();
        try {
            TransportChannelProvider channelProvider = FixedTransportChannelProvider.create(
                GrpcTransportChannel.create(channel)
            );
            NoCredentialsProvider credentialsProvider = NoCredentialsProvider.create();

            String topicId = "my-topic-id";
            createTopic(topicId, channelProvider, credentialsProvider);

            String subscriptionId = "my-subscription-id";
            createSubscription(subscriptionId, topicId, channelProvider, credentialsProvider);

            Publisher publisher = Publisher
                .newBuilder(TopicName.of(PROJECT_ID, topicId))
                .setChannelProvider(channelProvider)
                .setCredentialsProvider(credentialsProvider)
                .build();
            PubsubMessage message = PubsubMessage
                .newBuilder()
                .setData(ByteString.copyFromUtf8("test message"))
                .build();
            publisher.publish(message);

            SubscriberStubSettings subscriberStubSettings = SubscriberStubSettings
                .newBuilder()
                .setTransportChannelProvider(channelProvider)
                .setCredentialsProvider(credentialsProvider)
                .build();
            try (SubscriberStub subscriber = GrpcSubscriberStub.create(subscriberStubSettings)) {
                PullRequest pullRequest = PullRequest
                    .newBuilder()
                    .setMaxMessages(1)
                    .setSubscription(ProjectSubscriptionName.format(PROJECT_ID, subscriptionId))
                    .build();
                PullResponse pullResponse = subscriber.pullCallable().call(pullRequest);

                assertThat(pullResponse.getReceivedMessagesList()).hasSize(1);
                assertThat(pullResponse.getReceivedMessages(0).getMessage().getData().toStringUtf8())
                    .isEqualTo("test message");
            }
        } finally {
            channel.shutdown();
        }
    }
}
```

查看更多示例：

- [完整示例代码](https://github.com/testcontainers/testcontainers-java/tree/main/modules/gcloud/src/test/java/org/testcontainers/gcloud/PubSubEmulatorContainerTest.java)
- [与 Spring Boot 配合使用](https://github.com/saturnism/testcontainers-gcloud-examples/tree/main/springboot/pubsub-example/src/test/java/com/example/springboot/pubsub/PubSubIntegrationTests.java)

## 将此模块添加到项目依赖

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-gcloud:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-gcloud</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
