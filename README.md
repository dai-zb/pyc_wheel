2022-08-10   替换wheel包中py文件为pyc文件

指定路径下的py文件，编译成为pyc，并同目录结构复制到指定目录，并打成压缩包（zip格式）

如果当下工程内存在`dist/xxx-*.wheel`，则会生成一个`.dist/xxx-*.wheel`其中偏移文件都被替换成了pyc