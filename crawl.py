import argparse
import requests
from bs4 import BeautifulSoup
import warnings
from urllib.parse import urljoin
# File
import io
# Color
from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import TerminalFormatter
from colorama import init, Fore, Style
# Initialize colorama for Windows terminal color support
init()
headers = {'User-Agent': 'crawl.py'}

def main():
    parser = argparse.ArgumentParser(description="Tool crawl")
    parser.add_argument("-u", type=str, help="URL you want to crawl")
    parser.add_argument("-f", type=str, help="File URL you want to crawl")
    parser.add_argument("-o", type=str, help="Output file you want to save (txt)")
    
    intro = '''                                                                                                    
        @@@@@@@                                        @@                                       
     #@@      &@@                                      @@                                       
    @@              @@ @@@   @@@@@@   @@     @@    @@  @@        @@@@@@@    @@      @@         
    @@              @@@    @@     @@   @@   @@@    @@  @@        @@     @@   @@    @@          
    @@              @@         @@@@@   @@   @ @@  @@   @@        @@      @@   @@  @@           
     @@        @@@  @@     @@     @@    @@ @@  @@ @    @@        @@      @    @@  @@           
      @@@     @@@   @@     @@     @@     @@@   @@@@    @@        @@^    @@     @@@@            
         @@@@@      @@      @@@@@  @@    @@     @@     @@   @@   @@ @@@@        @@             
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
                print(f"List links of target: {args.u}")
                for link in links:
                    text = text + f"{link}" + "\n"
                    print(f"{Fore.GREEN}Link: {Fore.RESET}{Fore.BLUE}{link}{Fore.RESET}")
                print(f"{Fore.GREEN}Total links: {Fore.RESET}{Fore.BLUE}{len(links)}{Fore.RESET}")
            
                # Check arg output file
                if args.o:
                    # Open the file in write mode
                    with io.open(f'{args.o}', 'w', encoding="utf-8") as file:
                        file.write(text)
                    print(f"File saved: {args.o}")
            else:
                print("Usage: python crawl.py -u <target_url>")
                return

        # Check arg list
        elif args.f:
            with io.open(f'{args.f}', 'r', encoding="utf-8") as file:
                text = ""
                for line in file:
                    line = line.strip()
                    links = get_links(line)
                    if links:
                        print(f"{Fore.GREEN}List links of target: {Fore.RESET}{Fore.BLUE}{line}{Fore.RESET}")
                        for link in links:
                            text = text + f"{link}" + "\n"
                            print(f"{Fore.GREEN}Link: {Fore.RESET}{Fore.BLUE}{link}{Fore.RESET}")
                        print(f"{Fore.GREEN}Total links: {Fore.RESET}{Fore.BLUE}{len(links)}{Fore.RESET}")
                    else:
                        continue
                if args.o:
                    # Open the file in write mode
                    array = text.splitlines()
                    uniqueLinks = filter_unique_links(array)
                    listLinks = "\n".join(uniqueLinks)
                    with io.open(f'{args.o}', 'w', encoding="utf-8") as file:
                        file.write(listLinks)
                    print(f"File saved: {args.o}")
                    # # Check arg option
                    # if args.o:
                    #     # Get option link
                    #     if args.o == "link":
                    #         links = get_links(line)
                    #         if links:
                    #             print(f"{Fore.GREEN}List links of target: {Fore.RESET}{Fore.BLUE}{line}{Fore.RESET}")
                    #             for link in links:
                    #                 text = text + f"{link}" + "\n"
                    #                 print(f"{Fore.GREEN}Link: {Fore.RESET}{Fore.BLUE}{link}{Fore.RESET}")
                    #             print(f"{Fore.GREEN}Total links: {Fore.RESET}{Fore.BLUE}{len(links)}{Fore.RESET}")
                                
                    #     # Get option form   
                    #     elif args.o == "form":
                    #         form_elements = get_form(args.u)
                    #         if form_elements:
                    #             index = 1
                    #             text = f"List form of target: {args.u}" + "\n"
                    #             print(f"List form of target: {args.u}")
                    #             for form_element in form_elements:
                    #                 form_html = form_element.prettify()
                    #                 text = text + f"\nForm {index}:\n" + form_html + "\n"
                    #                 highlighted_html = highlight(form_html, HtmlLexer(), TerminalFormatter())
                    #                 print(f"{Fore.GREEN}Form {index}:{Fore.RESET}")
                    #                 print(highlighted_html)
                    #                 index = index + 1
                    #             text = text + f"Total forms: {len(form_elements)}" + "\n"
                    #             print(f"{Fore.GREEN}Total forms: {Fore.RESET}{Fore.BLUE}{len(form_elements)}{Fore.RESET}")

                                
                    #     # Get option response
                    #     elif args.o == "response":
                    #         response = get_response(args.u)
                    #         if response:
                    #             print(response.headers)

                    #     else:
                    #         print("Option: -o <option_crawl> must be: link, form, response, ...")     
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
                if href.startswith('/') or href.startswith('./') or href.startswith('../'):
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

# Process option form
def get_form(url):
    response = requests.get(url, headers=headers)

    # # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # # Find the form element
    form_elements = soup.find_all('form')
    if form_elements:
        return form_elements
    else:
        print("This site does not contain forms!")
        return

# Process option response
def get_response(url):
    response = requests.get(url, headers=headers)
    print(response.text)
    return response

if __name__ == "__main__":
    main()