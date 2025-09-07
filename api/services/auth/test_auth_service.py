import unittest
from unittest.mock import Mock, patch, MagicMock
from django.test import TestCase
from django.forms.models import model_to_dict
from time import time

from api.services.auth.auth_service import AuthService, AuthServiceImpl
from api.repositories.auth_repo import AuthRepository
from api.models import Account
from api.errors.common import *


class TestAuthService(TestCase):
    """Test cases for the abstract AuthService class"""
    
    def test_auth_service_is_abstract(self):
        """Test that AuthService cannot be instantiated directly"""
        with self.assertRaises(TypeError):
            AuthService()
    
    def test_verify_token_is_abstract(self):
        """Test that verifyToken is an abstract method"""
        # This is tested implicitly by the inability to instantiate AuthService
        pass
    
    def test_get_account_by_token_is_abstract(self):
        """Test that getAccountByToken is an abstract method"""
        # This is tested implicitly by the inability to instantiate AuthService
        pass


class TestAuthServiceImpl(TestCase):
    """Test cases for the AuthServiceImpl class"""
    
    def setUp(self):
        """Set up test dependencies"""
        self.auth_service = AuthServiceImpl()
        self.mock_auth_repo = Mock(spec=AuthRepository)
        self.auth_service.auth_repo = self.mock_auth_repo
        
        # Create a sample account for testing
        self.sample_account = Account(
            account_id="test123",
            username="testuser",
            email="test@example.com",
            password="hashedpassword",
            token="valid_token_123",
            token_expire=int(time()) + 3600,  # Valid for 1 hour
            is_active=True,
            is_private=True
        )
        
        self.expired_account = Account(
            account_id="test456",
            username="expireduser",
            email="expired@example.com",
            password="hashedpassword",
            token="expired_token_456",
            token_expire=int(time()) - 3600,  # Expired 1 hour ago
            is_active=True,
            is_private=True
        )
    
    def test_init(self):
        """Test AuthServiceImpl initialization"""
        service = AuthServiceImpl()
        self.assertIsInstance(service.auth_repo, AuthRepository)
    
    @patch('api.services.auth.auth_service.time')
    def test_verify_token_valid_token(self, mock_time):
        """Test verifyToken with a valid token"""
        mock_time.return_value = time()
        self.mock_auth_repo.getByToken.return_value = self.sample_account
        
        result = self.auth_service.verifyToken("valid_token_123")
        
        self.assertTrue(result)
        self.mock_auth_repo.getByToken.assert_called_once_with("valid_token_123")
    
    @patch('api.services.auth.auth_service.time')
    def test_verify_token_expired_token(self, mock_time):
        """Test verifyToken with an expired token"""
        mock_time.return_value = time()
        self.mock_auth_repo.getByToken.return_value = self.expired_account
        
        result = self.auth_service.verifyToken("expired_token_456")
        
        self.assertFalse(result)
        self.mock_auth_repo.getByToken.assert_called_once_with("expired_token_456")
    
    def test_verify_token_nonexistent_token(self):
        """Test verifyToken with a non-existent token"""
        self.mock_auth_repo.getByToken.side_effect = Account.DoesNotExist()
        
        result = self.auth_service.verifyToken("nonexistent_token")
        
        self.assertFalse(result)
        self.mock_auth_repo.getByToken.assert_called_once_with("nonexistent_token")
    
    def test_verify_token_none_token(self):
        """Test verifyToken with None token"""
        self.mock_auth_repo.getByToken.side_effect = Account.DoesNotExist()
        
        result = self.auth_service.verifyToken(None)
        
        self.assertFalse(result)
        self.mock_auth_repo.getByToken.assert_called_once_with(None)
    
    def test_verify_token_empty_string_token(self):
        """Test verifyToken with empty string token"""
        self.mock_auth_repo.getByToken.side_effect = Account.DoesNotExist()
        
        result = self.auth_service.verifyToken("")
        
        self.assertFalse(result)
        self.mock_auth_repo.getByToken.assert_called_once_with("")
    
    @patch('api.services.auth.auth_service.time')
    def test_get_account_by_token_valid_token(self, mock_time):
        """Test getAccountByToken with a valid token"""
        mock_time.return_value = time()
        self.mock_auth_repo.getByToken.return_value = self.sample_account
        
        result = self.auth_service.getAccountByToken("valid_token_123")
        
        self.assertEqual(result, self.sample_account)
        self.mock_auth_repo.getByToken.assert_called_once_with("valid_token_123")
    
    @patch('api.services.auth.auth_service.time')
    def test_get_account_by_token_expired_token(self, mock_time):
        """Test getAccountByToken with an expired token"""
        mock_time.return_value = time()
        self.mock_auth_repo.getByToken.return_value = self.expired_account
        
        result = self.auth_service.getAccountByToken("expired_token_456")
        
        self.assertIsNone(result)
        self.mock_auth_repo.getByToken.assert_called_once_with("expired_token_456")
    
    def test_get_account_by_token_nonexistent_token(self):
        """Test getAccountByToken with a non-existent token"""
        self.mock_auth_repo.getByToken.side_effect = Account.DoesNotExist()
        
        result = self.auth_service.getAccountByToken("nonexistent_token")
        
        self.assertIsNone(result)
        self.mock_auth_repo.getByToken.assert_called_once_with("nonexistent_token")
    
    def test_get_account_by_token_none_token(self):
        """Test getAccountByToken with None token"""
        self.mock_auth_repo.getByToken.side_effect = Account.DoesNotExist()
        
        result = self.auth_service.getAccountByToken(None)
        
        self.assertIsNone(result)
        self.mock_auth_repo.getByToken.assert_called_once_with(None)
    
    def test_get_account_by_token_empty_string_token(self):
        """Test getAccountByToken with empty string token"""
        self.mock_auth_repo.getByToken.side_effect = Account.DoesNotExist()
        
        result = self.auth_service.getAccountByToken("")
        
        self.assertIsNone(result)
        self.mock_auth_repo.getByToken.assert_called_once_with("")
    
    @patch('api.services.auth.auth_service.time')
    def test_verify_token_edge_case_exactly_expired(self, mock_time):
        """Test verifyToken when token expires exactly at current time"""
        current_time = time()
        mock_time.return_value = current_time
        
        # Create account with token expiring exactly now
        exactly_expired_account = Account(
            account_id="test789",
            username="exactlyexpired",
            email="exactly@example.com",
            password="hashedpassword",
            token="exactly_expired_token",
            token_expire=int(current_time),  # Expires exactly now
            is_active=True,
            is_private=True
        )
        
        self.mock_auth_repo.getByToken.return_value = exactly_expired_account
        
        result = self.auth_service.verifyToken("exactly_expired_token")
        
        # Should return True since token_expire >= current_time
        self.assertTrue(result)
    
    @patch('api.services.auth.auth_service.time')
    def test_get_account_by_token_edge_case_exactly_expired(self, mock_time):
        """Test getAccountByToken when token expires exactly at current time"""
        current_time = time()
        mock_time.return_value = current_time
        
        # Create account with token expiring exactly now
        exactly_expired_account = Account(
            account_id="test789",
            username="exactlyexpired",
            email="exactly@example.com",
            password="hashedpassword",
            token="exactly_expired_token",
            token_expire=int(current_time),  # Expires exactly now
            is_active=True,
            is_private=True
        )
        
        self.mock_auth_repo.getByToken.return_value = exactly_expired_account
        
        result = self.auth_service.getAccountByToken("exactly_expired_token")
        
        # Should return the account since token_expire >= current_time
        self.assertEqual(result, exactly_expired_account)
    
    @patch('api.services.auth.auth_service.model_to_dict')
    @patch('api.services.auth.auth_service.time')
    def test_verify_token_model_to_dict_called(self, mock_time, mock_model_to_dict):
        """Test that model_to_dict is called correctly in verifyToken"""
        mock_time.return_value = time()
        mock_model_to_dict.return_value = {'token_expire': int(time()) + 3600}
        self.mock_auth_repo.getByToken.return_value = self.sample_account
        
        result = self.auth_service.verifyToken("valid_token_123")
        
        self.assertTrue(result)
        mock_model_to_dict.assert_called_once_with(self.sample_account)
    
    @patch('api.services.auth.auth_service.model_to_dict')
    @patch('api.services.auth.auth_service.time')
    def test_get_account_by_token_model_to_dict_called(self, mock_time, mock_model_to_dict):
        """Test that model_to_dict is called correctly in getAccountByToken"""
        mock_time.return_value = time()
        mock_model_to_dict.return_value = {'token_expire': int(time()) + 3600}
        self.mock_auth_repo.getByToken.return_value = self.sample_account
        
        result = self.auth_service.getAccountByToken("valid_token_123")
        
        self.assertEqual(result, self.sample_account)
        mock_model_to_dict.assert_called_once_with(self.sample_account)


class TestAuthServiceIntegration(TestCase):
    """Integration tests for AuthService with real database interactions"""
    
    def setUp(self):
        """Set up integration test data"""
        self.auth_service = AuthServiceImpl()
        
        # Create a real account in the test database
        self.test_account = Account.objects.create(
            username="integrationtest",
            email="integration@test.com",
            password="testpassword",
            token="integration_token_123",
            token_expire=int(time()) + 3600,  # Valid for 1 hour
            is_active=True,
            is_private=True
        )
        
        # Create an expired account
        self.expired_test_account = Account.objects.create(
            username="expiredintegration",
            email="expiredintegration@test.com",
            password="testpassword",
            token="expired_integration_token",
            token_expire=int(time()) - 3600,  # Expired 1 hour ago
            is_active=True,
            is_private=True
        )
    
    def test_verify_token_integration_valid(self):
        """Integration test for verifyToken with valid token"""
        result = self.auth_service.verifyToken("integration_token_123")
        self.assertTrue(result)
    
    def test_verify_token_integration_expired(self):
        """Integration test for verifyToken with expired token"""
        result = self.auth_service.verifyToken("expired_integration_token")
        self.assertFalse(result)
    
    def test_verify_token_integration_nonexistent(self):
        """Integration test for verifyToken with non-existent token"""
        result = self.auth_service.verifyToken("nonexistent_integration_token")
        self.assertFalse(result)
    
    def test_get_account_by_token_integration_valid(self):
        """Integration test for getAccountByToken with valid token"""
        result = self.auth_service.getAccountByToken("integration_token_123")
        self.assertEqual(result.account_id, self.test_account.account_id)
        self.assertEqual(result.username, "integrationtest")
    
    def test_get_account_by_token_integration_expired(self):
        """Integration test for getAccountByToken with expired token"""
        result = self.auth_service.getAccountByToken("expired_integration_token")
        self.assertIsNone(result)
    
    def test_get_account_by_token_integration_nonexistent(self):
        """Integration test for getAccountByToken with non-existent token"""
        result = self.auth_service.getAccountByToken("nonexistent_integration_token")
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
