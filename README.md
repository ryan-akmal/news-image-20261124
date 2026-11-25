[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/ryan-akmal/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/ryan-akmal/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

# The World in One Day — Tuesday, 24 November 2026

**make.fun competition:** `news-image-20261124` — "Sum up 24 November's world news in one image"
**Entry title:** The World in One Day — Tuesday, 24 November 2026

A one-page newspaper front page that sums up Tuesday 24 November 2026 in a
single image. The date is named in the masthead; six stories cover Yemen and
Saudi Arabia, Gaza, Europe, Ukraine, markets and sport, with six more in the
"Also in the news" strip.

## The six stories

1. **Houthis strike Riyadh tower** — Houthi missiles hit Riyadh's tallest
   tower for the second time in five days; 11 people injured.
2. **Israel kills Hamas security chief** — Israeli airstrikes kill Hamas
   internal security director Naeem Abu Nahel and six others in Gaza.
3. **Russia warns Estonia of war** — Moscow warns Estonia's plan to shut
   border crossings risks "open war".
4. **Flat hit in Zaporizhzhia** — An overnight Russian strike hits an
   apartment block: 2 killed, 40 wounded, including four children.
5. **Stocks slip on rate fears** — The S&P 500 falls 0.95% and the Euro
   Stoxx 50 1.16% as a Fed official signals higher rates may come.
6. **Senegal champions again** — Senegal are reinstated as 2025 Africa Cup
   of Nations champions after the sport's top court rules in their favour.

Also in the news: Putin admits Ukraine's oil strikes strain Russia's fuel
market; Iraq orders takeover of Kurdish oilfields; UN seeks probe into
Benghazi port attacks; Nepal hit by a 5.6 earthquake; Jensen Huang back as
Nvidia chief; Spain amnesties Puigdemont.

## How the image was made

`generate_image.py` draws the front page with Pillow: flat vector-style
pictograms and DejaVu typesetting, no photographs, no copied artwork, no
network. `main.ts` copies the finished `entry.png` to the output directory
the grader reads.

Run it: `python3 generate_image.py` (writes `entry.png`), then
`mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts`.
