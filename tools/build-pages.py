#!/usr/bin/env python3
"""Generates static SEO pages (compounds, learn, legal, 404) and sitemap.xml. Run: python3 tools/build-pages.py"""
import os, json, html
from datetime import date
SITE="https://nuveraform.com"; TODAY=date.today().isoformat()
RUO="For laboratory research use only. Not for human or veterinary use. Not a drug, food, supplement or cosmetic."

COMPOUNDS=[
("retatrutide","Retatrutide","Research peptide","A long-chain synthetic peptide described in the scientific literature as acting on more than one receptor.",
 [("Class","Synthetic peptide"),("Format","Lyophilized powder, sealed vial"),("Sizes listed","5 mg, 10 mg, 15 mg"),("Typical lab use","Receptor-binding and in-vitro signalling assays")],
 "Retatrutide is a synthetic peptide that the literature describes as acting on more than one receptor. In laboratory work it is a reference material for receptor-signalling assays. This page covers the physical product only."),
("bpc-157","BPC-157","Research peptide","A synthetic pentadecapeptide (15 amino acids) whose sequence is derived from a protein fragment found in gastric juice.",
 [("Class","Synthetic peptide, 15 residues"),("Format","Lyophilized powder, sealed vial"),("Offered as","BPC-157 / TB-500 blend (10 mg) and the Research Duo bundle"),("Typical lab use","Cell-culture research")],
 "BPC-157 is a short synthetic peptide frequently referenced in preclinical literature. Nuvera Form lists it combined with TB-500 as a research blend. Product pages here describe the material, not any effect on people or animals."),
("tb-500","TB-500","Research peptide","A synthetic peptide related to a fragment of thymosin beta-4, supplied for laboratory investigation.",
 [("Class","Synthetic peptide"),("Format","Lyophilized powder, sealed vial"),("Offered as","BPC-157 / TB-500 blend, 10 mg"),("Typical lab use","Cell-biology assays")],
 "TB-500 is named in the literature as a synthetic fragment connected to thymosin beta-4, a protein studied in cell biology. It is sold here in blend form for in-vitro research."),
("ghk-cu","GHK-Cu","Research peptide","A naturally occurring tripeptide (glycine-histidine-lysine) that binds copper(II), supplied as a lyophilized copper complex.",
 [("Class","Tripeptide–copper complex"),("Format","Lyophilized powder, sealed vial"),("Size listed","100 mg"),("Typical lab use","Cell-culture research")],
 "GHK is a three-residue peptide with a strong affinity for copper ions. The copper complex is used as a reference material in laboratory studies of cell biology."),
("thymosin-alpha-1","Thymosin Alpha 1","Research peptide","A 28-amino-acid peptide originally characterized from thymus tissue extracts, produced synthetically for research.",
 [("Class","Synthetic peptide, 28 residues"),("Format","Lyophilized powder, sealed vial"),("Size listed","10 mg"),("Typical lab use","Cell-assay research")],
 "Thymosin alpha 1 is used in laboratories as a reference peptide in cell-signalling work. Nuvera Form supplies it only as a research reagent."),
("nad-plus","NAD+","Research reagent","Nicotinamide adenine dinucleotide, a coenzyme found in all living cells and widely used in biochemical assays.",
 [("Class","Dinucleotide coenzyme"),("Format","Lyophilized powder, sealed vial"),("Size listed","500 mg"),("Typical lab use","Enzyme kinetics and cell-metabolism assays")],
 "NAD+ participates in redox reactions and is a common substrate in enzyme assays. As a research reagent it is used in biochemistry and cell-biology workflows."),
("cjc-1295-ipamorelin","CJC-1295 / Ipamorelin","Research blend","A combination of two synthetic peptides: a GHRH-analog sequence and a five-residue growth hormone secretagogue peptide (ipamorelin).",
 [("Class","Two-peptide research blend"),("Format","Lyophilized powder, sealed vial"),("Size listed","10 mg"),("Typical lab use","Receptor-signalling assays")],
 "This blend pairs two synthetic sequences commonly discussed in endocrine-receptor research. It is supplied as a lyophilized blend for in-vitro work."),
("mots-c","MOTS-c","Research peptide","A 16-amino-acid peptide encoded in mitochondrial DNA, studied as a mitochondria-derived signalling peptide.",
 [("Class","Synthetic peptide, 16 residues"),("Format","Lyophilized powder, sealed vial"),("Size listed","10 mg"),("Typical lab use","Mitochondrial and cell-metabolism research")],
 "MOTS-c is notable because it is encoded by mitochondrial rather than nuclear DNA. Laboratories use the synthetic form in cell-based metabolic studies."),
("klow-blend","KLOW Blend","Research blend","A multi-component research blend supplied as a lyophilized powder.",
 [("Class","Research blend"),("Format","Lyophilized powder, sealed vial"),("Size listed","80 mg"),("Composition","Shown on the vial label; email us to confirm before ordering")],
 "KLOW is a blended research product. Email info@nuveraform.com to confirm the exact composition of the lot you are ordering."),
("kisspeptin","Kisspeptin","Research peptide","A peptide product of the KISS1 gene, studied in neuroendocrine research; the short active fragment is kisspeptin-10.",
 [("Class","Synthetic peptide"),("Format","Lyophilized powder, sealed vial"),("Size listed","10 mg"),("Typical lab use","Receptor-binding and signalling assays")],
 "Kisspeptins signal through the KISS1 receptor and appear in neuroendocrine literature. Nuvera Form supplies kisspeptin strictly for in-vitro research."),
("bacteriostatic-water","Bacteriostatic Water","Reconstitution reagent","Sterile water containing 0.9% benzyl alcohol as a bacteriostatic preservative, used as a laboratory diluent.",
 [("Class","Sterile diluent"),("Format","Multi-dose vial"),("Size listed","10 ml"),("Typical lab use","Reconstituting lyophilized research material")],
 "Bacteriostatic water is sterile water with a small amount of benzyl alcohol that inhibits bacterial growth in a multi-use vial. Laboratories use it as a diluent according to their written protocols."),
]

PRICES={"retatrutide":(115,240,3),"bpc-157":(110,110,1),"tb-500":(110,110,1),"ghk-cu":(85,85,1),"thymosin-alpha-1":(95,95,1),"nad-plus":(90,90,1),"cjc-1295-ipamorelin":(105,105,1),"mots-c":(95,95,1),"klow-blend":(120,120,1),"kisspeptin":(85,85,1),"bacteriostatic-water":(15,15,1)}
CATS=[("incretin-peptides","Incretin-family peptides","Research peptides studied for incretin-family receptor signalling.",["retatrutide"]),
("peptide-blends","Peptide blends","Pre-combined lyophilized research blends supplied in a single vial.",["bpc-157","tb-500","cjc-1295-ipamorelin","klow-blend"]),
("single-peptides","Single peptides and reagents","Individual peptides and coenzymes supplied as lyophilized powder.",["ghk-cu","thymosin-alpha-1","nad-plus","mots-c","kisspeptin"]),
("reconstitution","Reconstitution reagents","Sterile diluents used to reconstitute lyophilized research material.",["bacteriostatic-water"])]
CAT_OF={c:slug for slug,_,_,cs in CATS for c in cs}
CNAME={m[0]:m[1] for m in COMPOUNDS}
GUIDE_LINKS={"storing-lyophilized-peptides":"Storing lyophilized peptides","how-to-read-a-certificate-of-analysis":"How to read a certificate of analysis","reconstitution-for-lab-work":"Reconstitution for lab work","bacteriostatic-vs-sterile-water":"Bacteriostatic vs sterile water","peptide-research-glossary":"Peptide research glossary","what-research-use-only-means":"What research use only means"}
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
("reconstitution-for-lab-work","Reconstitution for lab work","How laboratories reconstitute lyophilized material: choosing a diluent, aseptic technique and working out concentration.",
 [("Start with the written protocol","Reconstitution should follow your institution’s written protocol and the documentation for the lot. This guide describes general laboratory practice for in-vitro work only. It does not describe use in people or animals."),
  ("Choosing a diluent","Common laboratory diluents include sterile water and bacteriostatic water. The right choice depends on the assay: a preservative such as benzyl alcohol can interfere with some cell-based work. See the comparison guide on bacteriostatic and sterile water."),
  ("Aseptic technique","Let the vial reach room temperature, wipe the stopper with alcohol, use sterile transfer equipment, and add diluent slowly down the vial wall so the powder dissolves without foaming. Swirl gently rather than shaking."),
  ("Working out concentration","Concentration is mass divided by volume. A vial containing 10 mg reconstituted in 2 mL gives 5 mg/mL. Record the date, diluent and final concentration on the label."),
  ("After reconstitution","Reconstituted material is generally less stable than powder. Store it as your protocol directs and discard it by the date you set.")]),
("bacteriostatic-vs-sterile-water","Bacteriostatic water vs sterile water","What the two diluents contain, how they differ and how to choose between them for laboratory work.",
 [("What they are","Sterile water is water with no preservative. Bacteriostatic water is sterile water with 0.9% benzyl alcohol added to inhibit bacterial growth."),
  ("Single use vs multi-use","Sterile water has no preservative, so a vial is generally treated as single use once opened. The benzyl alcohol in bacteriostatic water is what makes a multi-dose vial practical for repeated laboratory access."),
  ("Assay compatibility","Benzyl alcohol can affect some sensitive cell-based assays and certain analytical methods. If your assay is sensitive to preservatives, confirm the diluent in your protocol before use."),
  ("Our listing","Nuvera Form lists Bacteriostatic Water in a 10 ml vial. See the compound page for specifications.")]),
("peptide-research-glossary","Peptide research glossary","Plain-English definitions of terms used on peptide documentation and product pages.",
 [("Lyophilized","Freeze-dried. Water is removed under vacuum at low temperature, leaving a stable powder."),
  ("Reconstitution","Dissolving lyophilized powder in a liquid diluent to make a solution."),
  ("HPLC","High-performance liquid chromatography. A method that separates the components of a sample so purity can be measured."),
  ("Mass spectrometry (MS)","A method that measures molecular mass, used to confirm that the main component is the expected molecule."),
  ("Certificate of analysis (COA)","A document reporting the tests run on a specific batch and their results."),
  ("Lot or batch number","The identifier for a single production run. Documentation should match the lot on your vial."),
  ("Residue","One amino acid unit within a peptide chain. A 15-residue peptide has 15 amino acids."),
  ("Bacteriostatic","Inhibits bacterial growth without necessarily killing bacteria. Bacteriostatic water contains benzyl alcohol for this purpose."),
  ("Research use only (RUO)","A label meaning the product is for laboratory investigation and not for diagnostic, therapeutic or any use in people or animals.")]),
("how-to-read-a-certificate-of-analysis","How to read a certificate of analysis","What HPLC purity and mass spectrometry results mean, and what to check on any supplier’s paperwork.",
 [("HPLC purity","High-performance liquid chromatography separates a sample into components. The main peak’s share of the total area is reported as purity. A figure on its own says nothing without the method and the batch it came from."),
  ("Mass spectrometry","Mass spectrometry confirms the molecular mass of the main component, which helps verify identity. The measured mass should match the expected mass within the instrument’s tolerance."),
  ("What to check","Batch or lot number, date, the laboratory that ran the test, and whether the document matches the batch on your vial."),
  ("Our approach","Documentation availability varies by batch. We do not claim test results we cannot show. Email info@nuveraform.com to ask what is available for your order.")]),
]

LEGAL=[
("privacy","Privacy Policy","How Nuvera Form collects, uses and protects the information you give us.",
 [("What we collect","Name, email address, phone number and field of research when you create an account; the email you give for newsletters or documentation requests; and the order details you submit (name, shipping address, phone and items). Zelle payments are made through your own bank; we never collect or store bank or card details on this site."),
  ("How we use it","To create your account, apply your welcome discount, reply to requests, send order updates and, if you opt in, product announcements."),
  ("Who processes it","Form submissions are handled by Web3Forms; email, including your subscriber record, is handled through Resend; the site is hosted on Vercel. These providers process data only to deliver their service."),
  ("Your choices","Email info@nuveraform.com to access, correct or delete your data, or to unsubscribe. We do not sell personal information."),
  ("Cookies and storage","The site stores your age confirmation, cart and sign-in state in your browser’s local storage. It does not use advertising cookies.")]),
("terms","Terms of Sale","The conditions that apply when you buy from Nuvera Form.",
 [("Eligibility","Buyers must be 21 or older and purchase solely for laboratory research."),
  ("Research use only",RUO+" You are responsible for lawful handling, storage and disposal."),
  ("Pricing and stock","Prices and availability may change without notice. We may cancel an order if an item is unavailable or a price is shown in error, and will refund any payment taken."),
  ("Payment and discount code","Orders are currently paid by Zelle after you place them, and ship once payment is confirmed. The NUVERA20 code takes 20% off the first order placed with a new account and can be used once."),
  ("Replacements","Report a damaged or incorrect item within 72 hours of delivery at info@nuveraform.com and we will replace it."),
  ("Liability","To the extent permitted by law, Nuvera Form is not liable for misuse of products or for losses arising from use outside these terms.")]),
("shipping-returns","Shipping & Returns","Dispatch times, delivery, costs and what to do if something is wrong.",
 [("Dispatch","Orders typically dispatch within 1–2 business days of payment."),
  ("Delivery","Domestic delivery is typically 3–5 business days after dispatch. A tracking link is emailed when your order leaves."),
  ("Payment","We currently accept payment by Zelle to (305) 457-3814. Place your order on the site, then send the total with your order number in the memo. Orders ship after payment is confirmed. Card payments may be added later."),
  ("Cost","Orders of $200 or more after discounts ship free. Smaller orders ship at a flat $15."),
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
<link rel="canonical" href="{url}"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website"><meta property="og:site_name" content="Nuvera Form"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/og.png"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{SITE}/og.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">{extra}</head>'''
def crumbs_ld(items):
    return '<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":SITE+p} for i,(n,p) in enumerate(items)]})+'</script>'
def top():
    return '''<body><a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap bar"><a class="logo" href="/"><span class="dot"></span><span class="t">Nuvera Form</span></a>
<nav class="m" aria-label="Main"><a href="/#catalog">Catalog</a><a href="/compounds">Compounds</a><a href="/categories">Categories</a><a href="/learn">Learn</a><a href="/#faq">FAQ</a></nav></div></header>'''
NEWS='''<section class="nl" aria-label="Newsletter"><div class="wrap"><h2>Lot drops and restock alerts</h2><p>Occasional emails when new compounds or documentation are published. By subscribing you agree to receive them; unsubscribe any time.</p>
<form id="nl" class="nlf"><input type="email" name="email" placeholder="Email address" required aria-label="Email address"><input type="checkbox" name="botcheck" style="display:none" tabindex="-1" aria-hidden="true"><button class="btn">Subscribe</button></form><p id="nlm" role="status"></p></div></section>
<script src="/assets/site-config.js"></script><script src="/assets/forms.js"></script>'''
def foot():
    return NEWS+f'''<footer class="f"><div class="wrap"><div class="fg">
<div><p class="fh">Nuvera Form</p><p>Research peptides and reconstitution reagents for qualified laboratories.</p></div>
<div><p class="fh">Compounds</p><ul>{"".join(f'<li><a href="/compounds/{s}">{e(n)}</a></li>' for s,n,*_ in COMPOUNDS[:6])}<li><a href="/compounds">All compounds</a></li></ul></div>
<div><p class="fh">Categories</p><ul>{"".join(f'<li><a href="/categories/{s}">{e(n)}</a></li>' for s,n,*_ in CATS)}</ul></div>
<div><p class="fh">Learn</p><ul>{"".join(f'<li><a href="/learn/{s}">{e(t)}</a></li>' for s,t,*_ in LEARN)}</ul></div>
<div><p class="fh">Company</p><ul><li><a href="/shipping-returns">Shipping &amp; Returns</a></li><li><a href="/privacy">Privacy Policy</a></li><li><a href="/terms">Terms of Sale</a></li><li><a href="/research-use-policy">Research Use Policy</a></li><li><a href="/reviews">Customer reviews</a></li><li><a href="/contact">Contact us</a></li><li><a href="mailto:info@nuveraform.com">info@nuveraform.com</a></li><li><a href="tel:+13054573814">(305) 457-3814</a></li></ul></div>
</div><div class="legal"><p><strong>{RUO}</strong></p><p>Copyright © 2026 Nuvera Form. All rights reserved.</p></div></div></footer></body></html>'''
def write(path,content):
    fp=path.lstrip("/")+".html"
    os.makedirs(os.path.dirname(fp) or ".",exist_ok=True)
    open(fp,"w").write(content)
def vial(n):
    return f'<svg class="vial" width="96" height="144" viewBox="0 0 80 120" role="img" aria-label="Vial of {e(n)}, lyophilized research material"><rect x="26" y="6" width="28" height="16" rx="3" fill="#BF943C"/><rect x="30" y="22" width="20" height="8" fill="#e9dcc0"/><rect x="18" y="30" width="44" height="82" rx="10" fill="#fbf6ea" stroke="#BF943C" stroke-width="2"/><rect x="18" y="52" width="44" height="42" fill="#F0E4CE"/><text x="40" y="68" text-anchor="middle" font-size="6.5" font-weight="700" fill="#3A2816" font-family="Poppins,sans-serif">NUVERA FORM</text><text x="40" y="83" text-anchor="middle" font-size="7" font-weight="700" fill="#B87A6C" font-family="Poppins,sans-serif">{e(n[:14])}</text></svg>'
def fromp(s_):
    lo,hi,n=PRICES[s_]
    return f"${lo}" if lo==hi else f"${lo} – ${hi}"
def cta():
    return '<p style="margin-top:2rem"><a class="btn" href="/#catalog">Buy in the catalog</a> <a class="btn ghost" href="/categories">Browse categories</a></p>'
urls=[("/",1.0),("/compounds",0.9),("/learn",0.7)]

for s,n,kind,tag,specs,body in COMPOUNDS:
    path=f"/compounds/{s}"
    title=f"{n} | Research Peptide Specifications | Nuvera Form"
    desc=f"{n} specifications: format, sizes and handling notes. {RUO.split('.')[0]}. Dispatch from the U.S. in 1–2 business days."
    others=[m for m in COMPOUNDS if m[0]!=s][:3]
    rel="".join(f'<div class="card"><h3>{e(m[1])}</h3><p>{e(m[3])}</p><a class="more" href="{"/compounds/"+m[0]}">View specifications →</a></div>' for m in others)
    lo,hi,cnt=PRICES[s]
    offer={"@type":"Offer","price":str(lo),"priceCurrency":"USD","availability":"https://schema.org/InStock","url":SITE+path,"seller":{"@type":"Organization","name":"Nuvera Form"}} if cnt==1 else {"@type":"AggregateOffer","lowPrice":str(lo),"highPrice":str(hi),"offerCount":cnt,"priceCurrency":"USD","availability":"https://schema.org/InStock","url":SITE+path}
    ld='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"Product","name":n,"description":tag,"image":SITE+"/og.png","brand":{"@type":"Brand","name":"Nuvera Form"},"category":CATS[[c[0] for c in CATS].index(CAT_OF[s])][1],"url":SITE+path,"offers":offer})+'</script>'+crumbs_ld([("Home","/"),("Compounds","/compounds"),(n,path)])
    pricerow=f"<p class='price'>From {fromp(s)}</p>" if s not in ("bpc-157","tb-500") else "<p class='price'>From $110 <span style='font-size:.85rem;font-weight:500;color:var(--brown)'>(sold in the BPC-157 / TB-500 blend, 10 mg)</span></p>"
    catslug=CAT_OF[s]; catname=CATS[[c[0] for c in CATS].index(catslug)][1]
    gl=["storing-lyophilized-peptides","how-to-read-a-certificate-of-analysis"]+(["reconstitution-for-lab-work","bacteriostatic-vs-sterile-water"] if s=="bacteriostatic-water" else ["reconstitution-for-lab-work"])
    relhtml='<div class="rel">'+f'<a href="/categories/{catslug}">{e(catname)}</a>'+"".join(f'<a href="/learn/{g}">{e(GUIDE_LINKS[g])}</a>' for g in gl)+'<a href="/learn/peptide-research-glossary">Glossary</a></div>'
    page=head(title,desc,path,ld)+top()+f'''<main id="main"><div class="wrap prose">
<p class="crumbs"><a href="/">Home</a> / <a href="/compounds">Compounds</a> / {e(n)}</p>
{vial(n)}<span class="badge">{e(kind)} · Research use only · 21+</span><h1>{e(n)}</h1><p class="lede">{e(tag)}</p>{pricerow}
<h2>Specifications</h2><table>{"".join(f"<tr><th>{e(a)}</th><td>{e(b)}</td></tr>" for a,b in specs)}</table>
<h2>About this material</h2><p>{e(body)}</p>
<h2>Handling</h2><p>Store lyophilized vials sealed, dry, cold and away from light, and follow your institution’s written protocol. See <a href="/learn/storing-lyophilized-peptides">storing lyophilized peptides</a>.</p><h2>Related</h2>{relhtml}
<h2>Documentation</h2><p>Documentation availability varies by batch. <a href="mailto:info@nuveraform.com?subject=Documentation%20request%3A%20{e(n)}">Email us</a> to ask what is available for your order.</p>
<div class="note"><strong>Research use only.</strong> {RUO} Nothing on this page is a statement about effects, dosing or use in people or animals.</div><p style="margin-top:1.5rem;font-size:.9rem">Checkout requires a free account with a 21+ and research-use confirmation. New accounts get 20% off a first order with code NUVERA20.</p>{cta()}
<h2>Other compounds</h2><div class="grid">{rel}</div></div></main>'''+foot()
    write(path,page); urls.append((path,0.8))

cards="".join(f'<div class="card"><span class="badge">{e(k)}</span><h2 style="margin-top:.6rem">{e(n)}</h2><p class="price" style="font-size:1.1rem">From {fromp(s) if s not in ("bpc-157","tb-500") else "$110"}</p><p>{e(t)}</p><a class="more" href="/compounds/{s}">View specifications →</a></div>' for s,n,k,t,*_ in COMPOUNDS)
write("/compounds",head("Research Compounds | Nuvera Form","Browse Nuvera Form’s research peptides and reconstitution reagents with format, size and handling notes. Research use only, 21+.","/compounds",crumbs_ld([("Home","/"),("Compounds","/compounds")]))+top()+f'''<main id="main"><div class="wrap"><p class="crumbs"><a href="/">Home</a> / Compounds</p><h1>Research compounds</h1><p class="lede">Specifications and handling notes for every compound in the catalog. Prices are listed in the <a href="/#catalog">catalog</a>.</p><div class="grid" style="margin-top:1.5rem">{cards}</div>{cta()}</div></main>'''+foot())

def article(s,t,d,secs,section,dirp,rel=""):
    path=f"/{dirp}/{s}" if dirp else f"/{s}"
    ld=crumbs_ld([("Home","/")]+([(section,f"/{dirp}")] if dirp else [])+[(t,path)])
    if dirp=="learn": ld+='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"Article","headline":t,"description":d,"dateModified":TODAY,"mainEntityOfPage":SITE+path,"author":{"@type":"Organization","name":"Nuvera Form"},"publisher":{"@type":"Organization","name":"Nuvera Form"}})+'</script>'
    crumb=f'<a href="/">Home</a> / '+(f'<a href="/{dirp}">{section}</a> / ' if dirp else '')+e(t)
    return head(f"{t} | Nuvera Form",d,path,ld)+top()+f'''<main id="main"><div class="wrap prose"><p class="crumbs">{crumb}</p><h1>{e(t)}</h1><p class="lede">{e(d)}</p>{"".join(f"<h2>{e(a)}</h2><p>{e(b)}</p>" for a,b in secs)}{rel}<div class="note"><strong>Research use only.</strong> {RUO}</div></div></main>'''+foot()
for s,t,d,secs in LEARN:
    others=[g for g in GUIDE_LINKS if g!=s and g!="what-research-use-only-means"][:3]
    rel='<h2>Related</h2><div class="rel">'+"".join(f'<a href="/learn/{g}">{e(GUIDE_LINKS[g])}</a>' for g in others)+'<a href="/compounds">All compounds</a><a href="/categories">Categories</a></div>'
    write(f"/learn/{s}",article(s,t,d,secs,"Learn","learn",rel)); urls.append((f"/learn/{s}",0.7))
lc="".join(f'<div class="card"><h2>{e(t)}</h2><p>{e(d)}</p><a class="more" href="/learn/{s}">Read the guide →</a></div>' for s,t,d,_ in LEARN)
write("/learn",head("Learn | Research Peptide Guides | Nuvera Form","Plain-English guides on research-use-only labelling, storing lyophilized peptides and reading a certificate of analysis.","/learn",crumbs_ld([("Home","/"),("Learn","/learn")]))+top()+f'<main id="main"><div class="wrap"><p class="crumbs"><a href="/">Home</a> / Learn</p><h1>Learn</h1><p class="lede">Practical, non-clinical guides for laboratory buyers.</p><div class="grid" style="margin-top:1.5rem">{lc}</div></div></main>'+foot())
for s,t,d,secs in LEGAL:
    write(f"/{s}",article(s,t,d,secs,"",""));urls.append((f"/{s}",0.3))

for slug,cn,cd,cs in CATS:
    path=f"/categories/{slug}"
    items="".join(f'<div class="card"><h2>{e(CNAME[c])}</h2><p class="price" style="font-size:1.1rem">From {fromp(c) if c not in ("bpc-157","tb-500") else "$110"}</p><p>{e([m[3] for m in COMPOUNDS if m[0]==c][0])}</p><a class="more" href="/compounds/{c}">View specifications →</a></div>' for c in cs)
    ld=crumbs_ld([("Home","/"),("Categories","/categories"),(cn,path)])+'<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"ItemList","name":cn,"itemListElement":[{"@type":"ListItem","position":i+1,"url":f"{SITE}/compounds/{c}","name":CNAME[c]} for i,c in enumerate(cs)]})+'</script>'
    write(path,head(f"{cn} for Research | Nuvera Form",f"{cd} Prices, formats and handling notes. Research use only, 21+.",path,ld)+top()+f'<main id="main"><div class="wrap"><p class="crumbs"><a href="/">Home</a> / <a href="/categories">Categories</a> / {e(cn)}</p><h1>{e(cn)}</h1><p class="lede">{e(cd)}</p><div class="grid" style="margin-top:1.5rem">{items}</div><h2>Related guides</h2><div class="rel"><a href="/learn/reconstitution-for-lab-work">Reconstitution for lab work</a><a href="/learn/storing-lyophilized-peptides">Storing lyophilized peptides</a><a href="/learn/how-to-read-a-certificate-of-analysis">Reading a certificate of analysis</a></div>{cta()}</div></main>'+foot())
    urls.append((path,0.8))
cc="".join(f'<div class="card"><h2>{e(cn)}</h2><p>{e(cd)}</p><a class="more" href="/categories/{slug}">View category →</a></div>' for slug,cn,cd,_ in CATS)
write("/categories",head("Research Peptide Categories | Nuvera Form","Browse Nuvera Form by category: incretin-family peptides, blends, single peptides and reconstitution reagents. Research use only, 21+.","/categories",crumbs_ld([("Home","/"),("Categories","/categories")]))+top()+f'<main id="main"><div class="wrap"><p class="crumbs"><a href="/">Home</a> / Categories</p><h1>Categories</h1><div class="grid" style="margin-top:1.5rem">{cc}</div></div></main>'+foot())
urls.append(("/categories",0.9))
write("/contact",head("Contact Nuvera Form | Phone, Email and Hours","Reach Nuvera Form by phone at (305) 457-3814 or email info@nuveraform.com, Monday to Friday, 9 AM to 5 PM ET.","/contact",crumbs_ld([("Home","/"),("Contact","/contact")])+'<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"ContactPage","name":"Contact Nuvera Form","url":SITE+"/contact","mainEntity":{"@type":"Organization","name":"Nuvera Form","telephone":"+1-305-457-3814","email":"info@nuveraform.com"}})+'</script>')+top()+f'''<main id="main"><div class="wrap prose"><p class="crumbs"><a href="/">Home</a> / Contact</p><h1>Contact us</h1><p class="lede">Questions about an order, documentation or bulk pricing? We answer during regular office hours.</p>
<table><tr><th>Phone</th><td><a href="tel:+13054573814">(305) 457-3814</a></td></tr><tr><th>Email</th><td><a href="mailto:info@nuveraform.com">info@nuveraform.com</a></td></tr><tr><th>Hours</th><td>Monday to Friday, 9 AM to 5 PM ET</td></tr><tr><th>Social</th><td><a href="https://instagram.com/nuveraform" rel="noopener">Instagram</a> · <a href="https://tiktok.com/@nuveraform" rel="noopener">TikTok</a> · <a href="https://facebook.com/nuveraform" rel="noopener">Facebook</a></td></tr></table>
<h2>Paying for an order</h2><p>We currently accept Zelle. After you place an order, send the total to (305) 457-3814 and put your order number in the memo. See <a href="/shipping-returns">Shipping &amp; Returns</a>.</p>
<div class="note"><strong>Research use only.</strong> {RUO} We cannot answer questions about dosing, injection or use in people or animals.</div></div></main>'''+foot())
urls.append(("/contact",0.6))
REVIEWS=[r for r in json.load(open("data/reviews.json")) if r.get("approved")]
def stars(n): return "★"*n+"☆"*(5-n)
rlist="".join(f'<div class="card"><p class="price" style="font-size:1.1rem;letter-spacing:2px" aria-label="{r["rating"]} out of 5">{stars(r["rating"])}</p><p>{e(r["text"])}</p><p style="font-size:.85rem"><strong>{e(r["name"])}</strong> · {e(r["aspect"])} · {e(r["date"])}'+(' · <span class="badge">Verified purchase</span>' if r.get("verified") else '')+'</p></div>' for r in REVIEWS) or '<div class="card"><p>No reviews yet. Be the first to tell us how your order went.</p></div>'
OPTS="".join(f"<option>{o}</option>" for o in ["Shipping speed","Packaging","Communication","Order accuracy","Website experience"])
write("/reviews",head("Customer Reviews | Nuvera Form","Service reviews from verified Nuvera Form customers: shipping speed, packaging, communication, order accuracy and website experience.","/reviews",crumbs_ld([("Home","/"),("Reviews","/reviews")]))+top()+f'''<main id="main"><div class="wrap prose"><p class="crumbs"><a href="/">Home</a> / Reviews</p><h1>Customer reviews</h1><p class="lede">Feedback on our service. Every review is checked against a real order before it is published.</p>
<div class="grid" style="margin-top:1.5rem">{rlist}</div>
<h2>Leave a service review</h2>
<p>Tell us about shipping speed, packaging, communication, order accuracy or the website. Please do not describe any effect of a product: these are research materials and we cannot publish reviews about results, use or outcomes. We publish only reviews we can match to an order and may edit or decline others.</p>
<form id="rv" class="card" style="display:grid;gap:.8rem"><input class="nlf-in" name="name" placeholder="First name and last initial" required maxlength="60" aria-label="Name"><input class="nlf-in" type="email" name="email" placeholder="Email used on your order" required aria-label="Email"><input class="nlf-in" name="order_number" placeholder="Order number (NF-...)" required pattern="NF-[0-9]{{6}}-[A-Za-z0-9]{{4}}" aria-label="Order number">
<select class="nlf-in" name="aspect" required aria-label="What is your review about"><option value="">What is your review about?</option>{OPTS}</select>
<select class="nlf-in" name="rating" required aria-label="Rating"><option value="">Rating</option><option value="5">5 – Excellent</option><option value="4">4 – Good</option><option value="3">3 – Okay</option><option value="2">2 – Poor</option><option value="1">1 – Very poor</option></select>
<textarea class="nlf-in" name="text" rows="4" maxlength="600" required placeholder="Your review (service only, max 600 characters)" aria-label="Review"></textarea>
<label style="font-size:.85rem"><input type="checkbox" name="agree" value="yes" required> My review is about the service, not any effect of a product, and I agree it may be published with my name.</label>
<button class="btn" style="border:0;cursor:pointer;font:inherit;font-weight:600">Submit review</button><p id="rvm" role="status"></p></form>
</div></main>'''+foot())
urls.append(("/reviews",0.5))
write("/404",head("Page not found | Nuvera Form","The page you are looking for could not be found.","/404").replace('index,follow','noindex').replace('<link rel="canonical" href="https://nuveraform.com/404">','')+top()+'<main id="main"><div class="wrap prose"><h1>Page not found</h1><p class="lede">That page does not exist or has moved.</p><p><a class="btn" href="/">Back to the home page</a> <a class="btn ghost" href="/compounds">Browse compounds</a></p></div></main>'+foot())

sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f'<url><loc>{SITE}{p if p!="/" else "/"}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n' for p,pr in urls)+'</urlset>\n'
open("sitemap.xml","w").write(sm)
print(len(urls),"urls")
