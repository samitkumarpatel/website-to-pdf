import requests
from bs4 import BeautifulSoup
from weasyprint import HTML

BASE_URL = "https://gobyexample.com"
INDEX_PAGE = BASE_URL + "/"

def fetch_page(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_index_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    ul = soup.find('ul')
    li = ul.find_all('li')
    # Iterate over all <li> elements and extract the a href links
    links = []
    for li in li:
        links += li.find_all('a')
    print(links)
    # Filter out the links in the href attribute
    examples = []
    for link in links:
        examples.append(INDEX_PAGE + link['href'])
    print(examples)
    return examples

def fetch_and_combine_content(urls):
    content = ""
    for url in urls:
        page_html = fetch_page(url)
        page_soup = BeautifulSoup(page_html, 'html.parser')
        example_content = page_soup.find('body').prettify()
        content += example_content
    return content

def save_to_pdf(content, output_file):
    HTML(string=content).write_pdf(output_file)

# Fetch the index page
index_html = fetch_page(INDEX_PAGE)

# Parse the index page to get all example URLs
example_urls = parse_index_page(index_html)

# Fetch and combine the content from all example URLs
full_content = fetch_and_combine_content(example_urls)

# Save the combined content to a PDF file
output_file_path = "gobyexample.pdf"
save_to_pdf(full_content, output_file_path)

print(f"PDF generated and saved as {output_file_path}")

