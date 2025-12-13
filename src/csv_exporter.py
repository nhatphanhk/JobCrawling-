"""
CSV export functionality for Facebook posts
"""
import logging
import csv
from typing import List, Dict
from pathlib import Path
from datetime import datetime

from .config import CSV_DELIMITER, CSV_ENCODING, CSV_COLUMNS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CSVExporter:
    """
    Exports Facebook posts to CSV format
    """

    def __init__(self, output_dir: Path = None):
        """
        Initialize the CSV exporter

        Args:
            output_dir: Directory to save CSV files
        """
        from .config import OUTPUT_DIR
        self.output_dir = output_dir or OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_posts(
        self,
        posts: List[Dict],
        filename: str = None,
        custom_columns: List[str] = None
    ) -> Path:
        """
        Export posts to CSV file

        Args:
            posts: List of post dictionaries
            filename: Custom filename (without extension)
            custom_columns: Custom CSV columns

        Returns:
            Path to the created CSV file
        """
        if not posts:
            logger.warning("No posts to export")
            return None

        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"facebook_posts_{timestamp}"

        # Ensure .csv extension
        if not filename.endswith(".csv"):
            filename += ".csv"

        csv_path = self.output_dir / filename
        columns = custom_columns or CSV_COLUMNS

        try:
            with open(csv_path, "w", newline="", encoding=CSV_ENCODING) as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=columns, delimiter=CSV_DELIMITER)
                writer.writeheader()

                for post in posts:
                    # Only include columns that exist in the post data
                    row = {col: post.get(col, "") for col in columns}
                    writer.writerow(row)

            logger.info(f"Exported {len(posts)} posts to {csv_path}")
            return csv_path

        except Exception as e:
            logger.error(f"Error exporting posts to CSV: {e}")
            raise

    def export_posts_by_keyword(
        self,
        posts: List[Dict],
        keyword_column: str = "highlighted_text"
    ) -> Dict[str, Path]:
        """
        Export posts to separate CSV files by keyword

        Args:
            posts: List of post dictionaries
            keyword_column: Column name containing highlighted keywords

        Returns:
            Dictionary mapping keywords to CSV file paths
        """
        if not posts:
            logger.warning("No posts to export")
            return {}

        # Group posts by keywords
        keyword_posts = {}
        for post in posts:
            highlighted = post.get(keyword_column, "")
            if highlighted:
                # Use first few words as keyword group
                key = highlighted.split()[0][:20] if highlighted else "unknown"
                if key not in keyword_posts:
                    keyword_posts[key] = []
                keyword_posts[key].append(post)

        # Export each group
        exported_files = {}
        for keyword, group_posts in keyword_posts.items():
            safe_filename = "".join(c if c.isalnum() else "_" for c in keyword)
            csv_path = self.export_posts(group_posts, filename=f"posts_{safe_filename}")
            if csv_path:
                exported_files[keyword] = csv_path

        logger.info(f"Exported posts to {len(exported_files)} files by keyword")
        return exported_files

    def append_to_csv(
        self,
        posts: List[Dict],
        filepath: Path,
        custom_columns: List[str] = None
    ) -> None:
        """
        Append posts to an existing CSV file

        Args:
            posts: List of post dictionaries
            filepath: Path to CSV file
            custom_columns: Custom CSV columns
        """
        if not posts:
            logger.warning("No posts to append")
            return

        columns = custom_columns or CSV_COLUMNS
        filepath = Path(filepath)

        try:
            file_exists = filepath.exists()

            with open(filepath, "a", newline="", encoding=CSV_ENCODING) as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=columns, delimiter=CSV_DELIMITER)

                if not file_exists:
                    writer.writeheader()

                for post in posts:
                    row = {col: post.get(col, "") for col in columns}
                    writer.writerow(row)

            logger.info(f"Appended {len(posts)} posts to {filepath}")

        except Exception as e:
            logger.error(f"Error appending to CSV: {e}")
            raise

    def get_output_dir(self) -> Path:
        """
        Get the output directory path

        Returns:
            Path to output directory
        """
        return self.output_dir
