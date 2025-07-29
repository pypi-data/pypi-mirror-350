import argparse
from pyseoa.analyzer import BatchSEOAnalyzer
import os

def main():
    print('x')
    parser = argparse.ArgumentParser('Run SEO Analysis on one or more URLs')
    parser.add_argument('urls', nargs='*', help='List of URLs to analyze')
    parser.add_argument('-f', '--file', help='Path to text or CSV file containing URLs')
    parser.add_argument('-o', '--out', default='seo_reports', help='Output directory')
    parser.add_argument('-c', '--csv', default='seo_summary.csv', help='Combined CSV export path')
    parser.add_argument('-w', '--workers', default=3, help='Number of threads')

    args = parser.parse_args()

    # Load URLs from file if provided
    urls = args.urls
    if args.file:
        with open(args.file, 'r') as f:
            urls.extend([line.strip() for line in f if line.strip()])
    print(urls)
    if not urls:
        print('No urls provided.')
        return
    
    # Run batch analysis
    batch = BatchSEOAnalyzer(urls)
    batch.run_batch_analysis(max_workers=args.workers)
    os.makedirs(args.out, exist_ok=True)
    batch.export_all_to_json(args.out)
    batch.export_combined_csv(args.csv)
    print(f"\nAnalysis complete. JSON reports in '{args.out}', summary CSV at '{args.csv}")
    



if __name__ == '__main__':
    main()