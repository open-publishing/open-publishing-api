"""Unit tests for testing authentication."""
import os
from unittest import TestCase
from nose.plugins.attrib import attr
from open_publishing.gjp import AuthContext, AuthFailedException
import open_publishing as op


class TestAuthentification(TestCase):
    """Simple Test."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'APIHOST' not in os.environ:
            raise Exception("APIHOST not set in environment.")
        self.api_host = os.environ['APIHOST']

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @attr("simple")
    def test_auth_world(self):
        """Test authentification as user with correct credentials."""
        auth_context = AuthContext(api_host=self.api_host)
        auth_context.auth(realm_id=1)
        self.assertTrue(auth_context.authenticated)
        self.assertTrue(isinstance(auth_context.auth_token, str))

    @attr("simple")
    def test_auth_user_correct(self):
        """Test authentification as user with correct credentials."""
        auth_context = AuthContext(api_host=self.api_host)
        auth_context.auth(email='jm@grin.com', password='123', realm_id=1)
        self.assertTrue(auth_context.authenticated)
        self.assertTrue(isinstance(auth_context.auth_token, str))

    @attr("simple")
    def test_auth_user_wrong(self):
        """Test authentification as user with wrong credentials."""
        auth_context = AuthContext(api_host=self.api_host)
        with self.assertRaises(AuthFailedException):
            auth_context.auth(email='jm@grin.com', password='456', realm_id=1)
        self.assertFalse(auth_context.authenticated)

    @attr("simple")
    def test_auth_api_key_correct(self):
        """Test authentification with correct api_key."""
        auth_context = AuthContext(api_host=self.api_host)
        auth_context.auth(api_key='1_1R_3')
        self.assertTrue(auth_context.authenticated)
        self.assertTrue(isinstance(auth_context.auth_token, str))

    @attr("simple")
    def test_auth_api_key_wrong(self):
        """Test authentification with wrong api_key."""
        auth_context = AuthContext(api_host=self.api_host)
        with self.assertRaises(AuthFailedException):
            auth_context.auth(api_key='WRONG')
        self.assertFalse(auth_context.authenticated)

    @attr("simple")
    def test_auth_app_secret_correct(self):
        """Test authentification with correct app_secret."""
        auth_context = AuthContext(api_host=self.api_host)
        auth_context.auth(app_id=100, app_secret="app-secret-100")
        self.assertTrue(auth_context.authenticated)
        self.assertTrue(isinstance(auth_context.auth_token, str))

    @attr("simple")
    def test_auth_app_secret_wrong(self):
        """Test authentification with correct app_secret."""
        auth_context = AuthContext(api_host=self.api_host)
        with self.assertRaises(AuthFailedException):
            auth_context.auth(app_id=100, app_secret='app-secret-101')
        self.assertFalse(auth_context.authenticated)

    @attr("simple")
    def test_context_auth_traditional(self):
        """Test authentification within context - the traditional way."""
        with op.context(api_key='1_1R_3', host=self.api_host) as ctx:
            self.assertEqual(ctx.me.user_name, 'August Admin')
            self.assertEqual(ctx.me.realm_id, 1)
            self.assertEqual(ctx.me.realm_name, 'grin')
            self.assertEqual(ctx.me.app_name, None)
            self.assertEqual(ctx.me.app_id, None)

    @attr("simple")
    def test_context_auth_api_key(self):
        """Test authentification within context with api-key."""
        with op.context(host=self.api_host) as ctx:
            ctx.auth(api_key='1_1R_3')
            self.assertEqual(ctx.me.user_name, 'August Admin')
            self.assertEqual(ctx.me.realm_id, 1)
            self.assertEqual(ctx.me.realm_name, 'grin')
            self.assertEqual(ctx.me.app_id, None)
            self.assertEqual(ctx.me.app_name, None)

    @attr("simple")
    def test_context_auth_user_name_password(self):
        """Test authentification within context with username/password."""
        with op.context(host=self.api_host) as ctx:
            ctx.auth(email='admin@grin.com', password='123', realm_id=1)
            self.assertEqual(ctx.me.user_name, 'August Admin')
            self.assertEqual(ctx.me.realm_id, 1)
            self.assertEqual(ctx.me.realm_name, 'grin')
            self.assertEqual(ctx.me.app_id, None)
            self.assertEqual(ctx.me.app_name, None)

    @attr("simple")
    def test_context_auth_app(self):
        """Test authentification within context with app_id and app_secret."""
        with op.context(host=self.api_host) as ctx:
            ctx.auth(app_id=100, app_secret='app-secret-100')
            self.assertEqual(ctx.me.user_name, None)
            self.assertEqual(ctx.me.realm_id, None)
            self.assertEqual(ctx.me.realm_name, None)
            self.assertEqual(ctx.me.app_id, 100)
            self.assertEqual(ctx.me.app_name, "Parkteam")

    @attr("simple")
    def test_context_auth_world(self):
        """Test authentification within context with app_id and app_secret."""
        with op.context(host=self.api_host) as ctx:
            ctx.auth(realm_id=1)
            self.assertEqual(ctx.me.user_name, None)
            self.assertEqual(ctx.me.realm_id, 1)
            self.assertEqual(ctx.me.realm_name, 'grin')
            self.assertEqual(ctx.me.app_id, None)
            self.assertEqual(ctx.me.app_name, None)
