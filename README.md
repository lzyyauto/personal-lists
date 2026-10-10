# personal-lists

个人白名单、黑名单和 AI 专用名单的统一来源，可供不同客户端、路由器和网络工具使用。

## 名单文件

| 文件 | 内容 |
| --- | --- |
| `lists/whitelist.txt` | 白名单域名 |
| `lists/blacklist.txt` | 黑名单域名 |
| `lists/ailist.txt` | AI 专用名单 |

当前分流用途：白名单直连，黑名单走代理；同一域名同时命中时，白名单优先。其他工具接入时应显式指定动作，不能默认把黑名单解释为禁止访问。

三个文件保存名单匹配条件，不保存节点信息、订阅地址或凭据。客户端为每份名单指定动作，AI 专用名单当前默认使用 BWG，允许手动选择其他策略，后续更换出口无需修改名单。

## 维护约定

- 当前名单统一使用 `+.example.com` 形式，每行一个匹配条目，覆盖根域名及所有层级的子域名。其他工具接入时按目标客户端格式转换。
- 使用小写域名；国际化域名使用 Punycode。
- 空行与以 `#` 开头的注释忽略。
- 不写 URL、端口、路径、IP 地址或客户端规则指令。
- 不要将当前条目改成 `*.example.com` 或普通域名：在 Mihomo 中前者只匹配一级子域名，后者精确匹配根域名；二者都会缩小当前匹配范围。
- 发布前检查重复条目和三份名单之间的重叠。

例如，Mihomo 域名规则中的 `example.com` 只匹配根域名，`*.example.com` 匹配 `api.example.com`，但不匹配 `example.com` 或 `v1.api.example.com`；`+.example.com` 匹配三者。例子仅作说明，不会自动加入名单。格式说明见 [Mihomo 域名通配符文档](https://wiki.metacubex.one/handbook/syntax/#域名通配符)。

## 客户端接入

Mihomo 可以直接读取这三份 TXT 文件：在 `rule-providers` 中指定 `type: http`、`behavior: domain`、`format: text`，不需要 YAML 的 `payload` 包装。其他客户端需按其规则格式转换，保留精确匹配、根域名及子域名匹配、通配符匹配的区别。

名单只包含匹配条件；直连、代理等动作由客户端配置指定。不同客户端共享同一份源数据，避免分别修改后产生差异。

## AI 专用策略示例

见 [Mihomo 接入示例](examples/mihomo-ailist.yaml)。这是合并到现有客户端配置的示例片段，已填写三份名单的真实远程地址，不能直接作为完整配置运行。

- `ailist` 命中 `🤖 AI 专用`，与现有通用 AI / ChatGPT 分组分开。
- `🤖 AI 专用` 使用 `select`，默认选择 `👑 BWG`，也可手动改为美国、日本或默认代理策略。
- `👑 BWG` 建议按订阅来源 `use: [BWG]` 引入节点，避免仅靠名称筛选误选其他订阅中的节点。示例中的同名定义应替换现有定义，不能追加重复的策略组。
- 保持 `store-selected: true`，手动选择可在重启后恢复；首次使用或没有有效保存选择时才使用默认 BWG。
- 建议匹配顺序：内网直连 → 白名单 → AI 专用名单 → 普通黑名单 → 原有应用及其他规则。AI 专用名单覆盖普通黑名单；白名单仍可显式指定直连。
- 这是手动选择策略，BWG 不可用时不会因此自动切换到其他策略。自动故障切换需要另行配置。

当前仅准备接入示例，未修改两份客户端配置，设备端尚未验收。

## GitHub 仓库与远程地址

公开仓库：[lzyyauto/personal-lists](https://github.com/lzyyauto/personal-lists)。仅发布名单、说明及接入示例。客户端完整配置保留在原位置。

| 名单 | 远程 TXT 地址 |
| --- | --- |
| 白名单 | [whitelist.txt](https://raw.githubusercontent.com/lzyyauto/personal-lists/main/lists/whitelist.txt) |
| 黑名单 | [blacklist.txt](https://raw.githubusercontent.com/lzyyauto/personal-lists/main/lists/blacklist.txt) |
| AI 专用名单 | [ailist.txt](https://raw.githubusercontent.com/lzyyauto/personal-lists/main/lists/ailist.txt) |

名单修改并推送后，设备按示例中每小时一次的间隔拉取，也可在客户端手动更新规则。接入时需验证首次下载、定时更新、缓存、下载失败以及名单冲突时的行为。空黑名单表示暂时没有匹配条目。
