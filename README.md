# [English](https://github.com/hxz393/BrutalityExtractor/blob/main/README_EN.md) | [中文](https://github.com/hxz393/BrutalityExtractor/blob/main/README.md)

# 软件介绍

BrutalityExtractor 是一款专为高性能系统打造的暴力解压软件。针对现代多核处理器和高速固态硬盘优化，速度比常见解压软件提升 5 倍以上，彻底利用计算机硬件性能。

主要特性：

- 批量解压缩：自动扫描解压目录下所有压缩文件，即使文件后缀名不正确也能正确识别。
- 支持多格式：支持常见压缩文件格式 `7z`、`zip`、`rar`、`tar`、`gz`、`xz`、`bz2` ，并且能正确处理分卷压缩包。
- 支持多进程：根据处理器线程数，自定义解压进程数量，将解压速度翻倍。
- 支持密码列表：可以设置常用密码列表，自动匹配加密压缩包。
- 附加功能：消除目录冗余、删除空目录、删除垃圾文件等常用功能。

软件截图：

![1.0.0 版本截图](https://raw.githubusercontent.com/hxz393/BrutalityExtractor/main/capture/v1.0.0.jpg)



## 系统要求

使用前请仔细阅读下面软件的使用限制。

### 操作系统

软件开发编译环境为 `Win10 x64` 专业工作站版，版本号 `22H2`。只要是 `Win10 x64` 操作系统的用户可以直接打开使用。

在 `Win 11` 下没有测试过，应该没问题。更低版本的 `Win 7` 和 `Win XP` 因为使用 `Python 3.10` 版本的原因，不支持运行。

其他操作系统理论上可以手动编译成可执行文件，编译流程参见下面自行打包小节。

### 处理器

当处理器配置低于 2 核 4 线程时，软件将运行在单进程模式，不会有任何速度加成。

处理器配置高于 2 核 4 线程时，出于稳定性考虑，软件能设置进程数最高不超过处理器线程数的一半。

当然你可以选择多开软件运行，来实际上无视这一限制。因此造成的系统死机、崩溃、丢失数据等结果，请自行评估影响。

### 内存

内存限制比较宽松，这是因为无法评估运行时实际所需内存。解压所需内存由文件压缩格式、压缩算法、是否固实压缩等因素决定。

当内存被占满时，可能会发生解压失败、程序运行报错、系统异常报错等情况。一个比较稳妥的做法是，将单个或分卷大于 4GB 的文件分开存放，手动解压。因为这些文件解压可能会占用大量内存，并且本软件对大体积文件没有加速效果。

如果可用内存大小超过要解压文件总大小，那请随意使用。

### 硬盘

如果使用传统机械硬盘，则无论处理器或内存配置有多高，使用本软件或其他软件，都不能让解压速度超过硬盘读写速度。

现在使用 `PCI-E 3.0 x4` 以上接口的固态硬盘，还被其他解压软件限制在机械硬盘的速度，这是一种极大性能浪费。本软件没有发明新的解压算法来提高速度，但通过多进程运行的方式，让性能瓶颈转移到处理器上。

一个通用硬盘规格和进程数对应关系表如下：

| 硬盘规格          | 进程数 | 说明                                                         |
| ----------------- | ------ | ------------------------------------------------------------ |
| HDD SATA 3.0 18TB | 2      | 高性能 HDD，读写速度超 200MB/s，勉强可开 2 个进程            |
| SSD SATA 3.0 4TB  | 4      | 高性能 SATA 接口 SSD，读写速度最高 500MB/s，可开 4 个进程    |
| SSD PCI-E 1TB     | 8~64   | 常见 m.2 接口 SSD，通常有 1GB/s 以上读写速度，性能差异极大。进程数根据实际情况调整 |



## 下载地址

软件下载方式：

- 方式一：到 [release](https://github.com/hxz393/BrutalityExtractor/releases) 页面下载最新版的可执行文件，文件名为 `BrutalityExtractor.exe` 或 `BrutalityExtractorCli.exe` ，下载完毕可直接打开使用。
- 方式二：[百度网盘](https://pan.baidu.com/s/1LiL_Kvwcjsl44UvJxJIUTg?pwd=6666)分流下载。
- 方式三：[直连](https://www.x2b.net/download/BrutalityExtractor%20v1.0.0.zip)下载。



## 自行打包

手动编译需要事先安装好 `Python 3.10` 以上版本，和 `pyinstaller` 软件包。其他依赖报缺啥装啥，统一装最新版。

编译步骤如下：

1. 在安装有 `Git` 的主机上克隆项目。命令如下：

   ```sh
   git clone https://github.com/hxz393/BrutalityExtractor.git
   ```

   或者在 [项目主页](https://github.com/hxz393/BrutalityExtractor) 点击绿色`<> Code` 按钮选择 `Download ZIP` 选项，[下载](https://github.com/hxz393/BrutalityExtractor/archive/refs/heads/main.zip) 源码压缩包。下载完毕后用压缩软件或命令工具解压缩。

2. 使用命令切换到项目路径下面。

   例如在 Windows 系统下面，打开 `CMD` 命令提示符，输入：

   ```sh
   cd B:\git\BrutalityExtractor
   B:
   ```

   在 Linux 系统下面，通用使用 `cd` 命令切换到项目路径下面：

   ```sh
   cd /root/BrutalityExtractor
   ```

   如果使用 `PyCharm` 作为 IDE，可以直接在自带的终端栏目输入下面打包命令。

3. 使用 `pyinstaller` 命令编译打包成可执行文件：

   ```sh
   pyinstaller -F -w -i BrutalityExtractor.ico --add-binary 'bin/7z.exe;bin' --add-binary 'bin/7z.dll;bin' --collect-all="tksvg" BrutalityExtractor.py
   ```

   打包命令行模式脚本：
   
   ```sh
   pyinstaller -F -w -i BrutalityExtractor.ico --add-binary 'bin/7z.exe;bin' --add-binary 'bin/7z.dll;bin' --console BrutalityExtractorCli.py
   ```
   
   如果过程没有报错，可执行文件会生成到 `dist` 目录下面。



## 开源许可

本软件采用 [GPL-3.0 license](https://github.com/hxz393/BrutalityExtractor/blob/main/LICENSE) 源授权许可协议，若违背开源社区的基本准则，将开源项目据为私有用于商业用途，属于侵权行为，本人将追究法律责任。

用到的第三方开源库：

- 解压核心：7z-22.01
- 文件识别：magic-0.4.14
- 主题美化：ttkbootstrap-1.10.1
- 图标生成：tkfontawesome-0.2.0



# 软件使用

第一次运行时，由于缺少配置文件软件界面为英文。可以展开 Appearance Settings，在 Language 后面选择简体中文来切换语言。选择以后需要重启软件来生效。

## 基本配置

其中解压目录或目标目录为必填项。

- **解压目录**

  输入或选择压缩包存放的目录，例如`B:\Archive` 或 `B:/Archive/` 均可正常识别。

  目录内最好别放无关的文件，否则可能会有意外的解压行为，例如将游戏资源打包文件 `resources.pak` 给解压，造成游戏无法运行。

- **目标目录**

  输入解压后文件存放目录，解压后的目录结构会和解压目录中的保持一致。例如 `B:/Archive/xd1/test.zip` 会被解压到 `B:/New/xd1/test`。

  将目标目录设定到不同磁盘，可以稍微提升解压速度。

- **解压密码**

  输入单个密码或者密码列表文本文件位置。如果压缩包没有密码，随便输入什么密码都可以解压。如果有密码，会挨个尝试密码列表中的密码，直到密码正确或全部失败。

  软件本身没有对密码尝试做多进程处理。如果需要暴力破解压缩包密码，可将密码列表分为多份，运行多个软件实例来跑。将日志等级设为 Debug，可在日志中看到尝试结果。此功能请勿用于非法用途。



## 高级配置

高级配置中的设置需要根据实际情况来调整。

- **进程数量**

  设置同时运行解压的进程数。由于解压操作对处理器、内存和硬盘有极高的占用，建议运行时不要新开别的软件，保证解压顺利完成。

- **忽略警告**

  关闭解压运行前的系统资源检测。

- **释放空间**

  在压缩包解压完成后，删除压缩包。无论开启与否，如果解压失败都不会删除原始压缩包。

- **日志相关**

  控制写入本地日志文件的配置，设置后需要重启软件来生效。



## 外观配置

一些可以调整的外观主题设置。

- **关闭提示**

  关闭鼠标悬停在文字上时显示的提示信息。

- **迷你模式**

  使用小图标模式，让布局更紧凑。需要重启生效。

- **修改主题**

  选择自己喜好的软件主题配色风格。

- **修改语言**

  修改软件显示语言。目前仅有中英两种，欢迎提交其他语种的靠谱翻译。语言字典位于 `config/lang.py`。

- **窗口透明**

  配置窗口透明度。



## 附加功能

附加功能独立于解压功能存在，提供一些常用文件操作功能。

- **功能开关**

  开启功能开关后，将在目标目录下执行下面所配置的功能，解压操作暂时关闭。

- **消除冗余**

  消除冗余目录结构。只有在目录下有且仅有一个同名目录情况下会工作，一次只消除一层冗余结构。例如：将 `D:/test/test/` 下面的文件提取到 `D:/test/`，之后删除空的 `D:/test/test` 目录。

- **清理目录**

  删除指定目录下所有扫描到空目录。有时空目录有其特殊用途，请谨慎清理。

- **排除文件和排除目录**

  指定的文件或目录名，直接删除目标目录下找到的匹配目标。和解压密码一样，支持名称列表。



## 命令行模式

在命令行中运行时，需要下载命令行版本可执行文件 `BrutalityExtractorCli.exe` 。

命令行模式仅支持有限的功能，但速度更快。命令格式如下：

```sh
BrutalityExtractorCli.exe [-h] -d D [-p P] [-c C] [-v]
```

其中中括号 `[]` 内的参数为可选。可以使用 `BrutalityExtractorCli.exe -h` 命令来查看自带帮助。

参数说明如下：

- `-d`：指定压缩文件存放目录，解压操作也在同一目录进行，并且解压成功后会删除源压缩文件。
- `-c`：设置同时解压的进程数量。没有最高限制，请小心输入。
- `-p`：指定解压密码或密码列表。如果密码带空格，需要用双引号 `""` 将密码括起来。

下面是一个使用示例，指定解压目录为 `B:\Archive`，密码列表为 `B:/pass.txt`，运行进程数 50：

```sh
B:\new>BrutalityExtractorCli.exe -c 50 -d B:\Archive -p B:/pass.txt
BrutalityExtractor Copyright 2023 by assassing
2023-06-11 16:49:53,508 - INFO - BrutalityExtractorCli::main - ######Extracting files######
2023-06-11 16:49:53,522 - WARNING - file_ops::group_files_main - File B:\Archive\3333.flac is not supported, its type is: audio/x-flac
2023-06-11 16:49:53,523 - WARNING - file_ops::group_files_main - File B:\Archive\5555.zip is not supported, its type is: application/octet-stream
2023-06-11 16:49:53,525 - WARNING - file_ops::group_files_main - File B:\Archive\S1 is not supported, its type is: image/jpeg
2023-06-11 16:49:55,793 - INFO - file_unzip::unzip - Decompression Success : B:\Archive\a1.tar
2023-06-11 16:49:55,802 - INFO - file_unzip::unzip - Decompression Success : B:\Archive\new\a1.tar
2023-06-11 16:49:55,803 - INFO - file_unzip::unzip - Decompression Success : B:\Archive\s2
2023-06-11 16:49:55,804 - INFO - file_unzip::unzip - Decompression Success : B:\Archive\A1.bz2
2023-06-11 16:49:55,804 - WARNING - file_unzip::unzip - Decompression Failed : B:\Archive\7777.7z.001, unexpected end of archive
2023-06-11 16:49:55,804 - INFO - file_unzip::unzip - Decompression Success : B:\Archive\c.001.002.003.zip.gz
2023-06-11 16:49:55,805 - INFO - file_unzip::unzip - Decompression Success : B:\Archive\3333.gz
2023-06-11 16:49:55,807 - INFO - file_unzip::unzip - Decompression Success : B:\Archive\new\A1.bz2
2023-06-11 16:49:55,829 - INFO - file_unzip::unzip - Decompression Success : B:\Archive\3333.001
2023-06-11 16:49:55,841 - INFO - file_unzip::unzip - Decompression Success : B:\Archive\new\8888.001
2023-06-11 16:49:55,842 - WARNING - file_unzip::unzip - Decompression Failed : B:\Archive\new\3333.part01.rar, all passwords failed
2023-06-11 16:49:55,844 - INFO - file_unzip::unzip - Decompression Success : B:\Archive\8888.001
2023-06-11 16:49:55,847 - WARNING - file_unzip::unzip - Decompression Failed : B:\Archive\5555.001.zip, unexpected end of archive
2023-06-11 16:49:55,878 - INFO - file_unzip::unzip - Decompression Success : B:\Archive\3333.zip
2023-06-11 16:49:55,884 - INFO - file_unzip::unzip - Decompression Success : B:\Archive\new\bb.zip
2023-06-11 16:49:55,885 - INFO - file_unzip::unzip - Decompression Success : B:\Archive\bb.zip
2023-06-11 16:49:56,008 - WARNING - file_unzip::unzip - Decompression Failed : B:\Archive\3333.part1.rar, missing volume: 3333.part4.rar
2023-06-11 16:49:56,390 - INFO - file_unzip::unzip - Decompression Success : B:\Archive\3333.rar
2023-06-11 16:49:56,534 - INFO - BrutalityExtractorCli::main - ######Finished!######
Total compressed files: 32
Failed decompressions: 10
Successful decompressions: 22
Total compressed file size: 553.0 MB
Processes: 50
Time spent: 3.02 seconds
Processing speed: 183.08 MB/s
```



# 常见问题

软件运行遇见错误时，先查看下面总结的一些常见问题和解决方案。再查看所有 [Issue](https://github.com/hxz393/BrutalityExtractor/issues) 中是否有同样问题。如果都没有帮助，可以提交新 [Issue](https://github.com/hxz393/BrutalityExtractor/issues) ，并附上相关日志。

## 窗口最大化后不正常

全屏模式下折叠展开不会自动适应窗口高度。

**原因**：由于使用的框架原因，不支持全屏模式。

解决：欢迎提供解决方案。



## 增加批量压缩功能

不加入。常见压缩软件在压缩时资源利用率非常好，请尝试 `7z`、`PeaZip` 等开源免费软件。



## 增加自动改名功能

不加入。请尝试专业的软件，例如：`everything`、`PowerToys` 等优秀免费软件。



# 更新日志
为避免更新日志过长，只保留最近更新日志。

## 版本 1.0.0（2023.06.11）

发布第一个版本。