# BUILDORA Trading — Official Website

> **Where Every Project Begins.**  
> Premium building materials supply across Dubai, UAE.

---

## 🚀 Deploying to GitHub Pages (Free Hosting)

### Step 1 — Create a GitHub Repository
1. Go to [github.com](https://github.com) and sign in
2. Click **New repository**
3. Name it: `buildoramaterials.com` *(or any name you like)*
4. Set it to **Public**
5. Click **Create repository**

### Step 2 — Upload the Website File
1. In your new repo, click **Add file → Upload files**
2. Upload the `index.html` file
3. Commit the changes

### Step 3 — Enable GitHub Pages
1. Go to your repo **Settings → Pages**
2. Under **Source**, select `main` branch and `/ (root)` folder
3. Click **Save**
4. GitHub will give you a URL like: `https://yourusername.github.io/buildoramaterials.com/`

### Step 4 — Connect Your Custom Domain `buildoramaterials.com`
1. In the **Pages** settings, enter `buildoramaterials.com` under **Custom domain**
2. GitHub will create a `CNAME` file automatically
3. Go to your **domain registrar** (GoDaddy, Namecheap, etc.)
4. Add these DNS records:

| Type  | Name | Value                  |
|-------|------|------------------------|
| A     | @    | 185.199.108.153        |
| A     | @    | 185.199.109.153        |
| A     | @    | 185.199.110.153        |
| A     | @    | 185.199.111.153        |
| CNAME | www  | yourusername.github.io |

5. Wait 24–48 hours for DNS propagation
6. Enable **Enforce HTTPS** in GitHub Pages settings (free SSL!)

---

## 🔍 SEO — Getting Found on Google

### Submit to Google Search Console
1. Go to [search.google.com/search-console](https://search.google.com/search-console)
2. Add your property: `https://buildoramaterials.com`
3. Verify ownership (Google will guide you)
4. Submit your sitemap: `https://buildoramaterials.com/sitemap.xml`

### Upload the sitemap
Upload the `sitemap.xml` file to the same repository alongside `index.html`.

---

## 📁 File Structure
```
/
├── index.html       ← Main website (upload this)
├── sitemap.xml      ← For Google indexing (upload this)
└── README.md        ← This file
```

---

## ✏️ Updating Content

To update contact details, products, or text:
1. Open `index.html` in any text editor (Notepad, VS Code, etc.)
2. Search (`Ctrl+F`) for the text you want to change
3. Edit and save
4. Re-upload to GitHub

---

## 📞 Support
**BUILDORA Trading** — sales@buildoramaterials.com  
Website: [buildoramaterials.com](https://buildoramaterials.com)
