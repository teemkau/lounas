# Avantin lounaat

Staattinen GitHub Pages -sivu Liedon Avantin lounaslistoille. Mukana Avantin Paviljonki, Kajuutta ja Pegasus Avanti.

## Käyttöönotto
1. Kopioi tiedostot repositorioon `teemkau/lounas` ja puske `main`-haaraan.
2. GitHubissa: **Settings → Pages → Source: GitHub Actions**.
3. Aja **Actions → Update lunch menus and deploy → Run workflow** kerran käsin.

Työnkulku hakee listat arkisin klo 06:00 UTC, päivittää `data.json`:n ja julkaisee sivun. Paviljongin oma sivu käyttää ajoittain botintorjuntaa, joten sille on varalähde. Jos lähdettä ei saada, sivu näyttää tiedon puuttuvana eikä vanhaa listaa uutena.
