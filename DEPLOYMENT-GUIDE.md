# Buildora Materials – GitHub Pages & Google SEO Guide
### Complete Step-by-Step Guide to Deploy & Rank on Google

---

## WHAT YOU WILL ACHIEVE
After following this guide:
- ✅ Your website live at **buildoramaterials.com** (or a free GitHub URL)
- ✅ Indexed and appearing on **Google Search**
- ✅ Professional SEO setup to climb Google rankings
- ✅ Google Search Console monitoring
- ✅ Google Analytics tracking

---

## PART 1 — DEPLOY TO GITHUB PAGES

### Step 1 — Create a GitHub Account (if you don't have one)
1. Go to **https://github.com**
2. Click **Sign up**
3. Enter your email → create username → set password
4. Verify your email address

---

### Step 2 — Create the Repository
1. After login, click the **"+"** icon (top-right) → **"New repository"**
2. Fill in:
   - **Repository name:** `buildoramaterials.github.io`
     > ⚠️ IMPORTANT: The name must be **exactly** `yourusername.github.io`
     > Example: if your GitHub username is `buildoratrading`, name it `buildoramaterials.github.io`
   - **Description:** "Buildora Materials Trading - Premium Building Materials Saudi Arabia"
   - Set to **Public** ✅
   - Check **"Add a README file"** ✅
3. Click **"Create repository"**

---

### Step 3 — Upload Your Website Files
You have 4 files to upload:
- `index.html` (main website)
- `sitemap.xml` (for Google)
- `robots.txt` (for Google)
- `404.html` (error page)

**Upload method (easiest — no coding needed):**

1. Open your new repository on GitHub
2. Click **"Add file"** → **"Upload files"**
3. Drag all 4 files into the upload area
4. Scroll down → In the "Commit changes" box, type: `Add website files`
5. Click **"Commit changes"**

---

### Step 4 — Enable GitHub Pages
1. In your repository, click **"Settings"** (top menu)
2. Scroll down → click **"Pages"** (left sidebar)
3. Under **"Branch"**, select **main** → select **/ (root)**
4. Click **"Save"**
5. Wait 2-3 minutes
6. Refresh the page — you'll see:
   > **"Your site is live at https://buildoramaterials.github.io"** 🎉

Test it by opening that link in your browser.

---

### Step 5 — Connect Your Custom Domain (buildoramaterials.com)
If you already own `buildoramaterials.com`:

**In GitHub:**
1. Go to Settings → Pages
2. Under "Custom domain", type: `buildoramaterials.com`
3. Click **Save** — this creates a CNAME file automatically

**In your domain registrar (GoDaddy / Namecheap / etc.):**
1. Log in to your domain registrar
2. Find **DNS Settings** for buildoramaterials.com
3. Add these **A records** (delete any old ones pointing to other IPs):
   ```
   Type: A    Name: @    Value: 185.199.108.153
   Type: A    Name: @    Value: 185.199.109.153
   Type: A    Name: @    Value: 185.199.110.153
   Type: A    Name: @    Value: 185.199.111.153
   ```
4. Add a **CNAME record**:
   ```
   Type: CNAME    Name: www    Value: buildoramaterials.github.io
   ```
5. Wait 24-48 hours for DNS to propagate

**Enable HTTPS (FREE SSL):**
1. Go back to GitHub → Settings → Pages
2. Check **"Enforce HTTPS"** ✅

---

## PART 2 — GOOGLE SEARCH RANKING (SEO)

### Step 6 — Submit to Google Search Console
This tells Google your site exists.

1. Go to **https://search.google.com/search-console**
2. Sign in with your Google account
3. Click **"Add property"** → choose **"URL prefix"**
4. Enter: `https://buildoramaterials.com`
5. Click **Continue**

**Verify ownership (choose one method):**

**Method A – HTML File (easiest):**
- Google gives you a file like `google1234abcd.html`
- Download it
- Upload it to your GitHub repository (same folder as index.html)
- Commit, wait 2 min, then click **Verify** in Google Search Console

**Method B – Meta tag:**
- Google gives you a meta tag like:
  `<meta name="google-site-verification" content="XXXXXX">`
- Open your `index.html`
- Paste it inside the `<head>` section (after the charset line)
- Commit the file → click **Verify**

---

### Step 7 — Submit Your Sitemap to Google
1. In Google Search Console, click **"Sitemaps"** (left sidebar)
2. In the "Add a new sitemap" box, type: `sitemap.xml`
3. Click **Submit**
4. Google will now crawl and index all your pages

---

### Step 8 — Request Google to Index Your Site NOW
Don't wait for Google to find you — ask directly:

1. In Google Search Console → click **"URL Inspection"**
2. Type your URL: `https://buildoramaterials.com`
3. Click **"Request Indexing"**
4. Repeat for: `https://buildoramaterials.com/#products`

Google typically indexes within **24-72 hours** for new sites.

---

### Step 9 — Set Up Google Analytics (Track Visitors)
1. Go to **https://analytics.google.com**
2. Sign in → click **"Start measuring"**
3. Create an account → Property name: "Buildora Materials"
4. Choose **Web** → enter your URL
5. Copy the **Measurement ID** (looks like `G-XXXXXXXXXX`)
6. Open your `index.html` in GitHub
7. Just before `</head>`, add:
   ```html
   <!-- Google Analytics -->
   <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
   <script>
     window.dataLayer = window.dataLayer || [];
     function gtag(){dataLayer.push(arguments);}
     gtag('js', new Date());
     gtag('config', 'G-XXXXXXXXXX');
   </script>
   ```
   Replace `G-XXXXXXXXXX` with your real ID.

---

## PART 3 — ADVANCED SEO TO RANK HIGHER

### Step 10 — Update Your sitemap.xml Date Monthly
Every time you update your website:
1. Open `sitemap.xml` in GitHub
2. Click the **pencil (edit)** icon
3. Update `<lastmod>` to today's date (e.g. `2025-05-10`)
4. Commit changes
5. Go to Google Search Console → Sitemaps → click **Refresh**

---

### Step 11 — Google Business Profile (CRITICAL for local ranking)
This puts you on **Google Maps** and local search results.

1. Go to **https://business.google.com**
2. Click **"Add your business"**
3. Fill in:
   - Business name: `Buildora Materials Trading`
   - Category: `Building Materials Supplier`
   - Location: Dammam, Eastern Province, Saudi Arabia
   - Phone number
   - Website: `https://buildoramaterials.com`
4. Verify your business (Google sends a postcard or calls)
5. Add photos of your products and office
6. Write a business description using keywords:
   > "Buildora Materials Trading is a premium building materials supplier in Dammam, Saudi Arabia. We supply electrical components, cables, plumbing, HVAC, lighting, safety equipment, power tools, and hardware from trusted brands including ABB, Schneider, Makita, Jotun, and Grundfos."

---

### Step 12 — WhatsApp Business Button (Extra Conversion)
Add a floating WhatsApp button for easy contact.
Open `index.html`, find `</body>` and add just before it:

```html
<!-- WhatsApp Float Button -->
<a href="https://wa.me/966XXXXXXXXX?text=Hello%2C%20I%20need%20a%20quote%20for%20building%20materials"
   target="_blank"
   rel="noopener"
   style="position:fixed;bottom:2rem;right:2rem;z-index:999;
          background:#25D366;color:#fff;width:56px;height:56px;
          border-radius:50%;display:flex;align-items:center;
          justify-content:center;font-size:1.8rem;
          box-shadow:0 4px 20px rgba(37,211,102,.4);
          text-decoration:none;transition:transform .3s"
   aria-label="Contact on WhatsApp"
   onmouseover="this.style.transform='scale(1.1)'"
   onmouseout="this.style.transform='scale(1)'">
  💬
</a>
```
Replace `966XXXXXXXXX` with your Saudi mobile number (e.g., 966501234567).

---

## PART 4 — SEO CONTENT STRATEGY (Rank higher over time)

### Keywords to Target
These are what your customers search on Google:

| Priority | Keyword | Search Intent |
|----------|---------|--------------|
| HIGH | building materials Dammam | Local buyer |
| HIGH | electrical materials supplier Saudi Arabia | B2B buyer |
| HIGH | cable supplier KSA | Industrial buyer |
| HIGH | plumbing materials Saudi Arabia | Contractor |
| MED | ABB distributor Dammam | Brand-specific |
| MED | Schneider Electric supplier Saudi Arabia | Brand-specific |
| MED | Makita tools Saudi Arabia | Tools buyer |
| MED | Jotun paint supplier KSA | Paint buyer |
| LOW | construction materials trading Dammam | General |

### Your website already uses ALL these keywords in:
- Page title ✅
- Meta description ✅
- H1, H2, H3 headings ✅
- Product descriptions ✅
- Footer ✅
- JSON-LD structured data ✅

---

## PART 5 — MONTHLY MAINTENANCE CHECKLIST

Do this every month to maintain and improve ranking:

| Task | How |
|------|-----|
| Check Google Search Console | Look for errors, fix any issues |
| Update sitemap date | Edit sitemap.xml → new date |
| Request re-index | URL Inspection → Request Indexing |
| Add new content | Add new products or news to website |
| Reply to Google reviews | Google Business Profile |
| Check Analytics | See which pages get most visitors |

---

## QUICK TROUBLESHOOTING

| Problem | Solution |
|---------|---------|
| Website not showing after enabling Pages | Wait 5-10 min, hard refresh (Ctrl+Shift+R) |
| Custom domain not working | Check DNS A records, wait 24-48 hours |
| Google not indexing | Submit sitemap, use URL Inspection → Request Indexing |
| HTTPS not available | Enable "Enforce HTTPS" in GitHub Pages settings |
| Site not ranking | Add Google Business Profile, build backlinks |

---

## HOW LONG TO RANK ON GOOGLE?

| Timeline | What to Expect |
|---------|---------------|
| Day 1-3 | Google finds and indexes your site |
| Week 1-2 | Appears for "Buildora Materials" search |
| Month 1-2 | Appears for local searches (Dammam building materials) |
| Month 3-6 | Competing for keyword rankings |
| 6+ months | Strong organic traffic with consistent updates |

> 💡 **Pro tip:** The biggest ranking boost for a local business is **Google Business Profile** + **customer reviews**. Encourage every customer to leave a Google review.

---

## FILE STRUCTURE SUMMARY

```
buildoramaterials.github.io/
├── index.html      ← Main website (SEO optimized)
├── sitemap.xml     ← Tells Google your pages
├── robots.txt      ← Guides search engine crawlers
└── 404.html        ← Custom error page
```

---

*Guide prepared for Buildora Materials Trading — May 2025*
