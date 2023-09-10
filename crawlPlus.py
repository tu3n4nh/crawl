import argparse
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.common.by import By
# File
import io
# Color
from colorama import init, Fore
# Initialize colorama for Windows terminal color support
init()

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

    args = parser.parse_args()
    # Check arg url
    if args.u:
        url, links = getLinks(args.u)
        if links:
            if args.r:
                for link in links:
                    print(link)
            else:
                for link in links:
                    print(f"{Fore.GREEN}Link: {Fore.RESET}{Fore.BLUE}{link}{Fore.RESET}")
                print(f"{Fore.GREEN}Total links of {Fore.RESET}{Fore.BLUE}{url}: {Fore.RESET}{Fore.GREEN}{len(links)}{Fore.RESET}")
        # Check arg output file
        if args.o:
            # Open the file in write mode
            textLinks = '\n'.join(links)
            with io.open(f'{args.o}', 'w', encoding="utf-8") as file:
                file.write(textLinks)
            print(f"{Fore.YELLOW}File saved: {args.o}{Fore.RESET}")

    elif args.f:
        with io.open(f'{args.f}', 'r', encoding="utf-8") as file:
            text = ''
            if args.t:
                list_links = []
                urls = []
                for line in file:
                    urls.append(line.strip())
                with concurrent.futures.ThreadPoolExecutor(max_workers=args.t) as executor:
                    results = executor.map(getLinks, urls)

                # Process the results
                for url, links in results:
                    if links is not None:
                        list_links.extend(links)

                new_array = [remove_trailing_slash(link) for link in list_links]
                uniqueLinks = filter_unique_links(new_array)
                sortedLinks = sorted(uniqueLinks)
                
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
                    url, links = getLinks(line)
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


# Process get links
def getLinks(url):
    pass
    # 1. Start Session
    driver = webdriver.Firefox()
    
    # 2. Take action on browser
    url = check_view_source(url)
    driver.get(url)

    # Get links from 'a', 'img', 'script', 'link', 'area', 'form', 'frame', 'iframe', 'object', 'embed', 'source', 'base'
    links = ''
    aTags = driver.find_elements(By.TAG_NAME, "a")
    for aTag in aTags:
        links = links + aTag.get_attribute("href") + '\n'
    imgTags = driver.find_elements(By.TAG_NAME, "img")
    for imgTag in imgTags:
        links = links + imgTag.get_attribute("src") + '\n'
    scriptTags = driver.find_elements(By.TAG_NAME, "script")
    for scriptTag in scriptTags:
        links = links + scriptTag.get_attribute("src") + '\n'
    linkTags = driver.find_elements(By.TAG_NAME, "link")
    for linkTag in linkTags:
        links = links + linkTag.get_attribute("href") + '\n'
    areaTags = driver.find_elements(By.TAG_NAME, "area")
    for areaTag in areaTags:
        links = links + areaTag.get_attribute("src") + '\n'
    fromTags = driver.find_elements(By.TAG_NAME, "from")
    for fromTag in fromTags:
        links = links + fromTag.get_attribute("action") + '\n'
    frameTags = driver.find_elements(By.TAG_NAME, "frame")
    for frameTag in frameTags:
        links = links + frameTag.get_attribute("src") + '\n'
    iframeTags = driver.find_elements(By.TAG_NAME, "iframe")
    for iframeTag in iframeTags:
        links = links + iframeTag.get_attribute("src") + '\n'
    objectTags = driver.find_elements(By.TAG_NAME, "object")
    for objectTag in objectTags:
        links = links + objectTag.get_attribute("data") + '\n'
    embedTags = driver.find_elements(By.TAG_NAME, "embed")
    for embedTag in embedTags:
        links = links + embedTag.get_attribute("src") + '\n'
    sourceTags = driver.find_elements(By.TAG_NAME, "source")
    for sourceTag in sourceTags:
        links = links + sourceTag.get_attribute("src") + '\n'
    baseTags = driver.find_elements(By.TAG_NAME, "base")
    for baseTag in baseTags:
        links = links + baseTag.get_attribute("href") + '\n'

    # Link beautifier
    arrLinks = links.splitlines()
    new_array = [remove_trailing_slash(link) for link in arrLinks]
    uniqueLinks = filter_unique_links(new_array)
    sortedLinks = sorted(uniqueLinks)
    
    urls = [link for link in sortedLinks if link.startswith("http")]
    driver.close()

    return url, urls

# Process remove trailing slashes from the end of a link
def remove_trailing_slash(link):
    return link.rstrip('/')

# Process duplicate links
def filter_unique_links(links):
    unique_links = set()

    for link in links:
        unique_links.add(link)

    return list(unique_links)

# Process view source mode
def check_view_source(link):
    if link.startswith("view-source:"):
        return link.lstrip("view-source:")
    return link

if __name__ == "__main__":
    main()