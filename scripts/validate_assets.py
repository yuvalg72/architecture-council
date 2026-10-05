#!/usr/bin/env python3
"""Validate local user-facing visual assets against GHR-13.

Designed to be copied into a governed repository as scripts/validate_assets.py.
Dependencies: Pillow and CairoSVG.
"""
from __future__ import annotations
import argparse,io,json,math,re,sys
from pathlib import Path
from PIL import Image, ImageChops, ImageStat
import cairosvg

IMAGE_EXTENSIONS={".png",".jpg",".jpeg",".svg",".gif",".webp"}
PROHIBITED_PUBLISHED_EXTENSIONS={".jpg",".jpeg",".svg",".gif",".webp"}
DOC_EXTENSIONS={".md",".html",".htm"}; PUBLISHED_DIR_NAMES={"images","screenshots"}; SOURCE_DIR_NAMES={"source","sources","svg"}; DEFAULT_MAE_LIMIT=0.02
MD_IMAGE_RE=re.compile(r"!\[[^\]]*\]\(([^)\s]+)(?:\s+['\"][^'\"]*['\"])?\)"); HTML_IMAGE_RE=re.compile(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']",re.IGNORECASE)
FENCED_CODE_RE=re.compile(r"```[\s\S]*?```|~~~[\s\S]*?~~~")

def fail(message,errors): errors.append(message)
def warn(message,warnings): warnings.append(message)
def is_external(ref): return ref.lower().startswith(("http://","https://","data:","mailto:","#"))
def normalize_local_ref(root,doc,ref):
    ref=ref.split("#",1)[0].split("?",1)[0]
    if not ref or is_external(ref): return None
    return (doc.parent/ref).resolve()
def is_ignored(path,root):
    try: parts=path.relative_to(root).parts
    except ValueError: return False
    return any(part in {".git","node_modules","dist","build",".venv","venv","templates"} for part in parts)
def discover_published_asset_files(root,errors):
    published_pngs=set()
    for path in root.rglob("*"):
        if not path.is_file() or is_ignored(path,root): continue
        rel=path.relative_to(root); parts_lower=[part.lower() for part in rel.parts]
        if not any(part in PUBLISHED_DIR_NAMES for part in parts_lower[:-1]): continue
        if any(part in SOURCE_DIR_NAMES for part in parts_lower[:-1]): continue
        ext=path.suffix.lower()
        if ext in {".jpg",".jpeg",".gif",".webp"}: fail(f"Prohibited published image format: {rel.as_posix()}",errors)
        elif ext==".svg": fail(f"SVG belongs in a source/runtime directory, not a published-image directory: {rel.as_posix()}",errors)
        elif ext==".png": published_pngs.add(path.resolve())
    return published_pngs
def discover_rendered_local_images(root,errors):
    refs=set()
    for doc in root.rglob("*"):
        if not doc.is_file() or doc.suffix.lower() not in DOC_EXTENSIONS or is_ignored(doc,root): continue
        try: text=doc.read_text(encoding="utf-8")
        except UnicodeDecodeError: continue
        text=FENCED_CODE_RE.sub("",text)
        found=MD_IMAGE_RE.findall(text)+HTML_IMAGE_RE.findall(text)
        for raw in found:
            local=normalize_local_ref(root,doc,raw)
            if local is None: continue
            ext=local.suffix.lower()
            if ext not in IMAGE_EXTENSIONS: continue
            try: rel=local.relative_to(root.resolve())
            except ValueError: fail(f"Image reference escapes repository root: {doc.relative_to(root)} -> {raw}",errors); continue
            if ext in PROHIBITED_PUBLISHED_EXTENSIONS: fail(f"Published local content visual must be PNG: {doc.relative_to(root)} -> {rel}",errors)
            if not local.exists(): fail(f"Broken local image reference: {doc.relative_to(root)} -> {rel}",errors)
            refs.add(local)
    return refs
def load_manifest(path,errors):
    if not path.exists(): return None
    try: data=json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc: fail(f"Invalid asset manifest JSON: {exc}",errors); return None
    if data.get("version")!=1: fail("Asset manifest version must be 1",errors)
    if not isinstance(data.get("assets"),list): fail("Asset manifest must contain an assets array",errors); return None
    return data
def safe_repo_path(root,value,field,errors):
    path=(root/value).resolve()
    try: path.relative_to(root.resolve())
    except ValueError: fail(f"Manifest {field} path escapes repository root: {value}",errors); return None
    return path
def open_png(path,root,errors):
    try:
        image=Image.open(path)
        if image.format!="PNG": fail(f"File extension says PNG but decoder reports {image.format}: {path.relative_to(root)}",errors); return None
        image.verify(); return Image.open(path).convert("RGBA")
    except Exception as exc: fail(f"Unreadable/corrupted PNG {path.relative_to(root)}: {exc}",errors); return None
def normalized_mae(a,b):
    if a.size!=b.size: return math.inf
    diff=ImageChops.difference(a.convert("RGBA"),b.convert("RGBA")); stat=ImageStat.Stat(diff); return sum(stat.mean)/(len(stat.mean)*255.0)
def alpha_content_bbox(img):
    alpha=img.convert("RGBA").getchannel("A"); extrema=alpha.getextrema()
    if extrema==(255,255): return None
    return alpha.getbbox()
def validate_edge_safety(entry,img,warnings,errors):
    if entry.get("allow_edge_contact") is True: return
    margin=int(entry.get("safe_margin_px",2)); bbox=alpha_content_bbox(img)
    if bbox is None:
        if entry.get("require_edge_safety"): warn(f"Edge-safety check skipped for fully opaque asset {entry.get('id')}; use visual review or explicit background-aware tooling",warnings)
        return
    left,top,right,bottom=bbox
    if left<margin or top<margin or (img.width-right)<margin or (img.height-bottom)<margin:
        fail(f"Likely clipping/insufficient transparent safety margin for {entry.get('id')}: bbox={bbox}, canvas={img.size}, required margin={margin}px. Set allow_edge_contact=true only when edge contact is intentional.",errors)
def validate_vector_pair(root,entry,png_path,png,errors):
    source_value=entry.get("source")
    if not isinstance(source_value,str) or not source_value: fail(f"Vector asset {entry.get('id')} requires an SVG source",errors); return
    svg_path=safe_repo_path(root,source_value,"source",errors)
    if svg_path is None: return
    if svg_path.suffix.lower()!=".svg": fail(f"Vector asset source must be SVG: {source_value}",errors); return
    if not svg_path.exists(): fail(f"Missing SVG source for {entry.get('id')}: {source_value}",errors); return
    if svg_path.stem!=png_path.stem and not entry.get("allow_basename_mismatch"): fail(f"PNG/SVG basenames must correspond for {entry.get('id')}: {png_path.name} vs {svg_path.name}",errors)
    try:
        rendered=cairosvg.svg2png(bytestring=svg_path.read_bytes(),output_width=png.width,output_height=png.height); reference=Image.open(io.BytesIO(rendered)).convert("RGBA")
    except Exception as exc: fail(f"Failed to render SVG source for {entry.get('id')}: {exc}",errors); return
    limit=float(entry.get("max_normalized_mae",DEFAULT_MAE_LIMIT)); mae=normalized_mae(reference,png)
    if mae>limit: fail(f"PNG/SVG visual parity failed for {entry.get('id')}: normalized MAE {mae:.5f} > {limit:.5f}",errors)
def validate_manifest(root,data,rendered_refs,errors,warnings):
    ids=set(); published_seen=set()
    for index,entry in enumerate(data["assets"]):
        if not isinstance(entry,dict): fail(f"Manifest asset #{index+1} must be an object",errors); continue
        asset_id=entry.get("id")
        if not isinstance(asset_id,str) or not asset_id.strip(): fail(f"Manifest asset #{index+1} has no valid id",errors); continue
        if asset_id in ids: fail(f"Duplicate asset id: {asset_id}",errors)
        ids.add(asset_id); kind=entry.get("kind")
        if kind not in {"vector","raster"}: fail(f"Unsupported asset kind for {asset_id}: {kind}",errors); continue
        published_value=entry.get("published")
        if not isinstance(published_value,str) or not published_value: fail(f"Asset {asset_id} has no published path",errors); continue
        published=safe_repo_path(root,published_value,"published",errors)
        if published is None: continue
        if published in published_seen: fail(f"Duplicate published asset path: {published_value}",errors)
        published_seen.add(published)
        if published.suffix.lower()!=".png": fail(f"Published asset must be PNG for {asset_id}: {published_value}",errors); continue
        if not published.exists(): fail(f"Missing published PNG for {asset_id}: {published_value}",errors); continue
        png=open_png(published,root,errors)
        if png is None: continue
        ew,eh=entry.get("expected_width"),entry.get("expected_height")
        if ew is None or eh is None: fail(f"Asset {asset_id} must declare expected_width and expected_height",errors)
        else:
            try: ew,eh=int(ew),int(eh)
            except (TypeError,ValueError): fail(f"Invalid expected dimensions for {asset_id}: {ew}x{eh}",errors)
            else:
                if ew<=0 or eh<=0: fail(f"Expected dimensions must be positive for {asset_id}: {ew}x{eh}",errors)
                if png.size!=(ew,eh): fail(f"Dimension mismatch for {asset_id}: actual={png.size}, expected={(ew,eh)}",errors)
        display_width=entry.get("display_width")
        if display_width:
            try:
                dw=int(display_width); min_scale=float(entry.get("minimum_scale_factor",2.0))
                if dw<=0 or min_scale<=0: raise ValueError
                if png.width<math.ceil(dw*min_scale): fail(f"HiDPI resolution target not met for {asset_id}: published width {png.width}px < display_width {dw}px * minimum_scale_factor {min_scale}",errors)
            except (TypeError,ValueError): fail(f"Invalid display_width/minimum_scale_factor for {asset_id}",errors)
        validate_edge_safety(entry,png,warnings,errors)
        if kind=="vector": validate_vector_pair(root,entry,published,png,errors)
        elif entry.get("source") not in (None,""): fail(f"Raster asset {asset_id} must not declare an SVG source unless reclassified as vector",errors)
    for path in sorted(rendered_refs):
        if path.suffix.lower()==".png" and path not in published_seen: fail(f"Rendered local PNG is missing from asset manifest: {path.relative_to(root).as_posix()}",errors)
def run(root,manifest_path):
    errors=[]; warnings=[]; root=root.resolve(); rendered_refs=discover_rendered_local_images(root,errors); published_dir_pngs=discover_published_asset_files(root,errors); all_published=rendered_refs|published_dir_pngs; data=load_manifest(manifest_path,errors)
    if all_published and data is None: fail("Local user-facing images exist but .github/assets-manifest.json is missing",errors)
    elif data is not None: validate_manifest(root,data,all_published,errors,warnings)
    return errors,warnings
def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--root",default=None); parser.add_argument("--manifest",default=None); args=parser.parse_args(); default_root=Path(__file__).resolve().parents[1]; root=Path(args.root).resolve() if args.root else default_root; manifest=Path(args.manifest).resolve() if args.manifest else root/".github"/"assets-manifest.json"; errors,warnings=run(root,manifest)
    for item in warnings: print(f"WARNING: {item}")
    if errors:
        print("Asset validation FAILED:\n")
        for item in errors: print(f"- {item}")
        return 1
    print("Asset validation passed."); return 0
if __name__=="__main__": sys.exit(main())
