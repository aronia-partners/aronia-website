# ARONIA website

A static Astro website for ARONIA LLC, hosted on GitHub Pages at https://aroniapartners.com.

## Develop

Use Node 24 and pnpm 11.25.0.

```sh
pnpm install --frozen-lockfile
pnpm dev
pnpm build
```

Default builds block indexing for review. Production builds use `SITE_RELEASE=production pnpm build`.

## Publish

The Deploy ARONIA website workflow builds the source and deploys `dist/` after changes to main, or when dispatched manually. The custom domain is preserved in public/CNAME. GitHub Pages must use GitHub Actions as its publishing source.

src/layouts/Base.astro owns shared metadata, navigation, footer, and logo animation. Service pages share src/components/ServicePage.astro. Page content is in src/pages, with responsive styles in src/styles/global.css. Approved web assets are in public/assets.

All booking and general contact actions open https://calendly.com/aronia/30min. The contact page also offers an email option. No contact form or advertising/analytics scripts are included. The privacy page sets a 12-month policy for unsuccessful inquiries; following that policy requires operational record cleanup.

## Images

Original photographs remain outside this repository. Published copies contain only approved referenced images with identifying photo metadata stripped. The outdoor portrait credit is Levi Vepsa, Kauppalehti. Event captions and historical claims follow Ville's approved website copy. The ACA stage photo has the lower speaker profile removed; the Inno Fire photo has the trophy name blurred. Preserve those edits when replacing assets.

## Verification and rollback

Run `python3 scripts/check-site.py` against a default review build for link, asset, heading, metadata, and input-label checks. Production indexing is checked separately before release. Test responsive layouts and booking links after content changes.

The original one-page root index.html and assets/ are retained for historical comparison. To roll back the initial migration, select branch main and root in Pages settings; later releases can be rolled back by reverting the release commit or rerunning a prior workflow revision.
