# [English](https://github.com/hxz393/BrutalityExtractor/blob/main/README_EN.md) | [中文](https://github.com/hxz393/BrutalityExtractor/blob/main/README.md)

# Introduction

BrutalityExtractor is a multiprocess unzipping software designed for high-performance systems. Optimized for modern multicore processors and high-speed solid-state drives, its batch decompression speed is more than 5 times higher than that of common decompression software, fully utilizing the performance of computer hardware.

Features:

- Batch decompression: Automatically scans and decompresses all compressed files in the specified directory, even if the file extension is incorrect.
- Supports multiple formats: Supports common compression file formats `7z`, `zip`, `rar`, `tar`, `gz`, `xz`, `bz2` and can properly handle split compressed files.
- Supports multiprocessing: Customize the number of decompression processes based on the processor thread count, doubling the decompression speed.
- Supports password lists: You can set a list of common passwords to automatically match encrypted compressed files.
- Additional features: Includes useful functions such as removing directory redundancy, deleting empty directories, and deleting junk files.

Screenshot:

![newest screenshot](https://raw.githubusercontent.com/hxz393/BrutalityExtractor/main/capture/ui-en.jpg)

Command-Line:

![command-line screenshot](https://raw.githubusercontent.com/hxz393/BrutalityExtractor/main/capture/cli-en.jpg)

## System Requirements

Please read carefully the following usage limitations of the software.

### OS

The software development and compilation environment is `Win10 x64` Professional Workstation Edition, version `22H2`. Users with `Win10 x64` or above can directly use the software.

Lower versions such as `Win 7` and `Win XP` are not supported due to the use of `Python 3.10`.

In theory, other operating systems can manually compile into executable files. For the compilation process, please refer to the Self-packaging section below.

### Processor

When the processor configuration is less than 2 cores and 4 threads, the software will run in single-process mode, with no speed increase.

When the processor configuration is more than 2 cores and 4 threads, for stability considerations, the maximum number of processes that can be set by the software does not exceed half of the processor thread count.

Of course, you can choose to run multiple instances of the software, essentially ignoring this limit. However, this could potentially cause system crashes, data loss, and other side effects. Please assess the impact yourself.

### Memory

The memory requirements are quite flexible, as it is impossible to evaluate the actual memory needed at runtime. The memory required for decompression is determined by factors such as the file compression format, compression algorithm, and whether solid compression is used. When the memory is full, decompression failures, program errors, and system anomalies may occur.

It is recommended to manually decompress compressed files that are single or split volumes larger than 4GB. This is because decompressing these types of files may consume a lot of memory, and the current software does not speed up the decompression of large compressed packages.

The strategy of using multi-threading to speed up the decompression of large compressed packages is being evaluated. If the results are good, it will be included in subsequent updates.

### Hard Disk

If you're using a traditional mechanical hard drive, no matter how high the processor or memory is, neither this software nor any other software can make the decompression speed exceed the read-write speed of the hard drive.

Using a solid-state drive with a `PCI-E 3.0 x4` or higher interface is still being restricted to the speed of mechanical hard drives by other decompression software, which is a significant waste of performance. This software does not invent a new decompression algorithm to increase speed, but by running multiple processes, it moves the performance bottleneck to the processor.

A general table of hard disk specifications and corresponding process numbers is as follows:

| Hard Disk         | Process | Description                                                                                                                                  |
|-------------------|---------|----------------------------------------------------------------------------------------------------------------------------------------------|
| HDD SATA 3.0 18TB | 2       | High-performance HDD with R/W speed over 200MB/s, barely sufficient to run 2 processes                                                       |
| SSD SATA 3.0 4TB  | 4       | High-performance SATA SSD, with maximum R/W speed of 500MB/s, can run 4 processes                                                            |
| SSD PCI-E 1TB     | 8~64    | Common m.2 SSD, usually having a R/W speed over 1GB/s, with great performance variation. Adjust process number according to actual situation |

## Download Links

Software download methods:

- Method 1: Go to the [release](https://github.com/hxz393/BrutalityExtractor/releases) page to download the latest executable file, named `BrutalityExtractor.exe` or `BrutalityExtractorCli.exe`. It can be used directly after download.
- Method 2: [Direct link](https://www.x2b.net/download/BrutalityExtractor.7z) download.

The downloaded compressed file needs to be decompressed before running the executable file, otherwise the configs will not be saved.

## Self-packaging

Manual compilation requires to be pre-installed `Python 3.10` or higher and the `pyinstaller` lib. Install other dependencies as needed, always using the latest version.

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

- Decompression core: [7z](https://www.7-zip.org/)
- File recognition: [magic](https://github.com/ahupp/python-magic)
- Theme beautification: [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap)
- Icon generation: [tkfontawesome](https://github.com/israel-dryer/TkFontAwesome)

# Usage

When you first run the software, the interface will be in English due to the lack of a configuration file. You can expand the Appearance Settings and switch the language under Language. The software needs to be restarted to apply the changes.

## Basic Settings

Extraction Directory or Destination Directory is a mandatory field.

- **Extraction Directory**

  Enter or select the directory where the compressed files are stored, such as `B:\Archive` or `B:/Archive/`, both of which can be recognized normally.

  It's best not to put irrelevant files in the directory, otherwise, unexpected decompression behavior may occur, such as decompressing the game resource pack file `resources.pak`, causing the game to fail to run.

- **Destination Directory**

  Enter the directory where the decompressed files will be stored. The structure of the decompressed directory will be consistent with that in the extraction directory. For example, `B:/Archive/xd1/test.zip` will be decompressed to `B:/New/xd1/test`, if destination directory is `B:/New`.

  Setting the destination directory to a different disk can slightly increase the decompression speed.

- **Decryption Password**

  Enter a single password or the location of the password list text file. If the compressed file does not have a password, any password can be used to decompress it. If there is a password, the software will try the passwords in the list one by one until the correct one is found or all have failed.

  The software itself does not process password attempts with multiple processes. If you need to brute force crack the compressed file password, you can divide the password list into multiple parts and run multiple instances of the software. Set the log level to Debug to see the attempt results in the log. Do not use this feature for illegal purposes.

  To make sure the password is read correctly, please save the text using the `UTF-8` encoding format.

## Advanced Settings

Settings in the advanced configuration need to be adjusted according to actual conditions.

- **Processes**

  Set the number of decompression processes to run at the same time.

- **Ignore Warnings**

  Turn off system resource detection before decompression.

- **Remove Source**

  Delete the compressed file after decompression success. Whether it is turned on or not, the original compressed file will not be deleted if decompression fails.

- **Force Mode**

  Skip file type identification, attempt to decompress all files in the directory.

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

  Change the software display language. Currently, only Chinese and English are available. Welcome to submit reliable translations for other languages. The language dictionary is located at `modules/configs/lang_dict.py`.

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

- **Delete Files (Directories)**

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

Below is an example of use, specifying the decompression directory as `B:\Archive`, the password list as `B:/pass.txt`, and the number of running processes as 16:

```sh
BrutalityExtractorCli.exe -c 16 -d B:\Archive -p B:/pass.txt
```

# FAQ

When the software encounters errors during operation, first check the common problems and solutions summarized below. Then check whether there are the same problems in all [Issues](https://github.com/hxz393/BrutalityExtractor/issues). If it doesn't help, you can submit a new [Issue](https://github.com/hxz393/BrutalityExtractor/issues) and attach the relevant log files.

## The window is not normal after maximizing

The collapse and expansion do not automatically adapt to the window height in full-screen mode.

**Reason**: Due to the framework used, full-screen mode is not supported.

**Solution**: Welcome to provide a solution.

## Add batch compression function

No. Common compression software uses resources very well when compressing, please try `7z`, `PeaZip`, and other open-source free software.

## Add automatic renaming function

No. Please try professional software, such as `everything`, `PowerToys`, and other excellent free software.

# Update Logs

To avoid too long update logs, only the most recent update log is retained.

## Version 1.2.0 (2023.06.28)

Improvements:

1. Added a force mode switch, removing file type restrictions;
2. Updated 7z core program to version 23.1.

Bug fixes:

1. Fixed the issue of sub-processes remaining in the system when exiting the window.

## Version 1.1.0 (2023.06.20)

Improvements:

1. Optimized code structure, improved runtime speed;
2. Merged the functionality of deleting junk files and folders into one feature;
3. Optimized the log recording feature;
4. Added default configuration items.

Bug Fixes:

1. Fixed performance issues caused by the `pathlib` library, replaced it with the `os` library;
2. Fixed a bug that caused accidental deletion of files under specific circumstances.

## Version 1.0.2 (2023.06.15)

Improvements:

1. Change the log writing format to UTF-8;
2. When the total number of files to be decompressed is less than the number of processes, set the number of processes to the number of files.

Bug fixes:

1. Fixed the error in the file deletion count;
2. Fixed the issue of decimal places in file sizes being ignored;
3. Fixed some omitted text.

## Version 1.0.1 (2023.06.12)

Fixes:

1. When reading text, specify to use UTF-8 encoding.

## Version 1.0.0 (2023.06.11)

Released the first version.
