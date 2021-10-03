# knit_markdown

convert from markdown to PDF (presentation) using pandoc

This tool supports Japanese only

## 特徴

* Markdown を書くだけで、通常のPDFやプレゼンテーション用のPDFを作れる
    * プレゼンテーションの生成には LaTeX の beamer を用いている
* プレゼンテーションのテーマを簡単に変更できる
* 各種参照を簡単に書け、良い感じに出力される
* カラフルなブロックを簡単に作れる
* 生成はコマンド一発

## 必要なもの（テストした環境）

* TexLive 2021 （2018とかでも大丈夫なはず）
    * [この](https://github.com/tetutaro/dotfiles/tree/main/latex)方法でインストールしていることを前提としている
* pandoc 2.14.0.1 （少なくとも 2.11 以上が必要）
    * Linux (Ubuntu) の場合
        * [GitHub Repository](https://github.com/jgm/pandoc/releases) から最新版をダウンロードして入れる
    * Mac OSX の場合
        * `> brew install pandoc`
* Python 3.9.5 （3.7以降であれば大丈夫なはず）
* pipx
    * Linux (Ubuntu) の場合
        * `> /bin/pip3 install pipx --user`
    * Mac OSX の場合
        * `> brew install pipx`
    * `PATH` 環境変数に `${HOME}/.local/bin` を加える
    * `> pipx ensurepath`

## インストール方法

* Linux (Ubuntu) の場合
    * `> sudo ./install_system.sh`
* Mac OSX の場合
    * `> ./install_system.sh`
- `> ./install_user.sh`

## アンインストール方法

* Linux (Ubuntu) の場合
    * `> sudo ./uninstall_system.sh`
* Mac OSX の場合
    * `> ./uninstall_system.sh`
- `> ./uninstall_user.sh`

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

