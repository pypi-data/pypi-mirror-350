from datetime import timedelta

from django.test import RequestFactory, TestCase
from django.utils import timezone
from djangocms_blog.models import BlogConfig, Post

from djangocms_blog_agenda.models import PostExtension
from djangocms_blog_agenda.views import AgendaArchiveView, AgendaListView


class TestAgendaListView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/")

        # Create blog config with agenda template prefix
        self.config = BlogConfig.objects.create(
            namespace="agenda",
            app_title="Agenda",
        )
        self.config.app_data.config.template_prefix = "agenda"
        self.config.save()

        # Create test posts
        now = timezone.now()

        # Past event
        self.past_post = Post.objects.create(
            title="Past Event", app_config=self.config, publish=True
        )
        self.past_post.set_current_language("en")  # Set language
        self.past_post.title = "Past Event"  # Set translated fields
        self.past_post.save()
        PostExtension.objects.create(
            post=self.past_post, event_start_date=now - timedelta(days=10)
        )

        # Future event
        self.future_post = Post.objects.create(
            title="Future Event", app_config=self.config, publish=True
        )
        self.future_post.set_current_language("en")  # Set language
        self.future_post.title = "Future Event"  # Set translated fields
        self.future_post.save()
        PostExtension.objects.create(
            post=self.future_post, event_start_date=now + timedelta(days=10)
        )

    def test_agenda_list_view_shows_upcoming_events(self):
        view = AgendaListView()
        view.request = self.request
        view.config = self.config
        view.namespace = self.config.namespace
        view.model = Post
        view.kwargs = {"only_upcoming_events": True}

        # Get queryset
        posts = view.get_queryset()

        # Should include future events, but not past events
        self.assertIn(self.future_post.title, [p.title for p in posts])
        self.assertNotIn(self.past_post.title, [p.title for p in posts])

        # Check ordering - should be ordered by start date
        event_dates = [p.extension.first().event_start_date for p in posts]
        self.assertEqual(event_dates, sorted(event_dates))

    def test_agenda_archive_view_shows_past_events(self):
        view = AgendaArchiveView()
        view.request = self.request
        view.config = self.config
        view.namespace = self.config.namespace
        view.model = Post
        view.kwargs = {"only_past_events": True}

        # Get queryset
        posts = view.get_queryset()

        # Should include past events, but not future events
        self.assertIn(self.past_post.title, [p.title for p in posts])
        self.assertNotIn(self.future_post.title, [p.title for p in posts])

        # Check ordering - should be ordered by start date in reverse
        event_dates = [p.extension.first().event_start_date for p in posts]
        self.assertEqual(event_dates, sorted(event_dates, reverse=True))

    def test_agenda_list_view_shows_ongoing_events(self):
        now = timezone.now()

        # Create an ongoing event (started 10 days ago, ends in 10 days)
        ongoing_post = Post.objects.create(
            title="Ongoing Event", app_config=self.config, publish=True
        )
        ongoing_post.set_current_language("en")
        ongoing_post.title = "Ongoing Event"
        ongoing_post.save()

        PostExtension.objects.create(
            post=ongoing_post,
            event_start_date=now - timedelta(days=10),
            event_end_date=now + timedelta(days=10),
        )

        # Initialize view
        view = AgendaListView()
        view.request = self.request
        view.config = self.config
        view.namespace = self.config.namespace
        view.model = Post
        view.kwargs = {"only_upcoming_events": True}

        # Get queryset
        posts = view.get_queryset()

        # The ongoing event should be included in upcoming events
        self.assertIn(ongoing_post.title, [p.title for p in posts])

        # Verify it appears in the correct order (between past and future events)
        event_dates = [p.extension.first().event_start_date for p in posts]
        self.assertEqual(event_dates, sorted(event_dates))

    def test_agenda_list_view_pinned_events_first(self):
        now = timezone.now()

        # Create a pinned future event
        pinned_future = Post.objects.create(
            title="Pinned Future Event", app_config=self.config, publish=True
        )
        pinned_future.set_current_language("en")
        pinned_future.title = "Pinned Future Event"
        pinned_future.save()
        PostExtension.objects.create(
            post=pinned_future, event_start_date=now + timedelta(days=5), is_pinned=True
        )

        # Initialize view
        view = AgendaListView()
        view.request = self.request
        view.config = self.config
        view.namespace = self.config.namespace
        view.model = Post
        view.kwargs = {"only_upcoming_events": True}

        # Get queryset
        posts = view.get_queryset()
        post_titles = [p.title for p in posts]

        # Pinned event should appear first, followed by other future events
        self.assertEqual(post_titles[0], "Pinned Future Event")
        self.assertIn("Future Event", post_titles[1:])

    def test_agenda_archive_view_pinned_events_not_first(self):
        now = timezone.now()

        # Create a pinned past event
        pinned_past = Post.objects.create(
            title="Pinned Past Event", app_config=self.config, publish=True
        )
        pinned_past.set_current_language("en")
        pinned_past.title = "Pinned Past Event"
        pinned_past.save()
        PostExtension.objects.create(
            post=pinned_past, event_start_date=now - timedelta(days=5), is_pinned=True
        )

        # Initialize view
        view = AgendaArchiveView()
        view.request = self.request
        view.config = self.config
        view.namespace = self.config.namespace
        view.model = Post
        view.kwargs = {"only_past_events": True}

        # Get queryset
        posts = view.get_queryset()
        post_titles = [p.title for p in posts]

        # Pinned event should not appear first
        self.assertNotEqual(post_titles[0], "Pinned Past Event")
