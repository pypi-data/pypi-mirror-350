import os
import click
from sentence_transformers import SentenceTransformer
import bs4 as bs
import re
import json

def clean_path(path, dir):
    clean = '/' + os.path.relpath(path, dir)
    # remove ending index.html
    if clean.endswith('/index.html'):
        clean = clean[:-10]  # remove 'index.html'
    return clean

def find_html_files(dir):
    html_files = {}
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                html_files[path] = clean_path(path, dir)
    return html_files

def clean_text(text: str) -> str:
    # Remove leading and trailing whitespace
    clean = text.strip()
    # Remove invisible characters
    clean = ''.join(c for c in clean if c.isprintable())
    # Collapse multiple spaces or newlines into a single space
    clean = re.sub(r'\s+', ' ', clean)

    return clean
    

def extract_text_from_node(node: bs.Tag) -> tuple[list, str | None]:
    for ignore in node.select('[data-pagefind-ignore]'):
        ignore.decompose()
    sections = node.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'dt', 'dd'])
    results = []
    title = None

    for section in sections:
        elementID = section.get('id', '')
        text = section.get_text(strip=True)
        text = clean_text(text)
        if text:
            if not title and section.name == 'h1':
                title = text
            results.append({
                'id': elementID,
                'isHeading': section.name.startswith('h'),
                'text': text
            })
    return (results, title)

def extract_text_from_html(file_path: str) -> tuple[dict[str, list[str]], str | None]:
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = bs.BeautifulSoup(file, 'html.parser')
        body = soup.find(attrs={'data-pagefind-body': True})
        if not body or not isinstance(body, bs.Tag):
            return {}, None
        (texts, title) = extract_text_from_node(body)
        tags = {}
        curent_tag = ''
        for t in texts:
            if t['id']:
                curent_tag = t['id']
            if t['isHeading']:
                continue
            if curent_tag not in tags:
                tags[curent_tag] = [t['text']]
            else:
                tags[curent_tag].append(t['text'])
    return tags, title

def get_embeddings_for_site(site_structure, model: SentenceTransformer):
    embeddings = {}
    for path in site_structure:
        embeddings[path] = {}  # Initialize dictionary for this path
        for tag in site_structure[path]:
            print(f'Processing {path}#{tag}')
            texts = site_structure[path][tag]
            if not texts:
                continue
            # Generate embeddings for each text
            emb = model.encode(texts, show_progress_bar=False)
            # Save float32 vector
            embeddings[path][tag] = emb

    return embeddings

def encode_embeddings(embeddings, dim):
    encoded = bytearray()
    encoded.extend(dim.to_bytes(4, 'little'))  # Dimension of embeddings
    len_path = len(embeddings)
    encoded.extend(len_path.to_bytes(4, 'little'))  # Number of paths
    for path, tags in embeddings.items():
        path_bytes = path.encode('utf-8')
        len_path_bytes = len(path_bytes)
        encoded.extend(len_path_bytes.to_bytes(4, 'little'))  # Length of path
        encoded.extend(path_bytes)  # Path bytes
        len_tags = len(tags)
        encoded.extend(len_tags.to_bytes(4, 'little'))  # Number of tags
        for tag, emblist in tags.items():
            tag_bytes = tag.encode('utf-8')
            len_tag_bytes = len(tag_bytes)
            encoded.extend(len_tag_bytes.to_bytes(4, 'little'))  # Length of tag
            encoded.extend(tag_bytes)  # Tag bytes
            len_emb = len(emblist)
            encoded.extend(len_emb.to_bytes(4, 'little'))
            for emb in emblist:
                emb_bytes = emb.astype('float32').tobytes()
                # check size
                if len(emb_bytes) != dim * 4:
                    raise ValueError(f'Embedding size mismatch: expected {dim * 4}, got {len(emb_bytes)}')
                encoded.extend(emb_bytes)  # Embedding bytes
    return encoded

@click.command()
@click.option('--model-name', default='BAAI/bge-m3', help='Model name to use for embeddings')
@click.option('--path', default='./dist', help='Path to website files')
def main(model_name, path):
    html_files = find_html_files(path)
    site_structure = {}
    title_dict = {}
    for file_path, clean_path in html_files.items():
        (texts, title) = extract_text_from_html(file_path)
        if texts:
            site_structure[clean_path] = texts
            if title:
                title = clean_text(title)
                title_dict[clean_path] = title
    print(f'Found {len(site_structure)} HTML files in {path}')

    print(f'Loading model {model_name}...')
    model = SentenceTransformer(model_name)
    dim = model.get_sentence_embedding_dimension()
    embeddings = get_embeddings_for_site(site_structure, model)
    encoded = encode_embeddings(embeddings, dim)
    output_path = os.path.join(path, 'pagevecfind')
    os.makedirs(output_path, exist_ok=True)
    output_file = os.path.join(output_path, 'embeddings.bin')
    with open(output_file, 'wb') as f:
        f.write(encoded)
    print(f'Embeddings saved to {output_file}')
    title_file = os.path.join(output_path, 'info.json')
    with open(title_file, 'w', encoding='utf-8') as f:
        json.dump(title_dict, f, ensure_ascii=False)
    print(f'Path info saved to {title_file}')

if __name__ == '__main__':
    main()
