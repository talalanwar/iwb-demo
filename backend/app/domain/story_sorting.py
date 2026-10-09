"""Story sorting utilities for backlog order management."""


def sort_stories_by_backlog_order(stories: list) -> list:
    """Sort stories by backlog_order ascending.
    
    Args:
        stories: List of Story model instances
        
    Returns:
        Sorted list of stories
    """
    return sorted(stories, key=lambda s: s.backlog_order)
