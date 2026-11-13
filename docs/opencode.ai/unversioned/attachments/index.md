---
source_url: https://opencode.ai/docs/attachments/
source_hash: sha256:9102c792d9a9c8cb3762909ad4ed8e6f32623e051cab2f725b23fff01f3c0dd1
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 附件

## 附加文件

附加一个本地文件，然后让 OpenCode 在你的提示词中使用它。在桌面或网页客户端中，选择 **Attach file**、粘贴文件，或把文件拖入提示框。

```text
Summarize the attached README.md and list the required setup steps.
```

桌面端文件选择器的选择总量最多为 20 MiB。其他界面可能会应用更低的客户端限制。

<Callout type="warning">
  在附加图片之前，请选择一个支持图片输入的模型。OpenCode 可以把受支持的图片传递给 provider，但 provider 和模型仍然会强制执行它们自己的格式、尺寸、文件数量和大小限制。纯文本模型可能会拒绝该请求。
</Callout>

## 语法

V2 的提示和命令输入使用 `uri` 以及可选的 `name` 和 `description` 来描述一个附件：

```json
{
  "uri": "file:///home/me/project/src/server.ts",
  "name": "server.ts",
  "description": "HTTP server entrypoint"
}
```

对服务器可访问的文件或目录，使用绝对 `file:` URL。对于文本文件，正数的 `start` 和 `end` 参数按 1 起始的行号选择行。

```text
file:///home/me/project/src/server.ts?start=20&end=60
```

使用 `data:` URL 可以内联发送内容：

```json
{
  "uri": "data:text/plain;base64,SGVsbG8sIE9wZW5Db2RlIQ==",
  "name": "greeting.txt"
}
```

不支持 HTTP 和 HTTPS 附件 URL。关于以编程方式提交提示，参见生成的 [API 参考](../api/index.md)。

## 格式

当前的 V2 会话会把以下附件类型呈现给模型：

| 输入 | 模型收到 | 示例 |
| ----------------------- | -------------------------------------------------------- | ------------------ |
| UTF-8 文本文件 | 文件名和解码后的文本 | `README.md` |
| 目录 | 直接文件和目录的非递归列表 | `file:///home/me/` |
| PNG、JPEG、GIF 或 WebP | 图片媒体 | `diagram.png` |
| PDF | 文档媒体 | `report.pdf` |

PDF 需要一个支持 PDF 输入的模型。如果模型不支持某个附件的类型，OpenCode 会发送一条简短的说明代替它。

SVG 被视为文本。AVIF、BMP、音频、视频以及其他二进制提示附件不会包含在模型请求中。请先把不受支持的二进制转换为文本或受支持的图片；例如，附加 BMP 图片之前先把它转换为 PNG。

OpenCode 在接收提示之前会读取每个附件。无效的 URL、不可读取的路径、非文件或目录的路径，以及解码后超过 20 MiB 的附件都会被拒绝。媒体类型是从字节中检测的，因此更改文件名或 `data:` URL 的媒体类型不会让不受支持的二进制变得可见。

## 图片

在 `opencode.json` 或 `opencode.jsonc` 中配置图片归一化：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "media": {
    "image": {
      "auto_resize": true,
      "max_width": 2000,
      "max_height": 2000,
      "max_base64_bytes": 5242880,
    },
  },
}
```

所有字段都是可选的：

| 字段 | 默认值 | 行为 |
| ------------------ | --------- | ------------------------------------------------------------------------- |
| `auto_resize` | `true` | 超过配置上限时缩放图片；为 `false` 时，拒绝该图片。 |
| `max_width` | `2000` | 最大宽度（像素）；必须是正整数。 |
| `max_height` | `2000` | 最大高度（像素）；必须是正整数。 |
| `max_base64_bytes` | `5242880` | Base64 编码图片的最大字节数；必须是正整数。 |

例如，下面这样会拒绝而不是缩放宽度超过 1200 像素的图片：

```jsonc title="opencode.jsonc"
{
  "media": {
    "image": {
      "auto_resize": false,
      "max_width": 1200,
    },
  },
}
```

这些设置既适用于附加到提示中的受支持图片，也适用于内置 `read` 工具返回的图片。

## 处理

`read` 工具按内容识别 PNG、JPEG、GIF 和 WebP，最多读取 20 MiB 的源图片数据。它会根据配置的图片限制检查宽度、高度和 Base64 长度。

在 `auto_resize: true` 时，OpenCode 保持宽高比并缩小到尺寸上限。然后它会依次尝试越来越小的 PNG 和 JPEG 编码，直到满足 Base64 限制，因此输出媒体类型可能会变化。

```text
Input:  4000 × 2000 WebP
Limits: 2000 × 2000
Output: 2000 × 1000 PNG or JPEG
```

如果没有任何编码满足要求，处理就会失败。在 `auto_resize: false` 时，超过任何限制的图片会原样失败；无法解码的图片也会失败。

```text
Input:  2400 × 1600 JPEG
Limit:  max_width = 2000, auto_resize = false
Result: Image processing fails
```

如果图片缩放器不可用，OpenCode 会原样传递原始图片。因此图片设置是处理限制，而不是上传或安全边界。

## 限制

| 限制 | 值或行为 | 示例 |
| ----------------------------- | ------------------------------------------------------------- | -------------------------------------------- |
| 直接附件 | 每项解码后 20 MiB；客户端可能施加更低的限制 | 两个 12 MiB 的文件通过单项限制 |
| 桌面选择器的选择 | 总计 20 MiB | 两个 12 MiB 的文件超出选择限制 |
| `max_base64_bytes` | 仅计编码后的 Base64，不含完整的 `data:` URL | `SGVsbG8=` 算作 8 字节 |
| provider 图片限制 | 在 OpenCode 处理之后应用 | provider 可能拒绝一个已被接受的图片 |
| 文本附件的模型支持 | 不需要多模态模型 | `notes.txt` 会作为提示文本插入 |
| `read` 文本限制 | 使用单独的分页和截断限制 | 分页读取大型日志 |

客户端接受了某个文件并不保证其内容会到达模型。附件必须使用模型可见的格式，并且同时满足 OpenCode 和 provider 的限制。
