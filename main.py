from utils.logos import get_logos_from_websites
from utils.clusterer import Clusterer

logos, found_logo_rate = get_logos_from_websites("data/logos.parquet")

print(f"Possible logos found for {found_logo_rate * 100} % of websites.")

clusterer = Clusterer()
clusterer.cluster_logos(logos)

print(f"Logos could be downloaded for {clusterer.downloaded_logos_rate * 100} % of logos.")

clusterer.print_clusters()