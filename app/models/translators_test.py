# Copyright 2022 PingCAP, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from app.models.openai_client import translate as openai_trans


class TestTranslators(unittest.TestCase):
    html_example = """
            <p>【 TiDB 使用环境】生产环境 /测试/ Poc<br>
            生产环境<br>
            【 TiDB 版本】<br>
            v7.1.0<br>
            【复现路径】做过哪些操作出现的问题<br>
            新增索引<br>
            【遇到的问题：问题现象及影响】<br>
            加不上<br>
            【资源配置】<em>进入到 TiDB Dashboard -集群信息 (Cluster Info) -主机(Hosts) 截图此页面</em><br>
            """
    long_text = """
# 一、升级版本选择

1. ## 主推版本 Release Notes

**TiDB 7.5.1 Release Notes** ：https://docs.pingcap.com/zh/tidb/stable/release-7.5.1

**TiDB 7.1.** **5** **Release Notes** ：https://docs.pingcap.com/zh/tidb/stable/release-7.1.5

**TiDB 6.5.9 Release Notes**：https://docs.pingcap.com/zh/tidb/stable/release-6.5.9

2. ## 主推版本特性解读

TiDB 6.X 版本和7.X 版本主要区别：7.X 版本有 Resource Control 资源管控功能

### 7.5.x 相关特性解读

* [TiDB 7.5 LTS 发版丨提升规模化场景下关键应用的稳定性和成本的灵活性 ](https://tidb.net/blog/1cffec89)

* [TiDB v7.5.0 LTS 升级必读 | 新特性补充说明 ](https://tidb.net/blog/be2db121)

### 7.1.x 相关特性解读

* [新特性解析丨TiDB 资源管控的设计思路与场景解析 ](https://tidb.net/blog/67d82266)

* [TiDB v7.1.0 资源管控功能是如何降低运维难度和成本-实现集群资源最大化？](https://tidb.net/blog/0e600aaf)

* [TiDB v7.1.0 跨业务系统多租户解决方案](https://tidb.net/blog/2ce19df3)

* [TiDB v7.1.0版本 相关（部署、在线扩容、数据迁移）测试](https://tidb.net/blog/69083bca)

* [TiDB 7.1 资源管控验证测试](https://tidb.net/blog/9cd7dcb3)

* [TiDB 7.1.0 LTS 特性解读 | 浅析 TiSpark v3.x 新变化 ](https://tidb.net/blog/1a3daf9b)

* [TiDB 7.1.0 LTS 特性解读 | 资源管控 (Resource Control) 应该知道的 6 件事](https://tidb.net/blog/978ee7ab)

* [TiDB 7.x 源码编译之 TiDB Server 篇，及新特性详解](https://tidb.net/blog/8f6af887)

* [TiDB 7.x 源码编译之 TiUP 篇，及新特性解析](https://tidb.net/blog/1970f2ba)

* [tidb之旅——生成列](https://tidb.net/blog/15d0fbf6)

* [tidb之旅——资源管控](https://tidb.net/blog/26695303)

* [索引加速功能真能提升10倍吗？--TiDB V6.1.0-V7.1.0建索引速度对比](https://tidb.net/blog/a93d7c03)

### 6.5.x 相关特性解读

* [专栏 - TiDB 新特性解读 （6.0~6.6） | TiDB 社区](https://tidb.net/blog/da5c889f)

* [专栏 - 天下武功唯快不破：TiDB 在线 DDL 性能提升 10 倍 | TiDB 社区](https://tidb.net/blog/4f85e64a)

# 二、升级方案选择

![image|690x274](upload://sCRNPfm171HItzXD6uvnsM4j8tx.png)
可参考：https://tidb.net/blog/42a326ae
# 三、升级工具介绍&FAQ

1. ## TiUP

> 在物理机或虚拟机上的 TiDB 包管理器，管理着 TiDB 的众多的组件，如 TiDB、PD、TiKV 等。当你想要运行 TiDB 生态中任何组件时，只需要执行一行 TiUP 命令即可（TiDB v4.0 起）。

TiUP 文档介绍：https://docs.pingcap.com/zh/tidb/stable/tiup-overview

TiUP FAQ：https://docs.pingcap.com/zh/tidb/stable/tiup-faq

2. ## Dumpling

> 数据导出工具，可以把存储在 TiDB 或 MySQL 中的数据导出为 SQL 或 CSV 格式，用于逻辑全量备份。Dumpling 也支持将数据导出到 Amazon S3 中。

Dumpling 文档介绍：https://docs.pingcap.com/zh/tidb/stable/dumpling-overview

3. ## Lightning

> 数据导入工具，用于从静态文件导入 TB 级数据到 TiDB 集群的工具，常用于 TiDB 集群的初始化数据导入。

Lighting 文档介绍：https://docs.pingcap.com/zh/tidb/stable/tidb-lightning-overview

导入（新）数据库要求：https://docs.pingcap.com/zh/tidb/stable/tidb-lightning-requirements

Lightning 常见故障处理：https://docs.pingcap.com/zh/tidb/stable/troubleshoot-tidb-lightning

4. ## TiCDC

> 增量数据同步工具，通过拉取 TiKV 变更日志实现的 TiDB 增量数据同步。TiCDC 典型的应用场景为搭建多套 TiDB 集群间的主从复制，或者配合其他异构的系统搭建数据集成服务。

TiCDC 文档介绍：https://docs.pingcap.com/zh/tidb/stable/ticdc-overview

TiCDC 常见故障和解决方案：https://docs.pingcap.com/zh/tidb/stable/troubleshoot-ticdc

# 四、升级前应做哪些准备？

1. ## 升级前必看文档

* [TiDB 版本升级的小 Tips](https://tidb.net/blog/b63a37f3)

* [TiDB 版本升级常见问题处理（v6.0 及以上版本）](https://tidb.net/blog/6b1674cb)

* [TiDB 升级方案选择](https://tidb.net/blog/42a326ae)

* 升级 FAQ：https://docs.pingcap.com/zh/tidb/stable/upgrade-faq

* TiDB 功能在不同版本中的支持变化情况: https://docs.pingcap.com/zh/tidb/stable/basic-features

2. ## 了解系统的健康状况

1. 确认集群拓扑结构是否满足高可用需求

2. 集群拓扑是否健康

3. 硬件配置是否达标

4. 集群使用情况

  1. 集群数据量

  2. 大表情况

  3. 表宽度，字段数量

  4. SQL 语句 DDL\DML 执行情况 QPS

  5. 字符集等兼容情况

3. ## 升级常见问题

### （1）滚动升级有那些影响？

滚动升级 TiDB 期间，业务运行会受到一定影响。因此，不建议在业务高峰期进行滚动升级。需要配置最小集群拓扑 (TiDB * 2、PD * 3、TiKV * 3)，如果集群环境中有 Pump 和 Drainer 服务，建议先停止 Drainer，然后滚动升级（升级 TiDB 时会升级 Pump）。

### （2）集群在执行 DDL 请求期间可以进行升级操作吗？

* 如果升级前 TiDB 的版本低于 v7.1.0：

  * 集群中有 DDL 语句正在被执行时（通常为 `ADD INDEX` 和列类型变更等耗时较久的 DDL 语句），请勿进行升级操作。在升级前，建议使用 `ADMIN SHOW DDL` 命令查看集群中是否有正在进行的 DDL Job。如需升级，请等待 DDL 执行完成或使用 `ADMIN CANCEL DDL` 命令取消该 DDL Job 后再进行升级。

  * 在升级 TiDB 集群的过程中，请勿执行 DDL 语句，否则可能会出现行为未定义的问题。
* 如果升级前 TiDB 的版本为 v7.1.0 或更高的版本：

  * 不用遵循限制低版本升级时的限制，即在升级时可以接收用户 DDL 任务。建议参考[平滑升级 TiDB](https://docs.pingcap.com/zh/tidb/stable/smooth-upgrade-tidb)。

4. ## 用户版本升级实践

### 7.5.x升级实践

* [【新手升级必看】从 TiDB v6.5升级到 v7.5 的实践步骤 ](https://tidb.net/blog/b0fea026)

* [TiDB-v7.5.0 DDL 启停特性分析 ](https://tidb.net/blog/6ee4aafe)

### 7.1.x升级实践

* [一个 39.3T 的集群从TiDB v3.1.0迁移升级到 TiDB v7.1.2 的实践](https://tidb.net/blog/0629c299)

* [简单三步完成离线升级TIDB v7.1（服务器无互联网环境）](https://tidb.net/blog/e35af409)

* [TiDB v7.1.0 跨业务系统多租户解决方案 ](https://tidb.net/blog/2ce19df3)

* [中欧财富：分布式数据库的应用历程和 TiDB 7.1 新特性探索](https://tidb.net/blog/ccbaeda2)

* TiDB v7.1.1 [三地五中心，TiDB POC最佳实践探索 ](https://tidb.net/blog/b4732d88)

* [TiDB 同城双中心监控组件高可用方案 ](https://tidb.net/blog/44b9b8b1)

* [TiDB 7.1 资源管控验证测试](https://tidb.net/blog/9cd7dcb3)

* [TIDB v7.1 reource control资源管控特性体验贴](https://tidb.net/blog/60c87e38)

* [TiDB 多租户方案和原理 ](https://tidb.net/blog/a55c1d14)

* [TiDB 7.1.0 资源管控特性试用](https://tidb.net/blog/3ddb423a)

* [记一次 TiDB v7.1 版本生产环境的完整搭建流程 ](https://tidb.net/blog/1053fcd8)

* [HAProxy安装及搭建tidb数据库负载均衡服务实战 ](https://tidb.net/blog/88e78888)

* [TiDB v7.1.0离线升级命令版](https://tidb.net/blog/9a7357ee)

* [搭建TiDB负载均衡环境-LVS+KeepAlived实践](https://tidb.net/blog/f614b200)

* [搭建TiDB负载均衡环境-HAproxy+KeepAlived实践 ](https://tidb.net/blog/8e8cca1d)

* [TiDB v7.1.0 资源管控功能是如何降低运维难度和成本-实现集群资源最大化？](https://tidb.net/blog/0e600aaf)

* [TiDB v7.1.0：精准资源分配，实现数据流畅运行！ ](https://tidb.net/blog/8abfaa25)

# 升级中

[使用 TiUP 升级 TiDB](https://docs.pingcap.com/zh/tidb/stable/upgrade-tidb-using-tiup#%E4%BD%BF%E7%94%A8-tiup-%E5%8D%87%E7%BA%A7-tidb)

> 本文档适用于以下升级路径：
>
>
>
> * 使用 TiUP 从 TiDB 4.0 版本升级至 TiDB 7.5。
>
>
> * 使用 TiUP 从 TiDB 5.0-5.4 版本升级至 TiDB 7.5。
>
>
> * 使用 TiUP 从 TiDB 6.0-6.6 版本升级至 TiDB 7.5。
>
>
> * 使用 TiUP 从 TiDB 7.0-7.4 版本升级至 TiDB 7.5。
>
>
>
> 警告
>
>
>
> 1. 不支持将 TiFlash 组件从 5.3 之前的老版本在线升级至 5.3 及之后的版本，只能采用停机升级。如果集群中其他组件（如 tidb，tikv）不能停机升级，参考[不停机升级](https://docs.pingcap.com/zh/tidb/stable/upgrade-tidb-using-tiup#%E4%B8%8D%E5%81%9C%E6%9C%BA%E5%8D%87%E7%BA%A7)中的注意事项。
>
>
> 2. 在升级 TiDB 集群的过程中，请勿执行 DDL 语句，否则可能会出现行为未定义的问题。
>
>
> 3. 集群中有 DDL 语句正在被执行时（通常为 `ADD INDEX` 和列类型变更等耗时较久的 DDL 语句），请勿进行升级操作。在升级前，建议使用 `ADMIN SHOW DDL` 命令查看集群中是否有正在进行的 DDL Job。如需升级，请等待 DDL 执行完成或使用 `ADMIN CANCEL DDL` 命令取消该 DDL Job 后再进行升级。
>
>
>
> 从 TiDB v7.1 版本升级至更高的版本时，可以不遵循上面的限制 2 和 3，建议参考[平滑升级 TiDB 的限制](https://docs.pingcap.com/zh/tidb/stable/smooth-upgrade-tidb#%E4%BD%BF%E7%94%A8%E9%99%90%E5%88%B6)。

# 升级后

## 升级后常见问题

本小节列出了一些升级后可能会遇到的问题与解决办法。

### 执行 DDL 操作时遇到的字符集 (charset) 问题

TiDB 在 v2.1.0 以及之前版本（包括 v2.0 所有版本）中，默认字符集是 UTF8。从 v2.1.1 开始，默认字符集变更为 UTF8MB4。如果在 v2.1.0 及之前版本中，建表时显式指定了 table 的 charset 为 UTF8，那么升级到 v2.1.1 之后，执行 DDL 操作可能会失败。

要避免该问题，需注意以下两个要点：

* 在 v2.1.3 之前，TiDB 不支持修改 column 的 charset。所以，执行 DDL 操作时，新 column 的 charset 需要和旧 column 的 charset 保持一致。

* 在 v2.1.3 之前，即使 column 的 charset 和 table 的 charset 不一样，`show create table` 也不会显示 column 的 charset，但可以通过 HTTP API 获取 table 的元信息来查看 column 的 charset，下文提供了示例。

#### `unsupported modify column charset utf8mb4 not match origin utf8`

* 升级前：v2.1.0 及之前版本

```
create table t(a varchar(10)) charset=utf8;
```

```
Query OK, 0 rows affected
Time: 0.106s
```

```
show create table t
```

```
+-------+-------------------------------------------------------+
| Table | Create Table                                          |
+-------+-------------------------------------------------------+
| t     | CREATE TABLE `t` (                                    |
|       |   `a` varchar(10) DEFAULT NULL                        |
|       | ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin |
+-------+-------------------------------------------------------+
1 row in set
Time: 0.006s
```

* 升级后：v2.1.1、v2.1.2 会出现下面的问题，v2.1.3 以及之后版本不会出现下面的问题。

```
alter table t change column a a varchar(20);
```

```
ERROR 1105 (HY000): unsupported modify column charset utf8mb4 not match origin utf8
```

解决方案：显式指定 column charset，保持和原来的 charset 一致即可。

```
alter table t change column a a varchar(22) character set utf8;
```

* 根据要点 1，此处如果不指定 column 的 charset，会用默认的 UTF8MB4，所以需要指定 column charset 保持和原来一致。

* 根据要点 2，用 HTTP API 获取 table 元信息，然后根据 column 名字和 Charset 关键字搜索即可找到 column 的 charset。

```
curl "http://$IP:10080/schema/test/t" | python -m json.tool
```

* 这里用了 python 的格式化 json 的工具，也可以不加，此处只是为了方便注释。

{"ShardRowIDBits": 0,"auto_inc_id": 0,"charset": "utf8",table 的 charset"collate": "","cols": [ # 从这里开始列举 column 的相关信息{ ..."id": 1,"name": {"L": "a","O": "a"column 的名字},"offset": 0,"origin_default": null,"state": 5,"type": {"Charset": "utf8",column a 的 charset"Collate": "utf8_bin","Decimal": 0,"Elems": null,"Flag": 0,"Flen": 10,"Tp": 15}}], ... }

#### `unsupported modify charset from utf8mb4 to utf8`

* 升级前：v2.1.1，v2.1.2

```
create table t(a varchar(10)) charset=utf8;
```

```
Query OK, 0 rows affected
Time: 0.109s
```

```
show create table t;
```

```
+-------+-------------------------------------------------------+
| Table | Create Table                                          |
+-------+-------------------------------------------------------+
| t     | CREATE TABLE `t` (                                    |
|       |   `a` varchar(10) DEFAULT NULL                        |
|       | ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin |
+-------+-------------------------------------------------------+
```

* 上面 `show create table` 只显示出了 table 的 charset，但其实 column 的 charset 是 UTF8MB4，这可以通过 HTTP API 获取 schema 来确认。这是一个 bug，即此处建表时 column 的 charset 应该要和 table 保持一致为 UTF8，该问题在 v2.1.3 中已经修复。

* 升级后：v2.1.3 及之后版本

```
show create table t;
```

```
+-------+--------------------------------------------------------------------+
| Table | Create Table                                                       |
+-------+--------------------------------------------------------------------+
| t     | CREATE TABLE `t` (                                                 |
|       |   `a` varchar(10) CHARSET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL |
|       | ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin              |
+-------+--------------------------------------------------------------------+
1 row in set
Time: 0.007s
```

```
alter table t change column a a varchar(20);
```

```
ERROR 1105 (HY000): unsupported modify charset from utf8mb4 to utf8
```

解决方案：

* 因为在 v2.1.3 之后，TiDB 支持修改 column 和 table 的 charset，所以这里推荐修改 table 的 charset 为 UTF8MB4。

```
alter table t convert to character set utf8mb4;
```

* 也可以像问题 1 一样指定 column 的 charset，保持和 column 原来的 charset (UTF8MB4) 一致即可。

```
alter table t change column a a varchar(20) character set utf8mb4;
```

#### `ERROR 1366 (HY000): incorrect utf8 value f09f8c80(🌀) for column a`

TiDB 在 v2.1.1 及之前版本中，如果 charset 是 UTF8，没有对 4-byte 的插入数据进行 UTF8 Unicode encoding 检查。在 `v2.1.2` 及之后版本中，添加了该检查。

* 升级前：v2.1.1 及之前版本

```
create table t(a varchar(100) charset utf8);
```

```
Query OK, 0 rows affected
```

```
insert t values (unhex('f09f8c80'));
```

```
Query OK, 1 row affected
```

* 升级后：v2.1.2 及之后版本

```
insert t values (unhex('f09f8c80'));
```

```
ERROR 1366 (HY000): incorrect utf8 value f09f8c80(🌀) for column a
```

解决方案：

* v2.1.2 版本：该版本不支持修改 column charset，所以只能跳过 UTF8 的检查。

```
set @@session.tidb_skip_utf8_check=1;
```

```
Query OK, 0 rows affected
```

```
insert t values (unhex('f09f8c80'));
```

```
Query OK, 1 row affected
```

* v2.1.3 及之后版本：建议修改 column 的 charset 为 UTF8MB4。或者也可以设置 `tidb_skip_utf8_check` 变量跳过 UTF8 的检查。如果跳过 UTF8 的检查，在需要将数据从 TiDB 同步回 MySQL 的时候，可能会失败，因为 MySQL 会执行该检查。

```
alter table t change column a a varchar(100) character set utf8mb4;
```

```
Query OK, 0 rows affected
```

```
insert t values (unhex('f09f8c80'));
```

```
Query OK, 1 row affected
```

* 关于 `tidb_skip_utf8_check` 变量，具体来说是指跳过 UTF8 和 UTF8MB4 类型对数据的合法性检查。如果跳过这个检查，在需要将数据从 TiDB 同步回 MySQL 的时候，可能会失败，因为 MySQL 执行该检查。如果只想跳过 UTF8 类型的检查，可以设置 `tidb_check_mb4_value_in_utf8` 变量。

* `tidb_check_mb4_value_in_utf8` 在 v2.1.3 版本加入 `config.toml` 文件，可以修改配置文件里面的 `check-mb4-value-in-utf8` 后重启集群生效。

* `tidb_check_mb4_value_in_utf8` 在 v2.1.5 版本开始可以用 HTTP API 来设置，也可以用 session 变量来设置。

  * HTTP API（HTTP API 只在单台服务器上生效）

    * 执行下列命令启用 HTTP API：

```
curl -X POST -d "check_mb4_value_in_utf8=1" http://{TiDBIP}:10080/settings
```

    * 执行下列命令禁用 HTTP API：

```
curl -X POST -d "check_mb4_value_in_utf8=0" http://{TiDBIP}:10080/settings
```
  * Session 变量

    * 执行下列命令启用 Session 变量：

```
set @@session.tidb_check_mb4_value_in_utf8 = 1;
```

    * 执行下列命令禁用 Session 变量：

```
set @@session.tidb_check_mb4_value_in_utf8 = 0;
```
* v2.1.7 及之后版本，如果对表和 column 的字符集没有严格要求为 UTF8，也不想修改客户端代码去跳过 UTF8 检查或者手动修改 column 的 charset，可以在配置文件中把 `treat-old-version-utf8-as-utf8mb4` 打开。该配置的作用是自动把 v2.1.7 版本之前创建的旧版本的表和 column 的 UTF8 字符集转成 UTF8MB4。这个转换是在 TiDB load schema 时在内存中将 UTF8 转成 UTF8MB4，不会对实际存储的数据做任何修改。在配置文件中关闭 `treat-old-version-utf8-as-utf8mb4` 并重启 TiDB 后，以前字符集为 UTF8 的表和 column 的字符集仍然还是 UTF8。

* 注意

* `treat-old-version-utf8-as-utf8mb4` 参数默认打开，如果客户端强制需要用 UTF8 而不用 UTF8MB4，需要在配置文件中关闭。

# 拓展阅读

## 测试&对比&评测

* [TiDB 升级利器（参数对比）——TiDBA](https://tidb.net/blog/299f0bdc)

* [TiDB 7.1资源管控和Oceanbase 4.0多租户使用对比 ](https://tidb.net/blog/a33d3498)

* [【TiDB v7.1.0】资源管控调研及评测](https://tidb.net/blog/ad24240a)

* [TiDB v7.1.0版本 相关（部署、在线扩容、数据迁移）测试 ](https://tidb.net/blog/69083bca)

* [v7.1.0 Resource Control 功能测试 ](https://tidb.net/blog/24179946)

* [v7.1 LTS Resource Control 试用 ](https://tidb.net/blog/38269f09)


<div data-theme-toc="true"> </div>
"""

    def test_openai_translate(self):
        translated_html = openai_trans(self.html_example)
        print(translated_html)

