#!/usr/bin/env python3
"""Generates static SEO pages (compounds, learn, legal, 404) and sitemap.xml. Run: python3 tools/build-pages.py"""
import os, json, html
from datetime import date
SITE="https://www.nuveraform.com"; TODAY=date.today().isoformat()
RUO="Research compounds are for laboratory research use only. Not for human or veterinary use. Not a drug, food, supplement or cosmetic. Nuvera Form skincare products are cosmetics for external use."

COMPOUNDS=[
("glp-3","GLP-3","Research peptide","A long-chain synthetic peptide that appears in the scientific literature as a multi-receptor agonist studied in metabolic research models.",
 [("Class","Synthetic peptide"),("Format","Lyophilized powder, sterile vial"),("Sizes listed","5 mg, 10 mg, 15 mg"),("Typical lab use","Receptor-binding and in-vitro metabolic assays")],
 "GLP-3 is a synthetic peptide that researchers describe as acting on more than one incretin-family receptor. It is used in laboratory work to study receptor signalling in cell-based assays. This page covers the physical product only."),
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
("cagrilintide","Cagrilintide","Research peptide","A long-acting synthetic amylin-analogue peptide described in the literature as a model for amylin-receptor research.",
 [("Class","Synthetic acylated peptide"),("Format","Lyophilized powder, sterile vial"),("Size listed","5 mg"),("Typical lab use","Receptor-binding and in-vitro metabolic assays")],
 "Cagrilintide is a synthetic analogue of amylin, a peptide hormone studied alongside incretins in metabolic research. It is supplied here as a lyophilized research reagent. This page covers the physical product only."),
("dsip","DSIP","Research peptide","Delta sleep-inducing peptide, a nine-amino-acid neuropeptide first characterized in the 1970s and produced synthetically for research.",
 [("Class","Synthetic nonapeptide"),("Format","Lyophilized powder, sterile vial"),("Size listed","10 mg"),("Typical lab use","Neuropeptide and cell-signalling research")],
 "DSIP is a short neuropeptide referenced in neuroscience literature. Nuvera Form supplies it only as a lyophilized research reagent for in-vitro work."),
("tesamorelin","Tesamorelin","Research peptide","A synthetic 44-amino-acid analogue of growth hormone-releasing hormone (GHRH) with a modified N-terminus.",
 [("Class","Synthetic peptide, 44 residues"),("Format","Lyophilized powder, sterile vial"),("Size listed","10 mg"),("Typical lab use","GHRH-receptor signalling assays")],
 "Tesamorelin is a stabilized GHRH analogue used in laboratory studies of GHRH-receptor signalling. It is sold here as a research reagent only and is not a medicine."),
("kpv","KPV","Research peptide","A three-amino-acid peptide (lysine-proline-valine) matching the C-terminal end of alpha-melanocyte-stimulating hormone.",
 [("Class","Synthetic tripeptide"),("Format","Lyophilized powder, sterile vial"),("Size listed","10 mg"),("Typical lab use","Cell-culture research")],
 "KPV is a tripeptide fragment of alpha-MSH studied in cell-culture models. It is supplied as a lyophilized reagent for laboratory investigation."),
("5-amino-1mq","5-Amino-1MQ","Research compound","A small-molecule methylquinolinium compound studied as an inhibitor of the enzyme nicotinamide N-methyltransferase (NNMT).",
 [("Class","Small molecule (quinolinium)"),("Format","Lyophilized powder, sterile vial"),("Size listed","10 mg"),("Typical lab use","Enzyme-inhibition assays")],
 "5-Amino-1MQ is a small molecule used in biochemistry research on NNMT, an enzyme involved in cellular methylation and NAD+ metabolism. It is supplied as a research reagent only."),
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
 [("Payment","We accept Zelle. After you place an order we email your order number and Zelle details; include the order number in the Zelle memo."),
  ("Dispatch","Orders typically dispatch within 1–2 business days of receiving payment."),
  ("Delivery","Ground delivery is typically 3–5 business days after dispatch; overnight orders arrive the next business day after dispatch. A tracking link is emailed when your order leaves."),
  ("Cost","Ground shipping is a flat $25 per order, free on orders of $250 or more after discounts. Overnight shipping is a flat $60 per order."),
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
<link rel="stylesheet" href="/assets/site.css"><script defer src="/_vercel/insights/script.js"></script>{extra}</head>'''
def crumbs_ld(items):
    return '<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":SITE+p} for i,(n,p) in enumerate(items)]})+'</script>'
def top():
    return '''<body><a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap bar"><a class="logo" href="/"><img src="/assets/nuvera-logo-hd-96.png" srcset="/assets/nuvera-logo-hd-96.png 1x, /assets/nuvera-logo-hd-144.png 2x, /assets/nuvera-logo-hd-192.png 3x" alt="" width="48" height="48" class="brandmark"><span class="t">Nuvera Form</span></a>
<nav class="m" aria-label="Main"><a href="/#catalog">Catalog</a><a href="/compounds">Compounds</a><a href="/learn">Learn</a><a href="/about">About</a><a href="/#faq">FAQ</a></nav></div></header>'''
def foot():
    return f'''<footer class="f"><div class="wrap"><div class="fg">
<div><h4>Nuvera Form</h4><p>Research peptides and reconstitution reagents for qualified laboratories.</p></div>
<div><h4>Compounds</h4><ul>{"".join(f'<li><a href="/compounds/{s}">{e(n)}</a></li>' for s,n,*_ in COMPOUNDS[:6])}<li><a href="/compounds">All compounds</a></li></ul></div>
<div><h4>Learn</h4><ul>{"".join(f'<li><a href="/learn/{s}">{e(t)}</a></li>' for s,t,*_ in LEARN+[(x[0],x[1]) for x in NEW_LEARN])}</ul></div>
<div><h4>Company</h4><ul><li><a href="/about">About us</a></li><li><a href="/shipping-returns">Shipping &amp; Returns</a></li><li><a href="/privacy">Privacy Policy</a></li><li><a href="/terms">Terms of Sale</a></li><li><a href="/research-use-policy">Research Use Policy</a></li><li><a href="mailto:info@nuveraform.com">info@nuveraform.com</a></li></ul></div>
</div><div class="legal"><p><strong>{RUO}</strong></p><p>Copyright © 2026 Nuvera Form. All rights reserved.</p></div></div></footer></body></html>'''
def write(path,content):
    fp=path.lstrip("/")+".html"
    os.makedirs(os.path.dirname(fp) or ".",exist_ok=True)
    open(fp,"w").write(content)
def cta():
    return '<p style="margin-top:2rem"><a class="btn" href="/#catalog">View catalog and pricing</a> <a class="btn ghost" href="/#catalog">Create a free account</a></p>'
urls=[("/",1.0),("/compounds",0.9),("/learn",0.7)]

import re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seo_data import PRODUCTS, NEW_LEARN
# Read prices and stock from the storefront so product data always matches the catalog.
_src=open("index.html").read()
CAT={}
for m in re.finditer(r"\{id:'(\w+)',n:'([^']+)'[^\n]*?v:\{(.*)\}\}", _src):
    vs=re.findall(r"'([^']+)':\{p:([\d.]+),s:(null|\d+)\}", m.group(3))
    CAT[m.group(1)]=dict(n=m.group(2),v=[(a,float(b),None if c=="null" else int(c)) for a,b,c in vs])
NAMES={s:n for s,n,*_ in COMPOUNDS}
def money(x): return f"${x:,.2f}".replace(".00","")
def offers_for(info):
    rows=[]
    for cid in info["ids"]:
        for size,price,stock in CAT[cid]["v"]:
            rows.append((CAT[cid]["n"],size,price,stock))
    return rows

SHIP_LD={"@type":"OfferShippingDetails","shippingRate":{"@type":"MonetaryAmount","value":25,"currency":"USD"},"shippingDestination":{"@type":"DefinedRegion","addressCountry":"US"},
 "deliveryTime":{"@type":"ShippingDeliveryTime","handlingTime":{"@type":"QuantitativeValue","minValue":1,"maxValue":2,"unitCode":"DAY"},"transitTime":{"@type":"QuantitativeValue","minValue":1,"maxValue":5,"unitCode":"DAY"}}}
RET_LD={"@type":"MerchantReturnPolicy","applicableCountry":"US","returnPolicyCategory":"https://schema.org/MerchantReturnNotPermitted"}

# product photo per compound page (add more slugs as photos are made)
PAGE_IMG={"glp-3":("/assets/products/glp-3-10mg-studio.jpg","GLP-3 10 mg vial",1200,1200),
 "ghk-cu":("/assets/products/ghk-cu-100mg-studio.jpg","GHK-Cu 100 mg vial",1200,1200),
 "thymosin-alpha-1":("/assets/products/thymosin-alpha-1-10mg-studio.jpg","Thymosin Alpha 1 10 mg vial",1200,1200),
 "bpc-157":("/assets/products/bpc-157-tb-500-10mg-studio.jpg","BPC-157 / TB-500 10 mg vial",1200,1200),
 "tb-500":("/assets/products/bpc-157-tb-500-10mg-studio.jpg","BPC-157 / TB-500 10 mg vial",1200,1200),
 "nad-plus":("/assets/products/nad-plus-500mg-studio.jpg","NAD+ 500 mg vial",1200,1200),
 "cjc-1295-ipamorelin":("/assets/products/cjc-1295-ipamorelin-10mg-studio.jpg","CJC-1295 / Ipamorelin 10 mg vial",1200,1200),
 "mots-c":("/assets/products/mots-c-10mg-studio.jpg","MOTS-c 10 mg vial",1200,1200),
 "klow-blend":("/assets/products/klow-blend-studio.jpg","KLOW blend vial",1200,1200),
 "kisspeptin":("/assets/products/kisspeptin-10mg-studio.jpg","Kisspeptin 10 mg vial",1200,1200),
 "bacteriostatic-water":("/assets/products/bacteriostatic-water-10ml-studio.jpg","Bacteriostatic water 10 ml vial",1200,1200),
 "cagrilintide":("/assets/products/cagrilintide-5mg-studio.jpg","Cagrilintide 5 mg vial",1200,1200),
 "dsip":("/assets/products/dsip-10mg-studio.jpg","DSIP 10 mg vial",1200,1200),
 "tesamorelin":("/assets/products/tesamorelin-10mg-studio.jpg","Tesamorelin 10 mg vial",1200,1200),
 "kpv":("/assets/products/kpv-10mg-studio.jpg","KPV 10 mg vial",1200,1200),
 "5-amino-1mq":("/assets/products/5-amino-1mq-10mg-studio.jpg","5-Amino-1MQ 10 mg vial",1200,1200),
}
for s,n,kind,tag,specs,body in COMPOUNDS:
    info=PRODUCTS[s]; path=f"/compounds/{s}"
    title=info["title"]; desc=info["desc"]
    rows=offers_for(info); low=min(r[2] for r in rows); high=max(r[2] for r in rows)
    avail=any(r[3] is None or r[3]>0 for r in rows)
    product={"@context":"https://schema.org","@type":"Product","name":n,"description":tag,"sku":"NF-"+info["ids"][0].upper(),
        "brand":{"@type":"Brand","name":"Nuvera Form"},"category":kind,"image":[SITE+PAGE_IMG[s][0]] if s in PAGE_IMG else [SITE+"/og.png"],"url":SITE+path,
        "offers":{"@type":"AggregateOffer","priceCurrency":"USD","lowPrice":low,"highPrice":high,"offerCount":len(rows),
          "availability":"https://schema.org/"+("InStock" if avail else "OutOfStock"),"url":SITE+path,
          "seller":{"@type":"Organization","name":"Nuvera Form"},"shippingDetails":SHIP_LD,"hasMerchantReturnPolicy":RET_LD}}
    faq={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in info["faqs"]]}
    ld="".join('<script type="application/ld+json">'+json.dumps(x)+'</script>' for x in (product,faq))+crumbs_ld([("Home","/"),("Compounds","/compounds"),(n,path)])
    price_rows="".join(f"<tr><th>{e(nm if len(info['ids'])==1 and len(rows)==1 else (size if nm==n else nm+' · '+size))}</th><td>{money(p)}</td></tr>" for nm,size,p,_ in rows)
    bundle_rows=""
    for b in info.get("bundles",[]):
        bn=CAT[b]["n"]; bp=CAT[b]["v"][0][1]
        bundle_rows+=f"<tr><th>Bundle: {e(bn)}</th><td>{money(bp)}</td></tr>"
    rel="".join(f'<div class="card"><h3>{e(NAMES[r])}</h3><p>{e(next(m[3] for m in COMPOUNDS if m[0]==r))}</p><a class="more" href="/compounds/{r}">View {e(NAMES[r])} →</a></div>' for r in info["related"])
    guides=[x for x in NEW_LEARN if s in x[4]][:2]
    guide_links="".join(f'<li><a href="/learn/{g[0]}">{e(g[1])}</a></li>' for g in guides)+'<li><a href="/learn/storing-lyophilized-peptides">Storing lyophilized peptides in the lab</a></li>'
    faq_html="".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q,a in info["faqs"])
    page=head(title,desc,path,ld)+top()+f'''<main id="main"><div class="wrap prose">
<p class="crumbs"><a href="/">Home</a> / <a href="/compounds">Compounds</a> / {e(n)}</p>
<span class="badge">{e(kind)} · Research use only · 21+</span><h1>{e(n)}</h1><p class="lede">{e(tag)}</p>
{(f'<img src="{PAGE_IMG[s][0]}" alt="{e(PAGE_IMG[s][1])}" width="{PAGE_IMG[s][2]}" height="{PAGE_IMG[s][3]}" style="width:100%;max-width:{'22rem' if PAGE_IMG[s][2]==PAGE_IMG[s][3] else '16rem'};height:auto;border-radius:1rem;display:block;margin:1rem 0" fetchpriority="high">\n') if s in PAGE_IMG else ""}<p><strong>From {money(low)}</strong> · {"In stock" if avail else "Out of stock"} · Ships from the U.S. in 1–2 business days</p>
<h2>Specifications</h2><table>{"".join(f"<tr><th>{e(a)}</th><td>{e(b)}</td></tr>" for a,b in specs)}</table>
<h2>Sizes and pricing</h2><table>{price_rows}{bundle_rows}</table>
<p style="font-size:.85rem">Create a free account to order. First order: 10% off with NUVERA10. Shipping: $25 ground, free on $250+; $60 overnight.</p>
<h2>About this material</h2><p>{e(body)}</p>
<h2>Handling</h2><p>Store lyophilized vials sealed, dry, cold and away from light, and follow your institution’s written protocol.</p><ul>{guide_links}</ul>
<h2>Documentation</h2><p>Analytical documentation is being published batch by batch. <a href="mailto:info@nuveraform.com?subject=Documentation%20request%3A%20{e(n)}">Email us</a> to ask what is available for your order.</p>
<h2>Reviews</h2><div id="reviews" data-ids="{",".join(info["ids"])}"><p data-summary></p><div data-list><p>Loading reviews…</p></div></div><script src="/assets/reviews.js" defer></script>
<h2>{e(n)} FAQ</h2>{faq_html}
<div class="note"><strong>Research use only.</strong> {RUO} Nothing on this page is a statement about effects, dosing or use in people or animals.</div>{cta()}
<h2>Related compounds</h2><div class="grid">{rel}</div></div></main>'''+foot()
    write(path,page); urls.append((path,0.8))

cards="".join(f'<div class="card"><span class="badge">{e(k)}</span><h3 style="margin-top:.6rem">{e(n)}</h3><p>{e(t)}</p><a class="more" href="/compounds/{s}">View specifications →</a></div>' for s,n,k,t,*_ in COMPOUNDS)
write("/compounds",head("Research Compounds | Nuvera Form","Browse Nuvera Form’s research peptides and reconstitution reagents with format, size and handling notes. Research use only, 21+.","/compounds",crumbs_ld([("Home","/"),("Compounds","/compounds")]))+top()+f'''<main id="main"><div class="wrap"><p class="crumbs"><a href="/">Home</a> / Compounds</p><h1>Research compounds</h1><p class="lede">Specifications and handling notes for every compound in the catalog. Pricing is shown to registered researchers in the <a href="/#catalog">catalog</a>.</p><div class="grid" style="margin-top:1.5rem">{cards}</div>{cta()}</div></main>'''+foot())

def article(s,t,d,secs,section,dirp):
    path=f"/{dirp}/{s}" if dirp else f"/{s}"
    ld=crumbs_ld([("Home","/")]+([(section,f"/{dirp}")] if dirp else [])+[(t,path)])
    if dirp=="learn": ld+='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"Article","headline":t,"description":d,"dateModified":TODAY,"mainEntityOfPage":SITE+path,"author":{"@type":"Organization","name":"Nuvera Form"},"publisher":{"@type":"Organization","name":"Nuvera Form"}})+'</script>'
    crumb=f'<a href="/">Home</a> / '+(f'<a href="/{dirp}">{section}</a> / ' if dirp else '')+e(t)
    return head(f"{t} | Nuvera Form",d,path,ld)+top()+f'''<main id="main"><div class="wrap prose"><p class="crumbs">{crumb}</p><h1>{e(t)}</h1><p class="lede">{e(d)}</p>{"".join(f"<h2>{e(a)}</h2><p>{e(b)}</p>" for a,b in secs)}<div class="note"><strong>Research use only.</strong> {RUO}</div></div></main>'''+foot()
def article_html(s,t,d,secs,rel):
    path=f"/learn/{s}"
    ld=crumbs_ld([("Home","/"),("Learn","/learn"),(t,path)])+'<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"Article","headline":t,"description":d,"dateModified":TODAY,"mainEntityOfPage":SITE+path,"author":{"@type":"Organization","name":"Nuvera Form"},"publisher":{"@type":"Organization","name":"Nuvera Form"}})+'</script>'
    rc="".join(f'<div class="card"><h3>{e(NAMES[r])}</h3><a class="more" href="/compounds/{r}">View {e(NAMES[r])} →</a></div>' for r in rel)
    return head(f"{t} | Nuvera Form",d,path,ld)+top()+f'''<main id="main"><div class="wrap prose"><p class="crumbs"><a href="/">Home</a> / <a href="/learn">Learn</a> / {e(t)}</p><h1>{e(t)}</h1><p class="lede">{e(d)}</p>{"".join(f"<h2>{e(a)}</h2><p>{b}</p>" for a,b in secs)}<div class="note"><strong>Research use only.</strong> {RUO}</div><h2>Compounds mentioned</h2><div class="grid">{rc}</div></div></main>'''+foot()
for s,t,d,secs,rel in NEW_LEARN:
    write(f"/learn/{s}",article_html(s,t,d,secs,rel)); urls.append((f"/learn/{s}",0.7))
LEARN_ALL=LEARN+[(s,t,d,secs) for s,t,d,secs,_ in NEW_LEARN]
for s,t,d,secs in LEARN:
    write(f"/learn/{s}",article(s,t,d,secs,"Learn","learn")); urls.append((f"/learn/{s}",0.7))
lc="".join(f'<div class="card"><h3>{e(t)}</h3><p>{e(d)}</p><a class="more" href="/learn/{s}">Read the guide →</a></div>' for s,t,d,_ in LEARN_ALL)
write("/learn",head("Learn | Research Peptide Guides | Nuvera Form","Plain-English guides on research-use-only labelling, storing lyophilized peptides and reading a certificate of analysis.","/learn",crumbs_ld([("Home","/"),("Learn","/learn")]))+top()+f'<main id="main"><div class="wrap"><p class="crumbs"><a href="/">Home</a> / Learn</p><h1>Learn</h1><p class="lede">Practical, non-clinical guides for laboratory buyers.</p><div class="grid" style="margin-top:1.5rem">{lc}</div></div></main>'+foot())
for s,t,d,secs in LEGAL:
    write(f"/{s}",article(s,t,d,secs,"",""));urls.append((f"/{s}",0.3))


ABOUT_SECS=[
 ("Who we are","Nuvera Form is a small, Miami-based supplier of research peptides and reconstitution reagents, run by a two-person team. We started it to offer a short list of compounds presented clearly, with honest information and real people answering the phone."),
 ("What we sell","A focused catalog of research peptides, research blends and bacteriostatic water, each with its own <a href=\"/compounds\">specification page</a>. Every vial carries our own label showing the compound and quantity. Everything we sell is for laboratory research use only."),
 ("How we ship","Orders are packed in plain outer boxes and dispatched from the U.S. within 1–2 business days of payment. Ground shipping is a flat $25, free on orders of $250 or more after discounts, and overnight is a flat $60. We email tracking when your order leaves, and replace damaged or incorrect items reported within 72 hours. Full details are on our <a href=\"/shipping-returns\">shipping and returns</a> page."),
 ("Documentation","We publish analytical documentation batch by batch and do not claim results we cannot show. <a href=\"mailto:info@nuveraform.com?subject=Documentation%20request\">Email us</a> to ask what is available for your order."),
 ("How we sell","We sell only to buyers aged 21 or older who confirm research use, and we do not answer questions about dosing or use in people or animals. Read our <a href=\"/research-use-policy\">research use policy</a>."),
 ("Contact us","Email <a href=\"mailto:info@nuveraform.com\">info@nuveraform.com</a> or call <a href=\"tel:+13054573814\">305-457-3814</a> during regular business hours. Follow us on <a href=\"https://instagram.com/nuveraform\">Instagram</a>, <a href=\"https://tiktok.com/@nuveraform\">TikTok</a> and <a href=\"https://facebook.com/nuveraform\">Facebook</a> at @nuveraform."),
]
_ab_ld='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"AboutPage","url":SITE+"/about","mainEntity":{"@type":"Organization","name":"Nuvera Form","url":SITE+"/","logo":SITE+"/assets/nuvera-logo-hd-1024.png","email":"info@nuveraform.com","telephone":"+1-305-457-3814","address":{"@type":"PostalAddress","addressLocality":"Miami","addressRegion":"FL","addressCountry":"US"},"sameAs":["https://instagram.com/nuveraform","https://tiktok.com/@nuveraform","https://facebook.com/nuveraform"]}})+'</script>'+crumbs_ld([("Home","/"),("About",'/about')])
write("/about",head("About Nuvera Form | Miami Research Peptide Supplier","Nuvera Form is a small Miami-based supplier of research peptides and reagents. Who we are, how we ship and how to reach us.","/about",_ab_ld)+top()+f'''<main id="main"><div class="wrap prose"><p class="crumbs"><a href="/">Home</a> / About</p><h1>About Nuvera Form</h1><p class="lede">A small Miami-based supplier of research peptides, with clear information and real people on support.</p>{"".join(f"<h2>{e(a)}</h2><p>{b}</p>" for a,b in ABOUT_SECS)}<div class="note"><strong>Research use only.</strong> {RUO}</div>{cta()}</div></main>'''+foot()); urls.append(("/about",0.5))

_rv_js="""
(function(){var f=document.getElementById('rf'),msg=document.getElementById('rmsg'),step2=document.getElementById('step2'),q=new URLSearchParams(location.search);
if(q.get('o'))f.order.value=q.get('o');
function show(t,ok){msg.textContent=t;msg.style.color=ok?'#2e6b3a':'#a33';}
function post(d){return fetch('/api/review',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)}).then(function(r){return r.json().then(function(j){return {ok:r.ok,j:j}})})}
document.getElementById('find').onclick=function(){show('',1);post({order:f.order.value,email:f.email.value,lookup:true}).then(function(x){if(!x.ok)return show(x.j.error||'Something went wrong.');
f.product.innerHTML=x.j.products.map(function(p){return '<option value="'+p.id+'">'+p.name+'</option>'}).join('');step2.hidden=false;f.order.readOnly=f.email.readOnly=true;}).catch(function(){show('Something went wrong. Try again.')})};
f.onsubmit=function(e){e.preventDefault();var r=f.querySelector('input[name=rating]:checked');if(!r)return show('Choose a star rating.');
var b=f.querySelector('button[type=submit]');b.disabled=true;post({order:f.order.value,email:f.email.value,product:f.product.value,rating:+r.value,name:f.name.value,text:f.text.value,website:f.website.value}).then(function(x){b.disabled=false;
if(!x.ok)return show(x.j.error||'Something went wrong.');f.hidden=true;show('Thank you! Your review was received and will appear once it is checked.',1);}).catch(function(){b.disabled=false;show('Something went wrong. Try again.')})};})();
"""
_inp='style="padding:.6rem .8rem;border:1px solid var(--line);border-radius:12px;width:100%;max-width:26rem;font:inherit;background:#fff"'
_stars="".join(f'<label style="margin-right:.6rem;cursor:pointer"><input type="radio" name="rating" value="{i}"> {"★"*i}</label>' for i in range(5,0,-1))
write("/review",head("Leave a Review | Nuvera Form","Leave a verified review of your Nuvera Form order.","/review").replace('index,follow','noindex')+top()+f'''<main id="main"><div class="wrap prose"><h1>Leave a verified review</h1><p class="lede">Reviews are open to customers only. Enter your order number and the email you ordered with.</p>
<form id="rf" novalidate><input name="website" style="display:none" tabindex="-1" autocomplete="off">
<p><label>Order number<br><input name="order" required placeholder="NF-261103-ABCD" {_inp}></label></p>
<p><label>Email used for the order<br><input name="email" type="email" required {_inp}></label></p>
<p><button type="button" id="find" class="btn">Find my order</button></p>
<div id="step2" hidden>
<p><label>Product<br><select name="product" {_inp}></select></label></p>
<p>Rating<br>{_stars}</p>
<p><label>Your review<br><textarea name="text" rows="5" maxlength="1200" {_inp}></textarea></label></p>
<p><label>Name to show (optional)<br><input name="name" maxlength="40" placeholder="e.g. Kelly G." {_inp}></label></p>
<div class="note">Tell us about the order: shipping speed, packaging, labelling and service. Reviews that describe effects, dosing or use in people or animals cannot be published.</div>
<p><button type="submit" class="btn">Submit review</button></p></div></form>
<p id="rmsg" role="status" style="font-weight:600"></p></div></main><script>{_rv_js}</script>'''+foot())
write("/404",head("Page not found | Nuvera Form","The page you are looking for could not be found.","/404").replace('index,follow','noindex')+top()+'<main id="main"><div class="wrap prose"><h1>Page not found</h1><p class="lede">That page does not exist or has moved.</p><p><a class="btn" href="/">Back to the home page</a> <a class="btn ghost" href="/compounds">Browse compounds</a></p></div></main>'+foot())
os.rename("404.html","404.html") if os.path.exists("404.html") else None

sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f'<url><loc>{SITE}{p if p!="/" else "/"}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n' for p,pr in urls)+'</urlset>\n'
open("sitemap.xml","w").write(sm)
print(len(urls),"urls")
