#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup
import datetime
from pytz import timezone

country_dict = {'AD': {'companyen': 'Andorra', 'companyjp': 'アンドラ', 'location': '西ヨーロッパ'},
 'AE': {'companyen': 'United+Arab+Emirates',
  'companyjp': 'アラブ首長国連邦',
  'location': '中東'},
 'AF': {'companyen': 'Afghanistan', 'companyjp': 'アフガニスタン', 'location': '中東'},
 'AG': {'companyen': 'Antigua+and+Barbuda',
  'companyjp': 'アンティグア・バーブーダ',
  'location': '中央アメリカ'},
 'AI': {'companyen': 'Anguilla', 'companyjp': 'アンギラ', 'location': '中央アメリカ'},
 'AL': {'companyen': 'Albania', 'companyjp': 'アルバニア', 'location': '東ヨーロッパ'},
 'AM': {'companyen': 'Armenia', 'companyjp': 'アルメニア', 'location': '東ヨーロッパ'},
 'AO': {'companyen': 'Angola', 'companyjp': 'アンゴラ', 'location': '南アフリカ'},
 'AQ': {'companyen': 'Antarctica', 'companyjp': '南極', 'location': '南極'},
 'AR': {'companyen': 'Argentina', 'companyjp': 'アルゼンチン', 'location': '南アメリカ'},
 'AS': {'companyen': 'American+Samoa',
  'companyjp': 'アメリカ領サモア',
  'location': 'オセアニア'},
 'AT': {'companyen': 'Austria', 'companyjp': 'オーストリア', 'location': '東ヨーロッパ'},
 'AU': {'companyen': 'Australia', 'companyjp': 'オーストラリア', 'location': 'オセアニア'},
 'AW': {'companyen': 'Aruba', 'companyjp': 'アルバ', 'location': '中央アメリカ'},
 'AX': {'companyen': 'Åland+Islands',
  'companyjp': 'オーランド諸島',
  'location': '北ヨーロッパ'},
 'AZ': {'companyen': 'Azerbaijan',
  'companyjp': 'アゼルバイジャン',
  'location': '東ヨーロッパ'},
 'BA': {'companyen': 'Bosnia+and+Herzegovina',
  'companyjp': 'ボスニア・ヘルツェゴビナ',
  'location': '東ヨーロッパ'},
 'BB': {'companyen': 'Barbados', 'companyjp': 'バルバドス', 'location': '中央アメリカ'},
 'BD': {'companyen': 'Bangladesh', 'companyjp': 'バングラデシュ', 'location': '南アジア'},
 'BE': {'companyen': 'Belgium', 'companyjp': 'ベルギー', 'location': '西ヨーロッパ'},
 'BF': {'companyen': 'Burkina+Faso',
  'companyjp': 'ブルキナファソ',
  'location': '西アフリカ'},
 'BG': {'companyen': 'Bulgaria', 'companyjp': 'ブルガリア', 'location': '東ヨーロッパ'},
 'BH': {'companyen': 'Bahrain', 'companyjp': 'バーレーン', 'location': '中東'},
 'BI': {'companyen': 'Burundi', 'companyjp': 'ブルンジ', 'location': '中央アフリカ'},
 'BJ': {'companyen': 'Benin', 'companyjp': 'ベナン', 'location': '西アフリカ'},
 'BL': {'companyen': 'Saint+Barthélemy',
  'companyjp': 'サン・バルテルミー',
  'location': '中央アメリカ'},
 'BM': {'companyen': 'Bermuda', 'companyjp': 'バミューダ', 'location': '中央アメリカ'},
 'BN': {'companyen': 'Brunei+Darussalam',
  'companyjp': 'ブルネイ',
  'location': '東南アジア'},
 'BO': {'companyen': 'Bolivia, Plurinational State of',
  'companyjp': 'ボリビア',
  'location': '南アメリカ'},
 'BQ': {'companyen': 'Bonaire,+Saint+Eustatius+and+Saba',
  'companyjp': 'BES諸島',
  'location': '中央アメリカ'},
 'BR': {'companyen': 'Brazil', 'companyjp': 'ブラジル', 'location': '南アメリカ'},
 'BS': {'companyen': 'Bahamas', 'companyjp': 'バハマ', 'location': '中央アメリカ'},
 'BT': {'companyen': 'Bhutan', 'companyjp': 'ブータン', 'location': '南アジア'},
 'BV': {'companyen': 'Bouvet+Island', 'companyjp': 'ブーベ島', 'location': '南極'},
 'BW': {'companyen': 'Botswana', 'companyjp': 'ボツワナ', 'location': '南アフリカ'},
 'BY': {'companyen': 'Belarus', 'companyjp': 'ベラルーシ', 'location': '東ヨーロッパ'},
 'BZ': {'companyen': 'Belize', 'companyjp': 'ベリーズ', 'location': '中央アメリカ'},
 'CA': {'companyen': 'Canada', 'companyjp': 'カナダ', 'location': '北アメリカ'},
 'CC': {'companyen': 'Cocos+Islands',
  'companyjp': 'ココス諸島',
  'location': 'インド洋地域'},
 'CD': {'companyen': 'Congo-Kinshasa',
  'companyjp': 'コンゴ民主共和国',
  'location': '中央アフリカ'},
 'CF': {'companyen': 'Central+African+Republic',
  'companyjp': '中央アフリカ共和国',
  'location': '中央アフリカ'},
 'CG': {'companyen': 'Congo-Brazzaville',
  'companyjp': 'コンゴ共和国',
  'location': '中央アフリカ'},
 'CH': {'companyen': 'Switzerland', 'companyjp': 'スイス', 'location': '西ヨーロッパ'},
 'CI': {'companyen': 'Ivory+Coast',
  'companyjp': 'コートジボワール',
  'location': '西アフリカ'},
 'CK': {'companyen': 'Cook+Islands',
  'companyjp': 'クック諸島',
  'location': 'オセアニア'},
 'CL': {'companyen': 'Chile', 'companyjp': 'チリ', 'location': '南アメリカ'},
 'CM': {'companyen': 'Cameroon', 'companyjp': 'カメルーン', 'location': '中央アフリカ'},
 'CN': {'companyen': 'China', 'companyjp': '中国', 'location': '東アジア'},
 'CO': {'companyen': 'Colombia', 'companyjp': 'コロンビア', 'location': '南アメリカ'},
 'CR': {'companyen': 'Costa+Rica', 'companyjp': 'コスタリカ', 'location': '中央アメリカ'},
 'CU': {'companyen': 'Cuba', 'companyjp': 'キューバ', 'location': '中央アメリカ'},
 'CV': {'companyen': 'Cape+Verde', 'companyjp': 'カーボベルデ', 'location': '西アフリカ'},
 'CW': {'companyen': 'Curaçao', 'companyjp': 'キュラソー', 'location': '中央アメリカ'},
 'CX': {'companyen': 'Christmas+Island',
  'companyjp': 'クリスマス島',
  'location': 'オセアニア'},
 'CY': {'companyen': 'Cyprus', 'companyjp': 'キプロス', 'location': '地中海地域'},
 'CZ': {'companyen': 'Czech', 'companyjp': 'チェコ', 'location': '東ヨーロッパ'},
 'DE': {'companyen': 'Germany', 'companyjp': 'ドイツ', 'location': '西ヨーロッパ'},
 'DJ': {'companyen': 'Djibouti', 'companyjp': 'ジブチ', 'location': '東アフリカ'},
 'DK': {'companyen': 'Denmark', 'companyjp': 'デンマーク', 'location': '北ヨーロッパ'},
 'DM': {'companyen': 'Dominica', 'companyjp': 'ドミニカ国', 'location': '中央アメリカ'},
 'DO': {'companyen': 'Dominican+Republic',
  'companyjp': 'ドミニカ共和国',
  'location': '中央アメリカ'},
 'DZ': {'companyen': 'Algeria', 'companyjp': 'アルジェリア', 'location': '北アフリカ'},
 'EC': {'companyen': 'Ecuador', 'companyjp': 'エクアドル', 'location': '南アメリカ'},
 'EE': {'companyen': 'Estonia', 'companyjp': 'エストニア', 'location': '東ヨーロッパ'},
 'EG': {'companyen': 'Egypt', 'companyjp': 'エジプト', 'location': '北アフリカ'},
 'EH': {'companyen': 'Western Sahara',
  'companyjp': '西サハラ',
  'location': '西アフリカ'},
 'ER': {'companyen': 'Eritrea', 'companyjp': 'エリトリア', 'location': '東アフリカ'},
 'ES': {'companyen': 'Spain', 'companyjp': 'スペイン', 'location': '西ヨーロッパ'},
 'ET': {'companyen': 'Ethiopia', 'companyjp': 'エチオピア', 'location': '東アフリカ'},
 'FI': {'companyen': 'Finland', 'companyjp': 'フィンランド', 'location': '北ヨーロッパ'},
 'FJ': {'companyen': 'Fiji', 'companyjp': 'フィジー', 'location': 'オセアニア'},
 'FK': {'companyen': 'Falkland+Islands',
  'companyjp': 'フォークランド諸島',
  'location': '南アメリカ'},
 'FM': {'companyen': 'Micronesia',
  'companyjp': 'ミクロネシア連邦',
  'location': 'オセアニア'},
 'FO': {'companyen': 'Faroe+Islands',
  'companyjp': 'フェロー諸島',
  'location': '北ヨーロッパ'},
 'FR': {'companyen': 'France', 'companyjp': 'フランス', 'location': '西ヨーロッパ'},
 'GA': {'companyen': 'Gabon', 'companyjp': 'ガボン', 'location': '中央アフリカ'},
 'GB': {'companyen': 'United+Kingdom',
  'companyjp': 'イギリス',
  'location': '西ヨーロッパ'},
 'GE': {'companyen': 'Georgia', 'companyjp': 'グルジア', 'location': '東ヨーロッパ'},
 'GF': {'companyen': 'French+Guiana',
  'companyjp': 'フランス領ギアナ',
  'location': '南アメリカ'},
 'GG': {'companyen': 'Guernsey', 'companyjp': 'ガーンジー', 'location': '西ヨーロッパ'},
 'GH': {'companyen': 'Ghana', 'companyjp': 'ガーナ', 'location': '西アフリカ'},
 'GI': {'companyen': 'Gibraltar', 'companyjp': 'ジブラルタル', 'location': '西ヨーロッパ'},
 'GL': {'companyen': 'Greenland',
  'companyjp': 'グリーンランド',
  'location': '北ヨーロッパ'},
 'GMB': {'companyen': 'Gambia', 'companyjp': 'ガンビア', 'location': '西アフリカ'},
 'GN': {'companyen': 'Guinea', 'companyjp': 'ギニア', 'location': '西アフリカ'},
 'GO': {'companyen': 'Grenada', 'companyjp': 'グレナダ', 'location': '中央アメリカ'},
 'GP': {'companyen': 'Guadeloupe',
  'companyjp': 'グアドループ',
  'location': '中央アメリカ'},
 'GQ': {'companyen': 'Equatorial+Guinea',
  'companyjp': '赤道ギニア',
  'location': '中央アフリカ'},
 'GR': {'companyen': 'Greece', 'companyjp': 'ギリシャ', 'location': '西ヨーロッパ'},
 'GS': {'companyen': 'South+Georgia+and+the+South+Sandwich+Islands',
  'companyjp': 'サウスジョージア・サウスサンドウィッチ諸島',
  'location': '南アメリカ'},
 'GT': {'companyen': 'Guatemala', 'companyjp': 'グアテマラ', 'location': '中央アメリカ'},
 'GU': {'companyen': 'Guam', 'companyjp': 'グアム', 'location': 'オセアニア'},
 'GW': {'companyen': 'Guinea-Bissau',
  'companyjp': 'ギニアビサウ',
  'location': '西アフリカ'},
 'GY': {'companyen': 'Guyana', 'companyjp': 'ガイアナ', 'location': '南アメリカ'},
 'HKG': {'companyen': 'Hong+Kong', 'companyjp': '香港', 'location': '東アジア'},
 'HM': {'companyen': 'Heard+Island+and+McDonald+Islands',
  'companyjp': 'ハード島とマクドナルド諸島',
  'location': 'インド洋地域'},
 'HN': {'companyen': 'Honduras', 'companyjp': 'ホンジュラス', 'location': '中央アメリカ'},
 'HR': {'companyen': 'Croatia', 'companyjp': 'クロアチア', 'location': '東ヨーロッパ'},
 'HT': {'companyen': 'Haiti', 'companyjp': 'ハイチ', 'location': '中央アメリカ'},
 'HU': {'companyen': 'Hungary', 'companyjp': 'ハンガリー', 'location': '東ヨーロッパ'},
 'ID': {'companyen': 'Indonesia', 'companyjp': 'インドネシア', 'location': '東南アジア'},
 'IE': {'companyen': 'Ireland', 'companyjp': 'アイルランド', 'location': '西ヨーロッパ'},
 'IL': {'companyen': 'Israel', 'companyjp': 'イスラエル', 'location': '中東'},
 'IM': {'companyen': 'Isle+of+Man', 'companyjp': 'マン島', 'location': '西ヨーロッパ'},
 'IN': {'companyen': 'India', 'companyjp': 'インド', 'location': '南アジア'},
 'IO': {'companyen': 'British+Indian+Ocean+Territory',
  'companyjp': 'イギリス領インド洋地域',
  'location': 'インド洋地域'},
 'IQ': {'companyen': 'Iraq', 'companyjp': 'イラク', 'location': '中東'},
 'IR': {'companyen': 'Iran', 'companyjp': 'イラン', 'location': '中東'},
 'IS': {'companyen': 'Iceland', 'companyjp': 'アイスランド', 'location': '北ヨーロッパ'},
 'IT': {'companyen': 'Italy', 'companyjp': 'イタリア', 'location': '西ヨーロッパ'},
 'JE': {'companyen': 'Jersey', 'companyjp': 'ジャージー', 'location': '西ヨーロッパ'},
 'JM': {'companyen': 'Jamaica', 'companyjp': 'ジャマイカ', 'location': '中央アメリカ'},
 'JO': {'companyen': 'Jordan', 'companyjp': 'ヨルダン', 'location': '中東'},
 'JP': {'companyen': 'Japan', 'companyjp': '日本', 'location': '東アジア'},
 'KE': {'companyen': 'Kenya', 'companyjp': 'ケニア', 'location': '東アフリカ'},
 'KG': {'companyen': 'Kyrgyzstan', 'companyjp': 'キルギス', 'location': '中央アジア'},
 'KH': {'companyen': 'Cambodia', 'companyjp': 'カンボジア', 'location': '東南アジア'},
 'KI': {'companyen': 'Kiribati', 'companyjp': 'キリバス', 'location': 'オセアニア'},
 'KM': {'companyen': 'Comoros', 'companyjp': 'コモロ', 'location': 'インド洋地域'},
 'KN': {'companyen': 'Saint+Kitts+and+Nevis',
  'companyjp': 'セントクリストファー・ネイビス',
  'location': '中央アメリカ'},
 'KP': {'companyen': 'North+Korea',
  'companyjp': '朝鮮民主主義人民共和国',
  'location': '東アジア'},
 'KR': {'companyen': 'Korea', 'companyjp': '大韓民国', 'location': '東アジア'},
 'KW': {'companyen': 'Kuwait', 'companyjp': 'クウェート', 'location': '中東'},
 'KY': {'companyen': 'Cayman+Islands',
  'companyjp': 'ケイマン諸島',
  'location': '中央アメリカ'},
 'KZ': {'companyen': 'Kazakhstan', 'companyjp': 'カザフスタン', 'location': '中央アジア'},
 'LA': {'companyen': 'Laos', 'companyjp': 'ラオス', 'location': '東南アジア'},
 'LB': {'companyen': 'Lebanon', 'companyjp': 'レバノン', 'location': '中東'},
 'LC': {'companyen': 'Saint+Lucia',
  'companyjp': 'セントルシア',
  'location': '中央アメリカ'},
 'LI': {'companyen': 'Liechtenstein',
  'companyjp': 'リヒテンシュタイン',
  'location': '西ヨーロッパ'},
 'LK': {'companyen': 'Sri+Lanka', 'companyjp': 'スリランカ', 'location': '南アジア'},
 'LR': {'companyen': 'Liberia', 'companyjp': 'リベリア', 'location': '西アフリカ'},
 'LS': {'companyen': 'Lesotho', 'companyjp': 'レソト', 'location': '南アフリカ'},
 'LT': {'companyen': 'Lithuania', 'companyjp': 'リトアニア', 'location': '東ヨーロッパ'},
 'LU': {'companyen': 'Luxembourg',
  'companyjp': 'ルクセンブルク',
  'location': '西ヨーロッパ'},
 'LV': {'companyen': 'Latvia', 'companyjp': 'ラトビア', 'location': '東ヨーロッパ'},
 'LY': {'companyen': 'Libya', 'companyjp': 'リビア', 'location': '北アフリカ'},
 'MA': {'companyen': 'Morocco', 'companyjp': 'モロッコ', 'location': '北アフリカ'},
 'MC': {'companyen': 'Monaco', 'companyjp': 'モナコ', 'location': '西ヨーロッパ'},
 'MD': {'companyen': 'Moldova', 'companyjp': 'モルドバ', 'location': '東ヨーロッパ'},
 'ME': {'companyen': 'Montenegro',
  'companyjp': 'モンテネグロ',
  'location': '東ヨーロッパ'},
 'MF': {'companyen': 'Saint+Martin',
  'companyjp': 'サン・マルタン',
  'location': '中央アメリカ'},
 'MG': {'companyen': 'Madagascar',
  'companyjp': 'マダガスカル',
  'location': 'インド洋地域'},
 'MH': {'companyen': 'Marshall+Islands',
  'companyjp': 'マーシャル諸島',
  'location': 'オセアニア'},
 'MK': {'companyen': 'Macedonia',
  'companyjp': 'マケドニア共和国',
  'location': '東ヨーロッパ'},
 'ML': {'companyen': 'Mali', 'companyjp': 'マリ', 'location': '西アフリカ'},
 'MM': {'companyen': 'Myanmar', 'companyjp': 'ミャンマー', 'location': '東南アジア'},
 'MN': {'companyen': 'Mongolia', 'companyjp': 'モンゴル', 'location': '東アジア'},
 'MP': {'companyen': 'Northern+Mariana+Islands',
  'companyjp': '北マリアナ諸島',
  'location': 'オセアニア'},
 'MQ': {'companyen': 'Martinique',
  'companyjp': 'マルティニーク',
  'location': '中央アメリカ'},
 'MR': {'companyen': 'Mauritania', 'companyjp': 'モーリタニア', 'location': '西アフリカ'},
 'MS': {'companyen': 'Montserrat',
  'companyjp': 'モントセラト',
  'location': '中央アメリカ'},
 'MT': {'companyen': 'Malta', 'companyjp': 'マルタ', 'location': '地中海地域'},
 'MU': {'companyen': 'Mauritius', 'companyjp': 'モーリシャス', 'location': '南アフリカ'},
 'MV': {'companyen': 'Maldives', 'companyjp': 'モルディブ', 'location': 'インド洋地域'},
 'MW': {'companyen': 'Malawi', 'companyjp': 'マラウイ', 'location': '南アフリカ'},
 'MX': {'companyen': 'Mexico', 'companyjp': 'メキシコ', 'location': '中央アメリカ'},
 'MY': {'companyen': 'Malaysia', 'companyjp': 'マレーシア', 'location': '東南アジア'},
 'MZ': {'companyen': 'Mozambique', 'companyjp': 'モザンビーク', 'location': '南アフリカ'},
 'NA': {'companyen': 'Namibia', 'companyjp': 'ナミビア', 'location': '南アフリカ'},
 'NC': {'companyen': 'New Caledonia',
  'companyjp': 'ニューカレドニア',
  'location': 'オセアニア'},
 'NE': {'companyen': 'Niger', 'companyjp': 'ニジェール', 'location': '中央アフリカ'},
 'NF': {'companyen': 'Norfolk+Island',
  'companyjp': 'ノーフォーク島',
  'location': 'オセアニア'},
 'NG': {'companyen': 'Nigeria', 'companyjp': 'ナイジェリア', 'location': '中央アフリカ'},
 'NI': {'companyen': 'Nicaragua', 'companyjp': 'ニカラグア', 'location': '中央アメリカ'},
 'NL': {'companyen': 'Netherlands', 'companyjp': 'オランダ', 'location': '西ヨーロッパ'},
 'NO': {'companyen': 'Norway', 'companyjp': 'ノルウェー', 'location': '北ヨーロッパ'},
 'NP': {'companyen': 'Nepal', 'companyjp': 'ネパール', 'location': '南アジア'},
 'NR': {'companyen': 'Nauru', 'companyjp': 'ナウル', 'location': 'オセアニア'},
 'NU': {'companyen': 'Niue', 'companyjp': 'ニウエ', 'location': 'オセアニア'},
 'NZ': {'companyen': 'New+Zealand',
  'companyjp': 'ニュージーランド',
  'location': 'オセアニア'},
 'OM': {'companyen': 'Oman', 'companyjp': 'オマーン', 'location': '中東'},
 'PA': {'companyen': 'Panama', 'companyjp': 'パナマ', 'location': '中央アメリカ'},
 'PE': {'companyen': 'Peru', 'companyjp': 'ペルー', 'location': '南アメリカ'},
 'PF': {'companyen': 'French+Polynesia',
  'companyjp': 'フランス領ポリネシア',
  'location': 'オセアニア'},
 'PG': {'companyen': 'Papua+New+Guinea',
  'companyjp': 'パプアニューギニア',
  'location': 'オセアニア'},
 'PH': {'companyen': 'Philippines', 'companyjp': 'フィリピン', 'location': '東南アジア'},
 'PK': {'companyen': 'Pakistan', 'companyjp': 'パキスタン', 'location': '南アジア'},
 'PL': {'companyen': 'Poland', 'companyjp': 'ポーランド', 'location': '東ヨーロッパ'},
 'PM': {'companyen': 'Saint+Pierre+and+Miquelon',
  'companyjp': 'サンピエール島・ミクロン島',
  'location': '北アメリカ'},
 'PN': {'companyen': 'Pitcairn', 'companyjp': 'ピトケアン', 'location': 'オセアニア'},
 'PR': {'companyen': 'Puerto+Rico',
  'companyjp': 'プエルトリコ',
  'location': '中央アメリカ'},
 'PS': {'companyen': 'Palestine', 'companyjp': 'パレスチナ', 'location': '中東'},
 'PT': {'companyen': 'Portugal', 'companyjp': 'ポルトガル', 'location': '西ヨーロッパ'},
 'PW': {'companyen': 'Palau', 'companyjp': 'パラオ', 'location': 'オセアニア'},
 'PY': {'companyen': 'Paraguay', 'companyjp': 'パラグアイ', 'location': '南アメリカ'},
 'QA': {'companyen': 'Qatar', 'companyjp': 'カタール', 'location': '中東'},
 'RE': {'companyen': 'Réunion', 'companyjp': 'レユニオン', 'location': 'インド洋地域'},
 'RO': {'companyen': 'Romania', 'companyjp': 'ルーマニア', 'location': '東ヨーロッパ'},
 'RS': {'companyen': 'Serbia', 'companyjp': 'セルビア', 'location': '東ヨーロッパ'},
 'RU': {'companyen': 'Russian+Federation',
  'companyjp': 'ロシア',
  'location': 'ロシア'},
 'RW': {'companyen': 'Rwanda', 'companyjp': 'ルワンダ', 'location': '中央アフリカ'},
 'SA': {'companyen': 'Saudi+Arabia', 'companyjp': 'サウジアラビア', 'location': '中東'},
 'SB': {'companyen': 'Solomon+Islands',
  'companyjp': 'ソロモン諸島',
  'location': 'オセアニア'},
 'SC': {'companyen': 'Seychelles', 'companyjp': 'セーシェル', 'location': 'インド洋地域'},
 'SD': {'companyen': 'Sudan', 'companyjp': 'スーダン', 'location': '東アフリカ'},
 'SE': {'companyen': 'Sweden', 'companyjp': 'スウェーデン', 'location': '北ヨーロッパ'},
 'SG': {'companyen': 'Singapore', 'companyjp': 'シンガポール', 'location': '東南アジア'},
 'SH': {'companyen': 'Saint+Helena+Ascension+and+Tristan+da+Cunha',
  'companyjp': 'セントヘレナ・アセンションおよびトリスタンダクーニャ',
  'location': '西アフリカ'},
 'SI': {'companyen': 'Slovenia', 'companyjp': 'スロベニア', 'location': '東ヨーロッパ'},
 'SJ': {'companyen': 'Svalbard+and+Jan+Mayen',
  'companyjp': 'スヴァールバル諸島およびヤンマイエン島',
  'location': '北ヨーロッパ'},
 'SK': {'companyen': 'Slovakia', 'companyjp': 'スロバキア', 'location': '東ヨーロッパ'},
 'SL': {'companyen': 'Sierra+Leone',
  'companyjp': 'シエラレオネ',
  'location': '西アフリカ'},
 'SM': {'companyen': 'San+Marino', 'companyjp': 'サンマリノ', 'location': '西ヨーロッパ'},
 'SN': {'companyen': 'Senegal', 'companyjp': 'セネガル', 'location': '西アフリカ'},
 'SO': {'companyen': 'Somalia', 'companyjp': 'ソマリア', 'location': '東アフリカ'},
 'SR': {'companyen': 'Suriname', 'companyjp': 'スリナム', 'location': '南アメリカ'},
 'SS': {'companyen': 'South+Sudan', 'companyjp': '南スーダン', 'location': '東アフリカ'},
 'ST': {'companyen': 'Sao+Tome+and+Principe',
  'companyjp': 'サントメ・プリンシペ',
  'location': '中央アフリカ'},
 'SV': {'companyen': 'El+Salvador',
  'companyjp': 'エルサルバドル',
  'location': '中央アメリカ'},
 'SX': {'companyen': 'Sint+Maarten',
  'companyjp': 'シント・マールテン',
  'location': '中央アメリカ'},
 'SY': {'companyen': 'Syrian+Arab+Republic',
  'companyjp': 'シリア',
  'location': '中東'},
 'SZ': {'companyen': 'Swaziland', 'companyjp': 'スワジランド', 'location': '南アフリカ'},
 'TC': {'companyen': 'Turks+and+Caicos+Islands',
  'companyjp': 'タークス・カイコス諸島',
  'location': '中央アメリカ'},
 'TD': {'companyen': 'Chad', 'companyjp': 'チャド', 'location': '中央アフリカ'},
 'TF': {'companyen': 'French+Southern+Territories',
  'companyjp': 'フランス領南方・南極地域',
  'location': 'インド洋地域'},
 'TG': {'companyen': 'Togo', 'companyjp': 'トーゴ', 'location': '西アフリカ'},
 'TH': {'companyen': 'Thailand', 'companyjp': 'タイ', 'location': '東南アジア'},
 'TJ': {'companyen': 'Tajikistan', 'companyjp': 'タジキスタン', 'location': '中央アジア'},
 'TK': {'companyen': 'Tokelau', 'companyjp': 'トケラウ', 'location': 'オセアニア'},
 'TL': {'companyen': 'Timor-Leste',
  'companyjp': '東ティモール',
  'location': '東南アジア'},
 'TM': {'companyen': 'Turkmenistan',
  'companyjp': 'トルクメニスタン',
  'location': '中央アジア'},
 'TN': {'companyen': 'Tunisia', 'companyjp': 'チュニジア', 'location': '北アフリカ'},
 'TO': {'companyen': 'Tonga', 'companyjp': 'トンガ', 'location': 'オセアニア'},
 'TR': {'companyen': 'Turkey', 'companyjp': 'トルコ', 'location': '中東'},
 'TT': {'companyen': 'Trinidad+and+Tobago',
  'companyjp': 'トリニダード・トバゴ',
  'location': '中央アメリカ'},
 'TV': {'companyen': 'Tuvalu', 'companyjp': 'ツバル', 'location': 'オセアニア'},
 'TW': {'companyen': 'Taiwan', 'companyjp': '台湾', 'location': '東アジア'},
 'TZ': {'companyen': 'Tanzania', 'companyjp': 'タンザニア', 'location': '東アフリカ'},
 'UA': {'companyen': 'Ukraine', 'companyjp': 'ウクライナ', 'location': '東ヨーロッパ'},
 'UG': {'companyen': 'Uganda', 'companyjp': 'ウガンダ', 'location': '中央アフリカ'},
 'UM': {'companyen': 'United+States+Minor+Outlying+Islands',
  'companyjp': '合衆国領有小離島',
  'location': 'オセアニア'},
 'US': {'companyen': 'USA', 'companyjp': 'アメリカ合衆国', 'location': '北アメリカ'},
 'UY': {'companyen': 'Uruguay', 'companyjp': 'ウルグアイ', 'location': '南アメリカ'},
 'UZ': {'companyen': 'Uzbekistan',
  'companyjp': 'ウズベキスタン',
  'location': '中央アジア'},
 'VA': {'companyen': 'Vatican+City',
  'companyjp': 'バチカン',
  'location': '西ヨーロッパ'},
 'VC': {'companyen': 'Saint+Vincent+and+the+Grenadines',
  'companyjp': 'セントビンセント・グレナディーン',
  'location': '中央アメリカ'},
 'VE': {'companyen': 'Venezuela', 'companyjp': 'ベネズエラ', 'location': '南アメリカ'},
 'VG': {'companyen': 'Virgin+Islands+British',
  'companyjp': 'イギリス領ヴァージン諸島',
  'location': '中央アメリカ'},
 'VN': {'companyen': 'Viet+Nam', 'companyjp': 'ベトナム', 'location': '東南アジア'},
 'VU': {'companyen': 'Vanuatu', 'companyjp': 'バヌアツ', 'location': 'オセアニア'},
 'WF': {'companyen': 'Wallis+and+Futuna',
  'companyjp': 'ウォリス・フツナ',
  'location': 'オセアニア'},
 'WS': {'companyen': 'Samoa', 'companyjp': 'サモア', 'location': 'オセアニア'},
 'YE': {'alpha2': 'YE',
  'companyen': 'Yemen',
  'companyjp': 'イエメン',
  'location': '中東'},
 'YT': {'companyen': 'Mayotte', 'companyjp': 'マヨット', 'location': 'インド洋地域'},
 'ZA': {'companyen': 'South+Africa',
  'companyjp': '南アフリカ',
  'location': '南アフリカ'},
 'ZM': {'companyen': 'Zambia', 'companyjp': 'ザンビア', 'location': '南アフリカ'},
 'ZW': {'companyen': 'Zimbabwe', 'companyjp': 'ジンバブエ', 'location': '南アフリカ'}}


def code_country_en(arg):
    country_en = country_dict[arg]['companyen']
    r = requests.get(f"https://world.einnews.com/search/{country_en}")
    soup = BeautifulSoup(r.content, "html.parser")
 
    news_titles = [tag.text for tag in soup('a',attrs={"title"})]
    world_news_ad = 'http://world.einnews.com/'
    news_links = [tag.get('href') for tag in soup('a',attrs={"title"})]
    for i in range(len(news_links)):
        if world_news_ad not in news_links[i]:
            news_links[i] = world_news_ad+news_links[i]
    return news_titles, news_links
 

def code_country_jp(arg):
    country_jp = country_dict[arg]['companyjp']
    r= requests.get(f"https://news.google.com/search?q={country_jp}&hl=ja&gl=JP&ceid=JP%3Aja")
    soup = BeautifulSoup(r.content, "html.parser")
    
    news_titles = [tag.text for tag in soup('a',attrs={"DY5T1d"},limit=10)]
    news_links = [tag.get('href') for tag in soup('a',attrs={"VDXfz"},limit=10)]
    news_links = ["https://news.google.com/"+news_link[2:] for news_link in news_links]
    return news_titles, news_links


def utc_to(current_time):
    timestamp_utc = str(datetime.datetime.now(timezone('UTC')))
    datetime_utc = datetime.datetime.strptime(timestamp_utc , "%Y-%m-%d %H:%M:%S.%f%z")
    datetime_jst = datetime_utc.astimezone(datetime.timezone(datetime.timedelta(seconds=current_time)))
    timestamp_jst = datetime.datetime.strftime(datetime_jst, '%Y-%m-%d %H:%M:%S.%f')
    return timestamp_jst[11:16]


# %%
