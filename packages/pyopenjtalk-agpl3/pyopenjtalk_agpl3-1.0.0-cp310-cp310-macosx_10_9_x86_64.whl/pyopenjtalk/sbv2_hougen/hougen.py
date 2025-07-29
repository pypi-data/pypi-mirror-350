
import re

from pyopenjtalk.sbv2_hougen.strenum import StrEnum


class DialectRule(StrEnum):
    """実装されている日本語の喋り方ルール"""

    Standard = "Standard"  # 標準語
    Kansai = "Kansai"  # 近畿方言 (関西弁)
    Kyushu = "Kyushu"  # 九州方言


class SpeakingStyleRule(StrEnum):
    """実装されている日本語の喋り方ルール"""

    # fmt: off
    # 音素・モーラの置換系
    ConvertBToV = "ConvertBToV"                  # バ行をヴァ行に変換する
    ConvertTToTs = "ConvertTToTs"                # タ行をツァ行に変換する
    ConvertDToR = "ConvertDToR"                  # ダ行をラ行に変換し (ヂを除く) 、アクセントを平型にする
    ConvertRToD = "ConvertRToD"                  # ラ行をダ行に変換し (リを除く) 、アクセントを頭高型にする
    ConvertSToZ = "ConvertSToZ"                  # サ行をザ行に、シャ行をジャ行に変換し、アクセントを頭高型にする
    ConvertToHatsuonbin = "ConvertToHatsuonbin"  # 単語の先頭以外の "na", "no", "ra", "ru" を "N" に変換する (撥音便化)
    # 1モーラ目の音韻操作系
    ExtendFirstMora = "ExtendFirstMora"          # 文章の1モーラ目を長音化し、アクセントを頭高型にする
    GeminationFirstMora = "GeminationFirstMora"  # 文章の1モーラ目を促音化し、アクセントを頭高型にする
    RemoveFirstMora = "RemoveFirstMora"          # 文章の1モーラ目を "っ" に変換し、アクセントを平型にする
    DiphthongFirstMora = "DiphthongFirstMora"    # 各単語の最初を連母音にし、アクセントを頭高型にする ("e" は "ei", "o" は "ou" になる)
    # アクセント操作系
    LastMoraAccentH = "LastMoraAccentH"          # 最後の単語の終端のモーラをアクセント核にする
    LastWordAccent1 = "LastWordAccent1"          # 最後の単語のアクセントを頭高型にする
    # 拗音追加系
    AddYouonA = "AddYouonA"                      # 各単語に最初にア段が出てきた時、"ァ" をつけ "ァ" をアクセント核にする
    AddYouonI = "AddYouonI"                      # 各単語に最初にイ段が出てきた時、"ィ" をつけアクセントを頭高型にする
    AddYouonE = "AddYouonE"                      # 各単語に最初にエ段が出てきた時、"ェ" をつけ "ェ" をアクセント核にする
    AddYouonO = "AddYouonO"                      # 各単語に最初にオ段が出てきた時、"ぉ" をつけアクセントを頭高型にする
    # 特殊な話し方
    BabyTalkStyle = "BabyTalkStyle"              # "s" を "ch" に変換する (幼児語風)
    # fmt: on


# 事前に正規表現パターンをコンパイル
__KYUSHU_HATSUON_PATTERN = re.compile("[ヌニムモミ]+")
__YOUON_PATTERN = re.compile("[ァィゥェォャュョヮ]+")
__A_DAN_PATTERN = re.compile("[アカサタナハマヤラワガダバパ]|[ャヮ]+")
__I_DAN_PATTERN = re.compile("[イキシチニヒミリギジビピ]|ィ+")
__E_DAN_PATTERN = re.compile("[エケセテネヘメレゲデベペ]|ェ+")
__O_DAN_PATTERN = re.compile("[オコソトノホモヨロゴゾドボポ]|[ョォ]+")


def apply_dialect_diff(
    kata_list: list[str],
    accent_list: list[str | int],
    pos_list: list[str],
    dialect_rule: DialectRule,
    speaking_style_rules: list[SpeakingStyleRule],
) -> tuple[list[str], list[str | int]]:
    """
    NHK 日本語アクセント辞典を参考に、日本語方言や話者特有の訛り・アクセントの差分を適用する。
    区分は付録 NHK 日本語アクセント辞典 125p を参照した。
    持っていない人のためにも、細かくコメントを残しておく。

    Args:
        kata_list (list[str]): 単語単位の単語のカタカナ読みのリスト
        accent_list (list[str]): 単語単位の単語のアクセントのリスト
        pos_list (list[str]): 単語単位の単語の品詞 (Part-Of-Speech) のリスト
        dialect_rule (DialectRule): 適用対象の方言ルール。
            例えば DialectRule.Kansai 指定時はアクセントが京阪式になる。
        speaking_style_rules (list[SpeakingStyleRule]): 適用対象の喋り方ルールのリスト。
            例えば SpeakingStyleRule.ConvertBToV はバ行をヴァ行に変換し、外国語風の訛りを作る。

    Returns:
        tuple[list[str], list[str]]: 修正された kata_list と accent_list
    """

    """
    日本語方言の区分は以下の通り。
    - 本土方言
        - 八丈方言
        - 東部方言
        - 西部方言
            - 近畿方言 => DialectRule.Kansai
        - 九州方言 => DialectRule.Kyushu

    以下、厳密でない方言もしくは喋り方 (SpeakingStyleRule) の実装。
    - ConvertBToV: モーラ "b" を "v" に変換する
    - ConvertTToTs: モーラ "t" を "ts" に変換する
    - ConvertDToR: モーラ "d" を "r" に変換し、アクセントを平型にする
    - ConvertRToD: モーラ "r" を "d" に変換し、アクセントを頭高型にする
    - ConvertSToZ: モーラ "s" を "z" に、モーラ "sh" を "j" に変換し、アクセントを頭高型にする
    - ConvertToHatsuonbin: 単語の先頭以外の "na", "no", "ra", "ru" を "N" に変換する (撥音便化)

    - ExtendFirstMora: 文章の1モーラ目を長音化し、アクセントを頭高型にする / "やはり、" => "やーはり" (HLLL)
    - GeminationFirstMora: 文章の1モーラ目を促音化し、アクセントを頭高型にする / "やはり、" => "やっはり" (HLLL)
    - RemoveFirstMora: 文章の1モーラ目を "っ" に変換し、アクセントを平型にする / "やはり、" => "っはり" (LHH)
    - DiphthongFirstMora: 各単語の最初を連母音にし、アクセントを頭高型にする ("e" は "ei", "o" は "ou" になる) /
      "俺のターン。" => "おぅれのターン" / "先生。" => "せぃんせい"

    - LastMoraAccentH: 最後の単語の終端のモーラをアクセント核にする
    - LastWordAccent1: 最後の単語のアクセントを頭高型にする

    - AddYouonA: 各単語に最初にア段が出てきた時、"ァ" をつけ "ァ" をアクセント核にする /
      "そうさ、ボクの仕業さ。悪く思うなよ" => "そうさぁ。ボクの仕業さぁ。わぁるく思うなぁよ"
      ("ァ" は "ア" に置き換えられるので "ー" でも "ア" でもよいが、わかりやすくするため "ァ" とした)
    - AddYouonI: 各単語に最初にイ段が出てきた時、"ィ" をつけアクセントを頭高型にする /
      "しまった。にげられた。" => "しぃまった。にぃげられた"
    - AddYouonE: 各単語に最初にエ段が出てきた時、"ェ" をつけ "ェ" をアクセント核にする /
      "へえ、それで" => "へェえ、それェでェ"
    - AddYouonO: 各単語に最初にオ段が出てきた時、"ぉ" をつけアクセントを頭高型にする /
      "ようこそ。" => "よぉうこぉそ。"

    - BabyTalkStyle: "s" を "ch" に変換する (幼児語風)
      (幼児語のネイティブ話者つまり幼児の喋る幼児語でなく、我々大人の喋る (イメージする) 幼児語である)
    """

    # 九州方言
    if dialect_rule == DialectRule.Kyushu:
        for i in range(len(kata_list)):
            # 九州のほぼ全域で "e" を "ye" と発音する: 付録 131p
            kata_list[i] = kata_list[i].replace("エ", "イェ")

            # 九州のほぼ全域で "s e" を "sh e", "z e" を "j e" と発音する: 付録 132p
            kata_list[i] = kata_list[i].replace("セ", "シェ")
            kata_list[i] = kata_list[i].replace("ゼ", "ジェ")

            # 発音化: 語末の "ヌ", "ニ", "ム", "モ, "ミ" などが発音 "ンN" で表される: 付録 132p
            num = len(kata_list[i])
            if __KYUSHU_HATSUON_PATTERN.fullmatch(kata_list[i][num - 1]):
                kata_list[i] = kata_list[i][: num - 1] + "ン"

    # 近畿方言 (関西弁)
    if dialect_rule == DialectRule.Kansai:
        for i in range(len(kata_list)):
            # 1泊の名詞を長音化し2泊で発音する
            if pos_list[i] == "名詞" and len(kata_list[i]) == 1:
                if kata_list[i] in ["!", "?", "'"]:
                    kata_list[i] = kata_list[i] + "ー"

    # ここから特に参考資料はないが表現の幅が広がったり、話者の特性を再現できそうなもの

    # バ行をヴァ行に変換する
    if SpeakingStyleRule.ConvertBToV in speaking_style_rules:
        for i in range(len(kata_list)):
            if "バ" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("バ", "ヴァ")
            if "ビ" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("ビ", "ヴィ")
            if "ブ" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("ブ", "ヴ")
            if "ベ" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("ベ", "ヴェ")
            if "ボ" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("ボ", "ヴォ")

    # タ行をツァ行に変換する
    if SpeakingStyleRule.ConvertTToTs in speaking_style_rules:
        for i in range(len(kata_list)):
            if "タ" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("タ", "ツァ")
            if "チ" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("チ", "ツィ")
            if "テ" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("テ", "ツェ")
            if "ト" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("ト", "ツォ")

    # ダ行をラ行に変換し (ヂを除く) 、アクセントを平型にする
    if SpeakingStyleRule.ConvertDToR in speaking_style_rules:
        for i in range(len(kata_list)):
            if "ダ" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("ダ", "ラ")
            if "デ" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("デ", "レ")
            if "ド" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("ド", "ロ")
            # アクセントを平型に変更
            accent_list[0] = 0

    # ラ行をダ行に変換し (リを除く) 、アクセントを頭高型にする
    if SpeakingStyleRule.ConvertRToD in speaking_style_rules:
        for i in range(len(kata_list)):
            if "ラ" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("ラ", "ダ")
            if "レ" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("レ", "デ")
            if "ロ" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("ロ", "ド")
            # アクセントを頭高型に変更
            accent_list[0] = 1

    # サ行をザ行に、シャ行をジャ行に変換し、アクセントを頭高型にする
    if SpeakingStyleRule.ConvertSToZ in speaking_style_rules:
        for i in range(len(kata_list)):
            if "サ" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("サ", "ザ")
            if "スィ" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("スィ", "ズィ")
            if "ス" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("ス", "ズ")
            if "セ" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("セ", "ゼ")
            if "ソ" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("ソ", "ゾ")
            if "シャ" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("シャ", "ジャ")
            if "シ" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("シ", "ジ")
            if "シュ" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("シュ", "ジュ")
            if "シェ" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("シェ", "ジェ")
            if "ショ" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("ショ", "ジョ")
            # アクセントを頭高型に変更
            accent_list[0] = 1

    # 単語の先頭以外の "na", "no", "ra", "ru" を "N" に変換する (撥音便化)
    if SpeakingStyleRule.ConvertToHatsuonbin in speaking_style_rules:
        for i in range(len(kata_list)):
            # 1文字以外の時
            if len(str(kata_list[i])) != 1:
                # 各単語先頭と終端は置き換えない
                if "ナ" in str(kata_list[i][1:-1]):
                    kata_list[i] = kata_list[i].replace("ナ", "ン")
                elif "ノ" in str(kata_list[i][1:-1]):
                    kata_list[i] = kata_list[i].replace("ノ", "ン")
                # 一種ずつしか撥音化しない
                elif "ル" in str(kata_list[i][1:-1]):
                    kata_list[i] = kata_list[i].replace("ル", "ン")
                elif "ラ" in str(kata_list[i][1:-1]):
                    kata_list[i] = kata_list[i].replace("ラ", "ン")

    # "s" を "ch" に変換する (幼児語風)
    if SpeakingStyleRule.BabyTalkStyle in speaking_style_rules:
        for i in range(len(kata_list)):
            if "サ" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("サ", "チャ")
            if "シ" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("シ", "チ")
            if "ス" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("ス", "チュ")
            if "セ" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("セ", "チェ")
            if "ソ" in str(kata_list[i]):
                kata_list[i] = kata_list[i].replace("ソ", "チョ")

    # 各単語に最初にア段が出てきた時、"ァ" をつけ "ァ" をアクセント核にする
    if SpeakingStyleRule.AddYouonA in speaking_style_rules:
        for i in range(len(kata_list)):
            pos = __A_DAN_PATTERN.search(str(kata_list[i]))
            if pos:
                kata_list[i] = (
                    kata_list[i][: pos.end()] + "ァ" + kata_list[i][pos.end() :]
                )
                if type(pos.end()) == int:
                    # ァがアクセント核になる
                    accent_list[i] = pos.end()

    # 各単語に最初にイ段が出てきた時、"ィ" をつけアクセントを頭高型にする
    if SpeakingStyleRule.AddYouonI in speaking_style_rules:
        for i in range(len(kata_list)):
            pos = __I_DAN_PATTERN.search(str(kata_list[i]))
            if pos:
                # マッチした語が最後の以外で　シャ　等　マッチした文字の後に拗音が来ない場合
                if (
                    len(str(kata_list[i])) > pos.end()
                    and kata_list[i][pos.end()] != "ャ"
                ):
                    kata_list[i] = (
                        kata_list[i][: pos.end()] + "ィ" + kata_list[i][pos.end() :]
                    )
                    if type(pos.end()) == int:
                        # アクセントを頭高型にする。
                        accent_list[i] = 1
                # 上記以外のャが入っていない条件
                elif "ャ" not in kata_list[i]:
                    kata_list[i] = (
                        kata_list[i][: pos.end()] + "ィ" + kata_list[i][pos.end() :]
                    )
                    if type(pos.end()) == int:
                        # アクセントを頭高型にする
                        accent_list[i] = 1

    # 各単語に最初にエ段が出てきた時、"ェ" をつけ "ェ" をアクセント核にする
    if SpeakingStyleRule.AddYouonE in speaking_style_rules:
        for i in range(len(kata_list)):
            pos = __E_DAN_PATTERN.search(str(kata_list[i]))
            if pos:
                kata_list[i] = (
                    kata_list[i][: pos.end()] + "ェ" + kata_list[i][pos.end() :]
                )
                # ェがアクセント核になる
                if type(pos.end()) == int:
                    accent_list[i] = pos.end()

    # 各単語に最初にオ段が出てきた時、"ぉ" をつけアクセントを頭高型にする
    if SpeakingStyleRule.AddYouonO in speaking_style_rules:
        for i in range(len(kata_list)):
            pos = __O_DAN_PATTERN.search(str(kata_list[i]))
            if pos:
                kata_list[i] = (
                    kata_list[i][: pos.end()] + "ォ" + kata_list[i][pos.end() :]
                )
                # アクセントを頭高型にする。
                if type(pos.end()) == int:
                    accent_list[i] = 1

    # 文章の1モーラ目を長音化し、アクセントを頭高型にする
    if SpeakingStyleRule.ExtendFirstMora in speaking_style_rules:
        pos = __YOUON_PATTERN.search(str(kata_list[0]))
        if pos:
            # マッチしたパターンが二文字目から(一文字文字以内の場合)
            if pos.start() == 1:
                kata_list[0] = (
                    kata_list[0][: pos.end()] + "ー" + kata_list[0][pos.end() :]
                )
        else:
            kata_list[0] = kata_list[0][0] + "ー" + kata_list[0][1:]
        # アクセントを頭高型に変更
        accent_list[0] = 1

    # 文章の1モーラ目を促音化し、アクセントを頭高型にする
    if SpeakingStyleRule.GeminationFirstMora in speaking_style_rules:
        pos = __YOUON_PATTERN.search(str(kata_list[0]))
        if pos:
            # マッチしたパターンが二文字目から (一文字文字以内の場合)
            if pos.start() == 1:
                kata_list[0] = (
                    kata_list[0][: pos.end()] + "ッ" + kata_list[0][pos.end() :]
                )
        else:
            kata_list[0] = kata_list[0][0] + "ッ" + kata_list[0][1:]
        # アクセントを頭高型に変更
        accent_list[0] = 1

    # 文章の1モーラ目を "っ" に変換し、アクセントを平型にする
    if SpeakingStyleRule.RemoveFirstMora in speaking_style_rules:
        pos = __YOUON_PATTERN.search(str(kata_list[0]))
        if pos:
            # マッチしたパターンが二文字目からでかつ伸ばす必要がある (一文字文字以内の場合)
            if pos.start() == 1:
                kata_list[0] = "ッ" + kata_list[0][pos.end() :]
        else:
            kata_list[0] = "ッ" + kata_list[0][1:]

    # 各単語の最初を連母音にし、アクセントを頭高型にする ("e" は "ei", "o" は "ou" になる)
    if SpeakingStyleRule.DiphthongFirstMora in speaking_style_rules:
        pos = __O_DAN_PATTERN.search(str(kata_list[0]))
        if pos:
            kata_list[0] = kata_list[0][: pos.end()] + "ゥ" + kata_list[0][pos.end() :]
            # アクセントを頭高型に
            if type(pos.end()) == int:
                accent_list[0] = 1
        else:
            pos = __E_DAN_PATTERN.search(str(kata_list[0]))
            if pos:
                kata_list[0] = (
                    kata_list[0][: pos.end()] + "ィ" + kata_list[0][pos.end() :]
                )
                # アクセントを頭高型に
                if type(pos.end()) == int:
                    accent_list[0] = 1

    # 最後の単語の終端のモーラをアクセント核にする
    if SpeakingStyleRule.LastMoraAccentH in speaking_style_rules:
        last_word = kata_list[len(kata_list) - 1]
        accent_list[len(accent_list) - 1] = len(last_word)

    # 最後の単語のアクセントを頭高型にする
    if SpeakingStyleRule.LastWordAccent1 in speaking_style_rules:
        accent_list[len(accent_list) - 1] = 1

    return kata_list, accent_list

    # openjtalk only support single accent? 

    # openjtalk/src/njd_node.c line 532
    #  get_token_from_string(buff_acc, &index_acc, buff, '/');
    #  if (buff[0] == '\0') {
    #     j = 0;
    #     fprintf(stderr, "WARNING: NJDNode_load() in njd_node.c: Accent is empty.\n");
    #  } else {
    #     j = atoi(buff);
    #}
    #NJDNode_set_acc(node, j);

    # なので結合も考えて
    # 二音のall high は　頭高型 3音以上は　平型
    # all lowは　尾高にする

def apply_keihan_accent_diff(
    kata_list: list[str],
    accent_list: list[str | int],
    pos_list: list[str],
) -> list[str | int]:
    """
    NHK 日本語アクセント辞典を参考に、京阪式アクセントの差分を適用する。
    東京式と京阪式の対応表は付録 146p を参照した。
    持っていない人のためにも、細かくコメントを残しておく。

    Args:
        kata_list (list[str]): 単語単位の単語のカタカナ読みのリスト
        accent_list (list[str]): 単語単位の単語のアクセントのリスト
        pos_list (list[str]): 単語単位の単語の品詞 (Part-Of-Speech) のリスト
    Returns:
        accent_list (list[str]): 修正された accent_list
    """

    for i in range(len(pos_list)):
        # 分類が名詞の場合
        if pos_list[i] == "名詞":
            # 一音の場合(長音可で2泊化)されている
            if len(kata_list[i]) == 2 and kata_list[i][1] == "ー":
                # 平型の場合頭高型に
                if accent_list[i] == 0:
                    accent_list[i] = 1

                # 頭高型の場合全て低く
                if accent_list[i] == 1:
                    accent_list[i] = 2

            # ニ音の場合
            elif len(kata_list[i]) == 2:

                # 平型の場合全て高く
                if accent_list[i] == 0:
                    accent_list[i] = 1

                # 尾高型の場合頭高型に
                if accent_list[i] == 2:
                    accent_list[i] = 1

        # 分類が動詞の場合
        elif pos_list[i] == "動詞":
            # ニ音の場合
            if len(kata_list[i]) == 2:

                # 平型の場合全て高く
                if accent_list[i] == 0:
                    accent_list[i] = 0

                # 頭高型の場合尾高型に？(忘れた)
                if accent_list[i] == 1:
                    accent_list[i] = 2

            # 三音の場合
            if len(kata_list[i]) == 3:

                # 平型の場合全て高く
                if accent_list[i] == 0:
                    accent_list[i] = 0

                # 中高型の場合尾高型に
                if accent_list[i] == 2:
                    accent_list[i] = 3

        # 分類が形容詞の場合
        elif pos_list[i] == "形容詞":
            # ニ音の場合
            if len(kata_list[i]) == 2:
                # 頭高型の場合尾高型に
                if accent_list[i] == 1:
                    accent_list[i] = 2
            # 三音の場合
            if len(kata_list[i]) == 3:
                # 平型の場合頭高に
                if accent_list[i] == 0:
                    accent_list[i] = 1
                # 中高型の場合頭高に
                if accent_list[i] == 2:
                    accent_list[i] = 1

    return accent_list