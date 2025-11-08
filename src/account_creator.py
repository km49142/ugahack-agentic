from playwright.async_api import Page
from typing import Dict, Any, Optional
import re
import secrets
import string


class AccountCreator:
    """Handles automatic account creation for application portals."""

    def __init__(self, page: Page, profile: Dict[str, Any]):
        self.page = page
        self.profile = profile

    async def detect_account_creation_page(self) -> bool:
        """
        Detect if the current page is an account creation/signup page.

        Returns:
            True if on signup page, False otherwise
        """
        try:
            # Get page content
            page_text = await self.page.inner_text('body')
            page_text_lower = page_text.lower()

            # Get URL
            url = self.page.url.lower()

            # Check for signup indicators
            signup_keywords = [
                'create account',
                'sign up',
                'register',
                'new user',
                'create profile',
                'get started',
                'join us',
                'registration'
            ]

            url_indicators = ['signup', 'register', 'create-account', 'join']

            # Check URL
            for indicator in url_indicators:
                if indicator in url:
                    return True

            # Check page content
            for keyword in signup_keywords:
                if keyword in page_text_lower:
                    # Additional confirmation - look for password fields
                    password_fields = await self.page.query_selector_all('input[type="password"]')
                    if len(password_fields) >= 2:  # Likely has "password" and "confirm password"
                        return True
                    if len(password_fields) >= 1:
                        # Check for username/email field
                        has_email = await self.page.query_selector('input[type="email"]')
                        has_username = await self.page.query_selector('input[name*="username"]')
                        if has_email or has_username:
                            return True

            return False
        except Exception as e:
            print(f"Error detecting account creation page: {e}")
            return False

    async def detect_login_page(self) -> bool:
        """
        Detect if the current page is a login page.

        Returns:
            True if on login page, False otherwise
        """
        try:
            page_text = await self.page.inner_text('body')
            page_text_lower = page_text.lower()
            url = self.page.url.lower()

            # Check for login indicators
            login_keywords = ['log in', 'login', 'sign in', 'signin']
            url_indicators = ['login', 'signin', 'auth']

            # Check URL
            for indicator in url_indicators:
                if indicator in url:
                    return True

            # Check page content
            for keyword in login_keywords:
                if keyword in page_text_lower:
                    # Confirm with password field
                    password_fields = await self.page.query_selector_all('input[type="password"]')
                    if len(password_fields) >= 1:
                        return True

            return False
        except Exception as e:
            print(f"Error detecting login page: {e}")
            return False

    def generate_username(self) -> str:
        """
        Generate a username based on user's name and random suffix.

        Returns:
            Generated username
        """
        first_name = self.profile.get('personal_info', {}).get('first_name', 'user')
        last_name = self.profile.get('personal_info', {}).get('last_name', '')

        # Create base username
        base = f"{first_name.lower()}{last_name.lower()}"
        # Remove spaces and special characters
        base = re.sub(r'[^a-z0-9]', '', base)

        # Add random suffix
        suffix = ''.join(secrets.choice(string.digits) for _ in range(4))

        return f"{base}{suffix}"

    def generate_password(self, length: int = 16) -> str:
        """
        Generate a secure password.

        Args:
            length: Length of password

        Returns:
            Generated password
        """
        # Ensure password meets common requirements:
        # - At least one uppercase
        # - At least one lowercase
        # - At least one digit
        # - At least one special character

        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"

        while True:
            password = ''.join(secrets.choice(alphabet) for _ in range(length))

            # Verify it meets requirements
            if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
                and any(c in "!@#$%^&*" for c in password)):
                return password

    async def create_account(self) -> Dict[str, Any]:
        """
        Automatically create an account on the current page.

        Returns:
            Dictionary with username, password, and success status
        """
        try:
            print("\n🔐 Detecting account creation form...")

            # Get all input fields
            inputs = await self.page.query_selector_all('input')

            # Find relevant fields
            email_field = None
            username_field = None
            password_fields = []
            first_name_field = None
            last_name_field = None

            for input_elem in inputs:
                input_type = await input_elem.get_attribute('type')
                input_name = (await input_elem.get_attribute('name') or '').lower()
                input_id = (await input_elem.get_attribute('id') or '').lower()
                placeholder = (await input_elem.get_attribute('placeholder') or '').lower()

                combined = f"{input_name} {input_id} {placeholder}"

                # Detect email field
                if input_type == 'email' or 'email' in combined:
                    email_field = input_elem

                # Detect username field
                elif 'username' in combined or 'userid' in combined:
                    username_field = input_elem

                # Detect password fields
                elif input_type == 'password':
                    password_fields.append(input_elem)

                # Detect name fields
                elif 'first' in combined and 'name' in combined:
                    first_name_field = input_elem
                elif 'last' in combined and 'name' in combined:
                    last_name_field = input_elem

            # Generate credentials
            email = self.profile.get('personal_info', {}).get('email', '')
            username = self.generate_username()
            password = self.generate_password()

            print(f"\n✓ Generated credentials:")
            print(f"  Email: {email}")
            print(f"  Username: {username}")
            print(f"  Password: {password}")

            # Fill fields
            filled_fields = []

            # Fill email
            if email_field and email:
                await email_field.fill(email)
                filled_fields.append('email')
                print(f"  ✓ Filled email field")

            # Fill username
            if username_field:
                await username_field.fill(username)
                filled_fields.append('username')
                print(f"  ✓ Filled username field")

            # Fill password fields
            for i, pwd_field in enumerate(password_fields):
                await pwd_field.fill(password)
                filled_fields.append(f'password_{i+1}')
                print(f"  ✓ Filled password field {i+1}")

            # Fill name fields
            if first_name_field:
                first_name = self.profile.get('personal_info', {}).get('first_name', '')
                if first_name:
                    await first_name_field.fill(first_name)
                    filled_fields.append('first_name')
                    print(f"  ✓ Filled first name field")

            if last_name_field:
                last_name = self.profile.get('personal_info', {}).get('last_name', '')
                if last_name:
                    await last_name_field.fill(last_name)
                    filled_fields.append('last_name')
                    print(f"  ✓ Filled last name field")

            # Store credentials in profile
            if 'credentials' not in self.profile:
                self.profile['credentials'] = {}

            # Store by domain
            from urllib.parse import urlparse
            domain = urlparse(self.page.url).netloc

            self.profile['credentials'][domain] = {
                'email': email,
                'username': username,
                'password': password
            }

            return {
                'success': True,
                'email': email,
                'username': username,
                'password': password,
                'filled_fields': filled_fields,
                'domain': domain
            }

        except Exception as e:
            print(f"\n✗ Error creating account: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    async def find_create_account_button(self) -> Optional[Any]:
        """Find and click the 'Create Account' button."""
        create_account_selectors = [
            'button:has-text("Create Account")',
            'button:has-text("Sign Up")',
            'button:has-text("Register")',
            'button:has-text("Submit")',
            'input[type="submit"]',
            'button[type="submit"]',
            'a:has-text("Create Account")',
            '[role="button"]:has-text("Sign Up")'
        ]

        for selector in create_account_selectors:
            try:
                element = await self.page.query_selector(selector)
                if element:
                    return element
            except:
                continue

        return None

    async def login_with_credentials(self, domain: str) -> Dict[str, Any]:
        """
        Login using stored credentials for a domain.

        Args:
            domain: Domain name

        Returns:
            Dictionary with login status
        """
        try:
            credentials = self.profile.get('credentials', {}).get(domain)

            if not credentials:
                return {
                    'success': False,
                    'error': 'No stored credentials for this domain'
                }

            print(f"\n🔐 Logging in with stored credentials...")

            # Find login fields
            email_field = await self.page.query_selector('input[type="email"]')
            username_field = await self.page.query_selector('input[name*="username"]')
            password_field = await self.page.query_selector('input[type="password"]')

            # Fill email or username
            if email_field:
                await email_field.fill(credentials['email'])
                print(f"  ✓ Filled email: {credentials['email']}")
            elif username_field:
                await username_field.fill(credentials['username'])
                print(f"  ✓ Filled username: {credentials['username']}")

            # Fill password
            if password_field:
                await password_field.fill(credentials['password'])
                print(f"  ✓ Filled password")

            return {
                'success': True,
                'email': credentials['email'],
                'username': credentials.get('username')
            }

        except Exception as e:
            print(f"\n✗ Error during login: {e}")
            return {
                'success': False,
                'error': str(e)
            }
