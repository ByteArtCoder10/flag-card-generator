import docx, requests, os
import cairosvg
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from PIL import Image
import io
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import ImageReader


# Register the font with a name
pdfmetrics.registerFont(TTFont("Poppins-Bold", r"..\FlagGame\fonts\Poppins-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Poppins-Regular", r"..\FlagGame\fonts\Poppins-Regular.ttf"))

country_ISO = {
    "Afghanistan": "AF",
    "Albania": "AL",
    "Algeria": "DZ",
    "Andorra": "AD",
    "Angola": "AO",
    "Antigua and Barbuda": "AG",
    "Argentina": "AR",
    "Armenia": "AM",
    "Australia": "AU",
    "Austria": "AT",
    "Azerbaijan": "AZ",
    "Bahamas": "BS",
    "Bahrain": "BH",
    "Bangladesh": "BD",
    "Barbados": "BB",
    "Belarus": "BY",
    "Belgium": "BE",
    "Belize": "BZ",
    "Benin": "BJ",
    "Bhutan": "BT",
    "Bolivia": "BO",
    "Bosnia and Herzegovina": "BA",
    "Botswana": "BW",
    "Brazil": "BR",
    "Brunei": "BN",
    "Bulgaria": "BG",
    "Burkina Faso": "BF",
    "Burma (Myanmar)": "MM",
    "Burundi": "BI",
    "Cambodia": "KH",
    "Cameroon": "CM",
    "Canada": "CA",
    "Cape Verde": "CV",
    "Central African Republic": "CF",
    "Chad": "TD",
    "Chile": "CL",
    "China": "CN",
    "Colombia": "CO",
    "Comoros": "KM",
    "Costa Rica": "CR",
    "Croatia": "HR",
    "Cuba": "CU",
    "Cyprus": "CY",
    "Czech Republic": "CZ",
    "Democratic Republic of the Congo": "CD",
    "Denmark": "DK",
    "Djibouti": "DJ",
    "Dominica": "DM",
    "Dominican Republic": "DO",
    "East Timor": "TL",
    "Ecuador": "EC",
    "Egypt": "EG",
    "El Salvador": "SV",
    "Equatorial Guinea": "GQ",
    "Eritrea": "ER",
    "Estonia": "EE",
    "Ethiopia": "ET",
    "Fiji": "FJ",
    "Finland": "FI",
    "France": "FR",
    "Gabon": "GA",
    "Gambia": "GM",
    "Georgia": "GE",
    "Germany": "DE",
    "Ghana": "GH",
    "Greece": "GR",
    "Grenada": "GD",
    "Guatemala": "GT",
    "Guinea": "GN",
    "Guinea-Bissau": "GW",
    "Guyana": "GY",
    "Haiti": "HT",
    "Honduras": "HN",
    "Hungary": "HU",
    "Iceland": "IS",
    "India": "IN",
    "Indonesia": "ID",
    "Iran": "IR",
    "Iraq": "IQ",
    "Ireland": "IE",
    "Israel": "IL",
    "Italy": "IT",
    "Ivory Coast (Côte d'Ivoire)": "CI",
    "Jamaica": "JM",
    "Japan": "JP",
    "Jordan": "JO",
    "Kazakhstan": "KZ",
    "Kenya": "KE",
    "Kiribati": "KI",
    "Kuwait": "KW",
    "Kyrgyzstan": "KG",
    "Laos": "LA",
    "Latvia": "LV",
    "Lebanon": "LB",
    "Lesotho": "LS",
    "Liberia": "LR",
    "Libya": "LY",
    "Liechtenstein": "LI",
    "Lithuania": "LT",
    "Luxembourg": "LU",
    "Madagascar": "MG",
    "Malawi": "MW",
    "Malaysia": "MY",
    "Maldives": "MV",
    "Mali": "ML",
    "Malta": "MT",
    "Marshall Islands": "MH",
    "Mauritania": "MR",
    "Mauritius": "MU",
    "Mexico": "MX",
    "Micronesia": "FM",
    "Moldova": "MD",
    "Monaco": "MC",
    "Mongolia": "MN",
    "Montenegro": "ME",
    "Morocco": "MA",
    "Mozambique": "MZ",
    "Namibia": "NA",
    "Nauru": "NR",
    "Nepal": "NP",
    "Netherlands": "NL",
    "New Zealand": "NZ",
    "Nicaragua": "NI",
    "Niger": "NE",
    "Nigeria": "NG",
    "North Korea": "KP",
    "North Macedonia": "MK",
    "Norway": "NO",
    "Oman": "OM",
    "Pakistan": "PK",
    "Palau": "PW",
    "Panama": "PA",
    "Papua New Guinea": "PG",
    "Paraguay": "PY",
    "Peru": "PE",
    "Philippines": "PH",
    "Poland": "PL",
    "Portugal": "PT",
    "Qatar": "QA",
    "Republic of the Congo": "CG",
    "Romania": "RO",
    "Russia": "RU",
    "Rwanda": "RW",
    "Saint Kitts and Nevis": "KN",
    "Saint Lucia": "LC",
    "Saint Vincent and the Grenadines": "VC",
    "Samoa": "WS",
    "San Marino": "SM",
    "São Tomé and Príncipe": "ST",
    "Saudi Arabia": "SA",
    "Senegal": "SN",
    "Serbia": "RS",
    "Seychelles": "SC",
    "Sierra Leone": "SL",
    "Singapore": "SG",
    "Slovakia": "SK",
    "Slovenia": "SI",
    "Solomon Islands": "SB",
    "Somalia": "SO",
    "South Africa": "ZA",
    "South Korea": "KR",
    "South Sudan": "SS",
    "Spain": "ES",
    "Sri Lanka": "LK",
    "Sudan": "SD",
    "Suriname": "SR",
    "Sweden": "SE",
    "Switzerland": "CH",
    "Syria": "SY",
    "Tajikistan": "TJ",
    "Tanzania": "TZ",
    "Thailand": "TH",
    "Togo": "TG",
    "Tonga": "TO",
    "Trinidad and Tobago": "TT",
    "Tunisia": "TN",
    "Turkey": "TR",
    "Turkmenistan": "TM",
    "Tuvalu": "TV",
    "Uganda": "UG",
    "Ukraine": "UA",
    "United Arab Emirates": "AE",
    "United Kingdom": "GB",
    "United States": "US",
    "Uruguay": "UY",
    "Uzbekistan": "UZ",
    "Vanuatu": "VU",
    "Vatican City": "VA",
    "Venezuela": "VE",
    "Vietnam": "VN",
    "Yemen": "YE",
    "Zambia": "ZM",
    "Zimbabwe": "ZW" 
}
countries_data ={
  "Afghanistan": {
    "Capital": "Kabul",
    "Continent": "Asia",
    "Languages": "Dari, Pashto"
  },
  "Albania": {
    "Capital": "Tirana",
    "Continent": "Europe",
    "Languages": "Albanian"
  },
  "Algeria": {
    "Capital": "Algiers",
    "Continent": "Africa",
    "Languages": "Arabic"
  },
  "Andorra": {
    "Capital": "Andorra la Vella",
    "Continent": "Europe",
    "Languages": "Catalan"
  },
  "Angola": {
    "Capital": "Luanda",
    "Continent": "Africa",
    "Languages": "Portuguese"
  },
  "Antigua and Barbuda": {
    "Capital": "Saint John's",
    "Continent": "North America",
    "Languages": "English"
  },
  "Argentina": {
    "Capital": "Buenos Aires",
    "Continent": "South America",
    "Languages": "Spanish"
  },
  "Armenia": {
    "Capital": "Yerevan",
    "Continent": "Asia",
    "Languages": "Armenian"
  },
  "Australia": {
    "Capital": "Canberra",
    "Continent": "Oceania",
    "Languages": "English"
  },
  "Austria": {
    "Capital": "Vienna",
    "Continent": "Europe",
    "Languages": "German"
  },
  "Azerbaijan": {
    "Capital": "Baku",
    "Continent": "Asia",
    "Languages": "Azerbaijani"
  },
  "Bahamas": {
    "Capital": "Nassau",
    "Continent": "North America",
    "Languages": "English"
  },
  "Bahrain": {
    "Capital": "Manama",
    "Continent": "Asia",
    "Languages": "Arabic"
  },
  "Bangladesh": {
    "Capital": "Dhaka",
    "Continent": "Asia",
    "Languages": "Bengali"
  },
  "Barbados": {
    "Capital": "Bridgetown",
    "Continent": "North America",
    "Languages": "English"
  },
  "Belarus": {
    "Capital": "Minsk",
    "Continent": "Europe",
    "Languages": "Belarusian, Russian"
  },
  "Belgium": {
    "Capital": "Brussels",
    "Continent": "Europe",
    "Languages": "Dutch, French, German"
  },
  "Belize": {
    "Capital": "Belmopan",
    "Continent": "North\nAmerica",
    "Languages": "English"
  },
  "Benin": {
    "Capital": "Porto Novo and Cotonou",
    "Continent": "Africa",
    "Languages": "French"
  },
  "Bhutan": {
    "Capital": "Thimphu",
    "Continent": "Asia",
    "Languages": "Dzongkha"
  },
  "Bolivia": {
    "Capital": "Sucre",
    "Continent": "South America",
    "Languages": "Spanish, Quechua, Aymara"
  },
  "Bosnia and Herzegovina": {
    "Capital": "Sarajevo",
    "Continent": "Europe",
    "Languages": "Bosnian, Croatian, Serbian"
  },
  "Botswana": {
    "Capital": "Gaborone",
    "Continent": "Africa",
    "Languages": "English, Setswana"
  },
  "Brazil": {
    "Capital": "Bras\u00edlia",
    "Continent": "South America",
    "Languages": "Portuguese"
  },
  "Brunei": {
    "Capital": "Bandar Seri Begawan",
    "Continent": "Asia",
    "Languages": "Malay"
  },
  "Bulgaria": {
    "Capital": "Sofia",
    "Continent": "Europe",
    "Languages": "Bulgarian"
  },
  "Burkina Faso": {
    "Capital": "Ouagadougou",
    "Continent": "Africa",
    "Languages": "French"
  },
  "Burma (Myanmar)": {
    "Capital": "Naypyidaw",
    "Continent": "Asia",
    "Languages": "Burmese"
  },
  "Burundi": {
    "Capital": "Bujumbura",
    "Continent": "Africa",
    "Languages": "Kirundi, French"
  },
  "Cambodia": {
    "Capital": "Phnom Penh",
    "Continent": "Asia",
    "Languages": "Khmer"
  },
  "Cameroon": {
    "Capital": "Yaound\u00e9",
    "Continent": "Africa",
    "Languages": "English, French"
  },
  "Canada": {
    "Capital": "Ottawa",
    "Continent": "North America",
    "Languages": "English, French"
  },
  "Cape Verde": {
    "Capital": "Praia",
    "Continent": "Africa",
    "Languages": "Portuguese"
  },
  "Central African Republic": {
    "Capital": "Bangui",
    "Continent": "Africa",
    "Languages": "French, Sango"
  },
  "Chad": {
    "Capital": "N'Djamena",
    "Continent": "Africa",
    "Languages": "Arabic, French"
  },
  "Chile": {
    "Capital": "Santiago",
    "Continent": "South America",
    "Languages": "Spanish"
  },
  "China": {
    "Capital": "Beijing",
    "Continent": "Asia",
    "Languages": "Mandarin Chinese"
  },
  "Colombia": {
    "Capital": "Bogot\u00e1",
    "Continent": "South America",
    "Languages": "Spanish"
  },
  "Comoros": {
    "Capital": "Moroni",
    "Continent": "Africa",
    "Languages": "Arabic, Comorian, French"
  },
  "Costa Rica": {
    "Capital": "San Jos\u00e9",
    "Continent": "North America",
    "Languages": "Spanish"
  },
  "Croatia": {
    "Capital": "Zagreb",
    "Continent": "Europe",
    "Languages": "Croatian"
  },
  "Cuba": {
    "Capital": "Havana",
    "Continent": "North America",
    "Languages": "Spanish"
  },
  "Cyprus": {
    "Capital": "Nicosia",
    "Continent": "Europe",
    "Languages": "Greek, Turkish"
  },
  "Czech Republic": {
    "Capital": "Prague",
    "Continent": "Europe",
    "Languages": "Czech"
  },
  "Democratic Republic of the Congo": {
    "Capital": "Kinshasa",
    "Continent": "Africa",
    "Languages": "French"
  },
  "Denmark": {
    "Capital": "Copenhagen",
    "Continent": "Europe",
    "Languages": "Danish"
  },
  "Djibouti": {
    "Capital": "Djibouti",
    "Continent": "Africa",
    "Languages": "Arabic, French"
  },
  "Dominica": {
    "Capital": "Roseau",
    "Continent": "North America",
    "Languages": "English"
  },
  "Dominican Republic": {
    "Capital": "Santo Domingo",
    "Continent": "North America",
    "Languages": "Spanish"
  },
  "East Timor": {
    "Capital": "Dili",
    "Continent": "Asia",
    "Languages": "Portuguese, Tetum"
  },
  "Ecuador": {
    "Capital": "Quito",
    "Continent": "South America",
    "Languages": "Spanish"
  },
  "Egypt": {
    "Capital": "Cairo",
    "Continent": "Africa",
    "Languages": "Arabic"
  },
  "El Salvador": {
    "Capital": "San Salvador",
    "Continent": "North America",
    "Languages": "Spanish"
  },
  "Equatorial Guinea": {
    "Capital": "Malabo",
    "Continent": "Africa",
    "Languages": "Spanish, French, Portuguese"
  },
  "Eritrea": {
    "Capital": "Asmara",
    "Continent": "Africa",
    "Languages": "Tigrinya, Arabic, English"
  },
  "Estonia": {
    "Capital": "Tallinn",
    "Continent": "Europe",
    "Languages": "Estonian"
  },
  "Ethiopia": {
    "Capital": "Addis Ababa",
    "Continent": "Africa",
    "Languages": "Amharic"
  },
  "Fiji": {
    "Capital": "Suva",
    "Continent": "Oceania",
    "Languages": "English, Fijian, Hindi"
  },
  "Finland": {
    "Capital": "Helsinki",
    "Continent": "Europe",
    "Languages": "Finnish, Swedish"
  },
  "France": {
    "Capital": "Paris",
    "Continent": "Europe",
    "Languages": "French"
  },
  "Gabon": {
    "Capital": "Libreville",
    "Continent": "Africa",
    "Languages": "French"
  },
  "Gambia": {
    "Capital": "Banjul",
    "Continent": "Africa",
    "Languages": "English"
  },
  "Georgia": {
    "Capital": "Tbilisi",
    "Continent": "Asia",
    "Languages": "Georgian"
  },
  "Germany": {
    "Capital": "Berlin",
    "Continent": "Europe",
    "Languages": "German"
  },
  "Ghana": {
    "Capital": "Accra",
    "Continent": "Africa",
    "Languages": "English"
  },
  "Greece": {
    "Capital": "Athens",
    "Continent": "Europe",
    "Languages": "Greek"
  },
  "Grenada": {
    "Capital": "Saint George's",
    "Continent": "North America",
    "Languages": "English"
  },
  "Guatemala": {
    "Capital": "Guatemala City",
    "Continent": "North America",
    "Languages": "Spanish"
  },
  "Guinea": {
    "Capital": "Conakry",
    "Continent": "Africa",
    "Languages": "French"
  },
  "Guinea-Bissau": {
    "Capital": "Bissau",
    "Continent": "Africa",
    "Languages": "Portuguese"
  },
  "Guyana": {
    "Capital": "Georgetown",
    "Continent": "South America",
    "Languages": "English"
  },
  "Haiti": {
    "Capital": "Port-au-Prince",
    "Continent": "North America",
    "Languages": "French, Haitian Creole"
  },
  "Honduras": {
    "Capital": "Tegucigalpa",
    "Continent": "North America",
    "Languages": "Spanish"
  },
  "Hungary": {
    "Capital": "Budapest",
    "Continent": "Europe",
    "Languages": "Hungarian"
  },
  "Iceland": {
    "Capital": "Reykjav\u00edk",
    "Continent": "Europe",
    "Languages": "Icelandic"
  },
  "India": {
    "Capital": "New Delhi",
    "Continent": "Asia",
    "Languages": "Hindi, English"
  },
  "Indonesia": {
    "Capital": "Jakarta",
    "Continent": "Asia",
    "Languages": "Indonesian"
  },
  "Iran": {
    "Capital": "Tehran",
    "Continent": "Asia",
    "Languages": "Persian" 
  },
  "Iraq": {
    "Capital": "Baghdad",
    "Continent": "Asia",
    "Languages": "Arabic, Kurdish"
  },
  "Ireland": {
    "Capital": "Dublin",
    "Continent": "Europe",
    "Languages": "Irish, English"
  },
  "Israel": {
    "Capital": "Jerusalem",
    "Continent": "Asia",
    "Languages": "Hebrew, Arabic"
  },
  "Italy": {
    "Capital": "Rome",
    "Continent": "Europe",
    "Languages": "Italian"
  },
  "Ivory Coast (C\u00f4te d'Ivoire)": {
    "Capital": "Yamoussoukro",
    "Continent": "Africa",
    "Languages": "French"
  },
  "Jamaica": {
    "Capital": "Kingston",
    "Continent": "North America",
    "Languages": "English"
  },
  "Japan": {
    "Capital": "Tokyo",
    "Continent": "Asia",
    "Languages": "Japanese"
  },
  "Jordan": {
    "Capital": "Amman",
    "Continent": "Asia",
    "Languages": "Arabic"
  },
  "Kazakhstan": {
    "Capital": "Nur-Sultan",
    "Continent": "Asia",
    "Languages": "Kazakh, Russian"
  },
  "Kenya": {
    "Capital": "Nairobi",
    "Continent": "Africa",
    "Languages": "English, Swahili"
  },
  "Kiribati": {
    "Capital": "Tarawa",
    "Continent": "Oceania",
    "Languages": "English, Gilbertese"
  },
  "Kuwait": {
    "Capital": "Kuwait City",
    "Continent": "Asia",
    "Languages": "Arabic"
  },
  "Kyrgyzstan": {
    "Capital": "Bishkek",
    "Continent": "Asia",
    "Languages": "Kyrgyz, Russian"
  },
  "Laos": {
    "Capital": "Vientiane",
    "Continent": "Asia",
    "Languages": "Lao"
  },
  "Latvia": {
    "Capital": "Riga",
    "Continent": "Europe",
    "Languages": "Latvian"
  },
  "Lebanon": {
    "Capital": "Beirut",
    "Continent": "Asia",
    "Languages": "Arabic"
  },
  "Lesotho": {
    "Capital": "Maseru",
    "Continent": "Africa",
    "Languages": "English, Sesotho"
  },
  "Liberia": {
    "Capital": "Monrovia",
    "Continent": "Africa",
    "Languages": "English"
  },
  "Libya": {
    "Capital": "Tripoli",
    "Continent": "Africa",
    "Languages": "Arabic"
  },
  "Liechtenstein": {
    "Capital": "Vaduz",
    "Continent": "Europe",
    "Languages": "German"
  },
  "Lithuania": {
    "Capital": "Vilnius",
    "Continent": "Europe",
    "Languages": "Lithuanian"
  },
  "Luxembourg": {
    "Capital": "Luxembourg",
    "Continent": "Europe",
    "Languages": "Luxembourgish, French, German"
  },
  "Madagascar": {
    "Capital": "Antananarivo",
    "Continent": "Africa",
    "Languages": "Malagasy, French"
  },
  "Malawi": {
    "Capital": "Lilongwe",
    "Continent": "Africa",
    "Languages": "English, Chichewa"
  },
  "Malaysia": {
    "Capital": "Kuala Lumpur",
    "Continent": "Asia",
    "Languages": "Malay"
  },
  "Maldives": {
    "Capital": "Mal\u00e9",
    "Continent": "Asia",
    "Languages": "Dhivehi"
  },
  "Mali": {
    "Capital": "Bamako",
    "Continent": "Africa",
    "Languages": "French"
  },
  "Malta": {
    "Capital": "Valletta",
    "Continent": "Europe",
    "Languages": "Maltese, English"
  },
  "Marshall Islands": {
    "Capital": "Majuro",
    "Continent": "Oceania",
    "Languages": "Marshallese, English"
  },
  "Mauritania": {
    "Capital": "Nouakchott",
    "Continent": "Africa",
    "Languages": "Arabic"
  },
  "Mauritius": {
    "Capital": "Port Louis",
    "Continent": "Africa",
    "Languages": "English, French"
  },
  "Mexico": {
    "Capital": "Mexico City",
    "Continent": "North America",
    "Languages": "Spanish"
  },
  "Micronesia": {
    "Capital": "Palikir",
    "Continent": "Oceania",
    "Languages": "English"
  },
  "Moldova": {
    "Capital": "Chi\u0219in\u0103u",
    "Continent": "Europe",
    "Languages": "Romanian"
  },
  "Monaco": {
    "Capital": "Monaco",
    "Continent": "Europe",
    "Languages": "French"
  },
  "Mongolia": {
    "Capital": "Ulaanbaatar",
    "Continent": "Asia",
    "Languages": "Mongolian"
  },
  "Montenegro": {
    "Capital": "Podgorica",
    "Continent": "Europe",
    "Languages": "Montenegrin"
  },
  "Morocco": {
    "Capital": "Rabat",
    "Continent": "Africa",
    "Languages": "Arabic, Berber"
  },
  "Mozambique": {
    "Capital": "Maputo",
    "Continent": "Africa",
    "Languages": "Portuguese"
  },
  "Namibia": {
    "Capital": "Windhoek",
    "Continent": "Africa",
    "Languages": "English"
  },
  "Nauru": {
    "Capital": "Yaren",
    "Continent": "Oceania",
    "Languages": "Nauruan, English"
  },
  "Nepal": {
    "Capital": "Kathmandu",
    "Continent": "Asia",
    "Languages": "Nepali"
  },
  "Netherlands": {
    "Capital": "Amsterdam",
    "Continent": "Europe",
    "Languages": "Dutch"
  },
  "New Zealand": {
    "Capital": "Wellington",
    "Continent": "Oceania",
    "Languages": "English, M\u0101ori"
  },
  "Nicaragua": {
    "Capital": "Managua",
    "Continent": "North America",
    "Languages": "Spanish"
  },
  "Niger": {
    "Capital": "Niamey",
    "Continent": "Africa",
    "Languages": "French"
  },
  "Nigeria": {
    "Capital": "Abuja",
    "Continent": "Africa",
    "Languages": "English"
  },
  "North Korea": {
    "Capital": "Pyongyang",
    "Continent": "Asia",
    "Languages": "Korean"
  },
  "North Macedonia": {
    "Capital": "Skopje",
    "Continent": "Europe",
    "Languages": "Macedonian"
  },
  "Norway": {
    "Capital": "Oslo",
    "Continent": "Europe",
    "Languages": "Norwegian"
  },
  "Oman": {
    "Capital": "Muscat",
    "Continent": "Asia",
    "Languages": "Arabic"
  },
  "Pakistan": {
    "Capital": "Islamabad",
    "Continent": "Asia",
    "Languages": "Urdu, English"
  },
  "Palau": {
    "Capital": "Ngerulmud",
    "Continent": "Oceania",
    "Languages": "Palauan, English"
  },
  "Panama": {
    "Capital": "Panama City",
    "Continent": "North America",
    "Languages": "Spanish"
  },
  "Papua New Guinea": {
    "Capital": "Port Moresby",
    "Continent": "Oceania",
    "Languages": "English, Tok Pisin, Hiri Motu"
  },
  "Paraguay": {
    "Capital": "Asunci\u00f3n",
    "Continent": "South America",
    "Languages": "Spanish, Guaran\u00ed"
  },
  "Peru": {
    "Capital": "Lima",
    "Continent": "South America",
    "Languages": "Spanish, Quechua, Aymara"
  },
  "Philippines": {
    "Capital": "Manila",
    "Continent": "Asia",
    "Languages": "Filipino, English"
  },
  "Poland": {
    "Capital": "Warsaw",
    "Continent": "Europe",
    "Languages": "Polish"
  },
  "Portugal": {
    "Capital": "Lisbon",
    "Continent": "Europe",
    "Languages": "Portuguese"
  },
  "Qatar": {
    "Capital": "Doha",
    "Continent": "Asia",
    "Languages": "Arabic"
  },
  "Republic of the Congo": {
    "Capital": "Brazzaville",
    "Continent": "Africa",
    "Languages": "French"
  },
  "Romania": {
    "Capital": "Bucharest",
    "Continent": "Europe",
    "Languages": "Romanian"
  },
  "South Korea": {
    "Capital": "Seoul",
    "Continent": "Asia",
    "Languages": "Korean"
  },
  "South Sudan": {
    "Capital": "Juba",
    "Continent": "Africa",
    "Languages": "English"
  },
  "Spain": {
    "Capital": "Madrid",
    "Continent": "Europe",
    "Languages": "Spanish"
  },
  "Sri Lanka": {
    "Capital": "Sri Jayewardenepura Kotte",
    "Continent": "Asia",
    "Languages": "Sinhala, Tamil"
  },
  "Sudan": {
    "Capital": "Khartoum",
    "Continent": "Africa",
    "Languages": "Arabic, English"
  },
  "Suriname": {
    "Capital": "Paramaribo",
    "Continent": "South America",
    "Languages": "Dutch"
  },
  "Sweden": {
    "Capital": "Stockholm",
    "Continent": "Europe",
    "Languages": "Swedish"
  },
  "Switzerland": {
    "Capital": "Bern",
    "Continent": "Europe",
    "Languages": "German, French, Italian, Romansh"
  },
  "Syria": {
    "Capital": "Damascus",
    "Continent": "Asia",
    "Languages": "Arabic"
  },
  "Tajikistan": {
    "Capital": "Dushanbe",
    "Continent": "Asia",
    "Languages": "Tajik"
  },
  "Tanzania": {
    "Capital": "Dodoma",
    "Continent": "Africa",
    "Languages": "Swahili, English"
  },
  "Thailand": {
    "Capital": "Bangkok",
    "Continent": "Asia",
    "Languages": "Thai"
  },
  "Togo": {
    "Capital": "Lom\u00e9",
    "Continent": "Africa",
    "Languages": "French"
  },
  "Tonga": {
    "Capital": "Nuku'alofa",
    "Continent": "Oceania",
    "Languages": "Tongan, English"
  },
  "Trinidad and Tobago": {
    "Capital": "Port of Spain",
    "Continent": "North America",
    "Languages": "English"
  },
  "Tunisia": {
    "Capital": "Tunis",
    "Continent": "Africa",
    "Languages": "Arabic"
  },
  "Turkey": {
    "Capital": "Ankara",
    "Continent": "Europe/Asia",
    "Languages": "Turkish"
  },
  "Turkmenistan": {
    "Capital": "Ashgabat",
    "Continent": "Asia",
    "Languages": "Turkmen"
  },
  "Tuvalu": {
    "Capital": "Funafuti",
    "Continent": "Oceania",
    "Languages": "Tuvaluan, English"
  },
  "Uganda": {
    "Capital": "Kampala",
    "Continent": "Africa",
    "Languages": "English, Swahili"
  },
  "Ukraine": {
    "Capital": "Kyiv",
    "Continent": "Europe",
    "Languages": "Ukrainian"
  },
  "United Arab Emirates": {
    "Capital": "Abu Dhabi",
    "Continent": "Asia",
    "Languages": "Arabic"
  },
  "United Kingdom": {
    "Capital": "London",
    "Continent": "Europe",
    "Languages": "English"
  },
  "United States": {
    "Capital": "Washington, D.C.",
    "Continent": "North America",
    "Languages": "English"
  },
  "Uruguay": {
    "Capital": "Montevideo",
    "Continent": "South America",
    "Languages": "Spanish"
  },
  "Uzbekistan": {
    "Capital": "Tashkent",
    "Continent": "Asia",
    "Languages": "Uzbek"
  },
  "Vanuatu": {
    "Capital": "Port Vila",
    "Continent": "Oceania",
    "Languages": "Bislama, English, French"
  },
  "Vatican City": {
    "Capital": "Vatican City",
    "Continent": "Europe",
    "Languages": "Italian, Latin"
  },
  "Venezuela": {
    "Capital": "Caracas",
    "Continent": "South America",
    "Languages": "Spanish"
  },
  "Vietnam": {
    "Capital": "Hanoi",
    "Continent": "Asia",
    "Languages": "Vietnamese"
  },
  "Yemen": {
    "Capital": "Sana'a",
    "Continent": "Asia",
    "Languages": "Arabic"
  },
  "Zambia": {
    "Capital": "Lusaka",
    "Continent": "Africa",
    "Languages": "English"
  },
  "Zimbabwe": {
    "Capital": "Harare",
    "Continent": "Africa",
    "Languages": "English"
  }
}


def create_card(c, path, x, y, width, height):  
    img = ImageReader(path)
    c.saveState()
    c.drawImage(img, x, y, width=width, height=height)
    c.restoreState()

def create_card_rotate(c, path, x, y, width, height, needRotation=False):
    
    img = ImageReader(path)

    if not needRotation:
        # Rotate 90 degrees (clockwise)
        c.saveState()
        c.translate(x + width, y)  # New origin after rotation
        c.rotate(90)
        c.drawImage(img, 0, 0, width=height, height=width)
        c.restoreState()

    else:
        # Rotate 180 degrees (upside-down)
        c.saveState()
        c.translate(x + width / 2, y + height / 2)
        c.rotate(360)
        c.drawImage(img, -width / 2, -height / 2, width=width, height=height)
        c.restoreState()

def create_details(c, country, obj, x, y, rotate, card_width, card_height):
    # Lines of text
    lines = [
        country,
        f"Capital: {obj['Capital']}",
        f"Continent: {obj['Continent']}",
        f"Languages: {obj['Languages']}"
    ]

    # Fonts and layout
    title_font = "Poppins-Bold"
    text_font = "Poppins-Regular"
    title_size = 16
    text_size = 12
    line_height = 16
    total_height = line_height * len(lines)

    # Center of the card
    center_x = x + card_width / 4
    center_y = y + card_height / 1.5

    # Start text object
    text = c.beginText()

    if rotate:
        c.saveState()
        c.translate(center_x, center_y)
        c.rotate(270)
        text.setTextOrigin(-2*cm, (total_height / 2 - line_height)+1*cm)  # Start from top
    else:
        text.setTextOrigin(center_x, center_y + total_height / 2 - line_height)

    # Render lines manually centered
    for i, line in enumerate(lines):
        font_name = title_font if i == 0 else text_font
        font_size = title_size if i == 0 else text_size
        padding = 1.0 * cm  # or try 0.5 * cm if that's too much
        max_line_width = (card_height if rotate else card_width) - 2 * padding

        wrapped = wrap_text(line, font_name, font_size, max_line_width)

        for wrapped_line in wrapped:
            text.setFont(font_name, font_size)
            text.textLine(wrapped_line)


    # Draw and cleanup
    c.drawText(text)
    if rotate:
        c.restoreState()

def wrap_text(line, font_name, font_size, max_width):
    words = line.split()
    wrapped_lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if stringWidth(test_line, font_name, font_size) <= max_width:
            current_line = test_line
        else:
            if current_line:
                wrapped_lines.append(current_line)
            current_line = word
    if current_line:
        wrapped_lines.append(current_line)
    return wrapped_lines

def generate_sided_pdf(output_path, file_name):
    PAGE_WIDTH, PAGE_HEIGHT = A4
    try:
      c = canvas.Canvas(output_path + "/" + file_name + '.pdf', pagesize=A4)
    except Exception as e:
        print(f"Error - choose a valid file path ({e}).")
        return
    countries = list(countries_data.keys())
    count =0
    count2 =0
    continue_custom = 0 
    for i in range(1, 23):
        for j in range(1, 5):
            try:
                create_card(c, rf'../FlagGame/flags/{country_ISO[countries[count]]}.jpg',11*cm, PAGE_HEIGHT-j*(6*cm + 1*cm) - 1*cm, 9*cm, 6*cm)

            except Exception:
                continue
            count+=1
        for j in range(1, 5):
            try:
              create_card(c, rf'../FlagGame/flags/{country_ISO[countries[count]]}.jpg',1*cm, PAGE_HEIGHT-j*(6*cm + 1*cm) - 1*cm, 9*cm, 6*cm)
            except Exception:
                continue
            count+=1
        c.showPage()
        for j in range(1, 5):
            try:
              create_details(c, countries[count2], countries_data[countries[count2]], 1*cm, PAGE_HEIGHT-j*(6*cm + 1*cm) - 1*cm, False, 9 * cm, 6 * cm)
            except Exception:
                continue
            count2+=1     
        for j in range(1, 5):
            try:
                create_details(c, countries[count2], countries_data[countries[count2]], 11*cm, PAGE_HEIGHT-j*(6*cm + 1*cm) - 1*cm, False, 9 * cm, 6 * cm)
            except Exception:
                continue
            count2+=1   
        c.showPage()
    
      #SPECIFICS - SET HERE MANUALLY!\
      # --- --- --- --- --- --- --- ---



      # --- --- --- --- --- --- --- ---
    c.save()




            

