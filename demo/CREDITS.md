# Picture and type credits

NepalOS (Powered by GovTechNepal) does not use the national emblem. The photographs below are real pictures from Wikimedia Commons. They are not generated. Each one keeps the licence the photographer chose.

The browser demo shows the same credit on the wallpaper. The Debian image copies these files into `/usr/share/backgrounds/nepalos/`.

## Photographs

| File | Place | Author | Licence | Source |
| --- | --- | --- | --- | --- |
| `wallpapers/everest.jpg` | Mount Everest / सगरमाथा | Wang Lama Humla | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | https://commons.wikimedia.org/wiki/File:Mt.Everest.jpg |
| `wallpapers/himalaya.jpg` | Kali Gandaki valley, Himalaya / कालीगण्डकी उपत्यका | Vyacheslav Argenberg | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0) | https://commons.wikimedia.org/wiki/File:Kali_Gandaki_Valley,_Nepal,_Himalaya.jpg |
| `wallpapers/pashupatinath.jpg` | Pashupatinath, Surya Ghats / पशुपतिनाथ, सूर्य घाट | Gerd Eichmann | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | https://commons.wikimedia.org/wiki/File:Pashupatinath-Surya_Ghats-16-Verbrenner-2007-gje.jpg |
| `wallpapers/swayambhu.jpg` | Swayambhunath / स्वयम्भूनाथ | Vyacheslav Argenberg. Attribution requested as © Vyacheslav Argenberg / http://www.vascoplanet.com/ | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0) | https://commons.wikimedia.org/wiki/File:Swayambhu,_Kathmandu,_Nepal.jpg |
| `wallpapers/boudhanath.jpg` | Boudhanath / बौद्धनाथ | Sanish shr | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | https://commons.wikimedia.org/wiki/File:Boudhanath_Temple_Kathmandu.jpg |
| `wallpapers/patan.jpg` | Patan Durbar Square / पाटन दरबार क्षेत्र | Alexander Shafir | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | https://commons.wikimedia.org/wiki/File:Nepal_Patan_Durbar_Square_10_(full_res).jpg |

The files in this repository are 1600-pixel JPEG copies made for the demo and the desktop background. The Commons file is the original.

Share-alike applies to the five CC BY-SA photographs. A work that uses one of those pictures as a wallpaper should credit the photographer and link the licence, which the desktop caption and this file do.

## Keyboards

The Lipi repository `govtechnepal/tmp-7a225775f5ce0c97` was not readable from the build environment. The browser demo follows the Keyman keyboards `nepali_romanized` 1.0.1 and `nepali_traditional` 1.3.1 by Santosh Pradhan, MIT. Those keyboards record the Madan Puraskar Pratisthan Romanized and Traditional layouts. The MIT text is in `webdemo/data/KEYBOARDS-LICENSE.txt`.

## Preeti conversion

Character rules are from sapradhan/nep-ttf2utf (Apache-2.0), a port of foss-np/2utf8. The Preeti font file is not in the Debian packages.

## Fonts in the browser demo

Noto Sans and Noto Sans Devanagari are loaded from Google Fonts under the SIL Open Font License.

The prototype package `fonts-nepalos-kalimati` downloads `Kalimati.ttf` at build time from `https://github.com/mhnpd/nepali-font` (`fonts/Kalimati.ttf`). The name table says © Sanir Karmacharya and the file has no licence. That collection says the fonts are free to use and remain the intellectual property of their owners. It is not a free-software licence. Confirm redistribution rights before a production image. The browser demo still fetches the same file at runtime. If that fetch fails, the writer shows Noto Sans Devanagari and says so.

Preeti is not in the packages. `fonts/Preeti.TTF` is in the same repository, under the same unclear terms, so the Preeti package stays a skeleton. The demo may still fetch it for the legacy view.

The Dhaka-style diamond repeat in the panel and the splash is drawn for this project. It is not a scan of a particular topi or textile.
