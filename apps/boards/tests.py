from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Board, Post, PostReply

User = get_user_model()


class PostModelTest(TestCase):
    """게시글 모델 테스트"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        self.board = Board.objects.create(
            name='공지사항',
            board_type=Board.BoardType.NOTICE
        )

        self.post = Post.objects.create(
            board=self.board,
            author=self.user,
            title='Test Post',
            content='Test content'
        )

    def test_post_creation(self):
        """게시글 생성 테스트"""
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.board, self.board)
        self.assertEqual(self.post.author, self.user)

    def test_post_reply_creation(self):
        """답글 생성 테스트"""
        reply = PostReply.objects.create(
            post=self.post,
            author=self.user,
            content='Test reply'
        )
        self.assertEqual(reply.post, self.post)
        self.assertEqual(self.post.admin_replies.count(), 1)
