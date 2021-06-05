# knit_markdown

convert from markdown to PDF (presentation) using pandoc

This tool supports Japanese only

## 特徴

- Markdown を書くだけで、通常のPDFやプレゼンテーション用のPDFを作れる
    - プレゼンテーションの生成には LaTeX の beamer を用いている
- プレゼンテーションのテーマを簡単に変更できる
- 各種参照を簡単に書け、良い感じに出力される
- カラフルなブロックを簡単に作れる
- 生成はコマンド一発

## 必要なもの（テストした環境）

- Tex Live 2021 （2018とかでも大丈夫なはず）
- pandoc 2.14.0.1 （少なくとも 2.11 以上が必要）
- Python 3.9.5 （3.7以降であれば大丈夫なはず）
- panflute 2.1.0 （pandocのバージョンに対応したもの）

## インストール方法

- `> ./install.sh`

## アンインストール方法

- `> ./uninstall.sh`

## 使い方

```
knit_markdown [-h] [-c] filename

positional arguments:
  filename     file to convert

optional arguments:
  -h, --help   show this help message and exit
  -c, --clean  remove intermediate files
```

- ファイル名が `*.beamer.md` の場合
    - beamer を用いて、縦横比が 4:3 のプレゼンテーションを作成
- ファイル名が `*.beamer169.md` の場合
    - beamer を用いて、縦横比が 16:9 のプレゼンテーションを作成
- ファイル名が上記に該当せず `*.md` の場合
    - 通常のPDFを作成

## インストールされるもの

- pandoc 用テンプレート
    - `~/.pandoc/templates` 以下
- pandoc 用フィルタ
    - Python package `kmd-filters`
- beamer 用テーマ
    - `kpsewhich -var-value=TEXMFLOCAL` の値を `${TEXMFLOCAL}` とすると
    - `${TEXMFLOCAL}/tex/latex/beamer/themes` 以下
- 変換コマンド
    - Python package `knit-markdown`

## 準備（Macの場合）

### Tex Live

- `> brew cask install basictex`
- `> brew install ghostscript`
- `> eval "$(/usr/libexec/path_helper)"`
- `/usr/libexec/path_helper` の結果を `.zshrc` 等に追加する
- `> sudo tlmgr update --self --all`
- `> sudo tlmgr paper a4`
- `> sudo tlmgr repository add http://contrib.texlive.info/current tlcontrib`
- `> sudo tlmgr pinning add tlcontrib "*"`
- `> sudo tlmgr install collection-langjapanese`
- `> sudo tlmgr install collection-fontsrecommended`
- `> sudo tlmgr install collection-latexextra`
- `> sudo tlmgr install collection-fontsextra`
- `> sudo tlmgr install latexmk`
- `> sudo tlmgr install japanese-otf-nonfree`
- `> sudo tlmgr install japanese-otf-uptex-nonfree`
- `> sudo tlmgr install cjk-gs-integrate-macos`
- `> sudo tlmgr install ptex-fontmaps-macos`
- `> sudo tlmgr install noto`
- `> sudo tlmgr install biblatex`
- `> sudo tlmgr install biber`
- `> sudo cjk-gs-integrate --link-texmf --cleanup`
- `> sudo cjk-gs-integrate-macos --link-texmf`
- `kpsewhich -var-value TEXMFLOCAL` の結果を以降 `${TEXMFLOCAL}` とする
- `> cd ${TEXMFLOCAL}`
- `> cd ..`
- `> sudo chown -R ${USER}:admin texmf-local`
- `${TEXMFLOCAL}/../texmf.cnf` に以下を追加

```
shell_escape_commands = \
bibtex,bibtex8,bibtexu,upbibtex,biber,\
kpsewhich, makeindex,mendex,texindy,\
mpost,upmpost,\
repstopdf,epspdf,extractbb
```

- `$TEXMFLOCAL/fonts/map/dvipdfmx/noto/map` を以下のように作成

```
uprml-h unicode NotoSansCJKjp-Regular.otf
uprml-v unicode NotoSansCJKjp-Regular.otf
upgbm-h unicode NotoSansCJKjp-Bold.otf
upgbm-v unicode NotoSansCJKjp-Bold.otf
```

### pandoc

- `> brew install pandoc`

### panflute

- `> pip install panflute`

### latexmk の設定

`~/.latexmkrc` を以下のように作成

```
$latex = 'uplatex -file-line-error -halt-on-error -interaction=nonstopmode -synctex=1 %O %S';
$biber = 'biber %O --bblencoding=utf8 -u -U --output_safechars %B';
$bibtex = 'upbibtex %O %B';
$makeindex = 'upmendex %O -o %D %S';
$dvipdf = 'dvipdfmx -f noto.map %O -o %D %S';
$max_repeat = 3;
$pdf_mode = 3;
$pvc_view_file_via_temporary = 0;
if ($^O eq 'darwin') {
    $pdf_previewer = 'open -ga /Applications/Skim.app';
} elsif ($^O eq 'linux') {
    $pdf_previewer = 'xdg-open';
}
```

（上記はMacでのPDFビューアーとして Skim を用いる場合）

### Skim

- `> brew install skim`

## ヘッダの書き方

各 Markdown の先頭に YAML を書くことによって、タイトルなどのヘッダを生成できる。YAML は `---` という行で囲む必要がある。

（例）
```
---
title: タイトル
subtitle: サブタイトル
author: 著者
institute: 所属
date: \jtoday
pandoctheme: bluewave
themetype: a
bib: sample.bib
---
```

- `title`: タイトル
- `subtitle`: サブタイトル
- `author`: 著者
- `institute`: 所属
    - beamerのみ
- `data`: 日付
    - `\jtoday`とすることで `YYYY/MM/DD` 形式のコンパイル当日の日付になる
- `pandoctheme`: beamerのテーマ名
    - beamerのみ
    - `bluewave`, `greenleaf`, `redflower`, `whitesnow` のいずれか
- `themetype`: beamerのテーマ内のタイプ
    - beamerのみ
    - `a`, `b`, `c` のいずれか
- `bib`: 参考文献が書かれたファイル名
    - 必要な場合のみ
    - 本文中で参照があった参考文献のみが表示される
    - 書き方は [Wikipedia - BibTex](https://ja.wikipedia.org/wiki/BibTeX) に詳しい

## Markdown の書き方

[sampleディレクトリ](samples) 内の md ファイル、
もしくはそれを `knit_markdown` で変換したPDFを参照のこと

## beamer テーマのサンプル

### bluewave - a

![](beamer/samples/bw169a.gif)

### bluewave - b

![](beamer/samples/bw169b.gif)

### bluewave - c

![](beamer/samples/bw169c.gif)

### greenleaf - a

![](beamer/samples/gl169a.gif)

### greenleaf - b

![](beamer/samples/gl169b.gif)

### greenleaf - c

![](beamer/samples/gl169c.gif)

### redflower - a

![](beamer/samples/rf169a.gif)

### redflower - b

![](beamer/samples/rf169b.gif)

### redflower - c

![](beamer/samples/rf169c.gif)

### whitesnow - a

<img src="beamer/samples/ws169a.gif" width=534>

### whitesnow - b

<img src="beamer/samples/ws169b.gif" width=534>

### whitesnow - c

<img src="beamer/samples/ws169c.gif" width=534>

