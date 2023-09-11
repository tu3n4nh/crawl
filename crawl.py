import argparse
import requests
import concurrent.futures
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
import warnings
from urllib.parse import urljoin
# File
import io
# Color
from colorama import init, Fore
# Initialize colorama for Windows terminal color support
init()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}

def main():
    parser = argparse.ArgumentParser(description="Tool crawl")
    parser.add_argument("-u", type=str, help="URL you want to crawl")
    parser.add_argument("-f", type=str, help="File URL you want to crawl")
    parser.add_argument("-o", type=str, help="Output file you want to save (txt)")
    parser.add_argument("-r", action='store_true', help="Raw content view mode")
    parser.add_argument("-t", type=int, help="Threads of requests")

    intro = '''                                                                                                    
        @@@@@@@                                        @@                                       
     #@@      &@@                                      @@                                       
    @@              @@ @@@   @@@@@@   @@     @@    /@  @@       @@@@@@@    @@      @@         
    @@              @@@    @@     @@   @\   /@@    @@  @@       @@     @@   @@    @@          
    @@              @@       _#@@@@@   \@   @ @@  @@   @@       @@      @@   @@  @@           
     @@        @@@  @@     @@     @@    @@ @@  @@ @    @@       @@      @    @@  @@           
      @@@     @@@   @@     @@     @@     @@@   @@@@    @@       @@^    @@     @@@@            
         @@@@@      @@      @@@@@/ @@    \@     @@     @@  (@)  @@ @@@@        @@             
                                                                @@            @@              
                                                                @@          @@@                                                                                                                   
    '''
    print(f"{Fore.GREEN}{intro}{Fore.RESET}")
    try:
        args = parser.parse_args()
        # Check arg url
        if args.u:
            text = ""
            links = get_links(args.u)
            if links:
                for link in links:
                    text = text + f"{link}" + "\n"
                array = text.splitlines()
                new_array = [remove_trailing_slash(link) for link in array]
                uniqueLinks = filter_unique_links(new_array)
                listLinks = "\n".join(uniqueLinks)
                sortedLinks = sorted(listLinks.split('\n'))
                if args.r:
                    for link in sortedLinks:
                        print(link)
                else:
                    for link in sortedLinks:
                        print(f"{Fore.GREEN}Link: {Fore.RESET}{Fore.BLUE}{link}{Fore.RESET}")
                    print(f"{Fore.GREEN}Total links of {Fore.RESET}: {Fore.GREEN}{len(links)}{Fore.RESET}")
            
                # Check arg output file
                if args.o:
                    # Open the file in write mode
                    sortedLinks = '\n'.join(sorted(text.split('\n')))
                    with io.open(f'{args.o}', 'w', encoding="utf-8") as file:
                        file.write(sortedLinks)
                    print(f"{Fore.YELLOW}File saved: {args.o}{Fore.RESET}")
            else:
                print("Usage: python crawl.py -u <target_url>")
                return

        # Check arg list
        elif args.f:
            with io.open(f'{args.f}', 'r', encoding="utf-8") as file:
                text = ""
                if args.t:
                    list_links = []
                    urls = []
                    for line in file:
                        urls.append(line.strip())
                    with concurrent.futures.ThreadPoolExecutor(max_workers=args.t) as executor:
                        results = executor.map(fetch_url, urls)

                    # Process the results
                    for url, html_content in results:
                        if html_content is not None:
                            links = crawl_links(url, html_content)
                            if links:
                                list_links.extend(links)
                    new_array = [remove_trailing_slash(link) for link in list_links]
                    uniqueLinks = filter_unique_links(new_array)
                    listLinks = "\n".join(uniqueLinks)
                    sortedLinks = sorted(listLinks.split('\n'))
                    if args.r:
                        for link in sortedLinks:
                            print(f"{link}")
                    else:
                        for link in sortedLinks:
                            print(f"{Fore.GREEN}Link: {Fore.RESET}{Fore.BLUE}{link}{Fore.RESET}")
                        print(f"{Fore.GREEN}Total links of {Fore.RESET}{Fore.BLUE}{args.f}: {Fore.RESET}{Fore.GREEN}{len(sortedLinks)}{Fore.RESET}")
                    # Export crawled links to the output file, if specified
                    if args.o:
                        # Open the file in write mode
                        with io.open(f'{args.o}', 'w', encoding="utf-8") as file:
                            file.write('\n'.join(sortedLinks))
                        print(f"{Fore.YELLOW}File saved: {args.o}{Fore.RESET}")

                else:
                    sortedLinks = []
                    for line in file:
                        line = line.strip()
                        links = get_links(line)
                        if links:
                            for link in links:
                                text = text + f"{link}" + "\n"
                        else:
                            continue
                    array = text.splitlines()
                    new_array = [remove_trailing_slash(link) for link in array]
                    uniqueLinks = filter_unique_links(new_array)
                    listLinks = "\n".join(uniqueLinks)
                    sortedLinks = sorted(listLinks.split('\n'))
                    if args.r:
                        for link in sortedLinks:
                            print(f"{link}")
                    else:
                        for link in sortedLinks:
                            print(f"{Fore.GREEN}Link: {Fore.RESET}{Fore.BLUE}{link}{Fore.RESET}")
                        print(f"{Fore.GREEN}Total links of {Fore.RESET}{Fore.BLUE}{args.f}: {Fore.RESET}{Fore.GREEN}{len(sortedLinks)}{Fore.RESET}")

                    if args.o:
                        # Open the file in write mode
                        with io.open(f'{args.o}', 'w', encoding="utf-8") as file:
                            file.write('\n'.join(sortedLinks))
                        print(f"{Fore.YELLOW}File saved: {args.o}{Fore.RESET}")
        else:
            print("Usage: python crawl.py -h")

    except SystemExit:
        print("Usage: python crawl.py -h")


# Process option link
def get_links(url):
    try:
        response = requests.get(url, headers=headers, verify=False)
    except Exception:
        return None
  
    # Parse the HTML using BeautifulSoup
    warnings.filterwarnings("ignore")
    soup = BeautifulSoup(response.text, 'html.parser')

    links = []
    relative_links = []
    link_elements = soup.find_all(['a', 'img', 'script', 'link', 'area', 'form', 'frame', 'iframe', 'object', 'embed', 'source', 'base'])
    
    if link_elements:
        for element in link_elements:
            href = element.get('href') or element.get('src') or element.get('data') or element.get('action')
            if href and href.startswith('http'):
                links.append(href)
            elif href and not (href.startswith('#') and href.startswith('?')):
                if href.startswith('//'):
                    href = href.split('//')[1]
                    tmp_href = check_http_https(href)
                    if tmp_href:
                        links.append(tmp_href)
                elif href.startswith('/') or href.startswith('./') or href.startswith('../'):
                    relative_links.append(href)
                    full_links = [urljoin(url, relative_link) for relative_link in relative_links]
                    links = links + full_links
    else:
        return None
    
    # Filter duplicate links
    unique_links = filter_unique_links(links)
    return unique_links

# Process duplicate links
def filter_unique_links(links):
    unique_links = set()

    for link in links:
        unique_links.add(link)

    return list(unique_links)

# Process check http, https
def check_http_https(link):
    # Try an HTTPS request
    response_https = requests.get("https://" + link, headers=headers, verify=False, timeout=5)
    try:
        if response_https.status_code == 200:
            return f"https://{link}"
    except requests.exceptions.RequestException:
        pass
    try:
        response_http = requests.get("http://" + link, headers=headers, verify=False, timeout=5)
        if response_http.status_code == 200:
            return f"http://{link}"
    except requests.exceptions.RequestException:
        return None

# Process multi threads
def fetch_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return url, response.text
    except requests.exceptions.RequestException as e:
        return url, None

# Process crawl
def crawl_links(url, html_content):
    warnings.filterwarnings("ignore")
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    relative_links = []
    link_elements = soup.find_all(['a', 'img', 'script', 'link', 'area', 'form', 'frame', 'iframe', 'object', 'embed', 'source', 'base'])
    
    if link_elements:
        for element in link_elements:
            href = element.get('href') or element.get('src') or element.get('data') or element.get('action')
            if href and href.startswith('http'):
                links.append(href)
            elif href and not (href.startswith('#') and href.startswith('?')):
                if href.startswith('//'):
                    href = href.split('//')[1]
                    tmp_href = check_http_https(href)
                    if tmp_href:
                        links.append(tmp_href)
                elif href.startswith('/') or href.startswith('./') or href.startswith('../'):
                    relative_links.append(href)
                    full_links = [urljoin(url, relative_link) for relative_link in relative_links]
                    links = links + full_links
    else:
        return None
    
    # Filter duplicate links
    unique_links = filter_unique_links(links)
    return unique_links

# Process remove trailing slashes from the end of a link
def remove_trailing_slash(link):
    return link.rstrip('/')

if __name__ == "__main__":
    main()