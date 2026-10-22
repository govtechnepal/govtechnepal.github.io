# govtechnepal.org

The static site for **GovTech Nepal**, an independent, open-source community project. It is not affiliated with the Government of Nepal.
Projects: NepalOS (Powered by GovTechNepal), Lipi, Rasuwa Flood Bulletin, and the Mountain fonts.

## Structure
- `/` English, `/ne/` Nepali (हजुर register). Pages: home, projects, nepalos, nepalos/slides, lipi, contribute, about, brand, 404.
- `/demo/`: NepalOS web demo (static).
- `/assets/` CSS, JS, Mukta + Khand fonts, images, `brand/` logo files.
- `/downloads/` NepalOS proposal (pptx/pdf); `lipi/` holds the Lipi builds.
- Root: favicons, site.webmanifest, browserconfig.xml, og-image, sitemap.xml, robots.txt, CNAME.
- `src/build.py`: the dependency-free generator (`python3 src/build.py` rewrites the pages).

## Deploy to GitHub Pages
1. Push the contents of this folder to `main` of `govtechnepal/govtechnepal.github.io`.
2. Settings → Pages → Source: *Deploy from a branch*, `main` / root.
3. The `CNAME` file sets `govtechnepal.org`. At your DNS provider, add A records for the apex pointing to 185.199.108.153, .109.153, .110.153 and .111.153, and a CNAME from `www` to `govtechnepal.github.io`.
4. Once the certificate is issued, enable *Enforce HTTPS*.
5. To preview locally, run `python3 -m http.server 8000`.

## TODO
- Put `Lipi-macOS-0.1.6.dmg` and `Lipi-chrome-0.1.6.zip` in `downloads/lipi/`, then run `python3 src/build.py`. The buttons show "Coming soon" until the files are there.
- Set the Windows installer Drive file to "Anyone with the link". It is private right now.
- Add the NepalOS ISO link once it's released.
- The demo loads Kalimati/Preeti from raw.githubusercontent.com at runtime. Self-host them if you need it to work offline.
