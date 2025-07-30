# CustomMarkdownImage

## 开始使用

将整个项目clone下来，删除sample后，放入你的项目中，直接`import CustomMarkdownRenderer as Cmr`即可开始使用

## 如何使用

先使用`style = pillowmd.LoadMarkdownStyles(style路径)`，然后使用`style.Render(markdown内容)`即可快速渲染。若没有style，则可以`pillowmd.MdToImage(内容)`使用默认风格渲染

## 自定义style

见目录下的`how_to……`，里面有进一步指南，也可以进入Q群`498427849`

## 使用例

见目录下各`sample.py`文件

## 图片预览

> 元素预览
![元素预览](https://raw.githubusercontent.com/Monody-S/CustomMarkdownImage/refs/heads/main/preview/预览2.gif)

> 分页+侧边图渲染
![额外效果](https://raw.githubusercontent.com/Monody-S/CustomMarkdownImage/refs/heads/main/preview/预览1.gif)

## 其他

欢迎各位分享你自己的style风格，联系QQ`614675349`，或者直接在GitHub上提交PR


## TODO

LaTex解析
