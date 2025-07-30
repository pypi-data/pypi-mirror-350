"""Crew for selecting wiki articles."""

from ..agents import WikiSelectorAgent
from .base import BaseCrew


class WikiSelectorCrew(BaseCrew):
    """Crew for selecting wiki articles to update."""

    def __init__(self):
        """Initialize wiki selector crew."""
        super().__init__()
        self.selector = WikiSelectorAgent()
        self.agents = [self.selector]

    def _execute(self, diff: str, wiki_files: list[str]) -> list[str]:
        """Execute wiki article selection."""
        from .. import logger

        logger.info(f"🗂️ Starting wiki selection from {len(wiki_files)} available articles")

        task = self.selector.create_task(diff, wiki_files=wiki_files)
        crew = self._create_crew([task])

        logger.info("🎯 Kicking off wiki selector crew...")
        result = crew.kickoff()
        logger.info("✨ Wiki selector crew completed")
        logger.debug(f"Raw wiki selector result: {result}")

        # Handle None result (error case)
        if result is None:
            logger.warning("Wiki selector returned None - likely due to an error")
            return []

        # Extract raw output from CrewOutput object
        result_str = str(result.raw) if hasattr(result, "raw") else str(result)

        logger.debug(f"Extracted wiki selector result string: {result_str}")

        # Handle string output from CrewAI
        if result_str:
            # Parse the output to extract selected articles
            import json
            import re

            # Try to parse as JSON first
            try:
                # Remove any markdown code blocks around JSON
                json_match = re.search(r"```(?:json)?\n(.*?)\n```", result_str, re.DOTALL)
                json_str = json_match.group(1) if json_match else result_str

                # Parse JSON
                parsed = json.loads(json_str)
                if isinstance(parsed, dict) and "selected_articles" in parsed:
                    selected = parsed["selected_articles"]
                    # Filter to only include valid wiki files
                    filtered = [f for f in selected if f in wiki_files]
                    logger.debug(f"JSON parsed articles: {selected}, filtered: {filtered}")
                    return filtered
                elif isinstance(parsed, list):
                    # Direct list of articles
                    filtered = [f for f in parsed if f in wiki_files]
                    logger.debug(f"JSON list articles: {parsed}, filtered: {filtered}")
                    return filtered
            except (json.JSONDecodeError, AttributeError):
                # Not JSON, fall back to regex parsing
                # Look for list patterns in the output
                matches = re.findall(r'["\']([A-Za-z-]+\.md)["\']', result_str)
                if matches:
                    filtered = [m for m in matches if m in wiki_files]
                    logger.debug(f"Regex matches: {matches}, filtered: {filtered}")
                    return filtered
                # Fallback: look for wiki file names mentioned in the text
                selected = []
                for wiki_file in wiki_files:
                    if wiki_file in result_str:
                        selected.append(wiki_file)
                logger.debug(f"Fallback selected: {selected}")
                return selected

        # If result has pydantic attribute (future compatibility)
        if hasattr(result, "pydantic"):
            selected = result.pydantic.selected_articles
            logger.debug(f"Selected articles from pydantic: {selected}")
            return selected

        logger.debug("No articles selected")
        return []

    def _handle_error(self, error: Exception) -> list[str]:
        """Handle selection errors."""
        return []
