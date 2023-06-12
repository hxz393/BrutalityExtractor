# [English](https://github.com/hxz393/BrutalityExtractor/blob/main/README_EN.md) | [中文](https://github.com/hxz393/BrutalityExtractor/blob/main/README.md)

# Introduction

BrutalityExtractor is a brute-force decompression software specifically designed for high-performance systems. It is optimized for modern multi-core processors and high-speed solid-state drives, offering speeds that are more than 5 times faster than common decompression software, thoroughly exploiting the performance of computer hardware.

Features:

- Batch decompression: Automatically scans and decompresses all compressed files in the specified directory, even if the file extension is incorrect.
- Supports multiple formats: Supports common compression file formats `7z`, `zip`, `rar`, `tar`, `gz`, `xz`, `bz2` and can properly handle split compressed files.
- Supports multi-processing: Customize the number of decompression processes based on the processor thread count, doubling the decompression speed.
- Supports password lists: You can set a list of common passwords to automatically match encrypted compressed files.
- Additional features: Includes useful functions such as removing directory redundancy, deleting empty directories, and deleting junk files.

Screenshot:

![v1.0.0 screenshot:](https://raw.githubusercontent.com/hxz393/BrutalityExtractor/main/capture/v1.0.0-en.jpg)



## System Requirements

Please read carefully the following usage limitations of the software.

### OS

The software development and compilation environment is `Win10 x64` Professional Workstation Edition, version `22H2`. Users of any `Win10 x64` operating system can use it directly.

Although not tested under `Win 11`, it should work fine. Lower versions like `Win 7` and `Win XP` are not supported due to the use of `Python 3.10`.

For other operating systems, theoretically, it is possible to manually compile it into an executable file. Refer to the self-packaging section below for the compilation process.

### Processor

When the processor is less than 2 cores 4 threads, the software will run in single-process mode and there will be no speed increase.

For processor above 2 cores 4 threads, for stability considerations, the maximum number of processes that can be set by the software does not exceed half of the processor thread count.

You can choose to run multiple instances of the software to effectively ignore this limitation. For any system crashes, data loss, etc. that result from this, please assess the impact yourself.

### Memory

The memory requirement is relatively flexible, as it's impossible to assess the actual memory required at runtime. The memory required for decompression is determined by factors such as file compression format, compression algorithm, and whether solid compression is used.

If the memory is fully occupied, decompression may fail, program errors may occur, system errors may be reported, etc. A safer approach is to store files or volumes larger than 4GB separately and decompress them manually. This is because these files may take up a lot of memory when decompressed, and this software does not accelerate large-volume files.

If the available memory size exceeds the total size of the files to be decompressed, feel free to use the software.

### Hard Disk

If you're using a traditional mechanical hard drive, no matter how high the processor or memory is, neither this software nor any other software can make the decompression speed exceed the read-write speed of the hard drive.

Using a solid-state drive with a `PCI-E 3.0 x4` or higher interface is still being restricted to the speed of mechanical hard drives by other decompression software, which is a significant waste of performance. This software does not invent a new decompression algorithm to increase speed, but by running multiple processes, it moves the performance bottleneck to the processor.

A general table of hard disk specifications and corresponding process numbers is as follows:

| Hard Disk         | Process | Description                                                  |
| ----------------- | ------- | ------------------------------------------------------------ |
| HDD SATA 3.0 18TB | 2       | High-performance HDD with R/W speed over 200MB/s, barely sufficient to run 2 processes |
| SSD SATA 3.0 4TB  | 4       | High-performance SATA SSD, with maximum R/W speed of 500MB/s, can run 4 processes |
| SSD PCI-E 1TB     | 8~64    | Common m.2 SSD, usually having a R/W speed over 1GB/s, with great performance variation. Adjust process number according to actual situation |



## Download Links

Software download methods:

- Method 1: Go to the [release](https://github.com/hxz393/BrutalityExtractor/releases) page to download the latest executable file, named `BrutalityExtractor.exe` or `BrutalityExtractorCli.exe`. It can be used directly after download.
- Method 2: [Direct link](https://www.x2b.net/download/BrutalityExtractor v1.0.1.zip) download.



## Self-packaging

Manual compilation requires pre-installed `Python 3.10` or higher and the `pyinstaller` lib. Install other dependencies as needed, always using the latest version.

Compilation steps are as follows:

1. Clone the project on a machine with `Git` installed. The command is:

   ```sh
   git clone https://github.com/hxz393/BrutalityExtractor.git
   ```

   Or click the green `<> Code` button on the [project homepage](https://github.com/hxz393/BrutalityExtractor), select `Download ZIP`, and [download](https://github.com/hxz393/BrutalityExtractor/archive/refs/heads/main.zip) the source code zip file. Use compression software or command tools to decompress after download.

2. Use command line to switch to the project path.

   For example, on Windows, open `CMD` command prompt and enter:

   ```sh
   cd B:\git\BrutalityExtractor
   B:
   ```

   On Linux, generally use the `cd` command to switch to the project path:

   ```sh
   cd /root/BrutalityExtractor
   ```

   If you use `PyCharm` as your IDE, you can directly enter the packaging command in the built-in terminal column.

3. Use the `pyinstaller` command to compile and package into an executable file:

   ```sh
   pyinstaller -F -w -i BrutalityExtractor.ico --add-binary 'bin/7z.exe;bin' --add-binary 'bin/7z.dll;bin' --collect-all="tksvg" BrutalityExtractor.py
   ```

   The packaging command line mode script is:

   ```sh
   pyinstaller -F -w -i BrutalityExtractor.ico --add-binary 'bin/7z.exe;bin' --add-binary 'bin/7z.dll;bin' --console BrutalityExtractorCli.py
   ```

   If the process is error-free, the executable file will be generated in the `dist` directory.



## Open Source License

This software adopts the [GPL-3.0 license](https://github.com/hxz393/BrutalityExtractor/blob/main/LICENSE) for open-source authorization agreement. If the basic norms of the open-source community are violated, and the open-source project is used privately for commercial purposes, this will be considered an infringement act, and the author will pursue legal responsibility.

Third-party open source libraries used:

- Decompression core: 7z-22.01
- File recognition: magic-0.4.14
- Theme beautification: ttkbootstrap-1.10.1
- Icon generation: tkfontawesome-0.2.0



# Useage

When you first run the software, the interface will be in English due to the lack of a configuration file. You can expand the Appearance Settings and switch the language under Language. The software needs to be restarted to apply the changes.

## Basic Settings

Extraction Directory or Destination Directory is a mandatory field.

- **Extraction Directory**

  Enter or select the directory where the compressed files are stored, such as `B:\Archive` or `B:/Archive/`, both of which can be recognized normally.

  It's best not to put irrelevant files in the directory, otherwise, unexpected decompression behavior may occur, such as decompressing the game resource pack file `resources.pak`, causing the game to fail to run.

- **Destination Directory**

  Enter the directory where the decompressed files will be stored. The structure of the decompressed directory will be consistent with that in the extraction directory. For example, `B:/Archive/xd1/test.zip` will be decompressed to `B:/New/xd1/test`.

  Setting the destination directory to a different disk can slightly increase the decompression speed.

- **Decryption Password**

  Enter a single password or the location of the password list text file. If the compressed file does not have a password, any password can be used to decompress it. If there is a password, the software will try the passwords in the list one by one until the correct one is found or all have failed.

  The software itself does not process password attempts with multiple processes. If you need to brute force crack the compressed file password, you can divide the password list into multiple parts and run multiple instances of the software. Set the log level to Debug to see the attempt results in the log. Do not use this feature for illegal purposes.

  To make sure the password is read correctly, please save the text using the UTF-8 encoding format.



## Advanced Settings

Settings in the advanced configuration need to be adjusted according to actual conditions.

- **Processes**

  Set the number of decompression processes to run at the same time. As decompression operations occupy a lot of processor, memory, and hard disk resources, it's recommended not to open other software during operation to ensure smooth decompression.

- **Ignore Warnings**

  Turn off system resource detection before decompression.

- **Remove Source**

  Delete the compressed file after decompression success. Whether it is turned on or not, the original compressed file will not be deleted if decompression fails.

- **Log-related**

  Controls the configuration of writing to local log files. The software needs to be restarted to apply the changes.



## Appearance Settings

There are some adjustable theme settings.

- **Disable Hints**

  Turn off the tips displayed when the mouse hovers over the text.

- **Mini Mode**

  Use the small icon mode to make the layout more compact. Restart the software to apply.

- **Theme**

  Choose your favorite software theme color scheme.

- **Language**

  Change the software display language. Currently, only Chinese and English are available. Welcome to submit reliable translations for other languages. The language dictionary is located at `config/lang.py`.

- **Alpha**

  Configure the transparency of the window.



## Additional Features

Additional features exist independently of the decompression function and provide some common file operation functions.

- **Feature Switch**

  After turning on the feature switch, the following configured features will be executed in the destination directory, and the decompression operation will be temporarily turned off.

- **Eliminate Redundancy**

  Eliminate redundant directory structure. It only works if there is only one directory with the same name in the directory, and it only eliminates one layer of redundant structure at a time. For example, it will extract the files under `D:/test/test/` to `D:/test/`, and then delete the empty `D:/test/test` directory.

- **Purge Directories**

  Delete all scanned empty directories under the specified directory. Sometimes empty directories have their special uses, so clean up carefully.

- **Delete Files and Directories**

  Specified file or directory names will be directly deleted from the destination directory. Like the decryption password, it supports name lists file.



## Command Line Mode

When running in the command line, you need to download the command-line version executable file `BrutalityExtractorCli.exe`.

The command-line mode only supports limited functions, but it is faster. The command format is as follows:

```sh
BrutalityExtractorCli.exe [-h] -d D [-p P] [-c C] [-v]
```

The parameters in square brackets `[]` are optional. You can use the `BrutalityExtractorCli.exe -h` command to view the built-in help.

Parameter description:

- `-d`: Specify the directory where the compressed files are stored. The decompression operation is also performed in the same directory, and the source compressed file will be deleted after decompression is successful.
- `-c`: Set the number of simultaneous decompression processes. There is no upper limit, so enter it carefully.
- `-p`: Specify the decompression password or password list. If the password contains spaces, you need to enclose the password with double quotes `""`.

Below is an example of use, specifying the decompression directory as `B:\Archive`, the password list as `B:/pass.txt`, and the number of running processes as 50:

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



# FAQ

When the software encounters errors during operation, first check the common problems and solutions summarized below. Then check whether there are the same problems in all [Issues](https://github.com/hxz393/BrutalityExtractor/issues). If it doesn't help, you can submit a new [Issue](https://github.com/hxz393/BrutalityExtractor/issues) and attach the relevant log files.

## The window is not normal after maximizing

The collapse and expansion do not automatically adapt to the window height in full-screen mode.

**Reason**: Due to the framework used, full-screen mode is not supported.

Solution: Welcome to provide a solution.



## Add batch compression function

No. Common compression software uses resources very well when compressing, please try `7z`, `PeaZip`, and other open-source free software.

## Add automatic renaming function

No. Please try professional software, such as `everything`, `PowerToys`, and other excellent free software.



# Update Log

To avoid too long update logs, only the most recent update log is retained.

## Version 1.0.1 (2023.06.12)

Fixes:

1. When reading text, specify to use UTF-8 encoding.



## Version 1.0.0 (2023.06.11)

Released the first version.
