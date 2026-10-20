#!/usr/bin/env python3
"""Generates static SEO pages (compounds, learn, legal, 404) and sitemap.xml. Run: python3 tools/build-pages.py"""
import os, json, html
from datetime import date
SITE="https://nuveraform.com"; TODAY=date.today().isoformat()
RUO="For laboratory research use only. Not for human or veterinary use. Not a drug, food, supplement or cosmetic."

COMPOUNDS=[
("retatrutide","Retatrutide","Research peptide","A long-chain synthetic peptide that appears in the scientific literature as a multi-receptor agonist studied in metabolic research models.",
 [("Class","Synthetic peptide"),("Format","Lyophilized powder, sterile vial"),("Sizes listed","5 mg, 10 mg, 15 mg"),("Typical lab use","Receptor-binding and in-vitro metabolic assays")],
 "Retatrutide is a synthetic peptide that researchers describe as acting on more than one incretin-family receptor. It is used in laboratory work to study receptor signalling in cell-based assays. This page covers the physical product only."),
("bpc-157","BPC-157","Research peptide","A synthetic pentadecapeptide (15 amino acids) whose sequence is derived from a protein fragment found in gastric juice.",
 [("Class","Synthetic peptide, 15 residues"),("Format","Lyophilized powder, sterile vial"),("Offered as","BPC-157 / TB-500 blend, 10 mg and Recovery Duo bundle"),("Typical lab use","Cell-culture and tissue-model research")],
 "BPC-157 is a short synthetic peptide frequently referenced in preclinical literature. Nuvera Form lists it combined with TB-500 as a research blend. Product pages here describe the material, not any effect on people or animals."),
("tb-500","TB-500","Research peptide","A synthetic peptide related to a fragment of thymosin beta-4, supplied for laboratory investigation.",
 [("Class","Synthetic peptide"),("Format","Lyophilized powder, sterile vial"),("Offered as","BPC-157 / TB-500 blend, 10 mg"),("Typical lab use","Cell migration and cytoskeleton assays")],
 "TB-500 is named in the literature as a synthetic fragment connected to thymosin beta-4, a protein studied in cell biology. It is sold here in blend form for in-vitro research."),
("ghk-cu","GHK-Cu","Research peptide","A naturally occurring tripeptide (glycine-histidine-lysine) that binds copper(II), supplied as a lyophilized copper complex.",
 [("Class","Tripeptide–copper complex"),("Format","Lyophilized powder, sterile vial"),("Size listed","100 mg"),("Typical lab use","Cell-culture and extracellular-matrix research")],
 "GHK is a three-residue peptide with a strong affinity for copper ions. The copper complex is used in laboratory studies of cell and matrix biology."),
("thymosin-alpha-1","Thymosin Alpha 1","Research peptide","A 28-amino-acid peptide originally characterized from thymus tissue extracts, produced synthetically for research.",
 [("Class","Synthetic peptide, 28 residues"),("Format","Lyophilized powder, sterile vial"),("Size listed","10 mg"),("Typical lab use","Immunology cell-assay research")],
 "Thymosin alpha 1 is studied in immunology laboratories as a model peptide in cell-signalling work. Nuvera Form supplies it only as a research reagent."),
("nad-plus","NAD+","Research reagent","Nicotinamide adenine dinucleotide, a coenzyme found in all living cells and widely used in biochemical assays.",
 [("Class","Dinucleotide coenzyme"),("Format","Lyophilized powder, sterile vial"),("Size listed","500 mg"),("Typical lab use","Enzyme kinetics and cell-metabolism assays")],
 "NAD+ participates in redox reactions and is a common substrate in enzyme assays. As a research reagent it is used in biochemistry and cell-biology workflows."),
("cjc-1295-ipamorelin","CJC-1295 / Ipamorelin","Research blend","A combination of two synthetic peptides: a GHRH-analog sequence and a five-residue growth hormone secretagogue peptide.",
 [("Class","Two-peptide research blend"),("Format","Lyophilized powder, sterile vial"),("Size listed","10 mg"),("Typical lab use","Receptor-signalling assays")],
 "This blend pairs two synthetic sequences commonly discussed in endocrine-receptor research. It is supplied as a lyophilized blend for in-vitro work."),
("mots-c","MOTS-c","Research peptide","A 16-amino-acid peptide encoded in mitochondrial DNA, studied as a mitochondria-derived signalling peptide.",
 [("Class","Synthetic peptide, 16 residues"),("Format","Lyophilized powder, sterile vial"),("Size listed","10 mg"),("Typical lab use","Mitochondrial and cell-metabolism research")],
 "MOTS-c is notable because it is encoded by mitochondrial rather than nuclear DNA. Laboratories use the synthetic form in cell-based metabolic studies."),
("klow-blend","KLOW Blend","Research blend","A multi-component research blend supplied as a lyophilized powder; see the label for composition.",
 [("Class","Research blend"),("Format","Lyophilized powder, sterile vial"),("Size listed","Blend"),("Composition","Listed on the vial label; ask for documentation")],
 "KLOW is a blended research product. Request batch documentation for the exact composition of the lot you are ordering."),
("kisspeptin","Kisspeptin","Research peptide","A peptide product of the KISS1 gene, studied in neuroendocrine research; the short active fragment is kisspeptin-10.",
 [("Class","Synthetic peptide"),("Format","Lyophilized powder, sterile vial"),("Size listed","10 mg"),("Typical lab use","Receptor-binding and signalling assays")],
 "Kisspeptins signal through the KISS1 receptor and appear in neuroendocrine literature. Nuvera Form supplies kisspeptin strictly for in-vitro research."),
("bacteriostatic-water","Bacteriostatic Water","Reconstitution reagent","Sterile water containing 0.9% benzyl alcohol as a bacteriostatic preservative, used as a laboratory diluent.",
 [("Class","Sterile diluent"),("Format","Multi-dose vial"),("Size listed","10 ml"),("Typical lab use","Reconstituting lyophilized research material")],
 "Bacteriostatic water is sterile water with a small amount of benzyl alcohol that inhibits bacterial growth in a multi-use vial. Laboratories use it as a diluent according to their written protocols."),
]

LEARN=[
("what-research-use-only-means","What “research use only” means","A plain-English guide to the RUO label: what it covers, who it is for and what it rules out.",
 [("What the label says","Research use only (RUO) products are made and sold for laboratory investigation. They are not intended for use in diagnostic procedures, as drugs, or for any use in people or animals."),
  ("What it is not","An RUO product is not an approved medicine, food, dietary supplement or cosmetic. No statement on this site should be read as a health, dosing or treatment claim."),
  ("Who should buy","Qualified researchers and institutions aged 21 or older who will handle the material under appropriate laboratory practice and applicable law."),
  ("Why suppliers ask you to confirm","Reputable suppliers ask buyers to confirm RUO intent at sign-up and checkout so that the product reaches the right audience. Nuvera Form does this at account creation and again in the cart.")]),
("storing-lyophilized-peptides","Storing lyophilized peptides in the lab","General handling principles for freeze-dried research material, from receipt to the bench.",
 [("Why lyophilized","Freeze-drying removes water, which slows many degradation pathways and makes material easier to ship and store."),
  ("The usual principles","Keep vials sealed, dry, cold and away from light. Avoid repeated temperature swings, and let a cold vial reach room temperature before opening so condensation does not form."),
  ("After reconstitution","Reconstituted material is generally less stable than powder. Follow your institution’s written protocol for storage, labelling and discard dates."),
  ("Inspect on arrival","Do not use a vial with a damaged seal or visible contamination. If an order arrives damaged, email info@nuveraform.com within 72 hours.")]),
("how-to-read-a-certificate-of-analysis","How to read a certificate of analysis","What HPLC purity and mass spectrometry results mean, and what to check on any supplier’s paperwork.",
 [("HPLC purity","High-performance liquid chromatography separates a sample into components. The main peak’s share of the total area is reported as purity. A figure on its own says nothing without the method and the batch it came from."),
  ("Mass spectrometry","Mass spectrometry confirms the molecular mass of the main component, which helps verify identity. The measured mass should match the expected mass within the instrument’s tolerance."),
  ("What to check","Batch or lot number, date, the laboratory that ran the test, and whether the document matches the batch on your vial."),
  ("Our approach","Nuvera Form is publishing analytical documentation batch by batch. We do not claim test results we cannot show. Ask what is available for your order through the documentation request form.")]),
]

LEGAL=[
("privacy","Privacy Policy","How Nuvera Form collects, uses and protects the information you give us.",
 [("What we collect","Name, email address, phone number and field of research when you create an account; the email you give for newsletters or documentation requests; and order details when checkout opens."),
  ("How we use it","To create your account, apply your welcome discount, reply to requests, send order updates and, if you opt in, product announcements."),
  ("Who processes it","Form submissions are handled by Web3Forms; transactional email is sent through Resend; the site is hosted on Vercel. These providers process data only to deliver their service."),
  ("Your choices","Email info@nuveraform.com to access, correct or delete your data, or to unsubscribe. We do not sell personal information."),
  ("Cookies and storage","The site stores your age confirmation, cart and sign-in state in your browser’s local storage. It does not use advertising cookies.")]),
("terms","Terms of Sale","The conditions that apply when you buy from Nuvera Form.",
 [("Eligibility","Buyers must be 21 or older and purchase solely for laboratory research."),
  ("Research use only",RUO+" You are responsible for lawful handling, storage and disposal."),
  ("Pricing and stock","Prices and availability may change without notice. We may cancel an order if an item is unavailable or a price is shown in error, and will refund any payment taken."),
  ("Replacements","Report a damaged or incorrect item within 72 hours of delivery at info@nuveraform.com and we will replace it."),
  ("Liability","To the extent permitted by law, Nuvera Form is not liable for misuse of products or for losses arising from use outside these terms.")]),
("shipping-returns","Shipping & Returns","Dispatch times, delivery, costs and what to do if something is wrong.",
 [("Dispatch","Orders typically dispatch within 1–2 business days of payment."),
  ("Delivery","Domestic delivery is typically 3–5 business days after dispatch. A tracking link is emailed when your order leaves."),
  ("Cost","Orders over $200 after discounts ship free. Smaller orders ship at a flat $15."),
  ("Damaged or incorrect items","Email info@nuveraform.com within 72 hours of delivery with your order number and a photo. We will replace the item."),
  ("Returns","Because of the nature of the products, opened or used vials cannot be returned.")]),
("research-use-policy","Research Use Policy","The conditions under which Nuvera Form supplies its products.",
 [("Scope",RUO),
  ("Buyer confirmation","By creating an account and again at checkout you confirm you are 21 or older and buying for laboratory research."),
  ("No health claims","Nuvera Form does not make, and our staff and assistant will not answer, questions about dosing, injection, or use in people or animals."),
  ("Right to refuse","We may refuse or cancel any order where we believe a product will be used outside this policy.")]),
]

def e(s): return html.escape(s,quote=True)
def head(title,desc,path,extra="",og=True):
    url=f"{SITE}{path}"
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<meta name="robots" content="index,follow,max-image-preview:large"><meta name="theme-color" content="#F7F0E3">
<link rel="canonical" href="{url}"><link rel="icon" href="/favicon.ico?v=hd" sizes="any"><link rel="icon" href="/favicon-32.png?v=hd" type="image/png" sizes="32x32"><link rel="icon" href="/icon-192.png?v=hd" type="image/png" sizes="192x192"><link rel="apple-touch-icon" href="/apple-touch-icon.png?v=hd">
<meta property="og:type" content="website"><meta property="og:site_name" content="Nuvera Form"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/og.png?v=hd"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{SITE}/og.png?v=hd">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">{extra}</head>'''
def crumbs_ld(items):
    return '<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":SITE+p} for i,(n,p) in enumerate(items)]})+'</script>'
def top():
    return '''<body><a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap bar"><a class="logo" href="/"><img src="/assets/nuvera-logo-hd-96.png" srcset="/assets/nuvera-logo-hd-96.png 1x, /assets/nuvera-logo-hd-144.png 2x, /assets/nuvera-logo-hd-192.png 3x" alt="" width="48" height="48" class="brandmark"><span class="t">Nuvera Form</span></a>
<nav class="m" aria-label="Main"><a href="/#catalog">Catalog</a><a href="/compounds">Compounds</a><a href="/learn">Learn</a><a href="/#faq">FAQ</a></nav></div></header>'''
def foot():
    return f'''<footer class="f"><div class="wrap"><div class="fg">
<div><h4>Nuvera Form</h4><p>Research peptides and reconstitution reagents for qualified laboratories.</p></div>
<div><h4>Compounds</h4><ul>{"".join(f'<li><a href="/compounds/{s}">{e(n)}</a></li>' for s,n,*_ in COMPOUNDS[:6])}<li><a href="/compounds">All compounds</a></li></ul></div>
<div><h4>Learn</h4><ul>{"".join(f'<li><a href="/learn/{s}">{e(t)}</a></li>' for s,t,*_ in LEARN)}</ul></div>
<div><h4>Company</h4><ul><li><a href="/shipping-returns">Shipping &amp; Returns</a></li><li><a href="/privacy">Privacy Policy</a></li><li><a href="/terms">Terms of Sale</a></li><li><a href="/research-use-policy">Research Use Policy</a></li><li><a href="mailto:info@nuveraform.com">info@nuveraform.com</a></li></ul></div>
</div><div class="legal"><p><strong>{RUO}</strong></p><p>Copyright © 2026 Nuvera Form. All rights reserved.</p></div></div></footer></body></html>'''
def write(path,content):
    fp=path.lstrip("/")+".html"
    os.makedirs(os.path.dirname(fp) or ".",exist_ok=True)
    open(fp,"w").write(content)
def cta():
    return '<p style="margin-top:2rem"><a class="btn" href="/#catalog">View catalog and pricing</a> <a class="btn ghost" href="/#catalog">Create a free account</a></p>'
urls=[("/",1.0),("/compounds",0.9),("/learn",0.7)]

for s,n,kind,tag,specs,body in COMPOUNDS:
    path=f"/compounds/{s}"
    title=f"{n} | Research Peptide Specifications | Nuvera Form"
    desc=f"{n} for laboratory research: format, sizes and handling notes. {RUO.split('.')[0]}. Ships from the U.S. in 1–2 business days."
    related="".join(f'<div class="card"><h3>{e(m[1])}</h3><p>{e(m[3])}</p><a class="more" href="/compounds/{m[0]}">View specifications →</a></div>' for m in COMPOUNDS if m[0]!=s)[:0]
    others=[m for m in COMPOUNDS if m[0]!=s][:3]
    rel="".join(f'<div class="card"><h3>{e(m[1])}</h3><p>{e(m[3])}</p><a class="more" href="{"/compounds/"+m[0]}">View specifications →</a></div>' for m in others)
    ld='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"WebPage","name":title,"description":desc,"url":SITE+path,"isPartOf":{"@type":"WebSite","name":"Nuvera Form","url":SITE}})+'</script>'+crumbs_ld([("Home","/"),("Compounds","/compounds"),(n,path)])
    page=head(title,desc,path,ld)+top()+f'''<main id="main"><div class="wrap prose">
<p class="crumbs"><a href="/">Home</a> / <a href="/compounds">Compounds</a> / {e(n)}</p>
<span class="badge">{e(kind)} · Research use only · 21+</span><h1>{e(n)}</h1><p class="lede">{e(tag)}</p>
<h2>Specifications</h2><table>{"".join(f"<tr><th>{e(a)}</th><td>{e(b)}</td></tr>" for a,b in specs)}</table>
<h2>About this material</h2><p>{e(body)}</p>
<h2>Handling</h2><p>Store lyophilized vials sealed, dry, cold and away from light, and follow your institution’s written protocol. See <a href="/learn/storing-lyophilized-peptides">storing lyophilized peptides</a>.</p>
<h2>Documentation</h2><p>Analytical documentation is being published batch by batch. <a href="mailto:info@nuveraform.com?subject=Documentation%20request%3A%20{e(n)}">Email us</a> to ask what is available for your order.</p>
<div class="note"><strong>Research use only.</strong> {RUO} Nothing on this page is a statement about effects, dosing or use in people or animals.</div>{cta()}
<h2>Other compounds</h2><div class="grid">{rel}</div></div></main>'''+foot()
    write(path,page); urls.append((path,0.8))

cards="".join(f'<div class="card"><span class="badge">{e(k)}</span><h3 style="margin-top:.6rem">{e(n)}</h3><p>{e(t)}</p><a class="more" href="/compounds/{s}">View specifications →</a></div>' for s,n,k,t,*_ in COMPOUNDS)
write("/compounds",head("Research Compounds | Nuvera Form","Browse Nuvera Form’s research peptides and reconstitution reagents with format, size and handling notes. Research use only, 21+.","/compounds",crumbs_ld([("Home","/"),("Compounds","/compounds")]))+top()+f'''<main id="main"><div class="wrap"><p class="crumbs"><a href="/">Home</a> / Compounds</p><h1>Research compounds</h1><p class="lede">Specifications and handling notes for every compound in the catalog. Pricing is shown to registered researchers in the <a href="/#catalog">catalog</a>.</p><div class="grid" style="margin-top:1.5rem">{cards}</div>{cta()}</div></main>'''+foot())

def article(s,t,d,secs,section,dirp):
    path=f"/{dirp}/{s}" if dirp else f"/{s}"
    ld=crumbs_ld([("Home","/")]+([(section,f"/{dirp}")] if dirp else [])+[(t,path)])
    if dirp=="learn": ld+='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"Article","headline":t,"description":d,"dateModified":TODAY,"mainEntityOfPage":SITE+path,"author":{"@type":"Organization","name":"Nuvera Form"},"publisher":{"@type":"Organization","name":"Nuvera Form"}})+'</script>'
    crumb=f'<a href="/">Home</a> / '+(f'<a href="/{dirp}">{section}</a> / ' if dirp else '')+e(t)
    return head(f"{t} | Nuvera Form",d,path,ld)+top()+f'''<main id="main"><div class="wrap prose"><p class="crumbs">{crumb}</p><h1>{e(t)}</h1><p class="lede">{e(d)}</p>{"".join(f"<h2>{e(a)}</h2><p>{e(b)}</p>" for a,b in secs)}<div class="note"><strong>Research use only.</strong> {RUO}</div></div></main>'''+foot()
for s,t,d,secs in LEARN:
    write(f"/learn/{s}",article(s,t,d,secs,"Learn","learn")); urls.append((f"/learn/{s}",0.7))
lc="".join(f'<div class="card"><h3>{e(t)}</h3><p>{e(d)}</p><a class="more" href="/learn/{s}">Read the guide →</a></div>' for s,t,d,_ in LEARN)
write("/learn",head("Learn | Research Peptide Guides | Nuvera Form","Plain-English guides on research-use-only labelling, storing lyophilized peptides and reading a certificate of analysis.","/learn",crumbs_ld([("Home","/"),("Learn","/learn")]))+top()+f'<main id="main"><div class="wrap"><p class="crumbs"><a href="/">Home</a> / Learn</p><h1>Learn</h1><p class="lede">Practical, non-clinical guides for laboratory buyers.</p><div class="grid" style="margin-top:1.5rem">{lc}</div></div></main>'+foot())
for s,t,d,secs in LEGAL:
    write(f"/{s}",article(s,t,d,secs,"",""));urls.append((f"/{s}",0.3))

write("/404",head("Page not found | Nuvera Form","The page you are looking for could not be found.","/404").replace('index,follow','noindex')+top()+'<main id="main"><div class="wrap prose"><h1>Page not found</h1><p class="lede">That page does not exist or has moved.</p><p><a class="btn" href="/">Back to the home page</a> <a class="btn ghost" href="/compounds">Browse compounds</a></p></div></main>'+foot())
os.rename("404.html","404.html") if os.path.exists("404.html") else None

sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f'<url><loc>{SITE}{p if p!="/" else "/"}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n' for p,pr in urls)+'</urlset>\n'
open("sitemap.xml","w").write(sm)
print(len(urls),"urls")
