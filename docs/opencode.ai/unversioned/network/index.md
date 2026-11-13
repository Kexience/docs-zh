---
source_url: https://opencode.ai/docs/network/
source_hash: sha256:3d83e9802831cea6b2456a61db2b020b90493688886c517f5dca40d4478c9730
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---
# 网络

设置标准的代理环境变量，并排除回环地址。OpenCode 在 CLI 与其后台服务之间使用本地 HTTP 连接，因此在 CLI 环境中配置了代理时，必须排除回环地址。

```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
export NO_PROXY=localhost,127.0.0.1,::1

opencode
```

`HTTP_PROXY` 处理 HTTP 目标，`HTTPS_PROXY` 处理 HTTPS 目标。这两个变量的代理 URL 本身都可以使用 `http://`。`NO_PROXY` 是一个以逗号分隔的主机和地址列表，这些目标会直接连接而不走代理。

## 后台服务

只有在 shell 中启动后台服务时，shell 导出的环境变量才会生效。请把这些变量持久化到受管服务的配置中，这样以后启动服务时会使用相同的网络设置。

```bash
opencode service set env HTTP_PROXY http://proxy.example.com:8080
opencode service set env HTTPS_PROXY http://proxy.example.com:8080
opencode service set env NO_PROXY localhost,127.0.0.1,::1
opencode service start
```

修改受管环境变量会停止正在运行的服务。`service start` 会以新的环境重新启动服务。当 shell 设置了代理时，也要在这个 shell 中保留 `NO_PROXY`，因为受管服务的变量只作用于服务器进程，不作用于 CLI 进程。

使用 `service unset env` 移除已持久化的变量：

```bash
opencode service unset env HTTPS_PROXY
```

## 身份认证

如果代理接受 URL 凭据，请在每个需要认证的代理 URL 中包含用户名和密码。凭据中的 `@`、`:`、`/` 等字符需要进行百分号编码。

```bash
export HTTPS_PROXY='http://user:p%40ssword@proxy.example.com:8080'
```

对于后台服务，请持久化完整的 URL。该值保存在私有的服务配置中，并会通过 `opencode service get env` 显示，因此不要把这个输出分享出去。

```bash
opencode service set env HTTPS_PROXY 'http://user:p%40ssword@proxy.example.com:8080'
```

## 证书

当代理或目标使用的证书由私有证书颁发机构签署时，请将 `NODE_EXTRA_CA_CERTS` 设置为一个 PEM 文件。进程启动时，这些额外的证书颁发机构会被加入运行时的信任库。

```bash
export NODE_EXTRA_CA_CERTS=/etc/company/ca.pem
opencode --standalone
```

为后台服务持久化该文件路径，然后重启服务：

```bash
opencode service set env NODE_EXTRA_CA_CERTS /etc/company/ca.pem
opencode service start
```

## 杀毒软件与 HTTPS 检查

杀毒软件的"HTTPS 扫描"或"加密连接扫描"功能（Kaspersky、Avast、ESET 等）以及企业 SSL 检查代理会把服务器的证书替换成自己的证书。OpenCode 会拒绝该证书，请求会失败并报如下错误：

```text
self signed certificate in certificate chain
SELF_SIGNED_CERT_IN_CHAIN
CERT_NOT_YET_VALID
CERT_SIGNATURE_FAILURE
```

可以用以下两种方式之一解决：

- 在杀毒软件设置中将 `opencode.ai` 和 `*.opencode.ai` 排除在 HTTPS 扫描之外。如果你直接连接某个 provider，也请把它的 API 主机加进去，例如 `api.anthropic.com`。
- 将检查用的证书颁发机构导出为 PEM 文件，并通过 `NODE_EXTRA_CA_CERTS` 信任它，方法见[证书](#证书)。

## 前台运行

`--standalone` 和 `serve` 使用各自进程的环境变量，`opencode service set env` 不会作用于这些进程。

```bash
HTTP_PROXY=http://proxy.example.com:8080 \
HTTPS_PROXY=http://proxy.example.com:8080 \
NO_PROXY=localhost,127.0.0.1,::1 \
opencode --standalone
```

对前台运行的服务器也采用同样的方式：

```bash
HTTPS_PROXY=http://proxy.example.com:8080 \
NO_PROXY=localhost,127.0.0.1,::1 \
opencode serve
```

## 验证

应用设置后，检查 CLI 能否连接到后台服务：

```bash
opencode api get /api/info
```

健康检查响应成功即证明本地客户端到服务的连接正常。再发起一次正常的 provider 请求，以验证服务的出站代理和证书链路。
