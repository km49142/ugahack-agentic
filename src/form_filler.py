from playwright.async_api import Page, ElementHandle
from typing import Dict, Any, List, Optional
import re


class FormDetector:
    """Detect and analyze form fields on a page."""

    def __init__(self, page: Page):
        self.page = page

    async def detect_all_inputs(self) -> List[Dict[str, Any]]:
        """Detect all input fields on the page."""
        inputs = []

        # Get all input elements
        input_elements = await self.page.query_selector_all('input, textarea, select')

        for element in input_elements:
            field_info = await self._analyze_input_field(element)
            if field_info:
                inputs.append(field_info)

        return inputs

    async def _analyze_input_field(self, element: ElementHandle) -> Optional[Dict[str, Any]]:
        """Analyze a single input field to determine its purpose."""
        try:
            tag_name = await element.evaluate('el => el.tagName.toLowerCase()')
            input_type = await element.evaluate('el => el.type || "text"')
            name = await element.evaluate('el => el.name || ""')
            id_attr = await element.evaluate('el => el.id || ""')
            placeholder = await element.evaluate('el => el.placeholder || ""')
            label_text = await self._get_associated_label(element)
            required = await element.evaluate('el => el.required')

            # Determine field purpose based on attributes
            field_purpose = self._infer_field_purpose(
                name, id_attr, placeholder, label_text, input_type
            )

            # Log detected field info for debugging
            print(f"  [DEBUG] Detected field: tag='{tag_name}', type='{input_type}', name='{name}', id='{id_attr}', "
                  f"placeholder='{placeholder}', label='{label_text}', purpose='{field_purpose}'")

            return {
                'tag': tag_name,
                'type': input_type,
                'name': name,
                'id': id_attr,
                'placeholder': placeholder,
                'label': label_text,
                'required': required,
                'purpose': field_purpose,
                'selector': f'#{id_attr}' if id_attr else f'[name="{name}"]' if name else None
            }
        except Exception as e:
            print(f"Error analyzing input field: {e}")
            return None

    async def _get_associated_label(self, element: ElementHandle) -> str:
        """Get the label associated with an input field."""
        try:
            # Try to find label by 'for' attribute
            id_attr = await element.evaluate('el => el.id')
            if id_attr:
                label = await self.page.query_selector(f'label[for="{id_attr}"]')
                if label:
                    return await label.inner_text()

            # Try to find parent label
            label = await element.evaluate('''el => {
                const label = el.closest('label');
                return label ? label.innerText : '';
            }''')
            return label.strip()
        except:
            return ""

    def _infer_field_purpose(self, name: str, id_attr: str, placeholder: str,
                            label: str, input_type: str) -> str:
        """Infer the purpose of a field based on its attributes."""
        # Combine all text indicators
        combined = f"{name} {id_attr} {placeholder} {label}".lower()

        # Check for fields that need USER INPUT (yes/no questions, relocation, etc.)
        user_input_patterns = [
            (r'\bpreviously[\s_-]?worked\b|\bworked[\s_-]?for\b|\bformer[\s_-]?employee\b', 'ask_yes_no'),
            (r'\brelocate\b|\brelocation\b|\bwilling[\s_-]?to[\s_-]?relocate\b', 'ask_yes_no'),
            (r'\bsponsor\b|\bsponsorship\b|\bwork[\s_-]?authorization\b|\bvisa\b', 'ask_yes_no'),
            (r'\beligible[\s_-]?to[\s_-]?work\b|\blegal[\s_-]?to[\s_-]?work\b', 'ask_yes_no'),
        ]

        for pattern, purpose in user_input_patterns:
            if re.search(pattern, combined):
                return purpose

        # Check for fields we should SKIP (optional fields we don't have data for)
        skip_patterns = [
            r'\breferral\b',
            r'\brefer\b',
            r'\bemployee[\s_-]?referral\b',
            r'\bhow[\s_-]?did[\s_-]?you[\s_-]?hear\b',
            r'\bveteran\b',
            r'\bdisability\b',
            r'\bethnicity\b',
            r'\brace\b',
            r'\bgender\b',
        ]

        for pattern in skip_patterns:
            if re.search(pattern, combined):
                return 'skip_optional'

        # Define patterns for common fields (order matters - most specific first)
        patterns = {
            'first_name': r'\blegal[\s_-]?first\b|\bfirst[\s_-]?name\b(?!.*refer)',
            'last_name': r'\blegal[\s_-]?last\b|\blast[\s_-]?name\b(?!.*refer)',
            'middle_name': r'\bmiddle[\s_-]?name\b',
            'preferred_name': r'\bpreferred[\s_-]?name\b',
            'full_name': r'\bfull[\s_-]?name\b',
            'email': r'\bemail\b',
            'phone': r'\bphone\b|\btel\b|\bmobile\b',
            'address': r'\baddress\b|\bstreet\b|\baddress[\s_-]?line\b',
            'city': r'\bcity\b',
            'state': r'\bstate\b|\bprovince\b',
            'zip': r'\bzip\b|\bpostal\b',
            'country': r'\bcountry\b',
            'linkedin': r'\blinkedin\b',
            'github': r'\bgithub\b',
            'portfolio': r'\bportfolio\b|\bwebsite\b',
            'university': r'\buniversity\b|\bcollege\b|\bschool\b',
            'degree': r'\bdegree\b',
            'major': r'\bmajor\b|\bfield[\s_-]?of[\s_-]?study\b',
            'gpa': r'\bgpa\b',
            'graduation': r'\bgraduation\b|\bgrad[\s_-]?date\b',
            'resume': r'\bresume\b|\bcv\b',
            'cover_letter': r'\bcover[\s_-]?letter\b',
            'transcript': r'\btranscript\b',
            'start_date': r'\bstart[\s_-]?date\b',
            'end_date': r'\bend[\s_-]?date\b',
            'password': r'\bpassword\b',
        }

        # Check input type first
        if input_type == 'email':
            return 'email'
        elif input_type == 'tel':
            return 'phone'
        elif input_type == 'file':
            if 'resume' in combined or 'cv' in combined:
                return 'resume'
            elif 'cover' in combined:
                return 'cover_letter'
            elif 'transcript' in combined:
                return 'transcript'
            return 'file_upload'

        # Check patterns
        for purpose, pattern in patterns.items():
            if re.search(pattern, combined):
                return purpose

        return 'unknown'


class FormFiller:
    """Fill forms automatically based on user profile.

    If an `agent` is provided it will be used to answer open-ended or
    ambiguous questions.
    """

    def __init__(self, page: Page, profile: Dict[str, Any], agent: Optional[Any] = None):
        self.page = page
        self.profile = profile
        self.detector = FormDetector(page)
        self.agent = agent

    async def auto_fill_form(self, interactive: bool = True) -> Dict[str, Any]:
        """
        Automatically detect and fill form fields.

        Args:
            interactive: If True, ask user for yes/no questions

        Returns:
            Dictionary with fill status and unfilled fields
        """
        fields = await self.detector.detect_all_inputs()
        filled_fields = []
        unfilled_fields = []
        skipped_fields = []
        user_answered_fields = []

        for field in fields:
            try:
                # Skip optional fields we don't have data for
                if field['purpose'] == 'skip_optional':
                    skipped_fields.append(field['label'] or field['name'] or 'unknown')
                    continue

                # Ask user for yes/no questions
                if field['purpose'] == 'ask_yes_no' and interactive:
                    question_text = field['label'] or field['placeholder'] or field['name']
                    print(f"\n❓ Question: {question_text}")

                    # Detect if it's a dropdown or radio/text
                    if field['tag'] == 'select':
                        # It's a dropdown - get options
                        try:
                            element = await self.page.query_selector(field['selector'])
                            if element:
                                options_text = await element.inner_text()
                                print(f"   Options: Yes / No (or similar)")
                        except:
                            pass

                        user_input = input("   Your answer (yes/no): ").strip().lower()

                        # Try to select the appropriate option
                        if user_input in ['yes', 'y']:
                            try:
                                await self.page.select_option(field['selector'], label='Yes', timeout=2000)
                                user_answered_fields.append(question_text)
                                continue
                            except:
                                try:
                                    await self.page.select_option(field['selector'], value='Yes', timeout=2000)
                                    user_answered_fields.append(question_text)
                                    continue
                                except:
                                    pass
                        elif user_input in ['no', 'n']:
                            try:
                                await self.page.select_option(field['selector'], label='No', timeout=2000)
                                user_answered_fields.append(question_text)
                                continue
                            except:
                                try:
                                    await self.page.select_option(field['selector'], value='No', timeout=2000)
                                    user_answered_fields.append(question_text)
                                    continue
                                except:
                                    pass

                        # If selection failed, let user handle it manually
                        print(f"   ⚠️  Could not auto-select. Please select manually in the browser.")
                        unfilled_fields.append({
                            'purpose': field['purpose'],
                            'label': field['label'],
                            'name': field['name'],
                            'required': field['required']
                        })
                    else:
                        # It's a text field - just fill the answer
                        user_input = input("   Your answer: ").strip()
                        if user_input:
                            await self._fill_field(field, user_input)
                            user_answered_fields.append(question_text)
                        else:
                            # If user skipped and an agent is available, ask the agent
                            if self.agent:
                                try:
                                    resp = await self.agent.answer_question(question_text)
                                    answer = resp.get('answer') if isinstance(resp, dict) else str(resp)
                                    if answer:
                                        await self._fill_field(field, answer)
                                        user_answered_fields.append(question_text)
                                        continue
                                except Exception:
                                    pass

                            unfilled_fields.append({
                                'purpose': field['purpose'],
                                'label': field['label'],
                                'name': field['name'],
                                'required': field['required']
                            })
                    continue

                value = self._get_value_for_field(field['purpose'])

                if value and field['selector']:
                    await self._fill_field(field, value)
                    filled_fields.append(field['purpose'])
                else:
                    # Try agent for unknown or open-ended fields
                    if self.agent and field['purpose'] in ('unknown',) and field.get('label'):
                        try:
                            resp = await self.agent.answer_question(field['label'])
                            answer = resp.get('answer') if isinstance(resp, dict) else str(resp)
                            if answer and field['selector']:
                                await self._fill_field(field, answer)
                                filled_fields.append(field['purpose'])
                                continue
                        except Exception as e:
                            print(f"Agent error: {e}")

                    unfilled_fields.append({
                        'purpose': field['purpose'],
                        'label': field['label'],
                        'name': field['name'],
                        'required': field['required']
                    })
            except Exception as e:
                print(f"Error filling field {field['purpose']}: {e}")
                unfilled_fields.append(field)

        return {
            'total_fields': len(fields),
            'filled_count': len(filled_fields),
            'unfilled_count': len(unfilled_fields),
            'skipped_count': len(skipped_fields),
            'user_answered_count': len(user_answered_fields),
            'filled_fields': filled_fields,
            'unfilled_fields': unfilled_fields,
            'skipped_fields': skipped_fields,
            'user_answered_fields': user_answered_fields
        }

    def _get_value_for_field(self, field_purpose: str) -> Optional[str]:
        """Get the appropriate value from profile for a field."""
        personal_info = self.profile.get('personal_info', {})
        address = personal_info.get('address', {})

        field_mapping = {
            'first_name': personal_info.get('first_name'),
            'last_name': personal_info.get('last_name'),
            'middle_name': '',  # Most people don't have middle name
            'preferred_name': personal_info.get('first_name'),
            'full_name': f"{personal_info.get('first_name', '')} {personal_info.get('last_name', '')}".strip(),
            'email': personal_info.get('email'),
            'phone': personal_info.get('phone'),
            'address': address.get('street'),
            'city': address.get('city'),
            'state': address.get('state'),
            'zip': address.get('zip'),
            'country': address.get('country', 'USA'),
            'linkedin': personal_info.get('linkedin'),
            'github': personal_info.get('github'),
            'portfolio': personal_info.get('portfolio'),
        }

        # Get education info if available
        if self.profile.get('education'):
            latest_edu = self.profile['education'][0]
            field_mapping.update({
                'university': latest_edu.get('school'),
                'degree': latest_edu.get('degree'),
                'major': latest_edu.get('major'),
                'gpa': str(latest_edu.get('gpa', '')),
                'graduation': latest_edu.get('end_date'),
            })

        # Handle file uploads
        documents = self.profile.get('documents', {})
        field_mapping.update({
            'resume': documents.get('resume_path'),
            'cover_letter': documents.get('cover_letter_template'),
            'transcript': documents.get('transcript_path'),
        })

        return field_mapping.get(field_purpose)

    async def _fill_field(self, field: Dict[str, Any], value: str):
        """Fill a specific field based on its type."""
        selector = field['selector']

        # Check if field is visible before trying to fill
        try:
            element = await self.page.query_selector(selector)
            if not element:
                raise Exception(f"Element not found: {selector}")

            is_visible = await element.is_visible()
            if not is_visible:
                raise Exception(f"Element not visible: {selector}")

            if field['tag'] == 'select':
                # Handle dropdown
                await self.page.select_option(selector, value, timeout=5000)
            elif field['type'] == 'file':
                # Handle file upload
                if value:  # Only upload if file path exists
                    await self.page.set_input_files(selector, value, timeout=5000)
            elif field['type'] == 'checkbox':
                # Handle checkbox
                if value.lower() in ['true', 'yes', '1']:
                    await self.page.check(selector, timeout=5000)
            elif field['type'] == 'radio':
                # Handle radio button
                await self.page.check(selector, timeout=5000)
            else:
                # Handle text inputs
                await self.page.fill(selector, str(value), timeout=5000)
        except Exception as e:
            raise Exception(f"Failed to fill field {field['purpose']}: {str(e)}")
