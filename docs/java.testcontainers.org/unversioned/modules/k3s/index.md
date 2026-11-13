---
source_url: https://java.testcontainers.org/modules/k3s/
source_hash: sha256:12fa3222d90c06903c2d3fb2c3940d41a5c2e8f6c4b5295e86eaa8bf73c90591
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# K3s

> **注意**
>

> 此模块处于孵化阶段。虽然它已准备就绪并可在当前版本的 Testcontainers 中正常使用，但未来可能会引入破坏性变更。有关孵化模块策略的更多信息，请参阅[我们的贡献指南](../../contributing/index.md#incubating-modules)。

用于 Rancher [K3s](https://rancher.com/products/k3s/) 轻量级 Kubernetes 的 Testcontainers 模块。此模块旨在用于测试与 Kubernetes API 交互的组件——例如 operator。

## 使用示例

按如下方式启动 K3s 服务器：

**启动 K3S 服务器**

```java
K3sContainer k3s = new K3sContainer(DockerImageName.parse("rancher/k3s:v1.21.3-k3s1"))
    .withLogConsumer(new Slf4jLogConsumer(log))
```

### 连接到服务器

`K3sContainer` 通过 `getKubeConfigYaml()` 方法以 YAML 字符串的形式暴露可用的 Kubernetes 客户端配置。

它可以与 Kubernetes 客户端一起使用——例如[官方 Java 客户端](https://java.testcontainers.org/modules/k3s/connecting_with_k8sio)和 [Fabric8 Kubernetes 客户端](https://github.com/fabric8io/kubernetes-client)：

**官方 Java 客户端**

```java
String kubeConfigYaml = k3s.getKubeConfigYaml();

ApiClient client = Config.fromConfig(new StringReader(kubeConfigYaml));
CoreV1Api api = new CoreV1Api(client);

// interact with the running K3s server, e.g.:
V1NodeList nodes = api.listNode(null, null, null, null, null, null, null, null, null, null, null);
```

**Fabric8 Kubernetes 客户端**

```java
// obtain a kubeconfig file which allows us to connect to k3s
String kubeConfigYaml = k3s.getKubeConfigYaml();

// requires io.fabric8:kubernetes-client:5.11.0 or higher
Config config = Config.fromKubeconfig(kubeConfigYaml);

DefaultKubernetesClient client = new DefaultKubernetesClient(config);

// interact with the running K3s server, e.g.:
List<Node> nodes = client.nodes().list().getItems();
```

## 已知限制

> **警告**
>

> - K3sContainer 以特权容器方式运行，并且需要能够创建自己的容器。出于这些原因，K3sContainer 在某些 rootless Docker、Docker-in-Docker 或其他禁止特权容器的环境中将无法工作。
> - 当主机的 `/var/lib/docker` 位于 BTRFS 文件系统上时，k3s 容器可能无法运行。有关示例，请参阅 [k3s-io/k3s#4863](https://github.com/k3s-io/k3s/issues/4863)。
> - 在尝试使用已配置的 Fabric8 客户端时，你可能会遇到 PKIX 异常。这是由于较新的 k3s 发行版使用了椭圆曲线密钥。可以通过将 [BouncyCastle PKI 库](https://mvnrepository.com/artifact/org.bouncycastle/bcpkix-jdk15on) 添加到 classpath 来解决此问题。

## 将此模块添加到项目依赖中

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-k3s:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-k3s</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
