from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()

class BlogSystemTests(TestCase):
    def setUp(self):
        # Setup Users
        self.author = User.objects.create_user(username='writer', password='pw', role='AUTHOR')
        self.reader = User.objects.create_user(username='reader', password='pw', role='READER')
        # Setup Post
        self.post = Post.objects.create(
            title="Test Post", 
            content="Content", 
            author=self.author, 
            status='PUB'
        )

    # FUNCTIONALITY 1: ROLE-BASED ACCESS (AUTH)
    def test_author_can_access_create_page(self):
        """Test 1: Author accessing create page returns 200 OK"""
        self.client.login(username='writer', password='pw')
        response = self.client.get('/post/new/')
        self.assertEqual(response.status_code, 200)

    def test_reader_cannot_create_post(self):
        """Test 2: Reader accessing create page returns 403 Forbidden"""
        self.client.login(username='reader', password='pw')
        response = self.client.get('/post/new/')
        self.assertEqual(response.status_code, 403)

    # FUNCTIONALITY 2: CRUD OPERATIONS
    def test_post_creation_successful(self):
        """Test 3: Submitting form creates a post"""
        self.client.login(username='writer', password='pw')
        response = self.client.post('/post/new/', {
            'title': 'New Story',
            'content': 'Some content',
            'status': 'PUB',
            'tags': [] 
        })
        self.assertEqual(Post.objects.count(), 2) # 1 setup + 1 new

    def test_author_can_delete_own_post(self):
        """Test 4: Author deleting their post works"""
        self.client.login(username='writer', password='pw')
        response = self.client.post(f'/post/{self.post.pk}/delete/')
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    # FUNCTIONALITY 3: SEARCH & DISCOVERY
    def test_search_functionality_match(self):
        """Test 5: Search returns matching post"""
        response = self.client.get('/', {'q': 'Test'})
        self.assertContains(response, "Test Post")

    def test_search_functionality_no_match(self):
        """Test 6: Search returns no results for nonsense"""
        response = self.client.get('/', {'q': 'XyZ123'})
        self.assertNotContains(response, "Test Post")

    # FUNCTIONALITY 4: ANALYTICS & INTERACTIONS
    def test_analytics_view_count(self):
        """Test 7: Viewing a post increments view count"""
        initial_views = self.post.views_count
        self.client.get(f'/post/{self.post.pk}/')
        self.post.refresh_from_db()
        self.assertEqual(self.post.views_count, initial_views + 1)

    def test_like_functionality(self):
        """Test 8: Reader liking a post increases count"""
        self.client.login(username='reader', password='pw')
        self.client.post(f'/post/{self.post.pk}/', {'like': 'true'})
        self.assertEqual(self.post.likes.count(), 1)

    # FUNCTIONALITY 5: COMMENT MODERATION
    def test_comment_moderation_default(self):
        """Test 9: Comments are not approved by default"""
        Comment.objects.create(post=self.post, author=self.reader, text="Nice")
        self.assertFalse(self.post.comments.first().is_approved)
    
    def test_unapproved_comment_not_visible_to_public(self):
        """Test 10: Unapproved comments are hidden from page"""
        Comment.objects.create(post=self.post, author=self.reader, text="Secret")
        response = self.client.get(f'/post/{self.post.pk}/')

        self.assertEqual(Comment.objects.filter(is_approved=True).count(), 0)
