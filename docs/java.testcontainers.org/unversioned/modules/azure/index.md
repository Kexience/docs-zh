---
source_url: https://java.testcontainers.org/modules/azure/
source_hash: sha256:56bb8eb062795e46d7356c8a34a829cd16513177ae0bd18f6b06575e5efc70e2
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Azure

> **注意**
>
> 此模块处于孵化阶段（INCUBATING）。虽然它在当前版本的 Testcontainers 中已可用且可正常运行，但未来可能会引入破坏性变更。有关我们孵化模块策略的更多信息，请参阅[贡献指南](../../contributing/index.md#incubating-modules)。

Microsoft Azure [SDK](https://github.com/Azure/azure-sdk-for-java) 的 Testcontainers 模块。

目前，该模块支持 `Azurite`、`Azure Event Hubs`、`Azure Service Bus` 和 `CosmosDB` 模拟器。要使用它们，你应使用以下类：

| 类 | 容器镜像 |
| --- | --- |
| AzuriteContainer | [mcr.microsoft.com/azure-storage/azurite](https://github.com/microsoft/containerregistry) |
| EventHubsEmulatorContainer | [mcr.microsoft.com/azure-messaging/eventhubs-emulator](https://github.com/microsoft/containerregistry) |
| ServiceBusEmulatorContainer | [mcr.microsoft.com/azure-messaging/servicebus-emulator](https://github.com/microsoft/containerregistry) |
| CosmosDBEmulatorContainer | [mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator](https://github.com/microsoft/containerregistry) |

## 使用示例

### Azurite Storage Emulator

在测试期间启动 Azurite Emulator：

**启动 Azurite 容器**

```java
AzuriteContainer emulator = new AzuriteContainer("mcr.microsoft.com/azure-storage/azurite:3.33.0")
```

> **注意**
>
> 可以使用 `withSsl(MountableFile, String)` 和 `withSsl(MountableFile, MountableFile)` 方法进行 SSL 配置。

较新的 Azure Storage SDK 版本可能会发送 Azurite 不支持的 API 版本。可使用 `withCommandOptions(...)` 追加额外的 Azurite 参数，例如 `--skipApiVersionCheck`。`AzuriteContainer` 会在 `configure()` 中重建其进程命令，因此不能使用 `.withCommand(...)` 来添加额外参数。

**传递额外的 Azurite 命令选项**

```java
AzuriteContainer emulator = new AzuriteContainer("mcr.microsoft.com/azure-storage/azurite:3.33.0")
    .withCommandOptions("--skipApiVersionCheck");
```

如果被测应用需要使用多组凭据，可以将容器配置为使用自定义凭据。请参阅下面的一些示例。

**使用一个账户和两个密钥启动 Azurite Blob 容器**

```java
AzuriteContainer emulator = new AzuriteContainer("mcr.microsoft.com/azure-storage/azurite:3.33.0")
    .withEnv("AZURITE_ACCOUNTS", "account1:key1:key2")
```

**使用多个账户和密钥启动 Azurite Blob 容器**

```java
AzuriteContainer emulator = new AzuriteContainer("mcr.microsoft.com/azure-storage/azurite:3.33.0")
    .withEnv("AZURITE_ACCOUNTS", "account1:key1;account2:key2")
```

#### 与 Blob 配合使用

构建 Azure Blob 客户端：

**构建 Azure Blob Service 客户端**

```java
BlobServiceClient blobServiceClient = new BlobServiceClientBuilder()
    .connectionString(container.getConnectionString())
    .buildClient();
```

如果应用需要使用自定义凭据，我们可以通过不同的方法获取它们：

**获取使用非默认凭据的连接字符串**

```java
String connectionString1 = emulator.getConnectionString("account1", "key1");
// the second account will not have access to the same container
String connectionString2 = emulator.getConnectionString("account2", "key2");
```

#### 与 Queue 配合使用

构建 Azure Queue 客户端：

**构建 Azure Queue Service 客户端**

```java
QueueServiceClient queueServiceClient = new QueueServiceClientBuilder()
    .connectionString(container.getConnectionString())
    .buildClient();
```

> **注意**
>
> 我们可以使用与 Blob 部分中定义的相同方式来使用自定义凭据。

#### 与 Table 配合使用

构建 Azure Table 客户端：

**构建 Azure Table Service 客户端**

```java
TableServiceClient tableServiceClient = new TableServiceClientBuilder()
    .connectionString(container.getConnectionString())
    .buildClient();
```

> **注意**
>
> 我们可以使用与 Blob 部分中定义的相同方式来使用自定义凭据。

### Azure Event Hubs Emulator

**配置 Azure Event Hubs Emulator 容器**

```json
{
    "UserConfig": {
        "NamespaceConfig": [
            {
                "Type": "EventHub",
                "Name": "emulatorNs1",
                "Entities": [
                    {
                        "Name": "eh1",
                        "PartitionCount": "1",
                        "ConsumerGroups": [
                            {
                                "Name": "cg1"
                            }
                        ]
                    }
                ]
            }
        ],
        "LoggingConfig": {
            "Type": "File"
        }
    }
}
```

在测试期间启动 Azure Event Hubs Emulator：

**设置网络**

```java
Network network = Network.newNetwork();
```

**启动作为依赖的 Azurite 容器**

```java
AzuriteContainer azuriteContainer = new AzuriteContainer("mcr.microsoft.com/azure-storage/azurite:3.33.0")
    .withNetwork(network);
```

**启动 Azure Event Hubs Emulator 容器**

```java
EventHubsEmulatorContainer emulator = new EventHubsEmulatorContainer(
    "mcr.microsoft.com/azure-messaging/eventhubs-emulator:2.0.1"
)
    .acceptLicense()
    .withNetwork(network)
    .withConfig(MountableFile.forClasspathResource("/eventhubs_config.json"))
    .withAzuriteContainer(azuriteContainer);
```

#### 使用 Azure Event Hubs 客户端

配置 consumer 和 producer 客户端：

**配置客户端**

```java
EventHubProducerClient producer = new EventHubClientBuilder()
    .connectionString(emulator.getConnectionString())
    .fullyQualifiedNamespace("emulatorNs1")
    .eventHubName("eh1")
    .buildProducerClient();
EventHubConsumerClient consumer = new EventHubClientBuilder()
    .connectionString(emulator.getConnectionString())
    .fullyQualifiedNamespace("emulatorNs1")
    .eventHubName("eh1")
    .consumerGroup("cg1")
    .buildConsumerClient();
```

### Azure Service Bus Emulator

**配置 Azure Service Bus Emulator 容器**

```json
{
    "UserConfig": {
        "Namespaces": [
            {
                "Name": "sbemulatorns",
                "Queues": [
                    {
                        "Name": "queue.1",
                        "Properties": {
                            "DeadLetteringOnMessageExpiration": false,
                            "DefaultMessageTimeToLive": "PT1H",
                            "DuplicateDetectionHistoryTimeWindow": "PT20S",
                            "ForwardDeadLetteredMessagesTo": "",
                            "ForwardTo": "",
                            "LockDuration": "PT1M",
                            "MaxDeliveryCount": 3,
                            "RequiresDuplicateDetection": false,
                            "RequiresSession": false
                        }
                    }
                ],
                "Topics": []
            }
        ],
        "Logging": {
            "Type": "File"
        }
    }
}
```

在测试期间启动 Azure Service Bus Emulator：

**设置网络**

```java
Network network = Network.newNetwork();
```

**启动作为依赖的 SQL Server 容器**

```java
MSSQLServerContainer mssqlServerContainer = new MSSQLServerContainer(
    "mcr.microsoft.com/mssql/server:2022-CU14-ubuntu-22.04"
)
    .acceptLicense()
    .withPassword("yourStrong(!)Password")
    .withCreateContainerCmdModifier(cmd -> {
        cmd.getHostConfig().withCapAdd(Capability.SYS_PTRACE);
    })
    .withNetwork(network);
```

**启动 Service Bus Emulator 容器**

```java
ServiceBusEmulatorContainer emulator = new ServiceBusEmulatorContainer(
    "mcr.microsoft.com/azure-messaging/servicebus-emulator:1.1.2"
)
    .acceptLicense()
    .withConfig(MountableFile.forClasspathResource("/service-bus-config.json"))
    .withNetwork(network)
    .withMsSqlServerContainer(mssqlServerContainer);
```

#### 使用 Azure Service Bus 客户端

配置 sender 和 processor 客户端：

**配置 sender 客户端**

```java
ServiceBusSenderClient senderClient = new ServiceBusClientBuilder()
    .connectionString(emulator.getConnectionString())
    .sender()
    .queueName("queue.1")
    .buildClient();
```

**配置 processor 客户端**

```java
ServiceBusProcessorClient processorClient = new ServiceBusClientBuilder()
    .connectionString(emulator.getConnectionString())
    .processor()
    .queueName("queue.1")
    .processMessage(messageConsumer)
    .processError(errorConsumer)
    .buildProcessorClient();
```

### CosmosDB

在测试期间启动 Azure CosmosDB Emulator：

**启动 Azure CosmosDB Emulator 容器**

```java
CosmosDBEmulatorContainer emulator = new CosmosDBEmulatorContainer(
    DockerImageName.parse("mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:latest")
);
```

准备用于 SSL 的 KeyStore。

**从容器内的证书构建 KeyStore**

```java
Path keyStoreFile = tempFolder.resolve("azure-cosmos-emulator.keystore");
KeyStore keyStore = emulator.buildNewKeyStore();
keyStore.store(new FileOutputStream(keyStoreFile.toFile()), emulator.getEmulatorKey().toCharArray());
```

设置系统 trust-store 参数以使用已构建的 KeyStore：

**设置系统 trust-store 参数**

```java
System.setProperty("javax.net.ssl.trustStore", keyStoreFile.toString());
System.setProperty("javax.net.ssl.trustStorePassword", emulator.getEmulatorKey());
System.setProperty("javax.net.ssl.trustStoreType", "PKCS12");
```

构建 Azure CosmosDB 客户端：

**构建 Azure CosmosDB 客户端**

```java
CosmosAsyncClient client = new CosmosClientBuilder()
    .gatewayMode()
    .endpointDiscoveryEnabled(false)
    .endpoint(emulator.getEmulatorEndpoint())
    .key(emulator.getEmulatorKey())
    .buildAsyncClient();
```

针对 Emulator 进行测试：

**针对 Azure CosmosDB Emulator 容器进行测试**

```java
CosmosDatabaseResponse databaseResponse = client.createDatabaseIfNotExists("Azure").block();
assertThat(databaseResponse.getStatusCode()).isEqualTo(201);
CosmosContainerResponse containerResponse = client
    .getDatabase("Azure")
    .createContainerIfNotExists("ServiceContainer", "/name")
    .block();
assertThat(containerResponse.getStatusCode()).isEqualTo(201);
```

## 将此模块添加到项目依赖

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-azure:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-azure</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
