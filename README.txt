# a script get mp3 cover from douban.com

## Requirement

Python2

## Usage

```
python getCover.py /some/path/*.mp3 
```

It works at MacOS / Linux.


## Author Quote

> Python 脚本：自动从豆瓣获取专辑封面
> 
> 明城<i.feelinglucky#gmail.com>
> 2010-01-20
> 
> iTunes 下的显示专辑封面往往被看作是鸡肋，到不是因为它的功能不好用，
> 而是因为很多时候它都找不到中文歌曲的专辑封面。
> 
> 于是乎，就利用周末的时间用 Python 写了这样的一个脚本，用于自动从
> 豆瓣找专辑封面并嵌入至 mp3 文件中。
> 
> 使用方法相对简单，下载压缩包以后，命令行
> 
> python getCover.py *.mp3 
> 
> 即可。这里要说面下 
> 
> 1、文件可写
> 2、ID3 的信息必须清楚，因为搜索 豆瓣 上的专辑插图是以此为依据的
> 3、mp3  的 ID3 标签必须是 id3v2 和 utf-8 编码
> 
> Windows 下可以用 千千静听 批量转换 mp3 文件的 id3，如果在 Mac 平
> 台下，可以考虑使用 ID3Mod 这个工具。
> 
> 脚本在 Mac 下测试通过，理论上说 Windows 以及其他平台都可以正常
> 使用。如果在使用过程中碰到问题，欢迎联系我。
