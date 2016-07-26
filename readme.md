# Stellaris 简单立绘MOD生成器

做Stellaris的MOD的重复工作有点多，比如把`.png`文件变成`.dds`文件，写portrait对应的group之类的。
这个脚本将其统一代劳，你需要的只是按Stellaris的specie(例:哺乳动物) -> portrait_group(例:人类) -> portrait(例:人类的各张具体立绘) 
的级别安排一个文件夹结构，在适当的地方放上`.png`图片即可。然后进入命令行输入这样的命令

```
$ python CLI.py "E:\agent5\stellaris\mod_raw\galgame" "C:\Users\yiyuezhuo\Documents\Paradox Interactive\Stellaris\mod\galgame3"
```

就可以将`E:\agent5\stellaris\mod_raw\galgame`里文件结构与图片决定的MOD，自动填补相关信息，生成到
Stellaris用 MOD tool生成的那个空文件夹`C:\Users\yiyuezhuo\Documents\Paradox Interactive\Stellaris\mod\galgame3`里。

## 文件结构对MOD的影响

类似这样的文件结构
```
MOD_root
--mammal
----human
------human_man_1.png
------human_man_2.png
------human_woman_1.png
----rat
------rat_1.png
------rat_2.png
--galgame
----box
------miz.png
```
而将MOD_root的路径设为脚本的第一个参数后，运行脚本
（当然你之前要先用stellaris的 MOD tool生成空MOD来获得第二个参数的值），
设想你进入游戏后进入自定义种族界面，将发现如下不同。

appearance界面左边的文字类别选择部分将多出mammal与galgame可选。
选择mammal，则右边应当出现一张人的图与一张鼠人的图。
选择鼠人的图后，在ruler选择界面将发现雌雄都可以两个形象，正好就是rat_1.png与rat_2.png。

总之，和那些你见过那些最简单的立绘MOD一样。我试图使用最自然/简单的配置方式来完成这一点。

## 依赖项

* `Python3` (Python2可能可以运行，没有测试过)
* `jinja2`
* `Pillow` (Python标准版带的可能是PIL，可能可以运行，没测试过)

如果你不知道怎么做，最简单的方法就是下一个Anaconda，它携带了所有依赖项，
只是可能太大了(几百MB)。否则你可能需要下Python标准版(十几MB)，再用pip安装上面的依赖项(几MB)。
可能还需要配置环境变量。可能还要受怎么把PIL换成Pillow之苦。
