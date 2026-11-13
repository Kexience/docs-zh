---
source_url: https://java.testcontainers.org/contributing_docs/
source_hash: sha256:1ba89268504d87d7dd080dafd52db9a2a87a81124cfbc337867435dca841a46c
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# 文档贡献指南

Testcontainers for Java 的文档是一个用 [MkDocs](https://www.mkdocs.org/) 构建的静态站点。我们使用 [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) 主题，它为 MkDocs 提供了许多实用的扩展。

此外，我们还使用一个[自定义插件](https://github.com/rnorth/mkdocs-codeinclude-plugin)来引入代码片段。

我们使用 Netlify 发布文档。

## 预览渲染后的内容

### 在本地使用 Docker

项目根目录包含一个 `docker-compose.yml` 文件。只需运行 `docker-compose up`，然后在 [http://localhost:8000](http://localhost:8000) 访问文档。

### 在本地使用 Python

- 确保你使用的是 Python 3.12.0 或更高版本。
- 在 `testcontainers-java` 根目录下创建一个 virtualenv，并运行 `pip install -r requirements.txt`。
- Python 依赖安装完成后，运行 `mkdocs serve` 启动本地自动更新的 MkDocs 服务器。

### PR 预览部署

请注意，pull request 的文档会由 Netlify 自动发布为"部署预览"。这些部署预览可以通过每个 pull request 上出现的 `deploy/netlify` 检查访问。

## 代码引入（Codeincludes）

`docs/examples` 下的 Gradle 项目用于存放可编译、可运行的示例代码，这些代码可以在构建时以片段的形式引入到文档中。

这样一来，我们就更有把握相信文档中展示的代码样例是有效的。

我们使用一个 MkDocs 自定义插件把片段引入文档。

一个 codeinclude 块形似一段普通的 markdown 链接，外面包着一对 XML 注释，例如：

为了避免在渲染本页时它被当作 codeinclude 渲染，我们使用 HTML 标签。请查看它渲染后的样子以了解实际效果，或者去看看文档中的其他页面。

```
<!--codeinclude-->
[Human readable title for snippet](./relative_path_to_example_code.java) targeting_expression
<!--/codeinclude-->
```

其中 `targeting_expression` 可以是：

- `block:someString`，或者
- `inside_block:someString`

如果提供了这些，宏就会找到包含标记 `someString` 的任意一行，并抓取其后遇到的第一段以花括号分隔的代码块。`block` 会连同起始行和结束括号一起抓取，而 `inside_block` 会忽略这两者。

例如，假设有：

```java
public class FooService {

    public void doFoo() {
        foo.doSomething();
    }

    ...
```

如果我们使用 `block:doFoo` 作为定位表达式，页面中就会包含以下内容：

```java
public void doFoo() {
    foo.doSomething();
}
```

而使用 `inside_block:doFoo` 时，则只会包含该方法内部的内容：

```java
foo.doSomething();
```

请注意：

- 引入的任何代码，其缩进都会被减少
- 源文件中的每一行都会被搜索是否包含该标记（例如 `doFoo`）的实例。如果有多行包含该标记，那么可能会有多段代码块被定位并引入。建议使用具体且唯一的标记，以避免意外行为。

当我们想引入一段并不自然出现在花括号内的代码时，只要在注释中插入我们的标记，并配上对应的花括号即可。虽然有点丑，但这样在任何上下文中都管用，也容易理解。例如：

```java
public class FooService {

    public void boringMethod() {
        doSomethingBoring();

        // doFoo {
        doTheThingThatWeActuallyWantToShow();
        // }
    }
```
