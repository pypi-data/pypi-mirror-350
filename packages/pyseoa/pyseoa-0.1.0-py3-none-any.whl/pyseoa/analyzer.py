import csv
import json
import logging
import os
import requests
import re
import time
from bs4 import BeautifulSoup
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from typing import Optional, Dict, List
from urllib.parse import urlparse




FLAG_NONE               :int = 0
FLAG_TITLE              :int = 1
FLAG_META_DESCRIPTION   :int = 2
FLAG_H1_TAGS            :int = 4
FLAG_ALT_TAGS           :int = 8
FLAG_CANONICAL          :int = 16
FLAG_OPENGRAPH          :int = 32
FLAG_TWITTER            :int = 64
FLAG_ROBOTS_TXT         :int = 128
FLAG_SITEMAP            :int = 256
FLAG_FAVICON            :int = 512
FLAG_KEYWORD_DENSITY    :int = 1024
FLAG_MOBILE_FRIENDLY    :int = 2048
FLAG_LINKS              :int = 4096
FLAG_NOFOLLOW_LINKS     :int = 8192
FLAG_HREFLANG           :int = 16384
FLAG_META_ROBOTS        :int = 32768
FLAG_WEBVITALS          :int = 65536
FLAG_ACCESSIBILIY       :int = 131072
FLAG_STRUCTERED_DATA    :int = 262144
FLAG_AMP_COMPLIANCE     :int = 524288
FLAG_ALL                :int = 1048575



logging.basicConfig(
    filename='seo_errors.log',
    filemode='w',
    level=logging.WARNING,
    format="$(asctime)s - %(levelname)s - %(message)s"
)



class SEOAnalyzer:
    """
    A class to perform SEO analysis on a given webpage.
    """

    def __init__(self, url: str, google_api_key: Optional[str] = None) -> None:
        """
        Initializes the SEOAnalyzer with the target URL.

        Args:
            url (str): The url of the web page to analyze.
        """
        self.url = url
        self.html: Optional[str] = None
        self.soup: Optional[BeautifulSoup] = None
        self.analysis: Dict[str, object] = {}
        self.google_api_key = google_api_key

    def to_json(self) -> str:
        """
        Converts the analysis result to a json string.
        """
        return json.dumps(self.analysis, ensure_ascii=False, indent=2)

    def export_to_json(self, filepath: str) -> None:
        """
        Exports the SEO analysis to a JSON file.

        Args:
            filepath (str): Path to the output .json file.
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.analysis, f, indent=2, ensure_ascii=False)

    def export_to_csv(self, filepath: str) -> None:
        """
        Esports the SEO analysis to a CSV file.

        Args:
            filepath (str): Path to the output .csv file.
        """
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Metric", "Value"])
            for key, value in self.analysis.items():
                if isinstance(value, list):
                    writer.writerow([key, json.dumps(value)])
                elif isinstance(value, dict):
                    writer.writerow([key, json.dumps(value)])
                else:
                    writer.writerow([key, value])

    def export_to_html(self, filepath: str) -> None:
        """
        Exports the SEO analysis to a simple HTML report.

        Args:
            filepath (str): Path to the output .html file.
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f'<html><head><title>SEO Report for {self.url}</title></head><body>')
            f.write(f'<h1>SEO Report for {self.url}</h1>')
            f.write("<table border='1' cellpadding='5 cellspacing='0'>")
            for key, value in self.analysis.items():
                f.write('<tr>')
                f.write(f'<td><strong>{key}</strong></td>')
                if isinstance(value, (list, dict)):
                    f.write(f'<td><pre>{json.dumps(value, indent=2)}</pre></td>')
                else:
                    f.write(f"<td>{value}</td>")
                f.write('</tr>')
            f.write('</table></body></html>')

    def fetch_page(self) -> bool:
        """
        Fetches the HTML content of the target URL.

        Returns:
            bool: True if the page was fetched successfully, False otherwise.
        """
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            self.html = response.text
            self.soup = BeautifulSoup(self.html, 'html.parser')
            return True
        except requests.RequestException as e:
            print(f'Error fetching {self.url}: {e}')
            return False

    def analyze_title(self) -> 'SEOAnalyzer':
        """
        Analyzes the <title> tag.
        """
        title = self.soup.title.string.strip() if self.soup and self.soup.title else "Missing"
        self.analysis['title'] = title
        return self
    
    def analyze_meta_description(self) -> 'SEOAnalyzer':
        """
        Analyzes the meta description tag.
        """
        tag = self.soup.find('meta', attrs={'name':'description'}) if self.soup else None
        desc = tag['content'].strip() if tag and tag.get('content') else 'Missing'
        self.analysis['meta_description'] = desc
        return self
    
    def analyze_accessibility(self) -> 'SEOAnalyzer':
        """
        Performs bas accessibility checks (labels, landmarks).

        Returns:
            SEOAnalyzer: Returns this instance.
        """
        if not self.soup:
            self.analysis['accessibility_issues'] = 'Missing HTML'
            return self
        
        issues = []

        # Check for missing labels on inputs
        inputs = self.soup.find_all('input')
        for inp in inputs:
            if inp.get('type') not in ['hidden','submit']:
                if not inp.get('aria-label') and not inp.get('aria-labelledby') and not inp.get('id'):
                    issues.append('Input field without label or ARIA attributes')

        # Check landmarks
        landmarks = ['main','nav','header','footer']
        landmark_present = any(self.soup.find(tag) for tag in landmarks)
        if not landmark_present:
            issues.append('Missing semantic landmarks (main/nav/header/footer)')
        self.analysis['accessibility_issues'] = issues if issues else 'No major issues'
        return self
    
    def analyze_structured_data(self) -> 'SEOAnalyzer':
        """
        Detects presence of structured data using JSON-LD format.
        
        Returns:
            (SEOAnalyzer): Returns this instance.
        """
        if not self.soup:
            self.analysis['structured_data'] = 'Missing HTML'
            return self
        
        scripts = self.soup.find_all('script', type='application/json')
        if scripts:
            self.analysis['structered_data'] = f"{len(scripts)} JSON-LD blocks found"
        else:
            self.analysis['structered_data'] = 'None found'
        return self

    def analyze_h1_tags(self) -> 'SEOAnalyzer':
        """
        Extracts all H1 tags.

        Returns:
            (SEOAnalyzer): Returns this instance.
        """
        h1_tags = [h1.get_text(strip=True) for h1 in self.soup.find_all('h1')] if self.soup else []
        self.analysis['h1_tags'] = h1_tags or "Missing"
        return self
    
    def analyze_alt_tags(self) -> 'SEOAnalyzer':
        """
        Finds images missing alt attributes.
        """
        images = self.soup.find_all('img') if self.soup else []
        self.analysis['image_count'] = len(images)
        missing = [img.get('src') or 'unknown_src' for img in images if not img.get('alt')]
        self.analysis['missing_alt_tags'] = missing
        return self
    
    def analyze_canonical(self) -> 'SEOAnalyzer':
        """
        Checks for canonical link tag.
        """
        tag = self.soup.find('link', rel='canonical') if self.soup else None
        canonical = tag['href'] if tag and tag.get('href') else 'Missing'
        self.analysis['canonical_url'] = canonical
        return self
    
    def analyze_open_graph(self) -> 'SEOAnalyzer':
        """
        Extracts Open Graph meta tags.
        """
        og_title = self.soup.find('meta', property='og:title')
        og_desc = self.soup.find('meta', property='og:description')
        self.analysis['og:title'] = og_title['content'] if og_title and og_title.get('content') else 'Missing'
        self.analysis['og:description'] = og_desc['content'] if og_desc and og_desc.get('content') else 'Missing'
        return self
    
    def analyze_twitter_tags(self) -> 'SEOAnalyzer':
        """
        Checks for Twitter Card meta tag.

        Returns:
            SEOAnalyzer: This instance.
        """
        twitter_title = self.soup.find('meta', property='og:title')
        twitter_desc = self.soup.find('meta', property='og:description')
        self.analysis['twitter:title'] = twitter_title['content'] if twitter_title and twitter_title['content'] else 'Missing'
        self.analysis['twitter:description'] = twitter_desc['content'] if twitter_desc and twitter_desc['content'] else 'Missing'
        return self
    
    def analyze_hreflang(self) -> 'SEOAnalyzer':
        """
        Checks for presence and count of hreflang tags for international SEO.

        Returns:
            SEOAnalyzer: This instance.
        """
        if not self.soup:
            self.analysis['hreflang_tags'] = 0
            return self
        
        hreflang_tags = self.soup.find_all('link', rel='alternate', hreflang=True)
        self.analysis['hreflang_tags'] = len(hreflang_tags)
        return self

    def check_robots_txt(self) -> 'SEOAnalyzer':
        """
        Checks if robots.txt is present.
        """
        parsed = urlparse(self.url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        
        try:
            resp = requests.get(robots_url, timeout=5)
            self.analysis['robots_txt'] = "Present" if resp.status_code == 200 else "Missing"
        except:
            self.analysis['robots_txt'] = 'Error'
        
        return self
    
    def check_sitemap(self) -> 'SEOAnalyzer':
        parsed = urlparse(self.url)
        sitemap_url = f"{parsed.scheme}://{parsed.netloc}/sitemap.xml"
        
        try:
            resp = requests.get(sitemap_url, timeout=5)
            self.analysis['sitemap_xml'] = 'Present' if resp.status_code == 200 else 'Missing'
        except:
            self.analysis['sitemap_xml'] = 'Error'

        return self
    
    def check_favicon(self) -> 'SEOAnalyzer':
        """
        Checks for a fav icon link.

        Returns:
            SEOAnalyzer: Returns this instance.
        """
        tag = self.soup.find('link', rel=lambda r: r and 'icon' in r.lower()) if self.soup else None
        self.analysis['favicon'] = 'Present' if tag else 'Missing'
        return self
    
    def analyze_keyword_density(self, top_n = 10) -> 'SEOAnalyzer':
        """
        Analyzes the most common keywords in the body text.

        Args:
            top_n (int): Number of top keywords to include.

        Returns:
            SEOAnalyzer: Returns this instance.
        """
        if not self.soup:
            self.analysis['keyword_density'] = []
            return self
        
        # Extract visible text
        text = self.soup.get_text(separator=' ', strip=True).lower()
        words = re.findall(r'\b[a-z]{3,}\b', text) # 3+ letter words
        total_words = len(words)

        if total_words == 0:
            self.analysis['keyword_density'] = []
            return self
        
        words_count = Counter(words)
        most_common = words_count.most_common(top_n)
        density = [
            {'word':word, 'count':count, 'percent':round((count / total_words) * 100, 2)}
            for word, count in most_common
        ]

        self.analysis['keyword_density'] = density
        return self
    
    def analyze_mobile_friendly(self) -> 'SEOAnalyzer':
        """
        Performs a basic check for mobile-friendly design (viewport meta tag).

        Returns:
            SEOAnalyzer: Returns this instance.
        """
        tag = self.soup.find('meta', attrs={'name':'viewport'}) if self.soup else None
        self.analysis['mobile_friendly'] = 'Likely' if tag else 'Unlikely'
        return self
    
    def analyze_links(self) -> 'SEOAnalyzer':
        """
        Counts internal and external anchor tags.
        """
        if not self.soup:
            self.analysis['internal_links'] = 0
            self.analysis['external_links'] = 0
            return self
        
        domain = urlparse(self.url).netloc
        links = self.soup.find_all('a', href=True)
        internal = 0
        external = 0

        for link in links:
            href = link['href']
            if href.startswith('/') or domain in href:
                internal += 1
            else:
                external += 1

        self.analysis['internal_links'] = internal
        self.analysis['external_links'] = external

        return self
    
    def analyze_nofollow_links(self) -> 'SEOAnalyzer':
        """
        Counts how many anchor tags use rel="nofollow".

        Returns:
            SEOAnalyzer: Returns this instance.
        """
        if not self.soup:
            self.analysis['nofollow_links'] = 0
            return self
        links = self.soup.find_all('a', href=True, rel=True)
        nofollow_count = sum('nofollow' in link.get('rel', []) for link in links)
        self.analysis['nofollow_links'] = nofollow_count
        return self
    
    def analyze_meta_robots(self) -> 'SEOAnalyzer':
        """
        Checks if a meta robots tag is present and its value.
        """
        if not self.soup:
            self.analysis['meta_robots'] = 'Missing'
            return self
        
        tag = self.soup.find('meta', attrs={'name':'robots'})
        if tag and tag.get('content'):
            self.analysis['meta_robots'] = tag['content'].lower()
        else:
            self.analysis['meta_robots'] = 'Missing'
        return self
    
    def fetch_core_web_vitals(self) -> 'SEOAnalyzer':
        if not self.google_api_key:
            self.analysis['core_web_vitals'] = 'No google pagespeed insights API key specified.'
            return self

        api_url = (
            f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
            f"?url={self.url}&key={self.google_api_key}&strategy=mobile"
        )
        data = self._fetch_with_retry(api_url)
        # with open('result.json', 'w') as f:
        #    json.dump(data, f)
        # print(data)
        if data:
            # Score is a float between 0–1, convert to 0–100
            score = data["lighthouseResult"]["categories"]["performance"]["score"]
            self.analysis["lighthouse_score"] = int(score * 100)
            # audits
            vitals = data['lighthouseResult']['audits']
            self.analysis['core_web_vitals'] = {
                'LCP': vitals['largest-contentful-paint']['displayValue'],
                'FID': vitals['interactive']['displayValue'],
                'CLS': vitals['cumulative-layout-shift']['displayValue'],
            }
        else:
            self.analysis['core_web_vitals'] = 'Failed to fetch after retries'
        return self
    
    def check_amp_compliance(self) -> None:
        """
        Checks if the page is using AMP (Accelerated Mobile Pages).

        Returns:
            (SEOAnalyzer): Returns this instance.
        """
        if not self.soup:
            self.analysis['amp'] = 'Missing HTML'
            return
        
        # AMP pages often declare a lightning bolt and attribute like <html ⚡> or <html amp>
        html_tag = self.soup.find('html')
        if html_tag and ('⚡' in html_tag.attrs or 'amp' in html_tag.attrs):
            self.analysis['amp'] = 'Yes'
        else:
            # Fallback: look for canonical pointing to AMP
            link_tag = self.soup.find('link', rel='amphtml')
            self.analysis['amp'] = 'Yes' if link_tag else 'No'
    
    def _fetch_with_retry(self, url: str, retries: int = 3, timeout: int = 30, delay: float = 5.0) -> Optional[dict]:
        for attempt in range(retries):
            try:
                response = requests.get(url, timeout=timeout)
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(delay)
        return None
    
    def calculate_score(self) -> float:
        """
        Calculates an overall SEO score out of 100 based on presence of key elements.

        Return:
            int: The SEO score (1-100).
        """
        score = 0

        def score_if_present(key: str) -> float:
            value = self.analysis.get(key)
            if isinstance(value, str):
                return 10 if value != 'Missing' and value != 'Error' else 0
            elif isinstance(value, list):
                return 10 if value and value[0] != 'Missing' else 0
            return 0
        
        keys_to_check = [
            'title', 'meta_description', 'h1_tags', 'missing_alt_tags', 'canonical_url',
            'og:title', 'og:description', 'twitter:title', 'twitter:description',
            'robots_txt', 'sitemap_xml', 'favicon'
        ]

        for key in keys_to_check:
            if key == 'missing_alt_tags':
                missing = len(self.analysis.get(key, []))
                image_count: int = self.analysis.get('image_count', 0)
                
                if image_count > 0:
                    score += ((image_count - missing) * 10 / image_count)
                else:
                    score += 10
            else:
                score += score_if_present(key)
        score = round(score, 2)
        self.analysis['seo_score'] = score
        return score

    def run_analysis(self, include: int = FLAG_NONE, exclude: int = FLAG_NONE) -> Dict[str, object]:
        if not self.fetch_page():
            return {'error':'Failed to fetch page.'}

        def flag_set(flag: int):
            return include & flag == flag and exclude & flag != flag
            
        if flag_set(FLAG_TITLE):            self.analyze_title()
        if flag_set(FLAG_META_DESCRIPTION): self.analyze_meta_description()
        if flag_set(FLAG_H1_TAGS):          self.analyze_h1_tags()
        if flag_set(FLAG_ALT_TAGS):         self.analyze_alt_tags()
        if flag_set(FLAG_CANONICAL):        self.analyze_canonical()
        if flag_set(FLAG_OPENGRAPH):        self.analyze_open_graph()
        if flag_set(FLAG_TWITTER):          self.analyze_twitter_tags()
        if flag_set(FLAG_ROBOTS_TXT):       self.check_robots_txt()
        if flag_set(FLAG_SITEMAP):          self.check_sitemap()
        if flag_set(FLAG_FAVICON):          self.check_favicon()
        if flag_set(FLAG_KEYWORD_DENSITY):  self.analyze_keyword_density()
        if flag_set(FLAG_MOBILE_FRIENDLY):  self.analyze_mobile_friendly()
        if flag_set(FLAG_LINKS):            self.analyze_links()
        if flag_set(FLAG_NOFOLLOW_LINKS):   self.analyze_nofollow_links()
        if flag_set(FLAG_HREFLANG):         self.analyze_hreflang()
        if flag_set(FLAG_META_ROBOTS):      self.analyze_meta_robots()
        if flag_set(FLAG_WEBVITALS):        self.fetch_core_web_vitals()
        if flag_set(FLAG_ACCESSIBILIY):     self.analyze_accessibility()
        if flag_set(FLAG_STRUCTERED_DATA):  self.analyze_structured_data()
        if flag_set(FLAG_AMP_COMPLIANCE):   self.check_amp_compliance()

        return self.analysis

    
    def run_full_analysis(self) -> Dict[str, object]:
        """
        Performs the full SEO analysis and returns results.

        Returns:
            Dict[str, object]: The dictionary containing SEO audit results.
        """
        if not self.fetch_page():
            return {'error':'Failed to fetch page.'}
        (
            self.analyze_title() 
                .analyze_meta_description()
                .analyze_h1_tags()
                .analyze_alt_tags()
                .analyze_canonical()
                .analyze_open_graph()
                .analyze_twitter_tags()
                .check_robots_txt()
                .check_sitemap()
                .check_favicon()
                .analyze_keyword_density()
                .analyze_mobile_friendly()
                .analyze_links()
                .analyze_nofollow_links()
                .analyze_hreflang()
                .analyze_meta_robots()
                .fetch_core_web_vitals()
                .analyze_accessibility()
                .analyze_structured_data()
                .calculate_score()
        )

        return self.analysis
    


class BatchSEOAnalyzer:
    """
    Handles SEO analysis for multiple URLs.
    """

    def __init__(
            self, 
            urls: List[str], 
            google_api_key: Optional[str] = None, 
            include: Optional[int] = FLAG_ALL,
            exclude: Optional[int] = FLAG_NONE
            ) -> None:
        """
        Initializes the batch analyzer with a list of URLs.

        Args:
            urls (List[str]): A list of website URLs to analyze.
        """
        self.urls = urls
        self.google_api_key = google_api_key
        self.include = include or FLAG_ALL
        self.exclude = exclude or FLAG_NONE
        self.results: Dict[str, dict] = {}

    def run_batch_analysis(self, max_workers: int = 5) -> None:
        """
        Runs SEO analysis for all URLs and stores results.
        """
        print(f"Analyzing {len(self.urls)} URLs with {max_workers} workers ...")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {
                executor.submit(self._analyze_url, url): url for url in self.urls
            }

            for future in tqdm(as_completed(future_to_url), total=len(future_to_url), desc='Analyzing'):
                url = future_to_url[future]
                try:
                    result = future.result()
                    self.results[url] = result
                except Exception as e:
                    logging.warning(f"Failed to analyze {url}: {e}")
            for url in self.urls:
                print(f"Analyzing: {url}")
                analyzer = SEOAnalyzer(url, self.google_api_key)
                result = analyzer.run_analysis(self.include, self.exclude)
                self.results[url] = result

    def _analyze_url(self, url: str) -> dict:
        """
        Helper function to analyze a single URL.
        """
        analyzer = SEOAnalyzer(url)
        return analyzer.run_analysis(self.include, self.exclude)

    def export_all_to_json(self, directory: str) -> None:
        """
        Exports individual JSON reports for each URL.

        Args:
            directory (str): Directory to save json files in.
        """
        os.makedirs(directory, exist_ok=True)
        for url, data in self.results.items():
            domain = urlparse(url).netloc.replace('.', '_')
            filepath = os.path.join(directory, f"{domain}.json")
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=True, default=str)

    def export_combined_csv(self, filepath: str) -> None:
        """
        Exports a combined CSV file for all URLs.

        Args:
            filepath (str): Path to output CSV file.
        """
        all_keys = set()
        for result in self.results.values():
            all_keys.update(result.keys())

        all_keys = sorted(all_keys)

        with open(filepath, 'w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['URL'] + all_keys)
            for url, result in self.results.items():
                row = [url] + [json.dumps(result.get(k, '')) for k in all_keys] 
                writer.writerow(row)



if __name__ == '__main__':
    urls:List[str] = [
        'https://www.usvkautzen.at','https://pysty.dev/', 'https://nhl.com', 'https://www.hartlauer.at'
    ]
    batch = BatchSEOAnalyzer(urls, exclude=FLAG_WEBVITALS)
    batch.run_batch_analysis()
    batch.export_all_to_json('json')
    batch.export_combined_csv('reports.csv')