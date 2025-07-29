from django.db.models import Q
from django.utils import timezone


upcoming_events_query = (
    (
        Q(extension__event_end_date__isnull=True)
        & Q(extension__event_start_date__gte=timezone.now())
    )
    | (
        Q(extension__event_end_date__isnull=False)
        & Q(extension__event_end_date__gte=timezone.now())
    )
    | (  # Include events that have upcoming occurrences
        Q(extension__recurrences__isnull=False)
        & Q(extension__recurrences_end_date__gte=timezone.now())
    )
)

past_events_query = (
    Q(extension__event_end_date__isnull=True)
    & Q(extension__event_start_date__lt=timezone.now())
) | (
    Q(extension__event_end_date__isnull=False)
    & Q(extension__event_end_date__lt=timezone.now())
)


def add_recurrent_posts(qs, reverse=False, after=None):
    """Return a list containing all posts from the given quersyet and a clone post
    for each post that have recurring occurrences.
    """
    posts_with_recurrences = []

    for object in qs:
        if object.extension.exists():
            post_event = object.extension.first()
            if post_event.recurrences:
                posts_with_recurrences.extend(post_event.get_post_occurrences(after))
            else:
                # If this post has no recurrences, add the post to the list
                posts_with_recurrences.append(object)

    def get_sort_key(item):
        # Sort first by is_pinned (True comes first), then by date
        is_pinned = not item.extension.first().is_pinned
        start_date = getattr(
            item, "occurrence", item.extension.first().event_start_date
        )
        return (is_pinned, start_date)

    posts_with_recurrences.sort(key=get_sort_key, reverse=reverse)
    return posts_with_recurrences


def is_infinite_recurrence(recurrences) -> bool:
    return any([rule.count is rule.until is None for rule in recurrences.rrules])
