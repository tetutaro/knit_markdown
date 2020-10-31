# knit_markdown
[UNDER CONSTRUCTION] convert from markdown, ipynb to latex(beamer), docx, pptx using pandoc

## Motivation

- めんどくさい
    - 文章を作成するのに、エディタ（VIM等）でテキストを入力する以上の労力は使いたくない
        - Micro$oftやGoog1eのアプリでプレゼンテーション作りに四苦八苦するのはもうコリゴリ
    - テキスト入力に際しても、Markdown以上の難しい言語を使うのは嫌だ
    - データ分析やMachine LearningをするのにはJupyter Notebook(Lab)を使う
    - Jupyterから画像をダウンロードして貼り付ける作業はもう嫌だ
    - JupyterもMarkdownを使うので、出来ればIpython Notebook(ipynb)から直接プレゼンテーションを作りたい
    - pandocを使うと上記の希望はすべて実現できそうだが、設定などが難しくてなかなか実現できない
    - 設定項目もなるべくなくし、簡単に作成したい
- 綺麗なものが欲しい
    - pandocでMarkdownからPDFを作ると日本語が文字化けする
    - なので日本語用にきちんと設定したLaTeXを使いたい
    - プレゼンテーション用のPDFを作るのにはLaTeXのbeamerを使うが、そのテーマは自分で作った綺麗なものを使いたい
    - できればPowerPointのテーマも自分で設定したい
    - pandocfilterで引用とか参照を綺麗に表示したい
- 作るもの
    - pandoc用filter（panfluteベース）
        - pandocfilterは独特すぎる
    - pandoc用template
    - beamer用theme
    - powerpoint用theme
    - 変換用コマンド

