LANG_DICT = {
    "ENG": {
        "msg_info_title": "Notice",
        "msg_warning_title": "Warning",
        "msg_error_title": "Error",
        "change_language_msg": "Changing the language requires a program restart to take effect",
        "basic_area_title": "Basic Settings",
        "label_path_text": "Extraction Directory:  ",
        "bottom_path_text": "...",
        "tooltip_label_path": "Path for storing compressed files, do not put unrelated files in the directory",
        "tooltip_bottom_path": "Select directory",
        "label_dest_text": "Destination Directory:  ",
        "tooltip_label_dest": "The path for extracted files. If left blank, files will be extracted in place in the extraction directory",
        "label_pass_text": "Decryption Password:  ",
        "bottom_pass_text": "...",
        "tooltip_label_pass": "Leave it blank for no password. Enter a single password or a password text file (one per line), e.g., Abc12# or D:/pass.txt",
        "tooltip_bottom_pass": "Select a file with passwords",
        "advance_area_title": "Advanced Settings",
        "label_para_text": "Processes:  ",
        "tooltip_label_para": "Number of simultaneous decompression processes, not exceeding half of the CPU supported thread number",
        "label_warn_text": "Ignore Warnings:  ",
        "tooltip_label_warn": "Hardware resources will be checked before decompression begins. and if resources are insufficient, the operation will be rejected. Enabling this option will disable the check",
        "label_sdlt_text": "Remove Source:  ",
        "tooltip_label_sdlt": "Delete original compressed files immediately after successful decompression",
        "label_sfrc_text": "Force Mode:  ",
        "tooltip_label_sfrc": "Skip file type detection and attempt to decompress all files in the Extraction Directory",
        "label_logl_text": "Log Level:  ",
        "tooltip_label_logl": "Controls the level of logs written to the log file. After modifying log-related options, the program needs to be restarted to take effect",
        "label_logs_text": "Log Size:  ",
        "tooltip_label_logs": "Log will be split when exceeding the set size. Unit MB",
        "label_logc_text": "Log Count:  ",
        "tooltip_label_logc": "The number of log files retained on the disk",
        "skin_area_text": "Appearance Settings",
        "label_ntlp_text": "Disable Hints:  ",
        "tooltip_label_ntlp": "Disable tooltip information",
        "label_mini_text": "Mini Mode:  ",
        "tooltip_label_mini": "Switch icon size to solve display issues, effect after program restart",
        "label_theme_text": "Theme:  ",
        "tooltip_label_theme": "Change the color theme",
        "label_lang_text": "Language:  ",
        "tooltip_label_lang": "Change display language, requires a program restart to take effect",
        "label_alpha_text": "Alpha:  ",
        "tooltip_label_alpha": "Drag to set the transparency of the window",
        "extra_area_title": "Additional Features",
        "label_extr_text": "Feature Switch:  ",
        "tooltip_label_extr": "Additional feature switch. Disables decompression functionality when enabled, performs the following operations on the destination directory",
        "label_rddd_text": "Eliminate Redundancy:  ",
        "tooltip_label_rddd": "Eliminate redundant directory structure. For example, extract files in D:/zip/zip/zip/ to D:/zip/",
        "label_mpty_text": "Purge Directories:  ",
        "tooltip_label_mpty": "Delete empty directories",
        "label_xclf_text": "Delete Files:  ",
        "tooltip_label_xclf": "Files or folders to be deleted, leave blank to disable. Enter a single name or a text file of names",
        "tooltip_bottom_xclf": "Select a text file with file name list",
        "log_area_title": "Show Logs",
        "bottom_github_text": "Homepage",
        "bottom_update_text": "Check for Updates",
        "bottom_logpath_text": "Open Log File",
        "bottom_run_text": "Start Running",
        "check_update_info_1": "Current Version:  {}\nLatest Version:     {}\n\nPlease visit the homepage to download the latest version",
        "check_update_info_2": "Current Version:  {}\nLatest Version:     {}\n\nYou are using the latest version!",
        "check_update_error_msg": "Network Connection Error",
        "extra_path_dest_warning_msg": "Please enter the correct destination directory",
        "extra_no_action": "No processing needed for directory {}",
        "extra_info_start": "{}Beginning to execute additional features{}",
        "extra_xclf_info": "Deleted {1} junk files under: {0}\n",
        "extra_is_redundant_info": "Deleted {1} redundant directories under: {0}\n",
        "extra_is_empty_info": "Deleted {1} empty directories under: {0}\n",
        "extra_debug_del_list": "The deletion list is as follows:\n{}",
        "extra_error_run": "{}Additional features executed error: {}{}",
        "extra_info_done": "{}Additional features executed successfully{}",
        "extra_bottom_run_text": "Running...",
        "main_info_start": "{}Extracting files{}",
        "main_no_path_zip_warning": "{}Stopped. Please enter the correct Extraction Directory{}",
        "main_no_path_zip_warning_msg": "Please enter the correct Extraction Directory",
        "main_no_file_warning": "{}Scan complete. No files found in directory: {}{}",
        "main_no_file_warning_msg": "No files found in directory: {}",
        "main_path_dest_error": "{}Failed to create destination directory: {}: {}",
        "main_path_dest_error_msg": "Failed to create destination directory: {}. Please don't include forbidden special characters in directory name",
        "main_no_file_infos_warning": "{}Scan complete. No compressed files found in directory {}{}",
        "main_no_file_infos_warning_msg": "No compressed files found in directory {}",
        "disk_free_warning": "The current disk free space is lower than the compressed file size. Continuing the execution may result in:\nsystem instability, decompression failure, and other unknown errors\n\nEnable 'Ignore warnings' to skip disk space check",
        "cpu_usage_warning": "The current CPU usage is above 50%. Continuing the execution may result in:\nsystem freezing, decompression failure, or other program errors\n\nEnable 'Ignore warnings' to skip CPU usage checks",
        "memory_usage_warning": "The current memory usage is above 70%. Continuing the execution may result in:\nsystem error, decompression failure, and other program errors\n\nEnable 'Ignore warnings' to skip memory usage checks",
        "main_info_done": "{}Finished!{}\nTotal compressed files: {} \nFailed decompression: {} \nSuccessful decompression: {} \nTotal compressed file size: {} \nProcesses: {} \nTime spent: {}s \nProcessing speed: {}",
        "main_info_done_msg": "Finished!\nTotal compressed files: {} \nFailed decompression: {} \nSuccessful decompression: {} \nTotal compressed file size: {} \nProcesses: {} \nTime spent: {}s \nProcessing speed: {}",
        "main_error": "{}An error occurred during runtime. Error details below{}\n{}",
        "main_error_msg": "Runtime error. Please report the issue on Github :(",
        "second": "seconds",
        "minute": "minutes",
        "hour": "hours",
        "s": "s",
        "unzip_run_failed": "Command execution failed: {}",
        "unzip_success": "Decompression Success : {}",
        "unzip_failed1": "Decompression Failed : {}, target size mismatch",
        "unzip_failed2": "Decompression Failed : {}, all passwords failed",
        "unzip_failed3": "Decompression Failed : {}, unsupported file type",
        "unzip_failed4": "Decompression Failed : {}, compressed file not found",
        "unzip_failed5": "Decompression Failed : {}, missing volume",
        "unzip_failed6": "Decompression Failed : {}, CRC checksum failed",
        "unzip_failed7": "Decompression Failed : {}, file headers error",
        "unzip_failed8": "Decompression Failed : {}, unexpected end of archive",
        "unzip_failed9": "Decompression Failed : {}, file is corrupted",
        "unzip_failed10": "Decompression Failed : {}, other error",
        "get_target_size_error": "Unable to retrieve size of {}: \n{}",
        "read_json_debug": "Successfully read Json file: {}",
        "read_json_error": "An error occurred while reading Json file {}: \n{}",
        "remove_matched_info": "Target {} matched exclusion list, has been deleted",
        "remove_matched_error": "An error occurred while matching the exclusion list: \n{}",
        "remove_redundant_info": "Completed extraction of redundant directories from target {}",
        "remove_redundant_error": "An error occurred while extracting redundant directories: \n{}",
        "rename_path_error": "Failed to rename target {}: \n{}",
        "RM_cut": "Cut",
        "RM_copy": "Copy",
        "RM_paste": "Paste",
        "RM_select_all": "Select All",
        "RM_delete": "Delete",
        "RM_undo": "Undo",
        "RM_redo": "Redo",
        "test": "Aaaaaaaaaaaaaa!"
    },
    "CHS": {
        "msg_info_title": "提示",
        "msg_warning_title": "警告",
        "msg_error_title": "错误",
        "change_language_msg": "切换语言需要重启程序来生效",
        "basic_area_title": "基础配置",
        "label_path_text": "解压目录：",
        "bottom_path_text": "浏览...",
        "tooltip_label_path": "压缩文件存放路径，目录内别放无关文件",
        "tooltip_bottom_path": "手动选择目录",
        "label_dest_text": "目标目录：",
        "tooltip_label_dest": "解压文件存放路径，不填则在解压目录就地解压",
        "label_pass_text": "解压密码：",
        "bottom_pass_text": "选择...",
        "tooltip_label_pass": "不填为空。输入单个密码或密码文本（一行一个），例如：Abc12# 或 D:/pass.txt",
        "tooltip_bottom_pass": "手动选择密码文件",
        "advance_area_title": "高级配置",
        "label_para_text": "进程数量：",
        "tooltip_label_para": "同时运行解压进程数量，最高不超过 CPU 支持线程数的一半",
        "label_warn_text": "忽略警告：",
        "tooltip_label_warn": "解压开始前会检测硬件信息，如果资源不足会拒绝运行。打开此选项可以关闭检测",
        "label_sdlt_text": "释放空间：",
        "tooltip_label_sdlt": "解压成功后，立即删除原始压缩包文件",
        "label_sfrc_text": "强制模式：",
        "tooltip_label_sfrc": "不检测文件类型，直接对解压目录下所有文件尝试解压",
        "label_logl_text": "日志等级：",
        "tooltip_label_logl": "控制写入日志文件中日志的等级。日志相关选项修改后，要重启程序才能生效",
        "label_logs_text": "日志大小：",
        "tooltip_label_logs": "超过设定大小，将对日志进行分割。单位 MB",
        "label_logc_text": "日志数量：",
        "tooltip_label_logc": "硬盘中保留日志文件的数量",
        "skin_area_text": "外观配置",
        "label_ntlp_text": "关闭提示：",
        "tooltip_label_ntlp": "关闭气泡提示信息",
        "label_mini_text": "迷你模式：",
        "tooltip_label_mini": "切换图标大小用于解决显示错误，重启程序后生效",
        "label_theme_text": "修改主题：",
        "tooltip_label_theme": "修改配色主题",
        "label_lang_text": "修改语言：",
        "tooltip_label_lang": "改变显示语言，需要重启程序来生效",
        "label_alpha_text": "窗口透明：",
        "tooltip_label_alpha": "拖动来设置窗口透明度",
        "extra_area_title": "附加功能",
        "label_extr_text": "功能开关：",
        "tooltip_label_extr": "附加功能开关。开启后关闭解压功能，对目标目录执行下面操作",
        "label_rddd_text": "消除冗余：",
        "tooltip_label_rddd": "消除冗余目录结构。例如将 D:/zip/zip/zip/ 中的文件提取到 D:/zip/",
        "label_mpty_text": "清理目录：",
        "tooltip_label_mpty": "删除空目录，谨慎使用",
        "label_xclf_text": "删除垃圾：",
        "tooltip_label_xclf": "要永久删除的垃圾文件或文件夹，留空不开启。输入单个文件（夹）名或名字列表文本",
        "tooltip_bottom_xclf": "手动选择名字列表文本文件",
        "log_area_title": "显示日志",
        "bottom_github_text": "项目主页",
        "bottom_update_text": "检查更新",
        "bottom_logpath_text": "打开日志",
        "bottom_run_text": "开始运行",
        "check_update_info_1": "当前版本：{}\n最新版本：{}\n\n可以到项目主页下载最新版",
        "check_update_info_2": "当前版本：{}\n最新版本：{}\n\n目前使用的是最新版！",
        "check_update_error_msg": "网络请求错误",
        "extra_path_dest_warning_msg": "请输入正确目标目录",
        "extra_no_action": "目标目录 {} 不需要处理",
        "extra_info_start": "{}附加功能开始执行{}",
        "extra_xclf_info": "删除 {0} 下的垃圾文件 {1} 个。\n",
        "extra_is_redundant_info": "删除 {0} 下的冗余目录 {1} 个。\n",
        "extra_is_empty_info": "删除 {0} 下的空目录 {1} 个。\n",
        "extra_debug_del_list": "删除列表如下：\n{}",
        "extra_error_run": "{}附加功能执行出错：{}{}",
        "extra_info_done": "{}附加功能执行完毕{}",
        "extra_bottom_run_text": "运行中...",
        "main_info_start": "{}开始批量解压缩文件{}",
        "main_no_path_zip_warning": "{}无法运行。请输入正确解压目录{}",
        "main_no_path_zip_warning_msg": "请输入正确解压目录",
        "main_no_file_warning": "{}扫描完毕。目录 {} 下没有文件{}",
        "main_no_file_warning_msg": "目录 {} 下没有文件",
        "main_path_dest_error": "{}运行错误。目标目录 {} 创建失败：{}",
        "main_path_dest_error_msg": "目标目录 {} 创建失败。目录名请勿包含禁止的特殊字符",
        "main_no_file_infos_warning": "{}扫描完毕。目录 {} 下没有压缩文件{}",
        "main_no_file_infos_warning_msg": "目录 {} 下没有压缩文件",
        "disk_free_warning": "目前磁盘剩余空间小于压缩文件大小，继续执行可能导致：\n系统异常、解压失败、其他程序异常等未知错误\n\n打开忽略警告，可以跳过磁盘空间检查",
        "cpu_usage_warning": "目前 CPU 使用率大于 50%，继续执行可能导致：\n系统卡死、解压失败、其他程序异常等未知错误\n\n打开忽略警告，可以跳过 CPU 使用率检查",
        "memory_usage_warning": "目前内存使用率大于 70%，继续执行可能导致：\n系统卡死、解压失败、其他程序异常等未知错误\n\n打开忽略警告，可以跳过内存使用率检查",
        "main_info_done": "{}批量解压缩文件完成{}\n压缩文件总数：{} \n解压失败数量：{} \n解压成功数量：{} \n压缩文件总大小：{} \n进程数：{} \n花费时间：{}秒 \n处理速度：{}",
        "main_info_done_msg": "批量解压缩文件完成\n压缩文件总数：{} \n解压失败数量：{} \n解压成功数量：{} \n压缩文件总大小：{} \n进程数：{} \n花费时间：{}秒 \n处理速度：{}",
        "main_error": "{}运行出错，错误信息如下{}\n{}",
        "main_error_msg": "运行出错，请到 Github 反馈问题:(",
        "second": "秒",
        "minute": "分钟",
        "hour": "小时",
        "s": "秒",
        "unzip_run_failed": "解压命令执行失败: {}",
        "unzip_success": "文件解压成功：{}",
        "unzip_failed1": "文件解压失败：{}，目标大小不匹配",
        "unzip_failed2": "文件解压失败：{}，匹配密码全部失败",
        "unzip_failed3": "文件解压失败：{}，不支持的文件类型",
        "unzip_failed4": "文件解压失败：{}，找不到压缩文件",
        "unzip_failed5": "文件解压失败：{}，缺少分卷",
        "unzip_failed6": "文件解压失败：{}，CRC校验失败",
        "unzip_failed7": "文件解压失败：{}，文件头错误",
        "unzip_failed8": "文件解压失败：{}，文件不完整",
        "unzip_failed9": "文件解压失败：{}，文件已损坏",
        "unzip_failed10": "文件解压失败：{}，其他错误",
        "get_target_size_error": "无法获取 {} 大小：\n{}",
        "read_json_debug": "成功读取 Json 文件: {}",
        "read_json_error": "读取 Json 文件 {} 时发生错误: \n{}",
        "remove_matched_info": "目标 {} 匹配排除列表，已被删除",
        "remove_matched_error": "匹配排除列表时发生错误: \n{}",
        "remove_redundant_info": "目标 {} 提取冗余目录完成",
        "remove_redundant_error": "提取冗余目录时发生错误: \n{}",
        "rename_path_error": "目标 {} 重命名失败: \n{}",
        "RM_cut": "剪切",
        "RM_copy": "复制",
        "RM_paste": "粘贴",
        "RM_select_all": "全选",
        "RM_delete": "删除",
        "RM_undo": "撤销",
        "RM_redo": "重做",
        "test": "啊啊啊啊啊啊啊啊"
    }
}
